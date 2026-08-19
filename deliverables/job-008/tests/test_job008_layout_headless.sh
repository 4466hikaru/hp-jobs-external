#!/usr/bin/env bash
# Playable checkout only. Mirror / this box: Godot headless will fail.
set -euo pipefail
ROOT="${1:-.}"
godot --path "$ROOT/game" --headless --script res://tests/test_job008_layout_headless.gd
