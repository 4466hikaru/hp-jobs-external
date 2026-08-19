---
status: draft-wave2
approved_at: null
created_at: 2026-08-19
current_game_revision: 008746240edaef2c39f876832be31d6d9003d2b4
source_flow_revision: ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd
source_flow_artifact_sha256: d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a
source_flow_artifact: outputs/screen_flow_extract_0818/screen_flow.json
coverage_leaves: [I-2, I-4, I-5, I-6, I-7, I-8, I-10, I-11, I-12, II-8]
---

# 10-02 49画面・135遷移 現状仕様カタログ

本書は承認済み`10_screens.md`の画面目的/表示/状態と、検収合格済みscreen-flow抽出の49 node/135 edgeを機械結合した第2波draftである。画面構成は今後ユーザー決裁予定のため、現状仕様を承認済みへ昇格しない。edgeの完全表は`outputs/spec_coverage_wave2_0819/screen_trace.csv`。

## 10-02-00 共通契約

- 全画面: `spec_status=draft-wave2`, `approved_at=null`。
- 各節は目的、表示要素、遷移、状態、実装状態、gap、完成定義、根拠を必須とする。
- 遷移は`from/to/trigger/condition/source`を保持し、入力artifactとの集合一致をvalidatorで検査する。
- 見た目は承認済み理想画像との一致を別ゲートで判定し、到達可能=見た目合格とはしない。

## SCR-01 `boot_splash` — 起動スプラッシュ

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 起動状態と必要なお知らせを短く示す。
- **表示要素**: 固定=ロゴ・起動進捗・法的/年齢前段。 / 拡張=お知らせ1枠。 / 理想=`01_起動スプラッシュ.png`。
- **状態**: 操作/状態=Confirmで進む、`normal / loading / complete`。 到達性=`reachable`、capture=`captured`、entry=_ready() の通常起動。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `age_gate` | 自動待機完了または決定; _should_show_age_gate() | 年齢確認が必要かつ未受諾 | measured | `Main.gd:7055-7069` |
  | `title` | 自動待機完了または決定 | 年齢確認不要または受諾済み | measured | `Main.gd:7055-7069` |

- **実装状態**: 旧マスター=崩れあり。未コミット `r3` 自動監査=4違反。 screen-flow=`reachable/measured`。
- **ギャップ**: `[乖離]` 「開発中ビルド」等のデバッグ文言露出。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 年齢確認またはタイトルへ遷移し、製品画面にデバッグ文言が0件、理想一致ゲートがPass。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`01 boot_splash`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `boot_splash`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-02 `age_gate` — 年齢確認

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 年齢条件への同意/戻りを明示する。
- **表示要素**: 固定=年齢条件、同意・戻る。 / 拡張=ストア/地域注意。 / 理想=`02_年齢確認.png`。
- **状態**: 操作/状態=同意/戻るをクリック・Enter/A・Esc/B、`normal / denied / accepted`。 到達性=`conditional`、capture=`captured`、entry=ストア年齢確認が必要かつ未受諾の場合。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `title` | 「同意する」/Enter/A | 保存成功後 | measured | `Main.gd:7072-7095` |

- **実装状態**: 旧マスター=崩れあり、`r3`=3違反。 screen-flow=`conditional/measured`。
- **ギャップ**: `[乖離]` 表示確認用のデバッグ説明が露出。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 同意時のみタイトルへ進み、戻りで安全に終了/前画面へ戻り、説明は製品文言である。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`02 age_gate`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `age_gate`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-03 `title` — タイトル / メインメニュー

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 新規/続き/ギャラリー/設定への入口。
- **表示要素**: 固定=ロゴ、主導線4つ。 / 拡張=お知らせ/ストア。 / 理想=`03_タイトル.png`。D-01=明朝方向（2026-07-25）、D-03=現行パレット（2026-07-25）、D-02=現行より縮小。タイトルに墓地モチーフやメニュー箱を置かない（2026-07-15）。
- **状態**: 操作/状態=クリック・方向キー/D-pad・Enter/A、`normal / save_available / confirm_new`。 到達性=`reachable`、capture=`captured`、entry=boot完了; 年齢確認受諾; セーブ読込後; タイトル復帰。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `new_game_confirm` | 「はじめから」 | 既存または破損したセーブあり | static | `Main.gd:7183-7189` |
  | `scene_view` | 「はじめから」 | 空セーブかつプロローグデータあり | measured | `Main.gd:7205-7228` |
  | `town_menu` | 「つづきから」 | 有効セーブの最終位置が町 | static | `Main.gd:7266-7296` |
  | `world_map` | 「つづきから」 | 有効セーブに町解決先がない | static | `Main.gd:7266-7296` |
  | `save_load_menu` | B1タイトル第3アクション「セーブ/ロード」 | なし | static | `Main.gd:9813-9828` |
  | `system_menu` | F8 | debug build または --dev。実装上は任意run_stateからも発火するグローバル開発ショートカット | static | `Main.gd:2492-2502` |

- **実装状態**: 旧マスター=崩れあり、`r3`自動監査=0違反。ただし自動0は理想一致Passを意味しない。 screen-flow=`reachable/measured`。
- **ギャップ**: `[乖離]` 旧監査でロゴを赤線が横切る。人間の理想一致再判定も未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 4導線が到達可能、ロゴに装飾線が重ならず、書体/配色/密度が理想と一致。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`03 title`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `title`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-04 `new_game_confirm` — はじめから確認

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 新規開始による保存初期化を理解して確定する。
- **表示要素**: 固定=対象スロット、警告、開始/戻る。 / 拡張=バックアップ/詳細警告。 / 理想=`04_新規開始確認.png`。
- **状態**: 操作/状態=Confirm/Back、`normal / destructive_warning / confirmed`。 到達性=`conditional`、capture=`captured`、entry=タイトルで既存/破損セーブがある状態で「はじめから」。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `scene_view` | 「はじめから」確認 | プロローグデータあり | static | `Main.gd:7193-7228` |
  | `town_menu` | 「はじめから」確認 | プロローグデータがない場合のフォールバック | static | `Main.gd:7205-7257` |
  | `title` | 「キャンセル」/Esc/B | なし | static | `Main.gd:6532-6534,7201-7202` |

- **実装状態**: `STATE_NEW_GAME_CONFIRM`実装。旧マスターでは監査枠外だったが、未コミット `r3` は49件の一つとして撮影済み（1違反）。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 監査枠追加は未コミットで、人間の理想一致判定も未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 新規確定でプロローグへ、取消でタイトルへ戻り、監査画像と理想比較を保存。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`04 new_game_confirm`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `new_game_confirm`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-05 `save_load_menu` — セーブ / ロード

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 空/利用可能/破損スロットを区別しロードする。
- **表示要素**: 固定=スロット状態、ロード、新規、戻る。 / 拡張=最終日時/詳細。 / 理想=`05_セーブ選択.png`。
- **状態**: 操作/状態=クリック・上下・Enter/A・Esc/B、`empty / ready / corrupt / selected`。 到達性=`reachable`、capture=`captured`、entry=B1タイトルの第3アクション、ポーズ。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `title` | 新規スロット作成、ロード、または戻る | B1第1アクション/戻る | static | `Main.gd:7529-7760,9887-9921` |

- **実装状態**: セーブ状態定数と画面を実装。旧監査は問題なし、`r3`=1違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` 自動監査の英字トークン残り。理想一致未判定。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 3状態を誤認なく表示し、ロード/新規/戻るが正しく遷移する。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`05 save_load_menu`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `save_load_menu`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-06 `save_delete_confirm` — セーブ削除確認

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 削除対象と不可逆性を明示して二択にする。
- **表示要素**: 固定=スロット名、警告、削除、戻る。 / 拡張=復元猶予。 / 理想=`06_セーブ削除確認.png`。
- **状態**: 操作/状態=Confirm/Back、`normal / pending / deleted`。 到達性=`unwired_current`、capture=`captured`、entry=旧save_loadの削除だけが入口。現行B1 save/loadは削除アクションをbindしていない。
- **遷移**:

  - `classification=unwired_current`。現行runtime入口なし（SCR-G02）。edgeを発明せず、採用決裁後の再配線か製品対象外の明記を待つ。

- **実装状態**: 実装済み、旧監査は問題なし、`r3`=1違反。 screen-flow=`unwired_current/static`。
- **ギャップ**: `[乖離]` 自動監査の英字トークン。理想一致未判定。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 指定スロットだけを削除し、取消は無変更、警告と焦点が明瞭。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。 本画面は、製品導線へ配線して再抽出edgeを得るか、製品対象外と決裁されるまで未完了。
- **根拠**: `docs/spec/10_screens.md`の`06 save_delete_confirm`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `save_delete_confirm`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-07 `reset_confirm` — セーブリセット確認

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 開発用の全初期化を危険操作として隔離する。
- **表示要素**: 固定=危険性、対象、取消。 / 拡張=二段階コード入力。 / 理想=`07_全初期化確認.png`。
- **状態**: 操作/状態=dev時のみ Confirm/Back、`normal / armed / complete`。 到達性=`developer_only`、capture=`captured`、entry=system_menuの「セーブを初期化」。F8/--dev系が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `title` | 初期化後の戻る / 戻る | 開発モードで入口を使用 | static | `Main.gd:13609-13624` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`developer_only/static`。
- **ギャップ**: `[乖離]` 製品隔離の実機確認と英語破壊操作文言の解消が未検収。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 製品導線では到達不能、dev時は二段階確認後だけ初期化。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`07 reset_confirm`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `reset_confirm`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-08 `unlock_confirm` — 全解放デバッグ

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 開発用全解放を製品導線から隔離する。
- **表示要素**: 固定=対象・警告・取消。 / 拡張=解放対象一覧。 / 理想=`08_全解放確認.png`。
- **状態**: 操作/状態=dev時のみ Confirm/Back、`normal / confirmed`。 到達性=`developer_only`、capture=`captured`、entry=system_menuの「全解放」。F8/--dev系が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `title` | 全解放後の戻る / 戻る | 開発モードで入口を使用 | static | `Main.gd:13626-13681` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`developer_only/static`。
- **ギャップ**: `[乖離]` 隔離の実機確認と英語残りの解消が未検収。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = dev無効時は到達不能、dev有効時のみ全解放、製品文言。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`08 unlock_confirm`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `unlock_confirm`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-09 `credits_license` — クレジット / ライセンス

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 制作者・第三者・AI利用・ライセンスを表示する。
- **表示要素**: 固定=セクション、ライセンス行、画面内の戻る。 / 拡張=外部ライセンス詳細。 / 理想=`09_クレジットとライセンス.png`。
- **状態**: 操作/状態=スクロール/戻る、`normal / scrolling`。 到達性=`conditional`、capture=`captured`、entry=最終/個別ED完了後。開発system_menuからも可。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `title` | 戻る/決定 | エンディング起点またはタイトル起点 | measured | `Main.gd:7804-7857` |

- **実装状態**: 旧マスター=崩れあり、`r3`=30違反。 screen-flow=`conditional/measured`。
- **ギャップ**: `[乖離]` 戻る導線不在、仮名義・英字が残る。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 全文を読め、クリック/パッド/Esc/Bの全てで戻れ、仮題・仮名義が0件。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`09 credits_license`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `credits_license`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-10 `stage_select` — ステージ選択

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 開発用の直接起動。
- **表示要素**: 固定=ステージ、報酬、開始、戻る。 / 拡張=テスト条件。 / 理想=`10_ステージ選択.png`。
- **状態**: 操作/状態=dev時のみ選択/開始/戻る、`normal / selected / dev_only`。 到達性=`developer_only`、capture=`captured`、entry=F8で開くsystem_menuの開発メニューから。_dev_ui_screens_enabled が必須。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `world_field_playing` | 「Start Run」 | 開発画面かつ選択ステージが解放済み | static | `Main.gd:7897-7950` |
  | `title` | Back/Esc/B | 開発画面 | static | `Main.gd:7897-7950` |

- **実装状態**: 旧マスター=崩れあり、`r3`=7違反。 screen-flow=`developer_only/static`。
- **ギャップ**: `[乖離]` 通常導線未接続、英語・戻る表示なし。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 製品導線に出ず、dev時のみ到達/戻る可能。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`10 stage_select`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `stage_select`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-11 `world_map` — ワールドマップ一覧

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 解放済み地域と次の行き先を選ぶ。C案探検圏型（2026-07-15）=7地域×町1/主ボス1/前座2/イベント3/隠し1の56行き先。
- **表示要素**: 固定=ノード、解放、地域遷移。 / 拡張=凡例、目的ショートカット。 / 理想=`11_ワールドマップ.png`。D-06=全日本語化。
- **状態**: 操作/状態=ノードをクリック/方向キー/D-pad、Enter/A決定、Esc/Bは町へ、`normal / node_selected / node_locked`。 到達性=`reachable`、capture=`captured`、entry=町/地域/タイルマップからの復帰、既存セーブの継続。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `world_map` | 方向キー/ノード選択 | 接続ノードの選択のみ | static | `Main.gd:8013-8018,8851-8859` |
  | `town_menu` | town node を決定 | 地域/ノードが解放済み | static | `Main.gd:8654-8718,8885-8910` |
  | `dungeon_info` | dungeon/boss/prelude node を決定 | ダンジョン入場解放済み | static | `Main.gd:8141-8148,8654-8718` |
  | `world_tile_map` | field node の「地域を歩く」 | 地域が解放済み、world_tilesあり | static | `Main.gd:8654-8718` |
  | `world_field_playing` | field nodeの戦闘開始 | field nodeが行動可能 | static | `Main.gd:8654-8718,8885-8910` |
  | `objective_log` | 「目的」 | なし | static | `Main.gd:8024-8025` |
  | `title` | 戻る | 町起点でない場合 | static | `Main.gd:8801-8813` |

- **実装状態**: `worldmap.json` は7地域・56 nodes。`Main.gd`にマップ復帰処理がある未コミット状態。旧マスター=崩れあり、`r3`=1違反。 screen-flow=`reachable/measured`。
- **ギャップ**: `[乖離]` カード文字切断/凡例判別性。Esc復帰は未コミット・実機未検証。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 56ノードのロック/解放がデータ通りで、凡例・文字が判読でき、Esc/Bは町へ戻る。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`11 world_map`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `world_map`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-12 `objective_log` — 目的ログ

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 現在目的を一読で理解する。
- **表示要素**: 固定=現在目的、完了済み、戻る。 / 拡張=ピン留め、フィルタ。 / 理想=`12_目的ログ.png`。
- **状態**: 操作/状態=戻る、`normal / empty / objective_complete`。 到達性=`reachable`、capture=`captured`、entry=町、ポーズ、ワールドマップの目的導線。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `world_map` | 「地図で目的地を確認」または戻る | world_map起点 | static | `Main.gd:8917-8972,10392-10429` |
  | `town_menu` | 戻る | town起点 | static | `Main.gd:8958-8972` |
  | `pause` | 戻る | pause起点 | static | `Main.gd:8958-8972` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` 旧監査で目的本文がプレースホルダー。未コミット修正の実機/理想検収が未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = プレイヤー向けの現目的だけを表示し、開発監査文言が0件。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`12 objective_log`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `objective_log`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-13 `region_menu` — 地域詳細

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 地域内の町・ダンジョン・行動先を選ぶ。
- **表示要素**: 固定=行動先、帰還先、ロック。 / 拡張=地域説明、推奨戦力。 / 理想=`13_地域メニュー.png`。
- **状態**: 操作/状態=クリック/方向キー/D-pad/Enter/A、Esc/Bでマップへ、`normal / selected / locked`。 到達性=`reachable`、capture=`captured`、entry=町の戻る、ダンジョン情報の戻る。B3地域画面。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `town_menu` | 地域画面の町ホットスポット | 町データあり | static | `Main.gd:10939-10957` |
  | `dungeon_info` | 地域画面のダンジョンホットスポット | 入場解放済み | static | `Main.gd:10939-10957` |
  | `world_tile_map` | 「地域を歩く」 | world_tilesあり | static | `Main.gd:10939-10957` |
  | `world_map` | 「地図へ戻る」 | なし | static | `Main.gd:10939-10957` |

- **実装状態**: 実装・監査済み、旧マスター=崩れあり、`r3`=0違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` 旧監査のカード文字切断。理想一致未判定。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 解放済み行動先だけを決定でき、文言が切れず、戻る先が一貫。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`13 region_menu`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `region_menu`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-14 `world_tile_map` — 歩行型ワールドタイルマップ

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 条件付きフィールドで移動先/調査対象を選ぶ。
- **表示要素**: 固定=現在地、タイル、危険表示。 / 拡張=凡例、ズーム。 / 理想=`14_タイルフィールド.png`。
- **状態**: 操作/状態=タイル選択、Enter/A、Esc/B、`normal / tile_selected / tile_locked / data_missing`。 到達性=`conditional`、capture=`captured`、entry=町の「街道へ出発」、地域の「地域を歩く」。world_tilesデータが必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `town_menu` | 町オブジェクトを起動 | タイルマップ上の近接対象 | static | `Main.gd:8164-8175` |
  | `dungeon_info` | ボスダンジョンを起動 | タイルマップ上の近接対象 | static | `Main.gd:8164-8175` |
  | `world_field_playing` | prelude_dungeon nodeを起動 | ノード解放・データ依存 | unconfirmed | `Main.gd:8164-8175` |
  | `world_map` | 戻る | なし | static | `Main.gd:8181-8185` |

- **実装状態**: `world_tiles.json` schema v2、状態実装あり。旧マスターでは監査枠外、未コミット `r3`=3違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` dev隔離と理想一致が未検収。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = `world_tiles` 有効時だけ正しく動作し、製品主線には露出しない。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`14 world_tile_map`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `world_tile_map`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-15 `town_menu` — 町メニュー

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 購入、売却、編成、装備、強化、出発、目的、召喚を選ぶ拠点。
- **表示要素**: 固定=主要施設、出発、所持資源。 / 拡張=新施設/イベントカード。 / 理想=`15_町.png`。
- **状態**: 操作/状態=カードをクリック/方向キー/D-pad/Enter/A、Esc/Bはタイトル確認、`normal / menu_locked / objective_updated`。 到達性=`reachable`、capture=`captured`、entry=新規プロローグ後、継続、地域/タイル/結果から。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `objective_log` | 「目的を確認する」 | なし | static | `Main.gd:10043-10067` |
  | `shop` | 「商店で準備する」 | shopIdあり | static | `Main.gd:10043-10067` |
  | `equipment_list` | 「装備を整える」 | build_menus_unlocked | static | `Main.gd:10043-10067` |
  | `character_select` | 「仲間を編成する」 | build_menus_unlocked | static | `Main.gd:10043-10067` |
  | `world_tile_map` | 「街道へ出発する」 | 地域解放かつworld_tilesあり | static | `Main.gd:10043-10067` |
  | `region_menu` | 「戻る」 | 地域解放済み | static | `Main.gd:10043-10067` |
  | `scene_view` | ルート調整中の「会話する」 | RP選択肢を持つストア利用可能なsceneあり | unconfirmed | `Main.gd:9234-9375` |
  | `save_delete_confirm` | Esc/Bの「タイトルへ戻りますか」 | 画面IDをsave_delete_confirmとして再利用 | static | `Main.gd:6606-6616,7712-7719` |

- **実装状態**: `towns.json` 7町、`Main.gd`にタイトル確認の未コミット実装。旧マスター=崩れあり、`r3`=0違反。 screen-flow=`reachable/measured`。
- **ギャップ**: `[乖離]` カード説明の文字切断。Esc確認の実機検証/コミット未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 全主要導線が到達可能で、Esc/Bは即タイトル遷移せず確認を出す。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`15 town_menu`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `town_menu`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-16 `shop` — ショップ購入

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 黒貨、価格、効果、在庫を比較して購入する。
- **表示要素**: 固定=商品、価格、所持金、購入結果。 / 拡張=カテゴリ/数量。 / 理想=`16_商店.png`。
- **状態**: 操作/状態=商品を押下、Enter/A購入、Esc/B町、`normal / sold_out / insufficient_funds`。 到達性=`reachable`、capture=`captured`、entry=町の「商店で準備する」。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `sell_inventory` | B3ショップの「売却」 | なし | static | `Main.gd:10989-11041` |
  | `town_menu` | B3ショップの「戻る」 | なし | static | `Main.gd:10989-11041` |

- **実装状態**: `shops.json` 7店/21品、購入・売却コードあり。旧監査問題なし、`r3`=0違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` 人間の理想一致判定未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 価格・在庫・所持金の計算がデータ通りで、購入後に通貨/在庫/UIが同期。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`16 shop`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `shop`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-17 `sell_inventory` — 売却 / 所持品

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 所持品・売値・保護状態を確認して売却する。
- **表示要素**: 固定=所持数、売値、保護。 / 拡張=一括選択/保護タグ。 / 理想=`17_売却.png`。
- **状態**: 操作/状態=商品選択/売却、Esc/B町、`normal / empty / selected_item`。 到達性=`reachable`、capture=`captured`、entry=B3ショップの「売却」。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `item_detail` | 所持品行または「詳細を見る」 | 売却可能所持品あり | static | `Main.gd:11041-11073` |
  | `shop` | 「商店へ戻る」 | なし | static | `Main.gd:11041-11073` |

- **実装状態**: 実装済み、旧監査問題なし、`r3`=0違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` 理想一致未判定。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 保護品を誤売却せず、売却後に所持数/黒貨が同期。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`17 sell_inventory`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `sell_inventory`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-18 `item_detail` — 所持品詳細

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 性能・用途・使用/売却を読む。
- **表示要素**: 固定=効果、比較、使用/売却導線。 / 拡張=入手先/お気に入り。 / 理想=`18_アイテム詳細.png`。
- **状態**: 操作/状態=選択/Confirm、Esc/Bで戻る、`normal / usable / unusable`。 到達性=`conditional`、capture=`captured`、entry=売却一覧の詳細。売却可能な所持品が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `sell_inventory` | 「戻る」 | なし | static | `Main.gd:11073-11093,11284-11285` |

- **実装状態**: 旧マスター=崩れあり、未コミット修正を含む可能性、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` Description/Use/Sell等の英語と戻る導線を、実機/人間検収で再確認。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 画面内に戻る導線があり、製品文言は全て日本語で判読可能。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`18 item_detail`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `item_detail`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-19 `summon_select` — 召喚石選択

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 消費資源と召喚候補を理解して選ぶ。
- **表示要素**: 固定=召喚石、解放、装備決定。 / 拡張=詳細/比較。 / 理想=`19_召喚選択.png`。押下型原則の対象。
- **状態**: 操作/状態=召喚物絵を押下、方向キー/D-pad、Enter/A、Esc/B、`normal / locked / selected / empty`。 到達性=`reachable`、capture=`captured`、entry=ダンジョン情報の「召喚石」。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `summon_select` | 召喚石を選択 | 解放済み召喚石 | static | `Main.gd:9377-9435` |
  | `dungeon_info` | 戻る | dungeon_info起点 | static | `Main.gd:9435-9443` |
  | `town_menu` | 戻る | town起点 | static | `Main.gd:9435-9443` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` 全カード同一仮データ・英語。`[未決]` 新理想（対象画像押下）を承認すること。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 押下対象が召喚物そのもので、仮データなし、ロック理由が表示される。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`19 summon_select`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `summon_select`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-20 `character_select` — キャラクター選択

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 解放条件・性能を比較して出撃キャラを決める。
- **表示要素**: 固定=キャラ肖像、性能、解放、確定。 / 拡張=並替え/詳細比較。 / 理想=`20_キャラクター選択.png`。押下型原則の対象。
- **状態**: 操作/状態=肖像/デフォルメを押下、方向キー/D-pad、Enter/A、Esc/B、`normal / locked / selected`。 到達性=`conditional`、capture=`captured`、entry=町の「仲間を編成する」。build_menus_unlocked が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `dungeon_playing` | 「この編成で出撃」 | 選択キャラクター有効 | static | `Main.gd:11540-11572` |
  | `equipment_list` | 「装備を調整」 | なし | static | `Main.gd:11540-11572` |
  | `town_menu` | 戻る | town起点 | static | `Main.gd:12270-12291` |

- **実装状態**: 旧マスター=崩れあり、`r3`=5違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 首なしクロップ/白背景。`[未決]` image2.0の新理想案承認待ち。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 対象画像が押下面で、顔を含む透過素材、フォーカス/ロック理由/確定が明瞭。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`20 character_select`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `character_select`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-21 `equipment_list` — 女性キャラ装備一覧

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 誰の装備を編集するか選ぶ。
- **表示要素**: 固定=キャラ、装備状態、次画面。 / 拡張=プリセット。 / 理想=`21_装備一覧.png`。
- **状態**: 操作/状態=キャラ絵を押下、Enter/A、Esc/B、`normal / locked / selected`。 到達性=`conditional`、capture=`captured`、entry=町の「装備を整える」。build_menus_unlocked が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `equipment_slots` | 同行者カード/「装備を編集」 | 解放済み同行者あり | static | `Main.gd:10139-10188,11713-11760` |
  | `character_select` | 「ヒロイン編成」 | なし | static | `Main.gd:11713-11760` |
  | `town_menu` | 戻る | town起点 | static | `Main.gd:12270-12291` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 首なしクロップ/白背景。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 顔を含む対象画像を押して装備スロットへ進み、戻り先が保持される。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`21 equipment_list`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `equipment_list`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-22 `equipment_slots` — 装備スロット

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 現在装備・空き・ロックを確認し部位を選ぶ。
- **表示要素**: 固定=部位、装備状態、候補導線。 / 拡張=比較/外す。 / 理想=`22_装備スロット.png`。
- **状態**: 操作/状態=スロットを選択、Enter/A候補、Esc/B、`normal / empty_slot / equipped / locked`。 到達性=`conditional`、capture=`captured`、entry=装備一覧で解放済み同行者を選択。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `equipment_candidates` | スロット/「候補を選ぶ」 | 対象スロットあり | static | `Main.gd:11172-11206,11764-11803` |
  | `equipment_list` | 戻る | なし | static | `Main.gd:11172-11206,11764-11803` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 立ち絵パネルと金枠の位置ずれ。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 立ち絵が枠内に収まり、各部位の状態/選択焦点が一意。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`22 equipment_slots`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `equipment_slots`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-23 `equipment_candidates` — 装備候補比較

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 候補差分を比較して装着する。
- **表示要素**: 固定=候補、数値差分、装着。 / 拡張=フィルタ/ソート。 / 理想=`23_装備候補.png`。押下型原則の対象。
- **状態**: 操作/状態=アイテム絵を押下、Enter/A装着、Esc/B、`normal / selected / incompatible / locked`。 到達性=`conditional`、capture=`captured`、entry=装備スロットの候補選択。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `equipment_slots` | 戻るまたは装備変更後 | なし | static | `Main.gd:11206-11247,11803-11861` |

- **実装状態**: 旧マスター=崩れあり、`r3`=4違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 立ち絵枠ずれ、アイコンの識別性不足。`[未決]` 新理想の承認待ち。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = アイテム絵が押下面、武器種を識別でき、非互換理由を示す。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`23 equipment_candidates`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `equipment_candidates`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-24 `enhance_preview` — 仲間強化プレビュー

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 強化前後と必要素材を比較して実行する。
- **表示要素**: 固定=前後比較、素材、実行、戻る。 / 拡張=段階/履歴。 / 理想=`24_強化プレビュー.png`。
- **状態**: 操作/状態=実行/戻る、`normal / insufficient_material / max_level`。 到達性=`unwired_current`、capture=`captured`、entry=旧townのcommand.enhanceだけが入口。現行B1町メニューの6アクションに含まれない。
- **遷移**:

  - `classification=unwired_current`。現行runtime入口なし（SCR-G02）。edgeを発明せず、採用決裁後の再配線か製品対象外の明記を待つ。

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`unwired_current/static`。
- **ギャップ**: `[乖離]` 戻る表示不在・下端クリップ。未コミット修正の実機検収が未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 戻る導線が画面内にあり、下端がクリップせず、実行結果が保存/UIへ反映。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。 本画面は、製品導線へ配線して再抽出edgeを得るか、製品対象外と決裁されるまで未完了。
- **根拠**: `docs/spec/10_screens.md`の`24 enhance_preview`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `enhance_preview`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-25 `loading_transition` — ロード / 地域遷移

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 次の場所/目的を短く示して遷移する。
- **表示要素**: 固定=行先、目的、進捗。 / 拡張=Tips/アクセシビリティ。 / 理想=`25_遷移カード.png`。
- **状態**: 操作/状態=原則待機、必要時のみCancel/Back、`loading / fade_in / fade_out`。 到達性=`reachable`、capture=`captured`、entry=_transition_to のカード/フェード中の一時画面。
- **遷移**:

  - `classification=automatic_transient`。遷移先は呼出元`_transition_to`が動的に保持するため抽出edgeなし（SCR-G04）。

- **実装状態**: 旧マスター=崩れあり、`r3`=1違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` `Recommended Lv`等の英語。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 遷移先と進捗が日本語で判読でき、完了後に目標画面へ一度だけ遷移。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。 全呼出元で動的な目標画面へ一度だけ到達することを実機traceで確認する。
- **根拠**: `docs/spec/10_screens.md`の`25 loading_transition`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `loading_transition`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-26 `dungeon_info` — ダンジョン情報

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 危険度/条件/報酬を理解して入場判断する。
- **表示要素**: 固定=危険度、条件、報酬、入場。 / 拡張=持込条件/推奨編成。 / 理想=`26_ダンジョン出発確認.png`。
- **状態**: 操作/状態=入場/召喚/戻る、Enter/A、Esc/Bで地域へ、`normal / entry_ready / entry_locked`。 到達性=`reachable`、capture=`captured`、entry=地域、ワールドマップ、ワールドタイルのダンジョン起動。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `dungeon_playing` | 「ダンジョンへ入る」/最終出撃確定 | ダンジョン解放済み。最終戦はルート予測の追加確認 | measured | `Main.gd:6702-6742,11483-11530` |
  | `summon_select` | 「召喚石」 | 最終出撃確認中ではない | static | `Main.gd:10430-10472,11483-11530` |
  | `region_menu` | 「戻る」/Esc/B | 所属地域あり | static | `Main.gd:11525-11538` |

- **実装状態**: 旧マスター=崩れあり、`r3`=2違反。 screen-flow=`reachable/measured`。
- **ギャップ**: `[乖離]` 英語残り。Esc復帰は未コミット・実機未検証。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = ロック理由を示し、Enter/Aが入場、Esc/Bが地域へ戻り、全文日本語。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`26 dungeon_info`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `dungeon_info`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-27 `dungeon_round_result` — ダンジョンラウンド結果

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 獲得物と次の危険を確認する。
- **表示要素**: 固定=獲得物、継続/帰還の入口。 / 拡張=詳細報酬/次ラウンド予告。 / 理想=`27_中間到達結果.png`。
- **状態**: 操作/状態=Confirm/Enter/Aで継続選択へ、Esc/Bで帰還、`normal / round_complete / reward_pending`。 到達性=`conditional`、capture=`captured`、entry=ダンジョンラウンド境界に到達。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `dungeon_round_choice` | B2「継続と帰還を選ぶ」 | B2有効（現行true） | static | `Main.gd:10474-10522` |
  | `dungeon_playing` | Enter/Aの続行 | 次ラウンドあり | static | `Main.gd:2534-2589,16701-16724` |
  | `town_menu` | Esc/Bの帰還 | 帰還可能なラウンド | static | `Main.gd:2534-2589,16726-16784` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 旧監査で焦点枠なし。未コミット修正の実機検収が未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 選択中の焦点が常時可視で、継続/帰還の意味と持越しを判読できる。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`27 dungeon_round_result`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `dungeon_round_result`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-28 `dungeon_round_choice` — 継続 / 帰還選択

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: リスクと確定持帰りを比較して選ぶ。
- **表示要素**: 固定=継続、帰還、リスク、持越し。 / 拡張=報酬内訳/警告。 / 理想=`28_継続と帰還.png`。
- **状態**: 操作/状態=上下/D-pad選択、Enter/A確定、Esc/B帰還、`normal / continue_focus / return_focus`。 到達性=`conditional`、capture=`captured`、entry=B2ラウンド結果の「継続と帰還を選ぶ」。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `dungeon_playing` | 「続行する」 | 次ラウンドあり | static | `Main.gd:10499-10522` |
  | `town_menu` | 「帰還する」 | 帰還可能なラウンド | static | `Main.gd:10499-10522` |

- **実装状態**: 旧マスター=崩れあり。未コミット `r3` は画面を撮影（0違反）。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 旧監査はround_resultと同一画像で監査不能。r3の固有状態/理想一致を人間確認する必要。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 結果画面と異なる固有画面を撮影し、2選択の焦点・効果・戻り先が明確。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`28 dungeon_round_choice`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `dungeon_round_choice`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-29 `world_field_playing` — ワールドフィールド戦闘

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 生存、時間、経験値、フィールド行動を読む。
- **表示要素**: 固定=HP/EXP/HUD、行動。 / 拡張=ミニマップ/通知。 / 理想=`29_フィールド戦闘.png`。D-05=HUD現状維持。
- **状態**: 操作/状態=WASD/矢印/D-pad移動、1–6/Tab/7スキル、Esc/B Pause、`playing / boss / low_hp / paused`。 到達性=`conditional`、capture=`captured`、entry=ワールドマップのfield node。地域/進行ロック解除が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `level_up` | XPが必要値に到達 | 戦闘中 | static | `Main.gd:18798-18807` |
  | `boss_reward` | ボス撃破 | 報酬候補あり | static | `Main.gd:19029-19076` |
  | `pause` | P/Start/戻る | 戦闘中 | static | `Main.gd:2492-2607` |
  | `clear` | ステージ完走 | run完了 | measured | `Main.gd:19431-19457` |
  | `game_over` | HP 0 | 死亡 | measured | `Main.gd:19459-19488` |
  | `alert_overlay` | 警告/チュートリアル/宝箱など | ブロッキング結果画面中でない | static | `Main.gd:17446-17483,18784-18800,22870-22896` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` HP桁切れ、HUD/スキル文字重なり。D-05はレイアウト維持であり不具合容認ではない。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = HP最大値を省略せず読め、HUDとスキルが重ならず、Esc/Bでpause。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`29 world_field_playing`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `world_field_playing`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-30 `dungeon_playing` — ダンジョン戦闘

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 深度・ボス進行・生存を読む。
- **表示要素**: 固定=HP/EXP、ボスHP、ラウンド。 / 拡張=ミニマップ/警告。 / 理想=`30_ダンジョン戦闘.png`。
- **状態**: 操作/状態=29と同一入力、Esc/B Pause、`playing / boss / low_hp / paused`。 到達性=`conditional`、capture=`captured`、entry=dungeon_infoの「ダンジョンへ入る」。ダンジョン解放が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `level_up` | XPが必要値に到達 | 戦闘中 | static | `Main.gd:18798-18807` |
  | `boss_reward` | ボス撃破 | 報酬候補あり | static | `Main.gd:19029-19076` |
  | `dungeon_round_result` | ラウンド境界 | ダンジョンのラウンド完了 | static | `Main.gd:16105-16132,16553-16601` |
  | `pause` | P/Start/戻る | 戦闘中 | static | `Main.gd:2492-2607` |
  | `clear` | ダンジョン最終クリア | run完了 | measured | `Main.gd:19431-19457` |
  | `game_over` | HP 0 | 死亡 | measured | `Main.gd:19459-19488` |
  | `alert_overlay` | 警告/ハザード/チュートリアルなど | ブロッキング結果画面中でない | static | `Main.gd:17604-17674,22870-22896` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/measured`。
- **ギャップ**: `[乖離]` HP桁切れ、HUD文字重なり。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = HP全桁、ボス/ラウンド、スキルが互いを隠さず、Pauseへ戻る。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`30 dungeon_playing`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `dungeon_playing`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-31 `alert_overlay` — 通知オーバーレイ

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 購入/警告/結果をプレイを妨げず示す。
- **表示要素**: 固定=種別、本文、表示時間。 / 拡張=アクション/履歴。 / 理想=`31_短時間通知.png`。
- **状態**: 操作/状態=自動消去、`info / warning / error / timed_out`。 到達性=`conditional`、capture=`captured`、entry=購入、チュートリアル、警告等の _show_alert。下位画面を保存。
- **遷移**:

  - `classification=overlay_return`。保存した下位画面へ閉じて戻るoverlayであり、固定to edgeなし（SCR-G04）。

- **実装状態**: 旧マスター=崩れあり、`r3`=1違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` `Purchased`英語と透過重なり。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 下層の文字と重ならず、種別を色以外でも区別し、日本語表示。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。 各alert呼出元で下位画面・focus・状態を保持して一度だけ復帰することを実機traceで確認する。
- **根拠**: `docs/spec/10_screens.md`の`31 alert_overlay`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `alert_overlay`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-32 `pause` — ポーズ

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 再開・設定・離脱を安全に選ぶ。
- **表示要素**: 固定=Resume、目的、設定、セーブロード、再挑戦、タイトル。 / 拡張=ヘルプ/アクセシビリティ。 / 理想=`32_ポーズ.png`。
- **状態**: 操作/状態=クリック/Enter/A、Esc/B再開、`normal / confirm_title`。 到達性=`reachable`、capture=`captured`、entry=戦闘中にP/Start/戻る。boundary_shopも同IDを再利用。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `world_field_playing` | 「再開」 | フィールドrun | static | `Main.gd:7863-7889,10523-10542` |
  | `dungeon_playing` | 「再開」 | ダンジョンrun | static | `Main.gd:7863-7889,10523-10542` |
  | `objective_log` | 「目的ログ」 | なし | static | `Main.gd:7863-7881,10523-10542` |
  | `options` | 「オプション」 | なし | static | `Main.gd:7863-7881,10523-10542` |
  | `save_load_menu` | 「セーブ/ロード」 | なし | static | `Main.gd:10523-10542` |
  | `world_field_playing` | 「リトライ」 | フィールドrun | static | `Main.gd:10523-10542` |
  | `dungeon_playing` | 「リトライ」 | ダンジョンrun | static | `Main.gd:10523-10542` |
  | `title` | 「タイトルへ」 | なし | static | `Main.gd:10523-10542` |

- **実装状態**: 旧マスター=崩れあり、`r3`=1違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` メニュー英語混在。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = Esc/Bが再開、全項目が日本語で機能し、タイトル離脱は確認を経る。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`32 pause`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `pause`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-33 `level_up` — レベルアップ選択

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 強化候補を比較して強制選択する。
- **表示要素**: 固定=候補、効果、焦点、選択。 / 拡張=再抽選/詳細。 / 理想=`33_レベルアップ.png`。祭りB案（ドット祝祭、2026-07-11）を採用。
- **状態**: 操作/状態=候補をクリック/1–4/パッド、Esc/B取消不可、`normal / choice_focus / reroll_available`。 到達性=`conditional`、capture=`captured`、entry=戦闘中、XPが閾値以上。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `awaken_cutin` | 覚醒対象の強化を選ぶ | 選択強化のshould_show_awaken_cutin | static | `Main.gd:19165-19205` |
  | `world_field_playing` | 通常強化を選ぶ | フィールドrun | static | `Main.gd:19165-19215` |
  | `dungeon_playing` | 通常強化を選ぶ | ダンジョンrun | static | `Main.gd:19165-19215` |

- **実装状態**: `LevelUpFestivalView`専用実装、旧監査問題なし、`r3`=3違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` カード上のゴースト素材、理想一致未判定。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 強制選択で焦点が常時可視、候補が比較でき、選択後に戦闘へ一度だけ戻る。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`33 level_up`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `level_up`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-34 `boss_reward` — ボス報酬

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: ボス報酬を比較して強制選択する。
- **表示要素**: 固定=候補、効果、焦点、決定。 / 拡張=詳細/履歴。 / 理想=`34_ボス報酬.png`。
- **状態**: 操作/状態=33と同じ、`normal / choice_focus / rare_reward`。 到達性=`conditional`、capture=`captured`、entry=ボス撃破の報酬トリガー。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `world_field_playing` | 報酬を選ぶ | フィールドrun | static | `Main.gd:19300-19324` |
  | `dungeon_playing` | 報酬を選ぶ | ダンジョンrun | static | `Main.gd:19300-19324` |

- **実装状態**: FestivalView共有、旧監査問題なし、`r3`=5違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` 異なる報酬の同一アイコン、見出し/理想一致未達。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 効果の異なる候補が異なる絵/文言で識別でき、焦点が可視、確定後に正しい次状態へ。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`34 boss_reward`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `boss_reward`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-35 `clear` — クリア結果

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 達成、獲得、解放と次の行き先を示す。
- **表示要素**: 固定=成果、報酬、次導線。 / 拡張=共有/詳細統計。 / 理想=`35_クリア結果.png`。
- **状態**: 操作/状態=町/再挑戦/報酬シーン/ギャラリー/タイトル、`normal / new_unlock / reward_scene_available`。 到達性=`conditional`、capture=`captured`、entry=ステージ/ダンジョンの完走。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `town_menu` | 「町へ」 | run結果の帰還先町あり | measured | `Main.gd:10689-10760,14932-14947` |
  | `world_field_playing` | 「リトライ」 | フィールドrun | static | `Main.gd:10689-10760` |
  | `dungeon_playing` | 「リトライ」 | ダンジョンrun | static | `Main.gd:10689-10760` |
  | `gallery` | 「ギャラリー」 | なし | static | `Main.gd:10689-10760` |
  | `scene_view` | 「報酬シーン」 | 報酬sceneあり | static | `Main.gd:15202-15208,10689-10760` |
  | `title` | 「タイトル」 | なし | static | `Main.gd:10689-10760` |

- **実装状態**: 実装済み、旧監査問題なし、`r3`=0違反。 screen-flow=`conditional/measured`。
- **ギャップ**: `[乖離]` 理想一致の人間判定未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = すべての報酬/解放が保存され、各導線が正しい行き先へ遷移。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`35 clear`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `clear`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-36 `game_over` — ゲームオーバー結果

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 戦績を示し再挑戦/町/タイトルを選ぶ。
- **表示要素**: 固定=戦績、3導線。 / 拡張=攻略ヒント/詳細統計。 / 理想=`36_敗北結果.png`。
- **状態**: 操作/状態=町/再挑戦/タイトル、`normal / first_run_failure / retry_available`。 到達性=`conditional`、capture=`captured`、entry=プレイヤーHPが0。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `town_menu` | 「町へ」/Enter/A | run結果の帰還先町あり | measured | `Main.gd:10689-10760,14932-14947` |
  | `world_field_playing` | 「リトライ」 | フィールドrun | static | `Main.gd:10689-10760` |
  | `dungeon_playing` | 「リトライ」 | ダンジョンrun | static | `Main.gd:10689-10760` |
  | `gallery` | 「ギャラリー」 | なし | static | `Main.gd:10689-10760` |
  | `title` | 「タイトル」 | なし | static | `Main.gd:10689-10760` |

- **実装状態**: 実装済み、旧監査問題なし、`r3`=0違反。 screen-flow=`conditional/measured`。
- **ギャップ**: `[乖離]` 理想一致の人間判定未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 3導線が機能し、未確定報酬の損失規則が表示と保存で一致。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`36 game_over`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `game_over`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-37 `gallery` — ギャラリー

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 解放済み/未解放の回想を一覧し閲覧する。
- **表示要素**: 固定=回想一覧、ロック、閲覧。 / 拡張=カテゴリ/検索。 / 理想=`37_ギャラリー.png`。
- **状態**: 操作/状態=カード押下、方向キー/D-pad、Enter/A、Esc/B、`normal / locked / selected / empty`。 到達性=`reachable`、capture=`captured`、entry=クリア/敗北結果の「ギャラリー」。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `scene_view` | 解放済みsceneカードを選択 | storeで利用可能かつ解放済みscene | static | `Main.gd:11862-11943,14299` |
  | `adult_viewer_gate` | 成人向け回想入口 | DLsiteかつadult content有効 | static | `Main.gd:11862-11943` |
  | `clear` | 戻る | clear起点 | static | `Main.gd:12270-12291` |
  | `game_over` | 戻る | game_over起点 | static | `Main.gd:12270-12291` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` サムネ使い回し/シーン不対応。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 各サムネが対応シーンと一致し、未解放は内容を漏らさず、戻り先が保持。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`37 gallery`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `gallery`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-38 `scene_view` — 会話イベント

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 本文、話者、選択肢を読み進める。
- **表示要素**: 固定=本文、話者、肖像、操作列。 / 拡張=速度/ログショートカット。 / 理想=`38_シーン本文.png`。D-04=バストアップ表示領域を新立ち絵で作り直す。D-09=36字/秒、auto 2.5秒。
- **状態**: 操作/状態=クリック/Enter/A送り、LOG/AUTO/HIDE、Esc/B終了、`normal / auto / hidden / choice_pending`。 到達性=`reachable`、capture=`captured`、entry=新規プロローグ、ギャラリー、ルート会話、報酬/最終イベント。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `scene_log` | LOG/L/LB | ADV中 | static | `Main.gd:12843-12869,2499-2580` |
  | `scene_choice` | choicesを持つADV行まで進行 | 未選択のchoicesあり | static | `Main.gd:12607-12720` |
  | `town_menu` | シーン完了/スキップ | town起点または新規プロローグ完了 | measured | `Main.gd:6773-6787,7232-7257,13585-13608` |
  | `gallery` | シーン完了/スキップ | gallery起点 | static | `Main.gd:6773-6787,13585-13608` |
  | `clear` | 報酬シーン完了 | clear起点 | static | `Main.gd:13585-13608` |
  | `adult_viewer_gate` | 成人向けscene完了 | adult_viewer起点 | static | `Main.gd:13585-13608` |
  | `credits_license` | 最終/個別EDシーン完了 | final/route epilogue return target | measured | `Main.gd:6789-6855` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`reachable/measured`。
- **ギャップ**: `[乖離]` 未スキン英語ボタン、本文下地なし、旧portrait。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 指定速度/autoで進み、操作は日本語スキン、本文に読める下地、肖像は承認済み立ち絵。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`38 scene_view`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `scene_view`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-39 `scene_log` — 会話ログ

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 既読本文を時系列で読む。
- **表示要素**: 固定=発話履歴、スクロール、戻る。 / 拡張=検索/話者フィルタ。 / 理想=`39_バックログ.png`。
- **状態**: 操作/状態=スクロール、Esc/B、`normal / empty / scrolling`。 到達性=`conditional`、capture=`captured`、entry=ADV中のLOG/Lキー/LB。scene_view のoverlay。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `scene_view` | LOG/L/Esc/B | ADV中 | static | `Main.gd:12853-12869,2499-2580` |

- **実装状態**: 旧マスター=崩れあり、`r3`=2違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` BACKのレイヤー順不整合。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = モーダル階層が正しく、戻るが常に操作可能で、本文をスクロールして読める。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`39 scene_log`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `scene_log`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-40 `scene_choice` — 会話選択肢

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 選択肢を比較して決定する。
- **表示要素**: 固定=選択肢、焦点、条件。 / 拡張=条件説明/取消。 / 理想=`40_ADV選択肢.png`。選択肢も焦点を明確にする。
- **状態**: 操作/状態=クリック/方向キー/D-pad/Enter/A、Esc/Bはシーン規則、`normal / choice_focus / locked_choice`。 到達性=`conditional`、capture=`captured`、entry=ADV行に未選択のchoicesがある時のoverlay。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `scene_choice_result` | 選択肢を決定 | choice index有効 | static | `Main.gd:12704-12720,13381-13407` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` ボタン/立ち絵重なり、背景未透過、本文下地なし。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 立ち絵・本文・選択肢が重ならず、選択中とロック理由が明瞭。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`40 scene_choice`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `scene_choice`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-41 `scene_choice_result` — 会話選択結果

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 選択への反応と変化を読む。
- **表示要素**: 固定=選択結果、反応、続行。 / 拡張=詳細変化/ログ追加。 / 理想=`41_ADV選択結果.png`。
- **状態**: 操作/状態=Confirmで本文へ、`normal / result_revealed`。 到達性=`conditional`、capture=`captured`、entry=会話選択を確定後のoverlay。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `scene_view` | 次の台詞へ進む | 次行が選択肢でない | static | `Main.gd:12704-12720,13381-13407` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` バナーと立ち絵の重なり/背景未透過。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 結果バナー・立ち絵・本文が重ならず、続行で元シーンへ正しく戻る。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`41 scene_choice_result`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `scene_choice_result`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-42 `motion_check` — モーション確認

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 開発用に再生/停止/パラメータを検査する。
- **表示要素**: 固定=再生、停止、シーク、パラメータ。 / 拡張=速度/比較。 / 理想=`42_モーション確認.png`。
- **状態**: 操作/状態=dev時のみ再生切替/シーク、Esc/B、`normal / playing / paused / dev_only`。 到達性=`developer_only`、capture=`captured`、entry=system_menu。F8/--dev系が必要。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `system_menu` | 戻る/Esc/B | 開発モード | static | `Main.gd:7500-7526` |

- **実装状態**: 旧マスター=崩れあり、`r3`=17違反。 screen-flow=`developer_only/static`。
- **ギャップ**: `[乖離]` 開発英語、アーティファクト、ゲージ重なり。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 製品導線から隔離され、devでは各検査操作が働く。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`42 motion_check`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `motion_check`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-43 `adult_viewer_gate` — 成人向け回想ゲート

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 回想の年齢条件を確認して同意/戻るを選ぶ。
- **表示要素**: 固定=条件、同意、戻る。 / 拡張=規約/地域注意。 / 理想=`43_成人向け閲覧確認.png`。
- **状態**: 操作/状態=同意/戻る、`normal / store_guard / adult_enabled`。 到達性=`conditional`、capture=`captured`、entry=galleryの成人向け入口。DLsiteかつadult content有効時のみ。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `scene_view` | 成人向けsceneを再生 | DLsite adult profileかつsceneあり | unconfirmed | `Main.gd:11944-12024` |
  | `gallery` | 戻る | gallery起点 | static | `Main.gd:12025-12030` |

- **実装状態**: 旧マスター=崩れあり、`r3`=3違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` `(仮)`ラベル、英字。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 同意時のみ成人回想へ、戻るとギャラリーへ、仮ラベルなし。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`43 adult_viewer_gate`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `adult_viewer_gate`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-44 `run_history` — ラン履歴

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 過去ランを比較・詳細確認する。
- **表示要素**: 固定=履歴、詳細、戻る。 / 拡張=検索/エクスポート。 / 理想=`44_プレイ履歴.png`。
- **状態**: 操作/状態=行選択/詳細/戻る、`normal / empty / selected_row`。 到達性=`unwired_current`、capture=`captured`、entry=表示関数のみ。現行B1タイトル/B2結果/system_menuに入口なし。
- **遷移**:

  - `classification=unwired_current`。現行runtime入口なし（SCR-G02）。edgeを発明せず、採用決裁後の再配線か製品対象外の明記を待つ。

- **実装状態**: 旧マスター=崩れあり、`r3`=11違反。 screen-flow=`unwired_current/static`。
- **ギャップ**: `[未決]` 製品内導線を採用するか。`[乖離]` 英語混在。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 製品内導線が定義され、空/履歴ありを表示し、英語のままの情報がない。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。 本画面は、製品導線へ配線して再抽出edgeを得るか、製品対象外と決裁されるまで未完了。
- **根拠**: `docs/spec/10_screens.md`の`44 run_history`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `run_history`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-45 `options` — オプション

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 音量、表示、言語/文字、入力を変更する。
- **表示要素**: 固定=音量、言語/文字、入力、戻る。 / 拡張=プリセット/リセット。 / 理想=`45_設定.png`。D-07=当面BGM1曲、D-08=SE現状維持。
- **状態**: 操作/状態=項目選択、左右/D-pad、Esc/B、`normal / changed / defaulted`。 到達性=`reachable`、capture=`captured`、entry=ポーズ画面の「設定」。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `pause` | B2「戻る」 | pause起点 | static | `Main.gd:10543-10568,12453-12459` |
  | `title` | B2「戻る」 | title起点 | static | `Main.gd:10543-10568,12453-12459` |

- **実装状態**: 旧マスター=崩れあり、`r3`=7違反。 screen-flow=`reachable/static`。
- **ギャップ**: `[乖離]` 英語、スライダー/スクロールバー重なり。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 値変更が即時反映/保存され、スライダーが重ならず全項目が日本語。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`45 options`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `options`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-46 `options_language_text` — 言語・テキスト速度

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 可読性設定を変更する。
- **表示要素**: 固定=言語、文字サイズ、プレビュー。 / 拡張=フォント/行間。 / 理想=`46_言語と文字設定.png`。D-01/D-02を反映。
- **状態**: 操作/状態=左右/選択/戻る、`normal / preview / fallback_missing`。 到達性=`unwired_current`、capture=`captured`、entry=旧optionsだけの入口。B2 options が早期returnし、現行UIに遷移ボタンなし。
- **遷移**:

  - `classification=unwired_current`。現行runtime入口なし（SCR-G02）。edgeを発明せず、採用決裁後の再配線か製品対象外の明記を待つ。

- **実装状態**: 旧マスター=崩れあり、`r3`=6違反。 screen-flow=`unwired_current/static`。
- **ギャップ**: `[乖離]` 開発スタブ、ローカライズキー、下端クリップ。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 選択値が保存され、プレビューが一致し、生キー/スタブ/クリップが0件。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。 本画面は、製品導線へ配線して再抽出edgeを得るか、製品対象外と決裁されるまで未完了。
- **根拠**: `docs/spec/10_screens.md`の`46 options_language_text`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `options_language_text`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-47 `input_config` — 入力設定

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: キー/パッド割当を比較・変更する。
- **表示要素**: 固定=行動、キー、パッド、重複警告、初期化。 / 拡張=プリセット/検索。 / 理想=`47_操作設定.png`。
- **状態**: 操作/状態=項目選択、Enter/Aで捕捉、Esc/B取消/戻る、`normal / capturing / conflict / unassigned`。 到達性=`unwired_current`、capture=`captured`、entry=旧optionsだけの入口。B2 options が早期returnし、現行UIに遷移ボタンなし。
- **遷移**:

  - `classification=unwired_current`。現行runtime入口なし（SCR-G02）。edgeを発明せず、採用決裁後の再配線か製品対象外の明記を待つ。

- **実装状態**: 旧マスター=崩れあり、`r3`=50違反（最大）。 screen-flow=`unwired_current/static`。
- **ギャップ**: `[乖離]` 英語残り、下端クリップ。最優先のUI修正対象。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 再割当、重複検知、取消、初期化が動き、下端/文字が切れない。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。 本画面は、製品導線へ配線して再抽出edgeを得るか、製品対象外と決裁されるまで未完了。
- **根拠**: `docs/spec/10_screens.md`の`47 input_config`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `input_config`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-48 `system_menu` — システムメニュー

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 開発用に設定/保存/クレジット/QA入口をまとめる。
- **表示要素**: 固定=Options/SaveLoad/Credits/Back。 / 拡張=サポート/法務。 / 理想=`48_システムハブ.png`。
- **状態**: 操作/状態=dev時のみ選択/戻る、`normal / dev_options_visible`。 到達性=`developer_only`、capture=`captured`、entry=F8（debug/--dev）で開く。製品ビルドの通常導線にはない。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `options` | 「設定」 | 開発モード | static | `Main.gd:7457-7472` |
  | `save_load_menu` | 「セーブ/ロード」 | 開発モード | static | `Main.gd:7457-7472` |
  | `credits_license` | 「クレジット / ライセンス」 | 開発モード | static | `Main.gd:7457-7472` |
  | `stage_select` | 「ステージ選択」 | 開発モード | static | `Main.gd:7457-7472` |
  | `motion_check` | 「モーション確認」 | 開発モード | static | `Main.gd:7457-7472` |
  | `unlock_confirm` | 「全解放」 | 開発モード | static | `Main.gd:7457-7472` |
  | `reset_confirm` | 「セーブを初期化」 | 開発モード | static | `Main.gd:7457-7472` |
  | `title` | 戻る/Esc/B | 開発モード | static | `Main.gd:7457-7472` |

- **実装状態**: `STATE_SYSTEM`実装。旧マスターでは監査枠外、未コミット `r3`=0違反。 screen-flow=`developer_only/static`。
- **ギャップ**: `[乖離]` dev隔離と理想一致の実機検収未了。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 製品導線では到達不能、devでは子画面へ戻り先を保って遷移。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`48 system_menu`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `system_menu`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。

## SCR-49 `awaken_cutin` — 覚醒カットイン

- `spec_status`: `draft-wave2`
- `approved_at`: `null`
- **目的**: 武器進化の意味と強さを短く伝える。
- **表示要素**: 固定=能力名、解放内容、カットイン。 / 拡張=スキップ/演出軽減。 / 理想=`49_覚醒カットイン.png`。
- **状態**: 操作/状態=自動再生/終了シグナルで復帰、`playing / cut_in / auto_close`。 到達性=`conditional`、capture=`captured`、entry=選択した強化が覚醒演出対象の場合。
- **遷移**:

  | to | trigger | condition | confidence | source |
  |---|---|---|---|---|
  | `world_field_playing` | 演出完了/スキップ | フィールドrun | static | `Main.gd:19240-19298` |
  | `dungeon_playing` | 演出完了/スキップ | ダンジョンrun | static | `Main.gd:19240-19298` |

- **実装状態**: 旧マスター=崩れあり、`r3`=0違反。 screen-flow=`conditional/static`。
- **ギャップ**: `[乖離]` `SKIP`開発表記、帯の明度反転、画像ぼけ。 構成・情報密度・導線の最終決裁は未承認。
- **完成定義**: Yes = 終了後に元戦闘へ一度だけ戻り、開発表記/明度反転/ぼけがなく理想に一致。 加えて、本節の全outgoing edgeが実機で一度だけ発火し、戻り先・条件・入力focusがsourceと一致する。
- **根拠**: `docs/spec/10_screens.md`の`49 awaken_cutin`行; `/home/hikaru/projects/vampire-survivors-like/outputs/screen_flow_extract_0818/screen_flow.json` node `awaken_cutin`; edge sourceは上表; flow scope revision `ca4768d9f961cb0fb29634a04dacf4eff5e040b2+uncommitted-Main.gd`; artifact SHA-256 `d51cac692110584830c52dba32120e11c235046137d1f20d9ab748f58956cf8a`。現game HEAD `008746240edaef2c39f876832be31d6d9003d2b4`との一致は未検証（SCR-G01）。
