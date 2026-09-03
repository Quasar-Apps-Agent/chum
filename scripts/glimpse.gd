class_name Glimpse
extends Node3D
## T4.8: once, ever, under two seconds, unmediated. The fire corridor unseals
## on Day 4, and the elbow keeps its appointment.

var fire_door: CompoundDoor
var rect := [-9.75, -16.0, 7.5, 3.0]

var _firing := false


func _process(_delta: float) -> void:
	if fire_door and GameState.day >= 4 and fire_door.locked_reason != "":
		fire_door.locked_reason = ""
		if not GameState.fire_unsealed:
			GameState.fire_unsealed = true
			GameState.save_log()
			GameState.toast("The club unseals the fire corridor for the anniversary. Nobody goes first.")
	if GameState.glimpse_seen or _firing or not GameState.is_night or GameState.premiere_live:
		return
	var p := get_tree().get_first_node_in_group("player")
	if p == null:
		return
	var pos: Vector3 = p.global_position
	if absf(pos.x - rect[0]) < rect[2] / 2.0 and absf(pos.z - rect[1]) < rect[3] / 2.0:
		_firing = true
		_fire()


func _fire() -> void:
	GameState.toast("At the corridor's elbow, unmediated:")
	var it := Node3D.new()
	it.position = Vector3(-12.6, 0, -16.0)
	var body := MeshInstance3D.new()
	var bs := CapsuleMesh.new()
	bs.radius = 0.22
	bs.height = 2.5
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.03, 0.028, 0.026)
	bs.material = mat
	body.mesh = bs
	body.position = Vector3(0, 1.25, 0)
	it.add_child(body)
	var bar := MeshInstance3D.new()
	var bb := BoxMesh.new()
	bb.size = Vector3(1.8, 0.12, 0.12)
	bb.material = mat
	bar.mesh = bb
	bar.position = Vector3(0, 2.9, 0)
	it.add_child(bar)
	## strings, or tendons — part of what refuses to resolve
	for sx in [-0.8, -0.3, 0.3, 0.8]:
		var s := MeshInstance3D.new()
		var sb := BoxMesh.new()
		sb.size = Vector3(0.012, 1.4, 0.012)
		sb.material = mat
		s.mesh = sb
		s.position = Vector3(sx as float, 2.2, 0)
		s.rotation.z = -(sx as float) * 0.22
		it.add_child(s)
	add_child(it)
	await get_tree().create_timer(1.8).timeout
	it.queue_free()
	GameState.glimpse_seen = true
	GameState.save_log()
	GameState.toast("A puppeteer whose puppet is missing, or a puppet whose puppeteer is missing. The animation refused to resolve which.")
	await get_tree().create_timer(2.8).timeout
	GameState.toast("The plastic sheeting breathes once, with the draft of something that has already passed.")
