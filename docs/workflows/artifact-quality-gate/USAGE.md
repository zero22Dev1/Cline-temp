# Artifact Quality Gate Usage

## 概要

`/artifact-quality-gate.md` は、生成した成果物を要件、既存仕様、根拠、形式、自動検証の観点で確認し、完了可能か判定するWorkflowである。

## 使用するタイミング

- MarkdownやHTMLの仕様書を生成した後
- Excel、YAML、JSON、SQL、テストデータを作成した後
- ソースコードやテストコードを実装した後
- Mermaidなどの図を作成した後
- 納品前、commit前、push前に成果物の完成判定を行いたい
- 問題を限定修正して再チェックしたい

## 基本的な呼び出し方

```txt
/artifact-quality-gate.md

今回生成した成果物を分類し、要件対応表、自動検証結果、品質スコアを含むレポートを作成してください。
CriticalまたはMajorが残る場合は完了扱いにしないでください。
```

## 依頼例

### HTML仕様書を確認する

```txt
/artifact-quality-gate.md

docs/specs/order.md と output/order.html を比較してください。
仕様漏れ、表示崩れ、文字化け、見出し構造、印刷時の見切れを確認してください。
今回はレビューだけ行い、HTMLは修正しないでください。
```

### YAMLデータを確認する

```txt
/artifact-quality-gate.md

output/test-data.yaml を対象に、YAML構文、必須キー、型、重複ID、参照先IDを確認してください。
スキーマが存在する場合はスキーマ検証も実行してください。
```

### ソースコードを確認する

```txt
/artifact-quality-gate.md

今回の実装差分を、implementation-plan.md と照合してください。
build、lint、testを実行し、要件漏れ、不要変更、セキュリティ、テスト不足を確認してください。
```

### 問題を修正して再確認する

```txt
/artifact-quality-gate.md

CriticalとMajorだけを修正対象にしてください。
変更を最小限にして検証を再実行し、最大3回まで品質判定を繰り返してください。
```

## 成果物別の主な確認内容

| 種類 | 主な確認内容 |
|---|---|
| Markdown・仕様書 | 章構成、入出力、正常・異常系、用語、Unknown、根拠、リンク |
| HTML | 構文、文字化け、表示、表、長文、印刷、仕様網羅性 |
| Excel | シート、列、型、日付、数式、参照、重複、一意ID |
| YAML・JSON | 構文、必須キー、型、列挙、ID、参照、スキーマ |
| SQL・テストデータ | DDL、NOT NULL、PK、FK、UNIQUE、境界値、実行順序 |
| ソースコード | build、lint、test、既存設計、例外、ログ、セキュリティ |
| テスト | 正常、異常、境界、NULL、権限、期待結果、独立性 |
| Mermaid・図 | 構文、名称、遷移、異常系、矢印、本文との一致 |

## 品質判定

```txt
Quality Gate: PASS
Quality Gate: PASS WITH MINOR FIXES
Quality Gate: NEEDS REVISION
Quality Gate: FAIL
```

次の問題はスコアに関係なくFAILになる。

- 必須要件の欠落
- 構文エラーまたはビルドエラー
- 重大なDB制約違反
- 重大なセキュリティ問題
- 既存仕様との重大な矛盾
- 根拠のない内容を事実として記載
- テスト不能

## 出力

```txt
docs/quality/artifact-quality-report.md
```

レポートには次を含める。

- 対象成果物
- 品質判定とスコア
- 要件対応表
- 自動検証結果
- 不具合一覧
- 修正した問題と残存問題
- 仮定、Unknown、未実行検証
- 完了または差し戻しの結論

## 注意点

- レビューのみの依頼では成果物を修正しない。
- 修正する場合も問題箇所以外を不必要に変更しない。
- 実行できない検証は成功扱いにせず、`NOT RUN` と理由を記録する。
- 最大3回で合格しない場合は、残存問題を報告して停止する。
- PASS後は必要に応じて `memory-bank-updater` とGit Workflowへ進む。
