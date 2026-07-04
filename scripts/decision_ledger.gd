class_name DecisionLedger
extends Interactable
## Three entries possible in her hand. The pen is the loudest thing in the building.

const CHOICES := ["AUTHENTICATE", "DESTROY", "PERFORM"]
const COMMIT_LINES := {
	"AUTHENTICATE": "AUTHENTICATE. The premiere will go out clean. The club will weep in rows.",
	"DESTROY": "DESTROY. The degausser is warm already. Your hands know how to touch tape.",
	"PERFORM": "PERFORM. Merle, in the doorway, says nothing. The pen was the loudest thing in the building.",
}

var _hover := -1


func _ready() -> void:
	add_to_group("decision_ledger")


func is_pen_up() -> bool:
	return _hover >= 0 and GameState.decision == ""


func get_prompt() -> String:
	if GameState.decision != "":
		return "ACCESSION LEDGER · entry stands: %s · the ink does not entertain appeals" % GameState.decision
	if GameState.day < 3:
		return "ACCESSION LEDGER · three entries possible · the decision ripens Day 3"
	if _hover < 0:
		return "ACCESSION LEDGER · take up the pen (E)"
	return "LEDGER · pen over: %s · E next · SPACE commit" % CHOICES[_hover]


func interact(_player: Node3D) -> void:
	GameState.mark_read("D03")
	if GameState.decision != "" or GameState.day < 3:
		if GameState.decision != "":
			GameState.toast("The entry stands. The ink does not entertain appeals.")
		return
	_hover = (_hover + 1) % CHOICES.size()


func _unhandled_input(event: InputEvent) -> void:
	if GameState.decision != "" or _hover < 0 or GameState.day < 3:
		return
	if event.is_action_pressed("respond") and _is_targeted():
		var choice: String = CHOICES[_hover]
		GameState.decision = choice
		GameState.save_log()
		GameState.toast(COMMIT_LINES[choice])
		_hover = -1


func _is_targeted() -> bool:
	var p := get_tree().get_first_node_in_group("player")
	return p != null and p.has_method("current_target") and p.current_target() == self
