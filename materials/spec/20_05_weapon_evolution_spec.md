# 20-05 武器進化・シナジー仕様

> 版: v1.0 / 作成: 2026-07-28 / 状態: 現行実装棚卸し＋W-05との境界整理
>
> 主読者: 実装・ゲームデザイン・QA。2層構造では、概要仕様書の「姫=武器ビルド」という動機を、本書が現行9武器・3進化・将来のTier自動合成のデータ境界へ分解する。実装根拠: game repo HEAD `bbddcec52321749cafc57980bef0b43075c82b70` の `content/weapons.json`、`evolutions.json`、`upgrades.json`、`Main.gd`。上位決裁: `docs/spec/20_02_weapon_spec.md` W-01〜07、特にW-05。

## 20-05-01 目的と用語の分離

現行の**進化**は、所持中の基礎武器と指定upgrade rankを条件に、基礎武器を結果武器へ置換する一回限りのlevel-up候補である。W-05の**Tier自動合成**は、同一武器を低Tierから2本ずつまとめる将来の姫ビルド契約である。両者は同じ「強化」に見えても、現行コード上で同一の処理・データではない。

| 用語 | 現行/決裁 | 単位 | 結果 |
|---|---|---|---|
| 基礎武器 | 現行実装 | `weaponId` 1本 | 攻撃stateを作る |
| 進化 | 現行実装 | 基礎武器1本＋upgrade rank | 基礎stateを削除し、結果weapon stateを1本作る |
| Tier自動合成 | W-05決裁、未実装 | 同一`weaponDefinitionId`の同Tier2本 | 次Tierの1本へ統合する |
| シナジー | 一部実装（進化の必要upgrade） | 進化ごとの条件 | 条件を満たした進化候補を重み付きで出す |

## 20-05-02 現行9武器と進化対応（実装事実）

表記の攻撃パラメータは`weapons.json`の現行値であり、Tier値・姫専用値ではない。

| 基礎/結果 | 武器ID | 標的 | 射程 | CD秒 | 威力 | 弾数 | 貫通 | 進化対応 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 基礎 | `magic_bolt` 魔導弾 | nearest | 460 | 0.75 | 30 | 1 | 0 | → `starfall_core` |
| 基礎 | `ember_orbit` 火輪 | radial | 360 | 1.80 | 18 | 4 | 1 | → `solar_crown` |
| 基礎 | `moon_knife` 月刃 | nearest | 520 | 0.70 | 28 | 1 | 2 | → `lunar_fan` |
| 基礎 | `thorn_seed` 茨の種 | random | 420 | 1.25 | 26 | 2 | 0 | 進化なし（現行） |
| 基礎 | `ward_sigil` 守護印 | radial | 280 | 2.70 | 18 | 6 | 3 | 進化なし（現行） |
| 基礎 | `storm_chime` 嵐鈴 | random | 620 | 1.70 | 42 | 1 | 0 | 進化なし（現行） |
| 結果 | `starfall_core` 星落とし | nearest | 620 | 0.95 | 58 | 3 | 2 | 魔導弾の進化結果 |
| 結果 | `solar_crown` 陽冠 | radial | 420 | 1.35 | 28 | 8 | 2 | 火輪の進化結果 |
| 結果 | `lunar_fan` 月扇 | nearest | 560 | 1.05 | 34 | 3 | 4 | 月刃の進化結果 |

| 進化ID | 基礎→結果 | 必須upgrade | 条件 | 所有者/演出の現行挙動 |
|---|---|---|---|---|
| `evolution.magic_bolt_starfall` | 魔導弾→星落とし | `magic_bolt_damage` | rank 2以上 | 基礎weapon stateのownerを結果へ引継ぎ、キリハcut-inを出す。 |
| `evolution.ember_orbit_solar_crown` | 火輪→陽冠 | `move_speed` | rank 1以上 | 基礎weapon stateのownerを結果へ引継ぎ、アカリcut-inを出す。 |
| `evolution.moon_knife_lunar_fan` | 月刃→月扇 | `pickup_radius` | rank 1以上 | 基礎weapon stateのownerを結果へ引継ぎ、シオンcut-inを出す。 |

## 20-05-03 現行進化処理

1. level-up候補作成時、`_available_evolution_choices`が全`evolutions`を走査する。
2. 基礎weapon stateがあり、結果weapon stateがなく、進化自体が未取得で、指定upgrade rank以上のとき候補になる。
3. 候補weightは既定100に、`tags`/`requiredCompanionTags`/`requiredSubEquipmentTags`がactive tagと一致するごとに+35する。現行3進化データにはこれらtag群がないため、各々weight=100である。
4. 選択時は基礎weapon stateを消し、同じ`ownerCharacterId`で結果weapon stateを1本追加し、cut-in後に戦闘へ戻る。

進化は「基礎＋結果を同時保持する」処理ではない。基礎がない、結果が既にある、進化を既に選んだ、必須upgrade rankが不足する、のいずれかでは候補に出さない。

## 20-05-04 W-05 Tier自動合成との関係

W-05は`20-02`で決裁済みだが、現行の`weapons.json`には`tier`、複数本の同一武器所持、合成レシピ、合成処理がない。現行`weapon_states`はruntime weapon IDをkeyにし、既存keyなら追加しないため、同一weapon IDを2本保持できない。よって現行進化を「Tier2へ進化した」と表現してはならない。

| 比較 | 現行進化 | W-05 Tier自動合成 |
|---|---|---|
| 発火 | level-up候補をプレイヤーが選択 | 同一武器2本が揃った時点で自動 |
| 入力 | 基礎1本＋指定upgrade rank | 同一`weaponDefinitionId`かつ同Tier2本 |
| 出力 | 別`resultWeaponId`1本、基礎を削除 | 次Tierの同定義1本 |
| 所有者 | 基礎stateのownerを継承 | 同じ所有姫内だけ。別姫・異種・異属性は混ぜない |
| 現状 | 実装済み | 未実装 |
| 統合順序 | 未決 | Tier合成と進化の優先順位、進化条件がTierを参照するかは未決 |

実装時の固定境界は、(a)合成後も進化済み武器を再進化させない、(b)進化による基礎→結果置換が合成対象を二重消費しない、(c)所有姫をまたぐ合成をしない、である。これらを満たす具体的なTier上限、進化と合成の順序、結果武器のTier継承は未決である。

## 20-05-05 固定・変動・未決シナジー

| 区分 | 固定要素 | 変動要素 | 状態 |
|---|---|---|---|
| 武器定義 | 現行9ID、標的型、射程/CD/威力/弾数/貫通 | run modifierによる性能補正 | 基礎データ実装済み |
| 進化 | 3ID、基礎→結果、必須upgrade rank、基礎削除・結果追加 | 条件tagに一致した候補weight | 実装済み（現行tagなし） |
| Tier | 同一武器2本ずつ、低Tierから、異種/異属性/別所有者を混ぜない | Tier上限、数値倍率、結果武器への継承 | W-05決裁済み、実装/数値未決 |
| 属性/姫シナジー | 一致属性ダメージ増のみ。相性・耐性・状態異常なし（20-02 W-03） | 属性名、姫対応、倍率、候補重み | 未決 |
| 絆シナジー | D-32の`characterAffection`流用 | 進化条件・性能効果・閾値 | 未決。絆値を勝手に進化条件へ足さない。 |

## 20-05-06 テスト観点

| ID | Yesとなる条件 |
|---|---|
| WE-T-01 | 3進化それぞれで、基礎武器あり・必要rank直前/到達・結果武器あり・進化済みの各条件を確認し、到達時だけ候補に出る。 |
| WE-T-02 | 進化選択後、基礎stateが0、結果stateが1、ownerCharacterIdが基礎と一致し、同じ進化を再選択できない。 |
| WE-T-03 | 固定seedで進化候補を含むlevel-upを再現し、候補・weight・選択結果・cut-in後のrun stateが一致する。 |
| WE-T-04 | `tags`を持つfixtureでtag一致1件につきweightが+35され、現行3定義ではweight=100のままである。 |
| WE-T-05 | W-05実装後、Tier1×4+Tier2×2がTier3×1となり、異種・異属性・別所有姫の武器は合成されない。未実装の現HEADではこのテストはNo（未実装）と明記する。 |
| WE-T-06 | W-05統合後、進化と合成が同じ武器を二重消費/二重生成せず、基礎→結果置換のownerが保存・再読込後も一意である。 |

## 更新履歴

| 日付 | 箇所 | 変更前→変更後 | 理由 | 影響範囲 |
|---|---|---|---|---|
| 2026-07-28 | 初版 | 20-02の武器一般仕様→現行進化とTier合成を分離した詳細仕様 | 進化をTierと誤認せず実装可能にする | weapons、evolutions、upgrades、save、QA |
| 2026-07-28 | 20-05-04 | W-05と現行進化の関係が暗黙→発火・入力・出力・所有者を表で分離 | 決裁済みTier合成の実装境界を固定 | weapon states、候補、合成、進化 |
