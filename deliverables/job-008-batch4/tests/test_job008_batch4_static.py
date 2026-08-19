#!/usr/bin/env python3
"""Godot-free static checks for job-008 batch4 (020/024 rebase + 006 UP). Exit 0 on PASS."""
from __future__ import annotations

import re
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

    # 020 save delete alignment
    if 'func _add_info_card(title: String, lines: Array, variant: String = "default", alignment: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT) -> void:' not in main_gd:
        fail("020 _add_info_card must take alignment")
    if "_add_info_card(_localized_text(\"ui.save_load.slot_1.title\"), _save_slot_detail_lines(slot_summary), \"default\", HORIZONTAL_ALIGNMENT_CENTER)" not in main_gd:
        fail("020 delete confirm card must be centered")
    if "title_label.horizontal_alignment = alignment" not in main_gd:
        fail("020 info card title must honor alignment")

    # 024 options single chrome
    if "func _keep_approved_options_nav_focus_only" not in main_gd:
        fail("024 missing _keep_approved_options_nav_focus_only")
    if 'button.set_meta("ui_hover_suppress_hover_draw", true)' not in main_gd:
        fail("024 options nav must set ui_hover_suppress_hover_draw")
    if 'view.get_node_or_null("ApprovedComponent_options_nav_input")' not in main_gd:
        fail("024 must retarget baked ゲーム crop")
    if "func _hover_draw_suppressed" not in hover:
        fail("024 UiHoverOverlay missing _hover_draw_suppressed")
    if "pointer_hover := _hovered and not _hover_draw_suppressed()" not in hover:
        fail("024 overlay must ignore pointer hover when suppressed")
    if hover.count("func _hover_draw_suppressed") != 1:
        fail("024 overlay hook must appear once")

    # 006 pause UP (not the bounced DOWN)
    if "ApprovedB2Component_ui_wiring_b2_pause_options_hex" not in main_gd:
        fail("006 pause 設定 is missing the hex frame underlay")
    if "Rect2(430.0, 598.0, 420.0, 48.0)" in main_gd:
        fail("006 pause タイトルへ still uses the original 48px-tall rect")
    if "Rect2(430.0, 602.0, 420.0, 70.0)" in main_gd:
        fail("006 bounced DOWN title rect y=602/h=70 must not return")
    save_rect = re.search(
        r'_add_approved_ui_wiring_b2_component_action\(view, "ui_wiring_b2_pause_save", Rect2\(([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\)',
        main_gd,
    )
    if not save_rect:
        fail("006 pause save component action missing")
    else:
        sy = float(save_rect.group(2))
        if sy >= 486.0:
            fail(f"006 pause save y={sy} was not moved UP from original 486")
        if sy < 469.0:
            fail(f"006 pause save y={sy} overlaps 設定 label (bottom 469)")
    title_rect = re.search(
        r'_add_approved_ui_wiring_b2_component_action\(view, "ui_wiring_b2_pause_title", Rect2\(([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\)',
        main_gd,
    )
    if not title_rect:
        fail("006 pause title component action missing")
    else:
        y = float(title_rect.group(2))
        h = float(title_rect.group(4))
        bottom = y + h
        if abs(y - 566.0) > 0.01 or abs(h - 70.0) > 0.01:
            fail(f"006 pause title must be Rect2(430, 566, 420, 70); got y={y} h={h}")
        if abs(bottom - 636.0) > 0.01:
            fail(f"006 pause title bottom {bottom} must be 636")
        if bottom >= 646.0:
            fail(f"006 pause title bottom {bottom} must be < original 646 (UP, not DOWN)")
        margin = 720.0 - bottom
        if abs(margin - 84.0) > 0.01:
            fail(f"006 pause bottom margin {margin} must be 84px")

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
    print("PASS job-008 batch4 static layout checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
