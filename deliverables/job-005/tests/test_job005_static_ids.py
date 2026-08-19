#!/usr/bin/env python3
"""Godot-free static checks for job-005 wiring. Exit 0 on PASS."""
from __future__ import annotations

import json
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
    registry = read("game/scripts/ui/UiScreenRegistry.gd")
    main_gd = read("game/scripts/main/Main.gd")
    inventory = read("tools/screen-audit/screen-inventory.json")
    verifier = read("tools/screen-audit/verify-ui-audit-set.mjs")

    for screen_id in ("return_title_confirm", "boundary_shop"):
        if f'&"{screen_id}"' not in registry:
            fail(f"UiScreenRegistry missing {screen_id}")
        if f'"{screen_id}"' not in verifier:
            fail(f"verify-ui-audit-set missing {screen_id}")
        if f'"id": "{screen_id}"' not in inventory:
            fail(f"screen-inventory missing {screen_id}")

    if '"50_return_title_confirm.png"' not in inventory:
        fail("inventory screenshot for return_title_confirm must be 50_return_title_confirm.png")
    if '"51_boundary_shop.png"' not in inventory:
        fail("inventory screenshot for boundary_shop must be 51_boundary_shop.png")

    if "EXPECTED_SCREEN_COUNT = 51" not in verifier:
        fail("verify-ui-audit-set EXPECTED_SCREEN_COUNT is not 51")

    if '_push_ui_screen_overlay(&"return_title_confirm")' not in main_gd:
        fail("town title confirm must push return_title_confirm")
    town_fn = re.search(r"func _show_town_title_confirm\(\) -> void:\n(?:.*\n){8}", main_gd)
    if town_fn and '&"save_delete_confirm"' in town_fn.group(0):
        fail("town title confirm still reuses save_delete_confirm")
    if '_set_ui_screen_id(&"boundary_shop")' not in main_gd:
        fail("boundary shop must set boundary_shop id")
    render = re.search(r"func _render_boundary_shop\(\) -> void:\n(?:.*\n){8}", main_gd)
    if render and '_set_ui_screen_id(&"pause")' in render.group(0):
        fail("boundary shop still sets pause id")

    for token in (
        "ui_wiring_b2_options_language",
        "ui_wiring_b2_options_input",
        "_show_approved_b2_language_text",
        "_show_approved_b2_input_config",
        "ui_wiring_b1_save_load_delete",
        "_show_approved_save_delete_confirm",
        "func _show_run_history",
        "_record_run_history",
        '"run_history":',
    ):
        if token not in main_gd:
            fail(f"Main.gd missing required token: {token}")

    # Existing B2 tab labels must remain so test_ui_wiring_b2_runtime stays green.
    if '["画面", "音量", "ゲーム", "戻る"]' not in main_gd:
        fail("B2 options nav labels were changed; existing B2 tests would fail")

    if '"run_history"' not in registry:
        fail("run_history must remain in the registry")

    if errors:
        print("Job005StaticIds: FAIL")
        for item in errors:
            print(" -", item)
        return 1
    print("Job005StaticIds: PASS 51-id registry/inventory/audit + wiring tokens + ID split + run_history intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
