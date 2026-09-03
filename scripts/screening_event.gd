class_name ScreeningEvent
extends Interactable
## The Tape 1 mini-screening, playable: the reel, the line, the sign, the beat.
## SPACE answers with the room. Q improvises, and the show notices.

const BEAT := 0.8
const WINDOW := 3.2

var respond_sign: CueSign
var tv: BenchTV

var _running := false
var _window := false
var _answered := false
var _welapsed := 0.0
var _move_t := 0.0
var _moved := false
var _player: Node3D


func get_prompt() -> String:
	if _running:
		return "THE PROJECTOR · reel running"
	return "THE PROJECTOR · run the mini-screening (E)"


func interact(_player: Node3D) -> void:
	if _running:
		return
	_run()


func _run() -> void:
	_running = true
	GameState.screening_active = true
	if tv:
		tv.stage.play_screening(9.2)
	GameState.toast("The club settles into the rows. The reel threads itself true.")
	await _wait(2.4)
	GameState.toast("ON TAPE · CHUM: 'Goodnight, Gladhouse! Say it with me!'")
	await _wait(1.4)
	GameState.toast("Half the room answers with the tape. In sync. Eyes forward.")
	await _wait(1.4)
	_answered = false
	_moved = false
	_move_t = 0.0
	_welapsed = 0.0
	_window = true
	if respond_sign:
		respond_sign.set_lit(true)
	GameState.toast("THE SIGN PULSES · SPACE on the beat · Q improvises · or hold still")
	var beats := int(WINDOW / BEAT)
	for i in beats:
		if respond_sign:
			respond_sign.flash()
		await _wait(BEAT)
	_window = false
	if respond_sign:
		respond_sign.set_lit(false)
	if not _answered:
		if _moved:
			GameState.toast("You said nothing, but you shifted. On tape, the head tilts toward the shift.")
		else:
			Achievements.unlock("A05")
			GameState.toast("Stillness, held whole. Harriet's cup does not move. The episode resumes.")
	await _wait(1.2)
	GameState.screening_active = false
	GameState.toast("The reel runs out. Somebody is already asking to watch it again.")
	if not GameState.screening_done:
		GameState.demo_mark("screening")
		GameState.screening_done = true
		GameState.save_log()
	_running = false


func _process(delta: float) -> void:
	if not _window:
		return
	_welapsed += delta
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
	var held_still := GameState.assist_on and Input.is_action_pressed("interact")
	if _player and _player.velocity.length() > 0.4 and not held_still:
		_move_t += delta
		if _move_t > 0.3:
			_moved = true


func _on_beat() -> bool:
	var tol := 0.35 if GameState.assist_on else 0.2
	if GameState.is_dead("HARRIET"):
		tol = maxf(0.1, tol - 0.05)
	var phase := fmod(_welapsed, BEAT)
	return phase < tol or phase > BEAT - tol


func _unhandled_input(event: InputEvent) -> void:
	if not _window or _answered:
		return
	if event.is_action_pressed("respond"):
		_answered = true
		if _on_beat():
			Achievements.unlock("A04")
			GameState.toast("ON THE BEAT · 'Goodnight, Gladhouse.' The room exhales; a hand finds your shoulder.")
		else:
			GameState.toast("OFF THE BEAT · the room turns, all of it, one motion.")
	elif event.is_action_pressed("improvise"):
		_answered = true
		if _on_beat():
			GameState.add_pt(10)
			GameState.toast("'Goodnight, everyone.' On the beat. On tape, a delighted laugh. (PT +10)")
		else:
			GameState.add_pt(5)
			GameState.toast("The improvisation lands late. Somewhere, a pencil notes it. (PT +5)")


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
