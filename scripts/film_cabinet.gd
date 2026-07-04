class_name FilmCabinet
extends Interactable
## The instructional film: six signals, taught once, trusted forever.

const SIX := ["YOU'RE ON", "CUT", "STRETCH", "WRAP IT UP", "THIRTY SECONDS", "ON TIME"]

var _running := false


func get_prompt() -> String:
	if not GameState.has_key("TRAINING"):
		return "FILM CABINET · LOCKED · the key is tagged TRAINING, in green"
	if GameState.film_watched:
		return "FILM CABINET · run the orientation film again (E)"
	return "FILM CABINET · run the 1971 orientation film (E)"


func interact(_player: Node3D) -> void:
	if not GameState.has_key("TRAINING"):
		GameState.toast("Locked. Somewhere, a key is tagged TRAINING in green ink.")
		return
	if _running:
		return
	_run()


func _run() -> void:
	_running = true
	GameState.toast("WGLD STAFF ORIENTATION, 1971. A floor manager smiles at you across fifty years.")
	await _wait(2.0)
	for sig in SIX:
		GameState.add_show_signal(sig)
		GameState.toast("SIGNAL · %s" % sig)
		await _wait(1.1)
	if not GameState.film_watched:
		GameState.film_watched = true
		GameState.save_log()
		GameState.toast("Six signals. The film rattles out. It never mentions a seventh.")
	else:
		GameState.toast("The film rattles out, patient as ever.")
	_running = false


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
