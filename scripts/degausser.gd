class_name Degausser
extends Interactable
## The climate room's coil. Burning a daily takes her name off the line.


func get_prompt() -> String:
	if GameState.carried_id >= 0:
		return "THE DEGAUSSER · burn TAKE %d (E)" % GameState.carried_take
	return "THE DEGAUSSER · humming · bring it a daily"


func interact(_player: Node3D) -> void:
	if GameState.carried_id < 0:
		GameState.toast("It hums, felt-throated. It wants a canister.")
		return
	GameState.burn_daily()
