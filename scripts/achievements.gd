extends Node
## Autoload: achievements per the design doc. Idempotent unlocks persist to
## user://achievements.cfg; nothing surfaces during play. The queue flushes
## at exactly two gates: the morning toast and the title screen. Disabled
## entirely under DEMO. The once-ever moment has no entry here, on purpose.

signal achievement_unlocked(id: String)  ## future GodotSteam bridge

const CFG := "user://achievements.cfg"

const TITLES := {
	"A01": "FIRST SIGNATURE", "A02": "CAREFUL HANDS", "A03": "THE SCOPE READS MASTER",
	"A04": "ON THE BEAT", "A05": "STILLNESS, HELD WHOLE", "A06": "MID-MOTION",
	"A07": "HOLD YOUR APPLAUSE", "A08": "YOU WERE NOT QUIET", "A09": "TOMORROW'S DATE",
	"A10": "THE ROWS KEEP THEIR ORDER", "A11": "PER V. CARDONA", "A12": "NO SEARCHER SINGS",
	"A13": "THE UNFINISHED LINE", "A14": "I'VE READ THE ENDING", "A15": "ORDER MATTERS",
	"A16": "THE LONG WAY AROUND", "A17": "INK", "A18": "NEXT WEEK'S EPISODE",
	"A19": "EMPTY DRAWER", "A20": "SEALED FOR BROADCAST", "A21": "THERE'S COBBLER",
	"A22": "WELCOME HOME", "A23": "FILE UNDER: SAINTS", "A24": "IT'S OKAY. NOBODY'S WATCHING.",
	"A25": "SIGNED OFF", "A26": "FULL ACCESSION",
}
const ENDING_MAP := {
	"THE BURN": "A21", "THE NEW PRODUCER": "A22",
	"SIGN-OFF · RITA CLOSES": "A23", "SIGN-OFF · LELAND CLOSES": "A24",
	"DEAD AIR": "A25",
}

var _unlocked: Dictionary = {}
var _shown: Dictionary = {}
var _poll_t := 0.0


func _ready() -> void:
	_load()
	GameState.log_signed.connect(func(_st: String, _p: int) -> void: unlock("A01"))
	GameState.run_ended.connect(func(_take: int) -> void: unlock("A18"))
	GameState.night_changed.connect(func(on: bool) -> void:
		if not on:
			flush_to_toasts()
	)


func unlock(id: String) -> void:
	if id == "" or GameState.DEMO or _unlocked.has(id) or not TITLES.has(id):
		return
	_unlocked[id] = true
	_save()
	achievement_unlocked.emit(id)


func on_ending(name: String) -> void:
	unlock(ENDING_MAP.get(name, ""))


func _process(delta: float) -> void:
	_poll_t += delta
	if _poll_t < 1.0:
		return
	_poll_t = 0.0
	if GameState.captures.size() > 0: unlock("A02")
	if GameState.signals_known.size() >= 7: unlock("A07")
	if GameState.presigned_seen: unlock("A09")
	if GameState.dock_done: unlock("A10")
	if GameState.vess_credited: unlock("A11")
	if GameState.merle_1974: unlock("A12")
	if GameState.fire_tape_watched: unlock("A13")
	if GameState.leland_answers.size() >= 5: unlock("A14")
	if GameState.cascade_done: unlock("A15")
	if GameState.has_key("QUIET ROOM"): unlock("A16")
	if GameState.decision != "": unlock("A17")
	if GameState.items_lost >= 7: unlock("A19")
	if GameState.lockdown_done: unlock("A20")
	if GameState.read_props.size() >= 10: unlock("A26")


func pending() -> Array:
	var out: Array = []
	for id in _unlocked:
		if not _shown.has(id):
			out.append(TITLES[id])
	return out


func flush_to_toasts() -> void:
	var p := pending()
	if p.is_empty():
		return
	if p.size() <= 2:
		for t in p:
			GameState.toast("FILED · " + t)
	else:
		GameState.toast("FILED · %d entries, %s among them." % [p.size(), p[0]])
	_mark_all_shown()


func flush_silent() -> Array:
	var p := pending()
	_mark_all_shown()
	return p


func _mark_all_shown() -> void:
	for id in _unlocked:
		_shown[id] = true
	_save()


func _load() -> void:
	var cfg := ConfigFile.new()
	if cfg.load(CFG) != OK:
		return
	for id in cfg.get_value("ach", "unlocked", []):
		_unlocked[id] = true
	for id in cfg.get_value("ach", "shown", []):
		_shown[id] = true


func _save() -> void:
	var cfg := ConfigFile.new()
	cfg.set_value("ach", "unlocked", _unlocked.keys())
	cfg.set_value("ach", "shown", _shown.keys())
	cfg.save(CFG)
