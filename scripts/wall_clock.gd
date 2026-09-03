class_name WallClock
extends Node3D
## A studio clock repeater: the break-window schedule, readable on walls.

var _label: Label3D


func _ready() -> void:
	## the housing: a studio clock body behind the schedule readout
	var rim := MeshInstance3D.new()
	var rc := CylinderMesh.new()
	rc.top_radius = 0.34
	rc.bottom_radius = 0.34
	rc.height = 0.07
	rc.radial_segments = 20
	rc.material = PropKit.dark_plastic()
	rim.mesh = rc
	rim.rotation.x = PI / 2.0
	add_child(rim)
	var face := MeshInstance3D.new()
	var fc := CylinderMesh.new()
	fc.top_radius = 0.29
	fc.bottom_radius = 0.29
	fc.height = 0.02
	fc.radial_segments = 20
	var fmat := StandardMaterial3D.new()
	fmat.albedo_color = Color(0.87, 0.83, 0.72)
	fmat.roughness = 0.9
	fc.material = fmat
	face.mesh = fc
	face.rotation.x = PI / 2.0
	face.position.z = 0.03
	add_child(face)
	_label = Label3D.new()
	_label.font_size = 44
	_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	_label.position = Vector3(0, -0.55, 0.05)
	add_child(_label)


func _process(_delta: float) -> void:
	_label.text = Broadcast.phase_text()
	_label.modulate = Color(0.89, 0.64, 0.24) if Broadcast.on_air else Color(0.55, 0.78, 0.5)
