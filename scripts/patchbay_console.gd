class_name PatchbayConsole
extends Interactable
## Routing v0: one amperage budget, two circuits. Something is always dark.

var control_lights: Array = []
var hall_lights: Array = []
var control_rig: MonitorRig

var _control_live := true


func apply_initial() -> void:
	_apply()


var cascade_stage := 0


func get_prompt() -> String:
	if cascade_stage == 1:
		return "PANEL · RESTORE CIRCUIT B (E) · order matters"
	if cascade_stage == 2:
		return "PANEL · RESTORE CIRCUIT C (E)"
	if _any_killed():
		return "PATCHBAY · dead feed on the board · re-patch (E)"
	var live := "CONTROL RUN" if _control_live else "STAGE HALL"
	return "PATCHBAY · %s live · re-route (E)" % live


func _any_killed() -> bool:
	if control_rig and control_rig.killed:
		return true
	return false


func interact(_player: Node3D) -> void:
	if cascade_stage == 1:
		cascade_stage = 2
		GameState.set_blackout(0.55)
		GameState.toast("CIRCUIT B RESTORED · half the dark stands down. B before C, the way the panel is labeled.")
		return
	if cascade_stage == 2:
		cascade_stage = 0
		GameState.set_blackout(0.0)
		GameState.toast("CIRCUIT C RESTORED · the building remembers its own light.")
		return
	if _any_killed():
		control_rig.set_killed(false)
		GameState.toast("RE-PATCHED · the feed climbs back onto the board.")
		return
	_control_live = not _control_live
	_apply()
	var live := "CONTROL RUN" if _control_live else "STAGE HALL"
	var dark := "STAGE HALL" if _control_live else "CONTROL RUN"
	GameState.toast("PATCHED · %s live · %s dark. The budget is the budget." % [live, dark])


func _apply() -> void:
	for l in control_lights:
		l.visible = _control_live
	for l in hall_lights:
		l.visible = not _control_live
	if control_rig:
		control_rig.set_powered(_control_live)
