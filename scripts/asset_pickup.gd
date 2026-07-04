class_name AssetPickup
extends Interactable
## A Sign-Off asset, where canon left it.

@export var asset_id := "CART"
@export var display := "an asset"
@export var flavor := ""
@export var needs_dock := false
@export var read_id := ""


func _process(_delta: float) -> void:
	visible = (not needs_dock or GameState.dock_done) and not GameState.assets.has(asset_id)


func get_prompt() -> String:
	return "%s · take (E)" % display.to_upper()


func interact(_player: Node3D) -> void:
	if flavor != "":
		GameState.toast(flavor)
	if read_id != "":
		GameState.mark_read(read_id)
	GameState.gain_asset(asset_id, display)
	queue_free()
