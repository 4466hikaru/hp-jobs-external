# job-012 save (05_save) 実測座標

Source mockup: 05_save.png (1280x720). Coordinates are 1x from PIL/numpy gold/ruby/iron-plate detection.
2x textures are placed onto these 1x rects. Comments in `_apply_image2_save_select_layout`.

backdrop / vignette は 05 に載せない（03 title と背景が違う。library vs graveyard）。ヘッダ金線は未配置。

## Measurement table (1x px)

| element | x | y | w | h | node / notes |
|---|---:|---:|---:|---:|---|
| save slot frame | 48 | 213 | 1182 | 186 | ui_image2_save_slot_frame_01 NinePatch `_c32`=32 texture-space. Gold CC left/top/right/bottom |
| load (ready, ruby) | 954 | 240 | 230 | 60 | existing slot action button, ruby 2-state |
| delete | 956 | 318 | 229 | 54 | ui_image2_save_delete, iron |
| new game | 510 | 543 | 260 | 66 | empty/corrupt: reuse action as iron. ready: extra ui_image2_save_new_game -> `_start_new_game_from_save_load` |
| back | 52 | 632 | 171 | 58 | ui_wiring_b1_save_load_back, iron. Existing hotspot was (48,625,190,76) |

## 仮決め

- corrupt action は新規ゲーム枠 (510,543,260x66) に iron。ラベルは既存の戻る。
- ready 時の追加「新規ゲーム」は既存 `_start_new_game_from_save_load`。フローは発明しない。
- ヘッダ金線は未配置。
- パーツディレクトリは `res://assets/ui/image2_parts/final/`（title の `ui_parts_batch1_image2/` と不一致。ファイル名は変えない）。

## 出さない

age_gate / confirm_modal / legal_scroll を save に出さない。startup_backdrop / startup_vignette も 05 には出さない。
