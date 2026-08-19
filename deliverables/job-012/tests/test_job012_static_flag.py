#!/usr/bin/env python3
"""Godot-free static checks for job-012 --ui-staging=image2 flag. Exit 0 on PASS."""
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


def main() -> int:
    main_gd = read("game/scripts/main/Main.gd")
    if not main_gd:
        _report()
        return 1

    for token in (
        'var ui_staging_mode := ""',
        "func _configure_ui_staging_arg(args: PackedStringArray) -> void:",
        'if value == "--ui-staging":',
        'elif value.begins_with("--ui-staging="):',
        "func _ui_staging_is_image2() -> bool:",
        'return ui_staging_mode == "image2"',
        "_configure_ui_staging_arg(args)",
    ):
        if token not in main_gd:
            fail(f"Main.gd missing required token: {token}")

    # Flag branch must be live: configure is called from _configure_playtest,
    # not only declared.
    cfg = re.search(
        r"func _configure_playtest\(\) -> void:\n(?:.*\n){0,20}",
        main_gd,
    )
    if cfg is None or "_configure_ui_staging_arg(args)" not in cfg.group(0):
        fail("_configure_playtest must call _configure_ui_staging_arg (dead flag)")

    # OFF path: B1 title/save early returns must remain ungated by staging.
    title = re.search(
        r"func _show_title_menu\(\) -> void:\n(?:.*\n){12}",
        main_gd,
    )
    if title is None:
        fail("cannot find _show_title_menu")
    else:
        block = title.group(0)
        if "USE_APPROVED_UI_WIRING_B1 and _show_approved_title_menu" not in block:
            fail("title B1 early return missing")
        if "_ui_staging_is_image2" in block:
            fail("title menu is gated by ui-staging; OFF would not match current path")

    save = re.search(
        r"func _show_save_load_menu\(return_target: String = \"title\"\) -> void:\n(?:.*\n){12}",
        main_gd,
    )
    if save is None:
        fail("cannot find _show_save_load_menu")
    else:
        block = save.group(0)
        if "USE_APPROVED_UI_WIRING_B1 and _show_approved_save_load_menu" not in block:
            fail("save_load B1 early return missing")
        if "_ui_staging_is_image2" in block:
            fail("save_load menu is gated by ui-staging; OFF would not match current path")

    # Flag + placement must not pull age_gate/confirm/legal parts into Main.gd.
    for forbidden in (
        "age_gate_frame_c128_v001",
        "confirm_modal_frame_c48_v001",
        "legal_scroll_frame_c48_v001",
    ):
        if forbidden in main_gd:
            fail(f"flag-only patch must not invent placement node/part: {forbidden}")

    _report()
    return 1 if errors else 0


def _report() -> None:
    if errors:
        print("FAIL job-012 static flag")
        for item in errors:
            print(f"  - {item}")
    else:
        print("PASS job-012 static flag")


if __name__ == "__main__":
    sys.exit(main())
