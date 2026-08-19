extends SceneTree
# job-008 batch4 headless smoke. Playable checkout only.
# Wait >=0.35s after init before any UI read (job-005 lesson).
# This batch does not change transition seconds.

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
			"func _keep_approved_options_nav_focus_only",
			"alignment: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT",
			"ApprovedB2Component_ui_wiring_b2_pause_options_hex",
			"Rect2(430.0, 566.0, 420.0, 70.0)",
		]:
			if src.find(token) < 0:
				errors.append("missing " + token)
		if src.find("Rect2(430.0, 602.0, 420.0, 70.0)") >= 0:
			errors.append("bounced DOWN pause title rect still present")
	if errors.is_empty():
		print("PASS job-008 batch4 headless (waited %.2fs)" % WAIT_SEC)
		quit(0)
	else:
		print("FAIL")
		for e in errors:
			print(" - ", e)
		quit(1)
