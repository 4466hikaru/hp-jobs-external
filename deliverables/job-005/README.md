# job-005 納品: 死に画面3枚の復活配線 + 画面ID使い回し分離

対象コード: `https://github.com/4466hikaru/hp-game-share` (`main`、2026-08-19 時点を gh API で読取)。  
CloudAgent は GitHub 未再接続で起動失敗。clone はせず、`gh api` でファイルを読んで diff を書いた。  
hp-game-share は asset-stripped のコードレビューミラーであり、Godot では遊べない。

## 完成定義 (Yes/No)

- [Yes] B2設定から言語・テキスト速度と入力設定に到達でき、値の変更が保存される  
  `_show_approved_b2_options()` に既存カテゴリ列を壊さない「言語・テキスト」「入力設定」導線を追加。到達先は既存 `_show_language_text_settings` / `_show_input_config`。B2 時は Stage4MassBatch6 の approved view を使い、文字速度・自動送り・キー再割当/初期化は既存 save 経路のまま。
- [Yes] セーブ画面から削除→確認→削除実行が動き、誤って町→タイトル確認と混ざらない  
  B1 save/load に `ui_wiring_b1_save_load_delete` を追加し `save_delete_confirm` へ配線。町→タイトルは新ID `return_title_confirm`。run_state も元から別 (`STATE_SAVE_DELETE_CONFIRM` / `STATE_TOWN_TITLE_CONFIRM`)。
- [Yes] pause と境界ショップが別IDになり、既存の両機能が回帰なしで動く  
  `_render_boundary_shop()` の `_set_ui_screen_id(&"pause")` を `&"boundary_shop"` に変更。`_show_pause_menu()` は従来どおり `&"pause"`。
- [Partial] 追加・変更テストのログ同梱、既存テスト回帰ゼロのログ同梱  
  静的チェックと `verify-ui-audit-set` の node:test 4件は PASS。Godot headless (B1/B2 runtime / 本ジョブの到達+戻りテスト) はミラー/本箱では未実行。
- [Yes] 正直な申告リスト (本 README「ミラーでは検証できなかった点」と PR 本文)

run_history は入口を追加していない。参照 (`_show_run_history` / `_record_run_history` / registry) は残してある。

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート** (`game/scripts/main/Main.gd` がある場所)。`hp-jobs-external` ではない。

```bash
# 1. パッチを本体 repo へコピーして適用
git checkout -B job/005-screen-wiring
git apply --check path/to/hp-jobs-external/deliverables/job-005/patches/*.diff
git apply path/to/hp-jobs-external/deliverables/job-005/patches/*.diff

# 2. 新規 headless テストを配置
cp path/to/hp-jobs-external/deliverables/job-005/tests/test_job005_screen_wiring.gd game/tests/

# 3. 静的チェック (Godot 不要)
python3 path/to/hp-jobs-external/deliverables/job-005/tests/test_job005_static_ids.py .
node --test tools/screen-audit/tests/verify-ui-audit-set.test.mjs

# 4. Godot headless (プレイ可能 checkout のみ)
godot --path game --headless --script res://tests/test_job005_screen_wiring.gd
godot --path game --headless --script res://tests/test_ui_screen_registry.gd
godot --path game --headless --script res://tests/test_ui_wiring_b1_runtime.gd
godot --path game --headless --script res://tests/test_ui_wiring_b2_runtime.gd
```

`git apply` が拒否したら `patch -p1 < patches/00N-....diff` を1枚ずつ。  
適用後に screen-audit を回すと `50_return_title_confirm.png` と `51_boundary_shop.png` が新しいキャプチャ対象になる (`SCREEN_AUDIT_DEFAULT_IDS := UiScreenRegistry.ORDERED_SCREEN_IDS`)。歴史的 01-49 の番号は維持 (末尾 append)。

## パッチ一覧

| file | 内容 |
|---|---|
| `patches/001-uiscreenregistry-new-ids.diff` | `return_title_confirm` (M01 / danger_modal), `boundary_shop` (M05) を末尾追加 |
| `patches/002-main-screen-wiring.diff` | B2 options 統合、B1 削除ボタン、ID分離、audit 分岐、B2 language/input view |
| `patches/003-screen-inventory-new-ids.diff` | 50/51 を inventory に追加 |
| `patches/004-verify-ui-audit-set.diff` | canonical IDs と件数 51 |
| `patches/005-verify-ui-audit-set-test.diff` | node:test の期待件数を 51 に (元ファイルは 46 のまま放置されていた) |
| `patches/006-test-ui-screen-registry.diff` | registry 単体テストを 51 件に |

## 実装メモ

- B2 options の nav は従来どおり `画面 / 音量 / ゲーム / 戻る` (既存 `test_ui_wiring_b2_runtime.gd` 契約)。言語・入力は同じ設定本文カラム下のカテゴリ導線。
- 言語/入力の中身は新規デザインを作らず、既存 Stage4MassBatch6 の `options_language_text` / `input_config` layout を B2 から開く。
- B1 save/load の slot_actions は1枠のまま。削除は既存 back hotspot と同じ「追加アクション」様式。
- input_config の B2 view は approved 16 スロットに合わせ、先頭 8 action の key/joy を bind。残り 2 spec (`scene_auto`, `scene_hide`) は legacy shell 側に残る。

## ミラーでは検証できなかった点

- Godot 実行。B1/B2 runtime の既存テストと本ジョブの到達+戻りテストは未実行。
- 実機での設定保存 (user://save.json)、キー再bind、セーブ削除のファイル I/O。
- approved PNG / フォントが無いため B2 `build_view` の見た目と hover。
- screen-audit 実キャプチャ (`50_*.png` / `51_*.png` は未撮影)。
- 境界ショップの playtest 短絡 (`playtest_enabled and not battle_profile_ui_audit`) が audit 以外の経路で ID を落とさないことの実行確認。audit 分岐は `_render_boundary_shop()` を直接呼ぶ。

## 要判断

1. B2 言語/入力を options 本体の 4 行カテゴリにインラインするか、今回どおり専用 approved 画面へ遷移するか。4 nav 枠を増やさず既存テストを守るため遷移を選んだ。
2. B2 input の 16 スロットに 10 spec をどう載せるか。今回は先頭 8。残り 2 を足すなら layout 追加が要る。
3. `boundary_shop` の master を M05 (ダンジョン境界) にした。M03 (shop) や M06 (pause と同じ HUD) の方がよければ変更する。
4. 新規 audit PNG は未撮影。番号は 50/51 で 01-49 を動かしていない。
5. 町 B1 の「戻る」は地域/ワールドマップへ行っており、タイトル確認はキーボード back 経路。タイトル確認を町 B1 ボタンにも出すかは別判断。
