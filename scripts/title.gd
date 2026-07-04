extends Control
## The title screen: channel dark, the card, the menu.

@onready var new_btn: Button = $Menu/NewGame
@onready var cont_btn: Button = $Menu/Continue
@onready var quit_btn: Button = $Menu/Quit


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	cont_btn.disabled = not FileAccess.file_exists(GameState.SAVE_PATH)
	if GameState.lie_pending:
		new_btn.text = "NEW EPISODE"
		GameState.lie_pending = false
		GameState.save_log()
	if cont_btn.disabled:
		cont_btn.text = "CONTINUE · no log on file"
	new_btn.pressed.connect(_on_new)
	cont_btn.pressed.connect(_on_continue)
	($Menu/Options as Button).pressed.connect(func() -> void:
		add_child(OptionsPanel.new())
	)
	($Menu/Credits as Button).pressed.connect(func() -> void:
		get_tree().change_scene_to_file("res://scenes/credits.tscn")
	)
	quit_btn.pressed.connect(func() -> void: get_tree().quit())
	if GameState.DEMO:
		($Foot as Label).text = "TAPE 1 · FREE DEMO · the tower light stays on"
	var filed := Achievements.flush_silent()
	if not filed.is_empty():
		var stack := Label.new()
		stack.text = "FILED WHILE YOU WERE OUT:\n" + "\n".join(filed)
		stack.add_theme_color_override("font_color", Color(0.58, 0.65, 0.5))
		stack.add_theme_font_size_override("font_size", 14)
		stack.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_LEFT)
		stack.offset_left = 24.0
		stack.offset_top = -140.0
		stack.offset_right = 460.0
		add_child(stack)
	for c in $Menu.get_children():
		if c is Button:
			var sb := StyleBoxFlat.new()
			sb.bg_color = Color(0, 0, 0, 0)
			sb.border_color = Color(0.85, 0.93, 0.77)
			sb.set_border_width_all(2)
			sb.set_corner_radius_all(2)
			(c as Button).add_theme_stylebox_override("focus", sb)
	if not FileAccess.file_exists(GameState.SETTINGS_PATH):
		var booth := OptionsPanel.new()
		booth.first_run = true
		add_child(booth)
	new_btn.grab_focus()


func _on_new() -> void:
	GameState.reset_new_game()
	get_tree().change_scene_to_file("res://scenes/main.tscn")


func _on_continue() -> void:
	get_tree().change_scene_to_file("res://scenes/main.tscn")
