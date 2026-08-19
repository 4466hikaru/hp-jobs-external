extends SceneTree
# job-008 batch3 headless smoke. Playable checkout only.
# Wait >=0.35s after init before any UI read (job-005 lesson).
# This batch does not change transition seconds (032 only collapses a title space).

const WAIT_SEC := 0.35


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	await create_timer(WAIT_SEC).timeout
	var errors: PackedStringArray = []
	var main_script := load("res://scripts/main/Main.gd") as Script
	if main_script == null:
		errors.append("Main.gd failed to load")
	else:
		var src := main_script.source_code
		for token in [
			"func _center_character_select_button_caption",
			"func _suppress_save_load_duplicate_draw",
			"func _prohibit_mid_word_break",
			"func _keep_approved_options_nav_focus_only",
			"ADV_CHOICE_RESULT_HEIGHT",
			"ADV_DIALOGUE_BOTTOM_MARGIN",
			"ADV_NAME_TAB_SIZE := Vector2(200.0, 40.0)",
		]:
			if src.find(token) < 0:
				errors.append("missing " + token)
	if errors.is_empty():
		print("PASS job-008 batch3 headless (waited %.2fs)" % WAIT_SEC)
		quit(0)
	else:
		print("FAIL")
		for e in errors:
			print(" - ", e)
		quit(1)
