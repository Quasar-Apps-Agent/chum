class_name RecChairs
extends Node3D
## The armchairs. Casual until the lockdown converts them, on camera as it
## were, into forward-facing rows. They do not convert back.

const CASUAL := [
	[Vector3(0.6, 0, 0.2), 0.6], [Vector3(2.0, 0, 2.0), -0.9],
	[Vector3(-0.8, 0, 2.4), 1.9], [Vector3(3.2, 0, 0.4), 2.6],
	[Vector3(-2.2, 0, 0.2), -0.4],
]
const ROWS := [
	[Vector3(-1.5, 0, 0.6), -PI / 2.0], [Vector3(0.0, 0, 0.6), -PI / 2.0],
	[Vector3(1.5, 0, 0.6), -PI / 2.0], [Vector3(-0.75, 0, 1.8), -PI / 2.0],
	[Vector3(0.75, 0, 1.8), -PI / 2.0],
]

var _chairs: Array = []
var _arranged := false


func _ready() -> void:
	var colors := [Color(0.5, 0.36, 0.24), Color(0.42, 0.44, 0.3), Color(0.55, 0.42, 0.28), Color(0.38, 0.4, 0.34), Color(0.48, 0.38, 0.3)]
	for i in 5:
		var c := Node3D.new()
		var seat := MeshInstance3D.new()
		var sb := BoxMesh.new()
		sb.size = Vector3(0.6, 0.35, 0.6)
		var mat := StandardMaterial3D.new()
		mat.albedo_color = colors[i]
		sb.material = mat
		seat.mesh = sb
		seat.position = Vector3(0, 0.35, 0)
		c.add_child(seat)
		var back := MeshInstance3D.new()
		var bb := BoxMesh.new()
		bb.size = Vector3(0.6, 0.6, 0.1)
		bb.material = mat
		back.mesh = bb
		back.position = Vector3(0, 0.75, -0.26)
		c.add_child(back)
		c.position = CASUAL[i][0]
		c.rotation.y = CASUAL[i][1]
		add_child(c)
		_chairs.append(c)
	if GameState.lockdown_done:
		_arranged = true
		for i in 5:
			_chairs[i].position = ROWS[i][0]
			_chairs[i].rotation.y = ROWS[i][1]


func _process(_delta: float) -> void:
	if _arranged or not GameState.lockdown_done:
		return
	_arranged = true
	for i in 5:
		var tw := create_tween()
		tw.set_ease(Tween.EASE_IN_OUT)
		tw.set_trans(Tween.TRANS_CUBIC)
		tw.tween_property(_chairs[i], "position", ROWS[i][0], 1.6)
		tw.parallel().tween_property(_chairs[i], "rotation:y", ROWS[i][1], 1.6)
	GameState.toast("Behind you, without a sound worth naming, the armchairs stand in rows now. Facing forward.")
