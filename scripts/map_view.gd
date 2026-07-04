class_name MapView
extends Control
## M: the facility map, drawn live from the room bible's own constants.
## Rooms, landmarks, and you: a moving dot with a facing tick.

const WB := preload("res://scripts/world_builder.gd")
const LANDMARKS := [
	["BENCH", Vector2(9.0, -18.0)],
	["LEDGER", Vector2(8.2, -16.2)],
	["DOCK", Vector2(-19.5, -38.0)],
	["TRANSMITTER", Vector2(16.75, -6.5)],
	["ENTRY", Vector2(0.0, 6.0)],
	["SET", Vector2(-15.5, -31.2)],
]

var _player: Node3D


func _ready() -> void:
	visible = false
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("map"):
		visible = not visible


func _process(_delta: float) -> void:
	if visible:
		queue_redraw()


func _draw() -> void:
	var rooms: Dictionary = WB.ROOMS
	if rooms.is_empty():
		return
	draw_rect(Rect2(Vector2.ZERO, size), Color(0.02, 0.018, 0.012, 0.92))
	var minx := INF
	var maxx := -INF
	var minz := INF
	var maxz := -INF
	for name in rooms:
		var r: Array = rooms[name]
		minx = minf(minx, r[0] - r[2] / 2.0)
		maxx = maxf(maxx, r[0] + r[2] / 2.0)
		minz = minf(minz, r[1] - r[3] / 2.0)
		maxz = maxf(maxz, r[1] + r[3] / 2.0)
	var s := minf(size.x * 0.86 / (maxx - minx), size.y * 0.86 / (maxz - minz))
	var off := Vector2((size.x - (maxx - minx) * s) / 2.0, (size.y - (maxz - minz) * s) / 2.0)
	var font := ThemeDB.fallback_font
	for name in rooms:
		var r: Array = rooms[name]
		var px := off.x + (r[0] - r[2] / 2.0 - minx) * s
		var py := off.y + (r[1] - r[3] / 2.0 - minz) * s
		var rect := Rect2(px, py, r[2] * s, r[3] * s)
		draw_rect(rect, Color(0.08, 0.09, 0.07, 0.9))
		draw_rect(rect, Color(0.35, 0.42, 0.32), false, 1.5)
		draw_string(font, rect.position + Vector2(4, 13), str(name), HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 6, 10, Color(0.5, 0.56, 0.46))
	for sp in GameState.map_points:
		var spp: Vector2 = Vector2(off.x + (sp[1].x - minx) * s, off.y + (sp[1].y - minz) * s)
		draw_circle(spp, 4.0, Color(0.55, 0.75, 0.55))
		draw_string(font, spp + Vector2(6, 4), str(sp[0]), HORIZONTAL_ALIGNMENT_LEFT, -1, 9, Color(0.55, 0.7, 0.55))
	for lm in LANDMARKS:
		var p: Vector2 = Vector2(off.x + (lm[1].x - minx) * s, off.y + (lm[1].y - minz) * s)
		draw_circle(p, 3.5, Color(0.89, 0.64, 0.24))
		draw_string(font, p + Vector2(6, 4), lm[0], HORIZONTAL_ALIGNMENT_LEFT, -1, 9, Color(0.72, 0.55, 0.26))
	if _player == null:
		_player = get_tree().get_first_node_in_group("player")
	if _player:
		var pp := Vector2(off.x + (_player.global_position.x - minx) * s, off.y + (_player.global_position.z - minz) * s)
		draw_circle(pp, 5.0, Color(0.85, 0.93, 0.77))
		var fwd3 := -_player.global_transform.basis.z
		var fwd := Vector2(fwd3.x, fwd3.z).normalized() * 11.0
		draw_line(pp, pp + fwd, Color(0.85, 0.93, 0.77), 2.0)
	draw_string(font, Vector2(16, size.y - 14), "FACILITY MAP · %s to close · amber: landmarks · dot: you" % GameState.key_name("map").to_upper(), HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.58, 0.65, 0.5))
