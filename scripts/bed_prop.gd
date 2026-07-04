class_name BedProp
extends Interactable
## Rita's bed: the day/night lever. Nights belong to the schedule.


func get_prompt() -> String:
	if GameState.is_night:
		return "RITA'S BED · sleep until morning (E)"
	return "RITA'S BED · end the day (E)"


func interact(_player: Node3D) -> void:
	if GameState.DEMO:
		GameState.toast("The club insists you sleep at home until the contract is signed.")
		return
	if GameState.finale_done:
		GameState.toast("The show is over here. NEW GAME threads a fresh reel.")
		return
	if GameState.decision != "" and GameState.lockdown_done:
		GameState.toast("PLACES. The premiere begins.")
		GameState.start_finale()
		return
	GameState.set_night(not GameState.is_night)
