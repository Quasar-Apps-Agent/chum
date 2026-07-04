class_name RejectedEdit
extends Interactable
## T4.5: Vess threads his own cut. The club's silence has texture.

var tv: BenchTV

var _running := false


func _process(_delta: float) -> void:
	visible = GameState.crate_opened and not GameState.rejected_seen


func get_prompt() -> String:
	return "VESS'S CUT · he is asking without asking (E)"


func interact(_player: Node3D) -> void:
	if _running or GameState.rejected_seen:
		return
	_run()


func _run() -> void:
	_running = true
	GameState.toast("He threads it without meeting anyone's eye. His cut. The one the club never mentions.")
	if tv:
		tv.stage.play_screening(8.0)
	await _wait(3.2)
	GameState.toast("Competent. Loving. Wrong in a way no one can name: transitions landing a half-beat off the show's breath.")
	await _wait(3.4)
	if tv:
		tv.stage.stop_tape()
	GameState.toast("On the final frame the tape stops itself. A clean mechanical refusal. The take-up reel turns backward one rotation, deliberate as a headshake.")
	await _wait(3.6)
	GameState.toast("VESS · 'It does that. Every copy. Every machine.' The pin is in his fist.")
	await _wait(3.0)
	GameState.toast("VESS · 'Your cuts, it keeps. I checked the vault. It keeps yours.'")
	await _wait(3.0)
	GameState.toast("MERLE · soft, hands folded, merciless as weather: 'Sit down, sweetheart. There's cobbler.'")
	GameState.rejected_seen = true
	GameState.save_log()
	_running = false


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
