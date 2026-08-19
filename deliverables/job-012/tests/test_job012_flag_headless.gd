extends SceneTree

## Playable-checkout only. The asset-stripped mirror cannot run Godot.
## Flag-only commit: no image2 part nodes are asserted here.
## Transition waits follow job-005 (~0.35s) so later placement tests can hook in.

func _initialize() -> void:
	var src := FileAccess.get_file_as_string("res://scripts/main/Main.gd")
	if src.find("func _ui_staging_is_image2()") < 0:
		push_error("_ui_staging_is_image2 missing")
		quit(1)
		return
	if src.find("_configure_ui_staging_arg(args)") < 0:
		push_error("_configure_ui_staging_arg not wired")
		quit(1)
		return
	var wait_sec: float = 0.35
	await create_timer(wait_sec).timeout
	print("PASS job-012 headless flag constants")
	quit(0)
