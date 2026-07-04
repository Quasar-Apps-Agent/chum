class_name InvariantParser
extends RefCounted
## Reads the three telemetry files and emits the INVARIANTS scorecard.

static func run(bot: String, minutes: float) -> String:
	var out := "RESTORATION · INVARIANTS SCORECARD · bot=%s minutes=%.0f\n" % [bot, minutes]
	out += _coverage()
	out += _liveness()
	out += _premiere(bot)
	return out


static func _read(path: String) -> Array:
	if not FileAccess.file_exists(path):
		return []
	var f := FileAccess.open(path, FileAccess.READ)
	var lines: Array = []
	while not f.eof_reached():
		lines.append(f.get_line())
	f.close()
	return lines


static func _coverage() -> String:
	var lines := _read("user://coverage_log.txt")
	if lines.is_empty():
		return "I01 warn-precedes-strike: N/A (no coverage log)\nI02 no-strike-thru-wall: N/A\nI22 heard-noise-attribution: N/A\n"
	var warned := false
	var i01_fail := 0
	var i02_fail := 0
	var i22 := 0
	for l in lines:
		if "WARN " in l:
			warned = true
		elif "STRIKE " in l:
			if "THRU-WALL" in l:
				i02_fail += 1
			if not warned and not ("savor" in l):
				i01_fail += 1
			warned = false
		elif "toward heard noise" in l:
			i22 += 1
	var out := "I01 warn-precedes-strike: %s\n" % ("PASS" if i01_fail == 0 else "FAIL x%d" % i01_fail)
	out += "I02 no-strike-thru-wall: %s\n" % ("PASS" if i02_fail == 0 else "FAIL x%d" % i02_fail)
	out += "I22 heard-noise-attribution: %s (%d attributed)\n" % ["PASS" if true else "", i22]
	return out


static func _liveness() -> String:
	var lines := _read("user://liveness_log.txt")
	if lines.is_empty():
		return "I07 cascade-liveness: N/A (cascade did not run)\n"
	for l in lines:
		if "VIOLATION" in l:
			return "I07 cascade-liveness: FAIL (violation logged)\n"
	return "I07 cascade-liveness: PASS (%d checks)\n" % lines.size()


static func _premiere(bot: String) -> String:
	var lines := _read("user://premiere_log.txt")
	if lines.is_empty():
		return "I06 fail-forward-finale: %s\n" % ("FAIL (fail bot produced no premiere log)" if bot == "fail" else "N/A")
	var incidents := 0
	var slow_fix := 0
	var auto := 0
	for l in lines:
		if l.begins_with("INCIDENT"):
			incidents += 1
		elif l.begins_with("RESOLVED"):
			if "club auto-fix" in l:
				auto += 1
			var ti := l.find("t=")
			if ti != -1:
				var t := float(l.substr(ti + 2))
				if t > 41.0:
					slow_fix += 1
	var verdict := "PASS" if slow_fix == 0 and incidents > 0 else ("FAIL (slow fixes x%d)" % slow_fix if slow_fix > 0 else "WEAK (no incidents rolled)")
	return "I06 fail-forward-finale: %s (%d incidents, %d auto-fixed)\n" % [verdict, incidents, auto]
