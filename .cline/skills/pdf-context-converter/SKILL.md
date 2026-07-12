---
name: pdf-context-converter
description: 大きなPDFをClineが必要な範囲だけ検索・読込できるよう、索引とページ範囲別Markdownへ変換する。表や視覚構造を確認する場合はHTMLも生成する。PDF調査、コンテキスト圧迫の回避、ページ単位の出典保持、スキャンPDFの検出が必要な場合に使用する。
---

# PDF Context Converter

PDFを会話へ直接投入せず、検索可能な索引と小さなチャンクへ変換する。原本PDFを正本とし、生成物は検索・部分読込用の派生物として扱う。

## 出力方針

- 標準は`Markdown`。意味構造、差分、`rg`検索、部分読込を優先する。
- 表、段組み、配置の確認が必要な場合は`HTML`または`both`を選ぶ。
- 単一の巨大ファイルを標準出力にしない。
- ページ番号、原本名、抽出状態を失わない。
- 抽出文字が少ないページを成功扱いせず、`OCR_REQUIRED`として残す。

詳しい選択基準は[references/conversion-policy.md](references/conversion-policy.md)を読む。

## Workflow

### 1. Contract

次を確定する。

- 入力PDF
- 出力先（標準: `docs/ai/pdf/<document-name>/`）
- `markdown | html | both`
- 1チャンクのページ数
- 表、図、段組み、スキャン文書の有無
- 必要な検証レベル

### 2. Convert

```bash
python3 .cline/skills/pdf-context-converter/scripts/pdf_to_context.py \
  --input path/to/source.pdf \
  --output-dir docs/ai/pdf/source \
  --format markdown \
  --pages-per-chunk 5
```

既存出力を置換する場合だけ`--overwrite`を指定する。

### 3. Inspect

- `index.md`でページ範囲、文字数、抽出状態を確認する。
- `OCR_REQUIRED`があればOCR可否を判断し、未実施なら制約として報告する。
- 表や図が判断根拠になるページは原本レンダリングと照合する。
- HTMLはブラウザーで開き、見出し、表、文字化け、欠落を確認する。

### 4. Retrieve

調査時は次の順に読む。

1. `index.md`
2. `rg`で関連語を検索
3. 該当する`sections/pages-*.md`だけ読む
4. 配置が重要な場合だけ`document.html`または原本ページを確認

### 5. Report

- 入力と出力パス
- 総ページ数、チャンク数、抽出文字数
- `OK / LOW_TEXT / OCR_REQUIRED / EXTRACTION_ERROR`の件数
- 未検証の表、図、数式、OCR
- 調査で読むべきチャンク

## Quality Guardrails

- Markdown化だけでコンテキスト削減済みと判断しない。索引から必要チャンクだけ読む。
- PDFの表示順と抽出テキスト順が同一だと仮定しない。
- 空ページ、画像ページ、抽出例外を黙って欠落させない。
- HTMLへPDF本体やページ画像をBase64埋め込みしない。
- 原本PDFを削除・上書きしない。
- 数値、表、脚注、改ページを重要判断に使う場合は原本と照合する。

## Completion

- `index.md`、`metadata.json`、分割Markdownが生成されている
- 全ページがいずれかのチャンクに対応している
- 各チャンクから原本名とページ範囲を追跡できる
- 低抽出ページとエラーが明示されている
- 必要な場合だけHTMLが生成されている
- Clineが索引から必要範囲だけ取得できる
