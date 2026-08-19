# 正直な申告 (job-008 第4バッチ)

日時: 2026-08-19 19:15 JST (UTC 10:15)

## 実施した読取

- clone なし。`gh api repos/4466hikaru/hp-game-share/contents/...` で live HEAD を読取
- live HEAD `92ff9cdc66c9aa588f75b3665d03bc98ceea1527`
- live Main.gd blob `cf895716` (25230行 / 1019911 bytes / CR=0)
- live UiHoverOverlay.gd blob `b9bdaa87` (478行 / 17224 bytes / CR=0)
- 仮想ツリーは gh で取ったファイルを置いただけ。hp-game-share は clone していない
- PR#8 head `d4c669b16bcd0ee85ae3f5cf3fa3c882f30fcb1f` から 006 UP 版を取得。PR#8 には push していない
- batch3 main の 020/024 を取得。PR#10/#11 には触っていない
- main へ push していない
- job-002 は拾っていない。009/010/011 は開始していない。配置 agent は触っていない

## 実行できた検証

- 3枚の unified diff が live HEAD に孤立 `git apply --check` OK
- 連続 006 → 020 → 024 も OK
- 書き出し後 python で各パッチ `\r` カウント 0。適用後 Main.gd / UiHoverOverlay.gd も CR=0
- `tests/test_job008_batch4_static.py` がパッチ適用後 PASS、未適用 FAIL
- live HEAD 契約トークン `["画面", "音量", "ゲーム", "戻る"]` と `func _show_run_history` は残る
- 006 title bottom 636 / マージン 84 / bounced `Rect2(430, 602, 420, 70)` 不在を静的に確認
- 020 は関数名コンテキスト化した結果、近傍が違う Main.gd（approved B1 挿入済み）でも `git apply --check` OK

## 実行できなかった検証

- Godot headless すべて（本箱に Godot なし、ミラーは asset-stripped）
- 遷移アサート 0.35s: 未実行。headless スクリプトには待ちを入れてあり、プレイ可能 checkout で回せる。**本パッチは遷移秒を触っていない**
- 適用後の見た目再キャプチャ
- プレイ可能本体 repo そのものへの `git apply`（ミラー以外は gh で正としていない）。ローカルに残っていたより長い Main.gd では 024 だけ落ちることを確認した（言語/入力の追加行）

「既存テスト回帰ゼロ」は静的契約の維持までしか言えない。

## 024 の正直な限界

batch3 024 はミラー HEAD では元から当たる。落ちるのは bind04 と `_focus` の間に行が増えた側。3行コンテキストの unified diff は「直後の `_focus`」を要求するので、追加行をパッチに入れるとミラー HEAD が壊れる。本024はミラー HEAD を正として再掲した。プレイ可能へ先に当てるなら要判断。

## 006 方向

- HEAD: title y=598 h=48 bottom=646
- bounced (PR#8 c754246): title y=602 h=70 bottom=672（下＝画面下端に近づく。不採用）
- 本PR (d4c669b と同じ UP): title y=566 h=70 bottom=636 マージン 84px
