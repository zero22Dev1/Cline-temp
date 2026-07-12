# Source To Verified XLSM Workflow Usage

## 目的

既存ソースからHTMLモックとマクロ付きExcelを生成し、最終Excelまで処理内容が欠落・変質していないことを既存ソースへ戻って確認する。

Cline Custom Workflow、Cline Skills、Loop Engineering、Harness Engineeringを組み合わせて実行する。

## 必要な配置

```txt
templates/html/
└── <layout-template>/
templates/excel/
├── <template>.xlsm
└── <mapping>.json
```

## 使用例

```txt
/source-to-verified-xlsm.md

対象機能の既存ソースを正本として仕様化してください。
templates/html/のレイアウトを使用してHTMLモックを生成し、
各sectionをtext / image / image-and-textに分類してください。
templates/excel/の.xlsmをコピーしてExcelを生成し、
既存ソースからExcelまでのTraceability Matrixで欠落と矛盾を確認してください。
```

## 主な成果物

```txt
docs/specs/<feature>.md
docs/ai/unknowns/<date>-<feature>-unknowns.md
outputs/html/<feature>-mock.html
outputs/html/<feature>-section-manifest.json
outputs/html/screenshots/*.png
outputs/excel/<feature>.xlsm
docs/reviews/<date>-<feature>-source-xlsm-traceability.md
```

## 合格条件

- 必須処理が既存ソース、仕様、HTML、Excelで追跡可能
- HTMLテンプレートのレイアウトへ適合
- 文字・画像の分類とExcel出力が一致
- 既存ソースとの直接照合で重大な欠落・矛盾なし
- Excelテンプレート、VBA、数式、書式を保持
- 品質ゲートPASS、独立検証APPROVE

## 精度改善

欠落が見つかった場合は成果物だけを直さず、原因を抽出、仕様、HTML、キャプチャ、Excelマッピング、検査器へ分類する。同じ欠落が再発した場合はルール、テスト、Skill、追跡項目を改善する。

## Loop And Harness

```txt
Contract / Budget / Harness
  -> Source Specification
  -> HTML Generate / Observe / Evaluate
  -> XLSM Generate / Observe / Evaluate
  -> Direct Source Verification
  -> Gap Diagnose
  -> Artifact or Harness Improvement
  -> Repeat or Stop
  -> Project Learning
```

既定は最大3イテレーション。同じ失敗が2回続いた場合は再生成だけを行わず、ソース索引、抽出規則、REQ-ID、スクリーンショット観測、Excel検査、Evaluatorのいずれかを改善する。
