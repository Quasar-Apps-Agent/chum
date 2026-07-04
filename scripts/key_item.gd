class_name KeyItem
extends Interactable
## A key, somewhere it was left. Taking it is remembered.

@export var key_id: String = "KEY"
@export var display: String = "a key"


func get_prompt() -> String:
	return "%s · take (E)" % display.to_upper()


func interact(_player: Node3D) -> void:
	GameState.take_key(key_id, display)
	queue_free()
