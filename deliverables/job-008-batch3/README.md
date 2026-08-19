# job-008 納品: UI欠陥コード修正（第3バッチ / 中・低）

対象コード: `https://github.com/4466hikaru/hp-game-share` (`main` HEAD `92ff9cdc` / Main.gd blob `cf895716` 25230行、UiHoverOverlay.gd blob `b9bdaa87`)。`gh api` で読取。  
clone なし。パッチは live HEAD に番号順で `git apply` できることを確認した。本体へは当てていない。  
hp-game-share は asset-stripped のコードレビューミラーであり、Godot では遊べない。

対象リスト: 同梱の `triage-delta.md`（**このバッチで扱った指摘だけ**）。全指摘90件の再掲は PR#8 `deliverables/job-008/triage.md` を正とする。  
`jobs/job-008-ui-defect-code-fixes.md` の status は **open のまま**（バッチ継続中）。job-002 は拾っていない。

## 完成定義 (Yes/No)

- [Yes] 冒頭の対象リスト（本バッチ分は `triage-delta.md`。全指摘カバーは第1バッチ triage を継続）
- [Partial] コード対象の修正パッチ + 検証。未着手だった中・低のうち game 採否済みの分のみ。27/28 は No
- [Partial] 回帰ログ。静的 Python は PASS。Godot headless は本箱に Godot 無し・ミラーは asset-stripped のため未実行
- [Yes] 正直な申告（本 README + `logs/honest-unverified.md`）

PR#8 / `job/008-ui-defect-code-fixes` と PR#9 / `job/008-batch2-high-leftover` には commit していない。main 直 push していない。

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート** (`game/scripts/main/Main.gd` がある場所)。`hp-jobs-external` ではない。

本バッチの 28 本は **未適用の hp-game-share HEAD** に当たる（PR#8 / PR#9 は未マージ前提。007 の overlay は本バッチ 024 に1回だけ入っている）。

```bash
# 1. 第3バッチパッチ（番号順 012 → 039）
for p in \
  012-shop-soldout-overlap \
  013-character-select-caption \
  014-equipment-list-summary-wrap \
  015-equipment-slots-card-clip \
  016-equipment-candidates-compare \
  017-dungeon-info-overlap \
  018-dungeon-round-choice-width \
  019-save-load-duplicate-draw \
  020-save-delete-align \
  021-enhance-preview-name-break \
  022-item-detail-actions \
  023-scene-choice-result-width \
  024-options-single-chrome \
  025-gallery-title-spacer \
  026-system-menu-rows \
  027-motion-check-qa \
  028-stage-select-clip \
  029-world-map-node-snap \
  030-objective-log-rule \
  031-town-menu-back-align \
  032-loading-transition-gap \
  033-summon-select-header \
  034-scene-view-wait-inset \
  035-clear-captions-wrap \
  036-alert-overlay-align \
  037-scene-choice-bottom-margin \
  038-scene-choice-result-tab \
  039-credits-license-clip
do
  git apply --check path/to/hp-jobs-external/deliverables/job-008-batch3/patches/${p}.diff
done
for p in \
  012-shop-soldout-overlap \
  013-character-select-caption \
  014-equipment-list-summary-wrap \
  015-equipment-slots-card-clip \
  016-equipment-candidates-compare \
  017-dungeon-info-overlap \
  018-dungeon-round-choice-width \
  019-save-load-duplicate-draw \
  020-save-delete-align \
  021-enhance-preview-name-break \
  022-item-detail-actions \
  023-scene-choice-result-width \
  024-options-single-chrome \
  025-gallery-title-spacer \
  026-system-menu-rows \
  027-motion-check-qa \
  028-stage-select-clip \
  029-world-map-node-snap \
  030-objective-log-rule \
  031-town-menu-back-align \
  032-loading-transition-gap \
  033-summon-select-header \
  034-scene-view-wait-inset \
  035-clear-captions-wrap \
  036-alert-overlay-align \
  037-scene-choice-bottom-margin \
  038-scene-choice-result-tab \
  039-credits-license-clip
do
  git apply path/to/hp-jobs-external/deliverables/job-008-batch3/patches/${p}.diff
done

# 2. テスト配置
cp path/to/hp-jobs-external/deliverables/job-008-batch3/tests/test_job008_batch3_layout_headless.gd game/tests/
cp path/to/hp-jobs-external/deliverables/job-008-batch3/tests/test_job008_batch3_layout_headless.sh game/tests/

# 3. 静的チェック (Godot 不要)
python3 path/to/hp-jobs-external/deliverables/job-008-batch3/tests/test_job008_batch3_static.py .

# 4. Godot headless (プレイ可能 checkout のみ。遷移待ち 0.35s 込み)
godot --path game --headless --script res://tests/test_job008_batch3_layout_headless.gd
```

`git apply` が拒否したら番号順に `patch -p1 < patches/0NN-....diff`。

## 適用順

012 → 013 → 014 → 015 → 016 → 017 → 018 → 019 → 020 → 021 → 022 → 023 → 024 → 025 → 026 → 027 → 028 → 029 → 030 → 031 → 032 → 033 → 034 → 035 → 036 → 037 → 038 → 039

パッチ改行: **LF のみ**（CR=0。PR#8 検収の CRLF 全滅を踏まえて書き出し後に `\r` を数えた）。

## マージした衝突

- `Stage4MassBatch3.gd` `_add_text_slot`: 07 / 15 / 10 が別々に autowrap を足していた。**10 の完全版（clip / vertical TOP / no-trim）を 012 に1回だけ**入れた。各画面 spec の `autowrap` フラグは 012 / 016 / 017 に残す
- `UiHoverOverlay.gd`: batch2 007 と同型。PR#9 は未マージなので main HEAD 基準で **024 に1回だけ**入れる
- `Main.gd`: hunk が重ならない適用順。低 37（名前タブ高さ）と強化 37（結果文幅）は両方入れた
- `Stage4MassBatch4.gd`: 018 は regions、035 が `_add_text_slot` autowrap、036 は alert。033 クリアボタン重なり（batch2 010）は 035 で触っていない

## パッチ一覧

| file | 対象 triage 行 / 画面 | 内容 | 結果 |
|---|---|---|---|
| `012-shop-soldout-overlap.diff` | 12 (07_shop 売り切れ重なり) | 行井戸 280→230 + autowrap。価格を2行目へ。二重選択と 08 は未接触 | Yes（コード。Godot 未実行） |
| `013-character-select-caption.diff` | 23 (12 戻る/出撃 上寄り) | 承認プレートいっぱいに広げ、上パッドでキャプションを中央へ | Yes（コード。Godot 未実行） |
| `014-equipment-list-summary-wrap.diff` | 25 (13 右パネル省略) | 4行目スロット拡大 + wrap | Yes（コード。Godot 未実行） |
| `015-equipment-slots-card-clip.diff` | 29 (14 右端カード切れ) | 4枚の target/hotspot を画面内へ。14 ラベル欠け（PR#8 004）は未接触 | Yes（コード。Godot 未実行） |
| `016-equipment-candidates-compare.diff` | 30 (15 比較省略) | comparison 幅 450 + autowrap | Yes（コード。Godot 未実行） |
| `017-dungeon-info-overlap.diff` | 16 / 17 / 18 (10 剣食い込み・召喚密着・報酬省略) | 条件/報酬を改行。召喚を 8px 上げる | Yes（コード。Godot 未実行） |
| `018-dungeon-round-choice-width.diff` | 55 / 56 (31 続行/帰還が切れる) | choice_detail 145→280 | Yes（コード。Godot 未実行） |
| `019-save-load-duplicate-draw.diff` | 72 / 73 (41 二重タイトル / 二重ロード) | Stage4 タイトルを隠し、フッター「ロード」文字を空に | Yes（コード。Godot 未実行） |
| `020-save-delete-align.diff` | 75 (42 スロット1だけ左寄せ) | info card を中央寄せ。金枠 001 は未接触 | Yes（コード。Godot 未実行） |
| `021-enhance-preview-name-break.diff` | 80 / 81 (45 リリカ割れ・素材省略) | WORD JOINER + cost 帯拡幅 | Yes（コード。Godot 未実行） |
| `022-item-detail-actions.diff` | 85 (46 使うが画面外・文字上寄り) | 4ボタンを内側へ + 上パッド | Yes（コード。Godot 未実行） |
| `023-scene-choice-result-width.diff` | 66 (37 結果文切れ) | 結果バー幅 0.76・高さ 112・wrap | Yes（コード。Godot 未実行） |
| `024-options-single-chrome.diff` | 40 (20 二重フォーカス) | ゲーム焼き込みを音量プレートに差し替え。hover 抑制。下2行は触らない | Yes（コード。Godot 未実行） |
| `025-gallery-title-spacer.diff` | 33 (16 回想一覧上端欠け) | 24px spacer。金枠 001 は未接触 | Yes（コード。Godot 未実行） |
| `026-system-menu-rows.diff` | 89 (49 Back を金枠下辺が横切る) | 行間 6・ボタン高 40。文言は触らない | Yes（コード。Godot 未実行） |
| `027-motion-check-qa.diff` | 76 (43 QA 漏れ + 下地) | STANDING MOTION QA を描かない。左シェルを不透明クリア。Back 英語は触らない | Yes（コード。Godot 未実行） |
| `028-stage-select-clip.diff` | 4 / 5 (02 縦線切れ端・出撃赤装飾) | 上カード 1172 clip。「出撃する」幅 280 | Yes（コード。Godot 未実行） |
| `029-world-map-node-snap.diff` | 7 (03 接続線ズレ) | ノード座標を integer snap | Yes（コード。Godot 未実行） |
| `030-objective-log-rule.diff` | 9 (04 3行目横線) | card03 右の leftover rule を覆う | Yes（コード。Godot 未実行） |
| `031-town-menu-back-align.diff` | 10 (06 戻る右寄り) | back 井戸をプレート中央へ | Yes（コード。Godot 未実行） |
| `032-loading-transition-gap.diff` | 15 (09 「拠点 へ」空き) | 全角/半角スペースを潰し、帯幅を拡げる。遷移秒は未変更 | Yes（コード。Godot 未実行） |
| `033-summon-select-header.diff` | 20 (11 ヘッダ省略) | resource_cost 幅 300→580 | Yes（コード。Godot 未実行） |
| `034-scene-view-wait-inset.diff` | 34 (17 次へ三角端) | 待ち三角を +20px inset | Yes（コード。Godot 未実行） |
| `035-clear-captions-wrap.diff` | 61 (33 報酬キャプション省略) | unlock_rows wrap。**ボタン重なり（batch2 010）は未接触** | Yes（コード。Godot 未実行） |
| `036-alert-overlay-align.diff` | 64 (35 左右非対称・文字上) | 右星の飛び出しを mask。文字を 6px 下げる | Yes（コード。Godot 未実行） |
| `037-scene-choice-bottom-margin.diff` | 65 (36 本文が下端近い) | 対話下マージン 40px | Yes（コード。Godot 未実行） |
| `038-scene-choice-result-tab.diff` | 67 (37 名前箱が高すぎる) | 名前タブ 50→40。強化 37（023）と同居 | Yes（コード。Godot 未実行） |
| `039-credits-license-clip.diff` | 69 (38 枠外縦線) | credits で menu_panel を clip。金枠 001 は未接触 | Yes（コード。Godot 未実行） |

27 / 28 のパッチは作っていない。

## このバッチの Yes/No

| 画面 | 結果 | パッチ | メモ |
|---|---|---|---|
| 07_shop 売り切れ重なり | **Yes**（コード） | 012 | 二重選択枠と 08 `[仮]` は batch2。触っていない |
| 12_character_select ボタン上寄り | **Yes**（コード） | 013 | 選択同期・南京錠矛盾はやらない |
| 13_equipment_list 右パネル省略 | **Yes**（コード） | 014 | 空カード名はやらない |
| 14_equipment_slots 右端切れ | **Yes**（コード） | 015 | ラベル欠けは PR#8。黒箱スキンはやらない |
| 15_equipment_candidates 比較省略 | **Yes**（コード） | 016 | |
| 10_dungeon_info 重なり/省略 | **Yes**（コード） | 017 | |
| 31_dungeon_round_choice 切れ | **Yes**（コード） | 018 | |
| 41_save_load_menu 二重描画 | **Yes**（コード） | 019 | |
| 42_save_delete_confirm 整列 | **Yes**（コード） | 020 | 金枠は 001 |
| 45_enhance_preview 改行/省略 | **Yes**（コード） | 021 | 黒プレースホルダと「未接続」はやらない |
| 46_item_detail ボタン | **Yes**（コード） | 022 | データ割れ・`[仮]` はやらない |
| 37_scene_choice_result 結果文 | **Yes**（コード） | 023 | |
| 20_options 二重フォーカス | **Yes**（コード） | 024 | 下2行空欄はやらない |
| 16_gallery タイトル欠け | **Yes**（コード） | 025 | 金枠 X は 001。サムネ白地はやらない |
| 49_system_menu Back 横断 | **Yes**（コード） | 026 | 日英混在はやらない |
| 43_motion_check QA 漏れ | **Yes**（コード） | 027 | Back 英語はやらない。金枠 X は 001 |
| 02_stage_select 切れ端/余白 | **Yes**（コード） | 028 | 南京錠データ不一致はやらない |
| 03_world_map 接続線 | **Yes**（コード） | 029 | 日英混在はやらない |
| 04_objective_log 横線 | **Yes**（コード） | 030 | 空プレースホルダはやらない |
| 06_town_menu 戻る | **Yes**（コード） | 031 | |
| 09_loading_transition 空き | **Yes**（コード） | 032 | 遷移秒は未変更 |
| 11_summon_select ヘッダ省略 | **Yes**（コード） | 033 | 空カード絵はやらない |
| 17_scene_view 三角 | **Yes**（コード） | 034 | |
| 33_clear キャプション省略 | **Yes**（コード） | 035 | ボタン重なりは batch2 010。触っていない |
| 35_alert_overlay 左右/垂直 | **Yes**（コード） | 036 | |
| 36_scene_choice 下端 | **Yes**（コード） | 037 | |
| 37_scene_choice_result 名前タブ | **Yes**（コード） | 038 | 023 と両方入れる |
| 38_credits_license 枠外線 | **Yes**（コード） | 039 | 金枠は 001 |
| 27_level_up 中心ズレ | **No** | なし | HEAD で群中心≈640。job-004 の x≈507 は Festival ショーケース。+130 は右倒れ |
| 28_boss_reward 中心ズレ | **No** | なし | HEAD で群中心≈640。job-004 の x≈520 は同上。コード変更なし |

担当以外の画面は未変更。デザイン変更なし。画像は生成していない。job-002 は拾っていない。

## Godot / 検証

- Godot 実行: **未実行**（本箱に Godot なし。ミラーは asset-stripped）
- 遷移アサート 0.35s: 未実行。headless スクリプトには待ちを入れてあり、プレイ可能 checkout で回せる。**本パッチは遷移秒を触っていない**（032 はタイトル空白だけ）
- `git apply --check`: live HEAD に 012→039 が通る
- 静的 Python: パッチ適用後 PASS / 未適用 FAIL

## 要判断（オーナー）

1. 27/28 の PNG 左寄せ（job-004 キャプチャ）はアート側。現行 live 矩形は既に中央。コードでは触らない
