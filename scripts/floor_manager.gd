class_name FloorManager
extends Interactable
## The constant. Nights, on air, at the stack's end. One hand rises.
## Complete spoken inventory: nothing, here. The hands do the talking.

var _pointed := false
var _gone := false
var _watch_t := 0.0
var _label: Label3D
var _player: Node3D
var _arm: Node3D
var _rig: Node3D


func _process(_gd: float) -> void:
	if GameState.is_dead("FLOOR MANAGER") and not _gone:
		_gone = true
		visible = false


func _ready() -> void:
	## Black-clad, headset to nothing, clipboard angled away. The right arm is
	## the whole vocabulary: it hangs, and it points.
	var parts := CharacterKit.floor_manager()
	_rig = parts["rig"]
	add_child(_rig)
	_arm = parts["arm"]
	var col := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.3
	shape.height = 1.7
	col.shape = shape
	col.position = Vector3(0, 0.85, 0)
	add_child(col)
	_label = Label3D.new()
	_label.text = "FLOOR MANAGER"
	_label.font_size = 30
	_label.modulate = Color(0.4, 0.38, 0.34)
	_label.position = Vector3(0, 1.9, 0)
	_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(_label)
	GameState.night_changed.connect(func(on: bool) -> void:
		if not on:
			_pointed = false
	)


func _physics_process(delta: float) -> void:
	visible = GameState.is_night and Broadcast.on_air and not GameState.premiere_live
	if not visible:
		return
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
		return
	## he watches: the whole body turns to face you, always
	if _rig:
		var to_p := _player.global_position - global_position
		_rig.rotation.y = lerp_angle(_rig.rotation.y, atan2(to_p.x, to_p.z), minf(4.0 * delta, 1.0))
	## the arm: horizontal while a take is watched, hanging otherwise
	if _arm:
		var target := -PI / 2.0 if _watch_t > 0.0 else 0.0
		_arm.rotation.x = lerpf(_arm.rotation.x, target, minf(6.0 * delta, 1.0))
	if _watch_t > 0.0:
		_watch_t -= delta
		var held_still := GameState.assist_on and Input.is_action_pressed("interact")
		if _player.velocity.length() > 0.4 and not held_still:
			_watch_t = 0.0
			_label.text = "FLOOR MANAGER"
			GameState.toast("You moved on camera. Somewhere, a take is ruled spoiled.")
		elif _watch_t <= 0.0:
			_label.text = "FLOOR MANAGER"
			GameState.toast("The hand lowers. The take holds.")
		return
	if _pointed:
		return
	var to_me := global_position - _player.global_position
	if to_me.length() < 9.0:
		var facing := -_player.global_transform.basis.z
		if facing.dot(to_me.normalized()) > 0.5:
			_pointed = true
			_watch_t = 3.0
			_label.text = "YOU'RE ON"
			GameState.toast("YOU'RE ON. The point. Freeze: you are performance now.")


func get_prompt() -> String:
	return "THE FLOOR MANAGER · headphones connected to nothing"


func interact(_player_node: Node3D) -> void:
	if GameState.is_dead("FLOOR MANAGER"):
		return
	GameState.mark_read("D08")
	GameState.toast("The laminated run sheet is angled away from you. It was always going to be.")
