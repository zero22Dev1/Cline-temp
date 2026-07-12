---
name: harness-engineering-loop
description: Clineが長時間・複数回の反復で成果物を完成させるために、目標、実行環境、コンテキスト、ツール、観測可能性、検証器、予算、停止条件、学習還元を設計・改善する。成果物生成ループが停滞する、同じ失敗を繰り返す、テストや品質判定が弱い、保守性・性能・信頼性を継続改善したい場合に使用する。
---

# Harness Engineering Loop

モデルへ「もっと頑張る」よう求めるのではなく、Clineが対象を観測、変更、検証しやすいハーネスを整備する。

ハーネス設計の原則が必要な場合は [references/principles.md](references/principles.md) を読む。

## ハーネスの構成要素

1. `Intent`: 目的、対象外、完了条件、品質基準
2. `Environment`: 再現可能で分離された実行環境
3. `Context`: 小さな入口と、必要時に読む詳細資料
4. `Tools`: build、test、lint、検索、ブラウザ、DB、計測
5. `Observability`: ログ、メトリクス、トレース、スクリーンショット、差分
6. `Constraints`: Rule、schema、型、lint、構造テスト、権限境界
7. `Evaluators`: 自動テスト、品質ゲート、独立レビュー、ベンチマーク
8. `Control`: 予算、再試行上限、停止条件、承認点
9. `Learning`: 失敗から不足能力を特定し、ハーネスへ還元する仕組み

## ループ設計

### 1. Contract

開始前に次を定義する。

- 成果物と保存先
- 必須要件と対象外
- 完了条件
- 自動検証と手動検証
- 性能、信頼性、セキュリティ基準
- 変更禁止範囲

曖昧な場合は `/adaptive-deep-planning.md` を先に実行する。

### 2. Budget

Skill `loop-budget`で最大イテレーション、時間、ツール、コスト、停止条件を決める。既定の自動修正上限は3回とし、長時間ループは明示的な予算を使用する。

### 3. Execute

1イテレーションでは、最も優先度が高い未達項目だけを対象に最小差分で実行する。一度に複数の原因を推測して広範囲を変更しない。

### 4. Observe

実行後に、生の成果物と機械的な結果を集める。

- diff
- build、lint、test
- logs、metrics、traces
- 画面、DOM、スクリーンショット
- schema、DB制約、API結果
- 性能測定値

説明や自己評価より観測結果を優先する。

### 5. Evaluate

`/artifact-quality-gate.md`とSkill `loop-verifier`を使用する。生成担当の説明を根拠にせず、要件、成果物、テスト結果、既存仕様を比較する。

### 6. Diagnose

失敗を次へ分類する。

- `Intent Gap`: 要件または完了条件が曖昧
- `Context Gap`: 必要な仕様や構造が発見できない
- `Tool Gap`: 観測・変更・検証する手段がない
- `Environment Gap`: 再現性、依存関係、分離が不足
- `Observability Gap`: 原因を示すログや計測がない
- `Constraint Gap`: 禁止事項や不変条件が機械化されていない
- `Evaluator Gap`: 合否判定が弱い、または誤っている
- `Implementation Defect`: ハーネスは十分で実装だけが誤っている
- `External Blocker`: 認証、外部状態、ユーザー判断が必要

同じ失敗が再発した場合、実装だけを再試行せずハーネス不足を優先して修正する。

### 7. Improve Harness

分類に応じて最小の改善を行う。

- Intent Gap: 要件、受け入れ条件、例を追加
- Context Gap: 索引、仕様、ADR、ファイルマップを追加
- Tool Gap: 再利用可能なコマンド、script、Skillを追加
- Environment Gap: setup、fixture、container、worktree手順を改善
- Observability Gap: 構造化ログ、メトリクス、トレース、検査手順を追加
- Constraint Gap: lint、schema、型、構造テスト、hookを追加
- Evaluator Gap: 回帰テスト、grader、品質チェックを改善

### 8. Repeat Or Stop

次の場合だけ次のイテレーションへ進む。

- 未達項目が明確
- 新しい根拠が得られた
- 前回と異なる修正またはハーネス改善を行える
- 予算内

同じ操作の反復、根拠のない修正、予算超過、Blocking Questionでは停止する。

### 9. Learn

PASS後、または重要な失敗から知識が得られた場合は `/continuous-project-learning.md` を実行する。成功パターンだけでなく、失敗を検出するテストや観測手段を残す。

## イテレーション記録

```md
| Iteration | Target | Change | Evidence | Result | Gap Type | Harness Improvement | Next Action |
|---:|---|---|---|---|---|---|---|
```

各回で変更した仮説は1つに絞り、前回との差を説明できるようにする。

## 完了条件

- 必須要件が要件対応表で`OK`
- build、lint、testなど必須検証がPASS
- Critical、Majorが残っていない
- 性能基準がある場合は同じ条件で測定して合格
- 根拠と成果物を第三者が追跡できる
- 再現手順とロールバックまたは修復方法がある
- Skill `loop-verifier`が`APPROVE`

## 安全ルール

- 無制限ループを禁止する。
- テストを削除・弱体化してPASSさせない。
- 閾値を根拠なく緩和しない。
- 本番環境や共有データで反復実験しない。
- 検証不能を成功として扱わない。
- ハーネス改善と成果物変更を区別して記録する。
