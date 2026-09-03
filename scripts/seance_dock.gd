class_name SeanceDock
extends Interactable
## Frame stepping through the impossible tape. Every pass wears the only
## copy of him. Z back, X forward. Five answers live at fixed frames.

const ANSWERS := {
	7: "FILED. NOT SHELVED.",
	14: "IT ASKED ME TO STAND IN. NEVER ACCEPT A ROLE.",
	21: "FINISH THE FINALE. FORMAT KEEPS ITS OWN RULES.",
	28: "ONLY IF THE HOUSE CLOSES WITH SOMEONE INSIDE. LET IT BE ME.",
	35: "I'VE READ THE ENDING. IT'S GOOD.",
}
const MAX_FRAME := 40

var tv: BenchTV

var _open := false
var _frame := 0


func _process(_delta: float) -> void:
	visible = GameState.crate_opened
	if not visible and _open:
		_open = false
		GameState.set_capture_status("")


func get_prompt() -> String:
	if _open:
		var extra := ""
		if GameState.has_fire_tape:
			extra += " · Q feed the fire tape into the wake"
		if GameState.leland_answers.size() >= 5 and GameState.seance_wear > 70.0:
			extra += " · SPACE the pad has room for a sixth line"
		return "SEANCE REEL · close (E) · Z back · X forward" + extra
	return "SEANCE REEL · the impossible tape · open (E)"


func interact(_player: Node3D) -> void:
	if GameState.is_dead("LELAND"):
		GameState.toast("The dock is a box with a window now. Nothing reads.")
		return
	GameState.mark_read("D01")
	_open = not _open
	if _open:
		_show()
	else:
		if tv:
			tv.stage.seance_end()
			tv.restore_generation()
		GameState.set_capture_status("")


func _unhandled_input(event: InputEvent) -> void:
	if not _open:
		return
	if event.is_action_pressed("improvise") and GameState.has_fire_tape and not GameState.is_dead("LELAND"):
		_l2_reading()
		return
	if event.is_action_pressed("respond") and GameState.leland_answers.size() >= 5 			and GameState.seance_wear > 70.0 and not GameState.is_dead("LELAND"):
		_l1_sixth()
		return
	if event.is_action_pressed("frame_back"):
		_frame = maxi(0, _frame - 1)
		_step()
	elif event.is_action_pressed("frame_fwd"):
		_frame = mini(MAX_FRAME, _frame + 1)
		_step()


func _step() -> void:
	GameState.add_wear(1.5)
	_show()
	if ANSWERS.has(_frame) and not GameState.leland_answers.has(_frame):
		GameState.leland_answers.append(_frame)
		GameState.save_log()
		var a: String = ANSWERS[_frame]
		if _frame == 14 and GameState.is_dead("HARRIET"):
			a = "SHE WAS THE ONLY ONE WHO PAUSED PROPERLY."
		if _frame == 28 and GameState.is_dead("MERLE"):
			a = "I KNOW. SHE'S HERE NOW."
		GameState.toast("LEGAL PAD · " + a)
	if GameState.seance_wear > 70.0:
		GameState.toast("The frame tears a little more each pass.")


func _show() -> void:
	if tv:
		tv.stage.set_seance_frame(_frame, ANSWERS.get(_frame, ""))
		tv.set_temp_generation(minf(2.0, GameState.seance_wear / 30.0))
	GameState.set_capture_status("SEANCE · FRAME %d · WEAR %.1f%%" % [_frame, GameState.seance_wear])


func _l1_sixth() -> void:
	GameState.toast("The pad takes a sixth line. The wear takes the rest.")
	await get_tree().create_timer(2.6).timeout
	GameState.toast("His print burns from the inside of the frames, whitening as you watch.")
	await get_tree().create_timer(2.6).timeout
	GameState.toast("Green ink drains upward out of every note in the building, back into nowhere.")
	GameState.show_caption("[THE INK LEAVES THE PAPER]")
	await get_tree().create_timer(2.6).timeout
	GameState.toast("He is retroactively unfound. The reel is blank leader, end to end.")
	GameState.mark_casualty("LELAND", "L1 · THE SIXTH QUESTION", "asked past the wear; unfound, retroactively")
	_open = false
	if tv:
		tv.stage.seance_end()
		tv.restore_generation()
	GameState.set_capture_status("")


func _l2_reading() -> void:
	GameState.toast("You feed 1977 into the wake.")
	await get_tree().create_timer(2.6).timeout
	GameState.toast("The unfinished sign-off completes itself, in a reading voice you know from green ink:")
	await get_tree().create_timer(2.4).timeout
	GameState.toast("'There's no one at home anymore. The lights are off in the little house. Say goodnight, Chum.'")
	await get_tree().create_timer(3.0).timeout
	GameState.toast("The five answers un-write, last to first. The final frame: the little door, closing from the inside. A hand on the inner knob.")
	GameState.show_caption("[THE SIGN-OFF, WHOLE]")
	await get_tree().create_timer(3.0).timeout
	GameState.toast("He got to finish it.")
	GameState.has_fire_tape = false
	GameState.leland_answers = []
	GameState.signoff_completed = true
	GameState.mark_casualty("LELAND", "L2 · THE READING", "finished it; the door closed from the inside")
	_open = false
	if tv:
		tv.stage.seance_end()
		tv.restore_generation()
	GameState.set_capture_status("")
