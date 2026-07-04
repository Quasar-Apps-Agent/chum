// TAPE WORLD v0 · the artifact pipeline as a surface
// Chroma shift, scanlines, noise, tracking band, vignette. Generation scales
// the damage; the TBC steadies it. Applied to any screen that plays tape.
shader_type spatial;
render_mode unshaded;

uniform sampler2D tape_tex : source_color, filter_nearest;
uniform float generation : hint_range(0.0, 2.0) = 0.0;
uniform float tbc_on : hint_range(0.0, 1.0) = 0.0;
uniform float photo_safe : hint_range(0.0, 1.0) = 0.0;

float hash2(vec2 p) {
	return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void fragment() {
	vec2 uv = UV;
	float t = TIME;
	float g = generation;
	float steady = 1.0 - 0.7 * tbc_on;

	// time-base wobble
	uv.x += steady * (0.0012 + 0.0022 * g) * sin(t * 13.0 + uv.y * 42.0);

	// chroma separation
	float ca = 0.0012 + 0.0024 * g;
	vec3 col;
	col.r = texture(tape_tex, uv + vec2(ca, 0.0)).r;
	col.g = texture(tape_tex, uv).g;
	col.b = texture(tape_tex, uv - vec2(ca, 0.0)).b;

	// scanlines
	col *= 0.88 + 0.12 * sin(uv.y * 480.0);

	// noise floor
	float n = hash2(uv * (200.0 + 40.0 * g) + vec2(t * 61.0, t * 47.0));
	col += (n - 0.5) * (0.03 + 0.06 * g) * steady * (1.0 - 0.5 * photo_safe);

	// dot crawl along edges
	float crawl = sin(uv.x * 320.0 + t * 60.0) * sin(uv.y * 240.0);
	col += crawl * 0.014 * (0.5 + g) * steady * (1.0 - photo_safe);

	// tracking band, rolling
	float bp = fract(t * (0.05 + 0.05 * g));
	float band = exp(-pow((uv.y - bp) * 26.0, 2.0));
	col += band * 0.16 * g * steady * (1.0 - photo_safe);

	// head-switch tear at the bottom
	if (uv.y > 0.97 && photo_safe < 0.5) {
		col *= 0.6 + 0.4 * step(0.5, hash2(vec2(floor(uv.x * 40.0), floor(t * 12.0))));
	}

	// vignette
	col *= smoothstep(0.95, 0.4, length(uv - vec2(0.5)));

	ALBEDO = col;
}
