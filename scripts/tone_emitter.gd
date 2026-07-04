class_name ToneEmitter
extends Node3D
## Procedural room tone: two sines and optional noise through a generator
## stream. Placeholder voices for the hum, the coil, and the segments.

@export var freq_a := 55.0
@export var freq_b := 110.0
@export var noise := 0.0
@export var volume_db := -12.0
@export var reach := 20.0

var _player: AudioStreamPlayer3D
var _pb: AudioStreamGeneratorPlayback
var _phase_a := 0.0
var _phase_b := 0.0
var _active := true

const RATE := 22050.0


func _ready() -> void:
	_player = AudioStreamPlayer3D.new()
	var gen := AudioStreamGenerator.new()
	gen.mix_rate = RATE
	gen.buffer_length = 0.15
	_player.stream = gen
	_player.volume_db = volume_db
	_player.max_distance = reach
	add_child(_player)
	_start()


func _start() -> void:
	_player.play()
	_pb = _player.get_stream_playback()


func set_active(on: bool) -> void:
	_active = on
	if not on and _player.playing:
		_player.stop()
		_pb = null
	elif on and not _player.playing:
		_start()


func _process(_delta: float) -> void:
	if not _active or _pb == null:
		return
	var frames := _pb.get_frames_available()
	for i in frames:
		var v := sin(_phase_a) * 0.5 + sin(_phase_b) * 0.28
		if noise > 0.0:
			v += (randf() * 2.0 - 1.0) * noise
		_phase_a += TAU * freq_a / RATE
		_phase_b += TAU * freq_b / RATE
		_pb.push_frame(Vector2(v, v) * 0.4)
	_phase_a = fmod(_phase_a, TAU)
	_phase_b = fmod(_phase_b, TAU)
