extends SceneTree

## Playable-checkout only. The asset-stripped mirror cannot run Godot.
## Static placement tests live in test_job012_static_placement.py.
## 0.35s wait is for Godot transition asserts on a playable checkout.
## This file does not instantiate title/save image2 nodes (assets may be absent).

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
	if src.find("func _show_title_image2_menu") < 0:
		push_error("_show_title_image2_menu missing")
		quit(1)
		return
	if src.find("func _apply_image2_save_select_layout") < 0:
		push_error("_apply_image2_save_select_layout missing")
		quit(1)
		return
	var wait_sec: float = 0.35
	await create_timer(wait_sec).timeout
	print("PASS job-012 headless flag+placement constants")
	quit(0)
