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
		return "SEANCE REEL · close (E) · Z back · X forward"
	return "SEANCE REEL · the impossible tape · open (E)"


func interact(_player: Node3D) -> void:
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
		GameState.toast("LEGAL PAD · " + ANSWERS[_frame])
	if GameState.seance_wear > 70.0:
		GameState.toast("The frame tears a little more each pass.")


func _show() -> void:
	if tv:
		tv.stage.set_seance_frame(_frame, ANSWERS.get(_frame, ""))
		tv.set_temp_generation(minf(2.0, GameState.seance_wear / 30.0))
	GameState.set_capture_status("SEANCE · FRAME %d · WEAR %.1f%%" % [_frame, GameState.seance_wear])
