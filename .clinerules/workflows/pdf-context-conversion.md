# PDF Context Conversion Workflow

大きなPDFを索引付きの分割Markdownへ変換し、Clineが必要箇所だけ読める状態にする。

1. Skill `context-window-manager`で目的、対象PDF、必要ページ、完了条件を定義する。
2. Skill `pdf-context-converter`で形式とチャンクサイズを選ぶ。
3. 標準はMarkdownとし、表や視覚構造が必要な場合だけHTMLまたはbothを選ぶ。
4. `docs/ai/pdf/<document-name>/`へ`index.md`、`metadata.json`、`sections/`を生成する。
5. `OCR_REQUIRED`、抽出エラー、低文字量ページを確認する。
6. 表、図、数式、段組みが判断根拠になるページは原本レンダリングと照合する。
7. 以降の調査では`index.md`と検索結果から必要チャンクだけを読む。
8. Skill `artifact-quality-gate`で完全性、追跡性、可読性を判定する。

原本PDFは削除せず、変換物を正本として扱わない。
