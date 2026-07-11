# Harness Engineering Loop Usage

## 概要

`/harness-engineering-loop.md`は、成果物が完了条件を満たすまで、予算内で実装、観測、検証、診断、ハーネス改善を繰り返すWorkflowである。

同じプロンプトを繰り返すのではなく、失敗ごとに不足している文脈、ツール、環境、観測、制約、評価器を改善する。

## 使用するタイミング

- 複数回の反復が必要な成果物を作成する
- テストや品質ゲートを通るまで修正したい
- 同じ失敗を繰り返している
- 長時間タスクへ予算と停止条件を設定したい
- 保守性、性能、信頼性を計測しながら改善したい

## 基本的な呼び出し方

```txt
/harness-engineering-loop.md

この成果物を完了条件まで反復して作成してください。
最大3イテレーションとし、各回で変更対象を1つに絞ってください。
同じ失敗が続く場合は実装を再試行せず、ハーネス不足を分析してください。
```

## 性能改善の例

```txt
/harness-engineering-loop.md

API応答時間を同じ測定条件で800ms未満にしてください。
変更前後の値、測定条件、正確性への影響を記録してください。
閾値を緩和して合格させないでください。
```

## UI成果物の例

```txt
/harness-engineering-loop.md

HTML成果物を仕様どおりに完成させてください。
各回でブラウザ表示、長文、モバイル、印刷、仕様対応表を確認してください。
品質ゲートPASSと独立検証APPROVEを完了条件にしてください。
```

## 失敗分類

| Gap | 対応 |
|---|---|
| Intent | 要件・完了条件を明確化 |
| Context | 仕様、索引、ADRを追加 |
| Tool | script、コマンド、Skillを追加 |
| Environment | setup、fixture、分離環境を改善 |
| Observability | ログ、メトリクス、トレースを追加 |
| Constraint | lint、schema、型、構造テストを追加 |
| Evaluator | 回帰テスト、grader、品質判定を改善 |
| Implementation | 実装を最小修正 |
| External | 停止して必要な入力や状態を報告 |

## 完了条件

- 必須要件がすべてOK
- 必須のbuild、lint、test、計測がPASS
- Critical、Majorが残っていない
- 性能基準が同一条件で達成されている
- `/loop-verifier`が`APPROVE`
- 学習が `/continuous-project-learning.md`へ引き継がれている

## 注意点

- 無制限ループを設定しない。
- テストや閾値を弱めてPASSさせない。
- 同じ操作を根拠なく繰り返さない。
- 本番環境や共有データを反復実験に使わない。
- 予算超過やBlocking Questionでは停止する。
