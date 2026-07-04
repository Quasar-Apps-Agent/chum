class_name Lockdown
extends Node
## Tape 4's turn: every monitor the same frame, doors sealed on schedule,
## and Merle radiant at the head of the room.

var rigs: Array = []
var exterior_doors: Array = []

var _fired := false


func _ready() -> void:
	if GameState.lockdown_done:
		_apply(true)
		_fired = true


func _process(_delta: float) -> void:
	if _fired or GameState.lockdown_done:
		return
	if GameState.assets.size() >= 4 and GameState.is_night:
		_fired = true
		_fire()


func _fire() -> void:
	GameState.toast("Every monitor in the compound cuts to the same channel, on the same frame.")
	_apply(false)
	await get_tree().create_timer(2.2).timeout
	GameState.toast("Doors seal on schedule, not in anger.")
	await get_tree().create_timer(2.2).timeout
	GameState.toast("MERLE · 'Fifty years, and we have a premiere. Lock-in's just till broadcast, dear.'")
	GameState.lockdown_done = true
	GameState.save_log()


func _apply(silent: bool) -> void:
	if rigs.size() > 0:
		var tex: Texture2D = rigs[0].get_feed_texture()
		for rig in rigs:
			rig.sync_to(tex)
	for d in exterior_doors:
		d.locked_reason = "SEALED FOR BROADCAST · lock-in's just till air"
	if silent:
		pass
