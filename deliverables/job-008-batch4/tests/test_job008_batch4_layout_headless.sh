#!/usr/bin/env bash
# Playable checkout only. Godot was not run in the delivery box.
set -euo pipefail
ROOT="${1:-.}"
godot --path "$ROOT/game" --headless --script res://tests/test_job008_batch4_layout_headless.gd
