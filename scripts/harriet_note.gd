class_name HarrietNote
extends Interactable
## Folded paper on Harriet's chair. Not on any film.

const SEVENTH := "HOLD YOUR APPLAUSE"


func _process(_delta: float) -> void:
	visible = GameState.film_watched


func get_prompt() -> String:
	return "A FOLDED NOTE · Harriet's hand · read (E)"


func interact(_player: Node3D) -> void:
	GameState.mark_read("D06")
	GameState.add_show_signal(SEVENTH)
	GameState.save_log()
	GameState.toast("'Hold your applause.' Both hands pressed down, twice. They added that one later. You'll want it.")
	queue_free()
