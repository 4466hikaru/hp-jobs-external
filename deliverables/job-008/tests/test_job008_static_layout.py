#!/usr/bin/env python3
"""Godot-free static checks for job-008 UI defect fixes. Exit 0 on PASS."""
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


def first_int_list(pattern: str, text: str) -> list[int]:
    m = re.search(pattern, text)
    if not m:
        return []
    return [int(x) for x in re.findall(r"-?\d+", m.group(0))]


def main() -> int:
    main_gd = read("game/scripts/main/Main.gd")
    batch2 = read("game/scripts/ui/Stage4MassBatch2.gd")
    batch3 = read("game/scripts/ui/Stage4MassBatch3.gd")

    if "const MENU_PANEL_FRAME_INSET := 72.0" not in main_gd:
        fail("Main.gd missing MENU_PANEL_FRAME_INSET 72")
    if "maxf(content_margin, MENU_PANEL_FRAME_INSET)" not in main_gd:
        fail("9-slice / kit2 panel path must clamp content_margin to MENU_PANEL_FRAME_INSET")
    if "menu_panel.size.x - MENU_PANEL_FRAME_INSET * 2.0" not in main_gd:
        fail("_menu_content_width must subtract 2 * MENU_PANEL_FRAME_INSET")
    if "_kit2_menu_panel_style(26.0)" in main_gd:
        fail("legacy shell still uses _kit2_menu_panel_style(26.0)")
    if "_kit2_menu_panel_style(24.0)" in main_gd:
        fail("legacy shell still uses _kit2_menu_panel_style(24.0)")

    if "not _scene_log_is_open()" not in main_gd:
        fail("ADV overlay must stay hidden while the scene log is open")
    show_log = re.search(
        r"func _show_scene_log_overlay\(\) -> void:\n(?:.*\n){18}",
        main_gd,
    )
    if not show_log:
        fail("could not read _show_scene_log_overlay")
    elif "scene_adv_overlay.visible = false" not in show_log.group(0):
        fail("_show_scene_log_overlay must hide scene_adv_overlay before layout")

    if "approved_ui_wiring_b1_view != null" not in main_gd or "menu_panel.visible = false" not in main_gd:
        fail("_layout_ui must hide MenuPanel for approved B1/B2/B3 views")

    # world_tile_map header: 地点 / 危険度 / 黒貨 must be wider than the 75/110 job-004 boxes
    loc = first_int_list(r'"tile_tooltips".*?slot_rects": \[\[798, 6, 156, 42\]', batch2)
    if not loc:
        # fall back to any first tile_tooltips slot
        m = re.search(r'"tile_tooltips".*?slot_rects": \[\[(\d+), (\d+), (\d+), (\d+)\]', batch2)
        if not m:
            fail("world_tile_map tile_tooltips slot_rects missing")
        else:
            w = int(m.group(3))
            if w < 140:
                fail(f"world_tile_map 地点 slot width {w} still < 140")
    hud = re.search(r'"hud_labels".*?slot_rects": \[\[(\d+), (\d+), (\d+), (\d+)\]', batch2)
    if not hud:
        fail("world_tile_map hud_labels slot_rects missing")
    else:
        w = int(hud.group(3))
        if w < 100:
            fail(f"world_tile_map 黒貨 slot width {w} still < 100")

    slot = re.search(r'"slot_cards".*?slot_rects": \[\[(\d+), (\d+), (\d+), (\d+)\]', batch3)
    if not slot:
        fail("equipment_slots slot_cards missing")
    else:
        y = int(slot.group(2))
        h = int(slot.group(4))
        if y + h > 560:
            fail(f"equipment_slots label bottom {y+h} still sits on the card frame (want <= 560)")
        if y >= 535:
            fail(f"equipment_slots label y={y} was not moved up from the clipped 535 band")

    if "ApprovedB2Component_ui_wiring_b2_pause_options_hex" not in main_gd:
        fail("pause 設定 is missing the hex frame underlay")
    if "Rect2(430.0, 598.0, 420.0, 48.0)" in main_gd:
        fail("pause タイトルへ still uses the old 48px-tall bottom-hugging rect")
    save_rect = re.search(
        r'_add_approved_ui_wiring_b2_component_action\(view, "ui_wiring_b2_pause_save", Rect2\(([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\)',
        main_gd,
    )
    if not save_rect:
        fail("pause save component action missing")
    else:
        sy = float(save_rect.group(2))
        if sy >= 486.0:
            fail(f"pause save y={sy} was not moved up from original 486")
        if sy < 469.0:
            fail(f"pause save y={sy} overlaps 設定 label (bottom 469)")
    title_rect = re.search(
        r'_add_approved_ui_wiring_b2_component_action\(view, "ui_wiring_b2_pause_title", Rect2\(([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\)',
        main_gd,
    )
    if not title_rect:
        fail("pause title component action missing")
    else:
        y = float(title_rect.group(2))
        h = float(title_rect.group(4))
        bottom = y + h
        if bottom >= 646.0:
            fail(f"pause タイトルへ bottom {bottom} must be < original 646")
        if y > 576.0 and h >= 70.0:
            fail(f"pause タイトルへ y={y} with h={h} exceeds y<=576 guideline")
        if h < 60:
            fail(f"pause タイトルへ height {h} is too short for the hex frame")

    # job-005 contracts that this job must not break
    for token in (
        '["画面", "音量", "ゲーム", "戻る"]',
        "func _show_run_history",
        '_set_ui_screen_id(&"boundary_shop")',
        '_push_ui_screen_overlay(&"return_title_confirm")',
    ):
        if token not in main_gd:
            fail(f"job-005 contract token missing: {token}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS job-008 static layout checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
