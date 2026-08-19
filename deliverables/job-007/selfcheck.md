# selfcheck.md — job-007 batch1 rematch

規格6項目: 1透過PNG / 2境界色フチゼロ(全色相) / 3余白8px / 4_9スライス(ファイル名_cN) / 5命名_v001 / 6サイズ(2x目標)

検出器: `/workspace/job007/scripts/check_parts.py`（書き換えなし）。校正は known-NG で FAIL 9/11 が必須PASS。

| file | 1透過PNG | 2色フチゼロ | 3余白8px | 4_9スライス | 5命名 | 6サイズ |
|---|---|---|---|---|---|---|
| startup_backdrop_v001.png | Yes (opaque OK: 全面背景例外) | Yes (exempt) | Yes (N/A full-bleed) | Yes (N/A 非フレーム) | Yes | Yes 2560x1440 RGB |
| startup_vignette_v001.png | Yes | Yes | Yes (N/A full-bleed) | Yes (N/A 非フレーム) | Yes | Yes 2560x1440 RGBA |
| main_menu_frame_v001_c32.png | Yes | Yes | Yes (min_opaque_margin=8) | Yes (filename _c32; 実測は自信なし→ファイル名維持) | Yes | Yes 640x960 |
| save_slot_frame_v001_c24.png | Yes | Yes | Yes | Yes (filename _c24; 実測 top→straight≈8px 低信頼→ファイル名維持) | Yes | Yes 2160x400 |
| confirm_modal_frame_v001_c40.png | Yes | Yes | Yes | Yes (filename _c40; 実測 left→straight≈40px 参考、自信限定→ファイル名維持) | Yes | Yes 1440x840 |
| age_gate_frame_v001_c48.png | Yes | Yes | Yes | Yes (filename _c48; スパイクのため実測不安定→ファイル名維持) | Yes | Yes 1560x960 |
| legal_scroll_frame_v001_c16.png | Yes | Yes | Yes | Yes (filename _c16; 裂け縁のため実測不安定→ファイル名維持) | Yes | Yes 1280x1040 |
| ruby_primary_button_v001_c16.png | Yes | Yes | Yes | Yes (filename _c16; 実測 top≈14–16px 参考→ファイル名維持) | Yes | Yes 480x112 |
| ruby_primary_button_v001_focus_c16.png | Yes | Yes | Yes | Yes (filename _c16; 同上) | Yes | Yes 480x112 |
| iron_secondary_button_v001_c16.png | Yes | Yes | Yes | Yes (filename _c16; 実測≈16px 参考) | Yes | Yes 480x112 |
| iron_secondary_button_v001_focus_c16.png | Yes | Yes | Yes | Yes (filename _c16; 同上) | Yes | Yes 480x112 |

## 完成定義 Yes/No

- [x] Yes — 11ファイルが規格6項目PASS（selfcheck_log.txt 実測 + calibration_known_ng.txt 校正証跡）
- [x] Yes — 部位ごとの並置画像（compare/*_vs_crop.png）。vignette は code-made のため crop 並置なし
- [x] Yes — タイトル画面の合成プレビュー1枚（title_preview.png）
- [x] Yes — 正直な申告リスト（本ファイル）

## 検出器校正サマリ（known-NG FAIL = 検出器の PASS）

`job007/scripts/check_parts.py --dir job007/known_ng` → **2 OK, 9 FAIL / 11 files**（exit 1）。

- FAIL: age_gate_frame（fringe 5594, magenta=3401/purple=1660 他）, confirm, save_slot, main_menu, legal, ruby×2, iron×2
- OK: startup_backdrop (excepted), startup_vignette
- 証跡: `calibration_known_ng.txt`（scripts の校正を deliverables に複製）

finals: **11 OK, 0 FAIL**（全 framed の fringe_count=0）。ログ: `selfcheck_log.txt`

## 正直な申告

- main_menu_frame は 03_title に箱枠が無い（テキスト + ルビー菱形のみ）。本ファイルはタイトルの金属言語から最小限に発明した縦枠。CROP_NOTES も「boxed frame を発明するな」と注記するが、発注対象に main_menu_frame が残っているため枠を納品し、発明である旨をここに書く。
- Imagine ソースはすべて 1536x1024（16:9）。切り出し後に目標キャンバス (target-16) へ LANCZOS で引き伸ばした。アスペクト不一致は引き伸ばしで吸収。
- 9スライス `_cN` はファイル名指定値。画素から「bbox角→最初の長い直線辺」を測ったが信頼が低い（引き伸ばし後・装飾非矩形）。**サイレントに _cN は変更していない**。
- startup_vignette_v001.png は Imagine ではなくコード生成。黒ラジアル、中央 alpha 0、四隅 alpha=220。
- iron_secondary_button_v001_focus_c16.png は 03/05 に固有cropが無い。Imagine の focus 兄弟を処理した派生。金は足していない。
- 03/05 の framed ruby は発光1状態のみ。ruby 通常と focus の参照cropは同一画素（CROP_NOTES）。生成側は別 Imagine を通常/focus として処理。
- leftover mismatches vs crop:
  - save_slot 生成は **2パネル**（中央1本割り）。crop は **3ゾーン**（左エンブレム / 中央テキスト / 右ボタン）。
  - legal 生成は左右裂け + 上下ほぼ直線。crop も左右裂けが主（4辺裂けではない）。内側に罫線16本があり、crop のクレジット本文レイアウトとは中身が違う（文字は入れていないが罫が残る）。
  - age_gate 生成はスパイク枠で 18+ 円形クレスト/スカルが無い。crop より装飾が単純で、目標 1560x960 は crop 780x610 の2倍より横長。
  - confirm 生成は二重金線 + 天の菱形のみ。crop（06）は棘/中点突起 + ヘッダ/警告テキスト入り。
  - ruby 生成は左右ダイヤ付き赤枠。crop は「ロード」文字 + 赤グロー付き。デフリンジで外側グローは落ちている。
  - iron 生成は面取り四角。crop はノッチ角 + 「削除」文字。focus は通常の明るいリム派生ではなく Imagine 兄弟。
- デフリンジ後、検出器（chroma≥22 の境界も落とす）を通すため、最外周1–2pxの金属ハイライトは暗色内面色に置換した。外縁の金/ルビー光沢は落ちている。
- raw は RGB の焼き込みチェッカー。縁から洪水でキーし本物の RGBA にしてから `defringe.py` → サイズ合わせ。
- title_preview は 03_title（1280x720）に vignette（弱）と左の main_menu_frame、下部に ruby を1つ置いた配置プレビュー。追加画面は作っていない。
