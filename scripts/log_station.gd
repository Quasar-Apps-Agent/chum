class_name LogStation
extends Interactable
## A transmitter log clipboard: signing it saves. Paper is finite on Late Night.

@export var station_id: String = "S1"
@export var station_name: String = "LIBRARY LANDING"


func get_prompt() -> String:
	var remaining := GameState.paper_for(station_id)
	if remaining <= 0:
		return "%s · %s · no paper. walk to the next station." % [station_id, station_name]
	if remaining >= 99:
		return "%s · %s · sign the log (E) · unlimited paper" % [station_id, station_name]
	return "%s · %s · sign the log (E) · %d line(s) left" % [station_id, station_name, remaining]


func interact(_player: Node3D) -> void:
	if station_id == "S4" and GameState.day >= 2 and not GameState.presigned_seen:
		_presigned()
		return
	GameState.sign_log(station_id)


func _presigned() -> void:
	GameState.toast("The next line is not blank.")
	await get_tree().create_timer(1.6).timeout
	GameState.toast("Your handwriting. Tomorrow's date.")
	await get_tree().create_timer(1.8).timeout
	GameState.toast("You check the loops of the R the way you check a stranger's teeth. They are yours.")
	GameState.mark_presigned()
