class_name DailiesCanister
extends Interactable
## A canister labeled SCENE/TAKE. Its existence is a record of your worst nights.

var daily_id := -1
var take := 0


func get_prompt() -> String:
	return "DAILIES · SCENE 4 TAKE %d · pick up (E)" % take


func interact(_player: Node3D) -> void:
	if GameState.carried_id >= 0:
		GameState.toast("Hands full. One canister at a time.")
		return
	GameState.pick_daily(daily_id, take)
	queue_free()
