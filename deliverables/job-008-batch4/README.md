# job-008 納品: UI欠陥コード修正（第4バッチ / 020・024 rebase + 006 pause上方向）

対象コード: `https://github.com/4466hikaru/hp-game-share` (`main` HEAD `92ff9cdc66c9aa588f75b3665d03bc98ceea1527` / Main.gd blob `cf895716` 25230行、UiHoverOverlay.gd blob `b9bdaa87`)。`gh api` で読取。  
clone なし。本体へは当てていない。hp-game-share は asset-stripped のコードレビューミラーであり、Godot では遊べない。

本PRは **ちょうど3本**。PR#8 / PR#10 / PR#11 には追加pushしていない。main 直pushしていない。job-002 は拾っていない。009/010/011 は開始していない。配置agentは触っていない。

検収コメントの意図: 「020/024を現行main相当へ当たる形に作り直し+PR#8で差し戻した006(pause逆方向)の再修正、の3本を次のPRで」

## 完成定義 (Yes/No)

- [Yes] 020 `save-delete-align` を現行 hp-game-share HEAD へ関数名コンテキストで作り直し。`git apply --check` OK
- [Yes] 024 `options-single-chrome` を現行 HEAD へ当て直し。孤立・006/020との連続適用とも OK
- [Yes] 006 pause を **上方向** に再修正（title `Rect2(430, 566, 420, 70)` / bottom 636 / 下マージン 84px）。逆方向(y=602 bottom 672)は入れていない
- [Partial] 回帰。静的 Python は未適用 FAIL / 適用後 PASS。Godot headless は本箱に Godot 無し・ミラーは asset-stripped のため **未実行**
- [Yes] 正直な申告（本 README + `logs/honest-unverified.md`）

`jobs/job-008-ui-defect-code-fixes.md` の完成チェックボックスは **書き換えていない**（status のみ `in-progress(game)`）。

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート** (`game/scripts/main/Main.gd` がある場所)。`hp-jobs-external` ではない。

```bash
for p in \
  006-pause-hex-frames-margin \
  020-save-delete-align \
  024-options-single-chrome
do
  git apply --check path/to/hp-jobs-external/deliverables/job-008-batch4/patches/${p}.diff
done
for p in \
  006-pause-hex-frames-margin \
  020-save-delete-align \
  024-options-single-chrome
do
  git apply path/to/hp-jobs-external/deliverables/job-008-batch4/patches/${p}.diff
done

python3 path/to/hp-jobs-external/deliverables/job-008-batch4/tests/test_job008_batch4_static.py .

# Godot headless (プレイ可能 checkout のみ。遷移待ち 0.35s 込み)
godot --path game --headless --script res://tests/test_job008_batch4_layout_headless.gd
```

パッチ改行: **LF のみ**（CR=0。PR#8 の CRLF 全滅を踏まえて書き出し後に `\r` を数えた）。

適用順: 006 → 020 → 024（孤立でも当たる。連続でも当たる）。

## なぜ batch3 の 020/024 が「現行相当」で落ちるか

hp-game-share HEAD 自体は batch3 時点から動いていない（同じ `92ff9cdc` / Main.gd 25230行）。batch3 の 020/024 は **このミラー HEAD には当たる**。落ちるのは近傍が違うプレイ可能側:

| パッチ | share HEAD (`92ff9cdc`) | 近傍が変わった側（行ドリフト） |
|---|---|---|
| 020 | `_show_menu_shell` の直後に `_add_info_card(..., "default")` | approved B1 経路 `_show_approved_save_delete_confirm` が間に入り、`_show_menu_shell` と `_add_info_card` が隣接しない。 hunk 先頭 `@@ -7460` の3行コンテキストが一致しない |
| 024 | bind04 の直後が `_focus_approved_ui_wiring_b2_button(display_tab)` | `_show_approved_b2_options` に言語/入力の追加行があり、bind04 と `_focus` が隣接しない。15行一塊の hunk が一致しない |
| 006 | pause title `Rect2(430, 598, 420, 48)` bottom 646 | 矩形そのものは同じ。PR#8 初版は y=602/h=70 bottom **672** の下方向。d4c669b で上方向へ差し戻し済み。本PRはその UP 版を HEAD へ再掲 |

本バッチの対処:

- **020**: 呼び出し hunk を `_add_info_card` + `_delete_slot_1_save`（save_delete_confirm 固有）に切り直した。`_show_menu_shell` 隣接を要求しない。`_add_info_card` 本体は関数シグネチャで当てる。share HEAD と近傍違い側の両方で `git apply --check` OK
- **024**: share HEAD の関数塊（`_show_approved_b2_options` の4タブ bind + overlay）を維持。言語/入力行をパッチに入れるとミラー HEAD が壊れるので **入れてない**。ミラー HEAD では孤立・連続とも OK。プレイ可能側に追加カテゴリ行がある場合は hunk が bind04 直後の `_focus` を要求するため **要判断**
- **006**: PR#8 d4c669b の UP 版（LF）を現行 HEAD の pause 3矩形に当てる。下方向(y=602/bottom 672)は含まない

どの hunk も HEAD に既に入ってはいない（no-op なし）。

## パッチ一覧

| file | 対象 | 内容 | +/- | 結果 |
|---|---|---|---|---|
| `006-pause-hex-frames-margin.diff` | 32_pause 下端 | 設定 hex 下地。save/retry/title を **上へ**。title `Rect2(430, 566, 420, 70)` bottom 636 / マージン 84px（元 bottom 646 / マージン 74px） | +19 / -3 | Yes（コード。Godot 未実行） |
| `020-save-delete-align.diff` | 42_save_delete_confirm スロット1左寄せ | `_add_info_card` に alignment。delete confirm だけ CENTER。金枠 001 は未接触 | +6 / -2 | Yes（コード。Godot 未実行） |
| `024-options-single-chrome.diff` | 20_options 二重フォーカス | ゲーム焼き込みを音量プレートへ。nav は focus overlay のみ。下2行は触らない | +34 / -4 | Yes（ミラー HEAD。Godot 未実行） |

削除が挿入を大きく超えていない。デザイン/情報量/配色は変えていない。画面を新設していない。画像は生成していない。

## このバッチの Yes/No

| 項目 | 結果 | メモ |
|---|---|---|
| 020 を現行 HEAD へ作り直し | **Yes** | 関数名コンテキスト。share HEAD `git apply --check` OK |
| 024 を現行 HEAD へ作り直し | **Yes**（ミラー） | 孤立・連続 OK。プレイ可能側の追加カテゴリ行は 要判断 |
| 006 pause 逆方向の再修正 | **Yes** | UP。before y=598/h=48/bottom=646。after y=566/h=70/bottom=636。bounced y=602/bottom=672 は不採用 |
| Godot headless | **未実行** | 本箱に Godot なし。ミラーは asset-stripped |
| 遷移アサート 0.35s | **未実行** | headless スクリプトには待ちあり。本パッチは遷移秒を触っていない |

## 006 before / after y

viewport 高さ 720 前提。

| ボタン | HEAD (元) | bounced (不採用) | 本PR (UP) |
|---|---|---|---|
| save | y=486 h=48 bottom=534 | y=478 h=56 bottom=534 | y=470 h=44 bottom=514 |
| retry | y=542 h=48 bottom=590 | y=540 h=56 bottom=596 | y=518 h=44 bottom=562 |
| title | y=598 h=48 bottom=**646** / マージン 74 | y=602 h=70 bottom=**672** | y=**566** h=70 bottom=**636** / マージン **84** |

設定ラベル下端 469。save は 470 から（重ならない）。

## Godot / 検証

- Godot 実行: **未実行**（本箱に Godot なし。ミラーは asset-stripped）
- 遷移アサート 0.35s: 未実行。headless スクリプトには待ちを入れてあり、プレイ可能 checkout で回せる
- `git apply --check`: live HEAD に 006 / 020 / 024 が孤立でも連続でも通る
- 静的 Python: パッチ適用後 PASS / 未適用 FAIL
- LF: 3本とも CR=0

## 要判断（オーナー）

1. プレイ可能 main の `_show_approved_b2_options` に言語/入力行がある場合、024 の bind hunk（bind04 直後 `_focus`）は `git apply` が拒否する。ミラー HEAD にはその行が無い。ミラーを正とするなら本024のまま。プレイ可能へ先に当てるなら、その追加行を残したまま bind だけ掴む別 hunk が要る（本PRではミラー破壊を避けるため入れてない）
2. プレイ可能側の save_delete が approved B1 ビューを先に出す場合、020 の `_add_info_card` CENTER はフォールバック殻にしか効かない。B1 焼き込みの左寄せはアート/配置の話で、本パッチはコードの info card だけ
3. 006 の 84px 下マージンは検収指定どおり。見た目の再キャプチャは未実施

## やっていないこと

- PR#8 / PR#11 への追加push
- main 直push
- job-002 / 009 / 010 / 011
- 配置 agent へのアサイン
- 完成チェックボックスの書き換え
- 画面新設・GenerateImage・配色/情報量の変更
