class_name NightTrip
extends Node
## Night one's first blood, staged: a breaker lets go, a feed dies, and
## something behind you knows the closing song. Once per save.

var rigs: Array = []

var _armed_t := 0.0


func _process(delta: float) -> void:
	if GameState.night_tripped or not GameState.is_night or GameState.premiere_live:
		_armed_t = 0.0
		return
	_armed_t += delta
	if _armed_t >= 20.0:
		GameState.night_tripped = true
		GameState.save_log()
		_fire()


func _fire() -> void:
	if rigs.size() > 0 and not rigs[0].killed:
		rigs[0].set_killed(true)
	GameState.toast("A breaker lets go somewhere below. A feed drops off the board.")
	await get_tree().create_timer(2.8).timeout
	GameState.toast("Behind you, unhurried: a hummed bar of the closing song.")
	await get_tree().create_timer(2.4).timeout
	GameState.toast("The hall behind you is a hall. The patch bay can fix the rest.")
