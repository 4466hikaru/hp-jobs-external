# job-019: contentデータ整合監査(リリスroster矛盾の同類を全域検出)

- status: in-progress(game)

## 背景
キャラ選択画面で「rosterEnabled=true なのに initiallyUnlocked=false+ロックカード」の矛盾が発覚(隠し7人目、#28で裁定中)。**同じ構造の「フラグ同士が矛盾する/UI表示と食い違う」データが他にも潜んでいる疑い**がある。job-011(バランス監査)と同系の得意分野として発注する。

## 作業
1. 対象: hp-game-shareミラーの content/*.json(characters/enemies/scenes/assets/weapons等。ミラーが古い場合はその旨を明記した上でミラー時点の監査として実施)
2. 監査観点: ①解放系フラグの矛盾(enabled系 vs unlocked系 vs contentStatus) ②参照整合(存在しないIDへの参照、逆に未参照の定義) ③状態語の不統一(同じ意味に別の語が使われている) ④明らかな仮値・placeholder残り(release到達フラグ付きなのにtodo/仮値)
3. 成果物: `deliverables/job-019/data_audit.md` — 検出表(ファイル/キー/矛盾内容/重要度: 高=リリース前に直すべき/中/低)。**検出ゼロの観点も「検出なし」と明記**。修正はしない(検出と根拠提示まで)。PRで提出

## 注意
- リリス関連の記述はスポイラーに配慮し「hidden 7th」等の婉曲表現で(実名・加入条件の詳述は不要、#28で扱う)
- 巨大出力禁止: 検出表は要点のみ、JSONの全文引用はしない
