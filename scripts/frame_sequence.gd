class_name FrameSequence
extends RefCounted
## The impossible reel as an image sequence: one procedurally built frame per
## index, deterministic per frame (seeded grain), cached as textures. This is
## the exact pipeline real footage drops into: swap the generator for a loader
## and nothing upstream changes.

const W := 320
const H := 240

var _cache: Dictionary = {}


func get_frame(idx: int, is_answer: bool) -> ImageTexture:
	var key := idx * 2 + (1 if is_answer else 0)
	if _cache.has(key):
		return _cache[key]
	var tex := ImageTexture.create_from_image(_build(idx, is_answer))
	_cache[key] = tex
	return tex


func _build(idx: int, is_answer: bool) -> Image:
	var img := Image.create(W, H, false, Image.FORMAT_RGB8)
	var rng := RandomNumberGenerator.new()
	rng.seed = idx * 7919 + 13
	## background with baked vignette, row by row
	for y in H:
		var v := 1.0 - 0.55 * pow(absf(float(y) / float(H) - 0.5) * 2.0, 2.0)
		var base := Color(0.16, 0.19, 0.15) if y < 150 else Color(0.24, 0.2, 0.11)
		img.fill_rect(Rect2i(0, y, W, 1), base * v)
	## the set: cubby wall and a doorway of darker dark
	img.fill_rect(Rect2i(30, 60, 60, 80), Color(0.11, 0.14, 0.1))
	img.fill_rect(Rect2i(200, 50, 40, 100), Color(0.06, 0.07, 0.06))
	## Leland, cropped by the frame's right edge
	var lx := 284 + (idx % 5) * 2
	if is_answer:
		lx -= 14
	img.fill_rect(Rect2i(lx, 118, 30, 92), Color(0.045, 0.045, 0.05))
	img.fill_rect(Rect2i(lx + 5, 100, 18, 20), Color(0.05, 0.05, 0.055))
	img.fill_rect(Rect2i(lx + 8, 96, 12, 6), Color(0.05, 0.05, 0.055))
	## answer frames carry a scratch: something happened here
	if is_answer:
		var sy := 40 + (idx * 3) % 160
		img.fill_rect(Rect2i(0, sy, W, 1), Color(0.55, 0.55, 0.5))
	## deterministic grain: the same frame is always the same frame
	for i in 2600:
		var x := rng.randi_range(0, W - 1)
		var y2 := rng.randi_range(0, H - 1)
		var c := img.get_pixel(x, y2)
		var d := rng.randf_range(-0.06, 0.06)
		img.set_pixel(x, y2, Color(c.r + d, c.g + d, c.b + d))
	## head-switch tear
	img.fill_rect(Rect2i(0, H - 5, W, 5), Color(0.03, 0.03, 0.03))
	return img
