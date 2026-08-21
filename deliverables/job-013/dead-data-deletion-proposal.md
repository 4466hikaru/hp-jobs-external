# job-013 死にデータ削除提案（実削除なし）

対象ミラー: `https://github.com/4466hikaru/hp-game-share` `main` `92ff9cdc66c9aa588f75b3665d03bc98ceea1527`（pushed_at 2026-08-18 19:09 JST）。`gh api` で 2026-08-21 に再読。clone なし。
出典: job-011 `deliverables/job-011/balance_audit.md` の低（死にデータ）と、job-009 A-02。ID は発明していない。本ジョブでは **1件も削除していない**。

判定の定義（発注の「参照先のないID」「絶対に発動しない条件」）:

- 参照先のないID: content に定義があるが、付与・unlock・報酬・ワールドマップ等の現行 JSON から辿れない
- 絶対に発動しない条件: progression の condition が unlocks/milestones から参照されない、または exclude 条件がマッチ対象0件

## 削除を提案する（実削除はしない）

### 1. 絶対に発動しない条件（job-011 L3）

| ID | ファイル | 再読結果 | 提案 |
|---|---|---|---|
| `condition.affection.any_60` | `content/progression.json` | `unlocks[].conditionIds` と `milestones[].conditionId` のどちらからも未参照。`Main.gd` に `condition.affection` ヒットなし | 削除、または affection unlock に接続 |
| `condition.affection.any_90` | 同上 | 同上 | 同上 |

現行で参照されている condition は `condition.region.01.clear` … `condition.region.07.clear` の7件のみ。affection 2件は定義だけで発火経路が無い。

### 2. 付与経路の無いバフ ID（job-011 L4）

`content/buffs.json` の `buffs[]` 19件を、現行 `rewards.json` / `worldmap.json` `nodeRewardItems` / `dungeons.json` / `companion_equipment.json` / `shops.json` / `stages.json` の `buff.*` 文字列と突合した。

| ID | 再読結果 | 提案 |
|---|---|---|
| `buff.dungeon.attack_minor` | 付与経路なし | 削除、または clearReward に接続 |
| `buff.dungeon.pickup_minor` | 付与経路なし | 同上 |
| `buff.field.haste_short` | 付与経路なし（tag `temporary_field`） | 削除、またはフィールドイベントに接続 |
| `buff.field.recovery_short` | 同上 | 同上 |
| `buff.companion.material_sense` | 付与経路なし | 削除、またはコンパニオン装備に接続 |
| `buff.companion.xp_dance` | 付与経路なし | 同上 |

削除しない（付与経路あり、job-011 L4 の対象外）:

- `buff.dungeon.max_hp_minor` ← `reward.buff.status_resist` の `buff_unlock`（名前は不一致。job-011 M5。削除対象ではない）
- `buff.dungeon.move_speed_minor` ← `reward.buff.field_mobility`
- `buff.dungeon.cooldown_minor` ← `reward.buff.cooldown_focus`
- `buff.worldmap.*` 10件 ← `worldmap.json` `nodeRewardItems` の `buff_unlock`

補足: 現行 `Main.gd` は `unlockedBuffIds` を戦闘ステータスに適用しない（job-011 H3）。付与経路があるバフも戦闘効果は死んでいる。それはロード＋適用の要判断であり、本リストの「JSON 上の参照先なし」とは別件。

### 3. マッチ0件の exclude 条件（job-011 L5）

| 場所 | 内容 | 再読結果 | 提案 |
|---|---|---|---|
| `content/buffs.json` `carryoverRules[].excludeTags` | `"special_behavior"` | `buffs[].tags` に `special_behavior` は **0件**。`Main.gd` にも文字列なし | ルールから `special_behavior` を削る、または該当バフにタグを付ける。**ルール ID 自体は7ダンジョンから参照されており死んでいない** |

`temporary_field` タグは `buff.field.*` 2件が持つ。exclude 側の `temporary_field` は「付与されれば除外される」ので、フィールドバフ自体が未付与な今は実効なし。タグ削除ではなく、§2 のフィールドバフ削除/接続とセット。

## 削除提案に含めない（関連死にデータ・要判断）

job-011 が死にデータとしたが、本発注の「参照先のないID / 絶対に発動しない条件」から外れる、または数値・仕様の決裁が要るもの。

| job-011 | 内容 | 本ジョブの扱い |
|---|---|---|
| L1 | `enemies[].startsAt` はスポーン条件に未使用（使うのは round の startsAt） | フィールド削除の要判断。ID ではない |
| L2 | `project.json` `xpCurve.formula` 未参照。実XPは `upgrades.json` 配列 | フィールド削除の要判断 |
| L6 | `continueCarryoverBonusPerRound: 0.02` は stage にコピーされるが delta 計算は未使用 | フィールド削除か式に接続か要判断。**本ジョブの明示値補完対象ではない**（対象は base rate） |
| L14 | `carryover.material_focused.materialRewardMultiplier: 1.15` が carryover 計算に出てこない | 接続か削除か要判断。ルール ID 自体は溶鉱炉が参照 |
| M5 | 報酬ID名と中身の不一致 | 死にIDではない。リネームはバランス/コピーの決裁 |
| H3 | 個別バフの戦闘未適用 | コード側。JSON削除ではない |

`carryoverRules` 6本は7ダンジョンから参照されており、ルールIDの死にデータは無い（job-011 結論を再確認）。

## やっていないこと

- JSON/GDScript からの実削除ゼロ
- dangling ID のリネーム・付け替えゼロ（挙動が変わり得るため）
- `buffs.json` を `_load_content` に足していない（足すと cap / preferredTargets / 基礎率が変わる。job-011 要判断）
