class_name AssetRack
extends Node3D
## Four labels above the bench: the Sign-Off assets, banked or waiting.

const ORDER := ["VERSE", "CART", "SCRIPT", "CARD"]

var _labels: Array = []


func _ready() -> void:
	for i in ORDER.size():
		var l := Label3D.new()
		l.text = ORDER[i]
		l.font_size = 30
		l.position = Vector3(-0.9 + 0.6 * float(i), 0, 0)
		_labels.append(l)
		add_child(l)


func _process(_delta: float) -> void:
	for i in ORDER.size():
		var have: bool = GameState.assets.has(ORDER[i])
		_labels[i].modulate = Color(0.89, 0.64, 0.24) if have else Color(0.3, 0.28, 0.24)
