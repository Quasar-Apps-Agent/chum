class_name TapeStage
extends SubViewport
## A tiny Gladhouse inside a viewport: the tape's world. During capture it
## plays Tape 1's timeline, ending on the approach, the hold, and the lunge.

signal lunge_happened

var _chum: Node3D
var _bars: Node3D
var _t := 0.0
var _dur := 0.0
var _playing := false
var _lunged := false
var _idle_t := 0.0
var _lunge_enabled := true
var _fire := false
var _light: OmniLight3D
var _leland: Node3D
var _pad: Label3D
var _film_quad: MeshInstance3D
var _film_mat: StandardMaterial3D
var _seq := FrameSequence.new()


func _ready() -> void:
	own_world_3d = true
	size = Vector2i(320, 240)
	render_target_update_mode = SubViewport.UPDATE_ALWAYS
	var cam := Camera3D.new()
	cam.position = Vector3(0, 0.8, 2.6)
	add_child(cam)
	cam.look_at_from_position(cam.position, Vector3(0, 0.7, 0), Vector3.UP)
	var light := OmniLight3D.new()
	light.position = Vector3(0, 1.7, 1.6)
	light.light_color = Color(1.0, 0.9, 0.7)
	light.light_energy = 2.4
	add_child(light)
	_light = light
	_mesh(Vector3(0, -0.05, 0), Vector3(4, 0.1, 4), Color(0.42, 0.36, 0.2))
	_mesh(Vector3(0, 0.9, -1.6), Vector3(4, 1.9, 0.15), Color(0.3, 0.38, 0.28))
	_mesh(Vector3(-1.1, 0.5, -1.5), Vector3(0.8, 1.0, 0.1), Color(0.2, 0.26, 0.19))
	_chum = _build_chum()
	add_child(_chum)
	_bars = _build_bars()
	_bars.visible = false
	add_child(_bars)
	_leland = _mesh(Vector3(1.35, 0.85, -0.5), Vector3(0.35, 1.7, 0.25), Color(0.12, 0.12, 0.13))
	_leland.visible = false
	_pad = Label3D.new()
	_pad.font_size = 30
	_pad.modulate = Color(0.9, 0.88, 0.8)
	_pad.position = Vector3(0.55, 1.15, 0.4)
	_pad.width = 380.0
	_pad.autowrap_mode = TextServer.AUTOWRAP_WORD
	add_child(_pad)
	_film_quad = MeshInstance3D.new()
	var fq := QuadMesh.new()
	fq.size = Vector2(3.1, 2.35)
	_film_mat = StandardMaterial3D.new()
	_film_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	fq.material = _film_mat
	_film_quad.mesh = fq
	_film_quad.position = Vector3(0, 0.75, 1.1)
	_film_quad.visible = false
	add_child(_film_quad)


func _mesh(pos: Vector3, size3: Vector3, color: Color) -> MeshInstance3D:
	var m := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size3
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	box.material = mat
	m.mesh = box
	m.position = pos
	add_child(m)
	return m


func _build_chum() -> Node3D:
	var root := Node3D.new()
	var wool := load("res://shaders/wool.gdshader") as Shader
	var body_mat := ShaderMaterial.new()
	body_mat.shader = wool
	var body := MeshInstance3D.new()
	var bs := SphereMesh.new()
	bs.radius = 0.3
	bs.height = 0.6
	bs.material = body_mat
	body.mesh = bs
	body.position = Vector3(0, 0.38, 0)
	root.add_child(body)
	var head := MeshInstance3D.new()
	var hs := SphereMesh.new()
	hs.radius = 0.22
	hs.height = 0.44
	hs.material = body_mat
	head.mesh = hs
	head.position = Vector3(0, 0.82, 0)
	root.add_child(head)
	for side in [-1.0, 1.0]:
		var ear := MeshInstance3D.new()
		var cone := CylinderMesh.new()
		cone.top_radius = 0.0
		cone.bottom_radius = 0.09
		cone.height = 0.22
		cone.material = body_mat
		ear.mesh = cone
		ear.position = Vector3(0.13 * side, 1.05, 0)
		root.add_child(ear)
	var amber := MeshInstance3D.new()
	var asph := SphereMesh.new()
	asph.radius = 0.035
	asph.height = 0.07
	var amat := StandardMaterial3D.new()
	amat.albedo_color = Color(0.79, 0.64, 0.24)
	asph.material = amat
	amber.mesh = asph
	amber.position = Vector3(-0.08, 0.86, 0.19)
	root.add_child(amber)
	var button := MeshInstance3D.new()
	var bsph := SphereMesh.new()
	bsph.radius = 0.033
	bsph.height = 0.066
	var bmat := StandardMaterial3D.new()
	bmat.albedo_color = Color(0.08, 0.08, 0.1)
	bsph.material = bmat
	button.mesh = bsph
	button.position = Vector3(0.08, 0.86, 0.19)
	root.add_child(button)
	return root


func _build_bars() -> Node3D:
	var root := Node3D.new()
	var colors := [Color(0.72, 0.72, 0.64), Color(0.69, 0.63, 0.14),
		Color(0.18, 0.56, 0.53), Color(0.24, 0.49, 0.2),
		Color(0.49, 0.24, 0.46), Color(0.63, 0.2, 0.16), Color(0.16, 0.2, 0.43)]
	for i in colors.size():
		var m := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = Vector3(0.5, 2.4, 0.05)
		var mat := StandardMaterial3D.new()
		mat.albedo_color = colors[i]
		mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		box.material = mat
		m.mesh = box
		m.position = Vector3(-1.5 + 0.5 * float(i), 0.8, 2.0)
		root.add_child(m)
	return root


func play_screening(duration: float) -> void:
	play_tape(duration)
	_lunge_enabled = false


func play_fire(duration: float) -> void:
	play_tape(duration)
	_lunge_enabled = false
	_fire = true


func set_seance_frame(idx: int, answer: String) -> void:
	_playing = false
	_fire = false
	_bars.visible = false
	_chum.visible = false
	_leland.visible = false
	_film_quad.visible = true
	_film_mat.albedo_texture = _seq.get_frame(idx, answer != "")
	_pad.text = answer
	_light.light_energy = 1.6


func seance_end() -> void:
	_leland.visible = false
	_film_quad.visible = false
	_pad.text = ""
	_chum.visible = true
	_light.light_energy = 2.4


func play_tape(duration: float) -> void:
	_dur = duration
	_t = 0.0
	_playing = true
	_lunged = false
	_lunge_enabled = true
	_fire = false
	_leland.visible = false
	_film_quad.visible = false
	_pad.text = ""
	_light.light_energy = 2.4
	_bars.visible = false
	_chum.visible = true
	_chum.position = Vector3.ZERO
	_chum.scale = Vector3.ONE


func stop_tape() -> void:
	_playing = false
	_bars.visible = false
	_chum.position = Vector3.ZERO
	_chum.scale = Vector3.ONE


func _process(delta: float) -> void:
	_idle_t += delta
	if not _playing:
		_chum.rotation.z = sin(_idle_t * 1.4) * 0.05
		return
	_t += delta
	var remain := _dur - _t
	if _fire:
		_chum.rotation.z = sin(_idle_t * 2.2) * 0.12
		_light.light_energy = lerpf(2.4, 0.7, _t / _dur)
		if remain <= 0.0:
			_playing = false
			_fire = false
			_chum.visible = false
			_bars.visible = true
			await get_tree().create_timer(1.6).timeout
			_bars.visible = false
			stop_tape()
		return
	if remain > 3.2:
		_chum.rotation.z = sin(_idle_t * 1.4) * 0.05
	elif remain > 0.9:
		_chum.rotation.z = 0.0
		var target_z := 1.9 if _lunge_enabled else 1.0
		_chum.position.z = move_toward(_chum.position.z, target_z, delta * 1.35)
	elif remain > 0.12:
		pass  ## the hold: stillness, one beat past bearable
	elif remain > 0.0:
		if _lunge_enabled and not _lunged:
			_lunged = true
			_chum.scale = Vector3(1.45, 1.45, 1.45)
			lunge_happened.emit()
	elif not _lunge_enabled:
		stop_tape()
	else:
		_playing = false
		_chum.visible = false
		_bars.visible = true
		await get_tree().create_timer(1.6).timeout
		_bars.visible = false
		_chum.visible = true
		stop_tape()
