extends Node3D
## Dev tool: the cast on one stage, lit like the portraits, for checking the
## builds against docs/canon/art. Run: godot res://scenes/cast_preview.tscn
## (Also the render target the build machine uses to verify character work.)


func _ready() -> void:
	## floor
	var floor_mi := MeshInstance3D.new()
	var fb := BoxMesh.new()
	fb.size = Vector3(20, 0.1, 8)
	fb.material = PropKit.concrete()
	floor_mi.mesh = fb
	floor_mi.position = Vector3(0, -0.05, 0)
	add_child(floor_mi)
	## backdrop
	var wall := MeshInstance3D.new()
	var wb := BoxMesh.new()
	wb.size = Vector3(20, 5, 0.2)
	wb.material = PropKit.plaster()
	wall.mesh = wb
	wall.position = Vector3(0, 2.5, -2.5)
	add_child(wall)
	## the row: the named cast, then the chums
	var merle := CharacterKit.merle()
	merle.position = Vector3(-4.6, 0, 0)
	add_child(merle)
	var harriet := CharacterKit.harriet()
	harriet.position = Vector3(-3.5, 0, 0)
	add_child(harriet)
	var vess := CharacterKit.vess()
	vess.position = Vector3(-2.4, 0, 0)
	add_child(vess)
	var leland := CharacterKit.leland()
	leland.position = Vector3(-1.3, 0, 0)
	add_child(leland)
	var fm: Dictionary = CharacterKit.floor_manager()
	var fm_rig := fm["rig"] as Node3D
	fm_rig.position = Vector3(-0.2, 0, 0)
	add_child(fm_rig)
	var pilot := CharacterKit.chum_pilot()
	pilot.position = Vector3(0.8, 0, 0)
	add_child(pilot)
	var mini := CharacterKit.chum_mini()
	mini.position = Vector3(1.7, 0, 0)
	add_child(mini)
	## the hero, posed mid-fold with the head holding the camera
	var hero: Dictionary = CharacterKit.chum_hero()
	var hero_rig := hero["rig"] as Node3D
	hero_rig.position = Vector3(3.0, -0.35, 0)
	hero_rig.rotation.x = 0.55
	add_child(hero_rig)
	for pv in [["HipL", 0.55], ["HipR", 0.55], ["ShoulderL", -0.7], ["ShoulderR", -0.7]]:
		var n := hero_rig.find_child(pv[0], true, false) as Node3D
		if n:
			n.rotation.x = pv[1]
	var hh := hero["head"] as Node3D
	hh.rotation.x = -0.55
	hh.rotation.y = 0.4
	## the after-fire scale, for reference, and the tally eye lit
	var af: Dictionary = CharacterKit.chum_hero()
	var af_rig := af["rig"] as Node3D
	af_rig.position = Vector3(5.4, 0, -0.6)
	af_rig.scale = Vector3.ONE * (3.35 / 2.6)
	add_child(af_rig)
	var eye := MeshInstance3D.new()
	var es := SphereMesh.new()
	es.radius = 0.06
	es.height = 0.12
	var em := StandardMaterial3D.new()
	em.emission_enabled = true
	em.emission = Color(0.9, 0.15, 0.1)
	em.emission_energy_multiplier = 2.0
	em.albedo_color = Color(0.9, 0.15, 0.1)
	es.material = em
	eye.mesh = es
	eye.position = Vector3(0.14, 0.075, 0.3)
	(af["head"] as Node3D).add_child(eye)
	(af["jaw"] as Node3D).rotation.x = 0.4  ## jaw open, for the record
	## portrait light: one warm key, near darkness elsewhere
	var key := OmniLight3D.new()
	key.position = Vector3(-1.0, 3.2, 3.5)
	key.light_color = Color(0.95, 0.72, 0.45)
	key.light_energy = 2.4
	key.omni_range = 16.0
	key.shadow_enabled = true
	add_child(key)
	var env := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color(0.02, 0.018, 0.015)
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color(0.28, 0.25, 0.21)
	e.ambient_light_energy = 0.12
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.environment = e
	add_child(env)
	var cam := Camera3D.new()
	cam.position = Vector3(0.3, 1.55, 5.6)
	cam.fov = 55.0
	add_child(cam)
	cam.look_at(Vector3(0.3, 1.3, 0))
	cam.current = true
