class_name Harriet
extends Interactable
## Harriet Lund. She sways gently while the building is ON AIR, and freezes
## mid-motion for every break, resuming exactly where the cue left her.
## Her cup has been rising since Tape 1.

const LINES := ["'And now.'", "'But first.'", "'When we come back.'"]

var _t := 0.0
var _li := 0
var _cup: MeshInstance3D


func _ready() -> void:
	var wool := load("res://shaders/wool.gdshader") as Shader
	var wmat := ShaderMaterial.new()
	wmat.shader = wool
	var body := MeshInstance3D.new()
	var bs := CapsuleMesh.new()
	bs.radius = 0.24
	bs.height = 1.15
	bs.material = wmat
	body.mesh = bs
	body.position = Vector3(0, 0.72, 0)
	add_child(body)
	var head := MeshInstance3D.new()
	var hs := SphereMesh.new()
	hs.radius = 0.15
	hs.height = 0.3
	hs.material = wmat
	head.mesh = hs
	head.position = Vector3(0, 1.42, 0)
	add_child(head)
	var col := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.3
	shape.height = 1.6
	col.shape = shape
	col.position = Vector3(0, 0.8, 0)
	add_child(col)
	_cup = MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.height = 0.09
	cm.top_radius = 0.055
	cm.bottom_radius = 0.045
	var cmat := StandardMaterial3D.new()
	cmat.albedo_color = Color(0.87, 0.83, 0.72)
	cm.material = cmat
	_cup.mesh = cm
	add_child(_cup)
	var tag := Label3D.new()
	tag.text = "HARRIET"
	tag.font_size = 34
	tag.position = Vector3(0, 1.8, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.85, 0.93, 0.77)
	add_child(tag)


func _physics_process(delta: float) -> void:
	_cup.position = Vector3(0.3, 0.92 + 0.05 * minf(float(GameState.day), 6.0), 0.2)
	if not Broadcast.on_air:
		return  ## the freeze: mid-motion, until the return cue
	_t += delta
	rotation.z = sin(_t * 0.9) * 0.04


func get_prompt() -> String:
	if not Broadcast.on_air:
		return "HARRIET · mid-motion"
	return "HARRIET · in her chair (E)"


func interact(_player: Node3D) -> void:
	if not Broadcast.on_air:
		Achievements.unlock("A06")
		GameState.toast("She does not resume until the return cue. Her cup has been rising since Tape 1.")
		return
	GameState.toast("HARRIET · %s" % LINES[_li])
	_li = (_li + 1) % LINES.size()
