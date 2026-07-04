class_name Cascade
extends Node
## Spike 6's pass line: the Night 4 sequence, end to end. Trip, spread,
## ordered restoration, and circuit F, which cannot be de-energized.

var rigs: Array = []
var console: PatchbayConsole

var _fired := false


func _process(_delta: float) -> void:
	if _fired or GameState.cascade_done or GameState.premiere_live:
		return
	if GameState.is_night and GameState.day >= 4:
		_fired = true
		_run()


func _run() -> void:
	GameState.cascade_active = true
	GameState.set_blackout(0.55)
	_kill_range(2, 4)
	GameState.toast("PANEL EVENT · circuit C lets go. The stage end of the building drops dark.")
	await _wait(4.0)
	GameState.toast("The dark spreads room to room, patient, like it is reading the labels.")
	await _wait(16.0)
	if GameState.cascade_done:
		return
	GameState.set_blackout(0.75)
	_kill_range(4, 6)
	GameState.toast("Circuit B follows. The dark is administrative now. The panel is in the patch bay.")
	if console:
		console.cascade_stage = 1
	while console and console.cascade_stage != 0:
		await get_tree().process_frame
	GameState.cascade_active = false
	GameState.cascade_done = true
	GameState.save_log()
	GameState.toast("The panel holds. Circuit F never so much as flickered. It cannot be de-energized. You have read that somewhere.")


func _kill_range(a: int, b: int) -> void:
	for i in range(a, mini(b, rigs.size())):
		if not rigs[i].killed:
			rigs[i].set_killed(true)


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
