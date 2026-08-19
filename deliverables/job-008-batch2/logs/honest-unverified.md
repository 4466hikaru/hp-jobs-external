# 正直な申告 (job-008 第2バッチ)

日時: 2026-08-19 17:29 JST (UTC 08:29)

## 実施した読取

- clone なし。`gh api repos/4466hikaru/hp-game-share/contents/...` で live HEAD を読取
- live Main.gd blob `cf895716` (25230行 / 1019911 bytes)
- live UiHoverOverlay.gd blob `b9bdaa87` (17224 bytes)
- 仮想ツリー `/tmp/job008-batch2-apply`（gh raw を置いただけ。game repo の clone ではない）
- PR#8 / `job/008-ui-defect-code-fixes` は未接触。main へ push していない

## 実行できた検証

- 5 枚の unified diff が live HEAD に番号順 `git apply --check` OK
- 011 単独では HEAD に当たらない（010 後の文脈。想定どおり）
- `tests/test_job008_batch2_static.py` がパッチ適用後 PASS、未適用 FAIL
- live HEAD 契約トークン `["画面", "音量", "ゲーム", "戻る"]` と `func _show_run_history` は残る

## 実行できなかった検証

- Godot headless すべて（本箱に Godot なし、ミラーは asset-stripped）
- 遷移アサート 0.35s: 未実行。headless スクリプトには待ちを入れてあり、プレイ可能 checkout で回せる。**今回のパッチは遷移秒を触っていない**
- 実機キャプチャでの金線 x 再計測（job-004 は 2026-08-14。QG-13 前注記あり）
- 007/008/009/010/011 適用後の見た目再キャプチャ
- 08 の `[仮]` が approved PNG に焼き込まれているかのピクセル確認
- 34 の clip 後も Button theme margin で文字が左上に残るか（Godot 未実行）

「既存テスト回帰ゼロ」は静的契約の維持までしか言えない。

## No（パッチなし）

### 39_boot_splash

- 現行は 940 分岐 + UiSkin 1px 鉄。金の内側縦線は現行パスでは描かれない
- job-004 の x≈350 は 720+9-slice 時代の線（280+64=344）。940 なら内側は 170+64=234 で 350 ではない
- 72 inset を足すと 892+144=1036>940 で契約破壊。012 は作っていない

### 44_adult_viewer_gate / 47_new_game_confirm（要判断）

- reskin 2px が 72 を上書き。金は panel 外縁の 2px（940 なら x=170）。内側金線は無い
- 2→72 は QG-13 と 940 を壊しうる。指摘（x≈350 貫通）は現行 HEAD では既に構造上消えている公算
- 013 は作っていない。2px が唯一の直しならコードは変えない

### 23_reset_confirm / 24_unlock_confirm

- StyleBoxEmpty は画素を塗らない。空箱が金線を描いている証明ができず hide せず
- hide すると dialog 本体（children）も消える。leftover ではない

## 33 / 34 の正直注記（Yes だが Godot 未実行）

- キャプチャは 2026-08-14（QG-13 前）。HEAD は `EXPAND_IGNORE_SIZE` 済み。実機で TextureRect が既に 160×38 / 140×42 なら clip は冗長
- 33 の黒マスクを「溢れた crop」と断定した根拠は `33_clear_br.png` と、clear 経路に ColorRect が無いこと
- 34 の左上文字は「140×42 の Button が 350×105 枠の左上」。clip 後も Button 内部が左上なら theme margin が残っている可能性
- 見た目の再キャプチャはしていない
