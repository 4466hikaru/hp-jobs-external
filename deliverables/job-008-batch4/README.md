006 patch file (`patches/006-pause-hex-frames-margin.diff`) is unchanged from the previous commit; already on the refreshed mirror.

# job-008 納品追記: 020/024 を更新ミラーで作り直し

対象コード: `https://github.com/4466hikaru/hp-game-share` HEAD `3fd5cf040647`（実repo `f0ddcf6` 相当、バイト一致検証済みと検収コメント）。Main.gd 25897行。`gh api` で読取。clone なし。本体へは当てていない。

006 pause は本追記で **触っていない**（既に合格・ミラーにも y=566/h=70/bottom 636 が入っている）。

## 完成定義 Yes/No（本追記）

- 020 を更新ミラー HEAD へ関数名コンテキストで作り直し: **Yes**
- 024 を更新ミラー HEAD へ作り直し（言語/入力行を残す）: **Yes**
- apply-check だけでなく適用後に関数名目視/静的検査: **Yes**（`_add_character_portrait_card` は無改変。gdparse/Godot は本箱に無し）
- 正直な申告: **Yes**

## セルフチェック（前回の教訓）

1. `git apply --check` は孤立・連続・逆順とも通る
2. 適用後、`_add_character_portrait_card` の本文は適用前と **バイト一致**
3. `_add_info_card` にだけ `alignment` 引数が付く
4. `_show_approved_b2_options` に言語・入力の2行が残る
5. 静的 Python: 未適用 FAIL / 適用後 PASS
6. パッチ CR=0（LF のみ）
7. Godot headless: **未実行**（本箱に Godot なし。ミラーは asset-stripped）

## 020 `save-delete-align`（42_save_delete_confirm）

ライブ経路は `USE_APPROVED_UI_WIRING_B1=true` の `_show_approved_save_delete_confirm`。前回の `_add_info_card` だけのパッチはフォールバック殻にしか効かず、さらに第3 hunk の `title_label.text = title` が先に出る `_add_character_portrait_card` へ誤爆した。

今回:

- hunk コンテキストに `_menu_content_width` / `_reskin_menu_card_style` を入れ、肖像カードと共有しない
- フォールバック `_add_info_card(..., CENTER)` は残す
- **B1 ライブ**で `ui_text_save_delete_confirm_target_slot_01..03` の Value を中央揃え
- 金枠 001 は未接触

## 024 `options-single-chrome`（20_options）

更新ミラーの `_show_approved_b2_options` には言語/入力の追加行がある。前回パッチは bind04 直後 `_focus` を要求して実HEADで外れた。

今回:

- 言語/入力の2行は **残す**
- `_keep_approved_options_nav_focus_only` を pause と options の間に挿入
- 焼き込み「ゲーム」テクスチャを idle 音量プレートへ、nav は focus overlay のみ
- UiHoverOverlay の `_hover_draw_suppressed` は **更新ミラーに既にある**ので本パッチから外した（no-op を出さない）

## 要判断

なし（ミラーを正とする再依頼どおり。006は再提出しない）

## やっていないこと

- 006 の再提出 / PR#8 への追加
- main 直push / job-002 / 完成チェックボックス書き換え
- Godot 実行
