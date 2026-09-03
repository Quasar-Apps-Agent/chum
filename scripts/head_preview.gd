extends Node3D
## Dev tool: the after-fire head, close, lit like the bench light found him.
## The render target for matching docs/canon/art/after-fire-chum-dossier.png.
## Run: godot res://scenes/head_preview.tscn


func _ready() -> void:
	var parts: Dictionary = CharacterKit.chum_hero()
	var rig := parts["rig"] as Node3D
	add_child(rig)
	## the tally eye, seated exactly as rundown.gd seats it, lit
	var head := parts["head"] as Node3D
	var eye := MeshInstance3D.new()
	var es := SphereMesh.new()
	es.radius = 0.027
	es.height = 0.054
	var em := StandardMaterial3D.new()
	em.emission_enabled = true
	em.emission = Color(0.9, 0.15, 0.1)
	em.emission_energy_multiplier = 2.4
	em.albedo_color = Color(0.5, 0.08, 0.05)
	es.material = em
	eye.mesh = es
	eye.position = Vector3(0.13, 0.06, 0.39)
	head.add_child(eye)
	## jaw slightly open, per the dossier plate's pose
	(parts["jaw"] as Node3D).rotation.x = 0.35
	## portrait light: one warm key high left, a whisper of fill
	var key := OmniLight3D.new()
	key.position = Vector3(-1.2, 3.4, 2.2)
	key.light_color = Color(0.95, 0.75, 0.5)
	key.light_energy = 2.6
	key.omni_range = 10.0
	key.shadow_enabled = true
	add_child(key)
	var fill := OmniLight3D.new()
	fill.position = Vector3(1.6, 1.8, 1.6)
	fill.light_color = Color(0.5, 0.45, 0.4)
	fill.light_energy = 0.5
	fill.omni_range = 8.0
	add_child(fill)
	var env := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color(0.015, 0.013, 0.011)
	## the workshop HDRI feeds reflections only: metals get a real room
	if ResourceLoader.exists("res://assets/env/workshop_1k.hdr"):
		var sky := Sky.new()
		var pm := PanoramaSkyMaterial.new()
		pm.panorama = load("res://assets/env/workshop_1k.hdr")
		pm.energy_multiplier = 0.22
		sky.sky_material = pm
		e.sky = sky
		e.reflected_light_source = Environment.REFLECTION_SOURCE_SKY
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color(0.3, 0.26, 0.22)
	e.ambient_light_energy = 0.14
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	e.glow_enabled = true
	e.glow_intensity = 0.5
	e.glow_hdr_threshold = 0.95
	env.environment = e
	add_child(env)
	var cam := Camera3D.new()
	cam.position = Vector3(0.05, 2.32, 1.35)
	cam.fov = 42.0
	add_child(cam)
	cam.look_at(Vector3(0, 2.32, 0))
	cam.current = true
