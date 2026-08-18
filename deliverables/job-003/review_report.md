# hp-game-share コードレビュー（job-003）

本報告は未実行・静的解析による。実行環境がなく動作確認していない。
対象は `https://github.com/4466hikaru/hp-game-share`（branch `main`、`gh api` 遠隔読取のみ。clone なし）。

読取範囲の中心: `game/scripts/main/Main.gd`（25,230行 / 約1,519 func）、`SaveStore.gd`、`EnemyBehavior.gd`、`BattleProfileRuntime.gd`、`ProgressionEvaluator.gd`、`content/*.json`（構造）、`docs/main-gd-split-plan.md`、テストファイル一覧。R18本文はミラーで空。推測した箇所は末尾に申告する。

---

## ① アーキテクチャ所見（設計文書。大規模書き換えの実施提案ではない）

`Main.gd` は `extends Node2D` の単一オーケストレータで、状態機械（約30 STATE_*）、戦闘シミュレーション（Dictionary配列の敵/弾/宝石）、ADV、セーブ、UI構築、描画、audio、ワールドマップ、ダンジョン境界店、approved UI wiring B1–B3 を同居させている。既存 `docs/main-gd-split-plan.md`（2026-07-11、当時19,736行）は現行25,230行より古いが、方針は今も妥当である。

**分割方針（ストラングラー / 設計のみ）**

Main はオーケストレータとして残し、葉のサブシステムを純粋クラスまたは専用 Node へ切り出す。1切り出し=1コミット。合格条件は既存計画どおり (1) 対象の headless テスト追加 PASS (2) `tools/playtest/run-all-stages.sh` の PLAYTEST_RESULT 前後一致 (3) content validator PASS、ノイズdiffなし。

| 順 | 切り出し対象（現行の塊） | 行き先（案） | 規模感 | リスク |
|---|---|---|---|---|
| 1 | `screen_audit_*` / playtest / fx_p1 evidence（QA専用） | `scripts/qa/` | 小（~20 func） | ゼロ。ゲームプレイ非干渉 |
| 2 | `transition_*` / overlay / battle_result_darken | `scripts/ui/TransitionDirector.gd` | 中（~60 func） | 低。状態機械が比較的自己完結 |
| 3 | ADV: `scene_*` / age_gate / adult_viewer / localization表示 | `scripts/adv/` | 大 | 中。セーブの seen/completed に触れる |
| 4 | 戦闘ループ: spawn / weapons / projectiles / enemies / gems / hazards | `scripts/combat/CombatSim.gd`（データは Dictionary のまま） | 大（`_update_playing` 配下） | 中。決定論と playtest 一致が必須 |
| 5 | dungeon round / boundary shop / carryover / battle profile 適用 | `scripts/dungeon/DungeonDirector.gd` | 中 | 中。`BattleProfileRuntime` は既に分離済み |
| 6 | save normalize / migration / slot meta / progression apply | `scripts/save/`（`SaveStore` は既に分離） | 中 | 高。セーブ互換。設計レビュー必須 |
| 7 | world_map_* / world_tile / region01 draw | `scripts/world/`（`WorldMap.gd` / `WorldTileMap.gd` は既に部分分離） | 大 | 中 |
| 8 | 即時モード描画・演出プール（damage number / gem burst / death / shake） | `scripts/hud/` | 中 | 低 |
| 9 | inventory / shop / sub_equipment / companion rank | `scripts/meta/` | 中 | 中。セーブ互換 |

**やってはいけないこと（本報告の範囲外）**

- Main.gd の一括リライト、クラス階層の全面再設計、戦闘の Node 化（Area2D 化）を「今やる仕事」として提案しない。
- UI mass batch（`Stage4MassBatch1–6`、`UiWiringB*`）は Main から preload されているが、分割第1波に含めない。描画スキンと状態機械が絡む。

現行ですでに切り出されているもの: `SaveStore`、`EnemyBehavior`、`BattleProfileRuntime`、`ProgressionEvaluator`、`WeaponPickPool`、`RunRngStreams`、`VoicePlayback`、WorldMap/WorldTileMap シーン。これらを壊さず、Main 側の呼び出し面だけを薄くする。

---

## ② バグ・危険コード（重要度順、最大30件）

各件3行以内。確度は「確実」または「疑い」。すべて未実行・静的解析。

1. **[高] 確実** `Main.gd:15852-15856` / `18167-18168` / `18962-18963`  
   `_update_playing` は `_update_enemies` のあと `run_state` を見ない。接触死で `_game_over()` した同一フレームに `_update_gems` → `_start_level_up()` が走り、`STATE_GAME_OVER` が `STATE_LEVEL_UP` に上書きされる。強化確定 `_finish_level_up_choice` は無条件で `STATE_PLAYING` に戻す。

2. **[高] 確実** `Main.gd:19214-19228` / `20851-20856`  
   `_game_over` は `already_game_over` でも `_apply_dungeon_fail_rewards` と `_record_run_history` を再実行する。`failRewardIds`（例: `reward.material.ashen_scrap`）と履歴行が二重化され、`_write_save_data` も二重。`_update_enemy_projectiles:18128-18131` からも再入する。

3. **[高] 確実** `Main.gd:18115-18116` / `344-345`  
   敵弾はプレイヤーから 1400px 超で破棄。戦闘カメラは `BATTLE_MAP_DEFAULT_SCREEN_MULTIPLIER = (4,4)` で論理マップが約 5120×2880。遠距離弾・場外射出が途中消滅する。

4. **[高] 確実** `Main.gd:2910-2935` / `21082-21092` / `22123-22124`  
   `content/buffs.json`（ミラーに存在、9,570B）を `_load_content` が読まない。`_buff_by_id` / `carryoverCaps` / `carryoverRules` は常に空。バフ解放は ID だけセーブされ、引き継ぎ上限はハードコード fallback になる。

5. **[中] 確実** `Main.gd:15778` / `20603-20604`  
   ラン中 `player.characterId` は常に `MASTER_CHARACTER_ID`。選択ヒロインは `selectedHeroineId`。`_record_run_history` は `characterId`/`characterName` に Master を書く。履歴・シェア文がヒロインと一致しない。

6. **[中] 確実** `Main.gd:19343-19348` / `18621`  
   `_get_enemy_data` / `_get_weapon_data` / `_available_upgrade_candidate_pool` が `content["enemies"]["enemies"]` 等を直接参照。`_load_json` 失敗時は `{}` のため、最初のスポーン／レベルアップで実行時エラー。`_content_items` は安全なのに戦闘ホットパスだけ未使用。

7. **[中] 確実** `Main.gd:22598-22609`  
   `_set_message` / `_update_message_timer` が `message_label` を無ガード参照。`_load_content` → `_apply_selected_stage` は `_build_ui` より前。現状その経路は `_set_message` を呼ばないが、監査・初期化の呼び出し追加で即クラッシュする。

8. **[中] 疑い** `Main.gd:3186-3193` / `859-861` / `1895-1905`  
   `_exit_tree` は BGM/SE を止めるだけ。ヒットストップ中の `Engine.time_scale = 0.05` を戻さず、`UiHoverRuntime` 信号も切断しない。シーン差し替え／再生成で time_scale 残留と二重 connect の余地。

9. **[中] 疑い** `game/scripts/save/SaveStore.gd:80-85`  
   `rename` 成功後に親ディレクトリ fsync が失敗すると、実ファイルはコミット済みなのに `ok:false`。呼び出し側 `_write_save_data` は `save_file_state` を更新せず、次書き込みやユーザー通知が実態とずれる。

10. **[中] 疑い** `Main.gd:19600-19603`  
    `_normalize_save_data` は `unlockedIds` 等を raw 配列の参照コピーのまま採用し、要素型の正規化がない。非文字列・重複が残ると `_save_array_has` / `.has(String)` が外れ、解放判定が黙って失敗する。

11. **[中] 疑い** `ProgressionEvaluator.gd:49-58` vs `Main.gd:22427-22441`  
    Evaluator は `characterAffection[companionId]`、Main の条件判定は companion→`characterId` 変換。現行 `progression.json` は `companionId:"*"` のみなので latent。個別 companion 条件を足すと Evaluator 側だけ永遠に false。

12. **[中] 疑い** `Main.gd:13296-13304` / `19582-19583`  
    シーンスキップは残り choices の affection / routePreference を適用せず `completedSceneIds` に入れる。設定デフォルト `allowUnseenSceneSkip: true`。未読プロローグをスキップすると好感なしで完了扱い。

13. **[中] 疑い** `Main.gd:17253-17268` + `content/stages.json:66-72`  
    `_trigger_stage_event` のバーストは `wave.maxAlive` を見ない（グローバル 120 のみ）。`blue_bat` count=28 などが生存上限を超えて一度に載る。

14. **[低] 疑い** `Main.gd:19132-19135`  
    `player.maxHp` への effect は `maxHp` だけ更新し、現在 HP を連動させない。意図的ならドキュメント不足。最大HP強化直後に見た目と実HPが食い違う。

15. **[低] 疑い** `Main.gd:18943` / `19141-19142`  
    `_apply_upgrade` は `upgrade["effects"]` 必須。`_apply_effect` は `weapon_data[parts[2]]` を float キャスト。JSON 欠落・未知フィールドで実行時エラー。validator 依存。

16. **[低] 疑い** `Main.gd:17777-17798` vs `16952-16972`  
    弾ヒット死と `_defeat_enemy_at_index`（ボンド／召喚）が死亡処理を二重実装。ボス報酬・最終ボス clear の順序が既に微妙に異なり、片方だけ直すと再発する。

17. **[低] 疑い** `Main.gd:17733-17734` / `105-109`  
    プレイヤー弾と敵弾が `MAX_ACTIVE_PROJECTILES=80` を共有。敵弾 64 上限と合わせて、射撃武器が弾切れ（発射失敗）になる。

18. **[低] 疑い** `Main.gd:19229-19231` + ヒットストップ  
    初回ラン死亡は `_transition_to_new_game_first_town()` を即呼ぶ。ヒットストップ中なら `Engine.time_scale` が遷移演出の delta を歪める（`_clear_battle_effects` は `_game_over` から呼ばれない）。

19. **[低] 疑い** `Main.gd:19661-19668`  
    `runHistory` 正規化は Dictionary 以外を捨てるが、必須キー検査がない。壊れたエントリが履歴 UI の `%` フォーマットを壊す余地。

20. **[低] 疑い** `Main.gd:3716-3731`  
    `_load_json` は失敗時 `{}`。`localization/ja.json` と `voice_assets.json` はミラー除外のため、このリポジトリ単体では UI がキー生表示・ボイス無しになる（本体リポジトリでは存在する想定。ミラー固有）。

---

## ③ パフォーマンス懸念（大量スポーン時）

未実行。ホットパスはすべて Main 内の Dictionary 配列走査。

- **スポーン hitch**: `_update_spawning`（`17628-17649`）は `while spawn_timer >= interval` で追いつき、1間隔あたり `spawnCount` 体。フレーム落ち（delta 0.5s、interval 0.05、count 7）で数十体を同一フレーム生成。イベントバーストは `maxAlive` 非拘束（上記13）。
- **ヒット判定 O(弾×敵)**: `_update_projectiles`（`17737-17808`）は毎弾×全敵の `distance_squared_to`。上限 80×120=9,600。pierce 弾は break まで複数敵を見る。空間分割なし。
- **敵更新**: `_update_enemies`（`17822-17845`）は接触に `distance_to`（平方根）。120体で毎フレーム。`EnemyBehavior.update` も `direction.length()`。
- **宝石マージ O(n)**: `_spawn_gem`（`18386-18399`）は `MAX_ACTIVE_GEMS=220` 到達後、毎回全宝石を走査して最近傍に加算。撃破ラッシュでコストが跳ねる。
- **描画**: `_process` が毎フレーム `queue_redraw()`（`922`）。宝石はカリングするが弾・敵の `_draw` ループ自体は全件（`2880-2887`）。`draw_simple_entities` は閾値以上で簡略化する（`2841-2845`）が、ヒット判定コストは残る。
- **ヒットストップ**: `Engine.time_scale=0.05` 中も `_process` は毎フレーム走り、`_layout_ui` と redraw は止まらない。`_layout_ui` は viewport 不変なら early return（`5049-5050`）なのでここは軽い。
- **Dungeon taint**: `_build_dungeon_stage` は `spawnInterval / sqrt(count_multiplier)` と `spawnCount * min(count, 2.25)`。count 上昇で間隔短縮＋同時数増。`maxAlive` 既定 60、グローバル 120。
- **推奨観察指標（未計測）**: playtest は `playtest_peak_enemies/projectiles/gems` を取る。`tests/test_bug_004_peak_entity_thresholds.sh` があるが、閾値の中身と現行上限の対応は未読のまま。

---

## ④ content JSONスキーマの整合リスク

読んだファイル: `enemies`, `weapons`, `upgrades`, `stages`, `dungeons`, `battle_profiles`, `progression`, `project`, `characters`, `scenes`（先頭構造のみ。adult `lines` は空＋`redactedForMirror`）。`buffs.json` はツリー上存在を確認、本文は未読。

| リスク | 根拠 | 影響 |
|---|---|---|
| `buffs.json` 未ロード | `_load_content` にキーなし。`_content_items("buffs", …)` 依存 | バフ名・carryover ルールが常に空。validator はファイルを見てもランタイムは見ない |
| XPカーブ二重定義 | `upgrades.json` の `xpCurve` 配列を `_xp_needed` が使用。`project.json` の `xpCurve.formula` は未参照 | 企画側が project を直してもランに反映されない |
| `enemies[].startsAt` 未使用 | 敵JSONにあるが、スポーンは stage `waves.enemyWeights` / dungeon `spawnWeights` | 時刻ゲートだと思って書いた敵が、ウェイトに入った瞬間から出る |
| ダンジョンIDを `clearedStageIds` に混在 | `_mark_dungeon_clear` が dungeonId と stageId の両方を同配列へ | ProgressionEvaluator の `dungeon_clear` はこれに依存しており現状は整合。別名配列を足すと壊れる |
| companion affection キー不一致 | 上記11。条件は `companionId`、セーブは `characterId` | `*` 以外を足した瞬間に進行停止 |
| ローカライズ／voice ミラー除外 | READMEどおり。`_localized_text` はキーフォールバック | ミラー単体では全UIがキー生表示。本体の欠落検知にはならない |
| scenes の textKey 依存 | `scenes.json` は本文を持たず `textKey` | localization 欠落＝ADVが空。adult は `lines: []` + `redactedForMirror`（本文は想像しない） |
| `stages.json` は3本、ダンジョンは7本の runtime stage | フィールドは JSON、ダンジョンは `_build_dungeon_stage` 合成 | バリデータが stages だけ見るとダンジョン波を検証できない |
| BattleProfile の `grave_rise` フィルタ | `BattleProfileRuntime.gd:93-99` が hazard を実行時に落とす | JSON に残っていても動かない。仕様コメントあり |
| `_available_upgrade_candidate_pool` の必須キー | `id` / `maxRank` / `effects` 直参照 | schemaVersion は1だが、フィールド欠落の型検査はランタイムに無い |

`BattleProfileRuntime.validation_errors` はプロファイル欠落・duration 不一致を `push_error` するだけ（`2938-2940`）。起動は止まらない。

---

## ⑤ テストの穴

テスト資産は厚いが偏っている。`game/tests/` に UI wiring / skin / mass batch / worldmap / save migration / scene skip / battle profile / enemy behavior が多い。`tests/test_bug_00*.sh` はリリースゲート・決定論・peak entity・ボス報酬キャプチャ。

**無い／薄いもの（静的に判断）**

- `_update_playing` の死亡後ライフサイクル（game_over → gems → level_up → PLAYING 復帰）。同一フレーム再入の回帰がない。
- `_game_over` 冪等性（failReward / runHistory 二重）。
- 敵弾 1400px カリングと 4×マップの交差。
- `buffs.json` が content に載りランタイム辞書に入ること。
- 履歴の `characterId` が選択ヒロインであること。
- `_normalize_save_data` の配列要素型・未知キー。
- ProgressionEvaluator の個別 `companionId`（`*` 以外）。
- 未読スキップ時の choice affection 非適用。
- 戦闘の空間コスト（120敵×80弾）のユニットテスト。peak 閾値シェルはあるが、ヒットループ自体は未カバー。
- `Main.gd` 本体を直接 new するテストは監査／playtest 経由が中心。死亡分岐は playtest `flow` がダメージ0（`19166-19167`）のため踏まない。

`test_save_store.gd` は原子書き込みの故障注入（`interrupt_before_commit` 等）を持つが、rename 成功＋fsync 失敗の呼び出し側状態は見ていない（ファイル未ダウンロード、APIツリー上 4,689B）。

---

## 完成定義自己チェック

| 項目 | Yes/No |
|---|---|
| 冒頭に未実行・静的解析の宣言 | Yes |
| ① 分割案は設計文書。大規模書き換えの実施提案なし | Yes |
| ② 最大30件、重要度順、各3行以内、ファイル:行、確実/疑い | Yes（20件） |
| ③ 大量スポーン時の性能 | Yes |
| ④ content JSON 整合リスク | Yes |
| ⑤ テストの穴 | Yes |
| 末尾に本チェックと正直な申告 | Yes |
| R18本文を捏造していない | Yes |
| clone / push していない | Yes |
| パッチは最大3・1ファイル・挙動維持 | Yes（3本） |

---

## 正直な申告

- Godot も headless playtest も未実行。クラッシュ・二重報酬・弾消滅は静的に「そう読める」まで。
- `Main.gd` 25,230行を全行意味解析してはいない。func 一覧を作り、戦闘／セーブ／スポーン／ライフサイクル／ADV／content ロードを重点読取。UI mass batch・approved wiring・描画後半（region01 タイル等）は構造確認のみ。
- 読めなかった／未ダウンロード: `tools/content-validate/validate-content.js`（121KB）、`WorldMap.gd` / `WorldTileMap.gd` 本文、`content/buffs.json` 本文、`content/rewards.json` 本文、`localization/ja.json` と `voice_assets.json`（ミラー除外）、`game/tests/*.gd` 本文の大半。
- `docs/main-gd-split-plan.md` の行数は古い。分割表は現行 func 配置に合わせて再構成した（実施指示ではない）。
- adult シーンは `redactedForMirror=true` 前提で、lines 本文は見ていないし書いていない。
- パッチは「JSONが正しいときの戦闘式を変えない」ガード／参照の安全化／終了時クリーンアップに限定した。死亡後 level_up（所見1）と `_game_over` 冪等化（所見2）は挙動が変わるためパッチ化していない。
