# Adaptive Deep Planning Usage

## 概要

`/adaptive-deep-planning.md` は、依頼内容を分類して必要な計画工程だけを選ぶ入口Workflowである。

すぐに実装を始めず、要件の明確さ、変更規模、既存成果物、コード調査の必要性を確認する。

## 使用するタイミング

- 新機能や機能改修の進め方を決めたい
- 要件が曖昧で、実装前の確認が必要
- 複数ファイル、複数層、DB、API、画面に影響する
- 既存システムの移行やリプレースを計画したい
- 既存の計画書やタスク一覧が現在のコードと一致するか確認したい
- 調査だけ、または計画だけを依頼したい

文言修正など対象が明確な小規模変更では、通常の実装Skillだけで十分な場合がある。

## 基本的な呼び出し方

```txt
/adaptive-deep-planning.md

この機能追加について、要件の明確さと変更規模を分類してください。
必要な調査、要件整理、計画、タスク分割だけを実行してください。
計画承認前は実装しないでください。
```

## 依頼例

### 要件が曖昧な機能追加

```txt
/adaptive-deep-planning.md

管理画面の検索機能を改善したいです。
目的と完了条件を整理し、既存コードを調査して実装計画を作成してください。
不明点はBlocking QuestionとNon-blocking Questionに分けてください。
```

### 既存コードの調査だけ

```txt
/adaptive-deep-planning.md

注文登録処理の現在の挙動と影響範囲を調査してください。
今回は実装計画やコード変更は行わないでください。
```

### 大規模な移行計画

```txt
/adaptive-deep-planning.md

既存バッチを新しい実行基盤へ移行します。
既存仕様、DB、外部連携、運用手順を調査し、実装可能なタスクへ分割してください。
移行方法とロールバック方法を計画に含めてください。
```

### 既存計画のレビュー

```txt
/adaptive-deep-planning.md

docs/planning/implementation-plan.md を現在のコードと照合してください。
計画を最初から作り直さず、不足と古くなった箇所だけを修正候補として示してください。
```

## Workflowが選択する主なSkill

| 状況 | Skill |
|---|---|
| 要件が不明確 | `grill-with-docs` |
| Unknownや確認事項がある | `unknown-list-extractor` |
| 現行仕様が不明 | `legacy-source-spec-writer` |
| 計画や差分を確認する | `review-loop` |
| 計画承認後に実装する | `implementation-loop` |
| 完了を独立判定する | `loop-verifier` |
| 長期文脈を残す | `memory-bank-updater` |

## 主な成果物

選択したルートで必要なものだけを作成する。

```txt
docs/planning/
├── requirements.md
├── codebase-analysis.md
├── impact-analysis.md
├── open-questions.md
├── implementation-plan.md
├── tasks.md
└── tasks/
    └── task-<number>.md
```

## 完了時に確認する内容

- 要件の明確さ
- 変更規模
- 選択したルート
- 実行・スキップした工程と理由
- 作成・更新したファイル
- 確定事項、仮定、Unknown、Blocking Question
- Plan Review判定
- 次に実行する作業

## 注意点

- `Ready` または `Ready with Assumptions` になるまで実装しない。
- セキュリティ、権限、削除、金額、移行のBlocking Questionを推測で確定しない。
- 既存成果物がある場合は、同じ内容を作り直さない。
- 実装または成果物生成後は `/artifact-quality-gate.md` を実行する。
