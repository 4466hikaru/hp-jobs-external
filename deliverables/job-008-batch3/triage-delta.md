# job-008 第3バッチ triage-delta

第1バッチの全指摘表（やる 61 / やらない 29 / 全指摘 90）は PR#8 `deliverables/job-008/triage.md` を正とする。  
**このファイルはこのバッチで扱った指摘だけ**を書く。job-002 は拾わない。PR#8 / PR#9 の HIGH 済み分は混ぜない（07 二重選択・08 `[仮]`・33 ボタン重なり・44/47 は対象外）。

出典: `deliverables/job-004/ui_visual_review.md`、第1バッチ triage、game 採否済みパッチ。

対象コード: hp-game-share `main` HEAD `92ff9cdc` / Main.gd blob `cf895716`。clone なし。Godot 未実行。

## 扱った指摘

| # | 画面ID | 指摘要約 | このバッチ | 結果 |
|---|---|---|---|---|
| 4 | 02_stage_select | 最上段詳細の右に細い縦線の切れ端 | やる。上カードを 1172 で clip | **Yes**（028） |
| 5 | 02_stage_select | 「出撃する」右の赤装飾が「る」に近い | やる。enter 幅 280 | **Yes**（028） |
| 7 | 03_world_map | 接続線がアイコン中心から外れる | やる。integer snap | **Yes**（029） |
| 9 | 04_objective_log | 3行目だけ長い横線が枠端まで | やる。右 leftover を覆う | **Yes**（030） |
| 10 | 06_town_menu | 「戻る」が枠内で右寄り | やる。井戸を中央へ | **Yes**（031） |
| 12 | 07_shop | 3行目「売り切れ」が価格に被さる | やる。井戸縮小 + 2行。二重選択は batch2 | **Yes**（012） |
| 15 | 09_loading_transition | 「拠点」と「へ」の間が空き | やる。空白を潰す。遷移秒は触らない | **Yes**（032） |
| 16 | 10_dungeon_info | 「帰還 45%」と「続行」の間に剣 | やる。条件を改行 | **Yes**（017） |
| 17 | 10_dungeon_info | 「召喚石」が「出発する」上縁に密着 | やる。8px 上げる | **Yes**（017） |
| 18 | 10_dungeon_info | クリア報酬が省略 | やる。幅 + wrap | **Yes**（017） |
| 20 | 11_summon_select | ヘッダ「選択：…」が省略 | やる。帯幅 580 | **Yes**（033） |
| 23 | 12_character_select | 「戻る」「出撃する」が上寄り | やる。プレート中央 | **Yes**（013） |
| 25 | 13_equipment_list | 右パネル能力が省略 | やる。4行目 wrap | **Yes**（014） |
| 29 | 14_equipment_slots | 右端候補カードが画面外 | やる。4枚を内側へ | **Yes**（015） |
| 30 | 15_equipment_candidates | 比較行が省略 | やる。幅 450 + wrap | **Yes**（016） |
| 33 | 16_gallery | 「回想一覧」が上端で欠け気味 | やる。24px spacer。金枠は 001 | **Yes**（025） |
| 34 | 17_scene_view | 次へ三角が右下端 | やる。+20px inset | **Yes**（034） |
| 40 | 20_options | 「画面」金選択なのに「ゲーム」赤枠 | やる。焼き込み差し替え + hover 抑制 | **Yes**（024） |
| 49 | 27_level_up | 3カード中心が x≈507 | やらない。HEAD は既に≈640 | **No** |
| 51 | 28_boss_reward | 3カード中心が x≈520 | やらない。HEAD は既に≈640 | **No** |
| 55 | 31_dungeon_round_choice | 「続行する」下が切れる | やる。detail 幅 280 | **Yes**（018） |
| 56 | 31_dungeon_round_choice | 「帰還する」下が切れる | やる。018 と同じ | **Yes**（018） |
| 61 | 33_clear | 報酬カード下キャプション省略 | やる。unlock_rows wrap。ボタン重なりは 010 | **Yes**（035） |
| 64 | 35_alert_overlay | 左右非対称・文字が上 | やる。右星 mask + 文字下げ | **Yes**（036） |
| 65 | 36_scene_choice | 本文が画面下端に近い | やる。下マージン 40 | **Yes**（037） |
| 66 | 37_scene_choice_result | 結果文が切れる | やる。幅 0.76 + wrap | **Yes**（023） |
| 67 | 37_scene_choice_result | 名前箱が高すぎる | やる。タブ高 40 | **Yes**（038） |
| 69 | 38_credits_license | 枠外右上の細い縦線 | やる。credits で clip。金枠は 001 | **Yes**（039） |
| 72 | 41_save_load_menu | 左上黒箱にタイトル重複 | やる。Stage4 タイトルを隠す | **Yes**（019） |
| 73 | 41_save_load_menu | 巨大な「ロード」が二重 | やる。フッター文字を空に | **Yes**（019） |
| 75 | 42_save_delete_confirm | 「スロット 1」だけ左寄せ | やる。info card 中央。金枠は 001 | **Yes**（020） |
| 76 | 43_motion_check | QA が枠外に見える | やる。QA 非描画 + シェル不透明。金枠は 001 | **Yes**（027） |
| 80 | 45_enhance_preview | 「リリカ」が「リリ／カ」 | やる。WORD JOINER | **Yes**（021） |
| 81 | 45_enhance_preview | 必要素材が省略 | やる。cost 帯拡幅 | **Yes**（021） |
| 85 | 46_item_detail | 「使う」が画面外・文字上寄り | やる。スロット inset + 上パッド | **Yes**（022） |
| 89 | 49_system_menu | 金枠下辺が Back を横切る | やる。行間/高さ。金枠 inset は 001 | **Yes**（026） |

## やらない（このバッチ）

### 27_level_up / 28_boss_reward — No

HEAD `92ff9cdc` のカード矩形は 1280 画面で既に群中心 ≈640（27: 240–1041 → 640.5 / 28: scale 後 ≈161–1120 → 640.4）。  
job-004 の x≈507 / x≈520 は Festival ショーケース（LV12 / 血薔薇の鞭）。現行 live 27 は B2 approved PNG。  
+130px を足すと現行 HEAD は右へ倒れる。コード変更なし。PNG が左寄せならアート側。

### 44 / 47

本バッチ対象外。batch2 で既に書いた（2px reskin を 72 に寄せるか）。繰り返さない。

### 33_clear ボタン重なり

batch2 010。035 はキャプション wrap だけ。ボタン枠・行間隔・clip helper は触っていない。
