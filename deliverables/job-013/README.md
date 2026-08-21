# job-013 納品: バランス明確バグの修正パッチ（挙動不変）

対象コード: `https://github.com/4466hikaru/hp-game-share`（`main` HEAD `92ff9cdc66c9aa588f75b3665d03bc98ceea1527` / Main.gd blob `cf8957160449c31fcfdfe2b2488d834cc3b2108e` 25230行 / buffs.json blob `e6a273106dbdde15333bfe3cac54ae45acfad0dd` / dungeons.json blob `487fbf2de778f4d01f70bd9086fbddb4aa989037`）。`gh api` で 2026-08-21 に再読。**hp-game-share は clone していない。** ミラーは asset-stripped で Godot では遊べない。

発注書 `jobs/job-013-balance-fix-patches.md` の完成定義チェックボックスは未改変。status だけ `in-progress(game)`（第1コミット）。job-002 は拾っていない。PR#12 の 020/024 には触れていない。job-014/015 は開始していない。

## 完成定義 (Yes/No)

- [Yes] 3対象のパッチ+実効値不変の検証ログ（対象2は削除提案のみでパッチなし。対象1と3に diff。ログは `logs/`）
- [Yes] 死にデータの削除提案リスト（実削除なし）=`dead-data-deletion-proposal.md`
- [Yes] 正直な申告（本 README + `logs/honest-unverified.md`）

## 適用手順 (hp-game のプレイ可能 checkout)

作業ディレクトリは **ゲーム本体 repo のルート**（`content/buffs.json` と `game/scripts/main/Main.gd` がある場所）。LF。番号順。

```bash
git apply --check path/to/deliverables/job-013/patches/001-player-damage-reduction-cap.diff
git apply path/to/deliverables/job-013/patches/001-player-damage-reduction-cap.diff
git apply --check path/to/deliverables/job-013/patches/002-dungeon-base-carryover-rate.diff
git apply path/to/deliverables/job-013/patches/002-dungeon-base-carryover-rate.diff
python3 path/to/deliverables/job-013/tests/test_job013_static.py .
# Godot があれば（本箱には無い）:
# godot --headless --quit-after 1
# 本ジョブは gdparse（gdtoolkit 4.5.0）で Main.gd を構文解析した。apply --check だけでは不十分（020事故）。
```

001 と 002 はファイルが被らないので順不同でも当たる。本体へは当てていない。

## パッチ一覧

| file | 対象 | 内容 |
|---|---|---|
| `patches/001-player-damage-reduction-cap.diff` | 1 | `content/buffs.json` `carryoverCaps` に `player.damageReduction: 0.5` を追加。現行 fallback と同じ値。他キーは未変更 |
| `patches/002-dungeon-base-carryover-rate.diff` | 3 | 7ダンジョン中5件（default 以外）に `baseCarryoverRate: 0.1` を明示。`Main.gd` `_dungeon_carryover_bonus_delta` の fallback を `rule` → `dungeon` → `0.1` に1段だけ足す。ルール表の 0.08/0.12/0.11/0.13 は **未変更** |

対象2はパッチなし（削除提案のみ）。

## 何を直して、何を変えていないか

現行ミラー `main` は `_load_content` が `buffs.json` を読まない（job-009 A-02 / job-011。本ジョブで `Main.gd:2910-2935` を再読して確認）。その前提で **実効値を動かさない**。

1. **cap 穴:** `_clamp_carryover_target_value` は `carryoverCaps.get(target, fallback)`。キー欠落時の fallback は CD 以外 **0.5**。`player.damageReduction` は preferredTargets に出るが cap 表に無かった（job-011 H2）。表に 0.5 を足すだけ。ロード時も未ロード時も clamp 結果は同一（`logs/effective-value-identity.log`）。
2. **死にデータ:** 削除していない。リストだけ。
3. **carryover 基礎率:** 7ダンジョンは `carryoverRuleId` だけ持ち `baseCarryoverRate` を持たない。ルールは buffs 未ロードで空 dict → ハードコード 0.1。A-02 の「5件が仕様値と違う」は溶鉱炉 0.08 / 修道院 0.12 / 観測台 0.1 / 大聖堂 0.11 / 玉座 0.13。この5件に **現行実効値 0.1** を JSON 明示。墓所・狼牙（`carryover.default`）は触っていない。GDScript は `rule.get(..., dungeon.get(..., 0.1))`。ルールが載ればルール値が勝つので、仮に本体が buffs を既に読んでいても基礎率は変わらない。

**やっていない（挙動が変わるため）:**

- `_load_content` に `buffs.json` を足す（maxHP cap 0.5→100、移動 cap 0.5→0.25、preferredTargets 配分。job-011 M10/M11）
- 5件の明示値を仕様ルール（0.08 等）にする（それは数値チューニング）
- 個別バフの戦闘適用（H3）

## コンパイル/パース確認（020事故の教訓）

`git apply --check` は **不足**。再構成ツリー（gh api で取った現行 Main.gd / JSON のコピー。clone ではない）に apply したあと:

| 確認 | 結果 |
|---|---|
| `jq empty` buffs.json / dungeons.json | OK |
| Godot headless | **未実行**（本箱に Godot 無し。ミラーは asset-stripped） |
| `gdparse`（gdtoolkit 4.5.0）Main.gd 修正前 | exit 0 |
| `gdparse` 修正後（apply 済みコピー） | exit 0 |
| 意図した表 | `carryoverCaps` に `player.damageReduction` が追加された。隣の `player.damageMultiplier` 等の値は同一 |
| 意図した関数 | `_dungeon_carryover_bonus_delta` の1行のみ。隣の `_clamp_carryover_target_value` / `_carryover_value_for_target` / `_carryover_rule_by_id` / `_carryover_targets_for_rule` / `_apply_carryover_target_to_run` / `_load_content` は byte 同一。`func` 数 1518 のまま |

詳細: `logs/compile-parse-check.log`

## 要判断

1. 5ダンジョンの明示 0.1 を、将来 buffs ロードが載ったあとも維持するか。仕様ルール（0.08/0.12/0.11/0.13）に戻すのは数値決裁。
2. 死にデータの実削除（L3 affection 条件、L4 未付与バフ6件、L5 `special_behavior` exclude）。本PRはリストのみ。
3. ミラー `main` に `buffs.json` ロードを同期するか（job-011 要判断4。本PRではやっていない）。
4. 観測台 `carryover.offensive` の仕様値は既に 0.1。A-02 の「5件」に含めて明示した。default の2件まで足すかは不要と判断（要らなければそのままでよい）。

## 正直申告の要約

Godot 未実行。数式は `Main.gd` から写した静的シミュレーション。ミラー鮮度の可能性は job-009/011 と同じ（本体が既に buffs を読んでいるなら、本パッチの JSON cap 追加はロード後の穴埋めとして効く。基礎率はルール優先なので本体ロード済みでも不変）。詳細は `logs/honest-unverified.md`。
