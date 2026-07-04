class_name WallClock
extends Node3D
## A studio clock repeater: the break-window schedule, readable on walls.

var _label: Label3D


func _ready() -> void:
	_label = Label3D.new()
	_label.font_size = 44
	_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(_label)


func _process(_delta: float) -> void:
	_label.text = Broadcast.phase_text()
	_label.modulate = Color(0.89, 0.64, 0.24) if Broadcast.on_air else Color(0.55, 0.78, 0.5)
