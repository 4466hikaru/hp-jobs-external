# job-017 notes — 入稿要件調査ハイライト（2026-08-30）

事実と出典のみ。採否・方針判断はしない。

## 重要な変更・現行注意点

### DLsite
1. **モザイク規格は数値で公開されている**（長辺×1/100、最小4px、例示6/8/12px）。出典: [コンプライアンスポリシー](https://www.dlsite.com/home/mosaic)。ゲーム内解像度ごとにセルサイズを再計算する必要がある、という運用リスク。
2. **AIオプションは二択＋紹介文記載が必須**。「AI生成作品」はフロア分離・月3本上限・販売日指定不可など制約が重い。出典: [違い](https://cs-circle.dlsite.com/hc/ja/articles/14941563173657) / [販売に関して](https://cs-circle.dlsite.com/hc/ja/articles/14941627991321)。**どのオプションに該当するかの判定は本ジョブでは行わない**。
3. **紹介画像サイズの形式表記が公式ページ間で不一致**: `webup` は JPEG のみ、サークルヘルプは jpg/png（透過不可）。入稿直前に Webアップロード画面の現行ヒントで再確認が必要。
4. **審査目安は2〜3日**だが保証ではなく、AI生成は延長・販売順前後あり。販売希望日は申請日+3日以降。出典: [管理画面](https://cs-circle.dlsite.com/hc/ja/articles/31531949952281) / [販売日指定](https://cs-circle.dlsite.com/hc/ja/articles/360061739574)。
5. ゲームは **オフライン完結・対応OS設定・審査用データ推奨**。ネット必須作品は登録不可。

### Steam
1. **カプセルは2024-08以降の大型サイズのみ**。旧サイズは受理されない。出典: [Graphical Assets Overview](https://partner.steamgames.com/doc/store/assets)。
2. **スクショ最低5枚・1920×1080・16:9・実プレイのみ**。全年齢向け表示用マークの運用あり。出典: [Store Graphical Assets](https://partner.steamgames.com/doc/store/assets/standard)。
3. **AI開示は Content Survey の現行セクション**（Pre-Generated / Live-Generated）。効率化ツールは焦点外。Adult Only Sexual Content × Live-Generated AI は公式に「現時点で出荷したくない」。出典: [Content Survey](https://partner.steamgames.com/doc/gettingstarted/contentsurvey)。
4. **タイムラインの下限**: Direct料金後30日 + Coming Soon最低2週間 + ストア/ビルド各3–5営業日（各7営業日前提出推奨）。出典: [Steam Direct](https://partner.steamgames.com/steamdirect) / [Coming Soon](https://partner.steamgames.com/doc/store/coming_soon) / [Review Process](https://partner.steamgames.com/doc/store/review_process)。
5. 全年齢想定でも Mature Content Survey の正直な開示は必須（ビルド内に成人向けデータがある場合は非表示でも開示）。Adult Only Sexual Content マーク時は審査フローが変わる。

## リスク（事実ベース）

| リスク | 根拠 |
|---|---|
| DLsiteモザイク差し戻し | ピクセル基準・輪郭線・透過で明瞭になるケースがポリシー明示 |
| DLsite AIオプション誤選択 | 証明要求・オプション強制付与・月3本・販売日指定不可 |
| Steam旧カプセルサイズ | 2024-08以降旧寸法非受理 |
| Steam Coming Soon / 30日待機の見落とし | 12月目標からの逆算でクリティカルパスになり得る（数値は公式） |
| Survey未開示・不正確 | Content Survey FAQ: ルール遵守は Survey 完了だけでは足りない |

## 未確認リスト（公式で数値・全文を取れなかったもの）

1. DLsite 宣伝紹介文の**厳密な最大文字数**（「300字程度」以外）
2. Steam Mature Content Survey の**個別設問の完全一覧**
3. Steam short description の**公式文字数上限**（Editing doc に数値なし）
4. DLsite 紹介画像の **JPEGのみ vs png可** の現行UI実制限（ページ間表記差）
5. Steamworks パートナー専用画面にしか出ない追加チェック項目（ログイン必須領域は未取得）

## 調査手順メモ
- WebFetch / curl で公式ページ本文を取得（2026-08-30）。
- cs-circle.dlsite.com の一部は Cloudflare で WebFetch がブロックされることがあり、その場合は curl + User-Agent で取得。
- 第三者ブログ・Ci-en の数値は採用していない（モザイク例示は公式ポリシー本文で確認済み）。

