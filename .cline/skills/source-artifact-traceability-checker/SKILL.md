---
name: source-artifact-traceability-checker
description: 既存ソースを正本として、ソース由来仕様、HTMLモック、セクションmanifest、生成済みマクロ付きExcelの間で、処理、項目、分岐、検証、エラー、権限、画面状態、出典の欠落や矛盾を独立照合する。HTMLやExcelが既存ソースと合っているか、生成工程と別の観点で最終確認したい場合に使用する。
---

# Source Artifact Traceability Checker

生成担当の説明や中間成果物だけを正解にせず、既存ソースへ直接戻ってHTMLとExcelを検証する。

このSkillはClineの`.cline/skills/`から使用し、親Workflow`/source-to-verified-xlsm.md`の独立Evaluatorとして動作する。

## Inputs

- 既存ソース、設定、テンプレート、テスト、DDL、API
- `docs/specs/`のソース由来仕様
- `docs/ai/unknowns/`
- HTMLレイアウトテンプレート
- 生成HTMLとセクションmanifest
- Excelテンプレート、マッピング、生成`.xlsm`
- build、test、ブラウザ、Excel検査結果

## Canonical Traceability

各確認項目へ`REQ-<連番>`を割り当て、全段階で維持する。

```txt
既存ソースの根拠
  -> REQ-ID
  -> docs/specsの項目
  -> HTML section id
  -> manifest selector / render_mode
  -> Excel sheet / row / cell / image
```

HTMLの見た目だけでは表せない処理は`text`セクションとしてExcelへ残す。画面状態が重要な項目は`image`または`image-and-text`でHTMLレンダリング画像を残す。

## Review Dimensions

1. `Process`: 処理順、条件分岐、状態遷移、非同期処理
2. `Data`: 入出力、項目名、型、初期値、変換、保存先
3. `Validation`: 必須、形式、範囲、相関、重複、境界値
4. `Errors`: 例外、メッセージ、復旧、ロールバック
5. `Permissions`: ロール、認証、認可、表示・操作制御
6. `UI`: ラベル、入力、ボタン、一覧、モーダル、表示条件
7. `Integration`: API、DB、ファイル、外部システム
8. `Quality`: 性能、信頼性、セキュリティ、監査、ログ
9. `Unknown`: ソースから断定できない内容

## Independent Check Process

### 1. Reconstruct From Source

中間仕様を判定根拠にせず、対象ソースのエントリーポイント、呼び出し先、条件、テストから確認項目と根拠を再構成する。

### 2. Compare Specification

再構成した項目が`docs/specs/`に存在するか確認する。ソース由来仕様で欠落した項目は、後続成果物同士が一致していても合格にしない。

### 3. Compare HTML

Skill `html-artifact-checker`を使い、仕様と直接ソースの両方に対して確認する。

- レイアウトテンプレートへの適合
- `section id`の一意性
- 項目、操作、正常・異常状態
- 表示条件、バリデーション、エラー
- HTMLレンダリング画像が必要な状態の再現

### 4. Compare XLSM

- 必須シート、列、開始行、件数
- REQ-ID、section id、selector、render_mode
- `text / image / image-and-text`の意図との一致
- HTMLレンダリング画像とExcel画像の対応
- 文字のみセクションの説明充足
- 数式、名前定義、書式、行高、リンク
- 原本テンプレート不変と`vbaProject.bin`一致

### 5. Direct Source Sampling

少なくとも次を既存ソースから直接選び、Excelまで逆追跡する。

- 正常系1件
- 条件分岐1件
- バリデーションまたはエラー1件
- 権限または表示条件1件（存在する場合）
- データ更新または外部連携1件（存在する場合）

サンプルだけで全体網羅を主張せず、全件対応表と組み合わせる。

## Traceability Matrix

```md
| REQ-ID | Source Evidence | Spec | HTML Section | Mode | XLSM Location | Status | Notes |
|---|---|---|---|---|---|---|---|
```

`Status`は`OK / Partial / Missing / Contradiction / Unknown / Not Applicable`とする。

## Accuracy Loop

`Partial / Missing / Contradiction`がある場合は`/harness-engineering-loop.md`へ渡し、次へ分類する。

- `Source Extraction Gap`
- `Specification Gap`
- `HTML Coverage Gap`
- `Capture Gap`
- `XLSM Mapping Gap`
- `Evaluator Gap`

同じ欠落が再発した場合は、個別成果物だけでなく抽出規則、追跡ID、テスト、検査器を改善する。

判定結果はハーネスの観測データとして返し、生成担当の自己評価だけで次のイテレーションへ進めない。

## Decision

- `APPROVE`: 必須項目が全段階で`OK`、重大矛盾なし、検証根拠あり
- `REJECT`: 必須項目の欠落・矛盾、画像や文字の対応不良、検証失敗
- `ESCALATE_HUMAN`: ソースだけでは業務意図、画面表現、正解を決定不能

`Unknown`を推測で埋めてAPPROVEしない。

## Output

`docs/reviews/YYYYMMDD-<feature>-source-xlsm-traceability.md`へ次を出力する。

- 対象範囲と正本
- Traceability Matrix
- 直接ソース照合サンプル
- HTMLレイアウト・内容検証
- XLSM構造・画像・VBA検証
- 欠落、矛盾、Unknown
- 品質スコア
- `APPROVE / REJECT / ESCALATE_HUMAN`
- 次の修正対象または人間確認事項
