class_name ImpossibleCrate
extends Interactable
## Tape 4's delivery, at the front door. Vess, three days of beard, triumphant
## and afraid of his own cargo. Opening it unlocks the seance reel.


func _process(_delta: float) -> void:
	visible = GameState.day >= 2 and not GameState.crate_opened


func get_prompt() -> String:
	return "A CRATE · Vess is hovering (E)"


func interact(_player: Node3D) -> void:
	if GameState.crate_opened:
		return
	GameState.crate_opened = true
	GameState.save_log()
	GameState.toast("VESS · 'Storage auction. Paid cash. Unit was under CRAIK, E. That's Edith. She kept everything.'")
	await get_tree().create_timer(3.2).timeout
	GameState.toast("VESS · 'Tapes dated after the fire. After. Tell me what that means, because I've stopped being able to say it out loud.'")
	await get_tree().create_timer(3.0).timeout
	GameState.toast("The seance reel is on the bench now. He would not carry it further than that.")
