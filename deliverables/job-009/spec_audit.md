# job-009 仕様書と実装コードの矛盾監査

- 監査日: 2026-08-19
- 仕様側: `materials/spec/` 8本（jobs repo `job/009`、親コミットは `origin/main`）
- 実装側: https://github.com/4466hikaru/hp-game-share `main`
  - HEAD: `92ff9cdc66c9aa588f75b3665d03bc98ceea1527`（2026-08-18 17:01 JST / 08:01 UTC）
  - 取得: `gh api` のみ。clone なし。実行・実機なし（静的読取）
- 先行文脈: `deliverables/job-003/review_report.md` を参照したが、数値・行は本ジョブで再突合した
- 注記: ミラーは 2026-08-18 スナップショット。本体側の後続バグ修正（約5件）と画面配線は未反映。該当し得る件は **ミラー鮮度の可能性あり** と付ける
- 方針: 仕様が「未実装」と自己申告し、コードも未実装なら矛盾に数えない（既知ギャップ節）。仕様が現行値・完成定義として書いた数字がコードと違うものだけを A にする。判断はオーナー（所見は「要判断」へ）

---

## 8本の読了+突合済み

| # | 仕様 | 判定 | 突合した実装 |
|---|---|---|---|
| 1 | `10_02_screen_catalog_wave2.md` | 読了+突合済み | `UiScreenRegistry.gd`（49 ID）、`Main.gd` 状態機械・Esc/B・遷移（標本+全135 edge行の数え上げ） |
| 2 | `20_02_weapon_spec.md` | 読了+突合済み | `content/weapons.json`、`weapon_pick_pool.gd`、`Main.gd` weapon_states / startingWeaponIds |
| 3 | `20_03_economy_spec.md` | 読了+突合済み | `shops.json` / `rewards.json` / `upgrades.json` / `dungeons.json`、`Main.gd` wallet/XP/carryover、`RunRewardGrant.gd`、`consts_round.gd` |
| 4 | `20_04_difficulty_spec.md` | 読了+突合済み | `dungeons.json` 25round 全行、`enemies.json`、`Main.gd` MAX_ACTIVE_ENEMIES / taint 乗算 / spawn |
| 5 | `20_05_weapon_evolution_spec.md` | 読了+突合済み | `evolutions.json`、`weapons.json`、`Main.gd` `_available_evolution_choices` / `_evolution_choice_weight` |
| 6 | `20_06_round_return.md` | 読了+突合済み | `dungeons.json` return/streak、`consts_round.gd`、`Main.gd` round result/choice/carryover |
| 7 | `20_systems.md` | 読了+突合済み | `project.json`、content 件数、SAVE_SCHEMA、companionSlots、BGM/SE、scenes |
| 8 | `30_00_protagonist.md` | 読了+突合済み | `characters.json`、`scenes.json` prologue、`Main.gd` MASTER_* / character_select / NEW_GAME_PROLOGUE_SCENE_ID |

一致した現行値（矛盾に数えない、棚卸しのアンカー）:

- 武器9定義の射程/CD/威力/弾数/貫通は `weapons.json` と 20-02-02 / 20-05-02 が一致
- 進化3件の基礎→結果・必須upgrade rank・weight既定100・tag +35 は一致
- XP曲線 `[5,11,18,28,42,60,82,108,138,172,210,252]` と Lv13超 step=max(8, 252-210=42) は `upgrades.json` + `Main.gd:19174-19184` と一致
- 初期 wallet 300 / デバッグ 2400、通貨ID `currency.dark_coin` は一致
- 25wave の duration / maxAlive / enemyHpScale / enemySpeedScale / xpCurveScale の**データ値**は 20-04-03 表と一致（ただし実効HP/速度は taint 乗算。A-01）
- `MAX_ACTIVE_ENEMIES=120`、DEFAULT_TEXT_SPEED=36 / AUTO=2.5、level-up 候補上限3、7ダンジョン 3+3+3+4+4+4+4=25round、最終R `bossRound`+`canReturnAfter=false`、`returnCarryoverMultiplier=0.45` データ値は一致
- `UiScreenRegistry.ORDERED_SCREEN_IDS` は49、カタログ SCR-01〜49 と ID集合が一致。遷移表の `| to |` 行は135行
- 世界マップ 7地域 / 56 nodes / nodeRewardItems 21、progression 9/9/4、companionSlots initial1/max3、enemies 18、weapons 9、evolutions 3、upgrades 21 は 20_systems 記載と一致（shops/buffs/scenes/SE/rewards/schema は不一致）
- `rewards.json` 112定義に type=`currency` item は0件（20-03「経路のみ・供給値なし」と一致）
- 主人公名入力UI・`{name}` プレースホルダは scenes の残存 lines に0件。speaker は system + 姫のみ

---

## 既知ギャップ（仕様が未実装と明記しており、ミラーも未実装。Aに数えない）

姫=武器ビルド W-01〜W-06 / PB-REQ-01〜07: `ownerCompanionId` / `targetCompanionId` / `weaponDefinitionId` / `tier` / `attributes` は Main.gd に0ヒット。`weapon_states` は runtime weapon ID を key にし同一ID2本を持てない（20-05-04 記載どおり）。属性一致ダメ増も未実装。これらは仕様の自己申告どおり。

ただし **部分実装が決裁と食い違うもの**（グローバル4枠フィルタ、squad 6、主人公操作が姫選択のまま）は下記 A に入れる。

---

## A: 仕様と実装の矛盾

### A-01 高 — 25wave表の HP/SPD は実効値ではない（taint が追加乗算）

- 仕様: `20_04` §20-04-03 表（例: 墓所 R3 HP=1.000 / SPD=1.000）。§20-04-02 は taint を「存在し得るが、25wave数表の主補正は上記scale」と書く
- 実装: `Main.gd:14858-14861` で `round_hp_scale = enemyHpScale * taint.hp`、速度も同様。`taint.count` は spawnCount と spawnInterval にも入る（14859, 14864, 14870）
- 実データ: 全7ダンジョンで R1 taint.hp=1、R2=1.2、R3=1.45、R4=1.7。墓所 R3 の実効HP倍率は 1.000×1.45=1.45。玉座 R4 は 1.850×1.7=3.145
- 所見: 表を「見た目の設定値」とするか「実効圧力」とするか。プレイヤーが感じる難度は実効値
- 要判断: 表を taint込みに直す / taintを1固定にする / 仕様の「主補正」表現で足りる、のどれか

### A-02 高 — `buffs.json` を Main が読まないため、ダンジョン別 carryover 基礎率が全部 fallback 0.1

- 仕様: `20_03` §20-03-04 / ECO-U-03。carryover は rule の基礎率×深度×出口倍率。`20_06` も rule データ依存と明記
- 実装: `_load_content`（`Main.gd:2910-2935`）に `buffs.json` が無い。`_carryover_rule_by_id`（21091-21092）は `content["buffs"].carryoverRules` を読むため常に空。`baseCarryoverRate` fallback は 0.1（20978）
- 実データ: 墓所/狼牙=`carryover.default`(0.1)、溶鉱炉=`material_focused`(0.08)、修道院=`defensive`(0.12)、観測台=`offensive`(0.1)、大聖堂=`growth`(0.11)、玉座=`final`(0.13)。**7ダンジョン中5件が仕様データと違う基礎率で計算される**
- **ミラー鮮度の可能性あり**（job-003 指摘#4。本体の後続修正で load が足された可能性）
- 所見: 実装バグとして load を足すのが自然だが、ミラー後修正の有無は本体で確認
- 要判断: 本体 HEAD で `_load_content` に buffs があるか先に確認してから仕様/コードのどちらを正とするか

### A-03 高 — 同時同行は最大3人、実装の run_squad は解除済み姫を最大6人入れる

- 仕様: `20_02` W-02「同時同行は最大3人なので最大12武器」。`20_systems` / `companion_equipment.json` `maxSlots=3`。`project.json` `maxCompanionSlots=3`
- 実装: `SQUAD_MAX_SIZE := 6`（`Main.gd:82`）。`_build_run_squad`（16579-16597）は選択キャラに加え、解除済みなら `starting_squad_limit`（既定6）まで全員追加。companionSlots の 1/2/3 を見ない
- 所見: 「ラン中オービット部隊」と「恒久同行枠3」が別システムとして残っている。プレイヤーには3枠UIと6人同時攻撃が並立して見える
- 要判断: squadをmaxSlotsに揃える / 3枠は編成UIだけで戦闘は全員、のどちらが決裁か

### A-04 高 — streak / 続行倍率の「現行値」が仕様内でもコードでも一致しない

- 仕様:
  - `20_06-02`: 現行配列 `[1.0, 1.3, 1.7, 2.2]`
  - `20_06-04` 採択B: `1.0 / 1.35 / 1.85 / 2.45`（仮）
  - `20_06-04` 「現行読取値」: 帰還55% / +8% / streak 1.0/1.3/1.7/2.2
  - 同じ節の完走式: `1.0+0.10×(完了round-1)` → 1.0, 1.10, 1.20, 1.30
- 実装: `_dungeon_streak_multiplier_for_completed_rounds`（16403-16404）は JSON の `streakMultiplier` を使わず `RoundRules.continue_reward_multiplier` = `1.0 + 0.10*(n-1)`（`consts_round.gd:6-11`）
- データ: 全7ダンジョン `streakMultiplier=[1, 1.1, 1.2, 1.3]`（コピーは `Main.gd:14911` だが計算未使用）、`returnCarryoverMultiplier=0.45`、`continueRewardMultiplierPerRound=0.1`（後者は stage 構築時に RoundRules 定数で上書き `14917`）
- 画面表示: 帰還ボタン「引継 %.0f%%」（16355）は 45%
- 所見: プレイヤーに見える続行倍率は 1.0/1.1/1.2/1.3。B案の 1.35/1.85/2.45 も「現行読取値」55% も現行コードではない
- 要判断: 正とする数値セット（D-31の45%/+10%式 / B案streak表 / JSON配列 / 画面に出す%）

### A-05 高 — 敗北報酬の一度だけ付与がコード上保証されない

- 仕様: `20_06` R-T-04 / §20-06-03。`failRewardIds` は一度だけ。round 報酬は `applied_dungeon_round_reward_indices` で一度だけ
- 実装: round 報酬は 16362-16365 で idempotent。`_apply_dungeon_fail_rewards`（20851-20856）と `_apply_dungeon_reward_id`（20872-）に同等ガードが無い。`_game_over`（19214-19228）は `already_game_over` でも fail 報酬と履歴を再実行する
- **ミラー鮮度の可能性あり**（job-003 指摘#2。後続修正の候補）
- 所見: セーブの素材二重付与になり得る
- 要判断: 本体で再現するか。仕様の「一度だけ」を正にするなら fail 経路にガードが要る

### A-06 中 — W-07「姫ごと4枠満杯」vs 実装はラン全体4枠

- 仕様: `20_02` W-07 / 20-02-04 手順3。姫ごと4枠が満杯のときその姫の新武器を抽選から除外
- 実装: `weapon_pick_pool.gd:7-13` `MAX_WEAPON_SLOTS=4` を `owned_weapon_states.size()`（ラン全体の weapon_states）で判定。`Main.gd:18626` で level-up 候補に適用。姫別枠ではない
- 所見: VS準拠の「プレイヤー4枠」実装。決裁は姫ごと4×3=12。部分実装が決裁を狭く実現している
- 要判断: 現行4枠を暫定正とするか、姫ごと4の未実装として W-07 完成定義を据え置くか

### A-07 中 — 店の商品数・在庫枠

- 仕様: `20_03` 「7店・計31在庫枠」。`20_systems` 「shops.json: 1通貨、21品、7店」
- 実装: `shops.json` 店7（一致）、items 23（うち provisional gift 2）、inventory 行 33。価格フィールドは `buyPrice`（`Main.gd:11206-11207`）。仕様は `price`
- 内訳: gift 2品を除くと21品。在庫は black_forest_inn の gift 2枠を除くと31。仕様作成後に gift 仮データが足された形
- 所見: 数え方を「本商品21/31」に固定するか、gift込み23/33を現行値にするか
- 要判断: gift を経済台帳に含めるか（FL-03 仮）

### A-08 中 — 価格倍率 `priceScale` が実装済み vs 経済仕様は「未決の価格倍率を追加しない」

- 仕様: `20_03-03` 「未決の価格倍率・リロール・ロックを追加しない」。ECO-U-02 も価格式未決。一方 `20_systems` は「店ごとの価格倍率/在庫」を実装事実として書く
- 実装: 7店 `priceScale` 1.0 / 1.05 / 1.1 / 1.15 / 1.2 / 1.25 / 1.35。購入は `buyPrice * priceScale` を round（11206-11207）
- 所見: 20_systems と 20_03 が食い違う（B-03）。コードは倍率が生きている
- 要判断: 現行 priceScale を正として 20_03 を更新するか、倍率を1.0に戻すか

### A-09 中 — D-32「戦闘用の別絆値を作らない」vs ラン中 bond ゲージ

- 仕様: `20_03` D-32 / `20_systems`。戦闘とイベントの絆は `characterAffection` 共通。別パラメータを作らない
- 実装: `BOND_GAUGE_MAX=100`、`BOND_GAIN_PER_SECOND=7.5`（Main.gd:87-88）。squad member の `bond` / `bondGauge` が時間で溜まり、満タンで bondSkill 発火（2425, 16775, 24906）。`characterAffection` とは別変数
- 所見: 「スキルゲージ」と呼べば D-32 の外、仕様上の「絆」と名前が衝突する
- 要判断: ゲージを affection と切り離して改名するか、D-32 の対象に含めるか

### A-10 中 — SAVE_SCHEMA_VERSION 16 vs 仕様15

- 仕様: `20_systems` §1 セーブ「Mainは SAVE_SCHEMA_VERSION=15」
- 実装: `Main.gd:164` `const SAVE_SCHEMA_VERSION := 16`
- 所見: 仕様の読取日（2026-07-28）以降に +1。セーブ破壊そのものではないが、migration 話が15前提で書かれている
- 要判断: 仕様の版数を16へ追記するだけか、15→16の差分を仕様化するか

### A-11 中 — 画面カタログの行番号・「未コミット」がミラー HEAD と一致しない

- 仕様: `10_02` front matter `current_game_revision: 008746240edaef2c39f876832be31d6d9003d2b4`。各節が `Main.gd:NNNN` を source に持つ。自ら「現game HEAD との一致は未検証（SCR-G01）」と書く
- 実装ミラー HEAD: `92ff9cdc66…`。カタログが boot_splash に付ける `Main.gd:7055-7069` は、ミラーでは `_continue_town_from_save_data`（町続き判定）。F8 はカタログ 2492-2502、ミラーは 2490-2492
- 同じカタログ / `20_systems` は「Esc復帰は未コミット」と書く。ミラーでは `_return_from_dungeon_info` → region_menu（11286-11293）、`_return_from_world_map` → town_menu（8557-8569）、town Esc → `STATE_TOWN_TITLE_CONFIRM`（2653-2655, 6362）がコミット済み
- **ミラー鮮度の可能性あり**（カタログは本体 0087462 側。job-005 配線以降の差分）
- 所見: 49画面ID集合と135 edge「表の行数」は一致。行番号引用はミラー照合に使えない
- 要判断: カタログの正本をミラー SHA に張り直すか、本体 HEAD に張り直すか（本ジョブはミラー正）

### A-12 中 — 主人公表示名 `Master` / 操作対象が姫

- 仕様: `30_00` P-04 無名・デフォルト名なし。P-12 操作対象は主人公（現行は姫選択の旧方式、と自己申告の乖離）
- 実装: `MASTER_CHARACTER_ID="char.master"` / `MASTER_DISPLAY_NAME="Master"`（83-84）。`player.characterId` は常に master（15778）。選択姫は `selectedHeroineId`。`characters.json` は姫が `startingWeaponIds` と `spriteAssetId=*.sprite.player` を持つ。名前入力UIは無い（P-04 一致）
- 所見: 「無名」と英語 Master が衝突。P-12 の既知乖離は残ったまま
- 要判断: 表示から Master を消す時期と、操作対象切替の順序（P-12 が未定義と明記）

### A-13 中 — プロローグ差し替え「未着手」だが `scene.prologue` は配線済み

- 仕様: `30_00` P-20「`scene.prologue_akari` は legacyOnly。v2 本文への差し替えは未着手」
- 実装: `NEW_GAME_PROLOGUE_SCENE_ID := "scene.prologue"`（174）。`scenes.json`: `scene.prologue` は `scriptPass=common_route_v2_2026-07-15`、lines 96。`scene.prologue_akari` は legacyOnly のまま lines 7
- 所見: 差し替え未着手は事実ではない。本文が P-20 の3点（装置破損 / 姫対立 / 帰る動機）を満たすかは ja.json 除外のため未確認（正直申告）
- 要判断: P-20 の実装状態を「v2 シーンは配線済み、第三者読みチェック未了」に直すか

### A-14 中 — pause「タイトルへ」が確認なし

- 仕様: `10_02` SCR-32 完成定義「タイトル離脱は確認を経る」。`20_systems` 2026-07-27 採用は town_menu→タイトル確認（pause は対象外に読める）
- 実装: `_show_pause_menu`（7637）「タイトルへ」→ `_transition_to_title_menu` 直。town だけ `_transition_to_town_title_confirm`
- 所見: 町とポーズでポリシーが違う
- 要判断: pause にも確認を足すか、完成定義から確認を外すか

### A-15 低 — 件数の古い棚卸し（仕様が「現行」と書いた数がミラーで増えている）

| 項目 | 仕様 | ミラー |
|---|---|---|
| rewards 定義 | `20_03` 108 | `rewards.json` 112 |
| scenes | `20_systems` 87 | `scenes.json` 93（adult 49 / safe 27 / suggestive 16 / all 1） |
| buffs | `20_systems` 9 | `buffs.json` 19 |
| audio SE | `20_systems` 22 | `audio.json` se 40（bgm 7 は一致） |
| BGM 方針 | D-07 当面1曲 | runtime ID 7本（`20_systems` 自身が乖離と既記） |

- 所見: 2026-07-28 読取の棚卸しが 08-18 ミラーより古い
- 要判断: 件数を現行値に更新するタイミング

### A-16 低 — `continueCarryoverBonusPerRound=0.02` はデータにあるが計算未使用

- 仕様: `20_06-02`「全ダンジョン 0.02 をデータが保持。使用経路の回帰テスト要」
- 実装: stage へコピー（14918）のみ。`_dungeon_carryover_bonus_delta`（20963-20984）の式は `base_rate * depth_ratio * exit_multiplier + companion_bonus * 0.2`。0.02 項なし
- 所見: 仕様も「要回帰」と既記。死にデータ
- 要判断: 式に入れる / データから消す / 仮値として放置

### A-17 低 — `project.json` の死にデータが仕様の現行値と衝突しうる

- `playerDefaults.startingWeaponSlots: 1`（W-01 は0）。Main.gd に `startingWeaponSlots` ヒット0
- `xpCurve` formula base=6 linear=4 power=1.35（生きているのは `upgrades.json` 配列。`Main.gd:19175`）
- 所見: 仕様 20-03 は upgrades を正としており、project の式は未記載の穴（C-07）でもある
- 要判断: project.json の曲線/枠数を消すか、将来契約として残すか

---

## B: 仕様同士の矛盾

### B-01 高 — 帰還/続行の数値表が同一ファイル内で3種類

- `20_06-02` 現行 streak `[1.0,1.3,1.7,2.2]` かつ完走式 `1.0+0.10×(n-1)`
- `20_06-04` 「現行読取値」55% / +8% / 1.0/1.3/1.7/2.2
- `20_06-04` 採択B 45% / +10% / 1.0/1.35/1.85/2.45
- `20_03-04` D-31 は 45% / +10% のみ（streak 配列なし）
- 実装は A-04 参照。仕様だけでも「現行」が二重
- 要判断: 「現行読取値」行を削除して D-31 + RoundRules を正とするか、B案streakを別途実装するか

### B-02 中 — 商店の数え方

- `20_03`: 7店・31在庫枠。価格は商品の `price`
- `20_systems`: 21品・7店・店ごとの価格倍率
- gift 仮2件の有無で 21/23・31/33 が割れる。フィールド名 `price` vs `buyPrice`
- 要判断: 経済台帳のカウント規則（provisional を含めるか）

### B-03 中 — 価格倍率は未決か実装事実か

- `20_03` ECO-U-02 / 境界「未決の価格倍率を追加しない」
- `20_systems` 「店ごとの価格倍率/在庫」を実装済み列に書く
- 要判断: 20_03 を「現行は priceScale あり、恒久値は未決」に直すか

### B-04 中 — level-up 候補数 3 vs 画面カタログの 1–4 キー

- `20_03-03` 候補数3。`Main.gd:220` `LEVEL_CHOICE_BUTTON_COUNT := 3`
- `10_02` SCR-33「候補をクリック/1–4/パッド」。実装は KEY_1..KEY_4 を受け、KEY_4 は `_apply_choice(3)`（2507-2518）
- 要判断: キー4を消すか、カタログを 1–3 に直すか（4本目を将来枠として残すか）

### B-05 中 — W-07（姫ごと4枠除外）と 20-05（現行は単一開始武器・同一ID2本不可）

- 決裁済み完成定義と、現行進化仕様の「1本置換」が並立。20-05 は分離を書いており意図的だが、W-07 を「現行実装の完成定義」と読むと 20-05 と衝突
- 要判断: W-07 を姫ビルド導入後の AC に限定する文言にするか

### B-06 低 — 戦闘HUD「現行構造を維持」(D-05) vs カタログ完成定義「HP全桁・重ならない」

- `20_systems` D-05。`10_02` SCR-29/30 完成定義は桁切れ修正を Yes 条件にする。方針としては両立しうるが、「維持」と「直せ」が並ぶ
- 要判断: D-05 の範囲（レイアウト維持 vs バグ修正含む）を一文で固定

---

## C: 仕様の穴（実装にあるが8本に無い／不十分な挙動）

仕様が「未決」「スタブ扱うな」と既に書いているものは重複して短く書く。

### C-01 中 — 境界ショップ（リロール / ロック / 価格）

- `STATE_BOUNDARY_SHOP`、`boundary_shop_rerolls_used` / `lock_active` / `free_rerolls`（Main.gd:51, 542-547）。`20_03` はリロール・ロックを未決で追加禁止と書くが、コードパスは存在する
- `10_02` SCR-32 は「boundary_shop も pause と同ID再利用」とだけ触れる
- 要判断: 製品対象か、playtest専用か、仕様化してECO-U-02を更新するか

### C-02 中 — 棺復活（20秒）

- `REVIVE_SECONDS := 20.0`、`COFFIN_REVIVE_PICKUP_RADIUS := 72.0`（85-86, 17135-17153）
- 8本に復活ルールなし。敗北=ラン終了（20-06）と並立しうる
- 要判断: 製品仕様に入れるか、デバッグ/旧モードとして隠すか

### C-03 中 — 召喚石

- `SUMMON_STONE_*`（94-97）、dungeon_info から summon_select。SCR-19 は画面として存在。経済・戦闘仕様8本は効果量 72 / 半径 430 / 4秒を書いていない
- 要判断: 戦闘仕様へ数値を上げるか、画面カタログのみで足りるか

### C-04 中 — 宝箱

- `TREASURE_CHEST_REWARD_COUNT := 3` 等（99-101）。8本にチェスト報酬ルールなし
- 要判断: 報酬仕様へ上げるか

### C-05 中 — battle_profiles（A/B/C と boundary）

- `content/battle_profiles.json` を load。carryover の depthRatio 分岐（20970-20975）や `_uses_battle_profile_boundaries` が難度・経済に介入
- 20-04 の正は `dungeons[].rounds[]`。プロファイル上書きの優先順位が8本に無い
- 要判断: プロファイルをデバッグ専用と明記するか、難度仕様の主変数に含めるか

### C-06 中 — hazard `grave_rise` / `curse_fog`

- `Main.gd:17293`。20-04 DIF-U-04 が「スタブを実装済み扱いするな」と既記。発火はあるが仕様化されていない
- 要判断: DIF-U-04 のまま据え置くか（推奨は仕様どおり未決のまま）

### C-07 低 — `game/resources/content/` がミラーに無い

- `Main.gd:3716-3719` は `res://../content/` を先に、無ければ `res://resources/content/`
- `GreyboxRules.gd:5` は `res://resources/content/` のみ
- ミラー tree に `game/resources/content/` は0件（`content/` ルートのみ）。配布ミラー同期のチェックは未実行
- 要判断: ミラーに resources ミラーを含めるか、greybox を content/ 参照に揃えるか（本ジョブ対象外のツール話）

### C-08 低 — 進化 cut-in 英語字幕

- `evolutions.json` `cutinSubtitle`: "Kiriha Awaken" 等。D-06 日本語化・画面仕様の英字0と衝突しうるが、20-05 は現行挙動として cut-in を書くのみ
- 要判断: 字幕を日本語にするか、演出例外にするか

### C-09 低 — F8 `system_menu` が任意 run_state から発火

- 仕様: `10_02` SCR-03 が「実装上は任意 run_state からも発火するグローバル開発ショートカット」と既記。製品隔離は完成定義側
- 実装: `Main.gd:2490-2492` KEY_F8 + `_dev_features_enabled()`
- 穴というより既記。製品ビルドで `_dev_features_enabled` が false になることの8本での受入条件が薄い

### C-10 低 — ラン中 XP 補正の「runScale」実体

- 仕様 ECO-T-05: `max(1, round(baseXP×roundScale×runScale))`
- 実装: `Main.gd:18302` `base xp * options.xpMultiplier * _run_modifier_number("xpMultiplier")`。options.xpMultiplier は round の `xpCurveScale`。第二項は run modifier。名前は仕様と違うが2項構造は一致
- 要判断: 用語をコードに揃えるか（矛盾というより穴）

---

## 仕様が現行値として正しく、実装も一致した範囲（再掲しない）

武器9数値、進化3条件、XP曲線、初期300黒貨、25waveデータ表の scale 生値、round秒、maxAlive、bossRound、canReturnAfter、Esc/B=帰還（`Main.gd:2571-2577`）、level-up3候補、テキスト36字/秒、auto 2.5秒、49画面ID、7×56ワールドマップ、companion slot データ契約（付与ID。ただし squad 実数が A-03）。

---

## 正直な申告（突合できなかった領域と理由）

1. **実行していない。** headless / 実機 / 固定seed プレイなし。A-02 の「基礎率が全部0.1になる」は load 欠落と fallback の静的推論。A-05 の二重付与も制御流の静的推論。
2. **`content/localization/ja.json` はミラー除外**（`MIRROR_README.md`）。`20_systems` の 1,679 strings、P-20 のプロローグ3点が第三者に伝わるか、D-09 の実表示は未確認。scenes の本文は `textKey` のみ。
3. **`voice_assets.json` はミラーに無い**（Main は load する。`_load_json` 失敗時 `{}`）。voices=0 の現行確認は未実施。
4. **R18 `scenes.json` lines は redactedForMirror**（adult 49件）。成人回想と CG 結線は監査対象外。
5. **バイナリ資産なし。** P-02 立ち絵 B顔フードdown、D-04 承認済み立ち絵、HUD桁切れの見た目は未確認。
6. **`game/resources/content/` がミラーに無い。** 配布ビルドがどちらを読むかはパッケージ手順まで追っていない（C-07）。
7. **10_02 の135遷移を全 edge についてミラー行番号で再トレースしていない。** 表の行数は135。ID集合は49で一致。行番号は本体 SHA `0087462` 向けで、ミラーでは標本（boot/title/dungeon_info/world_map/town/round/pause/level_up/game_over）のみ行為を確認した。残 edge の condition 一致は SCR-G01 どおり未検証。
8. **後続バグ修正約5件と job-005 以降の画面配線はミラーに無い。** A-02, A-05, A-11, A-14 は本体で既に直っている可能性。**ミラー鮮度の可能性あり。**
9. **`30_02_spawn_table.md` は本ジョブの8本に含まれない。** 20-04 が参照する敵役割・重みの「正」は未読。`spawnWeights` 合計100と ID 存在だけ確認。moon_knight / night_bloom_witch が通常重みに入る件は 20-04 既知乖離として再確認した（観測台 R2-R4、大聖堂 R3、玉座 R2-R4）。
10. **job-003 の実行時クラッシュ系（同一フレーム game_over→level_up 等）は仕様8本の範囲外として再検証していない。** 仕様矛盾ではなくバグ。
11. **数値は invent していない。** 未計測の fps / 勝率 / 到達Lv は書いていない。

---

## 要判断（オーナー。本監査はどちらを正とも決めていない）

1. 帰還/続行の正の数値セット（D-31 の 0.45 と `1.0+0.10*(n-1)` / B案 streak 1.35… / JSON 配列 / 「現行読取値」55%）— A-04, B-01
2. taint を 25wave 表に折り込むか、taint を無効化するか — A-01
3. `buffs.json` を Main が読むべきか（本体 HEAD の鮮度確認が先）— A-02
4. 戦闘 squad 最大3か6か — A-03
5. W-07 の4枠は姫ごとかラン全体か、現行4を暫定正とするか — A-06
6. gift 仮アイテムを経済台帳に含めるか — A-07, B-02
7. `priceScale` を現行正とするか未決に戻すか — A-08, B-03
8. ラン中 bond ゲージは D-32 の対象か別スキル資源か — A-09
9. プロローグは `scene.prologue`（v2配線済み）を正として P-20 を書き換えるか — A-13
10. pause のタイトル離脱に確認を足すか — A-14
11. 境界ショップ / 棺復活 / 召喚石 / 宝箱 / battle_profiles を製品仕様に上げるか — C-01〜C-05
12. 画面カタログの正本 SHA をミラーに揃えるか本体 HEAD に揃えるか — A-11

---

## 件数サマリ

| 分類 | 高 | 中 | 低 | 計 |
|---|---:|---:|---:|---:|
| A 仕様 vs 実装 | 5 | 9 | 3 | 17 |
| B 仕様 vs 仕様 | 1 | 4 | 1 | 6 |
| C 仕様の穴 | 0 | 6 | 4 | 10 |
| 合計 | 6 | 19 | 8 | 33 |

既知ギャップ（姫ビルド未実装など、仕様自身が未実装と書いたもの）は上表に含めていない。
