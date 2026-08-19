#!/usr/bin/env python3
"""Godot-free static checks for job-012 title/save image2 placement. Exit 0 on PASS."""
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
    data = path.read_bytes()
    if b"\r" in data:
        fail(f"{rel} contains CR (LF-only required)")
    return data.decode("utf-8")


def func_body(src: str, name: str) -> str:
    m = re.search(rf"^func {re.escape(name)}\(", src, re.M)
    if m is None:
        fail(f"cannot find func {name}")
        return ""
    start = m.start()
    nxt = re.search(r"\nfunc ", src[start + 1 :])
    end = start + 1 + nxt.start() if nxt else len(src)
    return src[start:end]


def main() -> int:
    main_gd = read("game/scripts/main/Main.gd")
    title_gd = read("game/scripts/ui/TitleImage2Layout.gd")
    if not main_gd or not title_gd:
        _report()
        return 1

    # --- OFF: image2 helpers are not called unless the flag gate is true ---
    title_menu = func_body(main_gd, "_show_title_menu")
    if title_menu:
        if "if TitleImage2Layout.is_enabled() and _show_title_image2_menu(slot_summary):" not in title_menu:
            fail("title image2 helper must be gated by TitleImage2Layout.is_enabled()")
        if "USE_APPROVED_UI_WIRING_B1 and _show_approved_title_menu" not in title_menu:
            fail("OFF title must still early-return to approved B1")
        # helper call only inside the is_enabled gate (one call site)
        if title_menu.count("_show_title_image2_menu") != 1:
            fail("title image2 helper call sites must be exactly the gated one")

    approved_title = func_body(main_gd, "_show_approved_title_menu")
    if approved_title and (
        "TitleImage2Layout" in approved_title or "_show_title_image2_menu" in approved_title
    ):
        fail("approved title B1 body must not call image2 title helpers")

    save_menu = func_body(main_gd, "_show_save_load_menu")
    if save_menu and "_apply_image2_save_select_layout" in save_menu:
        fail("OFF save_load entry must not call image2 save helper")

    approved_save = func_body(main_gd, "_show_approved_save_load_menu")
    if approved_save:
        if 'if _cmdline_has_flag("--ui-staging=image2"):' not in approved_save:
            fail("save image2 helper must be gated by --ui-staging=image2")
        if "_apply_image2_save_select_layout" not in approved_save:
            fail("save image2 helper not called from approved save menu")
        # call only inside the flag if
        gate = re.search(
            r'if _cmdline_has_flag\("--ui-staging=image2"\):\n\t\t_apply_image2_save_select_layout\(view, action, slot_state\)',
            approved_save,
        )
        if gate is None:
            fail("save image2 apply must sit inside the cmdline flag if")
        if approved_save.count("_apply_image2_save_select_layout") != 1:
            fail("save image2 helper call sites must be exactly the gated one")

    # --- ON title node names / rects (NOTES.md / title-coords.md) ---
    expected_title = {
        "BACKDROP_RECT": "Rect2(0.0, 0.0, 1280.0, 720.0)",
        "VIGNETTE_RECT": "Rect2(0.0, 0.0, 1280.0, 720.0)",
        "FRAME_RECT": "Rect2(340.0, 16.0, 600.0, 300.0)",
        "TITLE_WORDMARK_RECT": "Rect2(400.0, 88.0, 480.0, 72.0)",
        "TITLE_SUBTITLE_RECT": "Rect2(470.0, 200.0, 340.0, 28.0)",
    }
    for const, rect in expected_title.items():
        if f"const {const} := {rect}" not in title_gd:
            fail(f"TitleImage2Layout {const} != {rect}")
    if "const FRAME_PATCH := 48" not in title_gd:
        fail("title NinePatch patch_margin must be 48 (texture-space _c48)")
    for node in (
        'view.name = "TitleImage2Layout"',
        '"StartupBackdrop"',
        '"StartupVignette"',
        'frame.name = "MainMenuFrame"',
        '"TitleWordmark"',
        '"TitleSubtitle"',
        'const ACTION_NODE_PREFIX := "ui_text_title_main_actions_"',
    ):
        if node not in title_gd:
            fail(f"title missing node token {node}")
    buttons = [
        "Rect2(28.0, 376.0, 264.0, 40.0)",
        "Rect2(28.0, 428.0, 264.0, 40.0)",
        "Rect2(28.0, 480.0, 264.0, 40.0)",
        "Rect2(28.0, 532.0, 264.0, 40.0)",
        "Rect2(28.0, 584.0, 264.0, 40.0)",
    ]
    for rect in buttons:
        if rect not in title_gd:
            fail(f"title missing button rect {rect}")

    # 2-state: ruby focus/hover/pressed; normal is empty (iron unused)
    if 'button.add_theme_stylebox_override("focus", focus_style)' not in title_gd:
        fail("title missing ruby focus style")
    if "Do not force iron_secondary" not in title_gd and "iron_secondary unused" not in title_gd:
        if "Do not force iron_secondary" not in title_gd:
            fail("title should document iron_secondary unused")

    # --- ON save node names / rects (save comments / save-coords.md) ---
    save_fn = func_body(main_gd, "_apply_image2_save_select_layout")
    place_fn = func_body(main_gd, "_image2_place_save_part_button")
    if save_fn:
        expected_save = [
            ('slot.name = "ui_image2_save_slot_frame_01"', "save slot node"),
            ("slot.position = Vector2(48.0, 213.0)", "slot pos 48,213"),
            ("slot.size = Vector2(1182.0, 186.0)", "slot size 1182x186"),
            ("slot.patch_margin_left = 32", "slot 9slice 32"),
            ('Rect2(52.0, 632.0, 171.0, 58.0)', "back 52,632 171x58"),
            ('"ui_image2_save_delete"', "delete node"),
            ("Rect2(956.0, 318.0, 229.0, 54.0)", "delete 956,318 229x54"),
            ("Rect2(510.0, 543.0, 260.0, 66.0)", "new 510,543 260x66"),
            ("Rect2(954.0, 240.0, 230.0, 60.0)", "load 954,240 230x60"),
            ('"ui_image2_save_new_game"', "ready extra new-game node"),
            ("_start_new_game_from_save_load", "ready extra uses existing new-game callback"),
        ]
        for token, label in expected_save:
            if token not in save_fn:
                fail(f"save helper missing {label}: {token}")
        if "startup_backdrop" in save_fn or "startup_vignette" in save_fn:
            fail("save 05 must not place title backdrop/vignette")
        if "SAVE_SLOT_STATE_CORRUPT" not in save_fn:
            fail("corrupt-slot 仮決め branch missing")
    if place_fn:
        if "ruby_primary_button_normal_v001.png" not in place_fn:
            fail("save missing ruby normal 2-state")
        if "ruby_primary_button_focus_v001.png" not in place_fn:
            fail("save missing ruby focus 2-state")
        if "iron_secondary_button_normal_v001.png" not in place_fn:
            fail("save missing iron normal 2-state")
        if "iron_secondary_button_focus_v001.png" not in place_fn:
            fail("save missing iron focus 2-state")

    # forbidden parts on title/save helpers (age_gate already exists elsewhere in Main.gd)
    for blob, label in ((title_gd, "TitleImage2Layout.gd"), (save_fn, "save helper")):
        for forbidden in (
            "age_gate_frame",
            "confirm_modal_frame",
            "legal_scroll_frame",
        ):
            if blob and forbidden in blob:
                fail(f"{label} must not place {forbidden}")

    # filenames stay exact; directories may disagree (仮決め)
    if 'const PARTS_DIR := "res://assets/ui/ui_parts_batch1_image2/"' not in title_gd:
        fail("title PARTS_DIR 仮決め path missing")
    if "res://assets/ui/image2_parts/final/" not in main_gd:
        fail("save image2_parts/final 仮決め path missing")
    for fn in (
        "startup_backdrop_v001.png",
        "startup_vignette_v001.png",
        "main_menu_frame_c48_v001.png",
        "save_slot_frame_c32_v001.png",
        "ruby_primary_button_normal_v001.png",
        "ruby_primary_button_focus_v001.png",
        "iron_secondary_button_normal_v001.png",
        "iron_secondary_button_focus_v001.png",
    ):
        if fn not in title_gd and fn not in main_gd:
            fail(f"filename {fn} missing from title+save sources")

    # hardcoded JP in title helper (honest)
    title_helper = func_body(main_gd, "_show_title_image2_menu")
    if title_helper:
        if '"設定"' not in title_helper or '"クレジット"' not in title_helper:
            fail("title helper 設定/クレジット hardcoded JP tokens missing (would be a silent drop)")

    _report()
    return 1 if errors else 0


def _report() -> None:
    if errors:
        print("FAIL job-012 static placement")
        for item in errors:
            print(f"  - {item}")
    else:
        print("PASS job-012 static placement")


if __name__ == "__main__":
    sys.exit(main())
