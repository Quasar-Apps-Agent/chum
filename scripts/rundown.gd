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
const AF_APPROACH_SPEED := 0.8
const AF_LOOM_DIST := 1.2
const AF_COOL_SECONDS := 2.0
const AF_HEIGHT := 3.35
const AF_FOLD_SECONDS := 2.2
const AF_DOOR_NEAR := 1.0
const AF_CROSSING_SPEED := 1.6
const DEADROOM_DOOR := Vector3(19.0, 0.0, 0.0)
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
var _af_seen_once := false
var _af_cool := -100.0
var _af_step_t := 0.0
var _af_bodied := false
var _fold_t := 0.0
var _fold_cool: Dictionary = {}
var doors: Array = []
var _rig: Node3D
var _head: Node3D
var _jaw: Node3D
var _hip_l: Node3D
var _hip_r: Node3D
var _shoulder_l: Node3D
var _shoulder_r: Node3D
var _tail_pivot: Node3D
var _eye: OmniLight3D
var _eye_ball: MeshInstance3D
var _deadroom_line := false

## the built rig stands ~2.7 to the ear tips; the scale law measures the body
const BASE_HEIGHT := 2.6

var _idx := 0
var _target := Vector3.ZERO
var _player: Node3D
var _warned := false
var _label: Label3D
var _audio: AudioStreamPlayer3D
var _tone: ToneEmitter

const SEGMENT_FREQS := [220.0, 262.0, 196.0]


func _ready() -> void:
	## The body: rebuilt salvage per the dossier — flannel, seams, the lever jaw.
	## (character_kit.gd. The old black box retired with the greybox era.)
	var parts := CharacterKit.chum_hero()
	_rig = parts["rig"]
	_head = parts["head"]
	_jaw = parts["jaw"]
	add_child(_rig)
	## limb pivots, present on the sculpted body (null on the fallback: guarded)
	_hip_l = _rig.find_child("HipL", true, false) as Node3D
	_hip_r = _rig.find_child("HipR", true, false) as Node3D
	_shoulder_l = _rig.find_child("ShoulderL", true, false) as Node3D
	_shoulder_r = _rig.find_child("ShoulderR", true, false) as Node3D
	_tail_pivot = _rig.find_child("TailPivot", true, false) as Node3D
	## the right eye socket carries the tally eye: red only while a capture runs
	_eye_ball = MeshInstance3D.new()
	var eb := SphereMesh.new()
	eb.radius = 0.027
	eb.height = 0.054
	var em := StandardMaterial3D.new()
	em.emission_enabled = true
	em.emission = Color(0.9, 0.15, 0.1)
	em.emission_energy_multiplier = 2.0
	eb.material = em
	_eye_ball.mesh = eb
	_eye_ball.position = Vector3(0.13, 0.06, 0.39)
	_head.add_child(_eye_ball)
	_eye = OmniLight3D.new()
	_eye.light_color = Color(0.9, 0.15, 0.1)
	_eye.light_energy = 0.0
	_eye.omni_range = 6.0
	_eye.position = Vector3(0.13, 0.06, 0.34)
	_head.add_child(_eye)
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
	if GameState.in_dead_room(pos):
		return
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
		if GameState.crossing:
			visible = true
			if _eye:
				_eye.light_energy = 0.0
			if _player == null:
				_player = get_tree().get_first_node_in_group("player")
			if _player == null:
				return
			if _fold_t > 0.0:
				_fold_t -= delta
				return
			if _door_fold_check():
				return
			var cd := global_position.distance_to(_player.global_position)
			if cd < _strike_r:
				if not GameState.crossing_caught:
					GameState.crossing_caught = true
					_strike_pose_t = 0.9
					GameState.toast("A hand the size of a door closes the distance. NEXT WEEK'S EPISODE.")
					GameState.run_ended.emit(GameState.dailies.size())
				return
			global_position = global_position.move_toward(_player.global_position, AF_CROSSING_SPEED * delta)
			_af_step_t += delta
			if _af_step_t > 0.7:
				_af_step_t = 0.0
				Sfx.thunk(global_position)
			return
		visible = false
		return
	if GameState.af_active and not _af_bodied:
		_af_bodied = true
		## the scale law: the whole rig grows to the eleven-footer; the tally
		## eye rides the head, so it lands at the canonical 3 m on its own
		_rig.scale = Vector3.ONE * (AF_HEIGHT / BASE_HEIGHT)
		_label.position.y = AF_HEIGHT + 0.35
	if _eye:
		_eye.light_energy = 1.6 if (GameState.af_active and GameState.recording) else 0.0
	if GameState.af_active and GameState.recording and _player:
		visible = true
		if _fold_t > 0.0:
			_fold_t -= delta
			return
		var pd := global_position.distance_to(_player.global_position)
		if GameState.in_dead_room(_player.global_position):
			if global_position.distance_to(DEADROOM_DOOR) > 0.6:
				if _door_fold_check():
					return
				global_position = global_position.move_toward(DEADROOM_DOOR, AF_APPROACH_SPEED * delta)
			elif not _deadroom_line:
				_deadroom_line = true
				GameState.toast("It stops at the felt door. The room inside owes the air nothing, and it knows.")
			return
		if pd > AF_LOOM_DIST:
			if _door_fold_check():
				return
			global_position = global_position.move_toward(_player.global_position, AF_APPROACH_SPEED * delta)
			_af_step_t += delta
			if _af_step_t > 1.1:
				_af_step_t = 0.0
				Sfx.thunk(global_position)
		elif not _af_seen_once:
			_af_seen_once = true
			GameState.show_caption("[THE JAW WORKS ITS LEVER]")
			GameState.toast("It stands at the edge of the bench light. Eleven feet of salvage, watching the tally. The jaw hand moves. Nothing else does.")
			_work_jaw()
		_af_cool = -100.0
		return
	if GameState.af_active and _player and _af_cool < -50.0 and not GameState.recording and visible and not GameState.is_night:
		if GameState.af_taught:
			_af_cool = AF_COOL_SECONDS
			GameState.toast("The tally cools.")
		else:
			GameState.af_taught = true
			_af_cool = 4.0
			GameState.toast("THE TALLY COOLS. Two doorways stand between you and anywhere. Use them.")
	if _af_cool > -50.0 and not GameState.is_night:
		_af_cool -= delta
		if _af_cool <= 0.0:
			if _player and global_position.distance_to(_player.global_position) < _strike_r + 0.4:
				if director:
					director.log_line("STRIKE af tally-cool")
				GameState.strike(_player)
			_af_cool = -100.0
			visible = false
			global_position = _anchor(_idx)
		return
	if not GameState.is_night:
		return
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
	if not Broadcast.on_air:
		if GameState.af_active and _fold_t > 0.0:
			_fold_t -= delta
			return
		if GameState.af_active and _door_fold_check():
			return
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
		_strike_pose_t = 0.9
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


func _door_fold_check() -> bool:
	if _fold_t > 0.0:
		return true
	var now := Time.get_ticks_msec() / 1000.0
	for i in doors.size():
		var dp: Vector3 = doors[i]
		if global_position.distance_to(dp) < AF_DOOR_NEAR and now - float(_fold_cool.get(i, -100.0)) > 6.0:
			_fold_cool[i] = now
			_fold_t = AF_FOLD_SECONDS
			Sfx.thunk(global_position)
			GameState.show_caption("[IT FOLDS THROUGH THE DOORWAY]")
			if _player and global_position.distance_to(_player.global_position) < 12.0:
				GameState.toast("A doorway. It stops, and bends, and keeps its eye on you the whole way through.")
			return true
	return false


func _anchor(i: int) -> Vector3:
	var zone: String = SEGMENTS[i][1]
	if rooms.has(zone):
		var r: Array = rooms[zone]
		return Vector3(r[0], 0, r[1])
	return Vector3.ZERO


func _work_jaw() -> void:
	## the jaw, worked twice on its lever. Nothing else moves.
	if _jaw == null:
		return
	var tw := create_tween()
	for i in 2:
		tw.tween_property(_jaw, "rotation:x", 0.55, 0.45).set_trans(Tween.TRANS_SINE)
		tw.tween_property(_jaw, "rotation:x", 0.0, 0.6).set_trans(Tween.TRANS_SINE)
		tw.tween_interval(0.4)


var _last_gp := Vector3.ZERO
var _gait_t := 0.0
var _idle_t := 0.0
var _strike_pose_t := 0.0
const HEAD_TILT := 0.045  ## delta 8: the restitched neck, never straight


func _process(delta: float) -> void:
	## The body language, layered by priority: the strike pose, the doorway
	## fold, the walk, and — when he only stands — the performance. The head
	## watches you through all of it. That is the character.
	if _rig == null:
		return
	var moved := global_position - _last_gp
	_last_gp = global_position
	moved.y = 0.0
	_head_track(delta)
	if _strike_pose_t > 0.0:
		_strike_pose_t -= delta
		_pose_strike(delta)
		return
	if _fold_t > 0.0 and visible:
		_pose_fold(delta)
		return
	if visible and moved.length() > 0.001:
		var stride := 1.5 if _af_bodied else 2.4
		_gait_t += delta * TAU * stride * 0.5
		var amp := 0.1 if _af_bodied else 0.05
		_rig.position.y = absf(sin(_gait_t)) * amp
		_rig.rotation.z = sin(_gait_t) * (0.05 if _af_bodied else 0.03)
		_rig.rotation.y = lerp_angle(_rig.rotation.y, atan2(moved.x, moved.z), minf(6.0 * delta, 1.0))
		## the walk, jointed: legs stride, arms counter-swing, the tail drags
		var swing := sin(_gait_t) * (0.32 if _af_bodied else 0.24)
		if _hip_l:
			_hip_l.rotation.x = swing
			_hip_r.rotation.x = -swing
			_shoulder_l.rotation.x = -swing * 0.6
			_shoulder_r.rotation.x = swing * 0.6
		if _tail_pivot:
			_tail_pivot.rotation.y = sin(_gait_t - 0.9) * 0.22
		return
	## standing: settle the frame, then perform
	_rig.position.y = lerpf(_rig.position.y, 0.0, minf(8.0 * delta, 1.0))
	_rig.rotation.x = lerpf(_rig.rotation.x, 0.0, minf(6.0 * delta, 1.0))
	_rig.rotation.z = lerpf(_rig.rotation.z, 0.0, minf(8.0 * delta, 1.0))
	var looming := GameState.af_active and GameState.recording
	if visible and Broadcast.on_air and GameState.is_night and not looming and not GameState.premiere_live:
		## the segment, performed to no one: the jaw works the lines, the
		## arms present to an audience that is not there
		_idle_t += delta
		_rig.rotation.z = sin(_idle_t * 1.1) * 0.02
		if _jaw:
			_jaw.rotation.x = maxf(0.0, sin(_idle_t * 5.6)) * 0.16 + maxf(0.0, sin(_idle_t * 12.7)) * 0.05
		if _shoulder_l:
			_shoulder_l.rotation.x = -0.28 + 0.2 * sin(_idle_t * 0.7)
			_shoulder_r.rotation.x = -0.28 + 0.2 * sin(_idle_t * 0.7 + PI)
		if _hip_l:
			_hip_l.rotation.x = lerpf(_hip_l.rotation.x, 0.0, minf(7.0 * delta, 1.0))
			_hip_r.rotation.x = lerpf(_hip_r.rotation.x, 0.0, minf(7.0 * delta, 1.0))
		if _tail_pivot:
			_tail_pivot.rotation.y = sin(_idle_t * 0.5) * 0.12
		return
	## truly still: everything eases home. The stillness is also a performance.
	if _jaw and not looming:
		_jaw.rotation.x = lerpf(_jaw.rotation.x, 0.0, minf(5.0 * delta, 1.0))
	if _hip_l:
		_hip_l.rotation.x = lerpf(_hip_l.rotation.x, 0.0, minf(7.0 * delta, 1.0))
		_hip_r.rotation.x = lerpf(_hip_r.rotation.x, 0.0, minf(7.0 * delta, 1.0))
		_shoulder_l.rotation.x = lerpf(_shoulder_l.rotation.x, 0.0, minf(7.0 * delta, 1.0))
		_shoulder_r.rotation.x = lerpf(_shoulder_r.rotation.x, 0.0, minf(7.0 * delta, 1.0))
	if _tail_pivot:
		_tail_pivot.rotation.y = lerpf(_tail_pivot.rotation.y, 0.0, minf(7.0 * delta, 1.0))


func _head_track(delta: float) -> void:
	## The eye finds you and holds. Through the walk, through the fold,
	## through the performance: the head is always the honest part.
	if _head == null:
		return
	var target_yaw := 0.0
	if _player and visible:
		var dp := _player.global_position - global_position
		if dp.length() < 11.0:
			var desired := atan2(dp.x, dp.z) - rotation.y - _rig.rotation.y
			target_yaw = clampf(wrapf(desired, -PI, PI), -1.05, 1.05)
	_head.rotation.y = lerp_angle(_head.rotation.y, target_yaw, minf(3.5 * delta, 1.0))
	_head.rotation.z = HEAD_TILT


func _pose_fold(delta: float) -> void:
	## The doorway fold, embodied: he compresses, ducks, pulls the arms in,
	## and does not stop watching you. Envelope peaks mid-threshold.
	var k := sin(PI * clampf(1.0 - _fold_t / AF_FOLD_SECONDS, 0.0, 1.0))
	_rig.position.y = -0.35 * k
	_rig.rotation.x = 0.55 * k
	if _hip_l:
		_hip_l.rotation.x = lerpf(_hip_l.rotation.x, 0.55 * k, minf(8.0 * delta, 1.0))
		_hip_r.rotation.x = lerpf(_hip_r.rotation.x, 0.55 * k, minf(8.0 * delta, 1.0))
		_shoulder_l.rotation.x = lerpf(_shoulder_l.rotation.x, -0.7 * k, minf(8.0 * delta, 1.0))
		_shoulder_r.rotation.x = lerpf(_shoulder_r.rotation.x, -0.7 * k, minf(8.0 * delta, 1.0))
	if _head:
		_head.rotation.x = -0.3 * k
	if _tail_pivot:
		_tail_pivot.rotation.y = 0.3 * k


func _pose_strike(_delta: float) -> void:
	## the delivery: both arms rise, the jaw opens past the grin
	if _jaw:
		_jaw.rotation.x = minf(_jaw.rotation.x + 6.0 * _delta, 0.9)
	if _shoulder_l:
		_shoulder_l.rotation.x = maxf(_shoulder_l.rotation.x - 8.0 * _delta, -1.6)
		_shoulder_r.rotation.x = maxf(_shoulder_r.rotation.x - 8.0 * _delta, -1.6)
	_rig.rotation.x = minf(_rig.rotation.x + 1.2 * _delta, 0.18)
