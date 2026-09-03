extends CharacterBody3D
## First-person controller: walk, look, interact by raycast. Deliberate weight.

const SPEED := 3.1
const ACCEL := 10.0
const MOUSE_SENS := 0.0022
const REACH := 2.6

var _pitch := 0.0
var locked := false

@onready var cam: Camera3D = $Camera3D
@onready var ray: RayCast3D = $Camera3D/RayCast3D


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	ray.target_position = Vector3(0, 0, -REACH)


func _input(event: InputEvent) -> void:
	## Mouse look lives in _input: no Control in the tree can eat the motion
	## event before it reaches us. (The HUD's full-rect Control was doing
	## exactly that — the camera never turned on any interactive run.)
	if locked:
		return
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		var sens := MOUSE_SENS * clampf(GameState.mouse_sens, 0.2, 3.0)
		rotate_y(-event.relative.x * sens)
		_pitch = clampf(_pitch - event.relative.y * sens, -1.3, 1.3)
		cam.rotation.x = _pitch


func _unhandled_input(event: InputEvent) -> void:
	if locked:
		return
	if event.is_action_pressed("ui_cancel"):
		GameState.pause_requested.emit()
	if event.is_action_pressed("toggle_tbc"):
		GameState.set_tbc(not GameState.tbc_enabled)
	if event.is_action_pressed("interact"):
		_try_interact()


func _physics_process(delta: float) -> void:
	if locked:
		return
	if not is_on_floor():
		velocity.y -= 12.0 * delta
	var input_dir := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var wish := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized() * SPEED
	velocity.x = move_toward(velocity.x, wish.x, ACCEL * delta)
	velocity.z = move_toward(velocity.z, wish.z, ACCEL * delta)
	move_and_slide()


func current_target() -> Interactable:
	if ray.is_colliding():
		var hit := ray.get_collider()
		if hit is Interactable:
			return hit
	return null


func _try_interact() -> void:
	var target := current_target()
	if target:
		target.interact(self)
