extends Node3D
## Dev tool: the tendon arm, close, for checking against the dossier's
## construction detail 3. Run: godot res://scenes/arm_preview.tscn


func _ready() -> void:
	var parts: Dictionary = CharacterKit.chum_hero()
	add_child(parts["rig"] as Node3D)
	var key := OmniLight3D.new()
	key.position = Vector3(-1.6, 2.6, 1.8)
	key.light_color = Color(0.95, 0.75, 0.5)
	key.light_energy = 2.2
	key.omni_range = 9.0
	key.shadow_enabled = true
	add_child(key)
	var fill := OmniLight3D.new()
	fill.position = Vector3(0.8, 1.0, 1.4)
	fill.light_color = Color(0.5, 0.45, 0.4)
	fill.light_energy = 0.4
	fill.omni_range = 7.0
	add_child(fill)
	var env := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color(0.015, 0.013, 0.011)
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color(0.3, 0.26, 0.22)
	e.ambient_light_energy = 0.14
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.environment = e
	add_child(env)
	var cam := Camera3D.new()
	cam.position = Vector3(-1.15, 1.1, 1.25)
	cam.fov = 45.0
	add_child(cam)
	cam.look_at(Vector3(-0.56, 1.05, 0))
	cam.current = true
