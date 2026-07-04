class_name Interactable
extends StaticBody3D
## Base class: anything the player's E-key raycast can touch.

@export var prompt: String = "Inspect"


func get_prompt() -> String:
	return prompt


func interact(_player: Node3D) -> void:
	pass
