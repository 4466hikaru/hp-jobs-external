# job-019 contentデータ整合監査

- 監査日: 2026-08-31 JST
- ミラー: `4466hikaru/hp-game-share` `3fd5cf0`（mirror refresh 0821 / 2026-08-21T03:55:12Z）
- 方法: content/*.json の静的読取のみ（ゲーム未起動・データ未改変）
- 鮮度: **ミラー時点の監査**。0821以降の本体更新は未反映の可能性あり
- 先行: `deliverables/job-011/balance_audit.md` / `deliverables/job-009/spec_audit.md` を参照したが、本表の値は再突合済み
- 「未参照」定義: 自レコードの `id` フィールドを除き、全content JSONの**文字列値**および `spawnWeights` / `enemyWeights` の**キー**として一度も出現しないこと。コード側参照は対象外

## 読了マーカー（JSON 24）

| ファイル | 読了 | 要約 |
|---|---|---|
| assets.json | 読了 | assets 699（status: todo 502 / review 122 / approved 74 / approved_source 1） |
| audio.json | 読了 | bgm 7 / se 40 |
| battle_profiles.json | 読了 | profiles A/B/C、default=C |
| buffs.json | 読了 | buffs 19 / carryoverRules 6 |
| characters.json | 読了 | characters 9 |
| companion_equipment.json | 読了 | companions 7 / subEquipmentItems 23 |
| credits.json | 読了 | sections 2 / licenseRows 2 |
| dungeons.json | 読了 | dungeons 7（各 rounds + spawnWeights） |
| enemies.json | 読了 | enemies 18 |
| evolutions.json | 読了 | evolutions 3 |
| progression.json | 読了 | conditions 9 / unlocks 9 / milestones 4 |
| project.json | 読了 | productionScope / unlockMilestones / runRules |
| rewards.json | 読了 | rewards 112（全 bundle） |
| route_preference.json | 読了 | provisional=true、heroineJoinOrder 7 |
| scenes.json | 読了 | scenes 93（adult 系は redactedForMirror） |
| shops.json | 読了 | shops 7 / items 23 |
| stages.json | 読了 | stages 3（MVP系） |
| themes.json | 読了 | themes 3 |
| towns.json | 読了 | towns 7 / commands 9 |
| upgrades.json | 読了 | upgradePool 21 |
| weapons.json | 読了 | weapons 9 |
| world_regions.json | 読了 | regions 7 |
| world_tiles.json | 読了 | maps 7 |
| worldmap.json | 読了 | nodes 56 / edges 6 / regions 7 |

README.md は対象外（指示どおり）。

## 観点サマリ

| 観点 | 結果 |
|---|---|
| ①解放系フラグ矛盾 | 検出あり（下表） |
| ②参照整合 | 検出あり（下表）。未参照は件数+例 |
| ③状態語の不統一 | 検出あり（下表） |
| ④release到達＋仮値 | 検出あり（下表） |

重要度: **高**=リリース前に直すべき / **中** / **低**。どのフラグを正とするかは決裁しない。

## 検出表

| # | ファイル | キー | 矛盾内容 | 重要度 | 根拠（値の要約） |
|---|---|---|---|---|---|
| A1 | characters.json | rosterEnabled / initiallyUnlocked / contentStatus | **hidden 7th**: ロスター有効なのに初期未解放（既知シード。加入条件の詳述なし） | 高 | 当該キャラのみ `rosterEnabled=true` かつ `initiallyUnlocked=false` かつ `contentStatus=active_post_game_roster`。他キャラは同三キー揃いが無い |
| A2 | characters.json ↔ companion_equipment.json | unlockConditions ↔ unlockConditionIds | 同一キャラの解放条件が二系統で型・意味が不一致 | 高 | characters側は `route_unlocked` / `stage_clear` / `dungeon_clear` 混在。companions側は全件 `condition.region.NN.clear`。例: 初期解放キャラは `initiallyUnlocked=true` だが対応companionは region.01 clear 必須 |
| A3 | characters.json | rosterEnabled / contentStatus | 9件中4件にしかキーが無い（スキーマ欠落） | 中 | キーあり: 交代枠・legacy・hidden 7th・common_end。残り5件は `initiallyUnlocked` のみ。UIが欠落をどう既定するかで表示矛盾になり得る |
| A4 | characters.json | unlockConditions.type=stage_clear | MVP stage クリア条件のまま残存（現行進行はダンジョン/地域） | 中 | 3キャラが `mvp_night_field` / `library_archive` / `moonlit_garden` 参照。対応companionは地域クリア条件 |
| A5 | world_regions.json | companionUnlockId（最終地域） | 最終地域に companionUnlockId が無い一方、post_game companion は定義あり | 中 | 他6地域は companionUnlockId あり。最終地域は null 相当。designRole文面は post-game companion に言及 |
| A6 | characters.json | spineVisual.enabled vs rosterEnabled | legacy枠外キャラなのに spineVisual.enabled=true | 低 | `contentStatus=legacy_out_of_roster` / `rosterEnabled=false` だが spineVisual.enabled=true |
| B1 | characters.json → weapons.json | startingWeaponIds | `weapon.*` 参照が weapons 定義IDと不一致 | 高 | 8キャラの startingWeaponIds が `weapon.ember_orbit` 等形式。weapons.json の id は `ember_orbit` 等（プレフィックス無し）。legacyStartingWeaponIds は裸IDで一致 |
| B2 | dungeons.json → stages.json | stageId | 7ダンジョン全てが stages.json に存在しない stageId を指す | 高 | 値は `stage.dungeon.<dungeon_suffix>` 形式。stages.json 定義は `mvp_night_field` / `library_archive` / `moonlit_garden` の3件のみ |
| B3 | rewards.json → stages.json | sourceStageId | 90件の sourceStageId が stages.json と不一致 | 高 | 例: `stage.library_archive`(48) / `stage.moonlit_garden`(30) / `stage.dungeon.blood_king_castle`(11) / `stage.mvp_night_field`(1)。定義側はプレフィックス無し |
| B4 | enemies.json → assets.json | assetId | 5敵の assetId が assets 台帳に無い | 中 | `enemy_blue_bat` / `enemy_grave_moth` / `enemy_curse_wisp` / `enemy_thorn_brute` / `enemy_night_bloom_witch`。他敵は `asset.enemy.*` で台帳ヒット |
| B5 | characters/stages 等 | routeId | `route.*` が content 内に定義ファイル無し | 中 | 9 routeId が参照されるが routes.json 等は無し（コード定義の可能性。ミラー時点では参照先不明） |
| B6 | 複数 | （未参照定義） | 定義はあるが他contentから未参照 | 低〜中 | 下記「未参照サマリ」 |
| C1 | scenes.json ↔ rewards.json | draftStatus | 同名キーなのに列挙子が別系統。紐付け84件で不一致 | 中 | scenes: `script_pass`/`script_final`。rewards: `approved`/`skeleton`/`adult_pending_stub`/`script_pass`/`scenario_shell`/`existing_draft`。`script_final`×stub系が49 |
| C2 | 複数 | 解放・到達語彙 | 同じ「解放/到達」意味に別語彙 | 中 | contentStatus / standardOrPostGame / draftStatus / status / visualStatus / lockedPlaceholder / provisional / initiallyUnlocked / rosterEnabled |
| C3 | characters / progression / companions | 条件type | 解放条件の型名が三系統 | 中 | `route_unlocked` / `stage_clear` / `dungeon_clear` / `condition.*` ID参照 |
| C4 | weapons / upgrades / characters | 武器ID名前空間 | 裸ID / `weapon.` 接頭 / `weapon.*.stat` が混在 | 中 | 定義=裸。startingWeaponIds=`weapon.*`。upgrades.target=`weapon.*.damage` 等 |
| C5 | stages / dungeons / rewards | stage ID名前空間 | 裸 / `stage.` / `stage.dungeon.` が混在 | 中 | B2/B3と同根 |
| D1 | enemies.json | visualStatus | 本番最終ダンジョンbossに placeholder 状態が残る | 高 | `boss.blood_king.visualStatus=placeholder_pending_new_design`。同IDが `dungeon.blood_king_castle` の bossEnemyId |
| D2 | scenes ↔ rewards | draftStatus vs lockedPlaceholder | scene が script_final なのに対応 reward が stub/shell | 中 | script_final シーン49に対し、reward 側 adult_pending_stub(33)+skeleton/scenario_shell 等。lockedPlaceholder=true は33（いずれも adult_pending_stub） |
| D3 | companion_equipment.json | initialReleaseItemCount + notesJa | 「initialRelease」件数にTODO balance注記の装備が含まれる | 中 | rules.initialReleaseItemCount=23（実件数と一致）。うち9件の notesJa に `TODO balance` |
| D4 | themes.json ← stages.json | assets.* / ui.* | MVP themes が placeholder パスのまま stages から参照 | 中 | 例: `player_placeholder.png` / `default_placeholder.tres` / `visual_novel_placeholder`。3 stages が各 themeId を参照 |
| D5 | route_preference.json / shops.json | provisional / gifts | 仮値ギフトがショップ在庫に載る | 低 | `provisional=true`（未到達自己申告）。`item.gift.placeholder.*` と表示名 `[仮]` が shops 在庫にも出現 |
| D6 | dungeons.json | hook.desc | 初回ダンジョン説明に TODOスタブ | 低 | border_catacomb.hook.desc に「TODOスタブ」文言 |

## 未参照サマリ（観点②）

定義は上記「未参照」定義に従う。コード専用カタログは件数のみ。

| 種別 | 定義数 | 未参照数 | 例 |
|---|---:|---:|---|
| assets | 699 | 581 | 未参照の status 内訳: todo 495 / review 55 / approved 30 / approved_source 1。例: `asset.adult.*.main_visual`, `asset.store.logo` |
| upgrades | 21 | 18 | evolutions が参照するのは3件（`magic_bolt_damage` / `move_speed` / `pickup_radius`）のみ |
| evolutions | 3 | 3 | evolution ID 自体を指す他JSON無し（一覧ロード想定） |
| buffs | 19 | 6 | `buff.companion.*` 2 / `buff.dungeon.attack_minor` 等。rewards の buff_unlock は別3件を参照 |
| progression.unlocks | 9 | 9 | 地域側は conditionIds を直接参照し unlock.* IDは未使用 |
| conditions (affection) | 2 | 2 | `condition.affection.any_60/90` |
| battle_profiles | 3 | 2 | A/B（defaultProfileId=C のみ参照） |
| bgm | 7 | 5 | scenes 等から参照される一部を除きコード寄り |
| se | 40 | 40 | content JSON内参照ゼロ（コードカタログ） |
| enemies | 18 | 0 | spawnWeights/enemyWeights キーを参照とみなすと全滅。最終地域 encounter の専用敵IDも参照扱い |

## 観点別「検出なし」確認

なし（4観点すべて検出あり）。ゼロ件の観点は無かった。

## 補足（決裁しない観察）

- productionScope の地域7/ダンジョン7/standardCompanions6/postGameCompanions1 は実件数と一致
- assets の status=todo 502件は「未到達」自己申告のため観点④には数えず、未参照件数に含めた
- job-011 指摘の buffs 未ロードはコード側のため本監査（content JSON）の検出表には入れていない

## 正直な制限

- ゲーム実行・セーブ遷移・UI実機でのロックカード表示は未確認（静的のみ）
- コードが `weapon.` 接頭を剥がす等の正規化をしている可能性は、本ミラーの JSON 間だけ見ると破綻して見える、という検出
- adult シーン本文は redactedForMirror のため draftStatus と reward の突合に限定
