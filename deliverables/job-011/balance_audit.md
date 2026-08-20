# job-011 バランス数値監査 — buffs有効化後の壊れ探し

対象ミラー: `https://github.com/4466hikaru/hp-game-share`  
読取: `gh api` のみ（clone なし）。  
ミラー `main` SHA: `92ff9cdc66c9aa588f75b3665d03bc98ceea1527`（pushed_at 2026-08-18 19:09 JST）。  
比較用に同リポ branch `fix/review-high-confidence`（Main.gd SHA `3a5e2782…`）の `_load_content` も確認した。ゲームコードは変更していない。

**結論（先に）**
- ミラー `main` の `_load_content()` は **いまも `buffs.json` を読まない**。job-009 A-02（2026-08-18）と同じ。**ミラー鮮度の可能性あり**。
- ファイル `content/buffs.json` 自体は存在する。スタジオ修正後にロードされると、carryover の **maxHP cap が fallback +0.5 → JSON +100** になる。1クリアでは +8.5 HP だが、同一ダンジョン周回 12 回で cap 到達。
- 個別バフ19件はロードされても、現行 `Main.gd` は `unlockedBuffIds` を戦闘ステータスに適用しない（解放IDの保存と表示名だけ）。

---

## 0. ツリーとロード経路

| 場所 | 結果 |
|---|---|
| `content/*.json` | 24ファイル存在（本監査の主対象） |
| `resources/content/*.json` | **不在**（404） |
| `game/resources/` | UI greybox/shell のみ。ゲーム数値JSONではない |
| `_load_json` | 先に `res://../content/%s`、無ければ `res://resources/content/%s`（`Main.gd:3716-3731`） |

`_load_content`（`Main.gd:2910-2935`）が読むキー: audio / voice_assets / project / battle_profiles / assets / characters / companion_equipment / credits / dungeons / enemies / evolutions / localization / progression / route_preference / rewards / scenes / shops / weapons / upgrades / stages / themes / towns / worldmap / world_regions / world_tiles。**`buffs` なし。**

`fix/review-high-confidence` では条件付きで `content["buffs"] = _load_json("buffs.json")` が入っている。`main` には無い。

---

## 1. content JSON 読了判定

すべて `content/<file>`。スキーマと件数を確認した。R18本文（`scenes.json` の adult `lines`）はミラーで空＋`redactedForMirror`。中身は想像していない。

| ファイル | 読了 | 中身の要約 |
|---|---|---|
| `content/buffs.json` | 読了 | carryoverCaps 6 / rules 6 / buffs 19 |
| `content/weapons.json` | 読了 | weapons 9（進化3含む） |
| `content/enemies.json` | 読了 | enemies 18 |
| `content/upgrades.json` | 読了 | upgradePool 21 + xpCurve 12要素 |
| `content/evolutions.json` | 読了 | evolutions 3 |
| `content/stages.json` | 読了 | stages 3（各 duration 180） |
| `content/dungeons.json` | 読了 | dungeons 7 |
| `content/battle_profiles.json` | 読了 | defaultProfileId `C`、profiles A/B/C |
| `content/progression.json` | 読了 | conditions 9 / unlocks 9 / milestones 4 |
| `content/project.json` | 読了 | playerDefaults / runRules / 未使用 xpCurve.formula |
| `content/shops.json` | 読了 | items 23 / shops 7 / currency `currency.dark_coin` |
| `content/rewards.json` | 読了 | rewards 112（bundle）。buff_unlock は3件 |
| `content/companion_equipment.json` | 読了 | companions 7 / subEquipmentItems 23 |
| `content/characters.json` | 読了 | characters 9 |
| `content/towns.json` | 読了 | towns 7 / commands 9 |
| `content/world_regions.json` | 読了 | regions 7 |
| `content/worldmap.json` | 読了 | nodes 56 / nodeRewardItems 21ノード |
| `content/world_tiles.json` | 読了 | maps 7 / terrain 8 |
| `content/scenes.json` | 読了（構造） | scenes 93。adult 49件は redacted |
| `content/assets.json` | 読了（台帳） | assets 699。status todo 502 / review 122 / approved 74 |
| `content/audio.json` | 読了 | bgm 7 / se 40 |
| `content/themes.json` | 読了 | themes 3 |
| `content/credits.json` | 読了 | sections 2 / licenseRows 2 |
| `content/route_preference.json` | 読了 | provisional=true。贈り物・専用スキルは仮値 |
| `content/README.md` | 読了 | `buffs.json` を正規ファイルとして記載。`game/resources/content/` 同期の話あり（本ミラーにはそのディレクトリ無し） |

`localization/ja.json` と `voice_assets.json` はミラー除外（`_load_json` は `{}`）。バランス数値の主対象外。読了対象の `content/*.json` は上記24で全件。

---

## 2. ミラーは buffs.json を実際にロードするか

| 経路 | ロードするか |
|---|---|
| ミラー `main` `_load_content` | **しない** |
| `_clamp_carryover_target_value`（`Main.gd:21082-21088`） | `content.get("buffs", {}).get("carryoverCaps", {})`。空なら fallback cap（maxHP **0.5**、他 0.5、CD **-0.25**） |
| `_carryover_rule_by_id`（`Main.gd:21091-21092`） | `_content_items("buffs", "carryoverRules")`。空なら `baseCarryoverRate` fallback **0.1**、`preferredTargets` 無し → dungeon `order % 3` |
| `_buff_by_id` / `_unlock_buff` | 辞書は空。解放は `unlockedBuffIds` に ID だけ積む（`21214-21218`）。**戦闘適用ループは無い**（`unlockedBuffIds` 参照はセーブ正規化のみ、6箇所） |
| branch `fix/review-high-confidence` | ファイル存在時にロードするコードあり。**main 未マージ** |

**ミラー鮮度の可能性あり。** スタジオが「直した」のはプライベート本体側で、share の 2026-08-18 19:09 JST スナップショットには載っていない、が一番自然な読み。以下の数値監査は「JSONが載った場合」と「現行ミラー実効」の両方。

---

## 3. 外れ値・矛盾・死にデータ

深刻度: **高**=詰み/無双化、**中**=体感が変わる、**低**=誤差/死にデータ。  
修正案は方向のみ。数値の決定はオーナー（要判断）。

### 高

| ID | 内容 | 根拠パス | 修正案の方向 |
|---|---|---|---|
| H1 | carryover maxHP cap が未ロード時 +0.5、ロード時 **+100**。`_carryover_value_for_target` は maxHP を `power * 100`。1クリア（profile C・8境界・clear）で +8.5 HP。同一ダンジョン周回 **12回**で cap 100。未ロードでは1回目で +0.5 に張り付く | `content/buffs.json` `carryoverCaps.player.maxHp` / `Main.gd:21074-21088` / `21002-21012`（加算マージ） | cap の桁を他倍率（0.25〜0.5）と揃えるか、maxHP だけ加算上限を別枠にする。周回で積み上がる仕様自体を「ダンジョンごとベスト1」にするか、要判断 |
| H2 | JSON ロード時だけ `carryover.defensive` の `preferredTargets` が生き、`player.damageReduction` が載る。このキーは **carryoverCaps に無い**ので fallback cap **0.5**（50%軽減）。`dungeon.silent_abbey` クリア約10回で cap。未ロード時は rule 空で order%3 に落ち、DR は積まれない | `content/buffs.json` rules / `content/dungeons.json` `dungeon.silent_abbey.carryoverRuleId` / `Main.gd:21053-21056`, `21082-21088` | DR を cap 表に明示する（他と同桁にする / 載せない）。防御ルールの preferredTargets から外す、のどれか |
| H3 | 個別バフの理論積算は無双級（後述）だが、現行コードは未適用。スタジオ修正が「ロード＋効果適用」なら **H1 とは別に**攻撃+1.0・HP+150 等が乗る | `content/buffs.json` `buffs[]` / `Main.gd:21214-21218`（unlock のみ） | 適用するなら stackLimit と carryover の二重取りを禁止。適用しないなら JSON の stack 値は死にデータとしてドキュメントする |

### 中

| ID | 内容 | 根拠パス | 修正案の方向 |
|---|---|---|---|
| M1 | ダンジョン `xpCurveScale` が敵XP倍率として使われる。1ダンジョン **3.4**、最終 **0.65**。敵HPは 1.0→1.85。序盤がXP過多・終盤がXP不足 | `content/dungeons.json` 各 `xpCurveScale` / `Main.gd:14862,14876,17646` | 倍率の向きを「必要XP」か「取得XP」か決め、序盤≤終盤になるよう並べ直す |
| M2 | レベルアップ `pickup_radius` が `multiply 1.45` × maxRank 3 → **約3.05倍**。carryover pickup cap 0.5 と桁が違う | `content/upgrades.json` `pickup_radius` | ランクあたり係数を他 multiply（1.12）に近づける / maxRank を下げる |
| M3 | `magic_bolt_cooldown` `multiply 0.85` ×5 → CD **0.44倍**。carryover CD cap -0.25 と複合するとさらに短い | `content/upgrades.json` / `content/weapons.json` `magic_bolt.cooldown=0.75` / `Main.gd:15654-15655`（床 0.05） | 武器CD強化とプレイヤーCD倍率の合成上限を1本化する |
| M4 | `recommendedPower` と地域 `dangerLevel` が 1..6 のあと **8**（7が欠番）。最終ダンジョンだけ段差 | `content/dungeons.json` `dungeon.blood_king_castle` / `content/world_regions.json` `region.blood_citadel` | 7にするか、8の段差を意図として他数値（HP1.85, dur 720）とセットで説明 |
| M5 | 報酬名と中身が不一致。`reward.buff.status_resist` → `buff.dungeon.max_hp_minor`（耐性ではなく最大HP+30）。`reward.buff.field_mobility` → `buff.dungeon.move_speed_minor` | `content/rewards.json` / `content/dungeons.json` clearRewardIds | 名前を中身に合わせる、または正しいバフIDに付け替える |
| M6 | `unlock_storm_chime` はあるが、嵐鈴の damage/CD 強化が無い。解放しても成長しない | `content/upgrades.json` / `content/weapons.json` `storm_chime` | 強化カードを足すか、unlock を外して進化専用にする |
| M7 | `char.ririsu` の初期武器が進化武器 `starfall_core`（legacy も同じ）。他キャラは基本武器 | `content/characters.json` / `content/weapons.json` `isEvolution: true` | 基本武器にする / ポストゲーム特例として明記 |
| M8 | 最終ダンジョン `maxAlive: 130`。job-003 時点のグローバル敵上限は 120。キャップでスポーンが黙って減る | `content/dungeons.json` `dungeon.blood_king_castle` | maxAlive をグローバル上限以下にするか、上限を上げる |
| M9 | `stages.json` の茨の巨兵イベントだけ `hpMultiplier: 1.6`。他中ボスは 0.6〜0.9。同一イベント列が3ステージにコピー | `content/stages.json` 3ステージの `event.miniboss_180` 相当 | 倍率を他中ボス帯に戻すか、この1体だけボス扱いと明記 |
| M10 | JSONロードで **移動cap が 0.5→0.25 に締まる**。未ロードより移動が弱くなる。体感差あり | `content/buffs.json` `player.moveSpeedMultiplier: 0.25` / fallback 0.5 | cap を他倍率と揃える |
| M11 | JSONルールが生きると攻撃寄りターゲットが減る。profile C・7クリア後のダメージ加算は未ロード **+0.425** vs ロード **+0.244**。ロードのほうが火力は低い（HP/DR/CDは厚い） | 下記シミュレーション / rules の preferredTargets | 「ロード＝全面強化」ではない。ルール配分を見て攻撃も残すか、未ロード fallback を rule と同じにする |
| M12 | ワールドマップパッシブ10種は `nodeRewardItems` から `buff_unlock` されるが、効果未適用。ロード＋適用が付くと取得範囲+0.14、火力+0.05 等が常時 | `content/worldmap.json` `nodeRewardItems` / `content/buffs.json` `buff.worldmap.*` | 適用するなら carryover と加算上限を共有。しないなら報酬をアイテムに変える |

### 低（死にデータ・誤差・プレースホルダ）

| ID | 内容 | 根拠パス | 修正案の方向 |
|---|---|---|---|
| L1 | `enemies[].startsAt` はスポーン条件に使われない（stage/dungeon の weights が正） | `content/enemies.json` / job-003 と同じ | 消すか、weights 生成に使う |
| L2 | `project.json` の `xpCurve.formula` は未参照。実XPは `upgrades.json` の配列 | `content/project.json` / `Main.gd:19174-19184` | 片方に寄せる |
| L3 | `condition.affection.any_60/90` は unlocks/milestones から参照されない。永久に発火しない | `content/progression.json` | unlock に繋ぐか削除 |
| L4 | 付与経路の無いバフ: `buff.dungeon.attack_minor`, `buff.dungeon.pickup_minor`, `buff.companion.*`, `buff.field.*` | `content/buffs.json` vs rewards / worldmap | 付与を足すか削除 |
| L5 | rules の `excludeTags: special_behavior` だが、そのタグを持つバフは0件 | `content/buffs.json` | タグを付けるか exclude を削る |
| L6 | `continueCarryoverBonusPerRound: 0.02` は stage にコピーされるが、delta 計算は `RoundRules.continue_reward_multiplier` のみ | `content/dungeons.json` / `Main.gd:14918` vs `20979-20984` | JSON を使うか、フィールドを削除 |
| L7 | 贈り物 `sellPrice: 0`、provisional | `content/shops.json` / `content/route_preference.json` | 仮値のままなら販売前に再決裁（既に注記あり） |
| L8 | stage ID と theme ID が同名（`library_archive`, `moonlit_garden`）。衝突はファイル跨ぎ | `content/stages.json` / `content/themes.json` | prefix を分ける |
| L9 | 敵 `assetId` が `enemy_blue_bat` 等で `assets.json` に無い（5体） | `content/enemies.json` / `content/assets.json` | 台帳IDに合わせる |
| L10 | `char.common_end` は武器・baseStats なし（システム用） | `content/characters.json` | 戦闘に出さない保証を残す |
| L11 | `moonlit_garden` 報酬に `sceneId` が無い（rewardId はある） | `content/stages.json` | 他ステージと同様に scene を付ける |
| L12 | `boss.blood_king` はリリス仮素材、`visualStatus: placeholder_pending_new_design` | `content/enemies.json` | アート差し替え（バランス外） |
| L13 | `audio.json` に schemaVersion 無し | `content/audio.json` | 他ファイルと揃える |
| L14 | 素材重視ルールの `materialRewardMultiplier: 1.15` は carryover 計算に出てこない | `content/buffs.json` `carryover.material_focused` | 報酬倍率に接続するか削除 |

`carryoverRules` 6本は7ダンジョンから参照されており、ルールID自体の死にデータは無い。`project.runRules.defaultCarryoverRuleId = carryover.default`。

---

## 4. バフ有効化の影響概算（数表）

### 4.1 計算に使ったコード（捏造なし）

クリア時（`Main.gd:20963-20999`）:

- `depth_ratio = 1.0`
- `exit_multiplier = 1.0 + 0.10 * max(0, economyDepthCount - 1)`（`consts_round.gd`）
- `carryover_power = baseCarryoverRate * depth_ratio * exit_multiplier`（コンパニオン補正は0と置いた）
- ターゲット数で割る。maxHP は `* 100`、CD は `* -0.75`
- 加算マージのあと cap

`battle_profiles.json` の default は **C**。各ダンジョン 8境界 → `economyDepthCount=8` → exit **1.70**。

未ロード時: `baseCarryoverRate=0.1` 固定、preferredTargets 無し、cap は maxHP 0.5。

### 4.2 キャンペーン累積（各ダンジョン1回クリア、profile C）

| クリア数 | 状態 | maxHP加算 | ダメージ加算 | CD加算 | XP加算 | 取得範囲 | DR |
|---|---|---|---|---|---|---|---|
| 0 | どちらも | 0 | 0 | 0 | 0 | 0 | 0 |
| 1（墓所） | 未ロード | **+0.5** | +0.085 | 0 | 0 | 0 | 0 |
| 1 | ロード | **+8.5** | +0.085 | 0 | 0 | 0 | 0 |
| 3 | 未ロード | +0.5 | +0.170 | 0 | +0.085 | +0.085 | 0 |
| 3 | ロード | +8.5 | +0.085 | 0 | +0.068 | +0.153 | 0 |
| 6 | 未ロード | +0.5 | +0.340 | 0 | +0.170 | +0.170 | 0 |
| 6 | ロード | +18.7 | +0.170 | -0.064 | +0.162 | +0.247 | +0.102 |
| 7 | 未ロード | +0.5 | +0.425 | 0 | +0.170 | +0.170 | 0 |
| 7 | ロード | +26.1 | +0.244 | -0.119 | +0.162 | +0.247 | +0.102 |

1周目の差はほぼ **HP +0.5 vs +8.5**（他は同じ）。終盤はロード側がHP/DR/CD、未ロード側が生ダメージ。

### 4.3 周回で cap に当たる場合（無双化ルート）

`dungeon.border_catacomb`（default、order 1 → ダメージ+maxHP）を繰り返しクリア:

| | 未ロード | ロード |
|---|---|---|
| 1回 | HP +0.5（即 cap）、dmg +0.085 | HP +8.5、dmg +0.085 |
| 6回 | HP +0.5、dmg **+0.5（cap）** | HP +51、dmg **+0.5（cap）** |
| 12回 | 同上 | HP **+100（cap）**、dmg +0.5 |

`dungeon.silent_abbey`（defensive）ロード時: 約10回で HP 100 かつ DR 0.5。

### 4.4 5分1ランの HP / DPS / ゴールド（派生）

前提は §5。ベース: `project.json` playerDefaults maxHP **120**、武器 `magic_bolt` 30/0.75s → 単発DPS **40**。ゴールドはラン中素材が XP をミラー（`battle_profiles.json` `mirrorsCollectedXp: true`）。

表の「%」は **バフJSONロード後 ÷ 未ロード**。初回ラン（クリア0）は差0なので省略。

| 直前までのクリア | HP 未ロード | HP ロード | HP% | DPS 未ロード | DPS ロード | DPS% | Gold(XP) 未ロード | Gold ロード | Gold% |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 120.5 | 128.5 | **+6.6%** | 43.4 | 43.4 | 0% | 1360 | 1360 | 0% |
| 3 | 120.5 | 128.5 | **+6.6%** | 46.8 | 43.4 | **-7.3%** | 1476 | 1452 | -1.6% |
| 6 | 120.5 | 138.7 | **+15.1%** | 53.6 | 50.0 | **-6.7%** | 1591 | 1687 | **+6.0%** |
| 7 | 120.5 | 146.1 | **+21.2%** | 57.0 | 56.5 | -0.9% | 1591 | 1793 | **+12.7%** |
| 墓所12周（cap） | 120.5 | **220** | **+82.6%** | 60.0 | 60.0 | 0% | （火力cap同じ） | 同左 | 火力は同じ、HPだけ倍近く |

「ロードで全面的に何%強くなる」ではない。**HPは確実に上振れ**、火力はルール配分でむしろ未ロードより弱い区間がある。無双化は **周回で HP100+DR50%** が本体。

個別バフをもし適用したら（現行コードではしない）: dungeon 小バフ最大スタックでダメージ +1.0・HP +150・CD -0.24。ワールドマップ全取得でさらに HP+10、ダメージ+0.05 等。これは表に混ぜていない。

---

## 5. 正直申告

シミュレーション前提:

1. default battle profile **C**（8境界）。`dungeons.json` の roundCount 3/4 だけだと exit は 1.2〜1.3 で、上表より小さい（同方向）。
2. 各ダンジョン **1回 clear**（return 中断なし）。return は `returnCarryoverMultiplier` 0.45 で power が約 1.7→0.45 に落ちる。
3. コンパニオン `carryoverBonus` = 0（ランク効果は未加算）。
4. 5分ランは「墓所相当の敵HP25・魔導弾のみ・常時命中・1発撃破・発射1.33/s」。スポーン上限 2/0.94≈2.13/s より火力が低いのでキルは発射律速。XP倍率は墓所 `xpCurveScale` **3.4**。300秒。
5. レベルアップカードの追加火力/HPは **入れてない**（ランダムで再現不能）。実際の5分はカード分だけ上に乗る。
6. ゴールドはラン中素材＝取得XP。黒貨（`currency.dark_coin`）の永続経済は未シミュレ。境界ショップでの消費も未シミュレ。
7. ヒット/回避/maxAlive/ノックバック/複数武器/進化は未モデル。
8. Godot 未実行。数式は静的に `Main.gd` から写した。
9. `assets.json` 699件は台帳として status 集計まで。1件ずつ画を見ていない。
10. `scenes.json` adult 本文は空。読了は構造と件数。
11. `fix/review-high-confidence` はロード有無の確認に使った。本体の未ミラー差分はこれ以上追っていない。
12. job-009 本文は main に無かった。A-02 は本ジョブで `Main.gd:2910-2935` を再読して独立確認した。

限界: 「5分で何%強いか」は **carryover の開始ステ差**が本体で、戦闘ループの実測ではない。カード運・複数武器・進化を入れると DPS 列は大きく動く。

---

## 6. 完成定義自己チェック

| 項目 | Yes/No |
|---|---|
| content JSON全ファイルに読了判定 | Yes（24ファイル + README。`resources/content` は不在と明記） |
| 外れ値・矛盾の全リスト（深刻度+パス） | Yes（高3 / 中12 / 低14） |
| バフ有効化の影響概算（数表） | Yes（累積・周回cap・5分HP/DPS/Gold%） |
| 正直な申告（前提と限界） | Yes |
| 完成定義チェックボックスは発注書で未変更 | Yes |
| ゲームコード変更なし / main 非push / ミラー非clone | Yes |

---

## 7. 要判断（数値は決めていない）

1. `player.maxHp` carryover cap を 100 のままにするか、他倍率と同じ桁に戻すか。
2. `player.damageReduction` を cap 表に入れるか、defensive ルールから外すか。
3. 個別バフ19件を戦闘に適用するか（今は ID 解放のみ）。適用するなら H3。
4. ミラー `main` に `buffs.json` ロードを同期するか（鮮度）。ロードすると M10/M11 のとおり **移動は弱く・配分で火力も変わる**。
5. `xpCurveScale` 3.4→0.65 の向きは意図か。
6. 報酬IDの名前（status_resist 等）を直すか。
7. 嵐鈴の強化カード不足、リリス初期進化武器を直すか。

本PRはどれも決めていない。
