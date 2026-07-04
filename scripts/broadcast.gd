extends Node
## Autoload: the broadcast clock. The building runs on a schedule.
## ON AIR: segments perform. BREAK: windows open and things relocate.

const ON_AIR_SECONDS := 50.0
const BREAK_SECONDS := 18.0

var on_air := true

var _t := ON_AIR_SECONDS

signal phase_changed(now_on_air: bool)


func _process(delta: float) -> void:
	_t -= delta
	if _t <= 0.0:
		on_air = not on_air
		_t = ON_AIR_SECONDS if on_air else BREAK_SECONDS
		phase_changed.emit(on_air)


func time_left() -> float:
	return maxf(_t, 0.0)


func phase_text() -> String:
	var s := int(ceil(time_left()))
	if on_air:
		return "● ON AIR · break in 0:%02d" % s
	return "○ BREAK · window closes 0:%02d" % s
