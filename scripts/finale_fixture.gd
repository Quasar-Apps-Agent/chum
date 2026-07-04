class_name FinaleFixture
extends Interactable
## A premiere fixture: aux panel, boom winch, card stand. Fixes one incident.

var live: Node
var fix_id := ""
var label := ""


func get_prompt() -> String:
	return label


func interact(_player: Node3D) -> void:
	if live:
		live.fix(fix_id)
