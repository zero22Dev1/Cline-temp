# PDF Context Conversion 使用方法

## 実行例

```txt
/pdf-context-conversion.md

work-folderのPDFを、コンテキスト効率の良い分割Markdownへ変換してください。
最初に索引を生成し、5ページ単位で分割してください。
表やレイアウトの確認が必要なページだけHTMLと原本を照合してください。
```

## 形式の指定例

```txt
pdf-context-converter Skillを使用してください。

input/manual.pdfをdocs/ai/pdf/manual/へ変換してください。
検索用Markdownと視覚確認用HTMLの両方を生成し、OCRが必要なページを報告してください。
```

## 読み方

1. `index.md`だけを読む
2. `rg -n "検索語" docs/ai/pdf/<name>/sections`で対象を絞る
3. 該当チャンクだけをClineへ読み込ませる
4. 表、図、数式、配置が重要な箇所だけ原本PDFを確認する

変換した全Markdownを一度に読み込ませると、コンテキスト削減効果がなくなる。
