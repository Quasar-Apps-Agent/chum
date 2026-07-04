class_name MonitorRig
extends Node3D
## Frame Discipline seed: a camera somewhere else, rendered live onto a wall set.
## Commit 002 proves the render-target pipeline the whole mediation system rides on.

var cam_position := Vector3.ZERO
var cam_look := Vector3.ZERO
var monitor_position := Vector3.ZERO
var monitor_yaw := 0.0
var label_text := "CAM"

var _screen_mat: StandardMaterial3D
var _vp: SubViewport
var _no_signal: Label3D
var _powered := true
var killed := false


func _ready() -> void:
	add_to_group("rig")
	var vp := SubViewport.new()
	_vp = vp
	vp.size = Vector2i(360, 270)
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(vp)
	var cam := Camera3D.new()
	vp.add_child(cam)
	cam.global_position = cam_position
	cam.look_at_from_position(cam_position, cam_look, Vector3.UP)
	cam.fov = 65.0

	var screen := MeshInstance3D.new()
	var quad := QuadMesh.new()
	quad.size = Vector2(1.6, 1.2)
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = vp.get_texture()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	quad.material = mat
	_screen_mat = mat
	screen.mesh = quad
	screen.position = monitor_position
	screen.rotation.y = monitor_yaw
	add_child(screen)

	var frame := MeshInstance3D.new()
	var frame_box := BoxMesh.new()
	frame_box.size = Vector3(1.8, 1.4, 0.12)
	var frame_mat := StandardMaterial3D.new()
	frame_mat.albedo_color = Color(0.09, 0.08, 0.06)
	frame_box.material = frame_mat
	frame.mesh = frame_box
	frame.position = monitor_position + Vector3(sin(monitor_yaw), 0, cos(monitor_yaw)) * -0.08
	frame.rotation.y = monitor_yaw
	add_child(frame)

	_no_signal = Label3D.new()
	_no_signal.text = "NO SIGNAL"
	_no_signal.font_size = 40
	_no_signal.modulate = Color(0.35, 0.33, 0.3)
	_no_signal.position = monitor_position
	_no_signal.rotation.y = monitor_yaw
	_no_signal.visible = false
	add_child(_no_signal)

	var tag := Label3D.new()
	tag.text = label_text
	tag.font_size = 36
	tag.modulate = Color(0.89, 0.64, 0.24)
	tag.position = monitor_position + Vector3(0, 0.85, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(tag)


func get_feed_texture() -> Texture2D:
	return _vp.get_texture()


func sync_to(tex: Texture2D) -> void:
	if _screen_mat == null:
		return
	_screen_mat.albedo_texture = tex
	_screen_mat.albedo_color = Color(1, 1, 1)
	if _no_signal:
		_no_signal.visible = false


func set_powered(on: bool) -> void:
	_powered = on
	_apply()


func set_killed(on: bool) -> void:
	killed = on
	_apply()


func _apply() -> void:
	if _screen_mat == null:
		return
	var live := _powered and not killed
	if live:
		_screen_mat.albedo_texture = _vp.get_texture()
		_screen_mat.albedo_color = Color(1, 1, 1)
	else:
		_screen_mat.albedo_texture = null
		_screen_mat.albedo_color = Color(0.02, 0.02, 0.02)
	if _no_signal:
		_no_signal.visible = not live
		_no_signal.text = "KILLED · RE-PATCH AT PB" if killed else "NO SIGNAL"
