class_name FireTapePickup
extends Interactable
## The 1977 reel, in Craik's cage. Heavier than it should be.


func get_prompt() -> String:
	return "REEL · 1977 · THE FINALE, UNFINISHED · take (E)"


func interact(_player: Node3D) -> void:
	GameState.has_fire_tape = true
	GameState.save_log()
	GameState.toast("TAKEN · the fire tape. The bench has a dock for it now.")
	queue_free()
