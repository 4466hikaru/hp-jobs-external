# job-012 正直申告（フラグ段階）

## ミラーに無かったので新設した

- `--ui-staging` は hp-game-share `92ff9cdc` の Main.gd に無かった。
- `--store-target` / `--store-target=` と同じ様式で `--ui-staging=image2` と `--ui-staging image2` を新設した。
- フラグOFF（未指定・空・image2以外）は `ui_staging_mode == ""`。title/save の builder は未変更。

## 配置を仮決めしていないこと

- タイトル/セーブの NinePatch・ボタン2状態・座標は別担当待ち。
- `age_gate` / `confirm_modal` / `legal_scroll` を title/save に置いていない（このパッチではどの画面にも出していない）。
- composite preview と 03_title カンプの差は、配置パッチが来てから honest に書く。

## 未実行

- Godot headless 未実行。
- `git apply` は本箱の Main.gd コピー（gh api 取得）に対する `--check` のみ。
