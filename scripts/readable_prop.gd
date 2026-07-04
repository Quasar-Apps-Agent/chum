class_name ReadableProp
extends Interactable
## A found document, physically in the world, per the props packet.

@export var doc_id := "D00"
@export var label := "A DOCUMENT"
@export var needs_day := 1
@export var needs_dock := false

var lines: Array = []

var _running := false


func _process(_delta: float) -> void:
	visible = GameState.day >= needs_day and (not needs_dock or GameState.dock_done)


func get_prompt() -> String:
	if GameState.read_props.has(doc_id):
		return "%s · read (E again)" % label
	return "%s · read (E)" % label


func interact(_player: Node3D) -> void:
	if _running:
		return
	_run()


func _run() -> void:
	_running = true
	for entry in lines:
		GameState.toast(entry[0])
		await get_tree().create_timer(entry[1]).timeout
	GameState.mark_read(doc_id)
	_running = false
