class_name CharacterKit
extends RefCounted
## The cast, embodied — per docs/canon/art. The club are PEOPLE (cast sheets:
## Merle Cottry, Harriet), built as stylized low-poly humans in the portrait
## palette: browns, creams, one warm light. Chum is a CAT — the after-fire
## dossier is explicit: triangular ears, wire whiskers, tally-light camera eye
## (right), melted button eye (left), manual jaw on a lever, throat-speaker
## chest, exposed tendons, weighted paw feet, bell at the collar, a tail.
## All procedural, nothing imported. Callers own collision and logic.

const NEAR_BLACK := Color(0.05, 0.045, 0.04)
const FELT_BUTTON := Color(0.08, 0.08, 0.1)
const AMBER := Color(0.79, 0.64, 0.24)
const SKIN := Color(0.68, 0.55, 0.45)

static var _wool_cache: Dictionary = {}


## Wool shader material, tinted, cached per tint. (Used by the chum bodies.)
static func wool(tint: Color = Color(0.34, 0.26, 0.17)) -> ShaderMaterial:
	var key := tint.to_html(false)
	if _wool_cache.has(key):
		return _wool_cache[key]
	var m := ShaderMaterial.new()
	m.shader = load("res://shaders/wool.gdshader") as Shader
	m.set_shader_parameter("albedo", Color(tint.r, tint.g, tint.b, 1.0))
	_wool_cache[key] = m
	return m


static func _sphere(r: float, mat: Material, pos: Vector3, parent: Node3D) -> MeshInstance3D:
	var s := SphereMesh.new()
	s.radius = r
	s.height = r * 2.0
	s.material = mat
	var mi := MeshInstance3D.new()
	mi.mesh = s
	mi.position = pos
	parent.add_child(mi)
	return mi


static func _capsule(r: float, h: float, mat: Material, pos: Vector3, parent: Node3D) -> MeshInstance3D:
	var c := CapsuleMesh.new()
	c.radius = r
	c.height = h
	c.material = mat
	var mi := MeshInstance3D.new()
	mi.mesh = c
	mi.position = pos
	parent.add_child(mi)
	return mi


static func _boxm(size: Vector3, mat: Material, pos: Vector3, parent: Node3D) -> MeshInstance3D:
	var b := BoxMesh.new()
	b.size = size
	b.material = mat
	var mi := MeshInstance3D.new()
	mi.mesh = b
	mi.position = pos
	parent.add_child(mi)
	return mi


static func _cyl(rt: float, rb: float, h: float, mat: Material, pos: Vector3, parent: Node3D) -> MeshInstance3D:
	var c := CylinderMesh.new()
	c.top_radius = rt
	c.bottom_radius = rb
	c.height = h
	c.radial_segments = 12
	c.material = mat
	var mi := MeshInstance3D.new()
	mi.mesh = c
	mi.position = pos
	parent.add_child(mi)
	return mi


static func _fabric(tint: Color) -> StandardMaterial3D:
	return PropKit.fabric(tint.to_html(false), tint)


static func _flat_mat(tint: Color, rough := 0.6) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = tint
	m.roughness = rough
	return m


## ---- the humans, plate-accurate ------------------------------------------------
## A real figure system: anatomy, faces, hairstyles, posed arms, held props.
## Each named builder matches its sheet in docs/canon/art. All figures face +Z.
## Proportions ~1.6 m (Vess 1.78). Callers own collision and logic.

const PEARL := Color(0.9, 0.88, 0.84)

static func _eye(head: Node3D, x: float, iris: Color) -> void:
	var white := _sphere(0.016, _flat_mat(Color(0.88, 0.86, 0.82), 0.35), Vector3(x, 0.02, 0.088), head)
	white.scale = Vector3(1.0, 0.85, 0.6)
	_sphere(0.008, _flat_mat(iris, 0.25), Vector3(x, 0.02, 0.101), head)


## The head: skull, cheeks, ears, nose, eyes, brows, mouth, aged softly.
## Returns the head Node3D (origin at head center) parented at `pos`.
static func _head(rig: Node3D, pos: Vector3, skin: Color, cfg: Dictionary = {}) -> Node3D:
	var skin_m := _flat_mat(skin, 0.88)
	var head := Node3D.new()
	head.position = pos
	rig.add_child(head)
	var skull := _sphere(0.105, skin_m, Vector3.ZERO, head)
	skull.scale = Vector3(0.94, 1.06, 0.98)
	## cheeks and jaw: a second, lower sphere rounds the face
	var jaw := _sphere(0.092, skin_m, Vector3(0, -0.035, 0.012), head)
	jaw.scale = Vector3(0.9, 0.82, 0.9)
	for side in [-1.0, 1.0]:
		_sphere(0.022, skin_m, Vector3(0.095 * side, -0.005, 0.0), head)
	## nose: bridge + tip
	var bridge := _boxm(Vector3(0.02, 0.05, 0.025), skin_m, Vector3(0, 0.0, 0.095), head)
	bridge.rotation.x = -0.15
	_sphere(0.017, skin_m, Vector3(0, -0.025, 0.102), head)
	_eye(head, -0.038, cfg.get("iris", Color(0.25, 0.2, 0.16)))
	_eye(head, 0.038, cfg.get("iris", Color(0.25, 0.2, 0.16)))
	## brows
	var brow_m := _flat_mat(cfg.get("brow", Color(0.4, 0.36, 0.32)), 0.85)
	for side in [-1.0, 1.0]:
		var brow := _boxm(Vector3(0.042, 0.008, 0.012), brow_m, Vector3(0.038 * side, 0.052, 0.092), head)
		brow.rotation.z = -0.12 * side
	## mouth: a soft line; age carries in the slight downturn
	_boxm(Vector3(0.042, 0.007, 0.012), _flat_mat(skin * 0.62, 0.8), Vector3(0, -0.065, 0.092), head)
	if cfg.get("stubble", false):
		var stub := _sphere(0.088, _flat_mat(skin * 0.78, 0.95), Vector3(0, -0.045, 0.014), head)
		stub.scale = Vector3(0.88, 0.72, 0.86)
	if cfg.get("earrings", false):
		for side in [-1.0, 1.0]:
			_sphere(0.011, _flat_mat(PEARL, 0.2), Vector3(0.098 * side, -0.035, 0.0), head)
	return head


## Hair styles per the sheets. Parented to the head so tilts carry it.
static func _hair(head: Node3D, tint: Color, style: String) -> void:
	var hm := _flat_mat(tint, 0.88)
	match style:
		"bun_neat":
			## Harriet: silver hair swept up, curled crown, neat high bun
			var cap := _sphere(0.112, hm, Vector3(0, 0.022, -0.014), head)
			cap.scale = Vector3(0.96, 0.92, 0.98)
			for c in 5:
				_sphere(0.028, hm, Vector3(-0.07 + 0.035 * float(c), 0.095, 0.045 - 0.01 * absf(float(c) - 2.0)), head)
			_sphere(0.048, hm, Vector3(0, 0.1, -0.07), head)
			_sphere(0.03, hm, Vector3(0.03, 0.115, -0.055), head)
		"bun_messy":
			## Merle: gray-brown, strays everywhere, low loose bun
			var cap2 := _sphere(0.114, hm, Vector3(0, 0.02, -0.012), head)
			cap2.scale = Vector3(0.98, 0.9, 1.0)
			_sphere(0.055, hm, Vector3(0, 0.09, -0.075), head)
			for st in 6:
				var strand := _boxm(Vector3(0.006, 0.075, 0.006), hm, Vector3(-0.1 + 0.04 * float(st), 0.02 - 0.02 * float(st % 3), 0.05 + 0.01 * float(st % 2)), head)
				strand.rotation.z = -0.5 + 0.22 * float(st)
			for c in 4:
				_sphere(0.024, hm, Vector3(-0.06 + 0.04 * float(c), 0.1, 0.03), head)
		"curly_dark":
			## Vess: a dark unruly mop, over the forehead and ears
			for c in [
				Vector3(0, 0.08, 0.01), Vector3(-0.06, 0.07, 0.04), Vector3(0.06, 0.07, 0.04),
				Vector3(-0.09, 0.045, -0.01), Vector3(0.09, 0.045, -0.01), Vector3(0, 0.075, -0.06),
				Vector3(-0.05, 0.09, -0.045), Vector3(0.05, 0.09, -0.045), Vector3(-0.045, 0.055, 0.075),
				Vector3(0.05, 0.05, 0.075), Vector3(-0.1, 0.0, -0.03), Vector3(0.1, 0.0, -0.03),
			]:
				_sphere(0.045, hm, c, head)
		"side_grey":
			## Leland: dark going grey, parted, a little long at the collar
			var cap3 := _sphere(0.111, hm, Vector3(0, 0.025, -0.02), head)
			cap3.scale = Vector3(0.96, 0.88, 1.0)
			for c in 3:
				_sphere(0.035, hm, Vector3(-0.07 + 0.07 * float(c), 0.06, 0.055), head)
			_sphere(0.04, hm, Vector3(-0.095, -0.02, -0.02), head)
			_sphere(0.04, hm, Vector3(0.095, -0.02, -0.02), head)


## A hand: palm plus mitten fingers and a thumb. `pos` is the wrist.
static func _hand(rig: Node3D, pos: Vector3, skin_m: Material, yaw := 0.0, pitch := 0.0) -> void:
	var h := Node3D.new()
	h.position = pos
	h.rotation.y = yaw
	h.rotation.x = pitch
	rig.add_child(h)
	var palm := _sphere(0.038, skin_m, Vector3.ZERO, h)
	palm.scale = Vector3(0.9, 1.15, 0.55)
	var fingers := _sphere(0.032, skin_m, Vector3(0, -0.048, 0.004), h)
	fingers.scale = Vector3(0.85, 1.0, 0.5)
	_sphere(0.014, skin_m, Vector3(0.036, -0.01, 0.012), h)


## An arm in a named pose. side: -1 left, +1 right (viewer's right at +X).
## Poses: "down" · "folded" (forearm across the waist) · "cup" (raised, holding)
## · "clutch" (pressed to the chest) · "pocket" (hand tucked at hip).
static func _arm(rig: Node3D, side: float, sleeve: Material, skin_m: Material, pose: String, shoulder_y := 1.17) -> void:
	match pose:
		"down":
			var up := _capsule(0.052, 0.24, sleeve, Vector3(0.2 * side, shoulder_y - 0.13, 0.0), rig)
			up.rotation.z = 0.1 * side
			var fore := _capsule(0.045, 0.22, sleeve, Vector3(0.225 * side, shoulder_y - 0.36, 0.015), rig)
			fore.rotation.z = 0.04 * side
			_hand(rig, Vector3(0.235 * side, shoulder_y - 0.52, 0.03), skin_m)
		"folded":
			var up2 := _capsule(0.052, 0.24, sleeve, Vector3(0.2 * side, shoulder_y - 0.13, 0.0), rig)
			up2.rotation.z = 0.12 * side
			var fore2 := _capsule(0.045, 0.22, sleeve, Vector3(0.12 * side, shoulder_y - 0.29, 0.1), rig)
			fore2.rotation.z = 1.25 * side
			fore2.rotation.x = -0.35
			_hand(rig, Vector3(0.015 * side, shoulder_y - 0.31, 0.16), skin_m, 0.0, -1.2)
		"cup":
			var up3 := _capsule(0.052, 0.22, sleeve, Vector3(0.2 * side, shoulder_y - 0.12, 0.02), rig)
			up3.rotation.z = 0.14 * side
			up3.rotation.x = -0.2
			var fore3 := _capsule(0.045, 0.2, sleeve, Vector3(0.19 * side, shoulder_y - 0.16, 0.13), rig)
			fore3.rotation.x = -1.35
			_hand(rig, Vector3(0.18 * side, shoulder_y - 0.06, 0.19), skin_m, 0.0, -0.7)
		"clutch":
			var up4 := _capsule(0.052, 0.22, sleeve, Vector3(0.2 * side, shoulder_y - 0.13, 0.0), rig)
			up4.rotation.z = 0.14 * side
			var fore4 := _capsule(0.045, 0.21, sleeve, Vector3(0.12 * side, shoulder_y - 0.2, 0.1), rig)
			fore4.rotation.z = 0.9 * side
			fore4.rotation.x = -0.75
			_hand(rig, Vector3(0.04 * side, shoulder_y - 0.12, 0.15), skin_m, 0.0, -0.9)
		"pocket":
			var up5 := _capsule(0.052, 0.24, sleeve, Vector3(0.2 * side, shoulder_y - 0.13, 0.0), rig)
			up5.rotation.z = 0.08 * side
			var fore5 := _capsule(0.045, 0.2, sleeve, Vector3(0.21 * side, shoulder_y - 0.34, 0.03), rig)
			fore5.rotation.x = -0.25


## The shared lower body + torso. cfg: skin, skirt/trousers, blouse, floral(bool)
static func _body_base(rig: Node3D, cfg: Dictionary) -> void:
	var skin_m := _flat_mat(cfg.get("skin", SKIN), 0.72)
	## shoes and, if skirted, the calves that show under the hem
	if cfg.has("skirt"):
		var skirt_m: Material = _fabric(cfg["skirt"])
		for sx in [-0.07, 0.07]:
			_boxm(Vector3(0.09, 0.055, 0.2), _flat_mat(Color(0.14, 0.11, 0.09), 0.45), Vector3(sx, 0.028, 0.02), rig)
			_capsule(0.042, 0.18, _flat_mat(Color(0.5, 0.42, 0.36), 0.8), Vector3(sx, 0.19, 0.0), rig)
		_cyl(0.165, 0.24, 0.52, skirt_m, Vector3(0, 0.58, 0), rig)
		## waistband
		_cyl(0.168, 0.17, 0.05, skirt_m, Vector3(0, 0.86, 0), rig)
	else:
		var tr_m: Material = _fabric(cfg.get("trousers", Color(0.1, 0.1, 0.11)))
		for sx in [-0.08, 0.08]:
			_boxm(Vector3(0.1, 0.06, 0.24), _flat_mat(Color(0.1, 0.09, 0.08), 0.5), Vector3(sx, 0.03, 0.03), rig)
			_capsule(0.068, 0.42, tr_m, Vector3(sx, 0.34, 0.0), rig)
			_capsule(0.08, 0.34, tr_m, Vector3(sx, 0.64, 0.0), rig)
		## hips join the legs to the torso
		_cyl(0.16, 0.17, 0.14, tr_m, Vector3(0, 0.83, 0), rig)
	## blouse/shirt torso, slightly stooped with age unless "young"
	var blouse_m: Material
	if cfg.get("floral", false):
		blouse_m = PropKit.fabric("floral_" + str(cfg["blouse"]), cfg["blouse"])
	else:
		blouse_m = _fabric(cfg["blouse"])
	var waist := _cyl(0.16, 0.175, 0.18, blouse_m, Vector3(0, 0.93, 0), rig)
	var chest := _cyl(0.175, 0.165, 0.26, blouse_m, Vector3(0, 1.13, 0), rig)
	## button placket + collar
	for b in 4:
		_sphere(0.008, _flat_mat(cfg["blouse"] * 0.7, 0.4), Vector3(0, 0.98 + 0.075 * float(b), 0.148), rig)
	var col_l := _boxm(Vector3(0.06, 0.045, 0.02), blouse_m, Vector3(-0.045, 1.275, 0.1), rig)
	col_l.rotation.z = 0.5
	var col_r := _boxm(Vector3(0.06, 0.045, 0.02), blouse_m, Vector3(0.045, 1.275, 0.1), rig)
	col_r.rotation.z = -0.5
	## neck
	_cyl(0.042, 0.05, 0.09, skin_m, Vector3(0, 1.31, 0), rig)


## The cardigan: shawl collar, long open fronts, shoulder yoke, cuff ribs.
static func _cardigan(rig: Node3D, tint: Color, length := 0.55) -> void:
	var cm := _fabric(tint)
	_boxm(Vector3(0.38, length, 0.09), cm, Vector3(0, 1.18 - length / 2.0, -0.14), rig)
	for side in [-1.0, 1.0]:
		var front := _boxm(Vector3(0.135, length, 0.06), cm, Vector3(0.11 * side, 1.16 - length / 2.0, 0.135), rig)
		front.rotation.y = 0.08 * side
		## shawl collar strip, angled from shoulder to mid-chest
		var lapel := _boxm(Vector3(0.05, 0.3, 0.05), cm, Vector3(0.065 * side, 1.16, 0.13), rig)
		lapel.rotation.z = 0.28 * side
	_boxm(Vector3(0.4, 0.09, 0.26), cm, Vector3(0, 1.235, -0.01), rig)
	for side in [-1.0, 1.0]:
		_sphere(0.07, cm, Vector3(0.2 * side, 1.2, 0.0), rig)


## ---- Chum, puppet scale ---------------------------------------------------------
## The mascot as the show used him: a cat. Round belly, triangular ears,
## whiskers, bell, tail, one amber eye and one button eye. ~1.05 tall.

## The 1971 pilot: cruder, no bell, yarn whiskers. Dock rows use it for the
## oldest units, so the generations read in order (fur going gray forward).
static func chum_pilot() -> Node3D:
	if ResourceLoader.exists("res://assets/models/chum_1971.glb"):
		return _chum_glb("res://assets/models/chum_1971.glb")
	return _chum_mini_procedural()


static func _chum_glb(path: String) -> Node3D:
	var ps := load(path) as PackedScene
	var inst := ps.instantiate()
	var rig := Node3D.new()
	rig.add_child(inst)
	var nor := "res://assets/textures/fabric_pattern_07_nor_1k.jpg"
	for mi in inst.find_children("*", "MeshInstance3D", true, false):
		var mesh := (mi as MeshInstance3D).mesh
		if mesh == null:
			continue
		for i in mesh.get_surface_count():
			var m := mesh.surface_get_material(i) as BaseMaterial3D
			if m == null:
				continue
			if "Wool" in m.resource_name or "Belly" in m.resource_name:
				var sm := m.duplicate() as BaseMaterial3D
				if ResourceLoader.exists(nor):
					sm.normal_enabled = true
					sm.normal_texture = load(nor)
				sm.uv1_triplanar = true
				sm.uv1_scale = Vector3.ONE * 3.0
				(mi as MeshInstance3D).set_surface_override_material(i, sm)
	return rig


static func chum_mini() -> Node3D:
	## The sculpted 1974 puppet (tools/build_chum_1974.py) when present;
	## the procedural build remains as the fallback.
	if ResourceLoader.exists("res://assets/models/chum_1974.glb"):
		return _chum_glb("res://assets/models/chum_1974.glb")
	return _chum_mini_procedural()


static func _chum_mini_procedural() -> Node3D:
	var rig := Node3D.new()
	var wm := wool()
	var belly_m := wool(Color(0.45, 0.36, 0.24))
	## body and belly patch
	_sphere(0.3, wm, Vector3(0, 0.38, 0), rig)
	var belly := _sphere(0.18, belly_m, Vector3(0, 0.34, 0.17), rig)
	belly.scale = Vector3(1.0, 1.2, 0.45)
	## head
	_sphere(0.22, wm, Vector3(0, 0.82, 0), rig)
	## triangular ears with contrasting inner patches: mustard viewer-left,
	## navy viewer-right (the 1974 plate, exactly)
	var inner_tints := {-1.0: Color(0.72, 0.55, 0.18), 1.0: Color(0.16, 0.2, 0.35)}
	for side in [-1.0, 1.0]:
		var ear := PrismMesh.new()
		ear.size = Vector3(0.14, 0.16, 0.06)
		ear.material = wm
		var emi := MeshInstance3D.new()
		emi.mesh = ear
		emi.position = Vector3(0.12 * side, 1.02, 0)
		emi.rotation.z = 0.15 * side
		rig.add_child(emi)
		var inner := PrismMesh.new()
		inner.size = Vector3(0.08, 0.09, 0.02)
		inner.material = _flat_mat(inner_tints[side], 0.9)
		var imi := MeshInstance3D.new()
		imi.mesh = inner
		imi.position = Vector3(0.12 * side, 1.0, 0.026)
		imi.rotation.z = 0.15 * side
		rig.add_child(imi)
	## the visible center seam on the round head
	_boxm(Vector3(0.008, 0.2, 0.3), _flat_mat(Color(0.2, 0.16, 0.12), 0.9), Vector3(0, 0.95, 0.02), rig)
	## whiskers
	var wmat := _flat_mat(Color(0.62, 0.53, 0.34), 0.9)
	for side in [-1.0, 1.0]:
		for w in 3:
			var wh := _boxm(Vector3(0.2, 0.006, 0.006), wmat, Vector3(0.17 * side, 0.78 + 0.02 * float(w), 0.16), rig)
			wh.rotation.y = 0.35 * side
			wh.rotation.z = (float(w) - 1.0) * 0.18 * side
	## eyes: amber left, button right · nose · stitched smile
	_sphere(0.035, _flat_mat(AMBER, 0.5), Vector3(-0.08, 0.86, 0.19), rig)
	_sphere(0.033, _flat_mat(FELT_BUTTON, 0.35), Vector3(0.08, 0.86, 0.19), rig)
	var nose := PrismMesh.new()
	nose.size = Vector3(0.05, 0.04, 0.03)
	nose.material = _flat_mat(FELT_BUTTON, 0.5)
	var nmi := MeshInstance3D.new()
	nmi.mesh = nose
	nmi.position = Vector3(0, 0.8, 0.2)
	nmi.rotation.x = PI
	rig.add_child(nmi)
	_boxm(Vector3(0.1, 0.014, 0.02), _flat_mat(FELT_BUTTON, 0.35), Vector3(0, 0.73, 0.2), rig)
	## paws with mustard toe caps, collar with the brass keyhole bell that
	## never rings, tail with its navy tip — the plate's patch ledger, honored
	for side in [-1.0, 1.0]:
		_sphere(0.08, wm, Vector3(0.3 * side, 0.42, 0.08), rig)
		_sphere(0.045, _flat_mat(Color(0.72, 0.55, 0.18), 0.85), Vector3(0.3 * side, 0.4, 0.15), rig)
	## rust chest patch and blue arm patch, blanket-stitched in spirit
	_boxm(Vector3(0.09, 0.07, 0.01), _flat_mat(Color(0.55, 0.25, 0.15), 0.95), Vector3(-0.12, 0.52, 0.25), rig)
	_boxm(Vector3(0.06, 0.06, 0.01), _flat_mat(Color(0.25, 0.32, 0.5), 0.95), Vector3(0.28, 0.47, 0.11), rig)
	var collar := TorusMesh.new()
	collar.inner_radius = 0.1
	collar.outer_radius = 0.13
	collar.material = _flat_mat(Color(0.3, 0.18, 0.1), 0.7)
	var cmi := MeshInstance3D.new()
	cmi.mesh = collar
	cmi.position = Vector3(0, 0.62, 0)
	rig.add_child(cmi)
	_sphere(0.045, _flat_mat(Color(0.7, 0.58, 0.28), 0.25), Vector3(0, 0.56, 0.13), rig)
	var tail := _capsule(0.045, 0.4, wm, Vector3(0.16, 0.28, -0.28), rig)
	tail.rotation.x = 0.9
	tail.rotation.z = -0.5
	_sphere(0.05, _flat_mat(Color(0.16, 0.2, 0.35), 0.9), Vector3(0.27, 0.13, -0.43), rig)
	return rig


## ---- Chum, after-fire -------------------------------------------------------------
## The eleven-footer, per the dossier plate: a scorched cat puppet rebuilt from
## salvage. Built at ~2.6 base height; rundown.gd scales the rig to 3.35.
## The right eye socket is left for the caller's tally eye.
## Returns { "rig": Node3D, "head": Node3D, "jaw": Node3D }.

static func chum_hero() -> Dictionary:
	## The sculpted body (tools/build_chum_af.py -> assets/models/chum_af.glb)
	## when present; the procedural build remains as the fallback.
	if ResourceLoader.exists("res://assets/models/chum_af.glb"):
		return _chum_hero_mesh()
	return _chum_hero_procedural()


static func _chum_hero_mesh() -> Dictionary:
	var ps := load("res://assets/models/chum_af.glb") as PackedScene
	var inst := ps.instantiate()
	var rig := Node3D.new()
	rig.add_child(inst)
	var head := inst.find_child("Head", true, false) as Node3D
	var jaw := inst.find_child("Jaw", true, false) as Node3D
	## the remeshed surfaces carry no UVs, so the scanned fabric relief goes
	## on triplanar: wool reads as wool at any scale, per the crafted doctrine
	var nor := "res://assets/textures/fabric_pattern_07_nor_1k.jpg"
	var rgh := "res://assets/textures/fabric_pattern_07_rough_1k.jpg"
	for mi in inst.find_children("*", "MeshInstance3D", true, false):
		var mesh := (mi as MeshInstance3D).mesh
		if mesh == null:
			continue
		for i in mesh.get_surface_count():
			var m := mesh.surface_get_material(i) as BaseMaterial3D
			if m == null:
				continue
			## the lightproof maw: Cycles' zero-emission trick exports to glTF
			## with a white base color, so the game paints it absolute black
			if "MawBlack" in m.resource_name:
				var mb := StandardMaterial3D.new()
				mb.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
				mb.albedo_color = Color.BLACK
				(mi as MeshInstance3D).set_surface_override_material(i, mb)
				continue
			## baked materials (albedo texture present) pass through untouched —
			## Blender's burlap/scorch/grime maps are the ground truth now.
			## The triplanar weave remains only as dressing for unbaked wool.
			if m.albedo_texture != null:
				continue
			if "Wool" in m.resource_name or "Patch" in m.resource_name or "Belly" in m.resource_name:
				var sm := m.duplicate() as BaseMaterial3D
				if ResourceLoader.exists(nor):
					sm.normal_enabled = true
					sm.normal_texture = load(nor)
					sm.normal_scale = 1.0
				if ResourceLoader.exists(rgh):
					sm.roughness_texture = load(rgh)
					sm.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
				sm.uv1_triplanar = true
				sm.uv1_scale = Vector3.ONE * 1.6
				(mi as MeshInstance3D).set_surface_override_material(i, sm)
	return {"rig": rig, "head": head, "jaw": jaw}


static func _chum_hero_procedural() -> Dictionary:
	var rig := Node3D.new()
	var burnt := _fabric(Color(0.14, 0.115, 0.09))     ## scorched body fabric
	var char_dark := _flat_mat(Color(0.07, 0.06, 0.05), 0.95)
	var belly_m := _fabric(Color(0.4, 0.32, 0.2))
	var cable := _flat_mat(Color(0.12, 0.11, 0.1), 0.5)
	var rod := PropKit.metal("chumrod", Color(0.35, 0.33, 0.3))
	## weighted paw feet, toes forward
	for side in [-1.0, 1.0]:
		var foot := _sphere(0.19, burnt, Vector3(0.19 * side, 0.12, 0.05), rig)
		foot.scale = Vector3(1.1, 0.6, 1.4)
		for t in 3:
			_sphere(0.05, char_dark, Vector3(0.19 * side - 0.07 + 0.07 * float(t), 0.08, 0.3), rig)
	## legs with exposed control rods (dossier: leg motion by internal rods)
	for side in [-1.0, 1.0]:
		_capsule(0.13, 0.75, burnt, Vector3(0.19 * side, 0.62, 0), rig)
		_boxm(Vector3(0.03, 0.6, 0.03), rod, Vector3(0.19 * side + 0.1 * side, 0.55, 0.06), rig)
	## the body: round-bellied, patched, burnt
	var body := _sphere(0.46, burnt, Vector3(0, 1.42, 0), rig)
	body.scale = Vector3(1.0, 1.25, 0.9)
	## delta 6, the belly, accessed: darker wool, a central seam opened and
	## resewn repeatedly, dense overlapping restitch scarring
	var belly := _sphere(0.26, _fabric(Color(0.2, 0.16, 0.12)), Vector3(0, 1.32, 0.3), rig)
	belly.scale = Vector3(1.0, 1.3, 0.4)
	for st in 5:
		var stitch := _boxm(Vector3(0.05, 0.014, 0.01), _flat_mat(Color(0.09, 0.08, 0.07), 0.8), Vector3(0, 1.14 + 0.09 * float(st), 0.41), rig)
		stitch.rotation.z = 0.3 if st % 2 == 0 else -0.3
	## delta 7, materials no toy should have: school-gray flannel at the
	## chest, glossy dark leather at the leg. The game never zooms in.
	var flannel_p := _boxm(Vector3(0.16, 0.13, 0.02), _flat_mat(Color(0.45, 0.45, 0.47), 0.95), Vector3(0.12, 1.78, 0.32), rig)
	flannel_p.rotation.x = -0.3
	var leather_p := _boxm(Vector3(0.12, 0.16, 0.02), _flat_mat(Color(0.1, 0.08, 0.07), 0.15), Vector3(-0.24, 0.7, 0.12), rig)
	leather_p.rotation.z = 0.2
	## salvage patches, colors gone dull
	for patch in [
		[Vector3(-0.28, 1.62, 0.26), Color(0.4, 0.18, 0.14), 0.3],
		[Vector3(0.3, 1.5, 0.24), Color(0.2, 0.3, 0.2), -0.2],
		[Vector3(-0.2, 1.14, 0.3), Color(0.35, 0.3, 0.2), 0.5],
	]:
		var pm := _boxm(Vector3(0.18, 0.14, 0.02), _fabric(patch[1]), patch[0], rig)
		pm.rotation.z = patch[2]
		pm.rotation.x = -0.25
	## throat speaker, mounted in the chest (dossier detail 2)
	var spk := _cyl(0.09, 0.09, 0.04, char_dark, Vector3(0, 1.72, 0.36), rig)
	spk.rotation.x = PI / 2.0 - 0.2
	## collar and bell
	var collar := TorusMesh.new()
	collar.inner_radius = 0.2
	collar.outer_radius = 0.26
	collar.material = _flat_mat(Color(0.25, 0.15, 0.1), 0.7)
	var cmi := MeshInstance3D.new()
	cmi.mesh = collar
	cmi.position = Vector3(0, 1.98, 0)
	rig.add_child(cmi)
	_sphere(0.06, _flat_mat(Color(0.7, 0.58, 0.28), 0.25), Vector3(0, 1.9, 0.24), rig)
	## arms: long, tendon-driven; the left shows its cables (dossier detail 3)
	for side in [-1.0, 1.0]:
		var arm := _capsule(0.11, 0.8, burnt, Vector3(0.5 * side, 1.5, 0), rig)
		arm.rotation.z = 0.18 * side
		if side < 0.0:
			for c in 2:
				var tendon := _cyl(0.012, 0.012, 0.78, cable, Vector3(0.5 * side + 0.1 * side, 1.5, 0.05 + 0.04 * float(c)), rig)
				tendon.rotation.z = 0.18 * side
		## clawed hands, big enough to close a distance
		var hand := _sphere(0.14, burnt, Vector3(0.62 * side, 1.02, 0.04), rig)
		hand.scale = Vector3(1.0, 1.2, 1.0)
		for f in 3:
			var claw := _cyl(0.005, 0.025, 0.14, char_dark, Vector3(0.62 * side - 0.06 * side + 0.06 * side * float(f), 0.88, 0.1), rig)
			claw.rotation.x = 0.5
	## the head, and everything the dossier wrote on it
	var head := Node3D.new()
	head.position = Vector3(0, 2.28, 0)
	## delta 8, the tilt: the neck restitched 2-3 degrees off true. The head
	## is permanently cocked, listening. The cheapest, most terrible delta.
	head.rotation.z = 0.045
	rig.add_child(head)
	_sphere(0.34, burnt, Vector3.ZERO, head)
	## triangular ears, one singed shorter
	var ear_sizes := [Vector3(0.24, 0.28, 0.1), Vector3(0.24, 0.2, 0.1)]
	var ear_i := 0
	for side in [-1.0, 1.0]:
		var ear := PrismMesh.new()
		ear.size = ear_sizes[ear_i]
		ear.material = burnt
		var emi := MeshInstance3D.new()
		emi.mesh = ear
		emi.position = Vector3(0.2 * side, 0.36, -0.02)
		emi.rotation.z = 0.18 * side
		head.add_child(emi)
		ear_i += 1
	## delta 4, whisker asymmetry: three singed stubs one side; two
	## replacements the other, too long, too straight, fine dark wire
	var stub_mat := _flat_mat(Color(0.3, 0.24, 0.16), 0.8)
	for w in 3:
		var stub := _boxm(Vector3(0.12, 0.01, 0.01), stub_mat, Vector3(-0.26, -0.06 + 0.045 * float(w), 0.24), head)
		stub.rotation.y = -0.5
		stub.rotation.z = (float(w) - 1.0) * 0.14
	var wire_mat := _flat_mat(Color(0.15, 0.14, 0.13), 0.35)
	for w in 2:
		var wire := _boxm(Vector3(0.6, 0.005, 0.005), wire_mat, Vector3(0.34, -0.04 + 0.05 * float(w), 0.24), head)
		wire.rotation.y = 0.5
		wire.rotation.z = 0.02
	## left eye: the melted button, scorched and warped, in a sunken ring
	var ring := TorusMesh.new()
	ring.inner_radius = 0.045
	ring.outer_radius = 0.075
	ring.material = char_dark
	var rmi := MeshInstance3D.new()
	rmi.mesh = ring
	rmi.position = Vector3(-0.14, 0.08, 0.29)
	rmi.rotation.x = PI / 2.0 - 0.3
	head.add_child(rmi)
	## delta 2, the wrong button: an adult coat button, too large, off-shade,
	## over-attached with excessive thread wraps
	var button := _sphere(0.065, _flat_mat(Color(0.22, 0.17, 0.12), 0.3), Vector3(-0.14, 0.075, 0.3), head)
	button.scale = Vector3(1.0, 0.6, 0.9)
	for w in 3:
		var wrap := _boxm(Vector3(0.015, 0.09, 0.01), _flat_mat(Color(0.09, 0.08, 0.07), 0.8), Vector3(-0.14, 0.075, 0.345), head)
		wrap.rotation.z = -0.6 + 0.6 * float(w)
	## nose: a dark felt triangle
	var nose := PrismMesh.new()
	nose.size = Vector3(0.09, 0.07, 0.05)
	nose.material = char_dark
	var nmi := MeshInstance3D.new()
	nmi.mesh = nose
	nmi.position = Vector3(0, -0.03, 0.32)
	nmi.rotation.x = PI
	head.add_child(nmi)
	## delta 1, the over-grin: the mouth sewn past where a cat's mouth ends,
	## tight vertical ticks in waxed near-black thread; the original smile
	## seam remains beneath as a faint scar
	_boxm(Vector3(0.56, 0.2, 0.12), _flat_mat(Color(0.02, 0.015, 0.012), 1.0), Vector3(0, -0.17, 0.22), head)
	_boxm(Vector3(0.38, 0.008, 0.01), _flat_mat(Color(0.22, 0.18, 0.14), 0.9), Vector3(0, -0.1, 0.3), head)
	for s in 9:
		var st := _boxm(Vector3(0.012, 0.05, 0.015), _flat_mat(Color(0.07, 0.06, 0.05), 0.5), Vector3(-0.24 + 0.06 * float(s), -0.07, 0.3), head)
		st.rotation.z = 0.0
	## the jaw: manual, hinged at the back, the lever inside the mouth
	var jaw := Node3D.new()
	jaw.position = Vector3(0, -0.2, -0.02)
	head.add_child(jaw)
	var jaw_body := _sphere(0.2, burnt, Vector3(0, -0.05, 0.2), jaw)
	jaw_body.scale = Vector3(1.5, 0.45, 1.2)
	for s in 4:
		_boxm(Vector3(0.02, 0.04, 0.015), _flat_mat(Color(0.5, 0.45, 0.35), 0.4), Vector3(-0.12 + 0.08 * float(s), -0.02, 0.4), jaw)
	## hand lever + linkage rod (manual jaw control breakdown, bottom-right plate)
	var lever := _boxm(Vector3(0.025, 0.3, 0.025), rod, Vector3(0.1, -0.22, 0.12), jaw)
	lever.rotation.x = 0.35
	## the tail, dragging low
	var t1 := _capsule(0.07, 0.6, burnt, Vector3(0.1, 0.72, -0.5), rig)
	t1.rotation.x = 1.1
	t1.rotation.z = -0.2
	var t2 := _capsule(0.05, 0.5, burnt, Vector3(0.24, 0.42, -0.82), rig)
	t2.rotation.x = 1.4
	t2.rotation.z = -0.5
	return {"rig": rig, "head": head, "jaw": jaw}


## ---- the named cast, per docs/canon/art ----------------------------------------

## MERLE COTTRY. President. Cook. Caretaker. Maroon cable cardigan, floral
## blouse and floral apron with the stitched 58, gray-brown hair up and
## escaping, reading glasses on a beaded chain, enamel pin, the towel her
## hands are never still without.
static func merle() -> Node3D:
	var rig := Node3D.new()
	var skin := Color(0.74, 0.58, 0.47)
	var skin_m := _flat_mat(skin, 0.72)
	var maroon := Color(0.31, 0.11, 0.11)
	_body_base(rig, {
		"skin": skin, "skirt": Color(0.5, 0.44, 0.33),
		"blouse": Color(0.62, 0.55, 0.4), "floral": true,
	})
	## the apron, floral, over everything: bib, fall, waist tie, pocket
	var apron_m := PropKit.fabric("apron_floral", Color(0.72, 0.66, 0.5))
	var bib := _boxm(Vector3(0.2, 0.24, 0.02), apron_m, Vector3(0, 1.08, 0.148), rig)
	bib.rotation.x = -0.06
	var fall := _boxm(Vector3(0.3, 0.5, 0.02), apron_m, Vector3(0, 0.62, 0.185), rig)
	fall.rotation.x = -0.1
	_boxm(Vector3(0.1, 0.09, 0.015), apron_m, Vector3(0.07, 0.55, 0.2), rig)
	_boxm(Vector3(0.32, 0.03, 0.03), apron_m, Vector3(0, 0.88, 0.15), rig)
	## the 58, stitched in red thread
	_boxm(Vector3(0.05, 0.045, 0.012), _flat_mat(Color(0.48, 0.15, 0.12), 0.9), Vector3(0, 1.05, 0.165), rig)
	_cardigan(rig, maroon, 0.6)
	## arms folded at the waist, the towel between her hands
	var card_m := _fabric(maroon)
	_arm(rig, -1.0, card_m, skin_m, "folded")
	_arm(rig, 1.0, card_m, skin_m, "folded")
	var towel := _boxm(Vector3(0.09, 0.2, 0.03), PropKit.fabric("towel", Color(0.8, 0.75, 0.66)), Vector3(0, 0.78, 0.18), rig)
	towel.rotation.x = 0.1
	_boxm(Vector3(0.09, 0.015, 0.032), _flat_mat(Color(0.6, 0.25, 0.2), 0.9), Vector3(0, 0.72, 0.185), rig)
	## reading glasses on a beaded chain, resting on the chest
	var chain_m := _flat_mat(Color(0.55, 0.45, 0.3), 0.4)
	for c in 7:
		_sphere(0.007, chain_m, Vector3(-0.075 + 0.025 * float(c), 1.22 - 0.03 * absf(float(c) - 3.0), 0.15), rig)
	for gx in [-0.025, 0.025]:
		var rim := TorusMesh.new()
		rim.inner_radius = 0.014
		rim.outer_radius = 0.02
		rim.material = chain_m
		var rmi := MeshInstance3D.new()
		rmi.mesh = rim
		rmi.position = Vector3(gx, 1.1, 0.155)
		rmi.rotation.x = PI / 2.0 - 0.3
		rig.add_child(rmi)
	## the enamel pin, polished daily
	_sphere(0.012, _flat_mat(Color(0.75, 0.6, 0.25), 0.15), Vector3(-0.09, 1.2, 0.14), rig)
	## head: warm, lined, smiling-eyed; messy gray-brown bun
	var head := _head(rig, Vector3(0, 1.46, 0), skin, {"brow": Color(0.42, 0.37, 0.32), "earrings": false})
	_hair(head, Color(0.5, 0.44, 0.38), "bun_messy")
	## a small necklace with a coin pendant
	_sphere(0.01, _flat_mat(Color(0.7, 0.6, 0.4), 0.3), Vector3(0, 1.26, 0.12), rig)
	return rig


## HARRIET. The Continuity Keeper. Chocolate cable cardigan over a cream
## buttoned blouse, brooch at the collar, tweed skirt, silver hair curled
## and pinned high, pearl earrings. Right hand holds the cup; the left,
## the saucer. Mid-motion, always.
static func harriet() -> Node3D:
	var rig := Node3D.new()
	var skin := Color(0.72, 0.59, 0.5)
	var skin_m := _flat_mat(skin, 0.72)
	var brown := Color(0.27, 0.2, 0.14)
	_body_base(rig, {
		"skin": skin, "skirt": Color(0.29, 0.24, 0.18),
		"blouse": Color(0.95, 0.9, 0.78),
	})
	## skirt belt with a small fabric buckle
	_boxm(Vector3(0.14, 0.035, 0.02), _fabric(Color(0.24, 0.2, 0.15)), Vector3(0, 0.865, 0.145), rig)
	_cardigan(rig, brown, 0.55)
	## cardigan buttons, done up once at the sternum
	for b in 3:
		_sphere(0.009, _flat_mat(brown * 0.6, 0.35), Vector3(0, 0.95 + 0.08 * float(b), 0.155), rig)
	## the brooch at the collar
	_sphere(0.014, _flat_mat(Color(0.62, 0.5, 0.3), 0.2), Vector3(0, 1.275, 0.115), rig)
	var card_m := _fabric(brown)
	## the pose the whole game knows: cup raised, saucer held beneath
	_arm(rig, 1.0, card_m, skin_m, "cup")
	_arm(rig, -1.0, card_m, skin_m, "clutch")
	## the saucer, in the left hand (the cup itself is script-owned and rises)
	var saucer := _cyl(0.055, 0.04, 0.012, _flat_mat(Color(0.85, 0.82, 0.74), 0.3), Vector3(-0.04, 1.06, 0.16), rig)
	saucer.rotation.x = 0.05
	## head: upright, precise; silver hair pinned high; pearls
	var head := _head(rig, Vector3(0, 1.46, 0), skin, {"brow": Color(0.5, 0.48, 0.45), "earrings": true})
	_hair(head, Color(0.58, 0.56, 0.52), "bun_neat")
	return rig


## VESS KEYS. Tape hunter. Early 20s, slight, dark washed jacket with the 58
## patch, patterned shirt, pens in the pocket, label maker on the belt,
## plastic pin, dark unruly hair. Wants badly to be chosen.
static func vess() -> Node3D:
	var rig := Node3D.new()
	var skin := Color(0.73, 0.62, 0.54)
	var skin_m := _flat_mat(skin, 0.72)
	_body_base(rig, {
		"skin": skin, "trousers": Color(0.12, 0.115, 0.12),
		"blouse": Color(0.5, 0.33, 0.23), "floral": true,
	})
	## taller, narrower
	rig.scale = Vector3(0.95, 1.07, 0.95)
	## the jacket: washed black, boxy, open
	var jacket := Color(0.13, 0.12, 0.12)
	var jm := _fabric(jacket)
	_boxm(Vector3(0.36, 0.5, 0.075), jm, Vector3(0, 0.95, -0.125), rig)
	for side in [-1.0, 1.0]:
		var front := _boxm(Vector3(0.12, 0.48, 0.05), jm, Vector3(0.11 * side, 0.94, 0.12), rig)
		front.rotation.y = 0.1 * side
		var lapel := _boxm(Vector3(0.055, 0.2, 0.05), jm, Vector3(0.06 * side, 1.16, 0.125), rig)
		lapel.rotation.z = 0.35 * side
	_boxm(Vector3(0.38, 0.08, 0.25), jm, Vector3(0, 1.225, -0.01), rig)
	for side in [-1.0, 1.0]:
		_sphere(0.062, jm, Vector3(0.19 * side, 1.19, 0.0), rig)
	## the 58 CLUB patch, left chest; the plastic pin beneath it
	_cyl(0.028, 0.028, 0.012, _flat_mat(Color(0.75, 0.72, 0.66), 0.8), Vector3(-0.115, 1.13, 0.148), rig).rotation.x = PI / 2.0
	_sphere(0.01, _flat_mat(Color(0.6, 0.58, 0.55), 0.6), Vector3(-0.11, 1.04, 0.15), rig)
	## pens in the chest pocket, chewed
	for pn in 3:
		var pen := _boxm(Vector3(0.008, 0.055, 0.008), _flat_mat([Color(0.7, 0.2, 0.15), Color(0.2, 0.3, 0.6), Color(0.1, 0.1, 0.1)][pn], 0.4), Vector3(0.09 + 0.014 * float(pn), 1.12, 0.145), rig)
		pen.rotation.z = -0.08
	## the label maker, on the belt, always touched
	_boxm(Vector3(0.07, 0.1, 0.04), _flat_mat(Color(0.09, 0.09, 0.1), 0.5), Vector3(0.13, 0.84, 0.11), rig)
	_boxm(Vector3(0.04, 0.014, 0.012), _flat_mat(Color(0.85, 0.83, 0.78), 0.7), Vector3(0.13, 0.87, 0.132), rig)
	## arms: right hand drifting to the label maker, left in a pocket
	_arm(rig, 1.0, jm, skin_m, "pocket")
	_arm(rig, -1.0, jm, skin_m, "down")
	## head: young, pale, dark-eyed, the mop
	var head := _head(rig, Vector3(0, 1.44, 0), skin, {"brow": Color(0.12, 0.1, 0.1), "iris": Color(0.15, 0.12, 0.1)})
	_hair(head, Color(0.09, 0.08, 0.08), "curly_dark")
	return rig


## LELAND MERRICK. Previous archivist. Filed, not shelved. Brown cardigan,
## shirt and dark tie, wire glasses, the legal pad clutched to his chest
## with the green-ink answers. Slightly cropped by every frame; the least
## we can do is build all of him.
static func leland() -> Node3D:
	var rig := Node3D.new()
	var skin := Color(0.7, 0.58, 0.49)
	var skin_m := _flat_mat(skin, 0.72)
	_body_base(rig, {
		"skin": skin, "trousers": Color(0.2, 0.17, 0.14),
		"blouse": Color(0.66, 0.61, 0.51),
	})
	rig.scale = Vector3(0.97, 1.06, 0.97)
	## the tie, loosened
	var tie := _boxm(Vector3(0.045, 0.3, 0.015), _fabric(Color(0.16, 0.13, 0.12)), Vector3(0.01, 1.1, 0.152), rig)
	tie.rotation.z = 0.06
	_cardigan(rig, Color(0.27, 0.2, 0.13), 0.58)
	var card_m := _fabric(Color(0.27, 0.2, 0.13))
	## the legal pad, held to the chest; green ink on the top sheet
	_arm(rig, -1.0, card_m, skin_m, "clutch")
	_arm(rig, 1.0, card_m, skin_m, "clutch")
	var pad := _boxm(Vector3(0.19, 0.26, 0.015), _flat_mat(Color(0.78, 0.7, 0.5), 0.85), Vector3(0, 1.02, 0.17), rig)
	pad.rotation.x = -0.12
	for ln in 5:
		var ink := _boxm(Vector3(0.13, 0.006, 0.006), _flat_mat(Color(0.2, 0.45, 0.25), 0.6), Vector3(0, 1.11 - 0.035 * float(ln), 0.181), rig)
		ink.rotation.x = -0.12
	## a pen behind the pad clip
	_boxm(Vector3(0.01, 0.06, 0.01), _flat_mat(Color(0.1, 0.3, 0.15), 0.4), Vector3(0.08, 1.14, 0.175), rig)
	## head: tired, kind, stubbled; wire glasses; dark hair going grey
	var head := _head(rig, Vector3(0, 1.44, 0), skin, {"brow": Color(0.2, 0.18, 0.16), "stubble": true})
	_hair(head, Color(0.22, 0.2, 0.18), "side_grey")
	## the glasses: two wire rims and a bridge
	var wire := _flat_mat(Color(0.45, 0.4, 0.3), 0.3)
	for gx in [-0.038, 0.038]:
		var rim := TorusMesh.new()
		rim.inner_radius = 0.02
		rim.outer_radius = 0.026
		rim.material = wire
		var rmi := MeshInstance3D.new()
		rmi.mesh = rim
		rmi.position = Vector3(gx, 0.02, 0.096)
		rmi.rotation.x = PI / 2.0 - 0.1
		head.add_child(rmi)
	_boxm(Vector3(0.026, 0.006, 0.006), wire, Vector3(0, 0.024, 0.098), head)
	return rig


## ---- the Floor Manager -----------------------------------------------------------
## Never named, face never fully lit: blacks, a dark cap, headset with the
## coiled cable connected to nothing, the laminated run sheet angled away.
## The right arm is a pivot the script raises for YOU'RE ON. Faces +Z.
## Returns { "rig": Node3D, "arm": Node3D }.

static func floor_manager() -> Dictionary:
	var rig := Node3D.new()
	var blacks := _fabric(Color(0.08, 0.075, 0.07))
	var shadow_skin := Color(0.42, 0.35, 0.3)
	var skin_m := _flat_mat(shadow_skin, 0.85)
	_body_base(rig, {
		"skin": shadow_skin, "trousers": Color(0.08, 0.075, 0.07),
		"blouse": Color(0.09, 0.085, 0.08),
	})
	rig.scale = Vector3(1.0, 1.08, 1.0)
	## the dark work jacket
	_boxm(Vector3(0.36, 0.5, 0.075), blacks, Vector3(0, 0.95, -0.125), rig)
	for side in [-1.0, 1.0]:
		_boxm(Vector3(0.12, 0.48, 0.05), blacks, Vector3(0.11 * side, 0.94, 0.12), rig)
	_boxm(Vector3(0.38, 0.08, 0.25), blacks, Vector3(0, 1.225, -0.01), rig)
	## left arm holds the run sheet, angled away, always
	_arm(rig, -1.0, blacks, skin_m, "clutch")
	var sheet := _boxm(Vector3(0.16, 0.22, 0.012), _flat_mat(Color(0.8, 0.77, 0.68), 0.4), Vector3(-0.06, 1.02, 0.16), rig)
	sheet.rotation.y = 0.6
	sheet.rotation.x = -0.1
	## the right arm: the pivot. At rest it hangs; raised, it points.
	var arm := Node3D.new()
	arm.position = Vector3(0.2, 1.17, 0)
	rig.add_child(arm)
	_capsule(0.052, 0.24, blacks, Vector3(0.015, -0.13, 0.0), arm)
	_capsule(0.045, 0.22, blacks, Vector3(0.03, -0.36, 0.015), arm)
	_hand(arm, Vector3(0.035, -0.52, 0.03), skin_m)
	## head: under a dark cap brim, the face keeps its own shadow
	var head := _head(rig, Vector3(0, 1.44, 0), shadow_skin, {"brow": Color(0.1, 0.09, 0.08), "iris": Color(0.1, 0.08, 0.07)})
	var cap := _sphere(0.112, _flat_mat(Color(0.06, 0.055, 0.05), 0.85), Vector3(0, 0.045, -0.01), head)
	cap.scale = Vector3(0.98, 0.75, 1.0)
	_boxm(Vector3(0.16, 0.015, 0.09), _flat_mat(Color(0.06, 0.055, 0.05), 0.85), Vector3(0, 0.015, 0.115), head)
	## the headset: band, earcups, boom, and the coiled cable to nothing
	var hs := _flat_mat(Color(0.07, 0.065, 0.06), 0.55)
	var band := TorusMesh.new()
	band.inner_radius = 0.105
	band.outer_radius = 0.125
	band.material = hs
	var bmi := MeshInstance3D.new()
	bmi.mesh = band
	bmi.position = Vector3(0, 0.03, 0)
	bmi.rotation.x = 0.2
	head.add_child(bmi)
	for side in [-1.0, 1.0]:
		_sphere(0.035, hs, Vector3(0.105 * side, -0.01, 0.0), head)
	var boom := _boxm(Vector3(0.014, 0.014, 0.1), hs, Vector3(0.07, -0.05, 0.07), head)
	boom.rotation.y = -0.5
	_sphere(0.018, hs, Vector3(0.045, -0.06, 0.105), head)
	## the coil, descending to nowhere
	for c in 6:
		var loop := TorusMesh.new()
		loop.inner_radius = 0.012
		loop.outer_radius = 0.02
		loop.material = hs
		var lmi := MeshInstance3D.new()
		lmi.mesh = loop
		lmi.position = Vector3(0.12, 1.32 - 0.05 * float(c), -0.04)
		lmi.rotation.z = 0.4
		rig.add_child(lmi)
	return {"rig": rig, "arm": arm}
