class_name BenchTV
extends Node3D
## The bench monitor: a tape stage behind glass, drawn through the artifact
## shader. The slate lies about the generation; the scope does not.

@export var slate_text := "SLATE: 3RD GENERATION DUB · SCOPE READS: MASTER"

var stage: TapeStage

var _mat: ShaderMaterial
var _base_gen := 0.0


func _ready() -> void:
	stage = TapeStage.new()
	add_child(stage)
	var screen := MeshInstance3D.new()
	var quad := QuadMesh.new()
	quad.size = Vector2(1.7, 1.28)
	_mat = ShaderMaterial.new()
	_mat.shader = load("res://shaders/crt_tape.gdshader") as Shader
	_mat.set_shader_parameter("tape_tex", stage.get_texture())
	_mat.set_shader_parameter("generation", 0.0)
	_mat.set_shader_parameter("tbc_on", 1.0 if GameState.tbc_enabled else 0.0)
	quad.material = _mat
	screen.mesh = quad
	add_child(screen)
	var frame := MeshInstance3D.new()
	var fbox := BoxMesh.new()
	fbox.size = Vector3(1.9, 1.46, 0.14)
	var fmat := StandardMaterial3D.new()
	fmat.albedo_color = Color(0.09, 0.08, 0.06)
	fbox.material = fmat
	frame.mesh = fbox
	frame.position = Vector3(0, 0, -0.08)
	add_child(frame)
	var slate := Label3D.new()
	slate.text = slate_text
	slate.font_size = 22
	slate.modulate = Color(0.76, 0.23, 0.18)
	slate.position = Vector3(0, -0.86, 0.02)
	add_child(slate)
	_mat.set_shader_parameter("photo_safe", 1.0 if GameState.photo_safe else 0.0)
	GameState.tbc_changed.connect(_on_tbc)
	GameState.photo_changed.connect(func(on: bool) -> void:
		_mat.set_shader_parameter("photo_safe", 1.0 if on else 0.0)
	)
	stage.lunge_happened.connect(_on_lunge)


func set_generation(g: float) -> void:
	_base_gen = g
	_mat.set_shader_parameter("generation", g)


func set_temp_generation(g: float) -> void:
	_mat.set_shader_parameter("generation", g)


func restore_generation() -> void:
	_mat.set_shader_parameter("generation", _base_gen)


func _on_tbc(on: bool) -> void:
	_mat.set_shader_parameter("tbc_on", 1.0 if on else 0.0)


func _on_lunge() -> void:
	GameState.demo_mark("lunge")
	GameState.toast("ON TAPE · it walked to the lens. It held. One frame.")
