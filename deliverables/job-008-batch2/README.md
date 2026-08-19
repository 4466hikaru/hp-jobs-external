# job-008 納品: UI欠陥コード修正（第2バッチ / HIGH残り）

対象コード: `https://github.com/4466hikaru/hp-game-share` (`main` HEAD blob `cf895716` / Main.gd 25230行、UiHoverOverlay.gd blob `b9bdaa87`)。`gh api` で読取。  
clone なし。パッチは live HEAD に番号順で `git apply` できることを確認した。本体へは当てていない。  
hp-game-share は asset-stripped のコードレビューミラーであり、Godot では遊べない。

対象リスト: 同梱の `triage-delta.md`（**このバッチで扱った指摘だけ**）。全指摘90件の再掲は PR#8 `deliverables/job-008/triage.md` を正とする。  
`jobs/job-008-ui-defect-code-fixes.md` の status は **open のまま**（バッチ継続中）。job-002 は拾っていない。

## 完成定義 (Yes/No)

- [Yes] 冒頭の対象リスト（本バッチ分は `triage-delta.md`。全指摘カバーは第1バッチ triage を継続）
- [Partial] コード対象の修正パッチ + 検証。HIGH 残りのうちコードで直した分のみ。直せなかった分は正直申告
- [Partial] 回帰ログ。静的 Python は PASS。Godot headless は本箱に Godot 無し・ミラーは asset-stripped のため未実行
- [Yes] 正直な申告（本 README + `logs/honest-unverified.md`）

PR#8 / branch `job/008-ui-defect-code-fixes` には commit していない。main 直 push していない。

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート** (`game/scripts/main/Main.gd` がある場所)。`hp-jobs-external` ではない。

第1バッチ（PR#8 `deliverables/job-008/patches/`）を先に当ててよい。本バッチの 5 本は **未適用の hp-game-share HEAD** にも当たる（第1バッチの hunk とは独立）。

```bash
# 1. 第2バッチパッチ（番号順。011 は 010 の後）
git apply --check path/to/hp-jobs-external/deliverables/job-008-batch2/patches/007-shop-single-selection-frame.diff
git apply --check path/to/hp-jobs-external/deliverables/job-008-batch2/patches/008-sell-drop-provisional-label.diff
git apply --check path/to/hp-jobs-external/deliverables/job-008-batch2/patches/009-hud-hide-legacy-panel.diff
git apply --check path/to/hp-jobs-external/deliverables/job-008-batch2/patches/010-clear-overlap-mask.diff
git apply --check path/to/hp-jobs-external/deliverables/job-008-batch2/patches/011-game-over-align.diff
git apply path/to/hp-jobs-external/deliverables/job-008-batch2/patches/007-shop-single-selection-frame.diff
git apply path/to/hp-jobs-external/deliverables/job-008-batch2/patches/008-sell-drop-provisional-label.diff
git apply path/to/hp-jobs-external/deliverables/job-008-batch2/patches/009-hud-hide-legacy-panel.diff
git apply path/to/hp-jobs-external/deliverables/job-008-batch2/patches/010-clear-overlap-mask.diff
git apply path/to/hp-jobs-external/deliverables/job-008-batch2/patches/011-game-over-align.diff

# 2. テスト配置
cp path/to/hp-jobs-external/deliverables/job-008-batch2/tests/test_job008_batch2_layout_headless.gd game/tests/
cp path/to/hp-jobs-external/deliverables/job-008-batch2/tests/test_job008_batch2_layout_headless.sh game/tests/

# 3. 静的チェック (Godot 不要)
python3 path/to/hp-jobs-external/deliverables/job-008-batch2/tests/test_job008_batch2_static.py .

# 4. Godot headless (プレイ可能 checkout のみ。遷移待ち 0.35s 込み)
godot --path game --headless --script res://tests/test_job008_batch2_layout_headless.gd
```

`git apply` が拒否したら番号順に `patch -p1 < patches/00N-....diff`。011 単独では HEAD に当たらない（010 後の文脈）。

## 適用順

007 → 008 → 009 → 010 → 011

## パッチ一覧

| file | 対象 triage 行 / 画面 | 内容 | 結果 |
|---|---|---|---|
| `patches/007-shop-single-selection-frame.diff` | 11 (07_shop 二重選択) | ホバー枠を落とす。focus のみ。`UiHoverOverlay` は meta `ui_hover_suppress_hover_draw` で pointer glow を描かない | Yes（コード。Godot 未実行） |
| `patches/008-sell-drop-provisional-label.diff` | 13 (08_sell `[仮]`) | live 文字の `[仮]` 接頭辞を切る。approved PNG 焼き込みの hide は発明しない | Yes（コード。Godot 未実行） |
| `patches/009-hud-hide-legacy-panel.diff` | 46 / 48 (25/26 HUD 二重) | `CombatHudSlots` があるとき leftover `hud_panel` / `hud_container` を隠す | Yes（コード。Godot 未実行） |
| `patches/010-clear-overlap-mask.diff` | 59 (33_clear 重なり+黒マスク) | extra-action を live rect で clip。行間隔 6→14px。ラベル z=2 | Yes（コード。Godot 未実行） |
| `patches/011-game-over-align.diff` | 62 (34_game_over 文字左上+赤装飾) | 同じ clip を game_over 4ボタンにも適用。leftover mask を `(800,345,480,140)` へ。010 の後に当てる | Yes（コード。Godot 未実行） |

012 / 013 は作っていない。

## このバッチの Yes/No

| 画面 | 結果 | パッチ | メモ |
|---|---|---|---|
| 07_shop 二重選択枠 | **Yes**（コード） | 007 | ホバーを落としてフォーカスのみ。プレビュー不一致（データ）はやらない |
| 08_sell_inventory `[仮]` | **Yes**（コード） | 008 | live 文字だけカット。PNG 焼き込みが残るならアート側 |
| 25 / 26 HUD 二重 | **Yes**（コード） | 009 | leftover `hud_panel` を CombatHudSlots 生存時に隠す。再現は Godot 未実行 |
| 33_clear | **Yes**（コード） | 010 | clip + 間隔。配色・キャプション省略はやらない |
| 34_game_over | **Yes**（コード） | 011 | clip + leftover mask 拡大。スタッツ枠切れ・見出し左寄せはやらない |
| 39_boot_splash | **No** | なし | 現行は 940 分岐 + UiSkin 1px 鉄。job-004 の x≈350 金線は 720+9-slice 時代の線。今のパスでは出ない。72 inset を足すと 940 契約破壊 |
| 44_adult_viewer_gate | **No**（要判断） | なし | reskin 2px が 72 を上書き。2→72 は QG-13 と 940 を壊しうる。現行に内側金線は無い |
| 47_new_game_confirm | **No**（要判断） | なし | 44 と同じ |
| 23_reset_confirm / 24_unlock_confirm | **No** | なし | StyleBoxEmpty が金線を描いている証明ができず hide せず |

担当以外の画面は未変更。デザイン変更なし。画像は生成していない。

## Godot / 検証

- Godot 実行: **未実行**（本箱に Godot なし。ミラーは asset-stripped）
- 遷移アサート 0.35s: 未実行。headless スクリプトには待ちを入れてあり、プレイ可能 checkout で回せる。**今回のパッチは遷移秒を触っていない**
- `git apply --check`: live HEAD に 007→008→009→010→011 が通る。011 単独では HEAD に当たらない
- 静的 Python: パッチ適用後 PASS / 未適用 FAIL

## 要判断（オーナー）

1. 44/47 の 2px reskin を 72 に寄せるか（940 契約と QG-13 の明示 2px 枠に抵触しうるので今回はやらない）
2. job-004 PNG を HEAD で取り直すか。取り直して線が x=170 外縁だけなら、39/44/47 のコード変更は不要
3. 08 の `[仮]` が approved PNG に焼き込まれて残るならアート側
