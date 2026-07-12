# Source To XLSM Template Workflow Usage

## 目的

既存ソースから生成したHTMLモックを`<section>`単位で整理し、文字またはHTMLレンダリング画像をワークフォルダー内の`.xlsm`テンプレートへ掲載する。画像は写真ではなく、ブラウザで描画したHTML画面キャプチャを使用する。

## 配置

```txt
templates/excel/
├── source-document-template.xlsm
└── source-document-mapping.json
outputs/excel/
```

## 実行例

```txt
/source-to-xlsm-template.md

既存ソースからHTMLモックを生成し、各画面を<section id="...">で分割してください。
各sectionをtext / image / image-and-textに分類し、画像対象だけをHTML画面キャプチャしてください。
templates/excel/のマクロ付きテンプレートをコピーし、outputs/excel/へ出力してください。
元テンプレートとVBAが変更されていないことも検証してください。
```

## 注意

- テンプレート原本は直接編集しない。
- `.xlsm`以外へ変換しない。
- マクロをClineから自動実行しない。
- 署名、ActiveX、外部接続を含む場合はWindows版Excelで確認する。
- 生成後は`verify_xlsm.py`へ生成時と同じ入力を渡し、マッピング列の期待値、VBA、シート、名前定義、結合セル、画像件数、許可範囲外の値・数式・書式を検証する。
- synthetic fixtureの成功だけで実テンプレートを合格にせず、実HTML・manifest・mapping・`.xlsm`でEnd-to-End検証する。
