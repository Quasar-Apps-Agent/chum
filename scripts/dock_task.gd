class_name DockTask
extends Interactable
## The scene dock inventory. Six units, one anomaly, zero incidents, by contract.

var chums: Array = []

var _counted := 0
var _warm_idx := -1


func setup() -> void:
	if not GameState.dock_done and chums.size() > 0:
		_warm_idx = randi() % chums.size()
	for c in chums:
		c.task = self


func is_warm(c: Node) -> bool:
	return chums.find(c) == _warm_idx


func notify_counted() -> void:
	_counted += 1
	if _counted >= chums.size():
		GameState.dock_done = true
		GameState.save_log()
		GameState.toast("Inventory complete: six units, one anomaly, zero incidents. The dock keeps its word.")


func get_prompt() -> String:
	if GameState.dock_done:
		return "INVENTORY CLIPBOARD · filed · the rows keep their order"
	return "INVENTORY CLIPBOARD · count the units (%d of %d)" % [_counted, chums.size()]


func interact(_player: Node3D) -> void:
	if GameState.dock_done:
		GameState.toast("Filed. Six units. The dock keeps its word.")
	else:
		GameState.toast("Count them by hand. E on each unit. Rows two deep, years in order.")
