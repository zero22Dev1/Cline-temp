# Harness Engineering Loop Workflow

成果物が完了条件を満たすまで、予算内で実装・観測・評価・診断・ハーネス改善を反復する。

## Step 1: Contract

Skill `harness-engineering-loop` を読み込み、目的、成果物、対象外、完了条件、品質・性能基準、変更禁止範囲を確定する。曖昧な場合は `/adaptive-deep-planning.md`へ戻る。

## Step 2: Budget And Harness Check

`/loop-budget`で予算と停止条件を定義する。実行前に環境、コンテキスト、ツール、観測可能性、制約、評価器が揃っているか確認する。

複数イテレーションまたは長時間作業では`/context-window-management.md`を開始し、各イテレーション後にContext Checkpointを更新する。次回に不要な生ログや探索過程は退避し、根拠パスと検証結果だけをworking setへ残す。

不足がある場合、成果物の実装より先に最小限のハーネスを整備する。

## Step 3: Iteration

各イテレーションで次を1回ずつ実行する。

```txt
優先する未達項目を1つ選ぶ
  -> 最小差分で実装・生成
  -> diffと観測結果を収集
  -> build / lint / test / 計測
  -> /artifact-quality-gate.md
  -> /loop-verifier
  -> PASSなら完了
  -> FAILならGap分類
  -> ハーネスまたは実装を最小修正
  -> 次のイテレーション
```

## Step 4: Failure Classification

失敗を `Intent / Context / Tool / Environment / Observability / Constraint / Evaluator / Implementation / External` のどれかへ分類する。

同じ失敗が2回続いた場合は、実装の再試行を止め、ハーネス改善を必須とする。

## Step 5: Iteration Log

```md
| Iteration | Target | Change | Evidence | Result | Gap Type | Harness Improvement | Next Action |
|---:|---|---|---|---|---|---|---|
```

前回と同じ操作を繰り返さず、新しい根拠または改善がある場合だけ続行する。

## Step 6: Stop Or Complete

次の場合は停止する。

- 予算を使い切った
- Blocking Questionまたは外部ブロッカーがある
- 同じ失敗に対する新しい仮説・観測・改善がない
- 検証器が信頼できず、合否を判断できない
- 本番・共有環境への危険な操作が必要

完了には品質ゲートPASSと`/loop-verifier`の`APPROVE`を必要とする。

## Step 7: Learning

完了後、または重要な失敗パターンを発見した場合は `/continuous-project-learning.md`を実行する。回帰テスト、性能基準、観測手段、Rule、Skill、ADRへ還元する。

## Final Output

- 最終判定
- 使用したイテレーションと予算
- 各回の対象、変更、根拠、結果
- 改善したハーネス
- 未解決事項
- 学習として昇格した内容
