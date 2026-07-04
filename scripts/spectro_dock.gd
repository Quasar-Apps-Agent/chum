class_name SpectroDock
extends Interactable
## The audio bench. The verse lives under the closing song, in the sidebands.

var _running := false


func get_prompt() -> String:
	if GameState.assets.has("VERSE"):
		return "SPECTROGRAM · the verse is banked"
	if GameState.captures.size() == 0:
		return "SPECTROGRAM · needs a captured tape first"
	return "SPECTROGRAM · pull the sidebands (E)"


func interact(_player: Node3D) -> void:
	if _running or GameState.assets.has("VERSE") or GameState.captures.size() == 0:
		return
	_run()


func _run() -> void:
	_running = true
	GameState.toast("Structure in the sidebands. Not noise. Words.")
	await get_tree().create_timer(2.2).timeout
	GameState.toast("RECOVERED · 'Close the door and dim the light. Fold the day away.'")
	await get_tree().create_timer(2.4).timeout
	GameState.toast("'Everyone we love is home. And no one has to stay.'")
	GameState.gain_asset("VERSE", "the missing verse")
	_running = false
