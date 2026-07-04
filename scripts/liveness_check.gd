class_name LivenessCheck
extends Node
## The invariant, witnessed at runtime: during the cascade, the panel is
## always reachable (window holds waived, console valid). Telemetry to file.

const LOG_PATH := "user://liveness_log.txt"

var console: PatchbayConsole

var _t := 0.0


func _physics_process(delta: float) -> void:
	if not GameState.cascade_active:
		return
	_t += delta
	if _t < 5.0:
		return
	_t = 0.0
	if console == null or not is_instance_valid(console):
		GameState.toast("LIVENESS VIOLATION · the panel is gone. File this.")
		_log("VIOLATION · console invalid")
		return
	_log("OK · console valid · window holds waived · stage %d" % console.cascade_stage)


func _log(text: String) -> void:
	var f := FileAccess.open(LOG_PATH, FileAccess.READ_WRITE)
	if f == null:
		f = FileAccess.open(LOG_PATH, FileAccess.WRITE)
	if f == null:
		return
	f.seek_end()
	f.store_line("[day %d] %s" % [GameState.day, text])
	f.close()
