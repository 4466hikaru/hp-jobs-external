# 週次技術・ツールウォッチ 2026-09-03（job-022 / 金曜枠 2026-09-04）

- 確認日: **2026-09-03（JST）**。数値・機能記述は特記なき限りこの日に一次ページから取得したスナップショット。
- 対象窓: **2026-08-20 〜 2026-09-03**（直近約2週間）。窓外は「窓外」と明記。
- スタジオ現行スタック（発注どおり。追加の製品主張はしない）: SDXL(WAI v17)+LoRA / ComfyUI / Anima Edit(マスク局所) / Wan2.2 i2v(ループ動画) / image2.0(キーポーズ下絵) / GPT-SoVITS。直近判明: **H3は背景固定不可で不採用**、モーションは**ジュース層+コード変形のD案**。
- 採否判断はしない。事実＋適用可能性の提示まで。誇大な宣伝は一次ソースで裏取りした項目のみ掲載。

---

## 1. 直近2週間の生成AI新技術（うちパイプライン影響候補）

選定方針: 画像モデル新版 / 動画の背景固定・キャラ一貫 / スプライト・ピクセル特化 / LoRA学習効率化のうち、窓内に一次ソースがあるもの。**WAI v17の後継は窓内に見つからず**（後述）。

| # | 項目 | 何ができる（事実） | 出典URL + 確認日 | うちのどの工程に効く可能性 |
|---|---|---|---|---|
| 1 | **Wan 3.0**（Alibaba） | 単パス最大**30秒**動画。入力: テキスト/画像/音声/動画/**文書**(PPT・PDF等)。参照最大約20資産（画像10+動画5+音声5+ファイル1、Comfy公式ブログ表記）。参照一貫性・指示編集・延長。解像度 480/720/1080p。API料金公式: **$0.05/s(480P)・$0.10/s(720P)・$0.20/s(1080P)**。公式が明記する現状弱点: **音声質感・画面内テキスト精度はまだ改善中**。 | [Alibaba Cloud Community 2026-08-13](https://www.alibabacloud.com/blog/wan3-0-30-second-ai-video-generation-from-any-input_603452) / [Comfy.org ブログ 2026-08-25](https://blog.comfy.org/p/wan-30-in-comfyui-native-30-second) / GA報道 [GIGAZINE 2026-08-25](https://gigazine.net/gsc_news/en/20260825-alibaba-wan-3-0/)（確認日 2026-09-03） | **Wan2.2 i2vループ**の上位候補・長尺プレビュー。ループ用ショートより「30秒物語」向き。ローカル重み配布の有無は**未確認**（現時点のComfy導線はAPI/Partnerノード寄り） |
| 2 | **ComfyUI v0.34.0**（2026-08-26） | Partnerノード: **Wan 3.0**動画生成、**Seedance 2.5**（ByteDance・延長/1080p）、**Pixverse V6**、**Fish Audio**基本ノード、**BFL Flux Video Upscale**。MiniMax **H3AddGuide**（任意フレームに画像/音声ガイド固定）、H3向け per-token video/audio latent noise mask、Empty Latent+H3、**taeh3**、HDR/AV1/mkv/webm保存、TRELLIS2 / Sam3d-body。 | [GitHub Release v0.34.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.34.0)（Published 2026-08-26T02:09:08Z）（確認日 2026-09-03） | **ComfyUI本流**の更新。H3は背景固定で不採用済みだが、ノード強化は今後の再評価材料。Fish Audioは**GPT-SoVITS隣接の音声選択肢**。Wan3/Seedanceは動画工程の比較対象 |
| 3 | **Seedance 2.5**（ByteDance / PixVerse掲載） | 4〜30秒。モード: Video(T2V/I2V) / Transition(首尾フレーム) / Reference（画像+動画+音声参照）。PixVerse側上限例: 画像30+動画10+音声10、動画/音声参照合計各最大30秒。480/720p（PixVerse表記）。1080pプロモは**2026-09-18 15:00 BJTまで**（期限付き）。Vercel AI Gateway掲載は2026-08-06（窓やや前）。 | [PixVerse公式 2026-08-20](https://pixverse.ai/en/blog/seedance-2-5-now-available-on-pixverse) / [Vercel Changelog 2026-08-06](https://vercel.com/changelog/seedance-2-5-now-available-on-vercel-ai-gateway) / Comfy Partner反映は上記 v0.34.0（確認日 2026-09-03） | Wan2.2代替比較・**キャラ/モーション参照パック**の実験。背景固定の保証は公式文面に**無し**（§2参照） |
| 4 | **Wan2.2 Fun Camera Control**（Alibaba PAI / Comfy公式チュートリアル）※モデル自体は窓前だが、うちスタック直結のため「現状操作系」として併記 | I2Vでカメラ運動を条件コード化。Comfy `WanCameraEmbedding` の Camera Motion に **Zoom In/Out, Pan系, Static 等**。重み: `alibaba-pai/Wan2.2-Fun-A14B-Control-Camera`（Apache-2.0）。任意で lightx2v 4-step LoRA（高速・ダイナミクス低下の可能性をComfy公式が明記）。 | [ComfyUI Docs Wan2.2 Fun Camera](https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-camera) / [HF README_en](https://huggingface.co/alibaba-pai/Wan2.2-Fun-A14B-Control-Camera/blob/main/README_en.md)（確認日 2026-09-03） | **現行Wan2.2 i2v**へのカメラ固定（Static）実験。ただし「背景ピクセル完全固定」ではない（§2） |
| 5 | **Spriteloom v1.0.0**（AsepriteローカルAI）※**窓やや外: 2026-08-03** | Aseprite内で Generate / Edit / Inpaint / Rotate。モデル **FLUX.2 Klein 4B**（Apache-2.0、約15GB、8-step蒸留）。ローカルGPUのみ（NVIDIA 12GB+推奨、8GBはLegacy遅延モード）。Windows + Aseprite 1.3+。既存ピクセルはクリック挿入まで非破壊。 | [itch.devlog 2026-08-03](https://vkarach.itch.io/spriteloom/devlog/1616156/spriteloom-v100-local-ai-pixel-art-generator-for-aseprite) / [GitHub vkarach/spriteloom](https://github.com/vkarach/spriteloom)（確認日 2026-09-03） | **スプライト/ピクセル工程**の候補。160px級ジュースGIFや敵スプライト下絵の補助。Linux本番機への移植可否は**未確認** |

### 窓内で見つからなかったもの（明記）

| 探したもの | 結果（確認日 2026-09-03） |
|---|---|
| **WAI-illustrious-SDXL v18+** | 二次調査（[offlinecreator 2026-08-29時点](https://offlinecreator.com/civitai/illustrious-xl-nsfw-models-2026)）でも **v17.0が最新**と記載。作者側はハード故障で更新遅延を公表（[SeaArtモデルページ](https://www.seaart.ai/models/detail/d8300cd33eb1ab8018baa6685ec4a7e9)）。**窓内の新版リリースは未確認** |
| **LoRA学習の大幅新手法（窓内一次）** | デュアルGPU model-parallel（ai-toolkit/musubi/OneTrainer向け）は **2026-05** 前後のパッチ群（[flux2-dual-gpu-lora](https://github.com/genno-whittlery/flux2-dual-gpu-lora)）。**窓内の新リリース一次ソースは未確認** |
| **GPT-SoVITS本体の窓内メジャー更新** | 一次リリースノートを窓内で特定できず。**未確認**。Comfy側は Fish Audio Partnerノードが隣接候補（v0.34.0） |

---

## 2. 「背景固定つき動画生成」特化調査（D案アップグレード材料）

要求定義（発注）: **キャラだけ動かし、背景・カメラを完全固定**。H3はこれが不可で不採用済み。

### 2-A. 結論サマリ（判断ではなく現状）

| 問い | 調査日時点の事実 |
|---|---|
| 「背景ピクセル完全固定 + カメラ完全固定 + 被写体のみ運動」を**保証する**商用モデルは出たか？ | **一次ソースで保証文言を確認できた製品は無し**。プロンプトの "static" / Staticブラシ / Fun Camera の Static は「カメラ運動ゼロ条件」や「領域を動かさない指示」であり、**背景の幾何・テクスチャがフレーム間で完全凍結される保証ではない** |
| 最も近い実務レバー | (1) Wan2.2 Fun Camera **Static** (2) Kling系 **Static Brush / 低モーション**（窓前機能の現状確認） (3) Runway系 Motion Brush で背景未塗り or still（二次教程が多く、Gen-4.5公式の完全保証は未確認） |
| 研究側の進展 | **OrthoMotion**（arXiv:2606.22835）がカメラ/被写体運動の表現的絡み合いを証明し、注意演算子で直交分離。Wan2.1バックボーンで CTE を大幅低減。**製品組み込み・Wan2.2/3.0移植は未確認** |

### 2-B. モデル/手法対照表

| モデル・手法 | 窓との関係 | 「背景・カメラ固定」関連の公式事実 | 被写体のみ動かす実用度（事実ベース） | 出典 + 確認日 |
|---|---|---|---|---|
| **MiniMax H3 / Hailuo 03** | 既知・不採用 | プロンプトに Static / カメラ語彙あり。編集ガイドは「背景のどの幾何を残すか」を文章で指定する方式 | スタジオ既判定どおり**背景固定不可**。Comfy v0.34でガイド強化はあるが、固定保証の公式主張は無し | [H3 prompt guide](https://minimax-h3.app/prompt-guide) / [fal H3解説](https://fal.ai/learn/tools/minimax-h3-explained) / [ComfyUI v0.34.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.34.0)（確認日 2026-09-03） |
| **Wan2.2 Fun Camera** | 現行スタック直結 | `WanCameraEmbedding` に **Static** を含むカメラコード。パン/ズーム等も条件化 | **カメラを静止条件にできる**。背景がピクセル単位で凍結するかの公式保証は**無し**。Comfy公式は「カメラ運動への忠実」を謳う | [Comfy Docs](https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-camera) / [HF Control-Camera](https://huggingface.co/alibaba-pai/Wan2.2-Fun-A14B-Control-Camera/blob/main/README_en.md)（確認日 2026-09-03） |
| **Wan 3.0** | 窓内新着 | 30秒・参照一貫・指示編集。「要素を残して変更」は編集機能の説明。**背景完全固定APIは未記載** | 長尺・一貫性は前進。背景固定要件への適合は**未実測・公式未保証** | [Alibaba Cloud](https://www.alibabacloud.com/blog/wan3-0-30-second-ai-video-generation-from-any-input_603452) / [Comfy blog 08-25](https://blog.comfy.org/p/wan-30-in-comfyui-native-30-second)（確認日 2026-09-03） |
| **Kling VIDEO 3.0 / Omni** | **窓前**（2026-02公開系）。現状機能の確認 | Subject Binding / Elements 3.0。教程系に **Static Brushで顔・背景ロック**、Motion Brushで動かす記述。デフォルトがパララックス寄りなので "camera static" 明示が必要、との二次教程あり | 領域ロックUIは「最も近い商用UX」候補。**ピクセル完全固定の一次保証は未確認**。公式ブログ（2026-06-26記事）は一貫性・カメラ制御中心で背景凍結を主訴にしていない | [kling.ai Subject Binding](https://kling.ai/blog/kling-3-subject-binding-character-consistency) / 二次: [AI Tools Guidebook Kling tutorial](https://aitoolsguidebook.com/en/articles/kling-tutorial/) / 公式ローンチ [Kuaishou IR 2026-02-05](https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-30-model-ushering-era-where-everyone-can-be)（確認日 2026-09-03） |
| **Seedance 2.5** | 窓内 | 参照パック・Transition。カメラ/背景ロック専用機能の公式記載**無し** | 背景固定用途の根拠なし（未確認） | [PixVerse 08-20](https://pixverse.ai/en/blog/seedance-2-5-now-available-on-pixverse)（確認日 2026-09-03） |
| **Runway Gen-4.5 + Motion Brush** | Gen-4.5自体は窓前〜年末2025系。ブラシ運用は継続 | 二次教程: 背景を塗らない / still、camera static。Gen-2時代のブラシはGen-4でプロンプト寄りに移行したとの説明もあり、**Gen-4.5公式が「背景完全固定を保証」と書いた一次ページは本調査で未取得** | 部分領域モーションの実務手段としては広く言及。スタジオ要件の保証としては**未確認** | [Runway Gen-4.5 research](https://runway.com/research/introducing-runway-gen-4.5) / 二次教程複数（確認日 2026-09-03） |
| **Luma Ray3.x** | 窓外中心 | キーフレーム・Camera Motion Transfer等（Luma公式比較記事）。**背景固定専用の一次保証は未確認** | 同上 | [Luma vs Runway](https://lumalabs.ai/news/luma-vs-runway)（確認日 2026-09-03） |
| **OrthoMotion**（研究） | 論文 arXiv **2606.22835**（2026-06系）。窓内の製品化は未確認 | 2D条件ではカメラ並進と物体運動が \(1/Z\) で非識別 → 絡み合いは表現問題。RoPE位相（幾何）と cross-attn value注入（意味）を直交正則化。Wan2.1で CTE \(c\to s\) を 11.3→**4.6 px**（正則化有無比較） | **「独立ダイヤル」の理論的回答**。静カメラ+被写体運動に近づく材料。**コード公開・Wan2.2/3.0対応・ゲームスプライト用途の実測は未確認** | [arXiv abs](https://arxiv.org/abs/2606.22835) / [HTML全文](https://arxiv.org/html/2606.22835v1)（確認日 2026-09-03） |
| **ARGUS**（研究・Wan系） | arXiv **2606.11670** | 被写体**同一性**の動的メモリ（3×3モザイク注入）。背景固定問題ではない | キャラ一貫の将来材料。背景固定とは別軸 | [arXiv abs](https://arxiv.org/abs/2606.11670)（確認日 2026-09-03） |
| **AnimateDiff / SVD / 古典ControlNet video** | 古典・窓外 | 歴史的にカメラ制御やポーズ条件はあるが、**2026-08-20以降の「背景完全固定を新規解決した」一次リリースは未確認** | D案の代替としては古く、新規突破なし | 窓内一次なし（確認日 2026-09-03） |

### 2-C. D案との関係（事実のみ）

- 現状のD案（ジュース層+コード変形）は、**生成動画に背景固定を求めない**設計。
- 将来アップグレード材料として一次ソース上もっとも具体的なのは:
  1. **Wan2.2 Fun Camera Static**（既存スタックで即試せる操作）
  2. **OrthoMotion系のカメラ/被写体分離**（研究、製品化は未確認）
  3. **Kling Static Brush系の領域ロックUX**（商用、完全固定は未保証）
- Wan 3.0 / Seedance 2.5 は長尺・参照一貫では前進だが、**背景固定問題の解答としては公式未主張**。

---

## 3. 改善提案（採用はユーザー）

判断・採否はしない。事実 → 選択肢まで。

1. **事実:** 窓内の最大イベントは **Wan 3.0（〜08-24/25）+ ComfyUI 0.34.0（08-26）**。現行は Wan2.2 i2v。公式は30秒・多参照・編集を前進させつつ、音声/画面文字は弱点と自己申告。  
   **選択肢:** (a) Wan2.2ループを維持し Wan3 はAPI比較だけ (b) ループ用途で Wan3 I2Vを短尺テスト (c) 触らない。採否はユーザー。

2. **事実:** 背景完全固定を保証する新モデルは窓内に出ていない。Fun Camera の **Static** と領域ブラシ系が最寄り。OrthoMotionは研究で CTE 低減を数値提示。  
   **選択肢:** (a) D案維持のまま Fun Camera Static を計測ログだけ取る (b) OrthoMotion/類似の実装動向を次週以降ウォッチリスト化 (c) Kling Static Brush をクラウドで1日検証。採否はユーザー。

3. **事実:** WAI v17後継は窓内未確認。Spriteloomは08-03公開（窓やや外）でローカルAseprite+FLUX.2 Klein。  
   **選択肢:** (a) 画像基盤はWAI v17据え置き (b) SpriteloomをWindows作業機でスプライト下絵試験 (c) 両方見送り。採否はユーザー。

4. **事実:** Comfy 0.34 に Fish Audio Partnerノード。GPT-SoVITS本体の窓内更新は未確認。  
   **選択肢:** 音声は現状維持 / Fish Audioを試聴比較のみ / 週次でSoVITS更新を再サーチ。採否はユーザー。

---

## 正直申告

- 本調査は WebSearch + WebFetch。**実機で動画を生成して背景固定を測ったわけではない**。
- H3不採用は発注の前提事実として扱い、再実測していない。
- Kling / Runway の「Static Brushで背景が完全固定」は**教程・二次が多く、公式の保証文としては弱い**。未確認と明記した。
- Spriteloomは窓の約2.5週前（08-03）。スプライト特化のため表に入れたが、厳密な「直近2週間」からは外れる。
- Wan 3.0の**ローカル重み配布・商用ライセンス詳細・NSFW耐性**は未確認（Cloud/API導線中心）。
- LoRA効率化の窓内一次ニュースは薄く、5月のデュアルGPUパッチを「窓外」として触れたのみ。
- WAI新版なしは二次記事+作者コメントページに依存。Civitaiカードの直接スクレイプはブロックされうるため、**最終版番号の一次確定は弱い**（「未確認の新版なし」扱い）。
- 数値の捏造なし。取れない項目は「未確認」。

## 要判断（ユーザー。調査者は決めていない）

1. Wan 3.0 を Wan2.2 ループ工程の比較対象に入れるか。
2. 背景固定の再挑戦を Fun Camera Static / Klingブラシ / 研究ウォッチのどれ（または無し）にするか。
3. Spriteloomをスプライト工程の試験対象にするか（Windows前提）。
4. ComfyUI を v0.34.0 系へ上げるか（H3ノード増はあるがH3自体は不採用済み）。
