class_name Dresser
extends Interactable
## Rita's dresser and the seven items. One leaves per capture; the loupe goes last.

var _item_nodes: Array = []


func _ready() -> void:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.5, 0.42, 0.3)
	for i in GameState.ITEM_ORDER.size():
		var item := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = Vector3(0.16, 0.1, 0.16)
		box.material = mat
		item.mesh = box
		item.position = Vector3(-0.66 + 0.22 * i, 0.62, 0)
		add_child(item)
		var tag := Label3D.new()
		tag.text = GameState.ITEM_ORDER[i]
		tag.font_size = 18
		tag.modulate = Color(0.8, 0.77, 0.68)
		tag.position = Vector3(0, 0.16, 0)
		tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		item.add_child(tag)
		_item_nodes.append(item)
	GameState.sheet_changed.connect(func(_c: int) -> void: _refresh())
	_refresh()


func _refresh() -> void:
	for i in _item_nodes.size():
		_item_nodes[i].visible = i >= GameState.items_lost


func get_prompt() -> String:
	return "RITA'S DRESSER · take stock (E)"


func interact(_player: Node3D) -> void:
	var remaining := GameState.ITEM_ORDER.size() - GameState.items_lost
	if GameState.items_lost == 0:
		GameState.toast("Seven things, squared to the dresser's edge. Everything where you left it.")
	else:
		var gone: Array = GameState.ITEM_ORDER.slice(0, GameState.items_lost)
		GameState.toast("%d of seven remain. Gone: %s. They will be in the footage." % [remaining, ", ".join(gone)])
