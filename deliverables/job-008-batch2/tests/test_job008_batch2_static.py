#!/usr/bin/env python3
"""Godot-free static checks for job-008 batch 2 HIGH leftover fixes. Exit 0 on PASS."""
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

    # 007 shop: drop hover frame, keep focus only
    if "func _keep_approved_shop_row_focus_only" not in main_gd:
        fail("007 missing _keep_approved_shop_row_focus_only")
    if "_keep_approved_shop_row_focus_only(row)" not in main_gd:
        fail("007 shop row builder does not call _keep_approved_shop_row_focus_only")
    if 'button.set_meta("ui_hover_suppress_hover_draw", true)' not in main_gd:
        fail("007 shop rows must set ui_hover_suppress_hover_draw")
    if "func _hover_draw_suppressed" not in hover:
        fail("007 UiHoverOverlay missing _hover_draw_suppressed")
    if "pointer_hover := _hovered and not _hover_draw_suppressed()" not in hover:
        fail("007 UiHoverOverlay must ignore pointer hover when suppressed")

    # 008 sell: strip live [仮] prefix, do not invent PNG hide
    if "func _shop_item_product_display_name" not in main_gd:
        fail("008 missing _shop_item_product_display_name")
    if 'name.begins_with("[仮]")' not in main_gd:
        fail("008 must strip a leading [仮] from live sell titles")
    if main_gd.count("_shop_item_product_display_name") < 5:
        fail("008 sell cards / approved sell rows / summary must use product display name")
    if '"title": _shop_item_display_name(item)' in main_gd:
        fail("008 sell cards still use raw _shop_item_display_name for title")

    # 009 HUD: hide leftover hud_panel when CombatHudSlots is live
    if "func _legacy_combat_hud_replaced" not in main_gd:
        fail("009 missing _legacy_combat_hud_replaced")
    if 'ui_layer.get_node_or_null("CombatHudSlots")' not in main_gd:
        fail("009 must detect CombatHudSlots")
    sync = re.search(
        r"func _sync_gameplay_hud_visibility\(\) -> void:\n(?:.*\n){16}",
        main_gd,
    )
    if not sync:
        fail("could not read _sync_gameplay_hud_visibility")
    else:
        body = sync.group(0)
        if "_legacy_combat_hud_replaced()" not in body:
            fail("_sync_gameplay_hud_visibility must early-out when CombatHudSlots is live")
        if "hud_panel.visible = false" not in body:
            fail("legacy hud_panel must stay hidden when CombatHudSlots is live")

    # 010 clear: clip extra-actions + 14px row gap
    if "func _clip_approved_b2_result_action" not in main_gd:
        fail("010 missing _clip_approved_b2_result_action")
    if "clip.clip_contents = true" not in main_gd:
        fail("010 clip helper must set clip_contents")
    for rect in (
        "Rect2(895.0, 452.0, 160.0, 38.0)",
        "Rect2(1065.0, 452.0, 160.0, 38.0)",
        "Rect2(895.0, 504.0, 160.0, 38.0)",
        "Rect2(1065.0, 504.0, 160.0, 38.0)",
        "Rect2(895.0, 556.0, 160.0, 38.0)",
    ):
        if rect not in main_gd:
            fail(f"010 clear_action_rects missing {rect}")
    for old in (
        "Rect2(895.0, 464.0, 160.0, 38.0)",
        "Rect2(895.0, 508.0, 160.0, 38.0)",
        "Rect2(895.0, 552.0, 160.0, 38.0)",
    ):
        if old in main_gd:
            fail(f"010 leftover old 6px-gap rect {old}")

    # 011 game_over: same clip + leftover mask expanded (apply after 010)
    if "Vector2(800.0, 345.0)" not in main_gd:
        fail("011 leftover mask origin must be (800, 345)")
    if "Vector2(480.0, 140.0)" not in main_gd:
        fail("011 leftover mask size must be 480x140")
    if "Vector2(830.0, 345.0)" in main_gd:
        fail("011 leftover mask still starts at old x=830")
    if "Vector2(450.0, 140.0)" in main_gd:
        fail("011 leftover mask still uses old 450x140")
    if main_gd.count("_clip_approved_b2_result_action(view, action_node, rect)") != 1:
        fail("011 must clip every result extra-action (clear and game_over)")
    if "if cleared:\n\t\t\t_clip_approved_b2_result_action" in main_gd:
        fail("011 clip must not stay gated on cleared")

    # live HEAD contracts this batch must not break (job-005 tokens that exist without 005)
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
    print("PASS job-008 batch2 static layout checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
