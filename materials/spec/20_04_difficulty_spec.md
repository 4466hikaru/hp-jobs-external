# 20-04 難易度曲線仕様

> 版: v1.0 / 作成: 2026-07-28 / 状態: 現行25wave棚卸し
>
> 主読者: 実装・レベルデザイン・QA。2層構造では、概要仕様書の「waveを越え帰還か続行かを選ぶ」体験を、本書がspawn圧力・敵補正・固定seed検証へ具体化する。実装根拠: game repo HEAD `bbddcec52321749cafc57980bef0b43075c82b70` の `content/dungeons.json`、`enemies.json`、`Main.gd`。参照仕様: `docs/spec/30_02_spawn_table.md`。

## 20-04-01 目的と圧力設計原則

本作のBrotato準拠は、単に敵HPを増やすことではない。短いwaveごとに敵の**密度**、**構成**、**HP/速度補正**、ボス到達を切り替え、プレイヤーがビルドと帰還判断を学習できる圧力曲線にする。Brotatoは複数攻撃手段を積みwave間に選択する構造の参照枠であり、固有数値を転載・採用するものではない。

1. 主変数は`maxAlive`（密度）、`spawnWeights`（構成）、`enemyHpScale`/`enemySpeedScale`（質）である。単一の高HP敵だけで難度を上げない。
2. R1は学習可能な役割構成、R2/R3は混成・精鋭、最終Rは明示bossを基準にする。ただし新ダンジョンへ現行表を無断コピーしない。
3. `xpCurveScale`は難度そのものではなく成長速度の補助変数である。圧力上昇とXP補正を同時に変える場合は固定seedで到達Lvを測る。
4. `maxAlive`はround上限であり、グローバル`MAX_ACTIVE_ENEMIES=120`も同時に働く。round上限が120を超えて敵を増やす設計は禁止する。

## 20-04-02 データ責務と実装事実

| 変数 | 実装上の責務 | 現行事実 | 固定/変動 |
|---|---|---|---|
| `maxAlive` | 通常spawnのround同時生存上限 | 25waveで39〜130。グローバル上限120のため、130設定は実体上120で頭打ちになる。 | round別変動 |
| `spawnWeights` | 敵IDの相対抽選比 | 各roundの重み合計は100。構成の正は`dungeons[].rounds[]`。 | round別変動 |
| `enemyHpScale` | 敵基礎HPへ乗算 | 0.907〜1.850。enemy固有HPとrun modifierにも乗算する。 | round別変動 |
| `enemySpeedScale` | 敵基礎移動速度へ乗算 | 0.909〜1.150。enemy固有速度とrun modifierにも乗算する。 | round別変動 |
| `xpCurveScale` | 敵XPへ乗算し最低1に丸める | 0.625〜3.400。難度でなく成長ペースの調整変数。 | round別変動 |
| `taint` | roundのHP/速度補正に追加で乗算 | roundに存在し得るが、25wave数表の主補正は上記scale。 | round別変動 |
| boss | 最終roundの`bossEnemyId`を明示生成 | 全7ダンジョンの最終roundで`bossRound=true`、帰還不可。 | ダンジョン固定 |

ダンジョン中は`dungeons[].rounds[]`が最優先であり、旧`stages[].waves[]`や敵の`startsAt`を無断で混用しない。詳細な敵役割・重み表は30-02を正とする。

## 20-04-03 現行25wave実装値

表記: `秒 / A=最大同時数 / HP=enemyHpScale / SPD=enemySpeedScale / XP=xpCurveScale`。各行の最後のRはboss roundである。敵構成は`30-02`の同一roundを参照する。

| ダンジョン | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| 境界の地下墓所 | 120 / A39 / HP0.907 / SPD0.947 / XP3.288 | 120 / A55 / HP0.953 / SPD0.973 / XP3.342 | 120 / A70 / HP1.000 / SPD1.000 / XP3.400 | — |
| 狼牙の巣 | 132 / A44 / HP1.015 / SPD1.022 / XP2.708 | 132 / A62 / HP1.068 / SPD1.051 / XP2.754 | 132 / A80 / HP1.120 / SPD1.080 / XP2.800 | — |
| 錆の溶鉱炉 | 144 / A50 / HP1.133 / SPD0.909 / XP1.450 | 144 / A70 / HP1.192 / SPD0.934 / XP1.475 | 144 / A90 / HP1.250 / SPD0.960 / XP1.500 | — |
| 静寂の修道院 | 144 / A50 / HP1.199 / SPD0.959 / XP1.299 | 144 / A68 / HP1.246 / SPD0.979 / XP1.317 | 144 / A84 / HP1.293 / SPD1.000 / XP1.333 | 144 / A100 / HP1.340 / SPD1.020 / XP1.350 |
| 月蝕の観測台 | 156 / A55 / HP1.325 / SPD0.996 / XP1.155 | 156 / A75 / HP1.376 / SPD1.018 / XP1.169 | 156 / A92 / HP1.428 / SPD1.039 / XP1.185 | 156 / A110 / HP1.480 / SPD1.060 / XP1.200 |
| 大聖堂 | 168 / A60 / HP1.450 / SPD1.034 / XP1.203 | 168 / A82 / HP1.507 / SPD1.056 / XP1.218 | 168 / A101 / HP1.563 / SPD1.078 / XP1.234 | 168 / A120 / HP1.620 / SPD1.100 / XP1.250 |
| ハーフプリンセスの玉座 | 180 / A65 / HP1.656 / SPD1.081 / XP0.625 | 180 / A88 / HP1.720 / SPD1.104 / XP0.634 | 180 / A109 / HP1.785 / SPD1.127 / XP0.642 | 180 / A130 / HP1.850 / SPD1.150 / XP0.650 |

現行の実装値には乖離がある。玉座R4の`maxAlive=130`はグローバル120を越えるため、130を実際の到達密度とは記述しない。`moon_knight`/`night_bloom_witch`はboss roleながら通常round重みにも含まれ、意図かデータ誤りかは未決（30-02既知乖離）である。

## 20-04-04 固定・変動・受入境界

| 区分 | 固定要素 | 変動要素 | 境界 |
|---|---|---|---|
| wave構造 | 7ダンジョン、計25round、最終Rはboss/帰還不可 | round数・秒数・目標Lv・hazard | 新規ダンジョンのround数は未決。既存表の複製で確定しない。 |
| 圧力 | 密度・構成・HP/速度補正で圧力を作る | 各scale、上限、重み、hazard | `maxAlive`は120以下に正規化するか、グローバル上限を変えるかが未決。両方を黙って変えない。 |
| 抽選 | 固定seed+同一入力で同じRNG系列 | 敵ID比、角度・jitter、event数 | 非seedの目視だけで曲線を合格にしない。 |
| 報酬成長 | XPは敵基礎値×round/run補正、LvはXP曲線に従う | XP scale、upgrade候補、build | 難度調整でXPを変更したら到達Lv・勝率も同時に測る。 |

## 20-04-05 未決事項

| ID | 未決事項 | 必要な決裁/計測 |
|---|---|---|
| DIF-U-01 | `maxAlive=130`とグローバル120のどちらを正とするか | 負荷計測を添え、round上限を120へ下げるか、グローバル上限を上げるかを決裁する。 |
| DIF-U-02 | boss roleを通常重みに混ぜる意図 | moon_knight/night_bloom_witchの出現上限・報酬・勝利条件を定義する。 |
| DIF-U-03 | 各ダンジョンの目標勝率、許容被弾、到達Lv | 標準ビルド・固定seed・試行数を定めてから数値を調整する。 |
| DIF-U-04 | hazardの採否と強度 | `grave_rise`等のスタブを実装済み扱いせず、各hazardの発火・回避・ダメージを仕様化する。 |

## 20-04-06 テスト観点

| ID | Yesとなる条件 |
|---|---|
| DIF-T-01 | 25roundすべてで重み合計100、参照敵IDが存在、`maxAlive>0`、HP/速度/XP scaleが0より大きい。 |
| DIF-T-02 | 固定seed・同一入力で各roundの敵ID列、spawn時刻、HP、速度、XP、boss出現が一致する。 |
| DIF-T-03 | 各roundで通常enemy数が`min(maxAlive, 120)`を超えず、boss生成時は通常enemyを退場させてもbossが1体だけ出現する。 |
| DIF-T-04 | R1/R2/R3/R4の境界で、前roundの敵・敵弾・gem・hazardが仕様どおりに消去/保持され、次roundの重み以外が混入しない。 |
| DIF-T-05 | 代表seedを固定し、7ダンジョンで到達Lv、死亡/帰還/完走、被ダメージ、peak enemy数を記録する。DIF-U-03の目標値が未決である間は、計測済みをYes、バランス適合は未判定として分離する。 |
| DIF-T-06 | boss roleを`spawnWeights`に含む7roundで、boss報酬・clear・special pickupが二重発火しない。 |

## 更新履歴

| 日付 | 箇所 | 変更前→変更後 | 理由 | 影響範囲 |
|---|---|---|---|---|
| 2026-07-28 | 初版 | 散在するround値→主変数別の25wave難易度表 | P1仕様化、固定seed QA可能化 | dungeons、enemies、spawn、balance、QA |
| 2026-07-28 | 20-04-03 | `maxAlive`を設定値のまま圧力と見なす→グローバル120との乖離を明記 | 実装上の実効上限を隠さない | Main、dungeons、性能、難易度 |
