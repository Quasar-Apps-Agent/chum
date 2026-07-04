class_name CoatPegs
extends Interactable
## The entry pegs: a readable group-state meter. The club's palette drifts.

const NEUTRALS := [Color(0.42, 0.4, 0.38), Color(0.5, 0.48, 0.44), Color(0.36, 0.36, 0.38), Color(0.46, 0.43, 0.4), Color(0.4, 0.42, 0.42)]
const SHOW := [Color(0.79, 0.64, 0.24), Color(0.42, 0.49, 0.23), Color(0.7, 0.35, 0.17), Color(0.79, 0.64, 0.24), Color(0.42, 0.49, 0.23)]

var _mats: Array = []
var _last := -1.0


func _ready() -> void:
	for i in 5:
		var coat := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = Vector3(0.34, 0.8, 0.1)
		var mat := StandardMaterial3D.new()
		box.material = mat
		coat.mesh = box
		coat.position = Vector3(0, -0.45, -0.9 + 0.45 * float(i))
		_mats.append(mat)
		add_child(coat)
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.5, 1.0, 2.2)
	col.shape = shape
	col.position = Vector3(0, -0.45, 0)
	add_child(col)


func _drift() -> float:
	var d := clampf((float(GameState.day) - 1.0) / 4.0, 0.0, 1.0)
	if GameState.lockdown_done:
		d = clampf(d + 0.35, 0.0, 1.0)
	return d


func _process(_delta: float) -> void:
	var d := _drift()
	if absf(d - _last) < 0.01:
		return
	_last = d
	for i in _mats.size():
		_mats[i].albedo_color = NEUTRALS[i].lerp(SHOW[i], d)


func get_prompt() -> String:
	return "COAT PEGS · the club's palette (E)"


func interact(_player: Node3D) -> void:
	if _drift() < 0.3:
		GameState.toast("Cardigans in sensible grays. One mustard scarf, early to the party.")
	elif _drift() < 0.75:
		GameState.toast("The palette is drifting. Nobody has said anything about it, which is itself the thing.")
	else:
		GameState.toast("Show palette, head to toe, every peg. Somebody ironed.")
