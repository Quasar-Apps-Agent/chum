extends Control
## Minimal binder-toned HUD: interact prompt, save toast, TBC state.

@onready var prompt: Label = $Prompt
@onready var toast: Label = $Toast
@onready var tbc: Label = $TBC
@onready var capture: Label = $Capture
@onready var clock: Label = $Clock
@onready var sheet: Label = $Sheet
@onready var binder: Label = $Binder
@onready var retake: Control = $Retake
@onready var r1: Label = $Retake/Line1
@onready var r2: Label = $Retake/Line2
@onready var objective: Label = $Objective

var _player: CharacterBody3D
var _toast_t := 0.0


func _ready() -> void:
	_player = get_tree().get_first_node_in_group("player")
	GameState.log_signed.connect(_on_signed)
	GameState.log_refused.connect(_on_refused)
	GameState.tbc_changed.connect(_on_tbc)
	GameState.notify.connect(_on_notify)
	GameState.capture_status.connect(_on_capture)
	GameState.sheet_changed.connect(_on_sheet)
	GameState.captured.connect(_on_captured)
	GameState.run_ended.connect(_on_run_ended)
	GameState.finale_started.connect(_on_finale)
	GameState.demo_ended.connect(_on_demo_end)
	GameState.ui_scale_changed.connect(func(_v: float) -> void: _apply_text_prefs())
	GameState.caption.connect(_on_caption)
	GameState.pause_requested.connect(_toggle_pause)
	process_mode = Node.PROCESS_MODE_ALWAYS
	_caption = Label.new()
	_caption.add_theme_color_override("font_color", Color(0.85, 0.93, 0.77))
	_caption.add_theme_font_size_override("font_size", 18)
	_caption.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_RIGHT)
	_caption.offset_left = -420.0
	_caption.offset_top = -64.0
	_caption.offset_right = -18.0
	_caption.offset_bottom = -30.0
	_caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_caption.modulate.a = 0.0
	add_child(_caption)
	_apply_text_prefs()
	add_child(MapView.new())
	_blackout = ColorRect.new()
	_blackout.color = Color(0, 0, 0, 0)
	_blackout.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_blackout.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_blackout)
	move_child(_blackout, 0)
	GameState.blackout_changed.connect(_on_blackout)
	_on_sheet(GameState.strikes)
	_on_tbc(GameState.tbc_enabled)


var _binder_page := 0


var _blackout: ColorRect


func _on_blackout(alpha: float) -> void:
	var tw := create_tween()
	tw.tween_property(_blackout, "color:a", alpha, 1.2)


var _options: OptionsPanel
var _caption: Label
var _pause: Control


func _toggle_pause() -> void:
	var t := get_tree()
	if t.paused:
		t.paused = false
		AudioServer.set_bus_mute(0, false)
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		if _pause and is_instance_valid(_pause):
			_pause.queue_free()
		return
	var player := t.get_first_node_in_group("player")
	if player and player.locked:
		return
	t.paused = true
	AudioServer.set_bus_mute(0, true)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_pause = Control.new()
	_pause.process_mode = Node.PROCESS_MODE_ALWAYS
	_pause.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.7)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_pause.add_child(dim)
	var box := VBoxContainer.new()
	box.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	box.add_theme_constant_override("separation", 12)
	_pause.add_child(box)
	var h := Label.new()
	h.text = tr("INTERMISSION · WGLD holds its breath")
	h.add_theme_color_override("font_color", Color(0.85, 0.93, 0.77))
	h.add_theme_font_size_override("font_size", 20)
	box.add_child(h)
	for pair in [[tr("RESUME"), func() -> void: _toggle_pause()],
		[tr("THE BOOTH"), func() -> void:
			var b := OptionsPanel.new()
			b.process_mode = Node.PROCESS_MODE_ALWAYS
			_pause.add_child(b)],
		[tr("RETURN TO TITLE · progress holds at your last signature"), func() -> void:
			get_tree().paused = false
			AudioServer.set_bus_mute(0, false)
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
			get_tree().change_scene_to_file("res://scenes/title.tscn")]]:
		var btn := Button.new()
		btn.text = pair[0]
		btn.flat = true
		btn.add_theme_font_size_override("font_size", 16)
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(0, 0, 0, 0)
		sb.border_color = Color(0.85, 0.93, 0.77)
		sb.set_border_width_all(2)
		sb.set_corner_radius_all(2)
		btn.add_theme_stylebox_override("focus", sb)
		btn.pressed.connect(pair[1])
		box.add_child(btn)
	add_child(_pause)
	(box.get_child(1) as Button).grab_focus()
var _base_sizes: Dictionary = {}


func _apply_text_prefs() -> void:
	_walk_labels(self)


func _walk_labels(node: Node) -> void:
	for c in node.get_children():
		if c is Label:
			var l := c as Label
			if not _base_sizes.has(l):
				var sz := l.get_theme_font_size("font_size")
				_base_sizes[l] = sz if sz > 0 else 16
			l.add_theme_font_size_override("font_size", int(_base_sizes[l] * GameState.ui_scale))
			l.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.85))
			l.add_theme_constant_override("outline_size", 6)
		_walk_labels(c)


func _on_caption(text: String) -> void:
	_caption.text = text
	if not _base_sizes.has(_caption):
		_walk_labels(self)
	var tw := create_tween()
	_caption.modulate.a = 1.0
	tw.tween_interval(1.4)
	tw.tween_property(_caption, "modulate:a", 0.0, 0.6)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel") and get_tree().paused:
		_toggle_pause()
		get_viewport().set_input_as_handled()
		return
	if event.is_action_pressed("options"):
		if _options and is_instance_valid(_options):
			_options.queue_free()
		else:
			_options = OptionsPanel.new()
			add_child(_options)
		return
	if event.is_action_pressed("photo_safe"):
		GameState.set_photo_safe(not GameState.photo_safe)
		return
	if event.is_action_pressed("ledger"):
		_binder_page = (_binder_page + 1) % 3
		binder.visible = _binder_page != 0
		if _binder_page == 1:
			_fill_binder()
		elif _binder_page == 2:
			_fill_form()
	if _binder_page == 2 and event is InputEventKey and event.pressed and not event.echo:
		var k := (event as InputEventKey).physical_keycode
		if k == 49:
			GameState.set_mode(GameState.Mode.MATINEE)
			_fill_form()
		elif k == 50:
			GameState.set_mode(GameState.Mode.LATE_NIGHT)
			_fill_form()
		elif k == 51:
			GameState.set_mode(GameState.Mode.ONE_TAKE)
			_fill_form()


func _fill_form() -> void:
	var names := ["MATINEE", "LATE NIGHT", "ONE TAKE"]
	binder.text = "\n".join([
		"THE BINDER · PRESENTATION FORM · TAB closes",
		"",
		"MODE · press 1 / 2 / 3",
		"  1 MATINEE · unlimited paper, gentler sheet",
		"  2 LATE NIGHT · three lines per station, four sheet lines",
		"  3 ONE TAKE · any capture is final",
		"  current: %s" % names[GameState.mode],
		"",
		"TBC · %s · toggle with T anywhere" % ("ON" if GameState.tbc_enabled else "OFF"),
		"",
		"CONTROLS · WASD move · E interact · SPACE respond · Q improvise",
	])


func _fill_binder() -> void:
	var lines := [
		"THE BINDER · TAB closes",
		"",
		"MODE: LATE NIGHT · TBC: %s" % ("ON" if GameState.tbc_enabled else "OFF"),
		"SIGNATURES ON FILE: %d" % GameState.signatures.size(),
		"CASTING SHEET: %d of 4 guest lines" % GameState.strikes,
		"PRODUCER TRACK: %d" % GameState.pt,
		"KEYS: %s" % (", ".join(GameState.keys) if GameState.keys.size() > 0 else "none"),
		"DAILIES IN THE STACKS: %d · carrying: %s" % [GameState.dailies.size(), ("TAKE %d" % GameState.carried_take) if GameState.carried_id >= 0 else "nothing"],
		"COVERAGE READS YOU AS: %s (this session)" % GameState.coverage_label,
		"LELAND · wear %.0f%% · answers %d of 5" % [GameState.seance_wear, GameState.leland_answers.size()],
		"PHOTOSAFE: %s (P)" % ("ON" if GameState.photo_safe else "OFF"),
		"VESS · %s" % ("credited in the margin" if GameState.vess_credited else ("insight held, uncredited" if GameState.vess_insight else "his door is ajar")),
		"SIGNALS KNOWN: %d%s" % [GameState.signals_known.size(), (" · " + ", ".join(GameState.signals_known)) if GameState.signals_known.size() > 0 else ""],
		"",
		"CAPTURES:",
	]
	if GameState.captures.is_empty():
		lines.append("  none yet. the bench is patient.")
	else:
		for c in GameState.captures.slice(maxi(0, GameState.captures.size() - 5)):
			lines.append("  " + str(c.get("name", "?")))
	binder.text = "\n".join(lines)


func _on_captured(take: int, sheet_full: bool, lost_item: String, respawn: Vector3) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.locked = true
	retake.visible = true
	r1.text = "◼ CAPTURED"
	r2.text = ""
	await _wait(0.7)
	r1.text = "THE GLADHOUSE"
	r2.text = "SCENE 4 · TAKE %d" % take
	await _wait(0.9)
	r1.text = "◀◀ REWINDING"
	for i in range(14):
		r2.text = "TC 00:03:%02d:00" % maxi(0, 13 - i)
		await _wait(0.06)
	if player:
		player.global_position = respawn
		player.velocity = Vector3.ZERO
	if lost_item != "":
		r1.text = "ITEM MISSING"
		r2.text = "your %s is gone from the dresser. it will be in the footage." % lost_item.to_lower()
		await _wait(1.2)
	if sheet_full:
		r1.text = "THE SHEET IS FULL"
		r2.text = "the rewind would not stop. (prototype: the sheet resets.)"
		await _wait(1.4)
	else:
		r1.text = "PRESENTATION KEPT"
		r2.text = "resume from your last signature."
		await _wait(0.9)
	retake.visible = false
	if player:
		player.locked = false
	GameState.in_retake = false


func _on_run_ended(take: int) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.locked = true
	retake.visible = true
	r1.text = "◼ CAPTURED"
	r2.text = "TAKE %d" % take
	await _wait(1.0)
	r1.text = "◀◀ REWINDING"
	for i in range(10):
		r2.text = "TC 00:03:%02d:00" % maxi(0, 9 - i)
		await _wait(0.07)
	r1.text = "THE REWIND DOES NOT STOP"
	r2.text = ""
	await _wait(1.4)
	r1.text = "NEXT WEEK'S EPISODE"
	r2.text = "STARRING RITA IVORI"
	await _wait(2.2)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().change_scene_to_file("res://scenes/title.tscn")


func _say(a: String, b: String, t: float) -> void:
	r1.text = GameState.glyphs(tr(a))
	r2.text = GameState.glyphs(tr(b))
	await _wait(t)


func _await_choice(a: String, b: String) -> String:
	while true:
		await get_tree().process_frame
		if Input.is_action_just_pressed(a):
			return a
		if b != "" and Input.is_action_just_pressed(b):
			return b
	return a


func _roll_credits(label: String) -> void:
	await _say("ENDING · " + label, "RESTORATION", 2.6)
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().change_scene_to_file("res://scenes/credits.tscn")


func _on_demo_end() -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.locked = true
	await _wait(1.6)
	retake.visible = true
	await _say("THE RESPOND SIGN LIGHTS.", "Alone. Unasked.", 2.0)
	GameState.demo_mark("card")
	r1.text = "TAPE 1 OF 5. THE PROGRAM CONTINUES."
	r2.text = "Your ledger, your signatures, and your paper carry into the full game. WISHLIST RESTORATION."
	await _wait(3.0)
	r2.text = r2.text + "  ·  The 58 Club thanks you for careful hands. (any key)"
	while true:
		await get_tree().process_frame
		if Input.is_action_just_pressed("respond") or Input.is_action_just_pressed("interact") or Input.is_action_just_pressed("ui_accept"):
			break
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().change_scene_to_file("res://scenes/title.tscn")


func _on_finale(decision: String) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.locked = true
	retake.visible = true
	match decision:
		"DESTROY":
			await _end_burn()
		"AUTHENTICATE":
			await _end_producer()
		_:
			await _end_perform()


func _end_burn() -> void:
	await _say("You work through the night.", "Reel by reel. Entry by entry.", 2.6)
	await _say("Your hands know no other way to touch tape.", "", 2.2)
	await _say("MERLE, in the doorway.", "No anger anywhere on her, which is the worst available outcome.", 2.8)
	await _say("'Oh, honey. We have copies.'", "'Everyone has copies. That's what love is now.'", 3.0)
	await _say("'There's cobbler.'", "", 2.4)
	await _say("EPILOGUE", "The ledger, weeks later, a new hand: M. OYELARAN, INCOMING CONSERVATOR.", 3.0)
	GameState.mark_ending("THE BURN")
	await _roll_credits("3 · THE BURN")


func _end_producer() -> void:
	await _say("The premiere goes out clean.", "The club weeps with joy, in rows.", 2.6)
	await _say("In resolution the puppet was never built to survive,", "it leans to the lens.", 2.6)
	await _say("CHUM · 'There she is. Our new friend.'", "'Say it with me, everyone.'", 2.8)
	await _say("'WELCOME HOME.'", "", 2.6)
	await _say("MERLE · 'Now Merle is just going to watch it again.'", "", 2.6)
	GameState.mark_ending("THE NEW PRODUCER", true)
	await _roll_credits("2 · THE NEW PRODUCER")


func _end_perform() -> void:
	## hand the floor to the playable live production
	retake.visible = false
	var player := get_tree().get_first_node_in_group("player")
	if player:
		player.locked = false
	var outcome := "line"
	var lp := get_tree().get_first_node_in_group("live_production")
	if lp:
		outcome = await lp.run()
	if player:
		player.locked = true
	retake.visible = true
	if outcome == "dead_air":
		await _end_dead_air()
		return
	Sfx.bell()
	await _say("Fifty years silent.", "The bell rings once, three feet behind camera position.", 2.8)
	r1.text = "CAMERA ONE"
	r2.text = "SPACE · deliver the line"
	var _p := await _await_choice("respond", "")
	await _say("'That's our show. That was always our show.'", "", 2.6)
	await _say("'There's no one at home anymore. The lights are off.'", "'The children grew up. You can stop looking for them.'", 3.2)
	await _say("'Say goodnight, Chum.'", "", 2.6)
	if GameState.leland_answers.size() >= 5 and GameState.seance_wear <= 70.0:
		await _say("On every screen at once, inside the frame he was cropped from,", "he steps to center and is allowed to be whole.", 3.0)
		await _say("LELAND · 'Goodnight, everyone.'", "'It's okay. Nobody's watching.'", 3.0)
		await _say("CHUM, small, the performance finally allowed to end:", "'Goodnight, Gladhouse.'", 2.8)
		await _say("The card. Then, for the first time in fifty years,", "dark that is only dark.", 3.0)
		await _say("Harriet's cup, rising since Tape 1,", "comes down.", 2.6)
		GameState.mark_ending("SIGN-OFF · LELAND CLOSES")
		await _roll_credits("1A · SIGN-OFF")
	else:
		await _say("Someone must close the house from inside.", "", 2.4)
		await _say("RITA · 'I'll close up.'", "'Goodnight, everyone.'", 2.8)
		await _say("The ledger's last line is in green ink, not hers:", "SHE CLOSED IT PROPERLY. FILE UNDER: SAINTS.", 3.2)
		GameState.mark_ending("SIGN-OFF · RITA CLOSES")
		await _roll_credits("1B · SIGN-OFF")


func _end_dead_air() -> void:
	await _say("You close the felt door from inside.", "Outside the format entirely.", 2.8)
	await _say("RITA, into the radio, to every set on every band:", "'This is WGLD, Channel fifty-eight, leaving the air.'", 3.0)
	await _say("'The show is over.'", "'You can put the toys away.'", 2.8)
	await _say("The erase loop propagates outward like weather.", "", 2.6)
	await _say("You watch the archive die, reel by reel,", "your hands folded, because there is nothing left for them to save.", 3.2)
	await _say("FINAL LEDGER LINE, steady:", "'Signed off.'", 2.8)
	GameState.mark_ending("DEAD AIR")
	await _roll_credits("4 · DEAD AIR")


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout


func _on_sheet(count: int) -> void:
	sheet.text = "SHEET · %d/4" % count


func _process(delta: float) -> void:
	if _player and _player.has_method("current_target"):
		var t: Interactable = _player.current_target()
		prompt.text = GameState.glyphs(tr(t.get_prompt())) if t else ""
	var prefix := "NIGHT · " if GameState.is_night else "DAY %d · " % GameState.day
	clock.text = prefix + Broadcast.phase_text()
	objective.text = GameState.objective_text()
	clock.modulate = Color(0.89, 0.64, 0.24) if Broadcast.on_air else Color(0.55, 0.78, 0.5)
	if _toast_t > 0.0:
		_toast_t -= delta
		if _toast_t <= 0.0:
			toast.text = ""


func _on_signed(station: String, remaining: int) -> void:
	toast.text = "SIGNED · %s · %s line(s) of paper left" % [station, str(remaining) if remaining < 99 else "unlimited"]
	_toast_t = 2.5


func _on_refused(station: String) -> void:
	toast.text = "%s · NO PAPER. The log does not forgive on Late Night." % station
	_toast_t = 2.5


func _on_notify(text: String) -> void:
	toast.text = text
	_toast_t = 3.0


func _on_capture(text: String) -> void:
	capture.text = text


func _on_tbc(on: bool) -> void:
	tbc.text = "TBC: %s  (T)" % ("ON" if on else "OFF")
