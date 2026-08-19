# 20-03 経済仕様

> 版: v1.0 / 作成: 2026-07-28 / 状態: 現行実装棚卸し＋D-31/D-32反映
>
> 主読者: 実装・ゲームデザイン・QA。2層構造では、概要仕様書が示す「町とダンジョンを往復して成長する」ゲームサイクルを、ここでは通貨・ラン内XP・絆のデータ、損失境界、受入基準へ分解する。実装根拠: game repo HEAD `bbddcec52321749cafc57980bef0b43075c82b70` の `content/shops.json`、`rewards.json`、`upgrades.json`、`dungeons.json`、`Main.gd`。決裁根拠: `docs/decision-log.md` 2026-07-28 D-31/D-32。

## 20-03-01 目的と経済ループ

黒貨は町の恒久所持品を売買する通貨、XPはラン内のレベル選択を生む一時資源、絆はキャラクター別の進行値である。三者を混同せず、ダンジョンの帰還判断が「XPを保持して次waveに進むか」と「恒久報酬を45%で確定するか」を読める状態にする。

```text
敵撃破 → XP gem → ラン内XP → level-up候補 → ラン内ビルド
     \→ round/clear reward → 素材・アイテム・（定義があれば黒貨）→ 町の購入/売却
イベント/報酬/選択 → characterAffection → 絆条件・キャラクター進行
round終了 → 帰還45%でcarryover保存 / 続行でラン内ビルドを保持 → 次round
```

黒貨の獲得レート、売買価格の実データ、黒貨とcarryoverの交換関係は未決である。未決項目を実装側が任意の倍率や価格表で埋めてはならない。

## 20-03-02 実装事実

| 領域 | 現行値・挙動 | 根拠 | 状態 |
|---|---|---|---|
| 通貨ID・表示 | `currency.dark_coin` / 黒貨。保存先は`save_data.wallet`。 | `shops.json`、`Main.gd:_shop_currency_id/_currency_balance` | 実装済み |
| 初期残高 | 通常の既定セーブは300黒貨。デバッグ初期化は2,400黒貨。 | `Main.gd:_default_save_data`、デバッグ初期化 | 実装済み（用途別） |
| 消費先 | 7店・計31在庫枠で購入時に黒貨を減算する。所持品/素材は1個売却時に`item.sellPrice`を黒貨へ加算する。 | `shops.json`、`Main.gd:_buy_shop_item/_sell_owned_shop_item` | 実装済み |
| 価格・売却レート | 店在庫は商品IDとstockを持つが、`shops.json`の在庫行は価格を持たない。価格は商品定義の`price`、売却額は`item.sellPrice`を読む。全商品の数値表・購入/売却比はこの棚卸し時点で未集計。 | `Main.gd:_shop_buy_price`、`_sell_owned_shop_item` | 未決（レート） |
| 黒貨の報酬経路 | reward item type `currency` は`RunRewardGrant.currency_grant`を通り黒貨へ加算できる。現行`rewards.json`の108定義には通貨itemを確認できない。 | `Main.gd:_apply_reward_item`、`rewards.json` | 経路のみ実装済み、供給値なし |
| ラン内XP | 敵死亡時に敵XPと補正をgemへ保存し、接触/磁石で回収すると`xp`へ加算する。run開始時はLv1/XP0、ラン終了時に恒久walletへ移さない。 | `Main.gd:_spawn_enemy/_spawn_gem/_collect_all_gems/_reset_run` | 実装済み |
| level報酬 | XPが必要値以上で、必要値を1回分だけ差し引きLvを+1し、最大3候補のlevel-upへ遷移する。残余XPがあれば選択後に再判定する。 | `Main.gd:_start_level_up/_finish_level_up_choice` | 実装済み |
| XP曲線 | Lv1からの必要XPは`[5,11,18,28,42,60,82,108,138,172,210,252]`。13Lv以降は直近差分42（最小8）ずつ加算する。 | `upgrades.json:xpCurve`、`Main.gd:_xp_needed` | 実装済み |
| round XP補正 | 各roundの`xpCurveScale`を敵のXPに掛け、最低1へ丸める。値域は0.625〜3.400。 | `dungeons.json`、`Main.gd:_spawn_enemy` | 実装済み |
| 絆 | `save_data.characterAffection[characterId]`を共通のキャラクター別整数値として保存し、報酬・ADV選択で加減算し、ルート条件/同行者rank条件が読む。 | `Main.gd:_add_character_affection*`、`_route_event_affection_met` | 実装済み |

## 20-03-03 固定・変動・境界

| 区分 | 固定要素 | 変動要素 | 境界・禁止事項 |
|---|---|---|---|
| 黒貨 | IDは`currency.dark_coin`、負残高にしない、購入は残高確認後、売却は`sellPrice`のみ加算 | 初期残高、商品価格、売却額、在庫、黒貨報酬額 | 黒貨をXPや絆へ自動変換しない。未決の価格倍率・リロール・ロックを追加しない。 |
| XP/Lv | ラン開始Lv1/XP0、敵XP→gem→回収、Lv上昇は必要XPを差引き、候補数3 | 敵基礎XP、round/ラン補正、必要XP曲線、候補内容 | XPを永続保存しない。敵撃破だけで未回収gemのXPを加算しない。 |
| 絆 | キーは`characterId`、保存先は`characterAffection`、0未満にしない | 報酬/選択の増減値、イベント閾値、上限 | D-32により戦闘用の別絆値を作らず、同じ値を流用する。上限・戦闘効果は未決。 |
| 帰還/続行 | 最終round以外で二択、続行ではLv・武器・buffを保持、敗北ではcarryoverを保存しない | round数、報酬、carryover対象、倍率 | 後述D-31の45%/+10%は仮値。黒貨そのものの保全率と読み替えない。 |

## 20-03-04 D-31/D-32との接続

### D-31: 帰還45%／続行+10%/round

`decision-log.md`のD-31はB（スリル）を採択した。実装は`returnCarryoverMultiplier=0.45`、完走時は`continueRewardMultiplierPerRound=0.10`を用い、carryover ruleの基礎率×到達深度×完走倍率で**恒久carryover bonus**を保存する。これは黒貨残高の45%を保存する仕様ではない。対象bonusと基礎率の個別レートはcarryover ruleデータに依存し、本書で未確認の値は未決とする。

| 結果 | ラン内XP/Lv | round報酬 | carryover | 黒貨wallet |
|---|---|---|---|---|
| 続行 | 保持 | 付与済み分を保持して次roundへ | 未保存 | 保持（ラン内で変動しない現行導線） |
| 中間帰還 | ラン終了で消滅 | 付与済みround報酬＋partial return rewardを保存 | 45%を基準に保存（仮） | 既存walletを保持 |
| 完走 | ラン終了で消滅 | clear rewardを保存 | 深度・+10%/roundで算出（仮） | 既存walletを保持 |
| 敗北 | 消滅 | `failRewardIds`のみ | 保存しない | 既存walletを保持 |

### D-32: 絆は`characterAffection`流用

決裁D-32=Aにより、戦闘とイベントの絆は`save_data.characterAffection`を共通パラメータとして使う。現行では報酬item `affection`とADV選択`affectionDelta`がこの値を変更し、ルート解放は`productionSlot`以上かで判定する。戦闘中にどの行動が絆を増減させるか、絆が武器/ダメージへ与える効果、最大値は未決である。

## 20-03-05 未決レートと決裁待ち

| ID | 未決事項 | 実装前に固定する値 | 勝手に確定してはならない理由 |
|---|---|---|---|
| ECO-U-01 | 黒貨の主な入手源と一回当たり額 | ダンジョン/イベント/売却別の供給表 | 現行rewardに通貨供給がなく、経済の総量が決まらない。 |
| ECO-U-02 | 店の商品価格表と購入/売却比 | 商品ID別`price`/`sellPrice`、在庫再入荷規則 | 価格倍率・リロール・ロックは既決でない。 |
| ECO-U-03 | carryover ruleの対象と基礎率 | target別base rate、上限、累積可否 | D-31は出口倍率を採択しただけで、全レートの確定ではない。 |
| ECO-U-04 | 絆の戦闘連動 | トリガー、増減量、上限、武器との効果 | D-32は保存値の流用決裁であり、効果量の決裁ではない。 |

## 20-03-06 テスト観点

| ID | Yesとなる条件 |
|---|---|
| ECO-T-01 | 初期wallet、購入、売却を通し、`currency.dark_coin`以外へ誤計上せず、残高が負にならない。 |
| ECO-T-02 | 同一商品について残高不足、在庫0、購入成功、保護品売却不可、売却成功を確認し、成功時だけ残高/所持数/在庫が各1回更新される。 |
| ECO-T-03 | 固定seedで同じ敵列を倒し同じgemを回収したrunは、XP、Lv、level-up候補、残余XPが一致する。 |
| ECO-T-04 | XP曲線のLv1〜13と13Lv超の各1点で、必要XP、差引き、連続level-upが期待値どおり。 |
| ECO-T-05 | 25roundの各`xpCurveScale`を使い、敵XPが`max(1, round(baseXP×roundScale×runScale))`となる。 |
| ECO-T-06 | D-31の固定seed試験で、帰還は45%基準、完走は+10%/round基準、敗北はcarryover 0となり、walletを誤って減らさない。 |
| ECO-T-07 | 報酬とADV選択の各1ケースで`characterAffection`だけが更新され、0未満にならず、同じ選択を再読込しても二重加算しない。 |

## 更新履歴

| 日付 | 箇所 | 変更前→変更後 | 理由 | 影響範囲 |
|---|---|---|---|---|
| 2026-07-28 | 初版 | 散在する通貨・XP・絆の実装→経済詳細仕様 | P1仕様化と現行棚卸し | shops、rewards、upgrades、dungeons、save、QA |
| 2026-07-28 | 20-03-04 | 帰還/続行の数値未反映→D-31の45%/+10%をcarryover仕様として明記 | 決裁D-31を実装境界へ接続 | return、carryover、balance、QA |
| 2026-07-28 | 20-03-04 | 絆の別パラメータ余地→`characterAffection`共通流用を明記 | 決裁D-32 | rewards、ADV、route、combat、save |
