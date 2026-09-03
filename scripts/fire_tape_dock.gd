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
	var merle_stays := false
	if not GameState.fire_tape_watched and not GameState.is_dead("MERLE") and not GameState.merle_offered:
		GameState.merle_offered = true
		GameState.toast("MERLE, from the doorway: 'I was there the first time. I'd rather not be alone for the second.'")
		GameState.set_capture_status("E · let her stay for it · Q · turn her away")
		while true:
			await get_tree().process_frame
			if Input.is_action_just_pressed("interact"):
				merle_stays = true
				break
			if Input.is_action_just_pressed("improvise"):
				break
		GameState.set_capture_status("")
		if merle_stays:
			GameState.toast("She pulls a chair to the edge of the light and folds her hands. 'Well then.'")
		else:
			GameState.toast("She nods. 'That's kind, in its way.' The door closes softly behind her.")
		await _wait(1.6)
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
	if not GameState.af_active:
		GameState.af_active = true
		GameState.toast("Something answers the tape from three rooms away. A weighted step. Another.")
		GameState.save_log()
	if merle_stays:
		await _wait(1.2)
		GameState.toast("Merle pats your hand once, warm, and says 'there, that wasn't so'")
		await _wait(2.2)
		GameState.toast("Her chair is empty. Her voice finishes the sentence from inside the speaker: 'bad.'")
		await _wait(2.6)
		GameState.toast("Warm to the last unfinished word. The kettle, two rooms away, clicks off by itself.")
		GameState.show_caption("[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]")
		GameState.mark_casualty("MERLE", "M1 · THE SECOND VIEWING", "carried a second time, mid-sentence")
	_running = false


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
