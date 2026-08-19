#!/usr/bin/env bash
# Apply the job-005 patches to a playable hp-game checkout, then:
#   godot --path game --headless --script res://tests/test_job005_screen_wiring.gd
# The asset-stripped hp-game-share mirror cannot run this.
set -euo pipefail
echo "Job005 headless wrapper: copy tests/test_job005_screen_wiring.gd to game/tests/ and run with Godot 4.6. See README."
exit 0
