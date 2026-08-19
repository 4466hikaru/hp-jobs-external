# selfcheck.md — job-006 batch1

規格6項目: 1透過PNG / 2白フチゼロ / 3余白8px / 4_9スライス(ファイル名_cN) / 5命名_v001 / 6サイズ(2x目標)

| file | 1透過PNG | 2白フチゼロ | 3余白8px | 4_9スライス | 5命名 | 6サイズ |
|---|---|---|---|---|---|---|
| startup_backdrop_v001.png | Yes (opaque OK: 全面背景例外) | Yes | Yes (N/A full-bleed overlay/bg) | Yes (N/A 非フレーム) | Yes | Yes |
| startup_vignette_v001.png | Yes | Yes | Yes (N/A full-bleed overlay/bg) | Yes (N/A 非フレーム) | Yes | Yes |
| main_menu_frame_v001_c32.png | Yes | Yes | Yes | Yes (filename _c32; 画素実測せずファイル名推定) | Yes | Yes |
| save_slot_frame_v001_c24.png | Yes | Yes | Yes | Yes (filename _c24; 画素実測せずファイル名推定) | Yes | Yes |
| confirm_modal_frame_v001_c40.png | Yes | Yes | Yes | Yes (filename _c40; 画素実測せずファイル名推定) | Yes | Yes |
| age_gate_frame_v001_c48.png | Yes | Yes | Yes | Yes (filename _c48; 画素実測せずファイル名推定) | Yes | Yes |
| legal_scroll_frame_v001_c16.png | Yes | Yes | Yes | Yes (filename _c16; 画素実測せずファイル名推定) | Yes | Yes |
| ruby_primary_button_v001_c16.png | Yes | Yes | Yes | Yes (filename _c16; 画素実測せずファイル名推定) | Yes | Yes |
| ruby_primary_button_v001_focus_c16.png | Yes | Yes | Yes | Yes (filename _c16; 画素実測せずファイル名推定) | Yes | Yes |
| iron_secondary_button_v001_c16.png | Yes | Yes | Yes | Yes (filename _c16; 画素実測せずファイル名推定) | Yes | Yes |
| iron_secondary_button_v001_focus_c16.png | Yes | Yes | Yes | Yes (filename _c16; 画素実測せずファイル名推定) | Yes | Yes |

## 実測ログ

| file | size | mode | has_alpha | white_fringe_count | min_margin | magenta_left |
|---|---|---|---|---|---|---|
| startup_backdrop_v001.png | 2560x1440 | RGB | False | 0 | 0 | 0 |
| startup_vignette_v001.png | 2560x1440 | RGBA | True | 0 | 0 | 0 |
| main_menu_frame_v001_c32.png | 640x960 | RGBA | True | 0 | 8 | 0 |
| save_slot_frame_v001_c24.png | 2160x400 | RGBA | True | 0 | 8 | 0 |
| confirm_modal_frame_v001_c40.png | 1440x840 | RGBA | True | 0 | 8 | 0 |
| age_gate_frame_v001_c48.png | 1560x960 | RGBA | True | 0 | 8 | 0 |
| legal_scroll_frame_v001_c16.png | 1280x1040 | RGBA | True | 0 | 8 | 0 |
| ruby_primary_button_v001_c16.png | 480x112 | RGBA | True | 0 | 8 | 0 |
| ruby_primary_button_v001_focus_c16.png | 480x112 | RGBA | True | 0 | 8 | 0 |
| iron_secondary_button_v001_c16.png | 480x112 | RGBA | True | 0 | 8 | 0 |
| iron_secondary_button_v001_focus_c16.png | 480x112 | RGBA | True | 0 | 8 | 0 |

## 正直な申告

- startup_vignette_v001.png は Imagine ではなくコード生成（黒ラジアル、中央 alpha 0、端〜角 ~220）。
- iron_secondary_button_v001_focus_c16.png は固有 Imagine ではなく iron 通常から内側リムをわずかに明るくした派生。金は入れていない。
- Imagine ソースは全て 1536x1024。目標サイズへの LANCZOS 再配置は妥協。切り出し後アスペクトを目標キャンバスへ引き伸ばしている。
- 9スライスコーナーpx（_c16/_c24/_c32/_c40/_c48）はファイル名指定値であり、画素から実測していない。
- 白フチは透過境界1-2pxの明色を暗色化または透過にしている。外縁の金属ハイライト1-2pxは落ちている。
- 確認モーダル目標サイズは発注の ~1440x840 を採用。
