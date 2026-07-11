---
name: artifact-quality-gate
description: Markdown、HTML、Excel、YAML、JSON、SQL、ソースコード、テスト、図などの生成成果物を、要件網羅性、正確性、一貫性、追跡性、形式、自動検証で判定する親Skill。成果物の完成判定、品質レポート、限定修正と再チェックに使用する。
---

# Artifact Quality Gate

成果物を分類し、必要なチェックだけを実行する。生成できたことだけを完了条件にしない。

## 1. 成果物を分類する

- `Document`: Markdown、HTML、仕様書、設計書、報告書、手順書
- `Structured Data`: YAML、JSON、CSV、XML
- `Spreadsheet`: Excel、テストデータ一覧、課題管理表
- `Source Code`: Java、TypeScript、JavaScript、Python、SQL
- `Test Artifact`: テストコード、テストケース、データ、シナリオ、期待結果
- `Diagram`: Mermaid、PlantUML、画面遷移、シーケンス、ER図

複合成果物には複数カテゴリを適用する。

## 2. 共通品質チェック

- `Completeness`: 必須要件、正常・異常系、対象外、Unknownが含まれる
- `Correctness`: コード、DDL、API、業務ルールと矛盾せず、推測を事実にしていない
- `Consistency`: 用語、項目、クラス、テーブル、画面名、章間の表現が統一されている
- `Traceability`: 要件ID、ファイル、クラス、メソッド、テーブル、シート・セル、API、Issueへ追跡できる
- `Readability`: 第三者が理解でき、曖昧な表現や不必要に長い記述がない
- `Maintainability`: 生成元と再生成方法が明確で、重複が少なく更新しやすい

## 3. 要件対応表

要件と成果物の対応を次の状態で記録する。

| 要件ID | 要件 | 対応箇所 | 状態 |
|---|---|---|---|
| REQ-001 | 要件 | セクションまたはファイル | OK / Partial / NG / Not Applicable / Unknown |

`Partial` または `NG` が存在する場合は原則不合格とする。

## 4. 根拠確認

各主張を `Confirmed / Derived / Assumption / Unknown` に分類し、確認可能な根拠を記録する。コードはファイルとシンボル、Excelはファイル・シート・セル、DDLはテーブル・カラム・型を示す。

## 5. 成果物別チェック

### Markdown・仕様書

章構成、目的・範囲、入出力、正常・異常系、用語、Unknown、根拠、見出し、リンクを確認する。

### HTML

`/html-artifact-checker` を使い、構文、文字化け、見出し、表、長文、印刷、仕様網羅性、Markdown版との一致、ブラウザ表示を確認する。

### Excel

シート・列・順序・型・日付・数式・参照・列幅・フィルター・重複・一意IDを確認する。

### YAML・JSON

パース、必須キー、型、列挙、重複ID、参照先、インデント、スキーマ、未定義項目を確認する。

### SQL・テストデータ

DDLとの一致、型、NOT NULL、PK、FK、UNIQUE、長さ、日付関係、正常・境界・異常データ、実行順序、ロールバックを確認する。

### ソースコード

`/review-loop` と `/loop-verifier` を使い、ビルド、lint、テスト、要件、既存設計、不要変更、例外、ログ、セキュリティ、重複、テスト対応を確認する。

### テスト

要件対応、正常・異常・境界・NULL・空文字・最大最小・重複・権限、具体的な期待結果、独立性、再実行性を確認する。

### Mermaid・図

構文、名称、遷移、戻り、異常系、矢印、本文との一致、情報量を確認する。

## 6. 自動検証

プロジェクトに存在する検証手段だけを使用する。

- Markdown: lint、リンク確認
- HTML: validator、ブラウザ表示
- YAML/JSON: parser、schema
- Java: build、test、Checkstyle、SpotBugs
- TypeScript: typecheck、lint、test
- SQL: 一時DB投入、制約確認
- Excel: シート、列、数式、参照の検証

実行コマンド、結果、詳細を記録する。未実行項目は理由を明記する。

## 7. 独立レビュー

可能なら生成処理とは別のレビュー観点で評価する。Reviewerには要件、完了条件、成果物、既存仕様、チェックリストを渡し、生成時の説明は判定根拠にしない。

## 8. スコアと強制Fail

| 評価項目 | 配点 |
|---|---:|
| 要件網羅性 | 25 |
| 正確性 | 25 |
| 一貫性 | 15 |
| 根拠・追跡性 | 15 |
| 可読性 | 10 |
| 保守性 | 10 |

- `90〜100`: Pass
- `80〜89`: Pass with Minor Fixes
- `60〜79`: Needs Revision
- `0〜59`: Fail

必須要件欠落、構文・ビルドエラー、重大なDB制約違反、重大なセキュリティ問題、既存仕様との重大矛盾、根拠のない断定、テスト不能は点数に関係なくFailとする。

## 9. 不具合一覧

| ID | Severity | Category | Location | Problem | Expected Fix |
|---|---|---|---|---|---|

Severityは `Critical / Major / Minor / Suggestion` とする。

## 10. 修正ループ

ユーザーがレビューのみを求めた場合は修正しない。修正が依頼範囲に含まれる場合だけ次を最大3回行う。

1. Critical、Majorから修正対象を限定する。
2. 問題箇所以外を不必要に変更しない。
3. 差分を確認し、自動検証を再実行する。
4. 品質ゲートを再判定する。

3回で合格しない場合は残存問題を報告して停止する。

## 11. 品質レポート

原則として `docs/quality/artifact-quality-report.md` に次を記録する。

- 対象成果物
- `PASS / PASS WITH MINOR FIXES / NEEDS REVISION / FAIL`
- 品質スコア
- 要件対応表
- 実行したチェックと自動検証結果
- 修正した問題と残存問題
- 仮定、Unknown、未実行検証
- 完了または差し戻しの結論

CriticalまたはMajorが残る場合、完了扱いにしない。
