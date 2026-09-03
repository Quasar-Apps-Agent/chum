extends Control
## The sign-off crawl. Period cards, phosphor on black, silence held.
## Any key after a short grace skips to title.

const SPEED := 42.0

var _t := 0.0
var _crawl: VBoxContainer
var _done := false


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var bg := ColorRect.new()
	bg.color = Color(0.027, 0.027, 0.02)
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(bg)
	_crawl = VBoxContainer.new()
	_crawl.add_theme_constant_override("separation", 46)
	add_child(_crawl)
	var cards := [
		["RESTORATION", 30],
		["an accession of the 58 CLUB", 16],
		["written, designed, and built by\nCIEL ESSEL", 20],
		["with THE GLADHOUSE (1971 to 1977)\nappearing courtesy of the estate of A. CRAIK", 16],
		["MERLE ······ herself\nVESS ······ himself\nHARRIET ······ mid-motion\nTHE FLOOR MANAGER ······ uncredited, by request", 16],
		["and CHUM\nas himself", 20],
		["made with GODOT\ncaptured to tape at WGLD, channel 58", 14],
		["for everyone who was carried", 16],
		["WGLD signs off.", 20],
	]
	if GameState.ending_reached == "A ONE-WOMAN SHOW":
		cards[4] = ["MERLE ······ RITA IVORI\nVESS ······ RITA IVORI\nHARRIET ······ RITA IVORI\nTHE FLOOR MANAGER ······ RITA IVORI", 16]
		cards[5] = ["and CHUM\nas RITA IVORI", 20]
	if GameState.ending_reached != "":
		cards.insert(6, ["ENDING REACHED\n" + GameState.ending_reached, 14])
	for c in cards:
		var l := Label.new()
		l.text = c[0]
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.add_theme_color_override("font_color", Color(0.85, 0.93, 0.77))
		l.add_theme_font_size_override("font_size", c[1])
		_crawl.add_child(l)
	await get_tree().process_frame
	var vw := get_viewport_rect().size
	_crawl.position = Vector2(vw.x * 0.5 - _crawl.size.x * 0.5, vw.y + 20.0)


func _process(delta: float) -> void:
	_t += delta
	if _done:
		return
	_crawl.position.y -= SPEED * delta
	if _crawl.position.y < -_crawl.size.y - 40.0:
		_hold_and_exit()


func _unhandled_input(event: InputEvent) -> void:
	if _t > 1.5 and (event is InputEventKey or event is InputEventMouseButton) and event.pressed:
		_to_title()


func _hold_and_exit() -> void:
	_done = true
	var l := Label.new()
	l.text = "the tower light stays on"
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_color_override("font_color", Color(0.35, 0.42, 0.32))
	l.add_theme_font_size_override("font_size", 14)
	l.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	add_child(l)
	await get_tree().create_timer(3.0).timeout
	_to_title()


func _to_title() -> void:
	if is_queued_for_deletion():
		return
	get_tree().change_scene_to_file("res://scenes/title.tscn")
