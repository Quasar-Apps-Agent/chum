class_name VessBinder
extends Interactable
## His research, in his room, door ajar. One true insight, one confident error.


func _process(_delta: float) -> void:
	visible = not GameState.vess_insight


func get_prompt() -> String:
	return "VESS'S RESEARCH BINDER · read (E) · his door was ajar"


func interact(_player: Node3D) -> void:
	GameState.mark_read("D07")
	GameState.vess_insight = true
	GameState.save_log()
	GameState.toast("His insight, real: the slate-number skips are clustered, not random. Nobody else saw it.")
	await get_tree().create_timer(2.6).timeout
	GameState.toast("Also, in confident block letters, a theory that is wrong. You close the binder the way you found it.")
