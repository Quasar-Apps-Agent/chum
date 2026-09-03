class_name PropKit
extends RefCounted
## The art pass, as code. The building was greyboxed in flat StandardMaterial3D;
## this library gives every surface real relief (procedural normal + roughness
## maps, no imported textures) and turns the hero props from boxes into meshes.
## All materials are cached and shared, so a hundred walls cost one material.
## Node structure, collisions, and the SubViewport feed are never touched by this
## file — callers keep their own bodies and only borrow the looks.

const OCHRE := Color(0.89, 0.64, 0.24)

static var _mats: Dictionary = {}
static var _noise_cache: Dictionary = {}


## ---- procedural surface generation ------------------------------------------

static func _noise_tex(nseed: int, freq: float, as_normal: bool, bump: float = 1.0) -> NoiseTexture2D:
	var key := "%d:%f:%s:%f" % [nseed, freq, str(as_normal), bump]
	if _noise_cache.has(key):
		return _noise_cache[key]
	var fn := FastNoiseLite.new()
	fn.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	fn.seed = nseed
	fn.frequency = freq
	fn.fractal_octaves = 4
	var tex := NoiseTexture2D.new()
	tex.width = 256
	tex.height = 256
	tex.seamless = true
	tex.noise = fn
	tex.as_normal_map = as_normal
	if as_normal:
		tex.bump_strength = bump
	_noise_cache[key] = tex
	return tex


## Real scanned PBR (CC0, Poly Haven, assets/textures). Triplanar world-space
## mapping so procedurally-sized boxes tile honestly. Falls back to the
## procedural surface if the files are absent (headless soaks, trimmed zips).
static func _pbr(id: String, slug: String, tint: Color, per_meter: float, fallback: Callable) -> StandardMaterial3D:
	if _mats.has(id):
		return _mats[id]
	var base := "res://assets/textures/%s_" % slug
	if not ResourceLoader.exists(base + "diff_1k.jpg"):
		return fallback.call()
	var m := StandardMaterial3D.new()
	m.albedo_texture = load(base + "diff_1k.jpg")
	m.albedo_color = tint
	if ResourceLoader.exists(base + "nor_1k.jpg"):
		m.normal_enabled = true
		m.normal_texture = load(base + "nor_1k.jpg")
		m.normal_scale = 0.85
	if ResourceLoader.exists(base + "rough_1k.jpg"):
		m.roughness_texture = load(base + "rough_1k.jpg")
		m.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
	m.roughness = 1.0
	m.uv1_triplanar = true
	m.uv1_scale = Vector3.ONE * per_meter
	_mats[id] = m
	return m


## A physically-lit surface: base tint, a normal map for tactile relief, and a
## roughness map so highlights break up instead of reading as one plastic sheet.
static func _surface(id: String, tint: Color, rough: float, metalness: float, nseed: int, freq: float, bump: float, uv: float, grain_y := 1.0) -> StandardMaterial3D:
	if _mats.has(id):
		return _mats[id]
	var m := StandardMaterial3D.new()
	m.albedo_color = tint
	m.metallic = metalness
	m.roughness = rough
	m.normal_enabled = true
	m.normal_texture = _noise_tex(nseed, freq, true, bump)
	m.normal_scale = 1.0
	m.roughness_texture = _noise_tex(nseed + 7, freq * 0.6, false)
	m.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_GRAYSCALE
	m.ao_enabled = false
	# grain_y stretches the pattern along one axis for wood grain / brushed metal
	m.uv1_scale = Vector3(uv, uv * grain_y, uv)
	_mats[id] = m
	return m


## ---- named materials --------------------------------------------------------

static func plaster() -> StandardMaterial3D:
	## scanned worn plaster, tinted down: this building is lit in pools
	return _pbr("plaster", "worn_cracked_plaster", Color(0.62, 0.56, 0.46), 0.55,
		func() -> StandardMaterial3D: return _surface("plaster_p", Color(0.33, 0.30, 0.24), 0.94, 0.0, 11, 0.9, 0.5, 2.2))


static func concrete() -> StandardMaterial3D:
	return _pbr("concrete", "concrete_floor_worn_001", Color(0.5, 0.47, 0.42), 0.4,
		func() -> StandardMaterial3D: return _surface("concrete_p", Color(0.17, 0.15, 0.12), 0.97, 0.0, 23, 1.4, 0.7, 3.0))


static func wood(id: String, tint: Color) -> StandardMaterial3D:
	## scanned worn wood; the tint keys each piece (texture is mid-brown, so
	## the tint is applied brightened to preserve per-prop variety)
	var t := Color(minf(tint.r * 2.2, 1.0), minf(tint.g * 2.2, 1.0), minf(tint.b * 2.2, 1.0))
	return _pbr("wood_" + id, "wood_table_worn", t, 1.1,
		func() -> StandardMaterial3D: return _surface("wood_p_" + id, tint, 0.62, 0.0, 41 + id.length(), 0.5, 0.45, 1.4, 6.0))


static func metal(id: String, tint: Color) -> StandardMaterial3D:
	var m := _pbr("metal_" + id, "metal_plate", Color(minf(tint.r * 1.6, 1.0), minf(tint.g * 1.6, 1.0), minf(tint.b * 1.6, 1.0)), 0.9,
		func() -> StandardMaterial3D: return _surface("metal_p_" + id, tint, 0.42, 0.85, 61 + id.length(), 1.1, 0.25, 2.0, 3.0))
	m.metallic = 0.75
	return m


static func fabric(id: String, tint: Color) -> StandardMaterial3D:
	## gentle brighten only: the weave is midtone, and the cast sheets are
	## browns and creams, not rust
	return _pbr("fabric_" + id, "fabric_pattern_07", Color(minf(tint.r * 1.3, 1.0), minf(tint.g * 1.3, 1.0), minf(tint.b * 1.3, 1.0)), 2.4,
		func() -> StandardMaterial3D: return _surface("fabric_p_" + id, tint, 0.97, 0.0, 83 + id.length(), 2.2, 0.7, 3.0))


static func carpet() -> StandardMaterial3D:
	return _pbr("carpet", "dirty_carpet", Color(0.55, 0.52, 0.45), 0.7,
		func() -> StandardMaterial3D: return _surface("carpet_p", Color(0.3, 0.34, 0.22), 0.98, 0.0, 141, 2.0, 0.8, 3.0))


static func dark_plastic() -> StandardMaterial3D:
	return _surface("plastic", Color(0.07, 0.065, 0.06), 0.34, 0.0, 97, 1.6, 0.2, 1.0)


static func _flat(id: String, tint: Color, rough: float, metalness: float) -> StandardMaterial3D:
	if _mats.has(id):
		return _mats[id]
	var m := StandardMaterial3D.new()
	m.albedo_color = tint
	m.roughness = rough
	m.metallic = metalness
	_mats[id] = m
	return m


## ---- prop builders ----------------------------------------------------------

static func _box_mi(size: Vector3, mat: Material, pos: Vector3, parent: Node3D) -> MeshInstance3D:
	var b := BoxMesh.new()
	b.size = size
	b.material = mat
	var mi := MeshInstance3D.new()
	mi.mesh = b
	mi.position = pos
	parent.add_child(mi)
	return mi


## A control knob: fluted cap on a shaft. Used across consoles and the CRT.
static func knob(mat: Material) -> Node3D:
	var n := Node3D.new()
	var cap := CylinderMesh.new()
	cap.top_radius = 0.045
	cap.bottom_radius = 0.055
	cap.height = 0.05
	cap.radial_segments = 12
	cap.material = mat
	var mi := MeshInstance3D.new()
	mi.mesh = cap
	mi.rotation.x = PI / 2.0
	n.add_child(mi)
	# index dot so the knob reads as turnable
	_box_mi(Vector3(0.006, 0.02, 0.03), OCHRE_MAT(), Vector3(0, 0.018, 0.028), n)
	return n


static func OCHRE_MAT() -> StandardMaterial3D:
	return _flat("ochre", OCHRE, 0.5, 0.2)


## A deep period CRT cabinet. Screen faces +Z; the opening is centered on local
## origin so the caller's live-feed quad drops straight into the bezel. The body
## runs back along -Z (these sets were as deep as they were wide).
static func crt_shell(screen_w: float, screen_h: float) -> Node3D:
	var n := Node3D.new()
	var body_mat := dark_plastic()
	var bezel_mat := _flat("bezel", Color(0.11, 0.10, 0.09), 0.5, 0.05)
	var border := 0.14
	var ow := screen_w + border * 2.0
	var oh := screen_h + border * 2.0
	var depth := maxf(screen_w, 0.5) * 0.62
	# cabinet body, tapering back a touch via a smaller rear box
	_box_mi(Vector3(ow, oh, depth), body_mat, Vector3(0, 0, -depth / 2.0 - 0.01), n)
	_box_mi(Vector3(ow * 0.7, oh * 0.7, 0.12), body_mat, Vector3(0, 0, -depth - 0.06), n)
	# bezel: four front frames around the opening
	var fd := 0.06
	var fz := fd / 2.0
	_box_mi(Vector3(ow, border, fd), bezel_mat, Vector3(0, (screen_h + border) / 2.0, fz), n)
	_box_mi(Vector3(ow, border, fd), bezel_mat, Vector3(0, -(screen_h + border) / 2.0, fz), n)
	_box_mi(Vector3(border, screen_h, fd), bezel_mat, Vector3((screen_w + border) / 2.0, 0, fz), n)
	_box_mi(Vector3(border, screen_h, fd), bezel_mat, Vector3(-(screen_w + border) / 2.0, 0, fz), n)
	# control cluster, lower-right of the bezel
	var kx := (screen_w + border) / 2.0 - 0.02
	for i in 2:
		var k := knob(_flat("knob", Color(0.16, 0.15, 0.14), 0.4, 0.1))
		k.position = Vector3(kx, -(screen_h + border) / 2.0 + 0.02, fd + 0.01)
		k.position.y += i * 0.08
		n.add_child(k)
	# a dim amber power lamp
	var lamp := _box_mi(Vector3(0.03, 0.03, 0.02), _flat("lamp", Color(0.9, 0.5, 0.15), 0.3, 0.0), Vector3(-kx, -(screen_h + border) / 2.0 + 0.03, fd + 0.01), n)
	var lm := lamp.mesh as BoxMesh
	var lmat := lm.material as StandardMaterial3D
	lmat.emission_enabled = true
	lmat.emission = Color(1.0, 0.55, 0.18)
	lmat.emission_energy_multiplier = 2.0
	return n


## An upholstered club armchair: cushion, back, arms, wooden legs. Replaces the
## two-box stand-in. Faces -Z (the back is at -Z), matching the old prop.
static func club_chair(tint: Color) -> Node3D:
	var n := Node3D.new()
	var seat_mat := fabric(tint.to_html(false), tint)
	var frame_mat := wood("chairleg", Color(0.28, 0.20, 0.13))
	# seat base + cushion
	_box_mi(Vector3(0.62, 0.14, 0.62), frame_mat, Vector3(0, 0.30, 0), n)
	_box_mi(Vector3(0.58, 0.16, 0.58), seat_mat, Vector3(0, 0.44, 0), n)
	# back
	_box_mi(Vector3(0.6, 0.55, 0.14), seat_mat, Vector3(0, 0.72, -0.24), n)
	# arms
	for sx in [-1.0, 1.0]:
		_box_mi(Vector3(0.12, 0.30, 0.6), seat_mat, Vector3(0.31 * sx, 0.52, 0), n)
	# four legs
	for lx in [-0.26, 0.26]:
		for lz in [-0.26, 0.26]:
			var leg := CylinderMesh.new()
			leg.top_radius = 0.035
			leg.bottom_radius = 0.03
			leg.height = 0.24
			leg.radial_segments = 8
			leg.material = frame_mat
			var mi := MeshInstance3D.new()
			mi.mesh = leg
			mi.position = Vector3(lx, 0.12, lz)
			n.add_child(mi)
	return n


## A continuous baseboard skirt around a rectangular room, in wood. Purely
## decorative (no collision) — it grounds the wall/floor seam.
static func baseboard(cx: float, cz: float, sx: float, sz: float, parent: Node3D) -> void:
	var mat := wood("skirt", Color(0.30, 0.23, 0.16))
	var h := 0.16
	var t := 0.28
	var y := h / 2.0 + 0.01
	_box_mi(Vector3(sx, h, t), mat, Vector3(cx, y, cz - sz / 2.0), parent)
	_box_mi(Vector3(sx, h, t), mat, Vector3(cx, y, cz + sz / 2.0), parent)
	_box_mi(Vector3(t, h, sz), mat, Vector3(cx - sx / 2.0, y, cz), parent)
	_box_mi(Vector3(t, h, sz), mat, Vector3(cx + sx / 2.0, y, cz), parent)


## ---- the machines -------------------------------------------------------------

## A broadcast console: cabinet body with an angled fascia carrying knob rows
## and fader slots. Faces +Z. size is the cabinet body (fascia rides on top).
static func console(size: Vector3, knob_rows := 2, faders := 5) -> Node3D:
	var n := Node3D.new()
	var body_mat := dark_plastic()
	var panel_mat := metal("fascia", Color(0.22, 0.23, 0.25))
	_box_mi(size, body_mat, Vector3(0, size.y / 2.0, 0), n)
	## the fascia: angled toward the operator
	var panel := _box_mi(Vector3(size.x * 0.94, 0.05, size.z * 0.8), panel_mat, Vector3(0, size.y + 0.02, 0.04), n)
	panel.rotation.x = -0.32
	## knob rows
	var kmat := _flat("knob", Color(0.16, 0.15, 0.14), 0.4, 0.1)
	for r in knob_rows:
		var count := int(size.x / 0.16)
		for i in count:
			var k := knob(kmat)
			k.scale = Vector3.ONE * 0.7
			k.position = Vector3(-size.x * 0.42 + float(i) * (size.x * 0.84 / maxf(float(count - 1), 1.0)), size.y + 0.05 + 0.012 * float(r), 0.16 - 0.14 * float(r))
			k.rotation.x = -PI / 2.0 + 0.32
			n.add_child(k)
	## fader slots along the fascia's near edge
	var slot_mat := _flat("slot", Color(0.04, 0.04, 0.045), 0.7, 0.0)
	var cap_mat := _flat("fader", Color(0.82, 0.79, 0.72), 0.5, 0.1)
	for i in faders:
		var fx := -size.x * 0.35 + float(i) * (size.x * 0.7 / maxf(float(faders - 1), 1.0))
		var slot := _box_mi(Vector3(0.02, 0.012, 0.22), slot_mat, Vector3(fx, size.y + 0.045, 0.22), n)
		slot.rotation.x = -0.32
		var fcap := _box_mi(Vector3(0.05, 0.03, 0.035), cap_mat, Vector3(fx, size.y + 0.06, 0.22 + 0.05 - 0.02 * float(i % 3)), n)
		fcap.rotation.x = -0.32
	return n


## A reel-to-reel deck: the bench's instrument. Two reels proud of a deck face.
## Returns { "rig": Node3D, "reels": [Node3D, Node3D] } — spin the reels while
## a capture runs if the caller likes.
static func reel_deck() -> Dictionary:
	var n := Node3D.new()
	var deck_mat := metal("deck", Color(0.32, 0.33, 0.35))
	var reel_mat := _flat("reel", Color(0.72, 0.70, 0.66), 0.35, 0.6)
	_box_mi(Vector3(0.72, 0.5, 0.16), deck_mat, Vector3(0, 0, 0), n)
	var reels: Array = []
	for side in [-1.0, 1.0]:
		var hub := Node3D.new()
		hub.position = Vector3(0.17 * side, 0.1, 0.09)
		n.add_child(hub)
		var plate := CylinderMesh.new()
		plate.top_radius = 0.13
		plate.bottom_radius = 0.13
		plate.height = 0.02
		plate.radial_segments = 16
		plate.material = reel_mat
		var pmi := MeshInstance3D.new()
		pmi.mesh = plate
		pmi.rotation.x = PI / 2.0
		hub.add_child(pmi)
		## three spokes so rotation reads
		for s in 3:
			var spoke := _box_mi(Vector3(0.02, 0.2, 0.012), dark_plastic(), Vector3(0, 0, 0.012), hub)
			spoke.rotation.z = float(s) * PI / 3.0
		reels.append(hub)
	## transport buttons under the reels
	for i in 4:
		_box_mi(Vector3(0.06, 0.03, 0.02), _flat("btn", Color(0.14, 0.14, 0.15), 0.5, 0.1), Vector3(-0.14 + 0.09 * float(i), -0.18, 0.09), n)
	return {"rig": n, "reels": reels}


## A paneled door leaf hinged at local origin, running toward +X (matching the
## greybox leaf convention). Panels inset, handle at the far edge.
static func door_leaf(w: float, h: float, mat: Material, parent: Node3D) -> void:
	_box_mi(Vector3(w, h, 0.09), mat, Vector3(w / 2.0, h / 2.0, 0), parent)
	var inset := wood("doorpanel", Color(0.27, 0.20, 0.12))
	var pw := w * 0.36
	for py in [h * 0.3, h * 0.68]:
		for px in [w * 0.28, w * 0.72]:
			_box_mi(Vector3(pw, h * 0.28, 0.03), inset, Vector3(px, py, 0.04), parent)
	var handle_mat := metal("handle", Color(0.55, 0.5, 0.4))
	for zs in [0.07, -0.07]:
		var hd := SphereMesh.new()
		hd.radius = 0.035
		hd.height = 0.07
		hd.material = handle_mat
		var hmi := MeshInstance3D.new()
		hmi.mesh = hd
		hmi.position = Vector3(w - 0.12, h * 0.42, zs)
		parent.add_child(hmi)


## A log-station lectern: post, angled top, the binder and its pen on a chain.
static func lectern() -> Node3D:
	var n := Node3D.new()
	var post_mat := metal("station", Color(0.79, 0.64, 0.24))
	var top_mat := wood("lectern", Color(0.34, 0.26, 0.17))
	var paper_mat := _flat("paper", Color(0.87, 0.83, 0.72), 0.95, 0.0)
	_box_mi(Vector3(0.12, 0.95, 0.12), post_mat, Vector3(0, -0.08, 0), n)
	_box_mi(Vector3(0.34, 0.04, 0.3), post_mat, Vector3(0, -0.53, 0), n)
	var top := _box_mi(Vector3(0.5, 0.05, 0.42), top_mat, Vector3(0, 0.44, 0.02), n)
	top.rotation.x = -0.35
	var binder := _box_mi(Vector3(0.36, 0.03, 0.3), paper_mat, Vector3(0, 0.48, 0.04), n)
	binder.rotation.x = -0.35
	var pen := _box_mi(Vector3(0.11, 0.012, 0.012), dark_plastic(), Vector3(0.12, 0.51, 0.1), n)
	pen.rotation.z = 0.3
	pen.rotation.x = -0.35
	return n


## A key that reads as a key: bow ring, shaft, two teeth. Lies flat.
static func key_prop(tint: Color) -> Node3D:
	var n := Node3D.new()
	var mat := metal("key_" + tint.to_html(false), tint)
	var bow := TorusMesh.new()
	bow.inner_radius = 0.035
	bow.outer_radius = 0.06
	bow.material = mat
	var bmi := MeshInstance3D.new()
	bmi.mesh = bow
	bmi.position = Vector3(-0.1, 0, 0)
	n.add_child(bmi)
	_box_mi(Vector3(0.18, 0.016, 0.022), mat, Vector3(0.03, 0, 0), n)
	_box_mi(Vector3(0.025, 0.016, 0.05), mat, Vector3(0.09, 0, -0.03), n)
	_box_mi(Vector3(0.025, 0.016, 0.035), mat, Vector3(0.05, 0, -0.024), n)
	return n


## ---- the library and the hall ---------------------------------------------------

## A tape stack: uprights, shelves, and rows of spines with deterministic
## jitter (seeded from `vseed`, stable across loads). Runs along local X,
## faces +Z. Caller owns collision.
static func tape_shelf(w: float, h: float, shelves: int, vseed: int) -> Node3D:
	var n := Node3D.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = vseed
	var frame := wood("shelf", Color(0.30, 0.24, 0.17))
	var depth := 0.42
	for sx in [-w / 2.0, w / 2.0]:
		_box_mi(Vector3(0.06, h, depth), frame, Vector3(sx, h / 2.0, 0), n)
	var spine_tints := [
		Color(0.32, 0.28, 0.22), Color(0.25, 0.27, 0.3), Color(0.35, 0.25, 0.18),
		Color(0.28, 0.3, 0.24), Color(0.24, 0.22, 0.2), Color(0.4, 0.34, 0.24),
	]
	for s in shelves:
		var sy := h * (float(s) + 0.55) / float(shelves)
		_box_mi(Vector3(w, 0.04, depth), frame, Vector3(0, sy - h * 0.5 / float(shelves) + 0.02, 0), n)
		## the row of spines: tapes lean and gap like a used archive
		var x := -w / 2.0 + 0.09
		while x < w / 2.0 - 0.1:
			if rng.randf() < 0.12:
				x += rng.randf_range(0.06, 0.16)  ## a borrowed tape's gap
				continue
			var tw := rng.randf_range(0.035, 0.06)
			var th := rng.randf_range(0.24, 0.3)
			var tint: Color = spine_tints[rng.randi() % spine_tints.size()]
			var spine := _box_mi(Vector3(tw, th, 0.3), _flat("spine_" + tint.to_html(false), tint, 0.85, 0.0), Vector3(x, sy - h * 0.5 / float(shelves) + 0.04 + th / 2.0, 0.0), n)
			if rng.randf() < 0.1:
				spine.rotation.z = rng.randf_range(-0.09, 0.09)  ## the leaner
			x += tw + 0.012
	return n


## A transmitter rack cabinet: tall body, vent slats, dial gauges, lamps that
## remember being watched. Faces +Z.
static func transmitter_cabinet(h: float, vseed: int) -> Node3D:
	var n := Node3D.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = vseed
	var body := metal("txcab", Color(0.24, 0.26, 0.24))
	var slat := dark_plastic()
	_box_mi(Vector3(0.9, h, 0.7), body, Vector3(0, h / 2.0, 0), n)
	## vent slats, lower third
	for i in 5:
		_box_mi(Vector3(0.7, 0.025, 0.02), slat, Vector3(0, 0.25 + 0.09 * float(i), 0.36), n)
	## gauges: two dials behind glass rims
	for gx in [-0.2, 0.2]:
		var rim := CylinderMesh.new()
		rim.top_radius = 0.09
		rim.bottom_radius = 0.09
		rim.height = 0.04
		rim.radial_segments = 14
		rim.material = slat
		var rmi := MeshInstance3D.new()
		rmi.mesh = rim
		rmi.rotation.x = PI / 2.0
		rmi.position = Vector3(gx, h - 0.35, 0.36)
		n.add_child(rmi)
		var face := CylinderMesh.new()
		face.top_radius = 0.07
		face.bottom_radius = 0.07
		face.height = 0.02
		face.radial_segments = 14
		face.material = _flat("gauge", Color(0.85, 0.82, 0.72), 0.6, 0.0)
		var fmi := MeshInstance3D.new()
		fmi.mesh = face
		fmi.rotation.x = PI / 2.0
		fmi.position = Vector3(gx, h - 0.35, 0.375)
		n.add_child(fmi)
		var needle := _box_mi(Vector3(0.008, 0.05, 0.008), _flat("needle", Color(0.7, 0.2, 0.15), 0.5, 0.0), Vector3(gx, h - 0.34, 0.385), n)
		needle.rotation.z = rng.randf_range(-0.9, 0.9)
	## indicator lamps, one warm
	for i in 3:
		var live := i == (vseed % 3)
		var lmat := StandardMaterial3D.new()
		lmat.albedo_color = Color(0.9, 0.55, 0.2) if live else Color(0.2, 0.19, 0.17)
		lmat.roughness = 0.4
		if live:
			lmat.emission_enabled = true
			lmat.emission = Color(1.0, 0.55, 0.18)
			lmat.emission_energy_multiplier = 1.6
		var lamp := SphereMesh.new()
		lamp.radius = 0.022
		lamp.height = 0.044
		lamp.material = lmat
		var lmi := MeshInstance3D.new()
		lmi.mesh = lamp
		lmi.position = Vector3(-0.25 + 0.25 * float(i), h - 0.62, 0.36)
		n.add_child(lmi)
	## the big handle
	_box_mi(Vector3(0.06, 0.3, 0.06), metal("handle", Color(0.55, 0.5, 0.4)), Vector3(0.36, h * 0.45, 0.38), n)
	return n


## The transmitter tower: four tapering legs, cross-braces, the beacon.
## Returns { "rig": Node3D, "beacon_mat": StandardMaterial3D } so an ending can
## put the light out.
static func tower(h: float) -> Dictionary:
	var n := Node3D.new()
	var steel := metal("tower", Color(0.42, 0.4, 0.38))
	var base := 1.4
	var top := 0.3
	var sections := 4
	for s in sections:
		var y0 := h * float(s) / float(sections)
		var y1 := h * float(s + 1) / float(sections)
		var r0 := lerpf(base, top, float(s) / float(sections)) / 2.0
		var r1 := lerpf(base, top, float(s + 1) / float(sections)) / 2.0
		var rm := (r0 + r1) / 2.0
		var sh := y1 - y0
		var lean := atan2(r0 - r1, sh)
		for corner in [Vector2(-1, -1), Vector2(1, -1), Vector2(-1, 1), Vector2(1, 1)]:
			var leg := _box_mi(Vector3(0.07, sh / cos(lean), 0.07), steel, Vector3(corner.x * rm, (y0 + y1) / 2.0, corner.y * rm), n)
			leg.rotation.z = lean * corner.x
			leg.rotation.x = -lean * corner.y
		## cross braces at the section joint
		for xb in [-1.0, 1.0]:
			var brace := _box_mi(Vector3(0.05, r1 * 2.8, 0.05), steel, Vector3(xb * r1, y1, 0), n)
			brace.rotation.x = PI / 2.0
			var brace2 := _box_mi(Vector3(r1 * 2.8, 0.05, 0.05), steel, Vector3(0, y1, xb * r1), n)
			brace2.rotation.y = 0.0
	## the beacon
	var bmat := StandardMaterial3D.new()
	bmat.albedo_color = Color(0.8, 0.15, 0.1)
	bmat.emission_enabled = true
	bmat.emission = Color(1.0, 0.12, 0.08)
	bmat.emission_energy_multiplier = 2.4
	var beacon := SphereMesh.new()
	beacon.radius = 0.12
	beacon.height = 0.24
	beacon.material = bmat
	var bmi := MeshInstance3D.new()
	bmi.mesh = beacon
	bmi.position = Vector3(0, h + 0.1, 0)
	n.add_child(bmi)
	_box_mi(Vector3(0.05, 0.35, 0.05), steel, Vector3(0, h - 0.12, 0), n)
	return {"rig": n, "beacon_mat": bmat}


## Felt acoustic panels along one wall face: the dead room's lining. Purely
## visual; the hum stops at the seam, not at physics.
static func felt_run(length: float, parent: Node3D, pos: Vector3, yaw: float) -> void:
	var fm := fabric("felt", Color(0.12, 0.11, 0.13))
	var count := int(length / 0.7)
	for i in count:
		var p := Node3D.new()
		p.position = pos
		p.rotation.y = yaw
		parent.add_child(p)
		_box_mi(Vector3(0.6, 2.0, 0.05), fm, Vector3(-length / 2.0 + 0.38 + 0.7 * float(i), 1.25, 0), p)


## ---- the kitchen, the set, the yard ---------------------------------------------

## The kettle. It matters more than its polygon count suggests.
static func kettle() -> Node3D:
	var n := Node3D.new()
	var steel := metal("kettle", Color(0.6, 0.58, 0.54))
	var body := CylinderMesh.new()
	body.top_radius = 0.07
	body.bottom_radius = 0.1
	body.height = 0.14
	body.radial_segments = 12
	body.material = steel
	var bmi := MeshInstance3D.new()
	bmi.mesh = body
	bmi.position = Vector3(0, 0.07, 0)
	n.add_child(bmi)
	## lid knob
	var knob_s := SphereMesh.new()
	knob_s.radius = 0.02
	knob_s.height = 0.04
	knob_s.material = dark_plastic()
	var kmi := MeshInstance3D.new()
	kmi.mesh = knob_s
	kmi.position = Vector3(0, 0.16, 0)
	n.add_child(kmi)
	## spout
	var spout := _box_mi(Vector3(0.03, 0.09, 0.03), steel, Vector3(0.1, 0.1, 0), n)
	spout.rotation.z = -0.5
	## handle arch
	_box_mi(Vector3(0.025, 0.09, 0.025), dark_plastic(), Vector3(-0.1, 0.13, 0), n)
	var grip := _box_mi(Vector3(0.09, 0.025, 0.025), dark_plastic(), Vector3(-0.06, 0.18, 0), n)
	grip.rotation.z = 0.15
	return n


## A run of base cabinets with counter, doors, a sink basin, and uppers.
## Runs along local X, back against -Z. Caller owns collision.
static func kitchen_block(length: float) -> Node3D:
	var n := Node3D.new()
	var cab := wood("kcab", Color(0.36, 0.3, 0.22))
	var face := wood("kface", Color(0.42, 0.35, 0.25))
	var counter := _flat("counter", Color(0.62, 0.6, 0.55), 0.5, 0.05)
	_box_mi(Vector3(length, 0.86, 0.58), cab, Vector3(0, 0.43, 0), n)
	_box_mi(Vector3(length + 0.04, 0.05, 0.64), counter, Vector3(0, 0.885, 0.02), n)
	## door faces with knobs
	var doors := int(length / 0.55)
	for i in doors:
		var dx := -length / 2.0 + 0.32 + float(i) * (length - 0.6) / maxf(float(doors - 1), 1.0)
		_box_mi(Vector3(0.44, 0.62, 0.03), face, Vector3(dx, 0.42, 0.3), n)
		var kn := SphereMesh.new()
		kn.radius = 0.018
		kn.height = 0.036
		kn.material = dark_plastic()
		var kmi := MeshInstance3D.new()
		kmi.mesh = kn
		kmi.position = Vector3(dx + 0.15, 0.42, 0.33)
		n.add_child(kmi)
	## the sink: a basin inset at the left end
	_box_mi(Vector3(0.5, 0.02, 0.4), _flat("basin", Color(0.5, 0.5, 0.5), 0.4, 0.6), Vector3(-length / 2.0 + 0.45, 0.9, 0.02), n)
	_box_mi(Vector3(0.42, 0.12, 0.32), _flat("basin_in", Color(0.3, 0.3, 0.32), 0.5, 0.5), Vector3(-length / 2.0 + 0.45, 0.85, 0.02), n)
	var tap := _box_mi(Vector3(0.03, 0.22, 0.03), metal("tap", Color(0.6, 0.58, 0.54)), Vector3(-length / 2.0 + 0.45, 1.0, -0.16), n)
	var tap2 := _box_mi(Vector3(0.03, 0.03, 0.14), metal("tap", Color(0.6, 0.58, 0.54)), Vector3(-length / 2.0 + 0.45, 1.1, -0.1), n)
	tap.rotation.z = 0.0
	tap2.rotation.z = 0.0
	## uppers
	_box_mi(Vector3(length * 0.7, 0.55, 0.34), cab, Vector3(-length * 0.12, 1.95, -0.12), n)
	return n


## The cubby wall from the Gladhouse set: a grid of cells, some still holding
## what a show for children keeps. Faces +Z; seeded stable.
static func cubby_wall(w: float, h: float, cols: int, rows: int, vseed: int) -> Node3D:
	var n := Node3D.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = vseed
	var frame := wood("cubby", Color(0.3, 0.36, 0.26))
	var back := wood("cubbyback", Color(0.25, 0.3, 0.22))
	var depth := 0.4
	_box_mi(Vector3(w, h, 0.04), back, Vector3(0, h / 2.0, -depth / 2.0), n)
	for c in cols + 1:
		_box_mi(Vector3(0.04, h, depth), frame, Vector3(-w / 2.0 + w * float(c) / float(cols), h / 2.0, 0), n)
	for r in rows + 1:
		_box_mi(Vector3(w, 0.04, depth), frame, Vector3(0, h * float(r) / float(rows), 0), n)
	## contents: ball, block, or tin, in about half the cells
	var toy_tints := [Color(0.7, 0.3, 0.2), Color(0.79, 0.64, 0.24), Color(0.35, 0.45, 0.3), Color(0.4, 0.45, 0.6)]
	for c in cols:
		for r in rows:
			if rng.randf() > 0.55:
				continue
			var cx := -w / 2.0 + w * (float(c) + 0.5) / float(cols)
			var cy := h * (float(r) + 0.22) / float(rows)
			var tint: Color = toy_tints[rng.randi() % toy_tints.size()]
			var kind := rng.randi() % 3
			if kind == 0:
				var ball := SphereMesh.new()
				ball.radius = 0.09
				ball.height = 0.18
				ball.material = _flat("toy_" + tint.to_html(false), tint, 0.8, 0.0)
				var mi := MeshInstance3D.new()
				mi.mesh = ball
				mi.position = Vector3(cx, cy + 0.07, 0)
				n.add_child(mi)
			elif kind == 1:
				_box_mi(Vector3(0.13, 0.13, 0.13), _flat("toy_" + tint.to_html(false), tint, 0.8, 0.0), Vector3(cx, cy + 0.085, 0), n)
			else:
				var tin := CylinderMesh.new()
				tin.top_radius = 0.06
				tin.bottom_radius = 0.06
				tin.height = 0.12
				tin.radial_segments = 10
				tin.material = metal("tin", Color(0.55, 0.52, 0.46))
				var mi := MeshInstance3D.new()
				mi.mesh = tin
				mi.position = Vector3(cx, cy + 0.08, 0)
				n.add_child(mi)
	return n


## A studio camera pedestal: column, pan head, camera body, lens, the handle
## the operator left at station. Lens faces +Z.
static func camera_pedestal() -> Node3D:
	var n := Node3D.new()
	var ped_mat := metal("pedestal", Color(0.16, 0.16, 0.17))
	var cam_mat := dark_plastic()
	var col := CylinderMesh.new()
	col.height = 1.15
	col.top_radius = 0.14
	col.bottom_radius = 0.3
	col.material = ped_mat
	var cmi := MeshInstance3D.new()
	cmi.mesh = col
	cmi.position = Vector3(0, 0.575, 0)
	n.add_child(cmi)
	## pan head + body
	_box_mi(Vector3(0.22, 0.1, 0.26), ped_mat, Vector3(0, 1.2, 0), n)
	_box_mi(Vector3(0.34, 0.34, 0.62), cam_mat, Vector3(0, 1.42, -0.05), n)
	## lens hood
	var lens := CylinderMesh.new()
	lens.top_radius = 0.09
	lens.bottom_radius = 0.11
	lens.height = 0.2
	lens.radial_segments = 12
	lens.material = cam_mat
	var lmi := MeshInstance3D.new()
	lmi.mesh = lens
	lmi.rotation.x = PI / 2.0
	lmi.position = Vector3(0, 1.42, 0.35)
	n.add_child(lmi)
	## viewfinder + operator handle
	_box_mi(Vector3(0.12, 0.1, 0.16), cam_mat, Vector3(0, 1.63, -0.2), n)
	var handle := _box_mi(Vector3(0.03, 0.03, 0.3), metal("handle", Color(0.55, 0.5, 0.4)), Vector3(0.16, 1.28, -0.3), n)
	handle.rotation.x = -0.5
	return n


## ---- green room, dorms, dock ----------------------------------------------------

## The green room vanity: mirror, bulb surround, counter. Faces +Z.
static func vanity() -> Node3D:
	var n := Node3D.new()
	var frame := wood("vanity", Color(0.34, 0.26, 0.17))
	_box_mi(Vector3(1.4, 0.06, 0.5), frame, Vector3(0, 0.78, 0.1), n)
	for lx in [-0.6, 0.6]:
		_box_mi(Vector3(0.08, 0.78, 0.4), frame, Vector3(lx, 0.39, 0.1), n)
	## the mirror: metallic and smooth enough to gesture at reflection
	var mir := StandardMaterial3D.new()
	mir.albedo_color = Color(0.75, 0.78, 0.8)
	mir.metallic = 1.0
	mir.roughness = 0.06
	_box_mi(Vector3(1.1, 1.1, 0.03), mir, Vector3(0, 1.5, 0.0), n)
	_box_mi(Vector3(1.22, 1.22, 0.05), frame, Vector3(0, 1.5, -0.025), n)
	## the bulbs: warm, half of them still working
	for i in 10:
		var on_side := i < 5
		var bx := (-0.52 if on_side else 0.52)
		var by := 1.1 + 0.2 * float(i % 5)
		var lit := (i % 3) != 1  ## two of three still burn
		var bmat := StandardMaterial3D.new()
		bmat.albedo_color = Color(1.0, 0.85, 0.6) if lit else Color(0.35, 0.32, 0.28)
		if lit:
			bmat.emission_enabled = true
			bmat.emission = Color(1.0, 0.75, 0.45)
			bmat.emission_energy_multiplier = 1.8
		var bulb := SphereMesh.new()
		bulb.radius = 0.032
		bulb.height = 0.064
		bulb.material = bmat
		var bmi := MeshInstance3D.new()
		bmi.mesh = bulb
		bmi.position = Vector3(bx, by, 0.03)
		n.add_child(bmi)
	return n


## A green-room couch: three cushions, low back, wooden feet. Faces +Z.
static func couch(tint: Color) -> Node3D:
	var n := Node3D.new()
	var fab := fabric("couch_" + tint.to_html(false), tint)
	var frame := wood("couchleg", Color(0.28, 0.20, 0.13))
	_box_mi(Vector3(1.9, 0.16, 0.7), frame, Vector3(0, 0.22, 0), n)
	for i in 3:
		_box_mi(Vector3(0.58, 0.16, 0.62), fab, Vector3(-0.62 + 0.62 * float(i), 0.38, 0.02), n)
	_box_mi(Vector3(1.9, 0.5, 0.16), fab, Vector3(0, 0.6, -0.28), n)
	for sx in [-1.0, 1.0]:
		_box_mi(Vector3(0.14, 0.34, 0.7), fab, Vector3(0.88 * sx, 0.5, 0), n)
		for fz in [-0.25, 0.25]:
			_box_mi(Vector3(0.08, 0.14, 0.08), frame, Vector3(0.8 * sx, 0.07, fz), n)
	return n


## A painted scenery flat, leaning where the dock keeps them. Faces +Z.
static func scene_flat(tint: Color, w: float, h: float) -> Node3D:
	var n := Node3D.new()
	var face := _flat("flat_" + tint.to_html(false), tint, 0.92, 0.0)
	var back := wood("flatback", Color(0.36, 0.3, 0.22))
	_box_mi(Vector3(w, h, 0.05), face, Vector3(0, h / 2.0, 0.03), n)
	_box_mi(Vector3(w, h, 0.04), back, Vector3(0, h / 2.0, -0.02), n)
	## brace battens
	for by in [h * 0.25, h * 0.75]:
		_box_mi(Vector3(w * 0.9, 0.07, 0.03), back, Vector3(0, by, -0.055), n)
	return n


## A dorm bed: simpler than Rita's, blanket loose because nobody checks.
static func dorm_bed(blanket_tint: Color) -> Node3D:
	var n := Node3D.new()
	var frame := wood("dormframe", Color(0.3, 0.22, 0.14))
	_box_mi(Vector3(2.0, 0.22, 1.0), frame, Vector3(0, 0.17, 0), n)
	_box_mi(Vector3(1.94, 0.18, 0.94), fabric("dormmatt", Color(0.58, 0.55, 0.48)), Vector3(0, 0.37, 0), n)
	var blanket := _box_mi(Vector3(1.2, 0.06, 0.97), fabric("dormblanket_" + blanket_tint.to_html(false), blanket_tint), Vector3(0.3, 0.48, 0.01), n)
	blanket.rotation.z = 0.02  ## loose
	_box_mi(Vector3(0.38, 0.09, 0.55), fabric("dormpillow", Color(0.78, 0.75, 0.68)), Vector3(-0.72, 0.49, 0), n)
	_box_mi(Vector3(0.05, 0.62, 1.0), frame, Vector3(-0.98, 0.31, 0), n)
	return n


## A run of staff lockers: doors, vents, handles, one ajar. Faces +Z.
static func locker_run(count: int) -> Node3D:
	var n := Node3D.new()
	var body := metal("locker", Color(0.35, 0.4, 0.38))
	var lw := 0.45
	_box_mi(Vector3(lw * float(count), 1.9, 0.5), body, Vector3(0, 0.95, 0), n)
	for i in count:
		var dx := -lw * float(count) / 2.0 + lw * (float(i) + 0.5)
		var ajar := i == count - 1
		var door := _box_mi(Vector3(lw - 0.05, 1.8, 0.03), metal("lockerdoor", Color(0.4, 0.45, 0.42)), Vector3(dx, 0.95, 0.26), n)
		if ajar:
			door.rotation.y = 0.35
			door.position.x += 0.06
		for v in 3:
			_box_mi(Vector3(0.2, 0.015, 0.01), dark_plastic(), Vector3(dx, 1.55 - 0.06 * float(v), 0.28), n)
		_box_mi(Vector3(0.03, 0.12, 0.03), dark_plastic(), Vector3(dx + 0.15, 0.95, 0.28), n)
	return n
