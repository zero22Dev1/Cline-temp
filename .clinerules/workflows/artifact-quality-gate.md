# Artifact Quality Gate Workflow

生成または実装した成果物を、種類に応じた検証へ振り分け、完了可能か判定する。

## Teams Notification Option

開始時に`Teams通知: 有効 / 無効`を選択する。未指定は`無効`とし、今回の実行だけに適用する。`有効`でも、この品質ゲートに加えてモード固有の完了条件を満たした時だけ通知する。

## Workflow Rules

- 成果物を生成できただけでは完了扱いにしない。
- 要件、既存仕様、根拠、形式、自動検証を確認する。
- レビューのみの依頼では成果物を修正しない。
- CriticalまたはMajorが残る場合は完了扱いにしない。
- ユーザーへの説明と出力は日本語で行う。

## Step 1: 親Skillを読み込む

Skill `artifact-quality-gate` を読み込み、対象成果物と参照資料を確認する。

必要な入力:

- 対象成果物
- 要件または完了条件
- `docs/specs/`、`docs/planning/`、`docs/ai/`、`memory-bank/`
- 関連するソース、DDL、API仕様、テスト

## Step 2: 成果物を分類する

- `Document`: Markdown、HTML、仕様書、設計書、報告書
- `Structured Data`: YAML、JSON、CSV、XML
- `Spreadsheet`: Excel、一覧、管理表
- `Source Code`: Java、TypeScript、JavaScript、Python、SQL
- `Test Artifact`: テストコード、ケース、データ、期待結果
- `Diagram`: Mermaid、PlantUML、画面遷移、シーケンス、ER図

複合成果物には複数カテゴリを適用する。

## Step 3: 共通チェックを行う

次の6観点を確認する。

1. 要件網羅性
2. 正確性
3. 一貫性
4. 根拠・追跡性
5. 可読性
6. 保守性

要件対応表を作成し、各項目を `OK / Partial / NG / Not Applicable / Unknown` で判定する。

## Step 4: 成果物別Skillと検証を選ぶ

必要なものだけを使用する。

- HTML: Skill `html-artifact-checker`
- ソースコード: Skill `review-loop` と Skill `loop-verifier`
- 不明な根拠: Skill `unknown-list-extractor`
- 実装修正: ユーザーが修正を依頼している場合だけ Skill `implementation-loop`

その他の形式は Skill `artifact-quality-gate` のチェックリストに従い、利用可能なparser、schema、lint、build、test、DB、ブラウザ検証を実行する。

## Step 5: 自動検証結果を記録する

| Check | Result | Details |
|---|---|---|
| 検証名 | `PASS / FAIL / NOT RUN` | 結果または未実行理由 |

存在しないツールやコマンドを推測で実行しない。実行できない検証は `NOT RUN` と理由を記録する。

## Step 6: 品質を判定する

| 評価項目 | 配点 |
|---|---:|
| 要件網羅性 | 25 |
| 正確性 | 25 |
| 一貫性 | 15 |
| 根拠・追跡性 | 15 |
| 可読性 | 10 |
| 保守性 | 10 |

- `90〜100`: PASS
- `80〜89`: PASS WITH MINOR FIXES
- `60〜79`: NEEDS REVISION
- `0〜59`: FAIL

必須要件欠落、構文・ビルドエラー、重大なDB制約違反、重大なセキュリティ問題、重大な仕様矛盾、根拠のない断定、テスト不能は強制FAILとする。

## Step 7: 不具合一覧を作る

```md
| ID | Severity | Category | Location | Problem | Expected Fix |
|---|---|---|---|---|---|
```

Severityは `Critical / Major / Minor / Suggestion` とする。

## Step 8: Repair Loop

修正が依頼範囲に含まれる場合だけ、最大3回実行する。

```txt
Quality Check
  -> Defect List
  -> Critical / Majorを限定修正
  -> Diff確認
  -> 自動検証を再実行
  -> Quality Checkを再実行
```

3回で合格しない場合は修正を停止し、残存問題を報告する。

## Step 9: Final Quality Report

`docs/quality/artifact-quality-report.md` に次を記録する。

- 対象成果物
- Quality Gate判定と品質スコア
- 要件対応表
- 実行したチェック
- 自動検証結果
- 修正した問題と残存問題
- 仮定、Unknown、未実行検証
- 完了または差し戻しの結論

最終判定は次のいずれかとする。

```txt
Quality Gate: PASS
Quality Gate: PASS WITH MINOR FIXES
Quality Gate: NEEDS REVISION
Quality Gate: FAIL
```

PASS後に Skill `memory-bank-updater` を実行する。再利用可能な訂正、失敗パターン、設計判断、性能測定、検証済みの改善がある場合は `/continuous-project-learning.md` へ進み、その後必要に応じて Skill `template-commit-workflow` または Skill `git-commit-workflow` へ進む。

`Teams通知: 有効`の場合、計画成果物はPlan Reviewの実装可能判定を確認して`/teams-completion-notification.md`の`plan`モードへ進む。ソースコード成果物は必須テスト、Skill `review-loop`、Skill `loop-verifier`までPASSしたことを確認して`implementation`モードへ進む。その他の成果物はWorkflow固有の完了条件とSkill `loop-verifier`の`APPROVE`を確認して`workflow`モードへ進む。品質ゲート単体のPASSだけでは送信しない。
