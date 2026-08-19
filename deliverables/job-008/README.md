# job-008 納品: UI欠陥コード修正（第1バッチ）

対象コード: `https://github.com/4466hikaru/hp-game-share` (`main` HEAD blob `cf895716` / Main.gd 25230行、2026-08-19 を gh API で読取)。  
clone なし。パッチは live HEAD に `git apply` できることを確認した。job-005 適用後ツリーにも同じパッチが当たる。  
hp-game-share は asset-stripped のコードレビューミラーであり、Godot では遊べない。

対象リスト: 同梱の `triage.md`（やる 61 / やらない 29 / 全指摘 90）。本バッチは系統金枠 + 根拠のある HIGH のみ。

## 完成定義 (Yes/No)

- [Yes] 対象リスト (`triage.md`) を公開ブランチに置いた
- [Yes] 系統金枠の内側縦線: `MENU_PANEL_FRAME_INSET := 72.0` で 9-slice / kit2 / UiSkin 経由の content_margin をクランプ。`_menu_content_width` も 2*72 を引く
- [Partial] ユニーク HIGH: 01 title / 18 scene_log / 14 equipment_slots / 32 pause / 48 world_tile_map はコード修正。07 shop / 08 sell `[仮]` / 25-26 HUD / 33 clear / 34 game_over は未修正（下記ギャップ）
- [Partial] テスト: 静的 Python は PASS。Godot headless はミラー/本箱では未実行
- [Yes] 正直な申告（本 README と `logs/honest-unverified.md`）

PR はまだ開いていない。第1バッチとしては系統金枠 + 直せる HIGH まで。残り HIGH は次コミット。

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート** (`game/scripts/main/Main.gd` がある場所)。`hp-jobs-external` ではない。

job-005 を先に当ててから本バッチを当てる（静的テストの job-005 契約トークン用）。本バッチの diff 自体は未適用の hp-game-share HEAD にも当たる。

```bash
# 0. job-005 を先に適用（未適用なら）
git apply --check path/to/hp-jobs-external/deliverables/job-005/patches/*.diff
git apply path/to/hp-jobs-external/deliverables/job-005/patches/*.diff

# 1. job-008 パッチ
git apply --check path/to/hp-jobs-external/deliverables/job-008/patches/*.diff
git apply path/to/hp-jobs-external/deliverables/job-008/patches/*.diff

# 2. テスト配置
cp path/to/hp-jobs-external/deliverables/job-008/tests/test_job008_layout_headless.gd game/tests/
cp path/to/hp-jobs-external/deliverables/job-008/tests/test_job008_layout_headless.sh game/tests/

# 3. 静的チェック (Godot 不要)
python3 path/to/hp-jobs-external/deliverables/job-008/tests/test_job008_static_layout.py .

# 4. Godot headless (プレイ可能 checkout のみ。遷移待ち 0.35s 込み)
godot --path game --headless --script res://tests/test_job008_layout_headless.gd
```

`git apply` が拒否したら番号順に `patch -p1 < patches/00N-....diff`。

## パッチ一覧

| file | 対象 triage 行 / 画面 | 内容 |
|---|---|---|
| `patches/001-gold-frame-content-inset.diff` | 系統金枠。高: 16 gallery / 19 run_history / 21 language (legacy) / 22 input (legacy) / 38 credits / 40 age_gate / 42 save_delete。中: 43 motion_check / 49 system_menu。39 boot は 940 分岐のため中信頼。44 adult / 47 new_game は `_reskin_panel_style(26)` 上書きのため未カバー。23/24 (x≈436) は `StyleBoxEmpty` のため未カバー | `MENU_PANEL_FRAME_INSET=72`。64px 9-slice 内側線の直後から本文。720 中央: left=280 → 本文 352。580 左寄せ: left≈90 → 本文 162 |
| `patches/002-hide-leftover-adv-and-shell.diff` | 1 (01_title 二系統UI) / 35 (18_scene_log ADV漏れ) | `_layout_ui` が B1/B2/B3 approved view 中は `menu_panel` を隠す。scene_log 中は ADV overlay を隠してから layout |
| `patches/003-world-tile-map-header-width.diff` | 87 (48_world_tile_map 省略) | 地点 156 / 危険度 136 / 調査 52 / 黒貨 118。resource_hud 下地 790×490。4欄は残す（情報削除なし） |
| `patches/004-equipment-slots-label-clip.diff` | 27 (14_equipment_slots ラベル欠け) | slot_cards を y=500 h=36 へ（旧 y=535 h=28 で下半分クリップ） |
| `patches/006-pause-hex-frames-margin.diff` | 57-58 (32_pause 設定/タイトルへ) | 設定の下に既存 hex (`pause_options_button`) を TextureRect で敷く（新ボタン/ヒット無し、z=-1）。タイトルへを 70px・下端 672 |

005 は欠番。title hide は 002 に同居（隣接 hunk）。

## 系統金枠の結論（仮説ではなく読んだ結果）

共有描画: `_show_menu_shell` → `_kit2_menu_panel_style` → `_image2_panel_style`。

現状 live の `_image2_panel_style` は **先に `UiSkin.panel_style` (StyleBoxFlat)** を返し、64px 9-slice は fallback。job-004 キャプチャの内側金縦線は 9-slice の ornament（panel.x+64）に一致する。

| クラスタ | layout | 内側線 | 72px 本文開始 |
|---|---|---|---|
| default 720×560 中央 | left=280 | ≈344 ≈ x350 | 352 |
| SYSTEM/CREDITS/SAVE_DELETE/MOTION 580 左 | left≈90 | ≈154 ≈ x160 | 162 |
| GALLERY 等 940 左 | left≈70 | ≈134（job-004 は x160 扱い） | 142 |
| BOOT/ADULT/NEW_GAME 940 中央 | left=170 | 9-slice なら ≈234。ADULT/NEW_GAME は 2px reskin | 変更せず |

gallery / run_history / credits / age_gate / save_delete / motion / system は今も `_show_menu_shell`。  
21/22 は job-005 後 approved B2 view（`menu_panel` 非表示）。job-004 の「言語設定」「現: A」は **legacy shell** のキャプチャ。001 は legacy 経路を直す。  
44/47 は `_reskin_panel_style(..., 26.0, 2, 6)` が上書き。26px のまま（940 契約を壊さない）。

## ユニーク HIGH の Yes/No

| 画面 | 結果 | メモ |
|---|---|---|
| 01_title 二系統UI | Yes (コード) | leftover `menu_panel` を B1/B2/B3 で隠す。左縦メニューが approved PNG に焼き込みなら残る |
| 07_shop 二重選択枠 | No | B3 approved shop。focus/hover の二重は1行では特定できず未着手 |
| 08_sell_inventory `[仮]` | No | GDScript に `[仮]` 無し。approved PNG 焼き込みの公算。clear_rect 未計測 |
| 14_equipment_slots ラベル欠け | Yes | ラベルをカード下端より上へ |
| 16_gallery 金枠 | Yes (001) | legacy shell。approved Batch5 経路があるが `_show_gallery` は shell |
| 18_scene_log ADV漏れ | Yes | `_effective_run_state()` が SCENE_VIEW のままなので layout が ADV を再表示していた |
| 19 / 21legacy / 22legacy / 38 / 40 / 42 | Yes (001) | 上記クラスタ |
| 25 / 26 HUD 二重 | No | `Main._draw` は HUD を CombatHudSlots に委譲済み。二重の再現源を未特定 |
| 32_pause | Yes | 既存 hex アセットを流用。新規デザイン無し |
| 33_clear | No | ボタン枠重なり + 黒マスク。未着手 |
| 34_game_over | No | 文字左上 + 赤装飾。未着手 |
| 39_boot_splash | Partial | 940 分岐。x≈350 と一致しない。001 は kit2 margin のみ |
| 44 / 47 | No | reskin 2px 上書きを温存 |
| 48_world_tile_map | Yes | 箱幅のみ。駒の破線選択はやらない |

## ミラーでは検証できなかった点

- Godot 実行。本箱に Godot 無し。ミラーは asset-stripped で headless は失敗する
- 実機キャプチャでの金線 x 再計測
- approved PNG 上の焼き込み（title 左メニュー、sell `[仮]`）
- 既存 B1/B2 runtime Godot テストの実行回帰（静的契約トークンのみ確認）

## 要判断

1. 44/47 の 2px reskin を 72 に寄せるか（940 契約と衝突しうるので今回はやらない）
2. title 左メニューが PNG 焼き込みなら、コードでは消せない（アート側）
3. 08 の `[仮]` も同様にアート側の公算
4. shop 二重枠を focus と hover のどちらを残すか
