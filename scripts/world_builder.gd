extends Node3D
## Commit 002: the full compound from the room inventory bible, as data.
## 20 zones (catwalks deferred: vertical greybox arrives with Studio A's grid pass).
## Fixes from 001: KITCHEN, DORMS, and BENCH wall planes now share their
## neighbors' planes, so those doorways cut both walls instead of one.

const WALL_H := 3.0
const WALL_T := 0.24

## name: [center_x, center_z, size_x, size_z]
const ROOMS := {
	"REC ROOM": [0.0, 0.0, 10.0, 8.0],
	"KITCHEN": [8.0, 0.0, 6.0, 5.0],
	"DORMS": [-9.0, 0.0, 8.0, 5.0],
	"ENTRY": [0.0, 7.0, 6.0, 6.0],
	"YARD": [0.0, 14.0, 30.0, 8.0],
	"SHED": [10.0, 14.0, 3.0, 3.0],
	"CORRIDOR": [0.0, -7.5, 3.0, 7.0],
	"TAPE LIBRARY": [0.0, -16.0, 12.0, 10.0],
	"BENCH ROOM": [9.0, -16.0, 6.0, 6.0],
	"CLIMATE": [14.25, -16.0, 4.5, 6.0],
	"TRANSMITTER HALL": [16.75, -6.5, 8.5, 13.0],
	"DEAD ROOM": [19.0, 2.5, 4.0, 5.0],
	"FIRE CORRIDOR": [-9.75, -16.0, 7.5, 3.0],
	"STAGE HALL": [-12.0, -20.75, 3.0, 6.5],
	"STUDIO A": [-15.5, -30.0, 12.0, 12.0],
	"PATCH BAY": [-5.5, -29.5, 8.0, 7.0],
	"CONTROL": [0.0, -24.5, 3.0, 7.0],
	"MASTER CONTROL": [5.5, -29.5, 8.0, 7.0],
	"GREEN ROOM": [-24.5, -27.0, 6.0, 6.0],
	"SCENE DOCK": [-15.5, -39.5, 10.0, 7.0],
}

## [room_a, room_b, gap_x, gap_z, gap_width, axis, door_type]
## door_type: "" open gap · "door" hinged · "locked:<reason>" hinged and held
const DOORS := [
	["REC ROOM", "KITCHEN", 5.0, 0.0, 1.4, "z", ""],
	["REC ROOM", "DORMS", -5.0, 0.0, 1.4, "z", ""],
	["REC ROOM", "ENTRY", 0.0, 4.0, 1.6, "x", "door"],
	["ENTRY", "YARD", 0.0, 10.0, 1.6, "x", "door"],
	["YARD", "SHED", 8.5, 14.0, 1.2, "z", "locked:PADLOCKED · the tag reads EDITH · a key exists|EDITH"],
	["REC ROOM", "CORRIDOR", 0.0, -4.0, 1.6, "x", ""],
	["CORRIDOR", "TAPE LIBRARY", 0.0, -11.0, 1.6, "x", ""],
	["TAPE LIBRARY", "BENCH ROOM", 6.0, -16.0, 1.4, "z", ""],
	["BENCH ROOM", "CLIMATE", 12.0, -16.0, 1.4, "z", ""],
	["CLIMATE", "TRANSMITTER HALL", 14.5, -13.0, 1.4, "x", ""],
	["TRANSMITTER HALL", "DEAD ROOM", 19.0, 0.0, 1.2, "x", "locked:LOCKED · felt-faced · the hum stops at the seam|QUIET ROOM"],
	["TAPE LIBRARY", "FIRE CORRIDOR", -6.0, -16.0, 1.4, "z", "locked:SEALED · reopens for the anniversary (Tape 4)"],
	["FIRE CORRIDOR", "STAGE HALL", -12.0, -17.5, 1.4, "x", ""],
	["STAGE HALL", "STUDIO A", -12.0, -24.0, 1.6, "x", "window"],
	["STUDIO A", "PATCH BAY", -9.5, -29.5, 1.4, "z", ""],
	["CONTROL", "PATCH BAY", -1.5, -27.0, 1.4, "z", ""],
	["CONTROL", "MASTER CONTROL", 1.5, -27.0, 1.4, "z", ""],
	["TAPE LIBRARY", "CONTROL", 0.0, -21.0, 1.6, "x", ""],
	["STUDIO A", "GREEN ROOM", -21.5, -27.0, 1.4, "z", ""],
	["STUDIO A", "SCENE DOCK", -15.5, -36.0, 1.6, "x", "window"],
]

## [id, display name, position]
const DEMO_OPEN := ["REC ROOM", "KITCHEN", "DORMS", "ENTRY", "CORRIDOR", "TAPE LIBRARY", "BENCH ROOM"]

const STATIONS := [
	["S5", "REC ROOM", Vector3(-4.2, 0.0, 3.2)],
	["S1", "LIBRARY LANDING", Vector3(-1.2, 0.0, -11.8)],
	["S2", "MASTER CONTROL", Vector3(7.0, 0.0, -31.0)],
	["S3", "GREEN ROOM", Vector3(-24.5, 0.0, -28.6)],
	["S4", "TRANSMITTER THRESHOLD", Vector3(14.5, 0.0, -11.4)],
]

## [camera_pos, camera_look_at, monitor_pos, monitor_yaw_rad, label]
const MONITORS := [
	[Vector3(0, 2.4, -10.6), Vector3(0, 1.2, -4.5), Vector3(2.4, 1.7, -3.82), PI, "CAM 1 · CORRIDOR"],
	[Vector3(0, 2.4, -20.4), Vector3(0, 1.2, -12.0), Vector3(7.2, 1.7, -13.18), 0.0, "CAM 2 · STACKS"],
]

var _floor_mat := StandardMaterial3D.new()
var _wall_mat := StandardMaterial3D.new()
var _station_mat := StandardMaterial3D.new()
var _door_mat := StandardMaterial3D.new()


func _ready() -> void:
	## Art pass: flat greybox colors give way to procedural PBR surfaces with
	## real relief. Same palette, textured. (See scripts/prop_kit.gd.)
	_floor_mat = PropKit.concrete()
	_wall_mat = PropKit.plaster()
	_station_mat = PropKit.metal("station", Color(0.79, 0.64, 0.24))
	_door_mat = PropKit.wood("door", Color(0.32, 0.24, 0.15))
	for room_name in ROOMS.keys():
		_build_room(room_name, ROOMS[room_name])
	for d in DOORS:
		if d[6] != "":
			_spawn_door(d)
	for s in STATIONS:
		_spawn_station(s[0], s[1], s[2])
	for m in MONITORS:
		_spawn_monitor(m)
	_spawn_bench()
	_spawn_wool_spike()
	_spawn_library_stacks()
	_spawn_transmitter_hall()
	_spawn_yard_dressing()
	_spawn_yard_ground()
	_spawn_dead_room_felt()
	_spawn_kitchen()
	_spawn_green_room()
	_spawn_scene_dock_dressing()
	_spawn_dorms_extra()
	_spawn_shed_interior()
	_build_studio_dressing()
	_build_catwalks()
	_spawn_wall_clocks()
	_spawn_casting_sheet()
	_spawn_rundown()
	_spawn_bed_and_dresser()
	_spawn_patchbay_circuits()
	_spawn_screening()
	_spawn_keys()
	_spawn_burn_loop()
	_spawn_film_and_note()
	_spawn_room_tones()
	_spawn_dock_task()
	_spawn_assets_and_decision()
	var lp := LiveProduction.new()
	lp.add_to_group("live_production")
	add_child(lp)
	_spawn_club()
	_spawn_details()
	_spawn_readables()
	_spawn_event_wave()
	add_child(RecChairs.new())
	add_child(NoiseTracker.new())
	var casc := Cascade.new()
	casc.rigs = _rigs
	add_child(casc)
	_cascade = casc
	var live_chk := LivenessCheck.new()
	add_child(live_chk)
	_liveness = live_chk
	_late_wire()
	var ld := Lockdown.new()
	ld.rigs = _rigs
	ld.exterior_doors = _ext_doors
	add_child(ld)
	GameState.night_changed.connect(_on_night_lighting)


func _build_room(room_name: String, r: Array) -> void:
	var cx: float = r[0]
	var cz: float = r[1]
	var sx: float = r[2]
	var sz: float = r[3]
	_box(Vector3(cx, -0.1, cz), Vector3(sx, 0.2, sz), _floor_mat)
	_wall_run(Vector3(cx, 0, cz - sz / 2.0), sx, "x")
	_wall_run(Vector3(cx, 0, cz + sz / 2.0), sx, "x")
	_wall_run(Vector3(cx - sx / 2.0, 0, cz), sz, "z")
	_wall_run(Vector3(cx + sx / 2.0, 0, cz), sz, "z")
	PropKit.baseboard(cx, cz, sx, sz, self)
	## The floating room names retired with the art pass; the map (M) names
	## rooms now. (room_name still keys ROOMS for systems that need it.)
	## One dim practical per room: Merle keeps the lights on. Barely.
	if room_name != "YARD":
		var prac := OmniLight3D.new()
		prac.position = Vector3(cx, 2.75, cz)
		prac.light_color = Color(0.95, 0.72, 0.45)
		prac.light_energy = 0.5
		prac.omni_range = maxf(sx, sz) * 0.75
		prac.shadow_enabled = false
		prac.add_to_group("practical")
		add_child(prac)


func _wall_run(center: Vector3, length: float, axis: String) -> void:
	var segments := [[-length / 2.0, length / 2.0]]
	for d in DOORS:
		var gx: float = d[2]
		var gz: float = d[3]
		var gw: float = d[4]
		var d_axis: String = d[5]
		if d_axis != axis:
			continue
		var on_wall := false
		var g_local := 0.0
		if axis == "x" and absf(gz - center.z) < 0.3 and absf(gx - center.x) <= length / 2.0 + 0.01:
			on_wall = true
			g_local = gx - center.x
		elif axis == "z" and absf(gx - center.x) < 0.3 and absf(gz - center.z) <= length / 2.0 + 0.01:
			on_wall = true
			g_local = gz - center.z
		if on_wall:
			segments = _cut(segments, g_local - gw / 2.0, g_local + gw / 2.0)
	for seg in segments:
		var a: float = seg[0]
		var b: float = seg[1]
		if b - a < 0.05:
			continue
		var mid := (a + b) / 2.0
		var seg_len := b - a
		var pos: Vector3
		var size: Vector3
		if axis == "x":
			pos = center + Vector3(mid, WALL_H / 2.0, 0)
			size = Vector3(seg_len, WALL_H, WALL_T)
		else:
			pos = center + Vector3(0, WALL_H / 2.0, mid)
			size = Vector3(WALL_T, WALL_H, seg_len)
		_box(pos, size, _wall_mat)


func _cut(segments: Array, lo: float, hi: float) -> Array:
	var out := []
	for seg in segments:
		var a: float = seg[0]
		var b: float = seg[1]
		if hi <= a or lo >= b:
			out.append(seg)
		else:
			if lo > a:
				out.append([a, lo])
			if hi < b:
				out.append([hi, b])
	return out


func _box(pos: Vector3, size: Vector3, mat: Material) -> void:
	var body := StaticBody3D.new()
	body.position = pos
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	col.shape = shape
	body.add_child(col)
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	box.material = mat
	mesh.mesh = box
	body.add_child(mesh)
	add_child(body)


func _spawn_door(d: Array) -> void:
	var gx: float = d[2]
	var gz: float = d[3]
	var gw: float = d[4]
	var axis: String = d[5]
	var kind: String = d[6]
	var door := CompoundDoor.new()
	door.door_label = "%s / %s" % [d[0], d[1]]
	if kind.begins_with("locked:"):
		var payload := kind.substr(7)
		var parts := payload.split("|")
		door.locked_reason = parts[0]
		if parts.size() > 1:
			door.required_key = parts[1]
	elif kind == "window":
		door.window_bound = true
	if d[0] == "ENTRY" or d[1] == "ENTRY":
		_ext_doors.append(door)
	if d[0] == "FIRE CORRIDOR" or d[1] == "FIRE CORRIDOR":
		_fire_door = door
	if GameState.DEMO and (not DEMO_OPEN.has(d[0]) or not DEMO_OPEN.has(d[1])):
		if "TRANSMITTER" in str(d[0]) or "TRANSMITTER" in str(d[1]):
			door.locked_reason = "SEALED · you can hear it from here. That is enough for today."
		else:
			door.locked_reason = "SEALED · the club opens the rest when the contract is signed."
	## hinge at one end of the gap
	if axis == "x":
		door.position = Vector3(gx - gw / 2.0, 0, gz)
	else:
		door.position = Vector3(gx, 0, gz - gw / 2.0)
		door.rotation.y = PI / 2.0
	var leaf_col := CollisionShape3D.new()
	var leaf_shape := BoxShape3D.new()
	leaf_shape.size = Vector3(gw, 2.2, 0.09)
	leaf_col.shape = leaf_shape
	leaf_col.position = Vector3(gw / 2.0, 1.1, 0)
	door.add_child(leaf_col)
	PropKit.door_leaf(gw, 2.2, _door_mat, door)
	add_child(door)


func _spawn_station(id: String, station_name: String, pos: Vector3) -> void:
	var st := LogStation.new()
	st.station_id = id
	st.station_name = station_name
	st.position = pos + Vector3(0, 0.55, 0)
	GameState.map_points.append([id, Vector2(pos.x, pos.z)])
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.5, 1.1, 0.4)
	col.shape = shape
	st.add_child(col)
	## the transmitter log, physical: a lectern, its binder, its chained pen
	st.add_child(PropKit.lectern())
	GameState.register_station(id, st.position)
	var label := Label3D.new()
	label.text = id + " LOG"
	label.font_size = 26
	label.position = Vector3(0, 0.85, 0)
	label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	label.modulate = Color(0.89, 0.64, 0.24)
	st.add_child(label)
	add_child(st)


var _rigs: Array = []
var _ext_doors: Array = []
var _fire_door: CompoundDoor
var _rec_tv: BenchTV
var _cascade: Cascade
var _liveness: LivenessCheck
var _console_ref: PatchbayConsole


func _spawn_monitor(m: Array) -> void:
	var rig := MonitorRig.new()
	_rigs.append(rig)
	rig.cam_position = m[0]
	rig.cam_look = m[1]
	rig.monitor_position = m[2]
	rig.monitor_yaw = m[3]
	rig.label_text = m[4]
	add_child(rig)


func _spawn_bench() -> void:
	var bench := CaptureBench.new()
	bench.position = Vector3(9.0, 0.5, -17.6)
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(1.8, 1.0, 0.8)
	col.shape = shape
	bench.add_child(col)
	## the workbench: top slab on legs, the reel deck standing on it
	var top_mat := PropKit.wood("benchtop", Color(0.24, 0.20, 0.15))
	var leg_mat := PropKit.metal("benchleg", Color(0.2, 0.2, 0.22))
	var bmesh := MeshInstance3D.new()
	var bbox := BoxMesh.new()
	bbox.size = Vector3(1.8, 0.08, 0.8)
	bbox.material = top_mat
	bmesh.mesh = bbox
	bmesh.position = Vector3(0, 0.46, 0)
	bench.add_child(bmesh)
	for lx in [-0.8, 0.8]:
		for lz in [-0.3, 0.3]:
			var leg := MeshInstance3D.new()
			var lb := BoxMesh.new()
			lb.size = Vector3(0.08, 0.92, 0.08)
			lb.material = leg_mat
			leg.mesh = lb
			leg.position = Vector3(lx, -0.04, lz)
			bench.add_child(leg)
	var deck: Dictionary = PropKit.reel_deck()
	var deck_rig := deck["rig"] as Node3D
	deck_rig.position = Vector3(-0.45, 0.78, -0.2)
	bench.add_child(deck_rig)
	bench.deck_reels = deck["reels"]
	var label := Label3D.new()
	label.text = "THE BENCH"
	label.font_size = 26
	label.position = Vector3(0, 1.1, 0)
	label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	label.modulate = Color(0.85, 0.93, 0.77)
	bench.add_child(label)
	add_child(bench)
	var tv := BenchTV.new()
	tv.position = Vector3(9.0, 1.55, -18.82)
	add_child(tv)
	bench.tv = tv
	var knob := GenKnob.new()
	knob.tv = tv
	knob.position = Vector3(10.2, 1.0, -18.5)
	var kc := CollisionShape3D.new()
	var kcs := BoxShape3D.new()
	kcs.size = Vector3(0.3, 0.3, 0.3)
	kc.shape = kcs
	knob.add_child(kc)
	var km := MeshInstance3D.new()
	var kmb := CylinderMesh.new()
	kmb.height = 0.12
	kmb.top_radius = 0.1
	kmb.bottom_radius = 0.1
	var kmat := StandardMaterial3D.new()
	kmat.albedo_color = Color(0.79, 0.64, 0.24)
	kmb.material = kmat
	km.mesh = kmb
	knob.add_child(km)
	add_child(knob)
	if GameState.DEMO:
		return
	var fdock := FireTapeDock.new()
	fdock.tv = tv
	fdock.position = Vector3(7.8, 0.9, -18.4)
	_dock_body(fdock, "1977 DOCK", Color(0.4, 0.2, 0.15))
	add_child(fdock)
	var sdock := SeanceDock.new()
	sdock.tv = tv
	sdock.position = Vector3(7.8, 0.9, -17.2)
	_dock_body(sdock, "SEANCE REEL", Color(0.18, 0.3, 0.22))
	add_child(sdock)
	if not GameState.has_fire_tape:
		var ft := FireTapePickup.new()
		ft.position = Vector3(17.0, 0.45, -10.0)
		_dock_body(ft, "REEL · 1977", Color(0.3, 0.28, 0.26))
		add_child(ft)


func _spawn_wool_spike() -> void:
	var wool := load("res://shaders/wool.gdshader") as Shader
	var root := Node3D.new()
	root.position = Vector3(10.8, 0, -14.3)
	var plinth := MeshInstance3D.new()
	var pbox := BoxMesh.new()
	pbox.size = Vector3(0.7, 0.5, 0.7)
	var pmat := StandardMaterial3D.new()
	pmat.albedo_color = Color(0.14, 0.13, 0.11)
	pbox.material = pmat
	plinth.mesh = pbox
	plinth.position = Vector3(0, 0.25, 0)
	root.add_child(plinth)
	var body_mat := ShaderMaterial.new()
	body_mat.shader = wool
	var body := MeshInstance3D.new()
	var sphere := SphereMesh.new()
	sphere.radius = 0.28
	sphere.height = 0.56
	sphere.material = body_mat
	body.mesh = sphere
	body.position = Vector3(0, 0.8, 0)
	root.add_child(body)
	var head := MeshInstance3D.new()
	var hs := SphereMesh.new()
	hs.radius = 0.2
	hs.height = 0.4
	hs.material = body_mat
	head.mesh = hs
	head.position = Vector3(0, 1.18, 0)
	root.add_child(head)
	var tag := Label3D.new()
	tag.text = "WOOL SPIKE 001"
	tag.font_size = 24
	tag.position = Vector3(0, 1.65, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.89, 0.64, 0.24)
	root.add_child(tag)
	add_child(root)


func _build_studio_dressing() -> void:
	## The rebuilt Gladhouse set, greyboxed: carpet, cubby wall, painted house,
	## the little door (held until Tape 5), Chum's mark, three camera pedestals.
	_box(Vector3(-15.5, 0.02, -31.5), Vector3(6.0, 0.06, 5.0), PropKit.carpet())
	## the cubby wall, cell by cell, some cells still holding their toys
	var cubbies := PropKit.cubby_wall(3.2, 2.0, 4, 3, 301)
	cubbies.position = Vector3(-19.0, 0, -33.7)
	add_child(cubbies)
	_collider(Vector3(-19.0, 1.0, -33.7), Vector3(3.2, 2.0, 0.5))
	var house_mat := StandardMaterial3D.new()
	house_mat.albedo_color = Color(0.45, 0.3, 0.2)
	_box(Vector3(-12.2, 1.2, -33.6), Vector3(2.6, 2.4, 0.4), house_mat)
	var little := CompoundDoor.new()
	little.door_label = "THE LITTLE DOOR"
	little.locked_reason = "Not yet. It closes on camera, in Tape 5."
	little.add_to_group("little_door")
	little.position = Vector3(-12.6, 0, -33.35)
	var lc := CollisionShape3D.new()
	var lcs := BoxShape3D.new()
	lcs.size = Vector3(0.8, 1.2, 0.08)
	lc.shape = lcs
	lc.position = Vector3(0.4, 0.6, 0)
	little.add_child(lc)
	PropKit.door_leaf(0.8, 1.2, _door_mat, little)
	add_child(little)
	var mark_mat := StandardMaterial3D.new()
	mark_mat.albedo_color = Color(0.8, 0.75, 0.6)
	_box(Vector3(-15.5, 0.06, -31.2), Vector3(0.4, 0.02, 0.4), mark_mat)
	var mark_label := Label3D.new()
	mark_label.text = "CHUM'S MARK"
	mark_label.font_size = 28
	mark_label.modulate = Color(0.6, 0.56, 0.48)
	mark_label.position = Vector3(-15.5, 0.6, -31.2)
	mark_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(mark_label)
	## three cameras on their marks, every lens on Chum's mark
	var cam_spots := [Vector3(-15.5, 0, -26.5), Vector3(-19.5, 0, -27.5), Vector3(-11.5, 0, -27.5)]
	var chums_mark := Vector3(-15.5, 0, -31.2)
	for i in cam_spots.size():
		var ped := PropKit.camera_pedestal()
		ped.position = cam_spots[i]
		var aim: Vector3 = chums_mark - cam_spots[i]
		ped.rotation.y = atan2(aim.x, aim.z)
		add_child(ped)
		_collider(cam_spots[i] + Vector3(0, 0.75, 0), Vector3(0.6, 1.5, 0.6))
		var tag := Label3D.new()
		tag.text = "CAM %d" % (i + 1)
		tag.font_size = 24
		tag.position = cam_spots[i] + Vector3(0, 1.8, 0)
		tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		tag.modulate = Color(0.89, 0.64, 0.24)
		add_child(tag)


func _build_catwalks() -> void:
	## The grid above Studio A: two crossing walkways with rails, reached by
	## a ramp from Stage Hall. Vertical greybox; ladders come with art.
	var walk_mat := StandardMaterial3D.new()
	walk_mat.albedo_color = Color(0.2, 0.21, 0.22)
	var rail_mat := StandardMaterial3D.new()
	rail_mat.albedo_color = Color(0.3, 0.3, 0.32)
	var y := WALL_H + 0.15
	_box(Vector3(-15.5, y, -30.0), Vector3(12.0, 0.1, 1.2), walk_mat)
	_box(Vector3(-15.5, y, -30.0), Vector3(1.2, 0.1, 12.0), walk_mat)
	for off in [-0.66, 0.66]:
		_box(Vector3(-15.5, y + 0.5, -30.0 + off), Vector3(12.0, 0.9, 0.06), rail_mat)
		_box(Vector3(-15.5 + off, y + 0.5, -30.0), Vector3(0.06, 0.9, 12.0), rail_mat)
	## ramp: stage hall corner up to the north walkway end
	var ramp := StaticBody3D.new()
	ramp.position = Vector3(-12.0, y / 2.0, -22.0)
	ramp.rotation.x = -0.68
	var rc := CollisionShape3D.new()
	var rcs := BoxShape3D.new()
	rcs.size = Vector3(1.4, 0.12, 5.2)
	rc.shape = rcs
	ramp.add_child(rc)
	var rm := MeshInstance3D.new()
	var rmb := BoxMesh.new()
	rmb.size = Vector3(1.4, 0.12, 5.2)
	rmb.material = walk_mat
	rm.mesh = rmb
	ramp.add_child(rm)
	add_child(ramp)
	_box(Vector3(-12.0, y, -25.2), Vector3(1.4, 0.1, 2.4), walk_mat)
	_box(Vector3(-13.4, y, -27.6), Vector3(4.0, 0.1, 1.2), walk_mat)


func _spawn_wall_clocks() -> void:
	var spots := [Vector3(0, 2.3, -24.5), Vector3(-15.5, 2.5, -24.6), Vector3(5.5, 2.3, -26.6), Vector3(0, 2.3, 0)]
	for p in spots:
		var c := WallClock.new()
		c.position = p
		add_child(c)


func _spawn_casting_sheet() -> void:
	var sheet := CastingSheetProp.new()
	sheet.position = Vector3(-20.9, 1.5, -30.0)
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.1, 1.2, 0.9)
	col.shape = shape
	sheet.add_child(col)
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(0.06, 1.2, 0.9)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.87, 0.83, 0.72)
	box.material = mat
	mesh.mesh = box
	sheet.add_child(mesh)
	var tag := Label3D.new()
	tag.text = "CASTING SHEET"
	tag.font_size = 24
	tag.position = Vector3(0, 0.85, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.76, 0.23, 0.18)
	sheet.add_child(tag)
	add_child(sheet)


func _spawn_rundown() -> void:
	if GameState.DEMO:
		return
	var cd := CoverageDirector.new()
	cd.rigs = _rigs
	add_child(cd)
	var r := Rundown.new()
	r.add_to_group("rundown")
	r.rooms = ROOMS
	for d in DOORS:
		r.doors.append(Vector3(d[2], 0.0, d[3]))
	r.rigs = _rigs
	r.director = cd
	add_child(r)


func _spawn_bed_and_dresser() -> void:
	var bed := BedProp.new()
	bed.position = Vector3(-9.0, 0.3, 1.5)
	var bc := CollisionShape3D.new()
	var bcs := BoxShape3D.new()
	bcs.size = Vector3(2.0, 0.6, 1.1)
	bc.shape = bcs
	bed.add_child(bc)
	## frame, mattress, blanket tucked hard, one pillow: made every morning
	var frame_mat := PropKit.wood("bedframe", Color(0.3, 0.22, 0.14))
	var bm := MeshInstance3D.new()
	var bmb := BoxMesh.new()
	bmb.size = Vector3(2.0, 0.24, 1.1)
	bmb.material = frame_mat
	bm.mesh = bmb
	bm.position = Vector3(0, -0.14, 0)
	bed.add_child(bm)
	var matt := MeshInstance3D.new()
	var mb := BoxMesh.new()
	mb.size = Vector3(1.94, 0.2, 1.04)
	mb.material = PropKit.fabric("mattress", Color(0.62, 0.58, 0.5))
	matt.mesh = mb
	matt.position = Vector3(0, 0.08, 0)
	bed.add_child(matt)
	var blanket := MeshInstance3D.new()
	var blb := BoxMesh.new()
	blb.size = Vector3(1.4, 0.06, 1.06)
	blb.material = PropKit.fabric("blanket", Color(0.42, 0.34, 0.26))
	blanket.mesh = blb
	blanket.position = Vector3(0.28, 0.2, 0)
	bed.add_child(blanket)
	var pillow := MeshInstance3D.new()
	var plb := BoxMesh.new()
	plb.size = Vector3(0.4, 0.1, 0.6)
	plb.material = PropKit.fabric("pillow", Color(0.8, 0.77, 0.7))
	pillow.mesh = plb
	pillow.position = Vector3(-0.72, 0.22, 0)
	bed.add_child(pillow)
	var headboard := MeshInstance3D.new()
	var hbb := BoxMesh.new()
	hbb.size = Vector3(0.06, 0.7, 1.1)
	hbb.material = frame_mat
	headboard.mesh = hbb
	headboard.position = Vector3(-1.0, 0.2, 0)
	bed.add_child(headboard)
	var btag := Label3D.new()
	btag.text = "RITA'S BED"
	btag.font_size = 24
	btag.position = Vector3(0, 0.9, 0)
	btag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	btag.modulate = Color(0.85, 0.93, 0.77)
	bed.add_child(btag)
	add_child(bed)

	var dresser := Dresser.new()
	dresser.position = Vector3(-11.5, 0.28, -1.8)
	var dc := CollisionShape3D.new()
	var dcs := BoxShape3D.new()
	dcs.size = Vector3(1.7, 0.56, 0.5)
	dc.shape = dcs
	dresser.add_child(dc)
	var dm := MeshInstance3D.new()
	var dmb := BoxMesh.new()
	dmb.size = Vector3(1.7, 0.56, 0.5)
	var dmat := StandardMaterial3D.new()
	dmat.albedo_color = Color(0.42, 0.33, 0.22)
	dmb.material = dmat
	dm.mesh = dmb
	dresser.add_child(dm)
	add_child(dresser)


func _spawn_patchbay_circuits() -> void:
	var ctl_light := OmniLight3D.new()
	ctl_light.position = Vector3(0, 2.6, -24.5)
	ctl_light.light_color = Color(0.98, 0.68, 0.32)
	ctl_light.light_energy = 1.9
	ctl_light.omni_range = 8.0
	add_child(ctl_light)
	var hall_light := OmniLight3D.new()
	hall_light.position = Vector3(-12.0, 2.6, -20.7)
	hall_light.light_color = Color(0.98, 0.68, 0.32)
	hall_light.light_energy = 1.9
	hall_light.omni_range = 8.0
	add_child(hall_light)

	var console := PatchbayConsole.new()
	console.position = Vector3(-5.5, 0.55, -31.8)
	_wire_cascade_console(console)
	var cc := CollisionShape3D.new()
	var ccs := BoxShape3D.new()
	ccs.size = Vector3(1.6, 1.1, 0.6)
	cc.shape = ccs
	console.add_child(cc)
	## the patchbay proper: cabinet, angled fascia, knobs, faders
	var desk := PropKit.console(Vector3(1.6, 0.85, 0.6), 2, 6)
	desk.position = Vector3(0, -0.55, 0)
	console.add_child(desk)
	var ctag := Label3D.new()
	ctag.text = "PATCHBAY"
	ctag.font_size = 26
	ctag.position = Vector3(0, 1.1, 0)
	ctag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	ctag.modulate = Color(0.89, 0.64, 0.24)
	console.add_child(ctag)
	console.control_lights = [ctl_light]
	console.hall_lights = [hall_light]
	if _rigs.size() > 0:
		console.control_rig = _rigs[0]
	add_child(console)
	console.apply_initial()


func _on_night_lighting(now_night: bool) -> void:
	var sun := get_node_or_null("../Sun") as DirectionalLight3D
	if sun:
		sun.light_energy = 0.005 if now_night else 0.07
	var we := get_node_or_null("../WorldEnvironment") as WorldEnvironment
	if we and we.environment:
		we.environment.ambient_light_energy = 0.03 if now_night else 0.09
	## nights, the practicals brown out: pools shrink, corners win
	for pr in get_tree().get_nodes_in_group("practical"):
		(pr as OmniLight3D).light_energy = 0.28 if now_night else 0.5


func _spawn_screening() -> void:
	var sign := CueSign.new()
	sign.sign_text = "RESPOND"
	sign.position = Vector3(-0.9, 2.5, 3.55)
	add_child(sign)
	var hold := CueSign.new()
	hold.sign_text = "HOLD"
	hold.position = Vector3(0.9, 2.5, 3.55)
	add_child(hold)
	## the screen on the rec room's west wall: a live tape stage
	var rec_tv := BenchTV.new()
	rec_tv.slate_text = "THE GLADHOUSE · CLUB PRINT"
	rec_tv.position = Vector3(-4.78, 1.6, 1.0)
	rec_tv.rotation.y = PI / 2.0
	add_child(rec_tv)
	_rec_tv = rec_tv
	var projector := ScreeningEvent.new()
	projector.respond_sign = sign
	projector.tv = rec_tv
	projector.position = Vector3(-1.4, 0.55, 1.0)
	var pc := CollisionShape3D.new()
	var pcs := BoxShape3D.new()
	pcs.size = Vector3(0.6, 0.5, 0.9)
	pc.shape = pcs
	projector.add_child(pc)
	## the club print's projector: body, lens toward the screen, two reels up top
	var pm := MeshInstance3D.new()
	var pmb := BoxMesh.new()
	pmb.size = Vector3(0.5, 0.4, 0.7)
	pmb.material = PropKit.metal("projector", Color(0.2, 0.2, 0.22))
	pm.mesh = pmb
	projector.add_child(pm)
	var lens := MeshInstance3D.new()
	var lc := CylinderMesh.new()
	lc.top_radius = 0.06
	lc.bottom_radius = 0.08
	lc.height = 0.22
	lc.material = PropKit.dark_plastic()
	lens.mesh = lc
	lens.rotation.z = PI / 2.0
	lens.position = Vector3(-0.33, 0.08, 0)
	projector.add_child(lens)
	for rz in [-0.18, 0.18]:
		var reel := MeshInstance3D.new()
		var rc := CylinderMesh.new()
		rc.top_radius = 0.16
		rc.bottom_radius = 0.16
		rc.height = 0.03
		rc.radial_segments = 16
		rc.material = PropKit.metal("filmreel", Color(0.45, 0.44, 0.4))
		reel.mesh = rc
		reel.rotation.z = PI / 2.0
		reel.position = Vector3(0.05, 0.36, rz)
		projector.add_child(reel)
	var ptag := Label3D.new()
	ptag.text = "PROJECTOR"
	ptag.font_size = 24
	ptag.position = Vector3(0, 0.7, 0)
	ptag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	ptag.modulate = Color(0.85, 0.93, 0.77)
	projector.add_child(ptag)
	add_child(projector)


func _spawn_keys() -> void:
	if not GameState.has_key("EDITH"):
		_spawn_key("EDITH", "the EDITH key, felt-tagged in a child's hand", Vector3(10.6, 1.2, -2.3), "KEY BOARD")
	if not GameState.has_key("TRAINING"):
		_spawn_key("TRAINING", "the TRAINING key, tagged in green ink", Vector3(10.2, 1.2, -2.3), "KEY BOARD")
	if not GameState.has_key("QUIET ROOM"):
		_spawn_key("QUIET ROOM", "the quiet room key · felt-wrapped", Vector3(10.0, 0.5, 14.0), "FOR THE QUIET ROOM")


func _spawn_key(id: String, display: String, pos: Vector3, label_text: String) -> void:
	var k := KeyItem.new()
	k.key_id = id
	k.display = display
	k.position = pos
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.4, 0.4, 0.4)
	col.shape = shape
	k.add_child(col)
	## a key that reads as a key, tag and all
	var key_body := PropKit.key_prop(Color(0.79, 0.64, 0.24))
	key_body.rotation.y = randf() * TAU
	k.add_child(key_body)
	var tag := Label3D.new()
	tag.text = label_text
	tag.font_size = 30
	tag.position = Vector3(0, 0.5, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.89, 0.64, 0.24)
	k.add_child(tag)
	add_child(k)


func _spawn_burn_loop() -> void:
	add_child(DailiesManager.new())
	var d := Degausser.new()
	d.position = Vector3(14.25, 0.55, -17.6)
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(1.2, 1.1, 0.8)
	col.shape = shape
	d.add_child(col)
	## the erasure machine: housing, exposed coil ring, hazard stripe
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(1.2, 0.9, 0.8)
	box.material = PropKit.metal("degausser", Color(0.22, 0.24, 0.28))
	mesh.mesh = box
	mesh.position = Vector3(0, -0.1, 0)
	d.add_child(mesh)
	var coil_mesh := MeshInstance3D.new()
	var ring := TorusMesh.new()
	ring.inner_radius = 0.18
	ring.outer_radius = 0.3
	ring.material = PropKit.metal("coil", Color(0.5, 0.32, 0.18))
	coil_mesh.mesh = ring
	coil_mesh.position = Vector3(0, 0.42, 0)
	d.add_child(coil_mesh)
	var stripe := MeshInstance3D.new()
	var sb := BoxMesh.new()
	sb.size = Vector3(1.22, 0.1, 0.82)
	sb.material = PropKit.OCHRE_MAT()
	stripe.mesh = sb
	stripe.position = Vector3(0, 0.15, 0)
	d.add_child(stripe)
	var tag := Label3D.new()
	tag.text = "DEGAUSSER"
	tag.font_size = 24
	tag.position = Vector3(0, 1.05, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.89, 0.64, 0.24)
	d.add_child(tag)
	var coil := ToneEmitter.new()
	coil.freq_a = 120.0
	coil.freq_b = 240.0
	coil.noise = 0.05
	coil.volume_db = -16.0
	coil.reach = 10.0
	d.add_child(coil)
	add_child(d)


func _spawn_film_and_note() -> void:
	var cab := FilmCabinet.new()
	cab.position = Vector3(-5.4, 0.7, -19.0)
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.7, 1.4, 0.7)
	col.shape = shape
	cab.add_child(col)
	## flat file: body plus four drawer faces, one not quite closed
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(0.7, 1.4, 0.7)
	box.material = PropKit.metal("cabinet", Color(0.33, 0.3, 0.24))
	mesh.mesh = box
	cab.add_child(mesh)
	var face_mat := PropKit.metal("drawer", Color(0.38, 0.34, 0.27))
	for i in 4:
		var face := MeshInstance3D.new()
		var fb := BoxMesh.new()
		fb.size = Vector3(0.62, 0.28, 0.03)
		fb.material = face_mat
		face.mesh = fb
		## the second drawer sits proud: it will not fully close
		face.position = Vector3(0, 0.5 - 0.33 * float(i), 0.36 + (0.03 if i == 1 else 0.0))
		cab.add_child(face)
		var pull := MeshInstance3D.new()
		var pb := BoxMesh.new()
		pb.size = Vector3(0.14, 0.03, 0.03)
		pb.material = PropKit.dark_plastic()
		pull.mesh = pb
		pull.position = face.position + Vector3(0, 0, 0.03)
		cab.add_child(pull)
	var tag := Label3D.new()
	tag.text = "FILM CABINET"
	tag.font_size = 24
	tag.position = Vector3(0, 1.1, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.85, 0.93, 0.77)
	cab.add_child(tag)
	add_child(cab)

	if not GameState.signals_known.has("HOLD YOUR APPLAUSE"):
		var note := HarrietNote.new()
		note.position = Vector3(2.8, 0.55, 2.2)
		var ncol := CollisionShape3D.new()
		var nshape := BoxShape3D.new()
		nshape.size = Vector3(0.4, 0.2, 0.4)
		ncol.shape = nshape
		note.add_child(ncol)
		var nmesh := MeshInstance3D.new()
		var nbox := BoxMesh.new()
		nbox.size = Vector3(0.3, 0.04, 0.22)
		var nmat := StandardMaterial3D.new()
		nmat.albedo_color = Color(0.87, 0.83, 0.72)
		nbox.material = nmat
		nmesh.mesh = nbox
		note.add_child(nmesh)
		add_child(note)


func _spawn_room_tones() -> void:
	## The transmitter hall's hum floor: the loudest room in the building.
	var hum := ToneEmitter.new()
	hum.freq_a = 55.0
	hum.freq_b = 110.0
	hum.volume_db = -8.0
	hum.reach = 26.0
	hum.position = Vector3(16.75, 1.6, -6.5)
	add_child(hum)


func _dock_body(node: Node3D, text: String, color: Color) -> void:
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.5, 0.5, 0.5)
	col.shape = shape
	node.add_child(col)
	## every dock reads as equipment now: plinth, cased body, rim, brass plaque
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(0.45, 0.4, 0.45)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = 0.8
	box.material = mat
	mesh.mesh = box
	node.add_child(mesh)
	var plinth := MeshInstance3D.new()
	var pb := BoxMesh.new()
	pb.size = Vector3(0.55, 0.07, 0.55)
	pb.material = PropKit.dark_plastic()
	plinth.mesh = pb
	plinth.position = Vector3(0, -0.235, 0)
	node.add_child(plinth)
	var rim := MeshInstance3D.new()
	var rb := BoxMesh.new()
	rb.size = Vector3(0.49, 0.03, 0.49)
	rb.material = PropKit.wood("dockrim", Color(0.3, 0.24, 0.17))
	rim.mesh = rb
	rim.position = Vector3(0, 0.21, 0)
	node.add_child(rim)
	var plaque := MeshInstance3D.new()
	var qb := BoxMesh.new()
	qb.size = Vector3(0.18, 0.07, 0.012)
	qb.material = PropKit.metal("plaque", Color(0.65, 0.55, 0.35))
	plaque.mesh = qb
	plaque.position = Vector3(0, -0.05, 0.23)
	node.add_child(plaque)
	var tag := Label3D.new()
	tag.text = text
	tag.font_size = 28
	tag.position = Vector3(0, 0.55, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.89, 0.64, 0.24)
	node.add_child(tag)


func _spawn_dock_task() -> void:
	if GameState.DEMO:
		return
	var task := DockTask.new()
	task.position = Vector3(-19.5, 0.7, -38.0)
	_dock_body(task, "CLIPBOARD", Color(0.87, 0.83, 0.72))
	add_child(task)
	for i in 6:
		var c := DockChum.new()
		c.idx = i + 1
		var col_i := i % 3
		var row_i := i / 3
		c.position = Vector3(-18.0 + 2.0 * float(col_i), 0, -40.0 - 1.7 * float(row_i))
		var col := CollisionShape3D.new()
		var shape := BoxShape3D.new()
		shape.size = Vector3(0.6, 1.4, 0.6)
		col.shape = shape
		col.position = Vector3(0, 0.7, 0)
		c.add_child(col)
		## generations of him, fur going gray in order: the first two units
		## are the 1971 pilot, the rest the 1974 rebuild
		c.add_child(CharacterKit.chum_pilot() if i < 2 else CharacterKit.chum_mini())
		var tag := Label3D.new()
		tag.text = "UNIT %d" % (i + 1)
		tag.font_size = 26
		tag.position = Vector3(0, 1.25, 0)
		tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		tag.modulate = Color(0.6, 0.56, 0.48)
		c.add_child(tag)
		add_child(c)
		task.chums.append(c)
	task.setup()


func _spawn_assets_and_decision() -> void:
	if GameState.DEMO:
		return
	var spectro := SpectroDock.new()
	spectro.position = Vector3(10.6, 0.9, -17.2)
	_dock_body(spectro, "SPECTROGRAM", Color(0.2, 0.26, 0.3))
	add_child(spectro)
	var rack := AssetRack.new()
	rack.position = Vector3(9.0, 2.35, -18.82)
	add_child(rack)
	var ledger := DecisionLedger.new()
	ledger.position = Vector3(8.2, 0.9, -16.2)
	_dock_body(ledger, "ACCESSION LEDGER", Color(0.87, 0.83, 0.72))
	add_child(ledger)

	var cart := AssetPickup.new()
	cart.asset_id = "CART"
	cart.display = "the station ID cart"
	cart.flavor = "CART AUDIO · 'You're watching The Gladhouse, on WGLD, Channel fifty-eight.'"
	cart.position = Vector3(4.0, 0.9, -31.5)
	_dock_body(cart, "CART RACK", Color(0.3, 0.3, 0.34))
	add_child(cart)

	var script_p := AssetPickup.new()
	script_p.read_id = "D02"
	script_p.asset_id = "SCRIPT"
	script_p.display = "the finale script"
	script_p.flavor = "Typed, hand-amended. The margin, pressed hard: 'No. Tell them the truth or it doesn't take.'"
	script_p.position = Vector3(16.2, 0.5, -10.0)
	_dock_body(script_p, "CRAIK'S BOX", Color(0.4, 0.34, 0.24))
	add_child(script_p)

	var card := AssetPickup.new()
	card.asset_id = "CARD"
	card.display = "the sign-off card"
	card.needs_dock = true
	card.flavor = "Hand-lettered. WGLD CHANNEL 58. GOODNIGHT."
	card.position = Vector3(-13.0, 0.5, -41.5)
	_dock_body(card, "PROPS CRATE", Color(0.42, 0.36, 0.28))
	add_child(card)


func _spawn_club() -> void:
	var vb := VessBinder.new()
	vb.position = Vector3(-6.5, 0.6, 1.8)
	_dock_body(vb, "VESS'S ROOM", Color(0.43, 0.5, 0.67))
	add_child(vb)
	var ce := CreditEntry.new()
	ce.position = Vector3(7.4, 0.9, -15.2)
	_dock_body(ce, "LEDGER MARGIN", Color(0.87, 0.83, 0.72))
	add_child(ce)
	var m := Merle.new()
	m.position = Vector3(8.0, 0.0, -1.0)
	var col := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.3
	shape.height = 1.6
	col.shape = shape
	col.position = Vector3(0, 0.8, 0)
	m.add_child(col)
	## Merle Cottry, plate-accurate: the full build lives in character_kit.gd
	m.add_child(CharacterKit.merle())
	var tag := Label3D.new()
	tag.text = "MERLE"
	tag.font_size = 26
	tag.position = Vector3(0, 1.8, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.85, 0.93, 0.77)
	m.add_child(tag)
	add_child(m)


func _spawn_details() -> void:
	var h := Harriet.new()
	h.position = Vector3(1.2, 0.0, 2.6)
	add_child(h)
	## Vess, at the shrine wall, cataloguing what he was never thanked for
	var v := VessProp.new()
	v.position = Vector3(-3.7, 0.0, -1.2)
	v.rotation.y = -PI / 2.0
	add_child(v)
	var pegs := CoatPegs.new()
	pegs.position = Vector3(2.7, 1.5, 7.0)
	add_child(pegs)
	if GameState.ng_relic != "":
		## one item from the prior run, on the set, in shot, unremarked
		var relic := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = Vector3(0.14, 0.08, 0.14)
		var mat := StandardMaterial3D.new()
		mat.albedo_color = Color(0.5, 0.42, 0.3)
		box.material = mat
		relic.mesh = box
		relic.position = Vector3(-14.6, 0.1, -31.0)
		add_child(relic)
		var tag := Label3D.new()
		tag.text = GameState.ng_relic.to_lower()
		tag.font_size = 20
		tag.position = Vector3(-14.6, 0.42, -31.0)
		tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		tag.modulate = Color(0.45, 0.42, 0.36, 0.7)
		add_child(tag)


func _spawn_event_wave() -> void:
	if GameState.DEMO:
		return
	var nt := NightTrip.new()
	nt.rigs = _rigs
	add_child(nt)
	var crate := ImpossibleCrate.new()
	crate.position = Vector3(0.0, 0.5, 6.0)
	_dock_body(crate, "DELIVERY", Color(0.45, 0.38, 0.28))
	add_child(crate)
	var fm := FloorManager.new()
	fm.position = Vector3(-4.5, 0.0, -19.4)
	add_child(fm)
	var re := RejectedEdit.new()
	re.tv = _rec_tv
	re.position = Vector3(-2.6, 0.9, 1.0)
	_dock_body(re, "VESS'S CUT", Color(0.43, 0.5, 0.67))
	add_child(re)
	var gl := Glimpse.new()
	gl.fire_door = _fire_door
	add_child(gl)


func _wire_cascade_console(console: PatchbayConsole) -> void:
	_console_ref = console
	if _cascade:
		_cascade.console = console
	if _liveness:
		_liveness.console = console


func _late_wire() -> void:
	## covers either creation order between console and cascade
	if _console_ref:
		_cascade.console = _console_ref
		_liveness.console = _console_ref


func _spawn_readables() -> void:
	var defs := [
		["D04", "THE CLIPPING · 1974, behind glass", Vector3(-4.2, 1.15, -1.5), 1, false, Color(0.87, 0.83, 0.72), [
			["COURIER, OCTOBER 1974 · LOCAL GIRL, 7, FOUND SAFE AFTER NIGHT IN CORNFIELD.", 3.0],
			["'We don't know which volunteer walked her back and we'd like to shake his hand,' said Sheriff D. Pruett.", 3.2],
			["The child, wrapped in a square of gray flannel her mother did not recognize, said only that she was 'carried the long way, singing.'", 3.4],
		]],
		["D05", "WELCOME PACKET · mimeograph purple", Vector3(-11.9, 0.9, -1.0), 1, false, Color(0.7, 0.6, 0.78), [
			["WELCOME TO THE FIFTY-EIGHT! Quiet hours are posted by the clocks and we do mean them. [ballpoint: we really do]", 3.2],
			["If a door is closed, it is closed for a reason and the reason is written on it. Make yourself at home. You already are.", 3.2],
			["[ballpoint, smaller] welcome home", 2.2],
		]],
		["D09", "FIRE MARSHAL REPORT · 1977, photocopy", Vector3(0.0, 0.8, -24.5), 2, false, Color(0.6, 0.6, 0.62), [
			["Cause: undetermined, consistent with deliberate ignition at the tape vault. Total loss of stored media.", 3.2],
			["Note of record: transmitting equipment found energized at time of entry and could not be de-energized by responding personnel.", 3.4],
			["Referred to station engineer. No further action.", 2.4],
		]],
		["D10", "A FAN LETTER · ruled paper, careful loops", Vector3(-12.2, 0.5, -40.6), 1, true, Color(0.87, 0.83, 0.72), [
			["Dear Chum, my brother says you are just a puppet but I know a secret which is that everybody is a puppet of somebody", 3.4],
			["and it only matters if the hands are kind. Your hands seem kind.", 3.0],
			["Please wave at camera one on my birthday which is the 9th. Your friend, Iris Bell, age 8 and one quarter.", 3.4],
		]],
	]
	defs.append(["D11", "PEAK ASSET DOSSIER · CHUM-AF-1974-P", Vector3(2.0, 0.9, -27.5), 4, false, Color(0.6, 0.55, 0.5), [
		["PEAK PRODUCTION ASSET DOSSIER. FILE CHUM-AF-1974-P (REV.). STATUS: ACTIVE / HAZARDOUS.", 3.2],
		["Rebuilt from the 1974 mascot body and salvaged studio materials. Entirely manually operated. Requires minimum three puppeteers for full performance.", 3.6],
		["Handwritten beneath: he works his own jaw. Count the hands. Report all sightings to Peak Security. HE REMEMBERS THE AUDIENCE.", 3.6],
	]])
	for d in defs:
		var rp := ReadableProp.new()
		rp.doc_id = d[0]
		rp.label = d[1]
		rp.position = d[2]
		rp.needs_day = d[3]
		rp.needs_dock = d[4]
		rp.lines = d[6]
		_dock_body(rp, d[1].split(" · ")[0], d[5])
		add_child(rp)


func _collider(pos: Vector3, size: Vector3) -> void:
	## invisible static collision for dressed props (meshes come from PropKit)
	var body := StaticBody3D.new()
	body.position = pos
	var col := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	col.shape = shape
	body.add_child(col)
	add_child(body)


func _spawn_library_stacks() -> void:
	## The stacks the room was named for: four used archives, aisles honest,
	## every lane to a door kept clear. Spines are seeded stable per shelf.
	var spots := [
		[Vector3(-3.2, 0, -13.2), PI, 101], [Vector3(3.2, 0, -13.2), PI, 102],
		[Vector3(-3.2, 0, -18.8), 0.0, 103], [Vector3(3.2, 0, -18.8), 0.0, 104],
	]
	for s in spots:
		var shelf := PropKit.tape_shelf(3.0, 2.2, 4, s[2])
		shelf.position = s[0]
		shelf.rotation.y = s[1]
		add_child(shelf)
		_collider(s[0] + Vector3(0, 1.1, 0), Vector3(3.0, 2.2, 0.5))


func _spawn_transmitter_hall() -> void:
	## The loudest room gets its furniture: rack cabinets along the east wall,
	## gauges disagreeing, one lamp per cabinet still warm.
	for i in 4:
		var z := -2.0 - 2.5 * float(i)
		var cab := PropKit.transmitter_cabinet(2.4, 200 + i)
		cab.position = Vector3(20.4, 0, z)
		cab.rotation.y = -PI / 2.0
		add_child(cab)
		_collider(Vector3(20.4, 1.2, z), Vector3(0.7, 2.4, 0.9))


func _spawn_yard_dressing() -> void:
	## The tower. Its light is the one the completed sign-off puts out.
	var t: Dictionary = PropKit.tower(7.5)
	var rig := t["rig"] as Node3D
	rig.position = Vector3(-9.0, 0, 14.5)
	rig.add_to_group("tower")
	add_child(rig)
	_collider(Vector3(-9.0, 1.2, 14.5), Vector3(1.5, 2.4, 1.5))
	GameState.ending_marked.connect(func(ending_name: String) -> void:
		if ending_name == "THE COMPLETED SIGN-OFF":
			var bm := t["beacon_mat"] as StandardMaterial3D
			bm.emission_enabled = false
			bm.albedo_color = Color(0.25, 0.1, 0.08)
	)
	## pallets by the base, the kind every yard accumulates
	var pallet_mat := PropKit.wood("pallet", Color(0.45, 0.38, 0.28))
	for p in [Vector3(-6.5, 0.06, 13.0), Vector3(-6.2, 0.06, 15.6)]:
		for i in 3:
			var slat := MeshInstance3D.new()
			var sb := BoxMesh.new()
			sb.size = Vector3(1.1, 0.05, 0.24)
			sb.material = pallet_mat
			slat.mesh = sb
			slat.position = p + Vector3(0, 0, -0.35 + 0.35 * float(i))
			add_child(slat)


func _spawn_dead_room_felt() -> void:
	## The lining: felt panels on the quiet room's inner faces. The hum stops
	## at the seam; the felt is why.
	PropKit.felt_run(3.6, self, Vector3(19.0, 0, 4.8), PI)
	PropKit.felt_run(4.4, self, Vector3(17.2, 0, 2.5), PI / 2.0)
	PropKit.felt_run(4.4, self, Vector3(20.8, 0, 2.5), -PI / 2.0)


func _spawn_kitchen() -> void:
	## The kitchen earns its name: counter run on the north wall, the sink,
	## and the kettle — the one that clicks off two rooms away, eventually.
	var block := PropKit.kitchen_block(5.0)
	block.position = Vector3(8.0, 0, -2.15)
	add_child(block)
	_collider(Vector3(8.0, 0.45, -2.15), Vector3(5.0, 0.95, 0.62))
	var kettle := PropKit.kettle()
	kettle.position = Vector3(9.4, 0.91, -2.1)
	kettle.rotation.y = 0.6
	add_child(kettle)
	## two mugs nobody collected
	for m in [Vector3(8.4, 0.91, -2.2), Vector3(8.62, 0.91, -2.05)]:
		var mug := MeshInstance3D.new()
		var mc := CylinderMesh.new()
		mc.top_radius = 0.04
		mc.bottom_radius = 0.035
		mc.height = 0.09
		mc.radial_segments = 10
		mc.material = PropKit.OCHRE_MAT()
		mug.mesh = mc
		mug.position = m + Vector3(0, 0.045, 0)
		add_child(mug)
	## a small table where the club took its breaks
	var table_mat := PropKit.wood("ktable", Color(0.4, 0.32, 0.22))
	var table := MeshInstance3D.new()
	var tb := BoxMesh.new()
	tb.size = Vector3(0.9, 0.05, 0.9)
	tb.material = table_mat
	table.mesh = tb
	table.position = Vector3(9.6, 0.74, 1.0)
	add_child(table)
	var t_leg := MeshInstance3D.new()
	var tlc := CylinderMesh.new()
	tlc.top_radius = 0.05
	tlc.bottom_radius = 0.09
	tlc.height = 0.72
	tlc.material = table_mat
	t_leg.mesh = tlc
	t_leg.position = Vector3(9.6, 0.36, 1.0)
	add_child(t_leg)
	_collider(Vector3(9.6, 0.4, 1.0), Vector3(0.9, 0.8, 0.9))


func _spawn_yard_ground() -> void:
	## the yard underfoot: packed dirt, and the path everyone actually walked
	var dirt := MeshInstance3D.new()
	var db := BoxMesh.new()
	db.size = Vector3(29.6, 0.03, 7.6)
	db.material = PropKit._surface("dirt", Color(0.3, 0.25, 0.18), 0.98, 0.0, 131, 2.0, 0.8, 4.0)
	dirt.mesh = db
	dirt.position = Vector3(0, 0.015, 14.0)
	add_child(dirt)
	var path_mat := PropKit._surface("path", Color(0.38, 0.32, 0.24), 0.99, 0.0, 137, 2.6, 0.5, 4.0)
	## entry door north to the shed door, two worn legs
	var leg1 := MeshInstance3D.new()
	var l1 := BoxMesh.new()
	l1.size = Vector3(1.1, 0.035, 4.2)
	l1.material = path_mat
	leg1.mesh = l1
	leg1.position = Vector3(0, 0.02, 12.4)
	add_child(leg1)
	var leg2 := MeshInstance3D.new()
	var l2 := BoxMesh.new()
	l2.size = Vector3(8.6, 0.035, 1.1)
	l2.material = path_mat
	leg2.mesh = l2
	leg2.position = Vector3(4.2, 0.02, 14.0)
	add_child(leg2)


func _spawn_green_room() -> void:
	## Where the cast waited: vanity with its two-of-three bulbs, the couch,
	## the low table. Ending 2 inherits a warm chair here; it should look sat-in.
	var v := PropKit.vanity()
	v.position = Vector3(-27.1, 0, -27.0)
	v.rotation.y = PI / 2.0
	add_child(v)
	_collider(Vector3(-27.1, 0.8, -27.0), Vector3(0.55, 1.6, 1.5))
	var c := PropKit.couch(Color(0.45, 0.38, 0.3))
	c.position = Vector3(-25.0, 0, -29.4)
	add_child(c)
	_collider(Vector3(-25.0, 0.4, -29.4), Vector3(1.9, 0.8, 0.75))
	var table := MeshInstance3D.new()
	var tb := BoxMesh.new()
	tb.size = Vector3(0.8, 0.06, 0.5)
	tb.material = PropKit.wood("greentable", Color(0.36, 0.28, 0.19))
	table.mesh = tb
	table.position = Vector3(-25.2, 0.4, -28.3)
	add_child(table)
	for lx in [-0.3, 0.3]:
		for lz in [-0.18, 0.18]:
			var leg := MeshInstance3D.new()
			var lb := BoxMesh.new()
			lb.size = Vector3(0.05, 0.4, 0.05)
			lb.material = PropKit.wood("greentable", Color(0.36, 0.28, 0.19))
			leg.mesh = lb
			leg.position = Vector3(-25.2 + lx, 0.2, -28.3 + lz)
			add_child(leg)
	_collider(Vector3(-25.2, 0.25, -28.3), Vector3(0.8, 0.5, 0.5))


func _spawn_scene_dock_dressing() -> void:
	## The dock holds what the show retired: flats leaning in ranks, crates
	## that were always about to ship somewhere.
	var flat_tints := [Color(0.35, 0.42, 0.24), Color(0.45, 0.3, 0.2), Color(0.43, 0.5, 0.67)]
	for i in 3:
		var f := PropKit.scene_flat(flat_tints[i], 2.0 - 0.3 * float(i), 2.4 - 0.2 * float(i))
		f.position = Vector3(-20.1 + 0.14 * float(i), 0, -38.2 - 1.4 * float(i))
		f.rotation.y = PI / 2.0
		f.rotation.z = -0.12 - 0.02 * float(i)  ## the lean
		add_child(f)
	_collider(Vector3(-19.9, 1.1, -39.6), Vector3(0.7, 2.2, 4.2))
	var crate_mat := PropKit.wood("crate", Color(0.45, 0.38, 0.28))
	var crate_spots := [
		[Vector3(-11.3, 0.35, -42.0), Vector3(0.7, 0.7, 0.7)],
		[Vector3(-11.3, 1.0, -42.0), Vector3(0.6, 0.6, 0.6)],
		[Vector3(-12.3, 0.3, -42.2), Vector3(0.6, 0.6, 0.8)],
	]
	for cs in crate_spots:
		var crate := MeshInstance3D.new()
		var cb := BoxMesh.new()
		cb.size = cs[1]
		cb.material = crate_mat
		crate.mesh = cb
		crate.position = cs[0]
		add_child(crate)
	_collider(Vector3(-11.7, 0.7, -42.1), Vector3(1.8, 1.4, 1.0))


func _spawn_dorms_extra() -> void:
	## The other beds. The club sleeps here, or stands where sleeping goes.
	var bed_a := PropKit.dorm_bed(Color(0.36, 0.4, 0.32))
	bed_a.position = Vector3(-12.0, 0, 1.6)
	add_child(bed_a)
	_collider(Vector3(-12.0, 0.3, 1.6), Vector3(2.0, 0.6, 1.0))
	var bed_b := PropKit.dorm_bed(Color(0.42, 0.34, 0.26))
	bed_b.position = Vector3(-6.2, 0, 1.6)
	add_child(bed_b)
	_collider(Vector3(-6.2, 0.3, 1.6), Vector3(2.0, 0.6, 1.0))
	var lockers := PropKit.locker_run(4)
	lockers.position = Vector3(-7.2, 0, -2.2)
	add_child(lockers)
	_collider(Vector3(-7.2, 0.95, -2.2), Vector3(1.8, 1.9, 0.55))


func _spawn_shed_interior() -> void:
	## Behind the EDITH padlock: a shelf of cans, a broom, and the reason
	## you came. The key sits where it always sat.
	var shelf := MeshInstance3D.new()
	var sb := BoxMesh.new()
	sb.size = Vector3(0.3, 0.04, 2.4)
	sb.material = PropKit.wood("shedshelf", Color(0.4, 0.33, 0.24))
	shelf.mesh = sb
	shelf.position = Vector3(11.2, 1.2, 14.0)
	add_child(shelf)
	for i in 3:
		var can := MeshInstance3D.new()
		var cc := CylinderMesh.new()
		cc.top_radius = 0.08
		cc.bottom_radius = 0.08
		cc.height = 0.2
		cc.radial_segments = 10
		cc.material = PropKit.metal("paintcan", Color(0.5, 0.47, 0.42))
		can.mesh = cc
		can.position = Vector3(11.2, 1.32, 13.4 + 0.6 * float(i))
		add_child(can)
	var broom := MeshInstance3D.new()
	var bb := BoxMesh.new()
	bb.size = Vector3(0.04, 1.5, 0.04)
	bb.material = PropKit.wood("broom", Color(0.5, 0.4, 0.28))
	broom.mesh = bb
	broom.position = Vector3(8.9, 0.75, 15.1)
	broom.rotation.z = 0.18
	add_child(broom)
	var head := MeshInstance3D.new()
	var hb := BoxMesh.new()
	hb.size = Vector3(0.3, 0.12, 0.06)
	hb.material = PropKit.fabric("broomhead", Color(0.6, 0.52, 0.36))
	head.mesh = hb
	head.position = Vector3(9.03, 0.06, 15.1)
	add_child(head)
