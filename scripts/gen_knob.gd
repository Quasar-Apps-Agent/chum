class_name GenKnob
extends Interactable
## The bench's generation display knob. The picture obeys; the scope does not.

const NAMES := ["MASTER", "1ST DUB", "3RD GEN"]

var tv: BenchTV

var _g := 0


func get_prompt() -> String:
	return "GEN KNOB · showing %s · cycle (E)" % NAMES[_g]


func interact(_player: Node3D) -> void:
	Achievements.unlock("A03")
	_g = (_g + 1) % 3
	if tv:
		tv.set_generation(float(_g))
	GameState.toast("GEN SET · the picture agrees to look %s. The scope still reads MASTER." % NAMES[_g])
