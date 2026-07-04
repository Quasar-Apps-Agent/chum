class_name BotDriver
extends Node
## Soak bots per the invariant suite: WANDERER (random legal movement),
## CHECKER (monitor camping), FAIL (premiere, ignores everything, then passes).

const WB := preload("res://scripts/world_builder.gd")

var mode := "wanderer"

var _player: CharacterBody3D
var _target := Vector3.ZERO
var _idle := 0.0
var _rig_i := 0
var _park := 0.0
var _fail_t := 0.0
var _fail_phase := 0


func _physics_process(delta: float) -> void:
	if _player == null:
		_player = get_tree().get_first_node_in_group("player") as CharacterBody3D
		if _player:
			_pick_wander()
		return
	match mode:
		"wanderer":
			_wander(delta)
		"checker":
			_check(delta)
		"fail":
			_fail(delta)


func _wander(delta: float) -> void:
	if _idle > 0.0:
		_idle -= delta
		_player.velocity = Vector3.ZERO
		return
	var to := _target - _player.global_position
	to.y = 0.0
	if to.length() < 0.6:
		if randf() < 0.3:
			_idle = randf_range(1.0, 3.0)
		_pick_wander()
		return
	var dir := to.normalized()
	_player.velocity = dir * 3.0
	_player.global_position += dir * 3.0 * delta


func _pick_wander() -> void:
	var keys: Array = WB.ROOMS.keys()
	var r: Array = WB.ROOMS[keys[randi() % keys.size()]]
	_target = Vector3(
		r[0] + randf_range(-r[2] / 2.0 + 0.8, r[2] / 2.0 - 0.8),
		1.0,
		r[1] + randf_range(-r[3] / 2.0 + 0.8, r[3] / 2.0 - 0.8)
	)


func _check(delta: float) -> void:
	var rigs := get_tree().get_nodes_in_group("rig")
	if rigs.is_empty():
		_wander(delta)
		return
	var rig: Node = rigs[_rig_i % rigs.size()]
	var mp: Vector3 = rig.monitor_position
	var stand := mp + Vector3(0, 0, 2.0)
	var to := stand - _player.global_position
	to.y = 0.0
	if to.length() > 0.5:
		var dir := to.normalized()
		_player.velocity = dir * 3.0
		_player.global_position += dir * 3.0 * delta
		return
	_player.velocity = Vector3.ZERO
	_player.look_at(Vector3(mp.x, _player.global_position.y, mp.z))
	_park += delta
	if _park > 4.0:
		_park = 0.0
		_rig_i += 1


func _fail(delta: float) -> void:
	_fail_t += delta
	if _fail_phase == 0:
		_player.velocity = Vector3.ZERO
		if _fail_t > 120.0:
			_fail_phase = 1
			Input.action_press("cam_1")
			Input.action_release("cam_1")
		return
	## then go stand the mark and spam the cue through
	var to := LiveProduction.MARK - _player.global_position
	to.y = 0.0
	if to.length() > 0.7:
		var dir := to.normalized()
		_player.velocity = dir * 3.0
		_player.global_position += dir * 3.0 * delta
		return
	_player.velocity = Vector3.ZERO
	if int(_fail_t * 2.0) % 2 == 0:
		Input.action_press("respond")
	else:
		Input.action_release("respond")
