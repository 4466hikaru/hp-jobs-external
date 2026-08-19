# 正直な申告 (job-008 第1バッチ)

日時: 2026-08-19 14:57 JST (UTC 05:57)

## 実施した読取

- clone なし。`gh api repos/4466hikaru/hp-game-share/contents/...` で live HEAD を再読取
- live Main.gd blob `cf895716` (25230行)。作業用 extract `/tmp/job008-orig` は job-005 適用後 (25411行)
- Batch2/3 live blob は extract と一致 (`a3d37add` / `fa556219`)
- 金枠経路: `_show_menu_shell` / `_kit2_menu_panel_style` / `_image2_panel_style` / `_layout_ui` の menu_size 分岐
- Stage4MassBatch2 world_tile_map、Batch3 equipment_slots、`_show_approved_b2_pause_menu`、`_show_scene_log_overlay`

## 実行できた検証

- 5 枚の diff が live HEAD と job-005 適用後の両方に `git apply --check` OK
- `tests/test_job008_static_layout.py` が job-005+008 ツリーで PASS
- job-005 契約トークン (`画面/音量/ゲーム/戻る`, `_show_run_history`, `boundary_shop`, `return_title_confirm`) が 008 後も残る（job-005 適用後ツリー）

## 実行できなかった検証

- Godot headless すべて（本箱に Godot なし、ミラーは asset-stripped）
- 実画面での金線 x 再計測（job-004 PNG の数値をレイアウト定数から逆算した）
- 07 shop / 08 sell `[仮]` / 25-26 HUD / 33 clear / 34 game_over の修正後見た目
- title 左縦メニューがコードの leftover か PNG 焼き込みかのピクセル確認

「既存テスト回帰ゼロ」は静的契約の維持までしか言えない。

## 006 作り直し (2026-08-19 17:46 JST)

前回はタイトルを70pxにした分を下へ足し、下端 646→672。指摘と逆だった。

今回: リストを上へ。title Rect2(430, 566, 420, 70) bottom 636、下マージン 84px（元 74）。設定 hex y=400 h=70 は残置。001-004 hunk 未変更。

検証:
- 5枚とも CR=0（file/python）。`git apply --check` が live HEAD (blob cf895716) に通った（gh api で /tmp に配置。hp-game-share は clone していない）
- 静的テストのポーズ座標チェックは PASS。job-005 契約トークン欠落は live HEAD 単体では従来どおり（job-005 先適用が必要）
- Godot 未実行。遷移 0.35s 未変更。
