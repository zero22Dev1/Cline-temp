# Source To Verified XLSM Workflow

既存ソースを正本としてHTMLモックとマクロ付きExcelを生成し、処理内容の欠落・矛盾がないことを独立検証する。

このファイルはCline Custom Workflowとして`/source-to-verified-xlsm.md`で実行する。詳細処理は`.cline/skills/`のSkillを必要な段階で読み込む。

## Workflow Rules

- 中間成果物同士の一致だけで合格にしない。
- 各段階で同じ`REQ-ID`、`section id`、出典を維持する。
- HTMLレイアウトテンプレートは見た目の基準、既存ソースは処理内容の正本とする。
- Unknownを推測で補完しない。
- CriticalまたはMajorの欠落・矛盾が残る場合は完了しない。
- 修正ループはSkill `loop-budget`で制限する。
- 各ループは`Execute -> Observe -> Evaluate -> Diagnose -> Improve -> Stop/Repeat`で実行する。
- 同じ失敗を繰り返さず、2回目にはハーネス改善を必須とする。

## Step 1: Context And Contract

`/context-window-management.md`でGoal、Scope、正本、変更禁止範囲、完了条件、検証方法を確定する。対象機能、既存ソース、HTMLテンプレート、Excelテンプレート、出力先を特定する。

Skill `harness-engineering-loop`とSkill `loop-budget`を読み込み、開始前に次を定義する。

- `Intent`: 既存ソースと一致するHTML・XLSM、対象外、完了条件
- `Context`: ソース索引、仕様、Unknown、テンプレート、REQ-ID
- `Tools`: 検索、build、test、ブラウザ、HTML検査、XLSM生成・検査
- `Observability`: diff、ログ、スクリーンショット、Traceability Matrix、VBAハッシュ
- `Constraints`: 原本不変、推測禁止、テンプレート準拠、最大3回
- `Evaluators`: HTML checker、traceability checker、quality gate、loop verifier
- `Control`: 各段階の停止条件、Blocking Unknown、人間確認点
- `Learning`: 欠落原因をRule、Skill、テスト、マッピングへ還元

## Step 2: Source Specification

Skill `legacy-source-spec-writer`で既存ソースから仕様を作成する。処理、データ、分岐、検証、エラー、権限、UI、外部連携へ`REQ-ID`を付与する。

Skill `unknown-list-extractor`で断定できない内容を分類する。Blocking Unknownがある場合は生成へ進まない。

## Step 3: HTML Mock Generation

HTMLレイアウトテンプレートを読み、既存の構造、CSS、寸法、セクション規則を維持する。Skill `implementation-loop`で仕様からHTMLモックを生成する。

各画面・処理説明を`<section id="一意なID" data-requirement-ids="REQ-..." data-source-evidence="file:symbol">`へ分け、対応するREQ-IDとソース出典を保持する。

```txt
templates/html/<layout-template>
  -> outputs/html/<feature>-mock.html
```

## Step 4: HTML Verification Gate

Skill `html-artifact-checker`で次を確認する。

- 既存ソースと`docs/specs/`の処理・項目を網羅
- 正常、異常、分岐、権限、表示条件を反映
- HTMLテンプレートのレイアウトへ適合
- section id、REQ-ID、出典が追跡可能
- ブラウザ表示に欠落、重なり、切れがない

不合格の場合はExcel生成へ進まない。

## Step 5: Section Classification And Capture

各HTMLセクションを`text / image / image-and-text`へ分類する。画像対象だけをブラウザでselector単位にキャプチャし、manifestへ`REQ-ID / selector / render_mode / image / source evidence`を記録する。

selectorの一意一致、非空画像、期待画面状態、viewport、キャプチャ時刻を観測記録へ残す。実HTMLのキャプチャが未実行の場合はXLSM生成へ進まない。

## Step 6: XLSM Generation

Skill `source-to-xlsm-template`で`.xlsm`テンプレートを毎回コピーし、HTMLセクション、説明、HTMLレンダリング画像、出典を出力する。

- 元テンプレートを上書きしない
- 既存出力は明示時だけ置換
- 一時ファイルで生成・検証後に置換
- VBA、数式、書式、名前定義を保持

実際のHTML、manifest、mapping、`.xlsm`テンプレートを使って生成する。synthetic fixtureだけを最終成果物の合格根拠にしない。

## Step 7: Independent Source-To-XLSM Verification

Skill `source-artifact-traceability-checker`を使用する。生成工程の説明を判定根拠にせず、既存ソースから独立に確認項目を再構成する。

```txt
Source Evidence
  -> Specification REQ-ID
  -> HTML section
  -> Capture manifest
  -> XLSM sheet / row / cell / image
```

全件Traceability Matrixと直接ソース照合サンプルを作り、欠落、矛盾、Unknownを判定する。

## Step 8: Quality And Repair Loop

`/artifact-quality-gate.md`とSkill `loop-verifier`で最終判定する。不合格の場合は`/harness-engineering-loop.md`を最大3回で実行する。

修正対象を`Source Extraction / Specification / HTML Coverage / Capture / XLSM Mapping / Evaluator`へ分類する。修正後は影響段階以降を再生成し、Step 7から再検証する。

同じ欠落が再発した場合は抽出規則、追跡ID、テスト、検査器を改善する。

各イテレーションを次の形式で記録する。

```md
| Iteration | Stage | Target REQ-ID | Change | Evidence | Result | Gap | Harness Improvement | Next |
|---:|---|---|---|---|---|---|---|---|
```

次の条件を満たす場合だけ再実行する。

- 未達REQ-IDが明確
- 前回と異なる修正またはハーネス改善がある
- 新しい観測結果を取得できる
- loop budget内

根拠のない再生成、同一操作の反復、評価基準の緩和は禁止する。

## Step 9: Complete And Learn

完了には次をすべて必要とする。

- 必須REQ-IDが全段階で`OK`
- Critical / Majorの欠落・矛盾なし
- HTML品質ゲートPASS
- XLSM構造、画像、VBA検証PASS
- 実テンプレートで数式、名前定義、書式、結合セルなど対象契約の保持を確認
- 直接ソース照合PASS
- Skill `loop-verifier`が`APPROVE`

完了後はSkill `memory-bank-updater`を実行する。再利用可能な欠落パターン、抽出規則、検査改善は`/continuous-project-learning.md`へ渡す。

## Final Output

- ソース由来仕様とUnknown一覧
- HTMLモックとHTMLレビュー
- セクションmanifestとHTML画面キャプチャ
- 生成`.xlsm`
- Source-to-XLSM Traceability Matrix
- 欠落、矛盾、未検証事項
- 使用した修正回数と改善した検査方法
- 最終品質判定
