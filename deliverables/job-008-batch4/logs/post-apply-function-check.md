# post-apply function check (refreshed hp-game-share HEAD 3fd5cf040647)

- git apply --check 020 isolated: OK
- git apply --check 024 isolated: OK
- git apply 020 then 024: OK
- git apply 024 then 020: OK
- _add_character_portrait_card body identical before/after 020+024: YES
- _add_info_card gained alignment param: YES
- _show_approved_save_delete_confirm centers target_slot_01..03: YES
- _show_approved_b2_options keeps language/input rows: YES
- UiHoverOverlay.gd not in these two patches (hook already on HEAD): YES
- CR bytes in both diffs: 0
- Godot/gdparse: not available on this box
- static test on applied tree: PASS
- static test on unpatched tree: FAIL (expected)
