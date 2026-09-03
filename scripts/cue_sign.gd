class_name CueSign
extends Node3D
## A studio cue sign. Dark until the show wants an answer.

@export var sign_text: String = "RESPOND"

var _label: Label3D
var _light: OmniLight3D
var _mat: StandardMaterial3D


func _ready() -> void:
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(1.5, 0.55, 0.14)
	_mat = StandardMaterial3D.new()
	_mat.albedo_color = Color(0.09, 0.07, 0.04)
	box.material = _mat
	mesh.mesh = box
	add_child(mesh)
	## the housing: a metal surround and a hood, like every studio sign
	var frame_mat := PropKit.metal("signframe", Color(0.2, 0.2, 0.22))
	var surround := MeshInstance3D.new()
	var sb := BoxMesh.new()
	sb.size = Vector3(1.62, 0.67, 0.1)
	sb.material = frame_mat
	surround.mesh = sb
	surround.position = Vector3(0, 0, -0.03)
	add_child(surround)
	var hood := MeshInstance3D.new()
	var hb := BoxMesh.new()
	hb.size = Vector3(1.66, 0.06, 0.3)
	hb.material = frame_mat
	hood.mesh = hb
	hood.position = Vector3(0, 0.36, 0.06)
	hood.rotation.x = -0.15
	add_child(hood)
	_label = Label3D.new()
	_label.text = sign_text
	_label.font_size = 44
	_label.modulate = Color(0.25, 0.19, 0.1)
	_label.position = Vector3(0, 0, 0.09)
	add_child(_label)
	_light = OmniLight3D.new()
	_light.light_color = Color(0.89, 0.64, 0.24)
	_light.light_energy = 0.0
	_light.omni_range = 4.0
	_light.position = Vector3(0, 0, 0.4)
	add_child(_light)


func flash() -> void:
	if _light == null:
		return
	var tw := create_tween()
	tw.tween_property(_light, "light_energy", 3.8, 0.05)
	tw.tween_property(_light, "light_energy", 2.4, 0.28)


func set_lit(on: bool) -> void:
	_label.modulate = Color(0.95, 0.72, 0.28) if on else Color(0.25, 0.19, 0.1)
	_light.light_energy = 2.4 if on else 0.0
	_mat.albedo_color = Color(0.16, 0.11, 0.05) if on else Color(0.09, 0.07, 0.04)
