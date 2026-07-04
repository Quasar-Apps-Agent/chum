class_name Rundown
extends Node3D
## The show, performing itself through the building. Stub of the free-roam threat.
## ON AIR: it performs a segment in its zone (approach at your peril).
## BREAK: it relocates. Segment audio is the location tell; audio assets arrive
## later, so for now the tell is the label and the toast.

## [segment name, home zone] · CRAFT TIME's true home is the workshop; PATCH BAY stands in.
const SEGMENTS := [
	["STORY CORNER", "TAPE LIBRARY"],
	["THE SONG", "STUDIO A"],
	["CRAFT TIME", "PATCH BAY"],
]
const MOVE_SPEED := 2.4
const WARN_RADIUS := 7.0
const STRIKE_RADIUS := 2.2

var rooms: Dictionary = {}
var rigs: Array = []
var director: CoverageDirector

var _warn_r := WARN_RADIUS
var _strike_r := STRIKE_RADIUS
var _heard_pos := Vector3.ZERO
var _heard_t := -100.0
var _heard_once := false

var _idx := 0
var _target := Vector3.ZERO
var _player: Node3D
var _warned := false
var _label: Label3D
var _audio: AudioStreamPlayer3D
var _tone: ToneEmitter

const SEGMENT_FREQS := [220.0, 262.0, 196.0]


func _ready() -> void:
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(0.6, 2.6, 0.6)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.05, 0.045, 0.04)
	box.material = mat
	mesh.mesh = box
	mesh.position = Vector3(0, 1.3, 0)
	add_child(mesh)
	_label = Label3D.new()
	_label.font_size = 40
	_label.modulate = Color(0.5, 0.45, 0.38)
	_label.position = Vector3(0, 2.9, 0)
	_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(_label)
	## Segment loop audio plugs in here when assets exist; the tone stands in.
	_audio = AudioStreamPlayer3D.new()
	_audio.max_distance = 24.0
	add_child(_audio)
	_tone = ToneEmitter.new()
	_tone.freq_a = SEGMENT_FREQS[0]
	_tone.freq_b = SEGMENT_FREQS[0] * 1.5
	_tone.volume_db = -16.0
	_tone.reach = 22.0
	add_child(_tone)
	_tone.set_active(GameState.is_night)
	GameState.noise_event.connect(_on_noise)
	global_position = _anchor(_idx)
	_target = global_position
	_label.text = SEGMENTS[_idx][0]
	Broadcast.phase_changed.connect(_on_phase)
	GameState.night_changed.connect(_on_night)
	visible = GameState.is_night


func _on_noise(pos: Vector3, loudness: float) -> void:
	if not GameState.is_night or GameState.premiere_live:
		return
	if pos.distance_to(global_position) < loudness * 3.0:
		_heard_pos = pos
		_heard_t = Time.get_ticks_msec() / 1000.0


func _on_night(now_night: bool) -> void:
	visible = now_night
	if _tone:
		_tone.set_active(now_night)
	if now_night:
		global_position = _anchor(_idx)
		_warned = false


func _on_phase(now_on_air: bool) -> void:
	if now_on_air:
		_label.text = SEGMENTS[_idx][0]
		_warned = false
		_strike_r = 2.6 if GameState.strikes >= 3 else STRIKE_RADIUS
		_warn_r = 5.0 if (director and director.profile() == "HIDER") else WARN_RADIUS
		if GameState.cascade_active:
			_warn_r = maxf(3.5, _warn_r - 1.5)
		if GameState.is_night:
			if director and director.profile() == "CHECKER":
				var m := director.most_watched_rig()
				if m and not m.killed and m.cam_position.distance_to(global_position) < 14.0:
					m.set_killed(true)
					director.log_line("KILL most-watched rig (CHECKER read)")
					GameState.toast("The feed you trust went dark first.")
			for rig in rigs:
				if not rig.killed and rig.cam_position.distance_to(global_position) < 9.0:
					rig.set_killed(true)
					GameState.toast("Somewhere, a camera dies. The map is shorter tonight.")
	else:
		var now_s := Time.get_ticks_msec() / 1000.0
		if now_s - _heard_t < 12.0:
			var best_h := _idx
			var best_hd := INF
			for i in SEGMENTS.size():
				var dh := _anchor(i).distance_to(_heard_pos)
				if dh < best_hd:
					best_hd = dh
					best_h = i
			_idx = best_h
			if director:
				director.log_line("RELOCATE toward heard noise at %s -> segment %d" % [str(_heard_pos.round()), _idx])
			if not _heard_once:
				_heard_once = true
				Achievements.unlock("A08")
				GameState.toast("It changed direction. You were not quiet.")
		elif director and director.profile() == "SPRINTER" and _player:
			var best := _idx
			var best_d := INF
			for i in SEGMENTS.size():
				var d := _anchor(i).distance_to(_player.global_position)
				if d < best_d:
					best_d = d
					best = i
			_idx = best
			director.log_line("RELOCATE sprinter-bias -> segment %d" % _idx)
		else:
			_idx = (_idx + 1) % SEGMENTS.size()
			if director:
				director.log_line("RELOCATE cycle -> segment %d (profile %s)" % [_idx, director.profile()])
		_target = _anchor(_idx)
		_label.text = "· in transit ·"
		if _tone:
			_tone.freq_a = SEGMENT_FREQS[_idx]
			_tone.freq_b = SEGMENT_FREQS[_idx] * 1.5


func _physics_process(delta: float) -> void:
	if GameState.premiere_live:
		visible = false
		return
	if not GameState.is_night:
		return
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
	if not Broadcast.on_air:
		global_position = global_position.move_toward(_target, MOVE_SPEED * delta)
		return
	if _player == null:
		return
	var d := global_position.distance_to(_player.global_position)
	if d < _strike_r:
		var thru := false
		var space := get_world_3d().direct_space_state
		var q := PhysicsRayQueryParameters3D.create(
			global_position + Vector3.UP, _player.global_position + Vector3.UP)
		q.exclude = [_player.get_rid()]
		var hit := space.intersect_ray(q)
		if hit and hit.get("collider") != _player:
			thru = true
		if director:
			director.log_line("STRIKE seg %d d=%.1f%s%s" % [
				_idx, d,
				" savor" if GameState.strikes >= 3 else "",
				" THRU-WALL" if thru else ""])
		GameState.strike(_player)
		_warned = false
	elif d < _warn_r and not _warned:
		_warned = true
		if director:
			director.log_line("WARN seg %d d=%.1f%s" % [_idx, d, " savor" if GameState.strikes >= 3 else ""])
		if GameState.strikes >= 3:
			GameState.toast("It is not hurrying anymore.")
		else:
			GameState.toast("You can hear it. %s, performed to no one." % SEGMENTS[_idx][0])


func _anchor(i: int) -> Vector3:
	var zone: String = SEGMENTS[i][1]
	if rooms.has(zone):
		var r: Array = rooms[zone]
		return Vector3(r[0], 0, r[1])
	return Vector3.ZERO
