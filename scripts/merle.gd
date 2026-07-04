class_name Merle
extends Interactable
## Merle Cottry, on her schedule: the kettle by day, her chair by night,
## and the doorway, saying nothing, when the pen is up.

const SPEED := 1.6
const KETTLE := Vector3(8.0, 0.0, -1.0)
const CHAIR := Vector3(2.6, 0.0, 1.2)
const DOORWAY := Vector3(6.0, 0.0, -16.4)


func _physics_process(delta: float) -> void:
	var target := _where()
	global_position = global_position.move_toward(target, SPEED * delta)


func _where() -> Vector3:
	if GameState.screening_active:
		return Vector3(0.4, 0.0, 1.4)
	if _pen_up():
		return DOORWAY
	if GameState.is_night or GameState.lockdown_done:
		return CHAIR
	return KETTLE


func _pen_up() -> bool:
	for n in get_tree().get_nodes_in_group("decision_ledger"):
		if n.has_method("is_pen_up") and n.is_pen_up():
			return true
	return false


func get_prompt() -> String:
	var where := "in the doorway" if _pen_up() else ("in her chair" if GameState.is_night else "at the kettle")
	return "MERLE · %s (E)" % where


func interact(_player: Node3D) -> void:
	if _pen_up():
		GameState.toast("She says nothing. Her hands are empty and open, watching the pen.")
		return
	if GameState.crate_opened and not GameState.merle_1974:
		_monologue()
		return
	if GameState.decision == "PERFORM":
		GameState.toast("MERLE · 'You'll be wonderful. You were always going to be.'")
	elif GameState.decision == "AUTHENTICATE":
		GameState.toast("MERLE · 'The whole world gets to be carried now.'")
	elif GameState.decision == "DESTROY":
		GameState.toast("MERLE · 'The degausser hums at night. I hear it too.' Her hands keep drying the plate.")
	elif GameState.day == 1:
		GameState.toast("MERLE · 'Oh, look at your gloves. You brought your own gloves.'")
	elif GameState.day == 2:
		GameState.toast("MERLE · 'He asks so many questions. You ask the right amount. I can tell.'")
	else:
		GameState.toast("MERLE · 'You've given us back a piece of our childhood, do you know that?'")


func _monologue() -> void:
	GameState.merle_1974 = true
	GameState.save_log()
	GameState.toast("MERLE · 'I was seven. Route 9, the culvert end, past where the county stopped mowing.'")
	await _wait(3.2)
	GameState.toast("'I walked out after a dog that wasn't mine, and the light went, and the corn does not care how loud a girl is.'")
	await _wait(3.4)
	GameState.toast("Her hands, for once, empty and open. 'And then the dark got warmer. Fur like a coat closet.'")
	await _wait(3.2)
	GameState.toast("'It carried me the whole way singing the closing song, and it set me down where the porch light reached.'")
	await _wait(3.2)
	GameState.toast("'The papers said a searcher found me. No searcher sings.'")
	await _wait(3.0)
	GameState.toast("'So bring me every date and every gap and every terrible arithmetic, and I will hold them. I promise you I will hold them.'")
	await _wait(3.4)
	GameState.toast("'But I was carried. You don't vote against being carried.'")


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
