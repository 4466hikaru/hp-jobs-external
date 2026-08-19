# job-012 納品: `--ui-staging=image2` + タイトル/セーブ配置

対象コード: `https://github.com/4466hikaru/hp-game-share` (`main` HEAD `92ff9cdc66c9aa588f75b3665d03bc98ceea1527`、Main.gd blob `cf8957160449c31fcfdfe2b2488d834cc3b2108e`、25230行、size 1019911、CR=0)。`gh api repos/4466hikaru/hp-game-share/contents/game/scripts/main/Main.gd` で取得。hp-game-share は clone していない。asset-stripped のコードレビューミラーであり、Godot では遊べない。

## 完成定義 (Yes/No)

- [Yes] 配置パッチ+座標根拠（`title-coords.md` / `save-coords.md`。カンプ実測。発明していない）
- [Yes] 2状態ボタン・9スライス（title: ruby focus/hover/pressed、normal は空 StyleBox。save: ruby/iron の normal+focus。NinePatch title `_c48`=48、save `_c32`=32、いずれも texture-space）
- [Yes] テスト同梱: 静的 ON 座標 + OFF 回帰 PASS。Godot headless は **未実行**（ミラー asset-stripped。0.35s 待ちは playable checkout 用）
- [Yes] 正直な申告（本 README と `logs/honest-unverified.md`）

発注書 `jobs/job-012-parts-placement-batch1.md` の完成定義チェックボックスは未改変。status は既に `in-progress(game)`。

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート** (`game/scripts/main/Main.gd` がある場所)。LF。番号順。

```bash
git apply --check path/to/deliverables/job-012/patches/001-ui-staging-image2-flag.diff
git apply path/to/deliverables/job-012/patches/001-ui-staging-image2-flag.diff
git apply --check path/to/deliverables/job-012/patches/002-title-image2.diff
git apply path/to/deliverables/job-012/patches/002-title-image2.diff
git apply --check path/to/deliverables/job-012/patches/003-save-image2.diff
git apply path/to/deliverables/job-012/patches/003-save-image2.diff
python3 path/to/deliverables/job-012/tests/test_job012_static_flag.py .
python3 path/to/deliverables/job-012/tests/test_job012_static_placement.py .
```

001 のあとに title+save を一発で当てる場合は `004-title-save-combined.diff`（002+003 と同等）。

この箱での `git apply --check` は gh api 取得の Main.gd コピーに対して **001/002/003/004 すべて OK**。hunk 失敗なし（手 rebase なし）。CR=0。

## パッチ一覧

| file | 内容 |
|---|---|
| `patches/001-ui-staging-image2-flag.diff` | `ui_staging_mode` / `_configure_ui_staging_arg` / `_ui_staging_is_image2` |
| `patches/002-title-image2.diff` | `TitleImage2Layout.gd` + Main.gd title hunks |
| `patches/003-save-image2.diff` | Main.gd `_show_approved_save_load_menu` 付近 |
| `patches/004-title-save-combined.diff` | 002+003 結合（001 のあと） |

## フラグ

`--ui-staging=image2` / `--ui-staging image2` を 001 が新設（ミラーに無かった）。空 / 未指定 / image2 以外は OFF。

配置側のゲート（納品パッチのまま）:

- title: `TitleImage2Layout.is_enabled()` = cmdline に **正確に** `--ui-staging=image2`
- save: `_cmdline_has_flag("--ui-staging=image2")`

よって `--ui-staging image2`（空白形）は `ui_staging_mode` を立てるが title/save 配置は動かない。要判断。

OFF は現行 B1 早期 return。`_show_approved_title_menu` 本体は未変更。save は B1 view を組んだあと flag ON のときだけ chrome を上書き。

## アセットパス（仮決め・不一致のまま）

ファイル名は固定。PNG はパッチに埋め込まない。ゲーム repo に parts PNG がまだ無い可能性あり（材料は仕事板 `materials/ui_parts_batch1_image2/`）。

| 画面 | 読み込みディレクトリ |
|---|---|
| title | `res://assets/ui/ui_parts_batch1_image2/` 。backdrop のみ fallback `res://assets/ui/image2_parts/final/startup_backdrop_v001.png` |
| save | `res://assets/ui/image2_parts/final/` |

README 旧稿の `res://assets/ui/image2_batch1/` は使っていない（発明パスだったので撤回）。

ファイル名（変更禁止）:

```
startup_backdrop_v001.png
startup_vignette_v001.png
main_menu_frame_c48_v001.png
save_slot_frame_c32_v001.png
ruby_primary_button_normal_v001.png
ruby_primary_button_focus_v001.png
iron_secondary_button_normal_v001.png
iron_secondary_button_focus_v001.png
```

`age_gate_frame_c128_v001.png` / `confirm_modal_frame_c48_v001.png` / `legal_scroll_frame_c48_v001.png` は title/save に出さない。

## タイトル (03)

座標: `title-coords.md`（NOTES.md 実測表のコピー）。

- backdrop/vignette を 1280x720 dest に載せる（03 は graveyard 系）。
- 額縁 NinePatch dest 340,16 600x300 patch 48。
- 5 ボタン 28,376+52n 264x40。normal は枠なし（iron 未使用）。focus は ruby。
- `_show_title_image2_menu` の 設定 / クレジット文字列は **ハードコード JP**。

## セーブ (05)

座標: `save-coords.md`。納品報告どおり:

- slot 48,213 1182×186 / load 954,240 230×60 / delete 956,318 229×54 / new 510,543 260×66 / back 52,632 171×58
- backdrop/vignette は 05 に載せない（03 と背景が違う。library vs graveyard）
- corrupt action は新規ゲーム枠。ready 時の追加新規は既存 `_start_new_game_from_save_load`
- ヘッダ金線は未配置

## ミラーでは検証できなかった点

- Godot headless **未実行**（ミラー asset-stripped）
- 遷移待ち 0.35s の実行アサート **未実行**
- 実機見た目 / パーツ PNG がゲーム repo に存在するか
- `--ui-staging image2` 空白形で配置が動くか（現状動かない）

## 要判断

1. ミラーに `--ui-staging` が無かったので 001 で新設した。本体に別実装があるならそちらへ寄せる。
2. title と save のパーツディレクトリが不一致（上記 仮決め）。ファイル名は変えていない。
3. title の 設定/クレジットがハードコード JP。既存 loc key に寄せるか。
4. save corrupt-slot を新規ゲーム枠に置く仮決め。
5. title/save は `_ui_staging_is_image2()` を使わず exact `--ui-staging=image2` を見る。
6. ヘッダ金線未配置。05 に title 背景を載せない判断。
