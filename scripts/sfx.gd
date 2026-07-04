extends Node
## Autoload: synthesized one-shots. The bell is two inharmonic partials and
## a long decay; fifty years of silence deserve a real strike.

var _bell: AudioStreamWAV
var _thunk: AudioStreamWAV
var _tick: AudioStreamWAV


func _ready() -> void:
	_bell = _synth(2.2, [[880.0, 0.55, 2.6], [1244.0, 0.3, 3.4], [2217.0, 0.12, 5.0]], 0.015)
	_thunk = _synth(0.16, [[85.0, 0.8, 14.0], [140.0, 0.25, 18.0]], 0.05)
	_tick = _synth(0.06, [[1600.0, 0.5, 60.0]], 0.0)


func bell() -> void:
	GameState.show_caption("[THE BELL RINGS · once]")
	_play(_bell, -6.0)


func tick() -> void:
	GameState.show_caption("[pen tick]")
	_play(_tick, -16.0)


func thunk(pos: Vector3) -> void:
	GameState.show_caption("[door]")
	var p := AudioStreamPlayer3D.new()
	p.stream = _thunk
	p.volume_db = -8.0
	p.max_distance = 14.0
	get_tree().current_scene.add_child(p)
	p.global_position = pos
	p.play()
	p.finished.connect(p.queue_free)


func _play(stream: AudioStreamWAV, db: float) -> void:
	var p := AudioStreamPlayer.new()
	p.stream = stream
	p.volume_db = db
	add_child(p)
	p.play()
	p.finished.connect(p.queue_free)


func _synth(dur: float, parts: Array, noise: float) -> AudioStreamWAV:
	var rate := 22050
	var n := int(dur * float(rate))
	var buf := PackedByteArray()
	buf.resize(n * 2)
	for i in n:
		var t := float(i) / float(rate)
		var v := 0.0
		for prt in parts:
			v += prt[1] * sin(TAU * prt[0] * t) * exp(-prt[2] * t)
		if noise > 0.0:
			v += noise * (randf() * 2.0 - 1.0) * exp(-8.0 * t)
		buf.encode_s16(i * 2, int(clampf(v, -1.0, 1.0) * 32000.0))
	var w := AudioStreamWAV.new()
	w.format = AudioStreamWAV.FORMAT_16_BITS
	w.mix_rate = rate
	w.stereo = false
	w.data = buf
	return w
