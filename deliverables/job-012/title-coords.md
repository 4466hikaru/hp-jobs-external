# job-012 title (03_title) 実測座標

Source mockup: `/workspace/redraw/ideal0819/03_title.png` (1280x720 RGBA).
Measured with PIL/numpy. Preview `title_screen_composite_preview.png` is reference only; カンプ wins.

Copied from `/workspace/job012/title/NOTES.md`.

## Measurement table (1x px)

| element | x | y | w | h | how measured |
|---|---:|---:|---:|---:|---|
| viewport / backdrop dest | 0 | 0 | 1280 | 720 | mockup size; backdrop 2560x1440 (2x) half-size dest |
| vignette dest | 0 | 0 | 1280 | 720 | vignette 2560x1440 (2x); alpha>8 inset 17px @2x |
| title plaque / main_menu_frame dest | 340 | 16 | 600 | 300 | 2x 1200x600 -> 1x half; x=(1280-600)/2. Crown lum>60 y=19..79 x=501..777. Burgundy well x=354..924 y=63..275 (571x213) |
| title wordmark label | 400 | 88 | 480 | 72 | inside burgundy well; code-drawn (not baked) |
| title subtitle label | 470 | 200 | 340 | 28 | PIL band y=200..279 x=480..799 |
| button 1 はじめから (focus) | 28 | 376 | 264 | 40 | lum>70 band y=375..411; chrome left diamond x=28; underline y=410..411 x=58..216 (159 red px) |
| button 2 つづきから | 28 | 428 | 264 | 40 | lum>100 y=426..454 x=75..264; pitch from item1 ~52px |
| button 3 セーブ／ロード | 28 | 480 | 264 | 40 | lum>100 y=479..506 x=75.. |
| button 4 設定 | 28 | 532 | 264 | 40 | lum>100 y=534..557 x=37..256 |
| button 5 クレジット | 28 | 584 | 264 | 40 | lum>100 y=586..611 x=77.. |
| footer 決定/戻る (existing chrome, not placed) | 27 | 684 | 139 | 16 | lum>80 x=27..165 y=684..699 |

Shared button column x=28 w=264 from item1 focus chrome. Dest h=40 (not 1x 250x70) so ruby 500x139 does not overlap the measured 52px pitch.

## NinePatch mapping

`main_menu_frame_c48_v001.png`: 1200x600, `_c48` = patch 48 in **texture px**.
Godot `NinePatchRect.patch_margin_*` is texture-space -> 48 (not 24).
Dest 600x300 (half). Content pad assumption 16px @2x -> 8px @1x.

## Node names (flag ON)

| node | rect |
|---|---|
| TitleImage2Layout | 0,0 1280x720 |
| StartupBackdrop | 0,0 1280x720 |
| StartupVignette | 0,0 1280x720 |
| MainMenuFrame | 340,16 600x300 patch 48 |
| TitleWordmark | 400,88 480x72 |
| TitleSubtitle | 470,200 340x28 |
| ui_text_title_main_actions_01..05 | 28,376 / 428 / 480 / 532 / 584 ; 264x40 |

iron_secondary unused (mockup normal rows are unframed text). Normal style is empty; focus/hover/pressed use ruby.
