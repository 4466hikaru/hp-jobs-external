extends SceneTree

## job-005: reach revived screens + return, and keep reused IDs split.
## Drives Main the same way B1/B2 runtime tests do. Requires the playable
## Godot project (not the asset-stripped hp-game-share mirror).

const MAIN_SCENE := preload("res://scenes/main/Main.tscn")
const TOWN_ID := "town.ashwing_refuge"

var failures := PackedStringArray()


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	var main := MAIN_SCENE.instantiate()
	root.add_child(main)
	await process_frame
	await process_frame
	main.set("screen_audit_enabled", true)
	main.call("_prepare_screen_audit_runtime")
	main.set("screen_audit_enabled", false)
	main.set("new_game_stage", "done")

	await _test_b2_language_and_input(main)
	await _test_save_delete_not_title_confirm(main)
	await _test_return_title_not_save_delete(main)
	await _test_boundary_shop_not_pause(main)
	_test_run_history_still_callable(main)

	main.queue_free()
	await process_frame
	if failures.is_empty():
		print("Job005ScreenWiring: PASS reach+back for language/input/save-delete/return-title/boundary-shop")
		quit(0)
		return
	for failure in failures:
		push_error("Job005ScreenWiring: " + failure)
	quit(1)


func _test_b2_language_and_input(main: Node) -> void:
	main.call("_show_options", "title")
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "options", "B2 options opens as options")
	var options_view := main.get("approved_ui_wiring_b2_view") as Control
	var language := options_view.get_node_or_null("ui_wiring_b2_options_language") as Button if options_view != null else null
	var input_btn := options_view.get_node_or_null("ui_wiring_b2_options_input") as Button if options_view != null else null
	if language == null or input_btn == null:
		# Legacy shell still exposes the old _show_options() items.
		main.call("_show_language_text_settings", "title")
	else:
		_expect(language.get_signal_connection_list(&"pressed").size() > 0, "language category action is connected")
		language.emit_signal("pressed")
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "options_language_text", "B2 options reaches options_language_text")
	_expect(str(main.get("run_state")) == "options_language_text", "language screen sets its own run state")
	var language_view := main.get("approved_ui_wiring_b2_view") as Control
	var speed_up := language_view.get_node_or_null("ui_wiring_b2_language_text_speed_up") as Button if language_view != null else null
	if speed_up != null:
		var before := float((main.call("_settings_data") as Dictionary).get("textSpeed", 36.0))
		speed_up.emit_signal("pressed")
		await process_frame
		await process_frame
		var after := float((main.call("_settings_data") as Dictionary).get("textSpeed", 36.0))
		_expect(not is_equal_approx(before, after), "language text-speed change is saved")
	main.call("_return_from_language_text_settings")
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "options", "language back returns to options")

	options_view = main.get("approved_ui_wiring_b2_view") as Control
	input_btn = options_view.get_node_or_null("ui_wiring_b2_options_input") as Button if options_view != null else null
	if input_btn == null:
		main.call("_show_input_config", "title")
	else:
		input_btn.emit_signal("pressed")
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "input_config", "B2 options reaches input_config")
	_expect(str(main.get("run_state")) == "input_config", "input screen sets its own run state")
	var input_view := main.get("approved_ui_wiring_b2_view") as Control
	var reset := input_view.get_node_or_null("ui_text_input_config_reset_action_01") as Button if input_view != null else null
	if reset != null:
		reset.emit_signal("pressed")
		await process_frame
		await process_frame
		_expect(str(main.call("get_ui_screen_id")) == "input_config", "input reset stays on input_config after save")
	main.call("_return_from_input_config")
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "options", "input back returns to options")


func _test_save_delete_not_title_confirm(main: Node) -> void:
	main.set("screen_audit_enabled", true)
	main.call("_show_save_load_menu", "title")
	main.set("screen_audit_enabled", false)
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "save_load_menu", "B1 save/load opens")
	var save_view := main.get("approved_ui_wiring_b1_view") as Control
	var delete_btn := save_view.get_node_or_null("ui_wiring_b1_save_load_delete") as Button if save_view != null else null
	_expect(delete_btn != null, "B1 save/load exposes a delete button")
	if delete_btn == null:
		main.call("_show_save_delete_confirm", "title")
	else:
		_expect(not delete_btn.disabled, "populated audit save enables delete")
		delete_btn.emit_signal("pressed")
	await create_timer(0.4).timeout
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "save_delete_confirm", "delete reaches save_delete_confirm")
	_expect(str(main.call("get_ui_screen_id")) != "return_title_confirm", "save delete is not the town-title confirm")
	_expect(str(main.get("run_state")) == "save_delete_confirm", "save delete uses its own run state")
	var confirm_view := main.get("approved_ui_wiring_b1_view") as Control
	var cancel := confirm_view.get_node_or_null("ui_text_save_delete_confirm_actions_02") as Button if confirm_view != null else null
	if cancel != null:
		cancel.emit_signal("pressed")
	else:
		main.call("_cancel_save_delete_confirm")
	await create_timer(0.4).timeout
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "save_load_menu", "save-delete cancel returns to save/load")


func _test_return_title_not_save_delete(main: Node) -> void:
	main.call("_show_town_menu", TOWN_ID)
	await process_frame
	await process_frame
	main.call("_show_town_title_confirm")
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "return_title_confirm", "town back-to-title uses return_title_confirm")
	_expect(str(main.call("get_ui_screen_id")) != "save_delete_confirm", "town-title confirm is not save_delete_confirm")
	_expect(str(main.get("run_state")) == "town_title_confirm", "town-title confirm keeps its own run state")
	main.call("_transition_cancel_town_title_confirm")
	await create_timer(0.4).timeout
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "town_menu", "town-title cancel returns to town")


func _test_boundary_shop_not_pause(main: Node) -> void:
	main.set("screen_audit_enabled", true)
	main.call("_show_screen_audit_state", "boundary_shop")
	main.set("screen_audit_enabled", false)
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "boundary_shop", "boundary shop uses its own screen id")
	_expect(str(main.call("get_ui_screen_id")) != "pause", "boundary shop is not pause")
	_expect(str(main.get("run_state")) == "boundary_shop", "boundary shop keeps STATE_BOUNDARY_SHOP")

	main.set("screen_audit_enabled", true)
	main.call("_show_screen_audit_state", "pause")
	main.set("screen_audit_enabled", false)
	await process_frame
	await process_frame
	_expect(str(main.call("get_ui_screen_id")) == "pause", "pause still opens as pause after the split")
	var pause_view := main.get("approved_ui_wiring_b2_view") as Control
	_expect(pause_view != null and str(pause_view.get_meta("runtime_approved_screen_id", "")) == "pause", "pause keeps its B2 identity")


func _test_run_history_still_callable(main: Node) -> void:
	_expect(main.has_method("_show_run_history"), "run_history builder remains")
	_expect(main.has_method("_transition_return_from_run_history"), "run_history return remains")
	_expect(main.has_method("_record_run_history"), "run_history recorder remains")


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
