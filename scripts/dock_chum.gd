class_name DockChum
extends Interactable
## A retired unit on its armature. One of them is warm. Nothing follows. Ever.

var task: Node
var idx := 0
var counted := false


func get_prompt() -> String:
	if counted or GameState.dock_done:
		return "UNIT %d · counted" % idx
	return "UNIT %d · count (E)" % idx


func interact(_player: Node3D) -> void:
	if counted or GameState.dock_done:
		return
	counted = true
	if task and task.is_warm(self):
		GameState.toast("Your gloved hand rests on it. It is warm. You write the number down anyway.")
	else:
		GameState.toast("UNIT %d · fur gone gray in order." % idx)
	if task:
		task.notify_counted()
