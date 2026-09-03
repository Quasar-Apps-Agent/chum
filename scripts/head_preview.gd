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
	## LOOK-DEV RIG (plan §R, unit 1.0b): the acceptance view's light stack.
	## Soft area-style key through a spot, cool rim, bounce handled by SSIL —
	## and the full modern pipeline: SSAO, SSIL, SDFGI, volumetric fog, AgX.
	var key := SpotLight3D.new()
	key.position = Vector3(-1.4, 3.5, 2.4)
	key.look_at_from_position(key.position, Vector3(0, 2.3, 0))
	key.light_color = Color(1.0, 0.82, 0.6)
	key.light_energy = 11.0
	key.spot_range = 12.0
	key.spot_angle = 38.0
	key.spot_angle_attenuation = 1.6
	key.shadow_enabled = true
	key.shadow_blur = 2.4
	key.light_volumetric_fog_energy = 1.6
	add_child(key)
	var rim := SpotLight3D.new()
	rim.position = Vector3(1.9, 3.0, -1.6)
	rim.look_at_from_position(rim.position, Vector3(0, 2.5, 0))
	rim.light_color = Color(0.6, 0.7, 0.95)
	rim.light_energy = 8.0
	rim.spot_range = 10.0
	rim.spot_angle = 40.0
	rim.shadow_enabled = true
	rim.shadow_blur = 2.0
	add_child(rim)
	var fill := OmniLight3D.new()
	fill.position = Vector3(1.6, 1.8, 1.8)
	fill.light_color = Color(0.5, 0.45, 0.4)
	fill.light_energy = 0.35
	fill.omni_range = 8.0
	add_child(fill)
	## a floor and back wall so GI and AO have something to bounce from
	var room := MeshInstance3D.new()
	var rb := BoxMesh.new()
	rb.size = Vector3(14, 0.2, 14)
	var rm := StandardMaterial3D.new()
	rm.albedo_color = Color(0.09, 0.08, 0.07)
	rm.roughness = 0.95
	rb.material = rm
	room.mesh = rb
	room.position = Vector3(0, -0.1, 0)
	add_child(room)
	var wall := MeshInstance3D.new()
	var wb := BoxMesh.new()
	wb.size = Vector3(14, 8, 0.2)
	wb.material = rm
	wall.mesh = wb
	wall.position = Vector3(0, 3.9, 2.4)
	add_child(wall)
	var env := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color(0.008, 0.007, 0.006)
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
	e.ambient_light_color = Color(0.28, 0.24, 0.2)
	e.ambient_light_energy = 0.06
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	e.tonemap_exposure = 1.15
	e.tonemap_white = 6.0
	e.ssao_enabled = true
	e.ssao_intensity = 2.4
	e.ssao_radius = 0.6
	e.ssao_detail = 1.0
	e.ssil_enabled = true
	e.ssil_intensity = 1.2
	e.sdfgi_enabled = true
	e.sdfgi_use_occlusion = true
	e.sdfgi_bounce_feedback = 0.6
	e.sdfgi_min_cell_size = 0.05
	e.volumetric_fog_enabled = true
	e.volumetric_fog_density = 0.008
	e.volumetric_fog_albedo = Color(0.6, 0.55, 0.5)
	e.volumetric_fog_emission_energy = 0.0
	e.volumetric_fog_anisotropy = 0.5
	e.glow_enabled = true
	e.glow_intensity = 0.55
	e.glow_bloom = 0.05
	e.glow_hdr_threshold = 1.1
	env.environment = e
	add_child(env)
	var cam := Camera3D.new()
	cam.position = Vector3(0.05, 2.32, 1.35)
	cam.fov = 42.0
	add_child(cam)
	cam.look_at(Vector3(0, 2.32, 0))
	cam.current = true
