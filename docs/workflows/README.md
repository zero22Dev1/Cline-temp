# Cline Workflows Usage

このディレクトリは、`.clinerules/workflows/` に配置したCline Workflowの使用方法をまとめる。

すべてのWorkflowで`Teams通知: 有効 / 無効`を実行ごとに選択できる。未指定時は`無効`とし、補助Workflowを含む処理途中では通知せず、対象の完了条件と品質ゲートを満たした時だけ通知する。

## 対応関係

```txt
.clinerules/workflows/
├── adaptive-deep-planning.md
├── artifact-quality-gate.md
├── continuous-project-learning.md
├── harness-engineering-loop.md
├── context-window-management.md
├── pdf-context-conversion.md
├── teams-completion-notification.md
├── source-to-xlsm-template.md
└── source-to-verified-xlsm.md

docs/workflows/
├── README.md
├── adaptive-deep-planning/
│   └── USAGE.md
├── artifact-quality-gate/
│   └── USAGE.md
├── continuous-project-learning/
│   └── USAGE.md
├── harness-engineering-loop/
│   └── USAGE.md
├── context-window-management/
│   └── USAGE.md
├── pdf-context-conversion/
│   └── USAGE.md
├── teams-completion-notification/
│   └── USAGE.md
├── source-to-xlsm-template/
│   └── USAGE.md
└── source-to-verified-xlsm/
    └── USAGE.md
```

## Workflow一覧

| Workflow | 用途 | 使用方法 |
|---|---|---|
| `/adaptive-deep-planning.md` | 依頼を分類し、必要な要件整理・調査・計画・レビュー工程を選ぶ | [adaptive-deep-planning/USAGE.md](adaptive-deep-planning/USAGE.md) |
| `/artifact-quality-gate.md` | 生成物を分類し、品質チェック・修正ループ・完了判定を行う | [artifact-quality-gate/USAGE.md](artifact-quality-gate/USAGE.md) |
| `/continuous-project-learning.md` | 検証済みの学習をmemory・ADR・Rule・Skill・回帰防止策へ昇格する | [continuous-project-learning/USAGE.md](continuous-project-learning/USAGE.md) |
| `/harness-engineering-loop.md` | 成果物を予算内で反復し、失敗をハーネス改善へ還元する | [harness-engineering-loop/USAGE.md](harness-engineering-loop/USAGE.md) |
| `/context-window-management.md` | 必要な文脈を選別・段階読込し、Checkpointと再構成で品質を維持する | [context-window-management/USAGE.md](context-window-management/USAGE.md) |
| `/pdf-context-conversion.md` | PDFを索引付き分割Markdownへ変換し、必要範囲だけ読み込む | [pdf-context-conversion/USAGE.md](pdf-context-conversion/USAGE.md) |
| `/teams-completion-notification.md` | 計画または実装の品質確認完了後にTeamsへ通知する | [teams-completion-notification/USAGE.md](teams-completion-notification/USAGE.md) |
| `/source-to-xlsm-template.md` | HTML／Markdownのセクションを`.xlsm`テンプレートのコピーへ出力する | [source-to-xlsm-template/USAGE.md](source-to-xlsm-template/USAGE.md) |
| `/source-to-verified-xlsm.md` | 既存ソースからHTML・XLSMを生成し、全段階の欠落・矛盾を独立照合する | [source-to-verified-xlsm/USAGE.md](source-to-verified-xlsm/USAGE.md) |

## 使用場面と選び方

| Workflow | 使用する場面 | 使用しない場面 | 主な完了条件 | Teams通知モード |
|---|---|---|---|---|
| `/adaptive-deep-planning.md` | 新機能、改修、調査を始める前に、要件・影響範囲・実装計画を整理したい | 実装内容と手順が既に確定し、単純な変更だけを行う | Blocking Questionなし、Plan Reviewが`Ready`系、計画品質が`PASS` | `plan` |
| `/artifact-quality-gate.md` | Markdown、HTML、Excel、コード、テストなどが完成条件を満たすか判定したい | まだ要件整理や実装を開始していない | 必須要件を網羅し、Critical／Majorなし、Quality Gateが`PASS` | 成果物に応じて`plan / implementation / workflow` |
| `/continuous-project-learning.md` | 完了作業や失敗から、再利用可能なRule、Skill、ADR、回帰テストを残したい | 一度だけの小さな作業で再利用可能な学習がない | 根拠付き学習だけを昇格し、Learning Quality Gateが`PASS` | 単独実行時は`workflow` |
| `/harness-engineering-loop.md` | 1回で完成しない成果物を、最大回数・観測・停止条件付きで反復したい | 単純な1回の修正で完了できる | 予算内、品質ゲート`PASS`、`loop-verifier: APPROVE` | `workflow` |
| `/context-window-management.md` | 長時間作業、複数Skill、大量資料、引き継ぎで文脈混線を防ぎたい | 小規模で短時間に終わる作業 | 最新指示と根拠が一致し、Checkpointから再開可能 | 単独実行時は`workflow` |
| `/pdf-context-conversion.md` | 大きなPDFを索引と分割Markdownへ変換し、必要ページだけ読みたい | 原本のレイアウトを完全再現する必要がある、OCR不能な画像PDFだけを扱う | 全ページ追跡可能、抽出状態明示、品質`PASS`、独立検証`APPROVE` | `workflow` |
| `/source-to-xlsm-template.md` | 準備済みHTML／Markdownを既存`.xlsm`テンプレートへ出力したい | 既存ソース調査からHTML生成・完全性確認まで一括実行したい | 原本不変、VBA保持、内容・画像・書式検証`PASS` | `workflow` |
| `/source-to-verified-xlsm.md` | 既存ソースから仕様、HTMLモック、XLSMを作り、欠落を逆照合したい | HTMLとmanifestが完成済みでExcel出力だけ行いたい | 全REQ-ID追跡、HTML／XLSM品質`PASS`、直接ソース照合`PASS` | `workflow` |
| `/teams-completion-notification.md` | 他Workflowの完了をTeamsへ通知したい | 作業途中、品質未確認、通知を希望しない | モード固有ゲート`PASS`、`loop-verifier: APPROVE`、HTTP 2xx | 呼び出し元に合わせる |

## 目的別クイック選択

| やりたいこと | 選ぶWorkflow |
|---|---|
| まず何を調査・計画すべきか決めたい | `/adaptive-deep-planning.md` |
| 作成済み成果物だけをレビューしたい | `/artifact-quality-gate.md` |
| 複数回修正しながら完成させたい | `/harness-engineering-loop.md` |
| 長い作業のコンテキストを整理したい | `/context-window-management.md` |
| PDFをClineが部分読込できる形式へ変換したい | `/pdf-context-conversion.md` |
| HTMLをマクロ付きExcelへ入れたい | `/source-to-xlsm-template.md` |
| 既存ソースからHTML・Excel・完全性確認まで行いたい | `/source-to-verified-xlsm.md` |
| 完了内容を次回以降の品質改善へつなげたい | `/continuous-project-learning.md` |
| 完了後にTeamsへ通知したい | 対象Workflowで`Teams通知: 有効`を指定 |

## 呼び出し例

### 新機能を計画して実装する

```txt
/adaptive-deep-planning.md

Teams通知: 有効
既存コードを調査し、実装計画を作成してください。
計画承認後に実装、テスト、レビュー、品質ゲートまで進めてください。
```

### PDFをコンテキスト用Markdownへ変換する

```txt
/pdf-context-conversion.md

Teams通知: 無効
manual.pdfを索引付きの分割Markdownへ変換し、OCRが必要なページを報告してください。
```

### 既存ソースから検証済みXLSMを作る

```txt
/source-to-verified-xlsm.md

Teams通知: 有効
既存ソースを正本として仕様、HTMLモック、XLSMを生成し、REQ-IDで欠落を確認してください。
```

### 成果物だけを品質確認する

```txt
/artifact-quality-gate.md

Teams通知: 無効
今回作成したHTMLとMarkdownについて、要件網羅性、正確性、追跡性を判定してください。
```

## 基本的な実行順

```txt
/adaptive-deep-planning.md
  ↓
 /context-window-management.md（長時間・複雑な場合）
  ↓
選択されたSkillで要件整理・調査・計画
  ↓
計画レビュー・承認
  ↓
実装または成果物生成
  ↓
/harness-engineering-loop.md（複数回の反復が必要な場合）
  ↓
/artifact-quality-gate.md
  ↓
memory-bank更新
  ↓
/continuous-project-learning.md（学習候補がある場合）
  ↓
Git Workflow
```

Workflowは複数Skillの実行順と分岐を管理する。個別Skillの詳しい使用方法は `docs/skills-usage.md` を参照する。
