class_name Harriet
extends Interactable
## Harriet Lund. She sways gently while the building is ON AIR, and freezes
## mid-motion for every break, resuming exactly where the cue left her.
## Her cup has been rising since Tape 1.

const LINES := [
	"And now. The tour continues.","'And now.'", "'But first.'", "'When we come back.'"]

var _t := 0.0
var _li := 0
var _slip_armed := false
var _h1_pending := false
var _doubled := false


func _process(_pd: float) -> void:
	if not GameState.is_dead("HARRIET"):
		return
	if GameState.cause_of("HARRIET").begins_with("H2"):
		if not _doubled:
			_splice_visual()
	else:
		visible = false


func _splice_visual() -> void:
	## the double: one whole Harriet, an inch to the left, both mouths
	_doubled = true
	var ghost := _rig.duplicate()
	ghost.position = _rig.position + Vector3(0.13, 0.0, 0.03)
	ghost.rotate_y(0.06)
	add_child(ghost)
var _cup: MeshInstance3D
var _rig: Node3D


func _ready() -> void:
	## Harriet, plate-accurate: cup hand raised, saucer held, pearls on.
	_rig = CharacterKit.harriet()
	add_child(_rig)
	var col := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.3
	shape.height = 1.6
	col.shape = shape
	col.position = Vector3(0, 0.8, 0)
	add_child(col)
	_cup = MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.height = 0.09
	cm.top_radius = 0.055
	cm.bottom_radius = 0.045
	var cmat := StandardMaterial3D.new()
	cmat.albedo_color = Color(0.87, 0.83, 0.72)
	cm.material = cmat
	_cup.mesh = cm
	add_child(_cup)
	var tag := Label3D.new()
	tag.text = "HARRIET"
	tag.font_size = 26
	tag.position = Vector3(0, 1.8, 0)
	tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tag.modulate = Color(0.85, 0.93, 0.77)
	add_child(tag)


func _physics_process(delta: float) -> void:
	## the cup sits in her raised hand and gains altitude by the day
	_cup.position = Vector3(0.18, 0.99 + 0.05 * minf(float(GameState.day), 6.0), 0.17)
	if not Broadcast.on_air:
		return  ## the freeze: mid-motion, until the return cue
	_t += delta
	rotation.z = sin(_t * 0.9) * 0.04


func get_prompt() -> String:
	if not Broadcast.on_air:
		return "HARRIET · mid-motion"
	return "HARRIET · in her chair (E)"


func interact(_player: Node3D) -> void:
	if GameState.is_dead("HARRIET"):
		if GameState.cause_of("HARRIET").begins_with("H2"):
			GameState.toast("Two of her. Neither resumes. The schedule has stopped scheduling this chair.")
		return
	if not Broadcast.on_air:
		if _slip_armed and not GameState.harriet_slip and not _h1_pending:
			GameState.harriet_slip = true
			_h1_pending = true
			GameState.toast("You slide the slip from her fingers. They do not close on the absence. Nothing does, yet.")
			return
		Achievements.unlock("A06")
		GameState.toast("She does not resume until the return cue. Her cup has been rising since Tape 1.")
		if GameState.day >= 2 and not GameState.harriet_slip and not _h1_pending:
			_slip_armed = true
			GameState.toast("Her hand holds a signature slip. Paper, free, unmoving. (E again to take it)")
		return
	if GameState.h2_pending and not GameState.is_dead("HARRIET"):
		GameState.h2_pending = false
		GameState.toast("The break comes. Harriet freezes, and one frame later, freezes again, an inch to the left.")
		await get_tree().create_timer(2.8).timeout
		GameState.toast("Doubled at the shoulders. Both mouths open on different vowels. The teacup rises in two hands at two heights.")
		GameState.show_caption("[ONE FRAME LEFT OF HERSELF]")
		_splice_visual()
		GameState.mark_casualty("HARRIET", "H2 · THE SPLICE", "doubled; the schedule stopped scheduling her")
		return
	if _h1_pending and not GameState.is_dead("HARRIET"):
		_h1_pending = false
		visible = false
		GameState.toast("The break ends. Harriet's chair is warm. Harriet is not in it, or anywhere.")
		await get_tree().create_timer(2.4).timeout
		GameState.toast("The film cabinet will not fully close. Inside, folded small, with leader tape where her voice was.")
		GameState.show_caption("[A REEL, LABELED IN HER HAND: ME]")
		GameState.mark_casualty("HARRIET", "H1 · CONTINUITY", "edited for continuity; the slip signs in her hand")
		return
	if GameState.is_dead("HARRIET"):
		return
	GameState.toast("HARRIET · %s" % LINES[_li])
	_li = (_li + 1) % LINES.size()
