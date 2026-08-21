# job-013 正直申告

日付: 2026-08-21 08:18 JST（記録開始。完了は同日）

## 実行していないこと

1. Godot headless / 実機 / 固定 seed プレイなし。キャリーオーバーの加算は `_dungeon_carryover_bonus_delta` の静的写経。
2. hp-game-share は clone していない。`gh api` の raw 取得のみ。
3. ゲーム本体 repo へパッチ未適用。jobs repo の `deliverables/job-013/patches/` に置いただけ。
4. `buffs.json` を `_load_content` に足していない。
5. 死にデータの実削除なし。
6. 数値チューニングなし（0.5 は 0.5、明示基礎率は現行 fallback 0.1）。
7. job-002、PR#12（020/024）、job-014、job-015 は未着手。
8. `fix/review-high-confidence` の Main.gd には本ジョブのパッチを当てていない（現行は `main`）。

## 検証の限界

- cap / base_rate の「修正前後で実効値が同一」は Python で `_clamp_carryover_target_value` と `rule.get`/`dungeon.get` を再実装した比較。エンジン実行ではない。
- gdparse は構文木が組めることまで。型・実行時の Dictionary キー欠落は見ていない。
- ミラー鮮度: `main` pushed_at は 2026-08-18 19:09 JST のまま。本体が既に buffs を読んでいる可能性は job-009/011 と同じ。その場合:
  - 001 の cap 追加は「ロード後にキー欠落で fallback していた穴」を同じ 0.5 で塞ぐ（H2 の意図）
  - 002 は `rule.get` が先なので、ルールに `baseCarryoverRate` がある限り dungeon 明示値は使われない → ロード済み本体でも基礎率は不変
- 個別バフ19件の戦闘未適用（H3）は残っている。
- `continueCarryoverBonusPerRound` は今回触っていない（L6。基礎率とは別フィールド）。

## 前提

- 現行ミラーの実効基礎率は全ダンジョン 0.1（buffs 未ロード）。
- A-02 の5件は `carryover.default` 以外（溶鉱炉/修道院/観測台/大聖堂/玉座）。観測台の仕様値は元から 0.1。
- 改行は取得ファイルもパッチも CR=0。
