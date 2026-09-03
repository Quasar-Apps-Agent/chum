class_name AssetRack
extends Node3D
## Four labels above the bench: the Sign-Off assets, banked or waiting.

const ORDER := ["VERSE", "CART", "SCRIPT", "CARD"]

var _labels: Array = []
var _cans: Array = []


func _ready() -> void:
	## the rack made physical: a plank, four berths, a canister per banked asset
	var plank := MeshInstance3D.new()
	var pb := BoxMesh.new()
	pb.size = Vector3(2.2, 0.05, 0.3)
	pb.material = PropKit.wood("rackplank", Color(0.3, 0.24, 0.17))
	plank.mesh = pb
	plank.position = Vector3(0, -0.22, 0)
	add_child(plank)
	for i in ORDER.size():
		var l := Label3D.new()
		l.text = ORDER[i]
		l.font_size = 30
		l.position = Vector3(-0.9 + 0.6 * float(i), 0, 0)
		_labels.append(l)
		add_child(l)
		var can := MeshInstance3D.new()
		var cc := CylinderMesh.new()
		cc.top_radius = 0.11
		cc.bottom_radius = 0.11
		cc.height = 0.05
		cc.radial_segments = 14
		cc.material = PropKit.metal("canister", Color(0.5, 0.47, 0.4))
		can.mesh = cc
		can.rotation.x = PI / 2.0
		can.position = Vector3(-0.9 + 0.6 * float(i), -0.12, 0)
		can.visible = false
		_cans.append(can)
		add_child(can)


func _process(_delta: float) -> void:
	for i in ORDER.size():
		var have: bool = GameState.assets.has(ORDER[i])
		_labels[i].modulate = Color(0.89, 0.64, 0.24) if have else Color(0.3, 0.28, 0.24)
		_cans[i].visible = have
