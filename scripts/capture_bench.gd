class_name CaptureBench
extends Interactable
## Commit 002 stub of the bench's core verb: capture runs in forced real time.
## Leave the bench mid-capture and the take aborts. No skip exists, by design.

const CAPTURE_SECONDS := 12.0
const TETHER := 4.0

var _running := false
var _t := 0.0
var _player: Node3D
var tv: BenchTV
var deck_reels: Array = []  ## reel hubs from PropKit.reel_deck; spun while rolling


func get_prompt() -> String:
	if _running:
		return "TAPE ROLLING · stay with it"
	return "THE BENCH · begin capture, Tape %d (E) · runs real time" % GameState.current_tape


func interact(player: Node3D) -> void:
	if _running:
		return
	_running = true
	GameState.recording = true
	GameState.recording_left = CAPTURE_SECONDS
	if GameState.af_active and not GameState.af_taught:
		var rd := get_tree().get_first_node_in_group("rundown")
		if rd:
			(rd as Node3D).global_position = Vector3(-5.0, 0.0, -16.0)
	GameState.demo_mark("capture_start")
	_t = CAPTURE_SECONDS
	_player = player
	if tv:
		tv.stage.play_tape(CAPTURE_SECONDS)
	GameState.set_capture_status("CAPTURE · TAPE %d · 00:%05.2f" % [GameState.current_tape, _t])


func _physics_process(delta: float) -> void:
	if not _running:
		return
	## tape rolling: supply and take-up turn at their honest, different speeds
	for i in deck_reels.size():
		(deck_reels[i] as Node3D).rotation.z -= delta * (2.6 + 1.1 * float(i))
	if _player and global_position.distance_to(_player.global_position) > TETHER:
		_running = false
		if tv:
			tv.stage.stop_tape()
		GameState.recording = false
		GameState.set_capture_status("")
		GameState.toast("CAPTURE ABORTED · the take is lost. The bench keeps no half-truths.")
		return
	_t -= delta
	if _t <= 0.0:
		_running = false
		GameState.recording = false
		GameState.set_capture_status("")
		GameState.log_capture("TAPE %d · A CLEAN SIGNAL" % GameState.current_tape)
		if GameState.DEMO:
			GameState.demo_mark("capture_done")
			GameState.demo_ended.emit()
	else:
		GameState.recording_left = _t
		GameState.set_capture_status("CAPTURE · TAPE %d · 00:%05.2f" % [GameState.current_tape, _t])
