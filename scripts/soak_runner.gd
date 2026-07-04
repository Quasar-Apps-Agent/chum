extends Node
## Headless soak entry. Run:
##   godot --headless res://scenes/soak.tscn -- --bot=wanderer --minutes=240
## Bots: wanderer, checker, fail. Emits user://INVARIANTS.txt and stdout.

var bot := "wanderer"
var minutes := 1.0


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--bot="):
			bot = a.substr(6)
		elif a.begins_with("--minutes="):
			minutes = float(a.substr(10))
	var main := (load("res://scenes/main.tscn") as PackedScene).instantiate()
	add_child(main)
	await get_tree().process_frame
	GameState.reset_new_game()
	if bot == "fail":
		GameState.day = 3
		GameState.current_tape = 3
		GameState.assets = ["VERSE", "CART", "SCRIPT", "CARD"]
		GameState.decision = "PERFORM"
		GameState.lockdown_done = true
		GameState.is_night = true
		GameState.start_finale()
	else:
		GameState.is_night = true
		GameState.night_changed.emit(true)
	var driver := BotDriver.new()
	driver.mode = bot
	add_child(driver)
	print("SOAK START · bot=%s · minutes=%.1f" % [bot, minutes])
	await get_tree().create_timer(minutes * 60.0).timeout
	var card := InvariantParser.run(bot, minutes)
	var f := FileAccess.open("user://INVARIANTS.txt", FileAccess.WRITE)
	if f:
		f.store_string(card)
		f.close()
	print(card)
	get_tree().quit()
