class_name FinaleBreaker
extends Interactable
## The patch bay during the premiere. The club is helping.

var live: Node
var label := "CART DECK BREAKER · restore (E)"


func get_prompt() -> String:
	return label


func interact(_player: Node3D) -> void:
	if live:
		live.restored = true
	GameState.toast("RESTORED. The board hums agreement.")
