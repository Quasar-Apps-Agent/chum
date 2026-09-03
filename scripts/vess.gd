class_name VessProp
extends Interactable
## Vess Keys, at the shrine wall. He sourced most of what the bench works on,
## and the ledger knows whether anyone ever wrote his name on it.

const LINES := [
	"VESS · 'I sourced most of what you'll be working on. I documented everything.'",
	"VESS · 'The provenance chains are, I mean. I can walk you through my system whenever.'",
	"VESS · 'Some tapes shouldn't exist. But they do. And I find them.'",
	"VESS · the label maker clicks in his pocket, twice, like a habit praying.",
]

var _li := 0


func _ready() -> void:
	add_child(CharacterKit.vess())
	var col := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.3
	shape.height = 1.7
	col.shape = shape
	col.position = Vector3(0, 0.85, 0)
	add_child(col)
	var tag := Label3D.new()
	tag.text = "VESS"
	tag.font_size = 24
	tag.position = Vector3(0, 1.95, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.85, 0.93, 0.77)
	add_child(tag)


func _process(_delta: float) -> void:
	if GameState.is_dead("VESS") and visible:
		visible = false


func get_prompt() -> String:
	return "VESS · at the shrine, cataloguing (E)"


func interact(_player: Node3D) -> void:
	if GameState.is_dead("VESS"):
		return
	GameState.toast(LINES[_li])
	_li = (_li + 1) % LINES.size()
