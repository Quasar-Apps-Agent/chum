// WOOL SPIKE 001 · crafted-world surface test
// Wrap diffuse + fresnel fuzz approximating fiber backscatter on boiled wool.
shader_type spatial;
render_mode diffuse_burley, specular_schlick_ggx;

uniform vec4 albedo : source_color = vec4(0.34, 0.26, 0.17, 1.0);
uniform vec4 fuzz_color : source_color = vec4(0.86, 0.77, 0.60, 1.0);
uniform float fuzz_strength : hint_range(0.0, 2.0) = 0.8;
uniform float fuzz_power : hint_range(0.5, 8.0) = 2.8;
uniform float wool_roughness : hint_range(0.0, 1.0) = 0.96;
uniform float weave_scale = 34.0;

float hash3(vec3 p) {
	return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453);
}

void fragment() {
	float n = hash3(floor(NODE_POSITION_WORLD * 0.0 + VERTEX * weave_scale));
	ALBEDO = albedo.rgb * (0.90 + 0.10 * n);
	ROUGHNESS = wool_roughness;
	SPECULAR = 0.12;
}

void light() {
	float ndl = dot(NORMAL, LIGHT);
	float wrap = clamp((ndl + 0.4) / 1.4, 0.0, 1.0);
	DIFFUSE_LIGHT += wrap * ATTENUATION * LIGHT_COLOR * ALBEDO;
	float fres = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), fuzz_power);
	float lit = max(ndl * 0.5 + 0.5, 0.0);
	DIFFUSE_LIGHT += fres * fuzz_strength * lit * ATTENUATION * LIGHT_COLOR * fuzz_color.rgb;
}
