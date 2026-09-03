extends Node
## Autoload: run state, settings, and the transmitter-log save system.
## Canon: saving is signing a log station; paper is finite on Late Night.

const SAVE_PATH := "user://transmitter_log.json"
const DEMO := false  ## flip true for the Tape 1 demo build
const SAVE_VERSION := 16

enum Mode { MATINEE, LATE_NIGHT, ONE_TAKE }

var mode: int = Mode.LATE_NIGHT
var tbc_enabled: bool = false
var current_tape: int = 1

## paper remaining per station (Late Night default: 3 lines per tape)
var paper: Dictionary = {"S1": 3, "S2": 3, "S3": 3, "S4": 3, "S5": 3}
var signatures: Array = []

signal tbc_changed(enabled: bool)
signal log_signed(station: String, remaining: int)
signal log_refused(station: String)
signal notify(text: String)
signal capture_status(text: String)

var captures: Array = []
var strikes: int = 0
var items_lost: int = 0
var day: int = 1
var is_night: bool = false
var in_retake: bool = false
var station_points: Dictionary = {}
var keys: Array = []
var pt: int = 0
var dailies: Array = []
var daily_seq: int = 0
var carried_id: int = -1
var carried_take: int = 0
var film_watched: bool = false
var signals_known: Array = []
var screening_done: bool = false
var run_complete: bool = false
var coverage_label: String = "AUDIENCE"
var has_fire_tape: bool = false
var fire_tape_watched: bool = false
var seance_wear: float = 0.0
var leland_answers: Array = []
var presigned_seen: bool = false
var dock_done: bool = false
var assets: Array = []
var decision: String = ""
var lockdown_done: bool = false
var finale_done: bool = false
var ending_reached: String = ""
var lie_pending: bool = false
var premiere_live: bool = false
var screening_active: bool = false
var map_points: Array = []
var vess_insight: bool = false
var vess_credited: bool = false
var ng_relic: String = ""
var cov_monitor: float = 0.0
var cov_move: float = 0.0
var cov_still: float = 0.0
var photo_safe: bool = false
var cascade_done: bool = false
var cascade_active: bool = false
var mouse_sens: float = 1.0
var ui_scale: float = 1.0
var captions_on: bool = false
var assist_on: bool = false
var read_props: Array = []
var af_active: bool = false
var recording: bool = false
var recording_left: float = 0.0
var af_taught: bool = false
var deadroom_seen: bool = false
var crossing: bool = false
var crossing_caught: bool = false
var casualties: Array = []
var harriet_slip: bool = false
var merle_offered: bool = false
var fader_self: bool = false
var signoff_completed: bool = false
var row_casualties: int = 0
var h2_pending: bool = false


func cause_of(who: String) -> String:
	for c in casualties:
		if c.get("who", "") == who:
			return str(c.get("cause", ""))
	return ""


func mint_shortcut_daily() -> void:
	daily_seq += 1
	dailies.append({"id": daily_seq, "take": -1})
	daily_added.emit(daily_seq, -1)
	save_log()


func all_cast_dead() -> bool:
	return is_dead("MERLE") and is_dead("VESS") and is_dead("HARRIET") and is_dead("FLOOR MANAGER")


func is_dead(who: String) -> bool:
	for c in casualties:
		if c.get("who", "") == who:
			return true
	return false


func mark_casualty(who: String, cause: String, epitaph: String) -> void:
	if is_dead(who):
		return
	casualties.append({"who": who, "cause": cause, "line": epitaph, "day": day})
	save_log()
	toast("THE LEDGER TAKES IT DOWN.")


func in_dead_room(pos: Vector3) -> bool:
	return absf(pos.x - 19.0) <= 2.2 and absf(pos.z - 2.5) <= 2.7

var _glyph_re: Dictionary = {}
const GLYPH_MAP := {"E": "interact", "SPACE": "respond", "Q": "improvise", "T": "toggle_tbc", "M": "map"}
var crate_opened: bool = false
var night_tripped: bool = false
var rejected_seen: bool = false
var glimpse_seen: bool = false
var merle_1974: bool = false
var fire_unsealed: bool = false

const ITEM_ORDER := ["WATCH", "PEN", "PHOTOGRAPH", "LIGHTER", "COMPACT", "KEYS", "LOUPE"]

signal sheet_changed(count: int)
signal night_changed(now_night: bool)
signal captured(take: int, sheet_full: bool, lost_item: String, respawn: Vector3)
signal daily_added(id: int, take: int)
signal daily_burned
signal run_ended(take: int)
signal finale_started(decision: String)
signal noise_event(pos: Vector3, loudness: float)
signal photo_changed(on: bool)
signal blackout_changed(alpha: float)
signal ui_scale_changed(scale: float)
signal caption(text: String)
signal pause_requested
signal demo_ended
signal ending_marked(ending_name: String)


func _ready() -> void:
	load_settings()
	load_log()


func paper_for(station: String) -> int:
	if mode == Mode.MATINEE:
		return 99
	return int(paper.get(station, 0))


func sign_log(station: String) -> bool:
	if mode != Mode.MATINEE:
		if paper_for(station) <= 0:
			if harriet_slip:
				harriet_slip = false
				toast("Signed. The hand on the slip is not yours, and the log accepts it anyway.")
			else:
				log_refused.emit(station)
				return false
		else:
			paper[station] = paper_for(station) - 1
		return _sign_finish(station)
	return _sign_finish(station)


func _sign_finish(station: String) -> bool:
	signatures.append({
		"station": station,
		"tape": current_tape,
		"signed": Time.get_datetime_string_from_system(),
	})
	save_log()
	Sfx.tick()
	if station == "S1":
		demo_mark("s1_signed")
	log_signed.emit(station, paper_for(station))
	noise_event.emit(respawn_point(), 4.0)
	return true


func glyphs(text: String) -> String:
	for token in GLYPH_MAP:
		if not _glyph_re.has(token):
			var r := RegEx.new()
			r.compile("\\b%s\\b" % token)
			_glyph_re[token] = r
		text = (_glyph_re[token] as RegEx).sub(text, key_name(GLYPH_MAP[token]).to_upper(), true)
	return text


func mark_read(id: String) -> void:
	if read_props.has(id):
		return
	read_props.append(id)
	save_log()
	toast("READ · filed to memory. (%d of 10 documents)" % read_props.size())


func toast(text: String) -> void:
	notify.emit(glyphs(tr(text)))


func set_capture_status_raw(text: String) -> void:
	capture_status.emit(text)


func set_capture_status(text: String) -> void:
	text = glyphs(text)
	capture_status.emit(text)


func log_capture(capture_name: String) -> void:
	captures.append({
		"name": capture_name,
		"tape": current_tape,
		"at": Time.get_datetime_string_from_system(),
	})
	save_log()
	notify.emit("CAPTURED · %s · presentation kept" % capture_name)


func register_station(id: String, pos: Vector3) -> void:
	station_points[id] = pos + Vector3(0, 0.5, 1.2)


func respawn_point() -> Vector3:
	if signatures.size() > 0:
		var last: Dictionary = signatures[signatures.size() - 1]
		var sid: String = str(last.get("station", ""))
		if station_points.has(sid):
			return station_points[sid]
	return Vector3(0, 1.0, 2.5)


func has_key(id: String) -> bool:
	return keys.has(id)


func take_key(id: String, display: String) -> void:
	if keys.has(id):
		toast("You already carry %s." % display)
		return
	keys.append(id)
	save_log()
	toast("TAKEN · %s" % display)


func add_show_signal(sig: String) -> void:
	if not signals_known.has(sig):
		signals_known.append(sig)


func pick_daily(id: int, take: int) -> void:
	for i in dailies.size():
		if int(dailies[i].get("id", -1)) == id:
			dailies.remove_at(i)
			break
	carried_id = id
	carried_take = take
	save_log()
	toast("CARRYING · SCENE 4 TAKE %d. The degausser is in the climate room." % take)


func burn_daily() -> void:
	var t := carried_take
	carried_id = -1
	carried_take = 0
	if strikes > 0:
		strikes -= 1
		toast("BURNED · TAKE %d. Her name fades from the line. Its read on you resets." % t)
	else:
		toast("BURNED · TAKE %d. The sheet was already clean. The canister burns anyway." % t)
	save_log()
	sheet_changed.emit(strikes)
	daily_burned.emit()


func set_mode(m: int) -> void:
	if mode == m:
		return
	mode = m
	save_log()
	var names := ["MATINEE", "LATE NIGHT", "ONE TAKE"]
	toast("MODE · %s" % names[m])
	if m == Mode.ONE_TAKE:
		toast("ONE TAKE · any capture ends the run. (Prototype honors sheet rules until run flow exists.)")


var _demo_t0 := 0


const SETTINGS_PATH := "user://settings.cfg"
const REMAP_ACTIONS := ["interact", "respond", "improvise", "toggle_tbc", "map"]


func load_settings() -> void:
	var cfg := ConfigFile.new()
	if cfg.load(SETTINGS_PATH) != OK:
		return
	var vol: float = cfg.get_value("audio", "master", 1.0)
	AudioServer.set_bus_volume_db(0, linear_to_db(maxf(vol, 0.001)))
	mouse_sens = clampf(cfg.get_value("input", "sensitivity", 1.0), 0.2, 3.0)
	ui_scale = cfg.get_value("access", "ui_scale", 1.0)
	captions_on = cfg.get_value("access", "captions", false)
	assist_on = cfg.get_value("access", "assist", false)
	for act in REMAP_ACTIONS:
		var pk: int = cfg.get_value("keys", act, 0)
		if pk > 0:
			rebind(act, pk, false)
	if cfg.get_value("video", "fullscreen", false) and DisplayServer.get_name() != "headless":
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)


func save_settings() -> void:
	var cfg := ConfigFile.new()
	cfg.set_value("audio", "master", db_to_linear(AudioServer.get_bus_volume_db(0)))
	cfg.set_value("input", "sensitivity", mouse_sens)
	cfg.set_value("access", "ui_scale", ui_scale)
	cfg.set_value("access", "captions", captions_on)
	cfg.set_value("access", "assist", assist_on)
	for act in REMAP_ACTIONS:
		for ev in InputMap.action_get_events(act):
			if ev is InputEventKey:
				cfg.set_value("keys", act, (ev as InputEventKey).physical_keycode)
				break
	cfg.set_value("video", "fullscreen",
		DisplayServer.get_name() != "headless"
		and DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN)
	cfg.save(SETTINGS_PATH)


func demo_mark(event: String) -> void:
	if not DEMO:
		return
	if _demo_t0 == 0:
		_demo_t0 = Time.get_ticks_msec()
	var f := FileAccess.open("user://demo_funnel.txt", FileAccess.READ_WRITE)
	if f == null:
		f = FileAccess.open("user://demo_funnel.txt", FileAccess.WRITE)
	if f == null:
		return
	f.seek_end()
	f.store_line("[min %.1f] %s" % [(Time.get_ticks_msec() - _demo_t0) / 60000.0, event])
	f.close()


func set_ui_scale(v: float) -> void:
	ui_scale = clampf(v, 0.8, 1.6)
	ui_scale_changed.emit(ui_scale)
	save_settings()


func set_assist(on: bool) -> void:
	assist_on = on
	save_settings()


func rebind(action: String, physical_keycode: int, persist: bool = true) -> void:
	for act in REMAP_ACTIONS:
		if act == action:
			continue
		for ev in InputMap.action_get_events(act):
			if ev is InputEventKey and (ev as InputEventKey).physical_keycode == physical_keycode:
				toast("KEY IN USE · that key already answers to %s." % act.to_upper())
				return
	for ev in InputMap.action_get_events(action):
		if ev is InputEventKey:
			InputMap.action_erase_event(action, ev)
	var k := InputEventKey.new()
	k.physical_keycode = physical_keycode
	InputMap.action_add_event(action, k)
	if persist:
		save_settings()


func key_name(action: String) -> String:
	for ev in InputMap.action_get_events(action):
		if ev is InputEventKey:
			return OS.get_keycode_string((ev as InputEventKey).physical_keycode)
	return "?"


func set_captions(on: bool) -> void:
	captions_on = on
	save_settings()


func show_caption(text: String) -> void:
	if captions_on:
		caption.emit(tr(text))


func set_blackout(alpha: float) -> void:
	blackout_changed.emit(alpha)


func noise(pos: Vector3, loudness: float) -> void:
	noise_event.emit(pos, loudness)


func set_photo_safe(on: bool) -> void:
	photo_safe = on
	save_log()
	photo_changed.emit(on)
	toast("PHOTOSENSITIVITY-SAFE MODE · %s" % ("ON · bands and flicker suppressed" if on else "OFF"))


func start_finale() -> void:
	finale_started.emit(decision)


func mark_ending(name: String, lie: bool = false) -> void:
	premiere_live = false
	finale_done = true
	ending_reached = name
	ending_marked.emit(name)
	Achievements.on_ending(name)
	if lie:
		lie_pending = true
	save_log()


func gain_asset(id: String, display: String) -> void:
	if assets.has(id):
		return
	assets.append(id)
	save_log()
	toast("ASSET BANKED · %s (%d of 4)" % [display, assets.size()])
	if assets.size() == 4:
		toast("All four. The finale has everything it needs, when night falls.")


func mark_presigned() -> void:
	presigned_seen = true
	signatures.append({
		"station": "S4",
		"tape": current_tape,
		"signed": "TOMORROW",
		"presigned": true,
	})
	save_log()
	log_signed.emit("S4", paper_for("S4"))


func add_wear(n: float) -> void:
	seance_wear += n
	save_log()


func add_pt(n: int) -> void:
	pt += n
	save_log()


func set_night(on: bool) -> void:
	is_night = on
	if not on:
		day += 1
		current_tape = mini(day, 5)
		toast("MORNING · Day %d · Tape %d. The building pretends nothing happened." % [day, current_tape])
		if day >= 3 and not run_complete:
			run_complete = true
			toast("PROTOTYPE COMPLETE · the loop is proven. The rest is production.")
	else:
		toast("NIGHT · the building belongs to the schedule.")
	save_log()
	night_changed.emit(on)


func strike(player: Node3D) -> void:
	if in_retake:
		return
	in_retake = true
	strikes += 1
	var take := strikes
	var lost := ""
	if items_lost < ITEM_ORDER.size():
		lost = ITEM_ORDER[items_lost]
		items_lost += 1
	var full := strikes >= 4 or mode == Mode.ONE_TAKE
	if full:
		strikes = 0
		save_log()
		sheet_changed.emit(strikes)
		run_ended.emit(take)
		return
	daily_seq += 1
	dailies.append({"id": daily_seq, "take": take})
	daily_added.emit(daily_seq, take)
	save_log()
	sheet_changed.emit(strikes)
	captured.emit(take, full, lost, respawn_point())
	if player:
		pass  ## repositioning happens inside the retake presentation


func set_tbc(on: bool) -> void:
	tbc_enabled = on
	tbc_changed.emit(on)


func save_log() -> void:
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f:
		var data := _save_dict()
		if DEMO:
			for k in ["decision", "assets", "leland_answers", "lockdown_done",
				"finale_done", "ending_reached", "lie_pending", "seance_wear",
				"has_fire_tape", "fire_tape_watched", "dock_done", "crate_opened",
				"presigned_seen", "cascade_done", "casualties"]:
				data.erase(k)
		f.store_string(JSON.stringify(data, "\t"))
		f.close()


func _save_dict() -> Dictionary:
	return ({
			"version": SAVE_VERSION,
			"mode": mode,
			"tbc": tbc_enabled,
			"tape": current_tape,
			"paper": paper,
			"signatures": signatures,
			"captures": captures,
			"strikes": strikes,
			"items_lost": items_lost,
			"day": day,
			"keys": keys,
			"pt": pt,
			"dailies": dailies,
			"daily_seq": daily_seq,
			"carried_id": carried_id,
			"carried_take": carried_take,
			"film_watched": film_watched,
			"signals_known": signals_known,
			"screening_done": screening_done,
			"run_complete": run_complete,
			"has_fire_tape": has_fire_tape,
			"fire_tape_watched": fire_tape_watched,
			"seance_wear": seance_wear,
			"leland_answers": leland_answers,
			"presigned_seen": presigned_seen,
			"dock_done": dock_done,
			"assets": assets,
			"decision": decision,
			"lockdown_done": lockdown_done,
			"finale_done": finale_done,
			"ending_reached": ending_reached,
			"lie_pending": lie_pending,
			"vess_insight": vess_insight,
			"vess_credited": vess_credited,
			"ng_relic": ng_relic,
			"crate_opened": crate_opened,
			"night_tripped": night_tripped,
			"cov_monitor": cov_monitor,
			"cov_move": cov_move,
			"cov_still": cov_still,
			"photo_safe": photo_safe,
			"cascade_done": cascade_done,
			"read_props": read_props,
			"af_active": af_active,
			"af_taught": af_taught,
			"casualties": casualties,
			"merle_offered": merle_offered,
			"signoff_completed": signoff_completed,
			"row_casualties": row_casualties,
			"h2_pending": h2_pending,
			"deadroom_seen": deadroom_seen,
			"rejected_seen": rejected_seen,
			"glimpse_seen": glimpse_seen,
			"merle_1974": merle_1974,
			"fire_unsealed": fire_unsealed,
	})


func load_log() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if f == null:
		return
	var data: Variant = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		return
	mode = int(data.get("mode", Mode.LATE_NIGHT))
	tbc_enabled = bool(data.get("tbc", false))
	current_tape = int(data.get("tape", 1))
	var p: Variant = data.get("paper", {})
	if typeof(p) == TYPE_DICTIONARY:
		for k in p.keys():
			paper[k] = int(p[k])
	var sigs: Variant = data.get("signatures", [])
	if typeof(sigs) == TYPE_ARRAY:
		signatures = sigs
	var caps: Variant = data.get("captures", [])
	if typeof(caps) == TYPE_ARRAY:
		captures = caps
	strikes = int(data.get("strikes", 0))
	items_lost = int(data.get("items_lost", 0))
	day = int(data.get("day", 1))
	var ks: Variant = data.get("keys", [])
	if typeof(ks) == TYPE_ARRAY:
		keys = ks
	pt = int(data.get("pt", 0))
	var dl: Variant = data.get("dailies", [])
	if typeof(dl) == TYPE_ARRAY:
		dailies = dl
	daily_seq = int(data.get("daily_seq", 0))
	carried_id = int(data.get("carried_id", -1))
	carried_take = int(data.get("carried_take", 0))
	film_watched = bool(data.get("film_watched", false))
	var sk: Variant = data.get("signals_known", [])
	if typeof(sk) == TYPE_ARRAY:
		signals_known = sk
	screening_done = bool(data.get("screening_done", false))
	run_complete = bool(data.get("run_complete", false))
	has_fire_tape = bool(data.get("has_fire_tape", false))
	fire_tape_watched = bool(data.get("fire_tape_watched", false))
	seance_wear = float(data.get("seance_wear", 0.0))
	var la: Variant = data.get("leland_answers", [])
	if typeof(la) == TYPE_ARRAY:
		leland_answers = la
	presigned_seen = bool(data.get("presigned_seen", false))
	dock_done = bool(data.get("dock_done", false))
	var av: Variant = data.get("assets", [])
	if typeof(av) == TYPE_ARRAY:
		assets = av
	decision = str(data.get("decision", ""))
	lockdown_done = bool(data.get("lockdown_done", false))
	finale_done = bool(data.get("finale_done", false))
	ending_reached = str(data.get("ending_reached", ""))
	lie_pending = bool(data.get("lie_pending", false))
	vess_insight = bool(data.get("vess_insight", false))
	vess_credited = bool(data.get("vess_credited", false))
	ng_relic = str(data.get("ng_relic", ""))
	crate_opened = bool(data.get("crate_opened", false))
	night_tripped = bool(data.get("night_tripped", false))
	cov_monitor = float(data.get("cov_monitor", 0.0))
	cov_move = float(data.get("cov_move", 0.0))
	cov_still = float(data.get("cov_still", 0.0))
	photo_safe = bool(data.get("photo_safe", false))
	cascade_done = bool(data.get("cascade_done", false))
	af_active = bool(data.get("af_active", false))
	af_taught = bool(data.get("af_taught", false))
	var cz: Variant = data.get("casualties", [])
	if typeof(cz) == TYPE_ARRAY:
		casualties = cz
	merle_offered = bool(data.get("merle_offered", false))
	signoff_completed = bool(data.get("signoff_completed", false))
	row_casualties = int(data.get("row_casualties", 0))
	h2_pending = bool(data.get("h2_pending", false))
	deadroom_seen = bool(data.get("deadroom_seen", false))
	var rp: Variant = data.get("read_props", [])
	if typeof(rp) == TYPE_ARRAY:
		read_props = rp
	rejected_seen = bool(data.get("rejected_seen", false))
	glimpse_seen = bool(data.get("glimpse_seen", false))
	merle_1974 = bool(data.get("merle_1974", false))
	fire_unsealed = bool(data.get("fire_unsealed", false))
	var v := int(data.get("version", 1))
	if v < SAVE_VERSION:
		save_log()
		call_deferred("_announce_migration", v)
	elif v > SAVE_VERSION:
		call_deferred("_announce_newer", v)


func _signed_station(id: String) -> bool:
	for sig in signatures:
		if str(sig.get("station", "")) == id:
			return true
	return false


func objective_text() -> String:
	if DEMO and captures.size() > 0:
		return "TAPE 1 · captured. Thank you for careful hands."
	if finale_done:
		return "ENDING REACHED: %s · thank you for watching · NEW GAME threads a fresh reel" % ending_reached
	if decision != "":
		return "ENTRY STANDS: %s · sleep to begin the premiere" % decision
	if run_complete and day >= 3:
		return "DAY %d · the ledger waits: AUTHENTICATE · DESTROY · PERFORM" % day
	if is_night:
		if dailies.size() > 0 or carried_id >= 0:
			return "NIGHT · optional: burn your dailies (library to climate room) · sleep when ready"
		return "NIGHT · the schedule owns the halls · sleep when ready"
	if day == 1:
		if not _signed_station("S1"):
			return "DAY 1 · sign the log at S1, the library landing"
		if not screening_done:
			return "DAY 1 · run the mini-screening at the rec room projector"
		if captures.size() == 0:
			return "DAY 1 · capture Tape 1 at the bench · it runs real time"
		return "DAY 1 · end the day at Rita's bed"
	if day >= 3:
		return "DAY %d · gather the four assets · the ledger ripens" % day
	return "DAY %d · the compound is yours: keys, signals, the sheet, the dark" % day


func reset_new_game() -> void:
	demo_mark("started")
	var relic := ""
	if finale_done and items_lost > 0:
		relic = ITEM_ORDER[mini(items_lost, ITEM_ORDER.size()) - 1]
	current_tape = 1
	paper = {"S1": 3, "S5": 3} if DEMO else {"S1": 3, "S2": 3, "S3": 3, "S4": 3, "S5": 3}
	signatures = []
	captures = []
	strikes = 0
	items_lost = 0
	day = 1
	is_night = false
	in_retake = false
	keys = []
	pt = 0
	dailies = []
	daily_seq = 0
	carried_id = -1
	carried_take = 0
	film_watched = false
	signals_known = []
	screening_done = false
	run_complete = false
	has_fire_tape = false
	fire_tape_watched = false
	seance_wear = 0.0
	leland_answers = []
	presigned_seen = false
	dock_done = false
	assets = []
	decision = ""
	lockdown_done = false
	finale_done = false
	ending_reached = ""
	premiere_live = false
	vess_insight = false
	vess_credited = false
	ng_relic = relic
	crate_opened = false
	night_tripped = false
	cov_monitor = 0.0
	cov_move = 0.0
	cov_still = 0.0
	rejected_seen = false
	glimpse_seen = false
	merle_1974 = false
	fire_unsealed = false
	cascade_done = false
	cascade_active = false
	read_props = []
	casualties = []
	row_casualties = 0
	h2_pending = false
	harriet_slip = false
	merle_offered = false
	save_log()


func _announce_migration(from_v: int) -> void:
	notify.emit("LOG MIGRATED · format v%d to v%d. Nothing was lost." % [from_v, SAVE_VERSION])


func _announce_newer(found_v: int) -> void:
	notify.emit("LOG FROM A NEWER BUILD · v%d read by v%d. Proceed gently." % [found_v, SAVE_VERSION])
