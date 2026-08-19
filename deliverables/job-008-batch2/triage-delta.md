# job-008 第2バッチ triage-delta

第1バッチの全指摘表（やる 61 / やらない 29 / 全指摘 90）は PR#8 `deliverables/job-008/triage.md` を正とする。  
**このファイルはこのバッチで扱った指摘だけ**を書く。job-002 は拾わない。batch3 CONTRACT は混ぜない。

出典: `deliverables/job-004/ui_visual_review.md`、第1バッチ README / triage、`notes-33-34.md` / `notes-39-44-47.md`（作業メモ。納品本体は本ディレクトリ）。

対象コード: hp-game-share `main` HEAD blob `cf895716`。clone なし。Godot 未実行。

## 扱った指摘

| # | 画面ID | 指摘要約 | 第1バッチ | このバッチ | 結果 |
|---|---|---|---|---|---|
| 11 | 07_shop | 1行目金枠・2行目赤枠の二重選択 | No（focus/hover が1行では切れない） | やる。ホバーを落としてフォーカスのみ | **Yes**（007。Godot 未実行） |
| 13 | 08_sell_inventory | 半透明帯に `[仮]` が乗りアイコンを覆う | No（GDScript に無し。PNG 焼き込みの公算） | やる。live 文字の `[仮]` だけカット | **Yes**（008。Godot 未実行） |
| 46 | 25_world_field_playing | HUD HP/絆の二重描画 | No（再現源未特定） | やる。CombatHudSlots 生存時に leftover hud_panel を隠す | **Yes**（009。Godot 未実行） |
| 48 | 26_dungeon_playing | 25と同じ HUD 二重 | No（同上） | やる。009 と同じ経路 | **Yes**（009。Godot 未実行） |
| 59 | 33_clear | 右下大枠が重なり、黒矩形マスクで背景欠け | No（未着手） | やる。clip + 行間隔 14px | **Yes**（010。Godot 未実行） |
| 62 | 34_game_over | 4小ボタン文字が枠左上、赤装飾が重なる | No（未着手） | やる。clip + leftover mask 拡大 | **Yes**（011。Godot 未実行） |
| 70 | 39_boot_splash | 金縦線 x≈350 が「Nightglow…」「起」を貫く | Partial（001 は kit2 margin のみ。940 分岐） | やらない。安全な直しが無い | **No**（012 なし） |
| 78 | 44_adult_viewer_gate | 金縦線 x≈350 が「ストア設定…」「戻」を貫く | No（reskin 2px 温存） | やらない。要判断 | **No**（013 なし） |
| 86 | 47_new_game_confirm | 金縦線 x≈350 が「現在の…」「スロット 1」を貫く | No（同上） | やらない。要判断 | **No**（013 なし） |
| 44 | 23_reset_confirm | 金縦線 x≈436。上端に短い横突起 | 001 未カバー（StyleBoxEmpty） | やらない。空箱が金線を描く証明不足 | **No**（hide せず） |
| 45 | 24_unlock_confirm | 23と同じ x≈436。右辺無し | 001 未カバー | やらない。同上 | **No**（hide せず） |

## やる（コード）

### 07_shop — Yes

- 指摘: 1行目金枠・2行目赤枠の二重選択
- 直し: approved shop 行の theme hover/focus を空にし、`UiHoverOverlay` の pointer glow を meta で抑止。フォーカスのみ残す
- やらない: 右プレビューと文言の不一致（データ）

### 08_sell_inventory — Yes

- 指摘: `[仮]` がアイコン帯に乗る
- 直し: `_shop_item_product_display_name` が live タイトルの `[仮]` 接頭辞を切る。sell cards / approved 行 / 選択サマリだけ差し替え
- やらない: approved PNG 焼き込みの hide（証拠が無いので発明しない）。データ不一致（売値/所持）

### 25 / 26 HUD — Yes

- 指摘: HP / 絆の二重描画
- 直し: `UiIdealBatch1/CombatHudSlots` があるとき `_update_hud` 経由の leftover `hud_panel` を再表示しない
- やらない: パッシブ文字色（配色）

### 33_clear — Yes

- 指摘: 結果コピー／町へ大枠がギャラリー／タイトルに重なり、黒マスクで背景欠け
- 直し: extra-action TextureRect を live 160×38 で clip。行間隔 6→14px（最終行 bottom 594、町へ y=610 まで 16px）。z-order のみ
- やらない: 「報酬シーン」の暗色。報酬カードキャプション省略。PNG 焼き込み黒帯が clip 後も残る場合はアート側

### 34_game_over — Yes

- 指摘: 4ボタン文字が枠左上、赤装飾が重なる。町へは中央で正しい
- 直し: 同じ clip helper を 140×42 に適用。Button 再固定 + 中央寄せ。leftover mask を `(800,345,480,140)` へ
- やらない: スタッツ枠切れ（Batch5 record_panel 幅）。「敗北結果」左寄せ。mask 色変更

## やらない（正直申告）

### 39_boot_splash — No

現行は 940 分岐 + UiSkin 1px 鉄枠。job-004 の x≈350 金線は 720幅 + 64px 9-slice 時代の線（left=280+64=344）。今のパスでは出ない。72 inset を boot だけ足すと子幅 892+144=1036>940 で契約破壊。leftover 第二 panel はコード上存在しない。

### 44_adult / 47_new_game — No（要判断）

reskin 2px / margin 26 が kit2 72 を直後に上書きする。reskin は StyleBoxFlat の外縁 2px。内側 ornament は無い。2→72 は QG-13（明示 2px 枠）と 940 本文幅を壊しうる。指摘の x≈350 貫通は現行パスでは出ない。2px が唯一の直しならコードは変えない。

### 23_reset / 24_unlock — No

`run_state=STATE_MENU` のまま `_show_menu_shell` → StyleBoxEmpty。空箱は画素を塗らない。hide すると title / ボタン（children）も消える。別 Control の leftover 空箱が x≈436 に残ることは証明できない。証明できるときだけ hide/clip、という指示に従い触らない。
