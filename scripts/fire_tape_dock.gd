class_name FireTapeDock
extends Interactable
## The forced watch. Restraint scene: no sting anywhere in it, by law.

var tv: BenchTV

var _running := false


func _process(_delta: float) -> void:
	visible = GameState.has_fire_tape


func get_prompt() -> String:
	if GameState.fire_tape_watched:
		return "DOCK · 1977 · watch it again (E)"
	return "DOCK · 1977 · thread the fire tape (E)"


func interact(_player: Node3D) -> void:
	if _running or not GameState.has_fire_tape:
		return
	_run()


func _run() -> void:
	_running = true
	if tv:
		tv.stage.play_fire(11.0)
	GameState.toast("1977. The studio is emptying.")
	await _wait(2.4)
	GameState.toast("ON TAPE · CHUM: 'Stay in your seats, friends! The Gladhouse loves you! Say it with me: the Gladhouse loves'")
	await _wait(3.6)
	GameState.toast("The line never finishes. The camera pans across an empty floor. No one stands behind it.")
	await _wait(3.2)
	GameState.toast("Transmission ends before any card, any song, any goodnight.")
	if not GameState.fire_tape_watched:
		GameState.fire_tape_watched = true
		GameState.save_log()
	_running = false


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
