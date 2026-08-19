# job-012 納品: `--ui-staging=image2` フラグ（配置パッチ待ち）

対象コード: `https://github.com/4466hikaru/hp-game-share` (`main` HEAD `92ff9cdc`、Main.gd 25230行、2026-08-19 を `gh api` で読取)。  
hp-game-share は clone していない。asset-stripped のコードレビューミラーであり、Godot では遊べない。

## 分業（2026-08-19 追記）

タイトル配置とセーブ配置は別担当。本ブランチのこの時点では **フラグ本体だけ** を入れる。  
`/workspace/job012/title/` と `/workspace/job012/save/` のパッチが来たらマージする。来ていなければ画面配置は発明しない。

## 完成定義 (Yes/No)

- [No] 配置パッチ+座標根拠（タイトル/セーブの配置パッチ未着。発明していない）
- [No] 2状態ボタン・9スライス（同上）
- [Partial] テスト同梱: フラグ静的テストは PASS。ON の各パーツ node 座標は配置パッチ待ち。OFF 回帰は「title/save の B1 早期 return がフラグで包まれていない」ことを静的に主張
- [Yes] 正直な申告（本 README と `logs/honest-unverified.md`）

## `--ui-staging` について（honest / 要判断）

ミラー HEAD `92ff9cdc` の `Main.gd` `_configure_playtest` / `_cmdline_has_flag` に `--ui-staging` は **無かった**（`--playtest` `--screen-audit` `--dev` `--store-target` はある）。  
仕事板の「既存機構に image2 を足す」が成立しなかったので、`--store-target` と同じ cmdline 様式で **新設** した。

受け付ける形:

- `--ui-staging=image2`
- `--ui-staging image2`

空 / 未指定 / `image2` 以外は `ui_staging_mode == ""`。`_ui_staging_is_image2()` は false。  
このパッチは title / save の builder を触らない。フラグOFFは現行と同一（B1 早期 return のまま）。

配置担当は `_ui_staging_is_image2()` が true のときだけ image2 パーツを載せる想定。

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート** (`game/scripts/main/Main.gd` がある場所)。

```bash
git apply --check path/to/hp-jobs-external/deliverables/job-012/patches/001-ui-staging-image2-flag.diff
git apply path/to/hp-jobs-external/deliverables/job-012/patches/001-ui-staging-image2-flag.diff
python3 path/to/hp-jobs-external/deliverables/job-012/tests/test_job012_static_flag.py .
```

タイトル/セーブ配置パッチが後から来る場合は、この 001 のあとに番号順で当てる。

## パッチ一覧

| file | 内容 |
|---|---|
| `patches/001-ui-staging-image2-flag.diff` | `ui_staging_mode` / `_configure_ui_staging_arg` / `_ui_staging_is_image2`。title/save 非変更 |

## 本体へパーツを置く場所（配置パッチ用。このコミットでは置かない）

ファイル名は固定。パッチに PNG は埋め込まない。

```
res://assets/ui/image2_batch1/
  startup_backdrop_v001.png
  startup_vignette_v001.png
  main_menu_frame_c48_v001.png
  save_slot_frame_c32_v001.png
  ruby_primary_button_normal_v001.png
  ruby_primary_button_focus_v001.png
  iron_secondary_button_normal_v001.png
  iron_secondary_button_focus_v001.png
```

仕事板: `materials/ui_parts_batch1_image2/` を上記へ同名コピー。  
`age_gate_frame_c128_v001.png` / `confirm_modal_frame_c48_v001.png` / `legal_scroll_frame_c48_v001.png` は title/save に出さない。

## カンプ実測表

配置パッチ未着のため未記入。正は `/workspace/redraw/ideal0819/03_title.png` と `05_save.png`（1280×720）。composite preview は参考、食い違い時はカンプを正。

## ミラーでは検証できなかった点

- Godot headless 未実行（ミラー asset-stripped）
- フラグONの実機見た目（配置パッチが無いので ON でも現行と同一）
- 遷移待ち 0.35s の実行アサート（配置パッチ側の headless で行う）

## 要判断

1. ミラーに `--ui-staging` が無かったので新設した。本体に別実装があるならそちらへ寄せる。
2. タイトル/セーブ配置は別担当待ち。この PR 時点では画面パッチを発明していない。
