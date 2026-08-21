#!/usr/bin/env python3
"""Godot-free static checks for job-013 behavior-unchanged patches. Exit 0 on PASS."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read_bytes(rel: str) -> bytes:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing {rel}")
        return b""
    data = path.read_bytes()
    if b"\r" in data:
        fail(f"{rel} contains CR (LF-only required)")
    return data


def load_json(rel: str) -> dict:
    raw = read_bytes(rel)
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{rel} JSON parse failed: {exc}")
        return {}


def extract_func(src: str, name: str) -> str | None:
    lines = src.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"func {name}"):
            start = i
            break
    if start is None:
        return None
    end = start + 1
    while end < len(lines) and not lines[end].startswith("func "):
        end += 1
    return "\n".join(lines[start:end])


def main() -> int:
    buffs = load_json("content/buffs.json")
    dungeons = load_json("content/dungeons.json")
    main_raw = read_bytes("game/scripts/main/Main.gd")
    main_gd = main_raw.decode("utf-8") if main_raw else ""

    caps = buffs.get("carryoverCaps", {})
    if caps.get("player.damageReduction") != 0.5:
        fail("carryoverCaps.player.damageReduction must be 0.5")
    expected_caps = {
        "player.damageMultiplier": 0.5,
        "player.maxHp": 100,
        "player.moveSpeedMultiplier": 0.25,
        "player.pickupRadiusMultiplier": 0.5,
        "player.cooldownMultiplier": -0.25,
        "player.xpGainMultiplier": 0.5,
        "player.damageReduction": 0.5,
    }
    for key, value in expected_caps.items():
        if caps.get(key) != value:
            fail(f"carryoverCaps.{key} expected {value} got {caps.get(key)}")
    extra = set(caps) - set(expected_caps)
    if extra:
        fail(f"unexpected carryoverCaps keys: {sorted(extra)}")

    # Neighbor name in preferredTargets must still exist; we did not retarget it.
    defensive = next((r for r in buffs.get("carryoverRules", []) if r.get("id") == "carryover.defensive"), {})
    if "player.damageReduction" not in defensive.get("preferredTargets", []):
        fail("defensive preferredTargets lost player.damageReduction")

    rule_rates = {r["id"]: r.get("baseCarryoverRate") for r in buffs.get("carryoverRules", [])}
    expected_rules = {
        "carryover.default": 0.1,
        "carryover.material_focused": 0.08,
        "carryover.defensive": 0.12,
        "carryover.offensive": 0.1,
        "carryover.growth": 0.11,
        "carryover.final": 0.13,
    }
    if rule_rates != expected_rules:
        fail(f"carryoverRules rates changed (tuning forbidden): {rule_rates}")

    items = dungeons.get("dungeons", [])
    if len(items) != 7:
        fail(f"expected 7 dungeons, got {len(items)}")
    patched = []
    unpatched = []
    for dungeon in items:
        did = dungeon.get("id")
        rule = dungeon.get("carryoverRuleId")
        has = "baseCarryoverRate" in dungeon
        if rule == "carryover.default":
            unpatched.append(did)
            if has:
                fail(f"{did} is default-rule and must not gain baseCarryoverRate")
        else:
            patched.append(did)
            if dungeon.get("baseCarryoverRate") != 0.1:
                fail(f"{did} baseCarryoverRate must be 0.1, got {dungeon.get('baseCarryoverRate')}")
    if len(patched) != 5:
        fail(f"expected 5 non-default dungeons patched, got {patched}")
    if unpatched != ["dungeon.border_catacomb", "dungeon.direwolf_den"]:
        fail(f"default dungeons unexpected: {unpatched}")

    if not main_gd:
        _report()
        return 1

    delta = extract_func(main_gd, "_dungeon_carryover_bonus_delta")
    if delta is None:
        fail("missing _dungeon_carryover_bonus_delta")
    elif 'var base_rate := float(rule.get("baseCarryoverRate", dungeon.get("baseCarryoverRate", 0.1)))' not in delta:
        fail("_dungeon_carryover_bonus_delta must read dungeon.baseCarryoverRate as fallback after rule")
    elif 'var base_rate := float(rule.get("baseCarryoverRate", 0.1))' in delta and "dungeon.get" not in delta:
        fail("old fallback line still present")

    clamp = extract_func(main_gd, "_clamp_carryover_target_value")
    if clamp is None:
        fail("missing _clamp_carryover_target_value")
    else:
        if "content.get(\"buffs\", {}).get(\"carryoverCaps\", {})" not in clamp:
            fail("clamp must still read carryoverCaps")
        if "player.cooldownMultiplier" not in clamp:
            fail("clamp CD neighbor branch missing")
        # Must not have grown a special-case for damageReduction (JSON table is the patch).
        if "damageReduction" in clamp:
            fail("clamp function itself must not special-case damageReduction; cap table is JSON")

    load = extract_func(main_gd, "_load_content")
    if load is None:
        fail("missing _load_content")
    elif "buffs.json" in load:
        fail("_load_content must not start loading buffs.json (that would change maxHP/move caps)")

    # Neighbor functions must still exist (not a similarly-named edit).
    for name in (
        "_carryover_value_for_target",
        "_carryover_rule_by_id",
        "_carryover_targets_for_rule",
        "_apply_carryover_target_to_run",
    ):
        if extract_func(main_gd, name) is None:
            fail(f"missing neighbor {name}")

    func_count = len(re.findall(r"^func ", main_gd, flags=re.M))
    if func_count != 1518:
        fail(f"func count changed: {func_count} (expected 1518, no new funcs)")

    _report()
    return 1 if errors else 0


def _report() -> None:
    if errors:
        print("FAIL job-013 static checks")
        for item in errors:
            print(f" - {item}")
    else:
        print("PASS job-013 static checks")


if __name__ == "__main__":
    sys.exit(main())
