# Cline Workflows Usage

このディレクトリは、`.clinerules/workflows/` に配置したCline Workflowの使用方法をまとめる。

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
