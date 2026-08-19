extends SceneTree

const Registry := preload("res://scripts/ui/UiScreenRegistry.gd")

const EXPECTED_IDS := [
	"title", "stage_select", "world_map", "objective_log", "region_menu", "town_menu", "shop", "sell_inventory",
	"loading_transition", "dungeon_info", "summon_select", "character_select", "equipment_list", "equipment_slots",
	"equipment_candidates", "gallery", "scene_view", "scene_log", "run_history", "options", "options_language_text",
	"input_config", "reset_confirm", "unlock_confirm", "world_field_playing", "dungeon_playing", "level_up", "boss_reward",
	"awaken_cutin", "dungeon_round_result", "dungeon_round_choice", "pause", "clear", "game_over", "alert_overlay",
	"scene_choice", "scene_choice_result", "credits_license", "boot_splash", "age_gate", "save_load_menu",
	"save_delete_confirm", "motion_check", "adult_viewer_gate", "enhance_preview", "item_detail",
	"new_game_confirm", "world_tile_map", "system_menu",
	"return_title_confirm", "boundary_shop",
]

var failures := 0


func _init() -> void:
	_test_exact_ordered_inventory()
	_test_descriptors_and_master_coverage()
	_test_unknown_ids()
	_test_validation_guards()
	if failures == 0:
		print("UiScreenRegistry: 51 screens and 11 master groups verified")
		quit(0)
	else:
		push_error("UiScreenRegistry: %d test(s) failed" % failures)
		quit(1)


func _test_exact_ordered_inventory() -> void:
	var ids := Registry.ordered_ids()
	_expect(ids.size() == 51, "registry contains exactly 51 audited IDs")
	var seen := {}
	for index in EXPECTED_IDS.size():
		_expect(str(ids[index]) == EXPECTED_IDS[index], "audit order %d is %s" % [index + 1, EXPECTED_IDS[index]])
		seen[ids[index]] = true
	_expect(seen.size() == 51, "all audited IDs are unique")


func _test_descriptors_and_master_coverage() -> void:
	var represented := {}
	var descriptors := Registry.descriptors()
	_expect(descriptors.size() == 51, "every audited ID has a descriptor")
	for descriptor in descriptors:
		for field in ["id", "master", "shell", "backdrop", "density", "overlay"]:
			_expect(descriptor.has(field), "%s descriptor has %s" % [descriptor.get("id", "unknown"), field])
		represented[descriptor.get("master")] = true
	_expect(represented.size() == 11, "all 11 masters are represented")
	for master in Registry.master_ids():
		_expect(represented.has(master), "master %s is represented" % master)
	_expect(Registry.validation_errors().is_empty(), "canonical registry validates cleanly")


func _test_unknown_ids() -> void:
	_expect(not Registry.has_screen(&"not_a_screen"), "unknown ID is not registered")
	_expect(Registry.master_for(&"not_a_screen") == &"", "unknown ID has no master")
	_expect(Registry.descriptor(&"not_a_screen").is_empty(), "unknown ID has no descriptor")


func _test_validation_guards() -> void:
	var duplicate_ids: Array = Array(Registry.ordered_ids())
	duplicate_ids.append(&"title")
	var duplicate_errors := Registry.validation_errors(duplicate_ids, Registry.screen_to_master())
	_expect(_contains_error(duplicate_errors, "duplicate screen id"), "duplicate IDs are diagnosed")
	var missing_group_ids: Array = Array(Registry.ordered_ids())
	missing_group_ids.erase("awaken_cutin")
	var missing_errors := Registry.validation_errors(missing_group_ids, Registry.screen_to_master())
	_expect(_contains_error(missing_errors, "missing master group: M11"), "missing master groups are diagnosed")
	var missing_mapping := Registry.screen_to_master()
	missing_mapping.erase(&"title")
	var mapping_errors := Registry.validation_errors(Array(Registry.ordered_ids()), missing_mapping)
	_expect(_contains_error(mapping_errors, "missing master mapping: title"), "missing mappings are diagnosed")


func _contains_error(errors: PackedStringArray, fragment: String) -> bool:
	for message in errors:
		if message.contains(fragment):
			return true
	return false


func _expect(condition: bool, label: String) -> void:
	if condition:
		return
	failures += 1
	push_error("FAIL: %s" % label)
