class_name OptionsPanel
extends Control

var first_run := false

var _awaiting := ""
var _remap_btns: Dictionary = {}
## The booth: master volume, mouse feel, the window, and the two access
## switches. Settings live in user://settings.cfg, apart from the log,
## so NEW GAME never touches them.


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.65)
	dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var panel := PanelContainer.new()
	panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	panel.custom_minimum_size = Vector2(520, 0)
	add_child(panel)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 14)
	panel.add_child(box)
	if first_run:
		GameState.save_settings()
	var title := Label.new()
	title.text = tr("OPTIONS · THE BOOTH")
	title.add_theme_color_override("font_color", Color(0.85, 0.93, 0.77))
	title.add_theme_font_size_override("font_size", 22)
	box.add_child(title)
	if first_run:
		var intro := Label.new()
		intro.text = tr("BEFORE THE SHOW · set your hands and eyes. O reopens this anytime.")
		intro.add_theme_color_override("font_color", Color(0.89, 0.64, 0.24))
		intro.add_theme_font_size_override("font_size", 14)
		box.add_child(intro)

	var vol := _slider_row(box, tr("MASTER VOLUME"),
		db_to_linear(AudioServer.get_bus_volume_db(0)), 0.0, 1.0)
	vol.value_changed.connect(func(v: float) -> void:
		AudioServer.set_bus_volume_db(0, linear_to_db(maxf(v, 0.001)))
		GameState.save_settings()
	)
	var sens := _slider_row(box, tr("MOUSE SENSITIVITY"), GameState.mouse_sens, 0.2, 3.0)
	sens.value_changed.connect(func(v: float) -> void:
		GameState.mouse_sens = v
		GameState.save_settings()
	)
	_check_row(box, tr("FULLSCREEN"),
		DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN,
		func(on: bool) -> void:
			DisplayServer.window_set_mode(
				DisplayServer.WINDOW_MODE_FULLSCREEN if on else DisplayServer.WINDOW_MODE_WINDOWED)
			GameState.save_settings()
	)
	_check_row(box, tr("TBC · steadier tape (T)"), GameState.tbc_enabled,
		func(on: bool) -> void: GameState.set_tbc(on))
	_check_row(box, tr("PHOTOSENSITIVITY-SAFE (P)"), GameState.photo_safe,
		func(on: bool) -> void: GameState.set_photo_safe(on))
	var scale := _slider_row(box, tr("UI TEXT SIZE"), GameState.ui_scale, 0.8, 1.6)
	scale.value_changed.connect(func(v: float) -> void: GameState.set_ui_scale(v))
	_check_row(box, tr("CAPTIONS · significant sounds"), GameState.captions_on,
		func(on: bool) -> void: GameState.set_captions(on))
	_check_row(box, tr("ASSIST · wider beats, slower clocks, hold E to be still"), GameState.assist_on,
		func(on: bool) -> void: GameState.set_assist(on))
	var rh := Label.new()
	rh.text = tr("REMAP · click, then press a key")
	rh.add_theme_color_override("font_color", Color(0.58, 0.65, 0.5))
	rh.add_theme_font_size_override("font_size", 14)
	box.add_child(rh)
	for act in GameState.REMAP_ACTIONS:
		_remap_row(box, act)

	var close := Button.new()
	_focusize(close)
	close.text = tr("CLOSE (O)")
	close.flat = true
	close.add_theme_font_size_override("font_size", 18)
	close.pressed.connect(queue_free)
	box.add_child(close)
	close.grab_focus()


func _slider_row(box: VBoxContainer, label_text: String, value: float, lo: float, hi: float) -> HSlider:
	var row := HBoxContainer.new()
	var l := Label.new()
	l.text = label_text
	l.custom_minimum_size = Vector2(240, 0)
	l.add_theme_color_override("font_color", Color(0.58, 0.65, 0.5))
	row.add_child(l)
	var s := HSlider.new()
	_focusize(s)
	s.min_value = lo
	s.max_value = hi
	s.step = 0.01
	s.value = value
	s.custom_minimum_size = Vector2(220, 0)
	row.add_child(s)
	box.add_child(row)
	return s


func _remap_row(box: VBoxContainer, act: String) -> void:
	var row := HBoxContainer.new()
	var l := Label.new()
	l.text = act.to_upper()
	l.custom_minimum_size = Vector2(240, 0)
	l.add_theme_color_override("font_color", Color(0.58, 0.65, 0.5))
	row.add_child(l)
	var b := Button.new()
	b.text = GameState.key_name(act)
	b.custom_minimum_size = Vector2(160, 0)
	_focusize(b)
	b.pressed.connect(func() -> void:
		_awaiting = act
		b.text = tr("PRESS A KEY")
	)
	_remap_btns[act] = b
	row.add_child(b)
	box.add_child(row)


func _unhandled_key_input(event: InputEvent) -> void:
	if _awaiting == "" or not (event is InputEventKey):
		return
	var k := event as InputEventKey
	if not k.pressed or k.echo:
		return
	GameState.rebind(_awaiting, k.physical_keycode)
	(_remap_btns[_awaiting] as Button).text = GameState.key_name(_awaiting)
	_awaiting = ""
	get_viewport().set_input_as_handled()


func _focusize(ctrl: Control) -> void:
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0, 0, 0, 0)
	sb.border_color = Color(0.85, 0.93, 0.77)
	sb.set_border_width_all(2)
	sb.set_corner_radius_all(2)
	ctrl.add_theme_stylebox_override("focus", sb)


func _check_row(box: VBoxContainer, label_text: String, value: bool, cb: Callable) -> void:
	var row := HBoxContainer.new()
	var l := Label.new()
	l.text = label_text
	l.custom_minimum_size = Vector2(240, 0)
	l.add_theme_color_override("font_color", Color(0.58, 0.65, 0.5))
	row.add_child(l)
	var c := CheckButton.new()
	_focusize(c)
	c.button_pressed = value
	c.toggled.connect(cb)
	row.add_child(c)
	box.add_child(row)


func _unhandled_input(event: InputEvent) -> void:
	if _awaiting != "":
		return
	if event.is_action_pressed("options") or event.is_action_pressed("ui_cancel"):
		queue_free()
		get_viewport().set_input_as_handled()
