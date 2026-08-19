#!/usr/bin/env python3
"""Godot-free static checks for job-008 batch 3 mid/low fixes. Exit 0 on PASS."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    main_gd = read("game/scripts/main/Main.gd")
    hover = read("game/scripts/ui/UiHoverOverlay.gd")
    b2 = read("game/scripts/ui/Stage4MassBatch2.gd")
    b3 = read("game/scripts/ui/Stage4MassBatch3.gd")
    b4 = read("game/scripts/ui/Stage4MassBatch4.gd")
    pilot = read("game/scripts/ui/Stage4EquipmentListPilot.gd")
    world = read("game/scripts/worldmap/WorldMap.gd")

    # 012 shop sold-out overlap + Batch3 wrap helper (complete version, once)
    if '"%s\\n%d黒貨  %s"' not in main_gd:
        fail("012 shop rows must be name + newline + price/stock")
    if "clip_contents = not wrap" not in b3:
        fail("012 Stage4MassBatch3 _add_text_slot must use the complete wrap path")
    if "VERTICAL_ALIGNMENT_TOP if wrap" not in b3:
        fail("012 wrap labels must top-align")
    if 'label.text_overrun_behavior = TextServer.OVERRUN_NO_TRIMMING if wrap' not in b3:
        fail("012 wrap labels must not trim")
    if b3.count("clip_contents = not wrap") != 1:
        fail("012 Batch3 wrap helper must appear once")

    # 013 character select captions
    if "func _center_character_select_button_caption" not in main_gd:
        fail("013 missing _center_character_select_button_caption")
    if "Vector2(852.0, 512.0)" not in main_gd:
        fail("013 confirm plate must fill approved rect")

    # 014 equipment list summary wrap
    if "Rect2(840.0, 294.0, 292.0, 44.0)" not in pilot:
        fail("014 summary line 4 must grow to 292x44")
    if "wrap: bool = false" not in pilot:
        fail("014 _add_text must accept wrap")

    # 015 equipment slots card clip
    if "Rect2(768.0, 420.0, 96.0, 155.0)" not in main_gd:
        fail("015 slot hotspot 1 must move in-frame")
    if "Rect2(1086.0, 420.0, 96.0, 155.0)" not in main_gd:
        fail("015 must expose the 4th slot hotspot")
    if "Rect2(780.0, 420.0, 105.0, 155.0)" in main_gd:
        fail("015 leftover old 3-slot hotspot")

    # 016 equipment candidates compare wrap
    if "[390, 615, 450, 20]" not in b3:
        fail("016 comparison labels must widen to 450")
    if '"id": "comparison_panel"' not in b3 or '"autowrap": true' not in b3:
        fail("016 comparison_panel must set autowrap")

    # 017 dungeon info overlap / wrap
    if '"帰還 45%\\n続行で報酬 +10%/R"' not in main_gd:
        fail("017 condition line must break before 続行")
    if "Rect2(985.0, 562.0, 250.0, 26.0)" not in main_gd:
        fail("017 summon/cancel must lift off 出発する")
    if "Rect2(985.0, 570.0, 250.0, 30.0)" in main_gd:
        fail("017 leftover old summon rect")

    # 018 dungeon round choice width
    if '"id": "choice_detail", "rect": [535, 215, 280, 181]' not in b4:
        fail("018 choice_detail region must widen to 280x181")
    if '"id": "choice_detail", "rect": [535, 215, 145, 175]' in b4:
        fail("018 leftover old 145-wide choice_detail")

    # 019 save/load duplicate draw
    if "func _suppress_save_load_duplicate_draw" not in main_gd:
        fail("019 missing _suppress_save_load_duplicate_draw")
    if "ui_save_load_title_well_cover" not in main_gd:
        fail("019 must cover leftover title well")

    # 020 save delete alignment
    if "alignment: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT" not in main_gd:
        fail("020 _add_info_card must take alignment")
    if "_add_info_card(_localized_text(\"ui.save_load.slot_1.title\"), _save_slot_detail_lines(slot_summary), \"default\", HORIZONTAL_ALIGNMENT_CENTER)" not in main_gd:
        fail("020 delete confirm card must be centered")

    # 021 enhance preview name break + cost width
    if "func _prohibit_mid_word_break" not in main_gd:
        fail("021 missing _prohibit_mid_word_break")
    if "char(0x2060)" not in main_gd:
        fail("021 CJK names must use WORD JOINER")
    if "[430, 468, 530, 36]" not in b2:
        fail("021 enhance cost band must widen")

    # 022 item detail actions
    if 'if screen_id == "item_detail"' not in b2:
        fail("022 item_detail buttons need top pad")
    if "[566, 602, 145, 52]" not in b2:
        fail("022 item_detail action slots must inset")

    # 023 scene choice result width (enhance 37)
    if "ADV_CHOICE_RESULT_HEIGHT" not in main_gd:
        fail("023 missing ADV_CHOICE_RESULT_HEIGHT")
    if "ADV_CHOICE_RESULT_MAX_WIDTH_RATIO" not in main_gd:
        fail("023 missing ADV_CHOICE_RESULT_MAX_WIDTH_RATIO")
    if "AUTOWRAP_WORD_SMART" not in main_gd:
        fail("023 result line must wrap")

    # 024 options single chrome + overlay once
    if "func _keep_approved_options_nav_focus_only" not in main_gd:
        fail("024 missing _keep_approved_options_nav_focus_only")
    if 'button.set_meta("ui_hover_suppress_hover_draw", true)' not in main_gd:
        fail("024 options nav must set ui_hover_suppress_hover_draw")
    if "func _hover_draw_suppressed" not in hover:
        fail("024 UiHoverOverlay missing _hover_draw_suppressed")
    if "pointer_hover := _hovered and not _hover_draw_suppressed()" not in hover:
        fail("024 overlay must ignore pointer hover when suppressed")
    if hover.count("func _hover_draw_suppressed") != 1:
        fail("024 overlay hook must appear once")

    # 025 gallery title spacer
    if "title_lift.custom_minimum_size = Vector2(1.0, 24.0)" not in main_gd:
        fail("025 gallery needs 24px title spacer")

    # 026 system menu rows
    if 'menu_box.add_theme_constant_override("separation", 6)' not in main_gd:
        fail("026 system_menu must tighten row gap")
    if "row.custom_minimum_size.y = 40.0" not in main_gd:
        fail("026 system_menu buttons must be 40px")

    # 027 motion check QA
    if "Skip STANDING MOTION QA" not in main_gd:
        fail("027 must skip STANDING MOTION QA draw")
    if 'draw_rect(Rect2(panel_pos, menu_panel.size), Color("#111017"))' not in main_gd:
        fail("027 must opaque-fill the left shell")

    # 028 stage select clip
    if "[48, 112, 1172, 162]" not in b2:
        fail("028 stage_card_01 must clip to 1172")
    if "[875, 638, 280, 48]" not in b2:
        fail("028 enter_action must shrink off the red ornament")

    # 029 world map snap
    if ").round()" not in world or "positionNormalized" not in world:
        fail("029 node draw position must integer-snap")
    if 'return map_rect.position + map_rect.size * Vector2(float(position.get("x", 0.5)), float(position.get("y", 0.5)))\n' in world:
        fail("029 leftover unsnapped node position")

    # 030 objective leftover rule
    if "ObjectiveCard03LeftoverRuleMask" not in main_gd:
        fail("030 missing card03 leftover rule mask")

    # 031 town back align
    if "[32, 640, 140, 42]" not in b3:
        fail("031 town back_action must recenter in the plate")

    # 032 loading gap
    if 'title.replace(" へ", "へ")' not in main_gd:
        fail("032 travel title must collapse space before へ")
    if "[410, 400, 460, 40]" not in b3:
        fail("032 destination band must widen")

    # 033 summon header
    if "[350, 88, 580, 35]" not in b2:
        fail("033 summon resource_cost must widen")

    # 034 scene view wait inset
    if "ADV_DIALOGUE_CONTENT_PADDING + 48.0 + 20.0" not in main_gd:
        fail("034 wait triangle needs extra 20px inset")

    # 035 clear captions wrap (must NOT touch batch2 010 button overlap)
    if "AUTOWRAP_ARBITRARY" not in b4:
        fail("035 clear unlock_rows need Batch4 autowrap")
    if "[400, 395, 150, 44]" not in b4:
        fail("035 unlock slot must grow")
    if "_clip_approved_b2_result_action" in b4 or "Rect2(895.0, 452.0, 160.0, 38.0)" in b4:
        fail("035 must not touch batch2 010 button overlap")

    # 036 alert overlay
    if "alert_spark_overshoot" not in b4:
        fail("036 missing alert spark overshoot mask")
    if "[564, 588, 180, 28]" not in b4:
        fail("036 alert_line must drop 6px")

    # 037 scene choice bottom margin (low 36)
    if "ADV_DIALOGUE_BOTTOM_MARGIN" not in main_gd:
        fail("037 missing ADV_DIALOGUE_BOTTOM_MARGIN")

    # 038 scene choice result tab height (low 37)
    if "const ADV_NAME_TAB_SIZE := Vector2(200.0, 40.0)" not in main_gd:
        fail("038 name tab height must be 40")
    if "const ADV_NAME_TAB_OVERLAP := ADV_NAME_TAB_SIZE.y - 16.0" not in main_gd:
        fail("038 name tab overlap must match quick row")
    if "const ADV_NAME_TAB_SIZE := Vector2(200.0, 50.0)" in main_gd:
        fail("038 leftover 50px name tab")

    # 039 credits leftover clip
    if "STATE_NEW_GAME_CONFIRM, STATE_CREDITS]" not in main_gd:
        fail("039 credits must clip leftover scroll line")

    # this batch must not include 27/28 card-cluster shifts
    for forbidden in (
        "func _card_group_shift_x",
        "func _centered_card_rect",
        "func _center_card_cluster_x",
        "VIEWPORT_CENTER_X := 640.0",
    ):
        if forbidden in main_gd or forbidden in b2 or forbidden in b3 or forbidden in b4:
            fail(f"27/28 must stay No; found {forbidden}")

    # live HEAD contracts this batch must not break
    for token in (
        '["画面", "音量", "ゲーム", "戻る"]',
        "func _show_run_history",
    ):
        if token not in main_gd:
            fail(f"live HEAD contract token missing: {token}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS job-008 batch3 static layout checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
