class_name NoiseTracker
extends Node
## Emits footstep noise for the player at night. The building listens.

var _t := 0.0
var _player: Node3D


func _physics_process(delta: float) -> void:
	if not GameState.is_night or GameState.premiere_live:
		return
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
		return
	if _player.velocity.length() > 0.5:
		_t += delta
		if _t >= 0.6:
			_t = 0.0
			GameState.noise(_player.global_position, 6.0)
