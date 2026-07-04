class_name CastingSheetProp
extends Interactable
## The death counter as a physical object, posted on the Studio A wall.


func get_prompt() -> String:
	return "THE CASTING SHEET · read (E)"


func interact(_player: Node3D) -> void:
	GameState.toast(
		"FINAL EPISODE · CAST: ALDER · BELL · PRICE · MERRICK · %d of 4 guest lines filled. The club dusts it."
		% GameState.strikes
	)
