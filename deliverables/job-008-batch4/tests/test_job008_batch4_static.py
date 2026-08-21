#!/usr/bin/env python3
"""Godot-free static checks for job-008 batch4 remake (020/024 vs refreshed mirror). Exit 0 on PASS."""
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


def func_body(src: str, name: str) -> str:
    m = re.search(r"^func %s\b.*$" % re.escape(name), src, re.M)
    if not m:
        return ""
    m2 = re.search(r"^func ", src[m.end() :], re.M)
    end = m.end() + m2.start() if m2 else len(src)
    return src[m.start() : end]


def main() -> int:
    main_gd = read("game/scripts/main/Main.gd")
    hover = read("game/scripts/ui/UiHoverOverlay.gd")

    portrait = func_body(main_gd, "_add_character_portrait_card")
    info = func_body(main_gd, "_add_info_card")
    if not portrait:
        fail("missing _add_character_portrait_card")
    if "alignment: HorizontalAlignment" in portrait.split("\n")[0] or "title_label.horizontal_alignment = alignment" in portrait:
        fail("020 polluted _add_character_portrait_card (previous dangerous apply)")

    if "func _add_info_card(title: String, lines: Array, variant: String = \"default\", alignment: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT) -> void:" not in main_gd:
        fail("020 _add_info_card must take alignment")
    if "_add_info_card(_localized_text(\"ui.save_load.slot_1.title\"), _save_slot_detail_lines(slot_summary), \"default\", HORIZONTAL_ALIGNMENT_CENTER)" not in main_gd:
        fail("020 delete confirm fallback card must be centered")
    if "title_label.horizontal_alignment = alignment" not in info:
        fail("020 info card title must honor alignment")
    if "ui_text_save_delete_confirm_target_slot_%02d" not in func_body(main_gd, "_show_approved_save_delete_confirm"):
        fail("020 B1 live path must center target_slot labels")

    if "func _keep_approved_options_nav_focus_only" not in main_gd:
        fail("024 missing _keep_approved_options_nav_focus_only")
    opt = func_body(main_gd, "_show_approved_b2_options")
    if "button.set_meta(\"ui_hover_suppress_hover_draw\", true)" not in func_body(main_gd, "_keep_approved_options_nav_focus_only"):
        fail("024 options nav must set ui_hover_suppress_hover_draw")
    if "view.get_node_or_null(\"ApprovedComponent_options_nav_input\")" not in opt:
        fail("024 must retarget baked game crop")
    if "ui_wiring_b2_options_language" not in opt or "ui_wiring_b2_options_input" not in opt:
        fail("024 must keep language/input extra category rows")
    if "func _hover_draw_suppressed" not in hover:
        fail("024 UiHoverOverlay missing _hover_draw_suppressed (expected already on refreshed HEAD)")
    if "pointer_hover := _hovered and not _hover_draw_suppressed()" not in hover:
        fail("024 overlay must ignore pointer hover when suppressed")

    if "ApprovedB2Component_ui_wiring_b2_pause_options_hex" not in main_gd:
        fail("006 pause settings missing hex frame underlay")
    if "Rect2(430.0, 598.0, 420.0, 48.0)" in main_gd:
        fail("006 pause title still uses original 48px-tall rect")
    if "Rect2(430.0, 602.0, 420.0, 70.0)" in main_gd:
        fail("006 bounced DOWN title rect y=602/h=70 must not return")
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

    for token in (
        '[\"画面\", \"音量\", \"ゲーム\", \"戻る\"]',
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
