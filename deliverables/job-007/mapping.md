# mapping.md — job-007 batch1 rematch

| file | 対応カンプ画面 | 部位 | 参照crop |
|---|---|---|---|
| startup_backdrop_v001.png | 03_タイトル | 起動/タイトル全画面背景 | crop_startup_backdrop.png (03 全画面) |
| startup_vignette_v001.png | 03_タイトル | 周辺減光オーバーレイ（コード生成） | なし（code-made） |
| main_menu_frame_v001_c32.png | 03_タイトル | メインメニュー縦枠（カンプに箱枠なし・発明） | crop_title_menu_region.png |
| save_slot_frame_v001_c24.png | 05_セーブ選択 | セーブスロット横枠 | crop_save_slot_frame.png |
| confirm_modal_frame_v001_c40.png | 06_セーブ削除（04は名前入力のため不使用） | 確認モーダル枠 | crop_confirm_modal_frame.png |
| age_gate_frame_v001_c48.png | 02_年齢 | 年齢確認枠 | crop_age_gate_frame.png |
| legal_scroll_frame_v001_c16.png | 09_クレジット | リーガル/規約スクロール枠 | crop_legal_scroll_frame.png |
| ruby_primary_button_v001_c16.png | 05_セーブ選択 | ルビー主ボタン（通常） | crop_ruby_primary_button.png |
| ruby_primary_button_v001_focus_c16.png | 05_セーブ選択 | ルビー主ボタン（フォーカス） | crop_ruby_primary_button_focus.png（通常と同じ画素） |
| iron_secondary_button_v001_c16.png | 05_セーブ選択 | 鉄二次ボタン（通常） | crop_iron_secondary_button.png |
| iron_secondary_button_v001_focus_c16.png | （03/05にフォーカス鉄なし） | 鉄二次ボタン（フォーカス・派生） | crop_iron_secondary_button.png を流用 |

raw → final:
- raw/startup_backdrop.png → startup_backdrop_v001.png
- raw/main_menu_frame.png → main_menu_frame_v001_c32.png
- raw/save_slot_frame.png → save_slot_frame_v001_c24.png
- raw/confirm_modal_frame.png → confirm_modal_frame_v001_c40.png
- raw/age_gate_frame.png → age_gate_frame_v001_c48.png
- raw/legal_scroll_frame.png → legal_scroll_frame_v001_c16.png
- raw/ruby_primary_button.png → ruby_primary_button_v001_c16.png
- raw/ruby_primary_button_focus.png → ruby_primary_button_v001_focus_c16.png
- raw/iron_secondary_button.png → iron_secondary_button_v001_c16.png
- raw/iron_secondary_button_focus.png → iron_secondary_button_v001_focus_c16.png
- vignette: コード生成（Imagineなし）
