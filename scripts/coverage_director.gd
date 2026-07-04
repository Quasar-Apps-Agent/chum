class_name CoverageDirector
extends Node
## v0 of the thing that watches how you watch. Profiles the player at night
## (checker, sprinter, hider) from behavior, never from menus. Burning dailies
## resets its read, honoring the promise the burn message has made since 006.

var rigs: Array = []

const LOG_PATH := "user://coverage_log.txt"

var _player: Node3D
var _monitor_s := 0.0
var _moving_s := 0.0
var _still_s := 0.0
var _watched: Dictionary = {}
var _save_t := 0.0


func _ready() -> void:
	GameState.daily_burned.connect(reset_read)
	_monitor_s = GameState.cov_monitor
	_moving_s = GameState.cov_move
	_still_s = GameState.cov_still
	log_line("SESSION OPEN · restored counters m=%.1f mv=%.1f st=%.1f" % [_monitor_s, _moving_s, _still_s])


func log_line(text: String) -> void:
	var f := FileAccess.open(LOG_PATH, FileAccess.READ_WRITE)
	if f == null:
		f = FileAccess.open(LOG_PATH, FileAccess.WRITE)
	if f == null:
		return
	f.seek_end()
	f.store_line("[day %d %s] %s" % [GameState.day, "night" if GameState.is_night else "day", text])
	f.close()


func _physics_process(delta: float) -> void:
	if not GameState.is_night:
		return
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
		return
	var moving: bool = _player.velocity.length() > 0.5
	if moving:
		_moving_s += delta
	else:
		_still_s += delta
	for rig in rigs:
		var to_mon: Vector3 = rig.monitor_position - _player.global_position
		if to_mon.length() < 3.5:
			var facing := -_player.global_transform.basis.z
			if facing.dot(to_mon.normalized()) > 0.6:
				_monitor_s += delta
				_watched[rig] = float(_watched.get(rig, 0.0)) + delta
	GameState.coverage_label = profile()
	_save_t += delta
	if _save_t > 5.0:
		_save_t = 0.0
		GameState.cov_monitor = _monitor_s
		GameState.cov_move = _moving_s
		GameState.cov_still = _still_s


func profile() -> String:
	if _monitor_s < 2.0 and _moving_s < 4.0 and _still_s < 4.0:
		return "AUDIENCE"
	if _monitor_s >= _moving_s and _monitor_s >= _still_s:
		return "CHECKER"
	if _moving_s >= _still_s:
		return "SPRINTER"
	return "HIDER"


func most_watched_rig() -> MonitorRig:
	var best: MonitorRig = null
	var best_t := 0.0
	for rig in _watched.keys():
		var t := float(_watched[rig])
		if t > best_t:
			best_t = t
			best = rig
	return best


func reset_read() -> void:
	_monitor_s = 0.0
	_moving_s = 0.0
	_still_s = 0.0
	_watched.clear()
	GameState.cov_monitor = 0.0
	GameState.cov_move = 0.0
	GameState.cov_still = 0.0
	GameState.coverage_label = "AUDIENCE"
	log_line("READ RESET · dailies burned")
