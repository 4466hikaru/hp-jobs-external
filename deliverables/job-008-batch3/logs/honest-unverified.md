# 正直な申告 (job-008 第3バッチ)

日時: 2026-08-19 18:00 JST (UTC 09:00)

## 実施した読取

- clone なし。`gh api repos/4466hikaru/hp-game-share/contents/...` で live HEAD を読取
- live HEAD `92ff9cdc66c9aa588f75b3665d03bc98ceea1527`
- live Main.gd blob `cf895716` (25230行 / 1019911 bytes)
- live UiHoverOverlay.gd blob `b9bdaa87` (17224 bytes)
- 仮想ツリー `/tmp/job008-batch3-apply`（gh raw / 一致確認済み `_src` を置いただけ。game repo の clone ではない）
- PR#8 / `job/008-ui-defect-code-fixes` と PR#9 / `job/008-batch2-high-leftover` は未接触。main へ push していない
- job-002 は拾っていない

## 実行できた検証

- 28 枚の unified diff が live HEAD に番号順 `git apply --check` OK
- 書き出し後 python で各パッチ `\r` カウント 0
- `tests/test_job008_batch3_static.py` がパッチ適用後 PASS、未適用 FAIL
- live HEAD 契約トークン `["画面", "音量", "ゲーム", "戻る"]` と `func _show_run_history` は残る
- 035 は Batch4 の unlock_rows / `_add_text_slot` だけ。batch2 010 のボタン重なりトークンは含まれない

## 実行できなかった検証

- Godot headless すべて（本箱に Godot なし、ミラーは asset-stripped）
- 遷移アサート 0.35s: 未実行。headless スクリプトには待ちを入れてあり、プレイ可能 checkout で回せる。**本パッチは遷移秒を触っていない**（032 はタイトル空白だけ）
- 適用後の見た目再キャプチャ
- 08 / title 等の approved PNG 焼き込みのピクセル確認（本バッチ対象外）

「既存テスト回帰ゼロ」は静的契約の維持までしか言えない。

## No（パッチなし）

### 27_level_up / 28_boss_reward

HEAD で群中心≈640。job-004 の x≈507 / x≈520 は Festival ショーケース。+130 は右倒れ。コード変更なし。  
job-004 の 27 キャプチャは Festival ショーケース（LV12 / 血薔薇の鞭）で、現行 live 27 は B2 approved PNG。PNG 側が左寄せならアート案件（今回は触らない）。  
`cards/27_level_up.diff` と `cards/28_boss_reward.diff` は納品に入れていない。

### 44_adult_viewer_gate / 47_new_game_confirm

今バッチ対象外。2px→72 は batch2 で既に書いた。繰り返さない。

## マージの正直注記

- Batch3 `_add_text_slot` は 10 の完全版を 012 に1本だけ入れた。07 / 15 の弱い版は捨てた
- overlay hunk は 024 に1回。batch2 007 と同型だが、PR#9 未マージの main HEAD には 007 が無い
- 低 37（タブ高さ）と強化 37（結果文幅）は両方 Main.gd に入っている
