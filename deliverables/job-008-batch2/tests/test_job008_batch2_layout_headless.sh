#!/usr/bin/env bash
# Playable checkout only. Mirror / this box: Godot headless will fail.
# Transition asserts wait >=0.35s (job-005 lesson). This batch does not change
# transition seconds; it only touches shop hover, sell live labels, HUD leftover
# hide, and result-screen clip / z-order.
set -euo pipefail
ROOT="${1:-.}"
godot --path "$ROOT/game" --headless --script res://tests/test_job008_batch2_layout_headless.gd
