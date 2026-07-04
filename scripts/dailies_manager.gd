class_name DailiesManager
extends Node3D
## Spawns canisters in the library stacks: existing ones on load, new per capture.

const SLOTS := [
	Vector3(-3.5, 0.35, -14.0), Vector3(2.5, 0.35, -18.5),
	Vector3(4.0, 0.35, -13.0), Vector3(-4.5, 0.35, -19.0),
]


func _ready() -> void:
	for d in GameState.dailies:
		_spawn(int(d.get("id", -1)), int(d.get("take", 0)))
	GameState.daily_added.connect(_spawn)


func _spawn(id: int, take: int) -> void:
	var c := DailiesCanister.new()
	c.daily_id = id
	c.take = take
	var base: Vector3 = SLOTS[id % SLOTS.size()]
	c.position = base + Vector3(0.4 * float(id / SLOTS.size()), 0, 0)
	var col := CollisionShape3D.new()
	var shape := CylinderShape3D.new()
	shape.radius = 0.3
	shape.height = 0.16
	col.shape = shape
	c.add_child(col)
	var mesh := MeshInstance3D.new()
	var cyl := CylinderMesh.new()
	cyl.top_radius = 0.3
	cyl.bottom_radius = 0.3
	cyl.height = 0.16
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.55, 0.53, 0.5)
	cyl.material = mat
	mesh.mesh = cyl
	c.add_child(mesh)
	var tag := Label3D.new()
	tag.text = "TAKE %d" % take
	tag.font_size = 28
	tag.position = Vector3(0, 0.4, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.76, 0.23, 0.18)
	c.add_child(tag)
	add_child(c)
