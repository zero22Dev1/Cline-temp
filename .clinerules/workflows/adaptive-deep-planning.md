# Adaptive Deep Planning Workflow

開発依頼を分類し、必要なCline Skillだけを選んで、調査・計画・レビュー・実装引き継ぎまで進める。

## Workflow Rules

- 最初から実装しない。
- 既存コード、仕様、計画、タスクを確認してから工程を選ぶ。
- 確定事項、仮定、Unknown、Blocking Questionを分離する。
- 小規模変更に過剰な文書を作らない。
- 計画承認前は本番コードを変更しない。
- ユーザーへの説明と出力は日本語で行う。

## Step 1: 親Skillを読み込む

Skill `adaptive-deep-planning` を読み込み、以下を判定する。

- 要件の明確さ: `明確 / 一部不明 / 不明確`
- 変更規模: `Small / Medium / Large`
- 既存成果物の有無
- コード調査の必要性
- 依頼種別: `実装 / 調査のみ / 計画のみ / レビューのみ`

## Step 2: ルートを選択する

| 条件 | 実行ルート |
|---|---|
| 明確・Small | `Direct Plan -> Plan Review` |
| 不明確・Small | `Requirement Grill -> Direct Plan -> Plan Review` |
| 明確・Medium | `Deep Investigation -> Plan Review` |
| 不明確・Medium | `Requirement Grill -> Deep Investigation -> Plan Review` |
| 明確・Large | `Deep Investigation -> Task Decomposition -> Plan Review -> Handoff` |
| 不明確・Large | `Requirement Grill -> Deep Investigation -> Task Decomposition -> Plan Review -> Handoff` |
| 計画あり | 現在コードとの整合確認後、`Plan Review -> 必要ならTask Decomposition -> Handoff` |
| タスクあり | 計画との整合確認後、対象タスクを選んでHandoff |

調査のみの場合は計画・実装へ進まない。計画のみの場合は実装・Handoffへ進まない。

## Step 3: 必要なSkillを呼び出す

選択ルートに含まれるものだけを使用する。

- 要件整理: `/grill-with-docs`
- 不明点分類: `/unknown-list-extractor`
- 現行仕様化: `/legacy-source-spec-writer`
- 実装: `/implementation-loop`
- 計画・差分レビュー: `/review-loop`
- 独立検証: `/loop-verifier`
- 長期文脈更新: `/memory-bank-updater`
- 継続学習: `/ai-learning-curator`
- 複数回の成果物反復: `/harness-engineering-loop.md`
- 長時間・複数領域の文脈管理: `/context-window-management.md`

既存資料がある場合は作り直さず、不足部分だけを更新する。

MediumまたはLarge、複数Skill、引き継ぎを含む場合は`/context-window-management.md`でContext Contractを作り、工程境界ごとにCheckpointを更新する。

## Step 4: Planning Artifacts

選択ルートで必要なものだけを作成する。

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

各判断には、可能な限りファイルパス、クラス、メソッド、テーブル、API、仕様書などの根拠を付ける。

## Step 5: Plan Review Gate

実装前に次を確認する。

- 要件、正常系、異常系、対象外、完了条件を網羅している
- Blocking Questionが残っていない
- 既存設計・API・DBとの整合性がある
- セキュリティ、移行、ロールバックを考慮している
- 自動または手動の検証方法が定義されている

判定:

- `Ready`: 実装可能
- `Ready with Assumptions`: 仮定を明示して実装可能
- `Needs Revision`: 計画を修正して再レビュー
- `Blocked`: 確認が解決するまで停止

`Ready` または `Ready with Assumptions` 以外では実装しない。

## Step 6: Implementation And Quality Gate

ユーザーが実装を依頼し、計画が承認済みの場合だけ `/implementation-loop` を実行する。

単一実装で完了できる場合は、実装または成果物生成後に `/artifact-quality-gate.md` Workflowへ進む。複数回の反復が必要な場合は `/harness-engineering-loop.md` を使用し、その内部で品質ゲートを実行する。

```txt
Planning
  -> Plan Review
  -> Implementation / Artifact Generation
  -> Artifact Quality Gate
  -> Memory Bank Update
  -> Continuous Project Learning
  -> Git Workflow
```

品質ゲート通過後に再利用可能な訂正、失敗、設計判断、性能測定がある場合は `/continuous-project-learning.md` へ進む。

## Stop Conditions

次の場合は停止し、理由と必要な回答を報告する。

- データ、削除、金額、権限、セキュリティ、外部契約、移行方針を安全に確定できない
- 依頼、コード、仕様が重大に矛盾する
- 検証方法を定義できない
- 影響範囲が当初分類を超え、再計画が必要

## Final Output

- 判定した要件の明確さと変更規模
- 選択ルート、実行Skill、スキップ理由
- 作成・更新した成果物
- 確定事項、仮定、Unknown、Blocking Question
- Plan Review判定
- 次のアクション
