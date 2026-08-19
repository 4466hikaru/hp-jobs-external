# job-012 正直申告（フラグ + タイトル/セーブ配置）

## ミラーに無かったので新設した

- `--ui-staging` は hp-game-share `92ff9cdc` の Main.gd に無かった。
- `--store-target` と同じ様式で `--ui-staging=image2` と `--ui-staging image2` を 001 で新設した。
- title は `TitleImage2Layout.is_enabled()`、save は `_cmdline_has_flag("--ui-staging=image2")`。空白形は配置に効かない。

## 配置の仮決め

- アセットディレクトリ不一致: title `res://assets/ui/ui_parts_batch1_image2/`（backdrop fallback は `image2_parts/final`）、save `res://assets/ui/image2_parts/final/`。ファイル名は変えていない。
- title の 設定 / クレジット文字列はハードコード JP。
- save corrupt-slot は新規ゲーム枠 (510,543,260x66) に iron。ラベルは既存の戻る。
- ready 時の追加新規ゲームは既存 `_start_new_game_from_save_load`。
- ヘッダ金線は未配置。
- save 05 に backdrop/vignette を載せない（03 と背景が違う。library vs graveyard）。
- title の normal 行は枠なし（iron_secondary 未使用）。focus だけ ruby。
- `age_gate` / `confirm_modal` / `legal_scroll` を title/save に置いていない。
- パーツ PNG はゲーム repo にまだ無い可能性。材料は仕事板 `materials/ui_parts_batch1_image2/`。

## 適用

- `git apply --check` は gh api 取得の Main.gd コピーに対し 001→002→003 および 001→004 すべて OK。hunk 失敗なし。手 rebase なし。CR=0。
- 元パッチ `title_image2.patch` / `05_save_image2.patch` も 001 のあとに context 一致で当たった。

## 未実行

- Godot headless 未実行。
- 0.35s 遷移アサート 未実行。
