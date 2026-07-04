class_name CompoundDoor
extends Interactable
## A hinged door. Locks state their reasons; keys satisfy them; window-bound
## doors honor the broadcast grammar and move only during the break.

@export var locked_reason: String = ""
@export var required_key: String = ""
@export var door_label: String = "Door"
@export var window_bound: bool = false

var _open := false
var _busy := false
var _key_toasted := false


func is_open() -> bool:
	return _open


func _locked() -> bool:
	if locked_reason == "":
		return false
	return not (required_key != "" and GameState.has_key(required_key))


func get_prompt() -> String:
	if _locked():
		return "%s · %s" % [door_label, locked_reason]
	if window_bound and Broadcast.on_air and not GameState.cascade_active:
		return "%s · HELD FOR AIR · moves on the break" % door_label
	return "%s · %s (E)" % [door_label, "close" if _open else "open"]


func interact(_player: Node3D) -> void:
	if _busy:
		return
	if _locked():
		GameState.toast(locked_reason)
		return
	if window_bound and Broadcast.on_air and not GameState.cascade_active:
		GameState.toast("HELD FOR AIR · the door moves during the break window.")
		return
	if required_key != "" and not _key_toasted:
		_key_toasted = true
		GameState.toast("The %s key turns. It was cut for this." % required_key)
	_busy = true
	_open = not _open
	Sfx.thunk(global_position)
	GameState.noise(global_position, 8.0)
	var target := -1.75 if _open else 0.0
	var tw := create_tween()
	tw.set_ease(Tween.EASE_OUT)
	tw.set_trans(Tween.TRANS_CUBIC)
	tw.tween_property(self, "rotation:y", target, 0.45)
	tw.tween_callback(func() -> void: _busy = false)
