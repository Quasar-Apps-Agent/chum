class_name CreditEntry
extends Interactable
## A margin in the accession ledger. Names can live where findings live.


func _process(_delta: float) -> void:
	visible = GameState.vess_insight and not GameState.vess_credited


func get_prompt() -> String:
	return "LEDGER MARGIN · credit the insight (E) · 'per V. Cardona'"


func interact(_player: Node3D) -> void:
	GameState.vess_credited = true
	GameState.save_log()
	GameState.toast("You write his name where findings live. Somewhere, a label maker clicks twice.")
