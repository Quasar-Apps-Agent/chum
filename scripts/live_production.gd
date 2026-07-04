class_name LiveProduction
extends Node3D
## Phase 2, playable: cues, sabotage sprints, the Vess breaker, the divert
## window in its canon slot, and the little door closed by hand, on camera.

const MARK := Vector3(-15.5, 1.0, -26.5)

const INCIDENTS := {
	"TALLY": "The tally lights swap. Camera one claims it is not program.",
	"HOUSE": "Half the house lights drop. The club murmurs an apology.",
	"BOOM": "The boom drifts into frame. Somebody's grandson is so sorry.",
	"CARDS": "The cue cards shuffle themselves. Vess swears he stacked them.",
}
const FIX_LINES := {
	"TALLY": "TALLY BUS RESET · the lights agree with reality again.",
	"HOUSE": "HOUSE DIMMER RESTORED · the room comes back, embarrassed.",
	"BOOM": "BOOM WINCHED · the frame is clean.",
	"CARDS": "CARDS RESTACKED · in Vess's order, which was right.",
}

var restored := false
var _pgm := 1
var _incident := ""
var _incident_started := 0.0
var _tally_refusals := 0
var _boom_held := false
var _fail_takes := 0
var _pressure_on := false

var _player: Node3D
var _spawned: Array = []
var _breaker: FinaleBreaker


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("cam_1"):
		_pgm = 1
	elif event.is_action_pressed("cam_2"):
		_pgm = 2
	elif event.is_action_pressed("cam_3"):
		_pgm = 3


func run() -> String:
	GameState.premiere_live = true
	GameState.is_night = true
	GameState.night_changed.emit(true)
	_player = get_tree().get_first_node_in_group("player")
	if _player:
		_player.global_position = Vector3(-15.5, 1.0, -28.5)
	_spawn_stage()
	GameState.toast("PLACES.")
	await _wait(2.4)
	GameState.toast("THE FLOOR MANAGER · 'In five, four...' The hands do the rest.")
	await _wait(2.6)

	## CUE 1 · COLD OPEN
	await _on_mark_press("CUE 1 · COLD OPEN · cut to camera one (1) · stand the mark · SPACE", 1)
	GameState.toast("RITA · 'Welcome back to the Gladhouse, friends. It's a special night.'")
	await _wait(2.8)
	GameState.toast("RITA · 'It's our last night.'  CHUM, warm as ever: 'Ohhh, don't be sad!'")
	await _wait(3.0)
	GameState.toast("CHUM · 'Every good day ends with a goodnight. That's how you know it was good.'")
	await _wait(2.8)
	_pressure_on = true
	_pressure()

	## CUE 2 · THE SONG, sabotaged
	GameState.toast("The cart deck loses power. The club is helping.")
	var take := 1
	restored = false
	_breaker.label = "CART DECK BREAKER · restore (E)"
	while not await _timed(45.0, "CUE 2 · RESTORE THE CART DECK AT THE PATCH BAY"):
		take += 1
		_fail_takes += 1
		restored = false
		GameState.toast("TAKE %d · from the top of the cue." % take)
	await _on_mark_press("CUE 2 · THE SONG · camera one (1) · back to the mark · SPACE", 1)
	GameState.toast("EVERYONE · 'Close the door and dim the light. Fold the day away.'")
	await _wait(3.0)
	GameState.toast("'Everyone we love is home. And no one has to stay.'")
	await _wait(3.0)

	## THE FINAL BREAKER · VESS
	if GameState.vess_credited:
		GameState.toast("VESS, at the final breaker, not looking at you.")
		await _wait(2.4)
		GameState.toast("VESS · 'The margin. You wrote my name. Somebody's name should be on something. Go finish it.'")
		await _wait(3.0)
	else:
		GameState.toast("The final breaker. VESS. The handle. The dark.")
		await _wait(2.6)
		restored = false
		_breaker.label = "MAIN BUS · earn the retake (E)"
		while not await _timed(30.0, "BLACKOUT · EARN THE RETAKE AT THE PATCH BAY"):
			_fail_takes += 1
			GameState.toast("Again. The dark is patient.")
			restored = false

	## THE FINAL BREAK · the divert window, in its canon slot
	if GameState.has_key("QUIET ROOM") and GameState.leland_answers.size() >= 5 and GameState.fire_tape_watched:
		GameState.set_capture_status("FINAL BREAK · SPACE places for cue three · Q divert to the dead room")
		var pick := await _choice("respond", "improvise")
		GameState.set_capture_status("")
		if pick == "improvise":
			_cleanup()
			return "dead_air"

	## CUE 3 · CLOSE THE HOUSE
	var door := _little_door()
	if door:
		door.locked_reason = ""
		GameState.set_capture_status("CUE 3 · CLOSE THE HOUSE · the little door, by hand")
		while not door.is_open():
			await get_tree().process_frame
		GameState.toast("Now close it. On camera.")
		while door.is_open():
			await get_tree().process_frame
		GameState.toast("The house is closed. The studio holds its breath on purpose.")
		await _wait(2.6)
	GameState.set_capture_status("")
	_cleanup()
	return "line"


func _little_door() -> CompoundDoor:
	for n in get_tree().get_nodes_in_group("little_door"):
		return n
	return null


func _spawn_stage() -> void:
	var wool := load("res://shaders/wool.gdshader") as Shader
	var wmat := ShaderMaterial.new()
	wmat.shader = wool
	var chum := Node3D.new()
	chum.position = Vector3(-15.5, 0, -31.2)
	var body := MeshInstance3D.new()
	var bs := SphereMesh.new()
	bs.radius = 0.28
	bs.height = 0.56
	bs.material = wmat
	body.mesh = bs
	body.position = Vector3(0, 0.5, 0)
	chum.add_child(body)
	var head := MeshInstance3D.new()
	var hs := SphereMesh.new()
	hs.radius = 0.2
	hs.height = 0.4
	hs.material = wmat
	head.mesh = hs
	head.position = Vector3(0, 0.9, 0)
	chum.add_child(head)
	var tag := Label3D.new()
	tag.text = "CHUM · ON HIS MARK"
	tag.font_size = 30
	tag.position = Vector3(0, 1.4, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.85, 0.93, 0.77)
	chum.add_child(tag)
	add_child(chum)
	_spawned.append(chum)
	_breaker = FinaleBreaker.new()
	_breaker.live = self
	_breaker.position = Vector3(-5.5, 0.9, -28.2)
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.5, 0.9, 0.4)
	col.shape = shape
	_breaker.add_child(col)
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(0.45, 0.85, 0.35)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.76, 0.23, 0.18)
	box.material = mat
	mesh.mesh = box
	_breaker.add_child(mesh)
	add_child(_breaker)
	_spawned.append(_breaker)
	_spawn_fixture("TALLY_HOUSE", "AUX PANEL · resets (E)", Vector3(-5.0, 0.9, -29.4), Color(0.3, 0.34, 0.4))
	_spawn_fixture("BOOM", "BOOM WINCH · crank (E)", Vector3(-13.4, 0.9, -30.4), Color(0.4, 0.34, 0.24))
	_spawn_fixture("CARDS", "CARD STAND · restack (E)", Vector3(-16.9, 0.9, -27.4), Color(0.87, 0.83, 0.72))


func _spawn_fixture(fid: String, label: String, pos: Vector3, color: Color) -> void:
	var f := FinaleFixture.new()
	f.live = self
	f.fix_id = fid
	f.label = label
	f.position = pos
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.5, 0.7, 0.4)
	col.shape = shape
	f.add_child(col)
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(0.45, 0.65, 0.35)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	box.material = mat
	mesh.mesh = box
	f.add_child(mesh)
	add_child(f)
	_spawned.append(f)


func _on_mark_press(label: String, need_cam: int = 1) -> void:
	while true:
		await get_tree().process_frame
		if _player == null:
			continue
		var near := _player.global_position.distance_to(MARK) < 1.6
		var suffix := " · PGM CAM %d" % _pgm
		if _incident != "":
			suffix += " · INCIDENT: " + _incident
		if near:
			suffix += " · ON MARK"
		GameState.set_capture_status(label + suffix)
		if near and _pgm == need_cam and Input.is_action_just_pressed("respond"):
			if _incident == "TALLY" and _tally_refusals < 2:
				_tally_refusals += 1
				GameState.toast("The tally is lying. Camera one IS program. Trust the mark, not the light.")
				continue
			if _incident == "TALLY":
				GameState.toast("You call it blind. Correctly.")
			if _incident == "BOOM" and not _boom_held:
				_boom_held = true
				GameState.toast("Hold. The boom is in frame. Winch it, or wait it out.")
				continue
			GameState.set_capture_status("")
			return
		if near and _pgm != need_cam and Input.is_action_just_pressed("respond"):
			GameState.toast("Wrong camera is program. The Floor Manager's hand does not move.")


func _timed(dur: float, label: String) -> bool:
	var t := dur * (1.5 if GameState.assist_on else 1.0)
	while t > 0.0:
		await get_tree().process_frame
		t -= get_process_delta_time()
		GameState.set_capture_status("%s · 0:%02d" % [label, int(ceil(t))])
		if restored:
			GameState.set_capture_status("")
			return true
	GameState.set_capture_status("")
	return false


func _choice(a: String, b: String) -> String:
	while true:
		await get_tree().process_frame
		if Input.is_action_just_pressed(a):
			return a
		if Input.is_action_just_pressed(b):
			return b
	return a


func fix(fid: String) -> void:
	var matched := (_incident == fid) or (fid == "TALLY_HOUSE" and _incident in ["TALLY", "HOUSE"])
	if not matched:
		GameState.toast("Nothing wrong here right now. The club appreciates the diligence.")
		return
	_resolve(_incident, "fixed by hand")


func _resolve(inc: String, how: String) -> void:
	if inc == "HOUSE":
		GameState.set_blackout(0.0)
	_plog("RESOLVED %s (%s) t=%.1f" % [inc, how, Time.get_ticks_msec() / 1000.0 - _incident_started])
	GameState.toast(FIX_LINES.get(inc, "Fixed."))
	_incident = ""
	_tally_refusals = 0
	_boom_held = false


func _pressure() -> void:
	while _pressure_on:
		var interval := maxf(14.0, 26.0 - 4.0 * float(_fail_takes))
		await _wait(interval)
		if not _pressure_on:
			return
		if _incident != "":
			## fail-forward: the club fixes what you left, apologizing
			if Time.get_ticks_msec() / 1000.0 - _incident_started > 40.0:
				_resolve(_incident, "club auto-fix")
			continue
		var keys := INCIDENTS.keys()
		_incident = keys[randi() % keys.size()]
		_incident_started = Time.get_ticks_msec() / 1000.0
		_plog("INCIDENT %s (fail_takes %d, interval %.0f)" % [_incident, _fail_takes, interval])
		GameState.toast("THE CLUB IS HELPING · " + INCIDENTS[_incident])
		if _incident == "HOUSE":
			GameState.set_blackout(0.35)


func _plog(text: String) -> void:
	var f := FileAccess.open("user://premiere_log.txt", FileAccess.READ_WRITE)
	if f == null:
		f = FileAccess.open("user://premiere_log.txt", FileAccess.WRITE)
	if f == null:
		return
	f.seek_end()
	f.store_line(text)
	f.close()


func _cleanup() -> void:
	_pressure_on = false
	if _incident == "HOUSE":
		GameState.set_blackout(0.0)
	_incident = ""
	for n in _spawned:
		if is_instance_valid(n):
			n.queue_free()
	_spawned.clear()


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout
