---
name: source-to-xlsm-template
description: 既存ソース、生成済みHTML、Markdownからセクションを抽出し、ワークフォルダー内のマクロ付きExcelテンプレート（.xlsm）を毎回コピーして帳票を生成する。VBA、既存書式、数式、シート構成を保持し、原本を変更せず、セクションと出典を追跡可能にしたい場合に使用する。
---

# Source To XLSM Template

`.xlsm`原本を直接編集せず、コピー先へHTMLセクションのHTMLレンダリング画像と説明を書き込む。画像は写真やAI生成画像ではなく、既存ソースから生成したHTMLをブラウザで描画・キャプチャしたものとする。Pythonコードは毎回生成せず、[scripts/generate_xlsm.py](scripts/generate_xlsm.py)を再利用する。

## Workspace Contract

```txt
templates/excel/
├── <template-name>.xlsm
└── <mapping-name>.json
outputs/excel/
```

テンプレートとマッピングの場所が指定されていない場合は、この構成から候補を検索する。候補が複数あり安全に選べない場合は確認する。

マッピング例は[references/mapping.md](references/mapping.md)を読む。

## Inputs

- `.md`: ATX見出し（`#`から`######`）ごとに抽出
- `.html`、`.htm`: `<section>`単位で抽出し、最初の`h1`から`h6`を見出しに使用
- その他の既存ソース: 先にSkill `legacy-source-spec-writer`でMarkdown仕様へ変換してから入力
- `.xlsm`: コピー元テンプレート
- `.json`: 出力先シート、開始行、列、消去範囲などのマッピング

## Workflow

1. 入力ソース、テンプレート、マッピング、出力先を確定する。
2. テンプレートが`.xlsm`で、`xl/vbaProject.bin`を含むことを確認する。
3. 元テンプレートのハッシュを記録する。
4. HTMLを`<section>`単位に解析し、見出し、本文、`id`由来のselector、REQ-ID、ソース出典を保持する。
5. 各セクションを`text / image / image-and-text`へ分類する。
6. 画像を使用するセクションはブラウザでselector単位にHTML画面をキャプチャし、manifestを作成する。
7. `generate_xlsm.py`でテンプレートをコピーし、分類に応じて説明とHTMLレンダリング画像をコピー先だけへ書き込む。
8. 元テンプレートのハッシュが不変であることを確認する。
9. 出力内のVBAプロジェクトがテンプレートと同一であることを確認する。
10. シート名、書込件数、画像、代表セル、数式、空欄、書式を検証する。
11. Windows版Excelでマクロ実行が必要な場合は、信頼済み環境で手動動作確認する。

## Command

```bash
python .cline/skills/source-to-xlsm-template/scripts/generate_xlsm.py \
  --template templates/excel/source-document-template.xlsm \
  --mapping templates/excel/source-document-mapping.json \
  --input outputs/html/mock.html \
  --screenshots outputs/html/section-screenshots.json \
  --output outputs/excel/example.xlsm
```

複数入力は`--input`を繰り返す。

既存の出力を置き換える場合だけ`--overwrite`を明示する。生成とVBA検証が完了するまでは既存出力を置換しない。

生成後は原本との契約検証を実行する。

```bash
python .cline/skills/source-to-xlsm-template/scripts/verify_xlsm.py \
  --template templates/excel/source-document-template.xlsm \
  --mapping templates/excel/source-document-mapping.json \
  --manifest outputs/html/section-screenshots.json \
  --input outputs/html/mock.html \
  --expected-sections <count> \
  --output outputs/excel/example.xlsm
```

## Required Behavior

- `load_workbook(..., keep_vba=True, keep_links=True)`を使用する。
- 出力拡張子を`.xlsm`に固定する。
- テンプレートを`copy2`でコピーしてから編集する。
- 一時ファイルで生成・検証し、成功後に出力先へ置換する。
- 既存出力は既定で拒否し、`--overwrite`指定時だけ置換する。
- 既存行・数式・名前定義・書式を必要以上に変更しない。
- VBAコードを編集しない。
- `vbaProject.bin`の存在とSHA-256一致を検証する。
- 生成件数と出典ファイルを最終結果に含める。
- HTMLモックは画像対象の`<section>`だけをキャプチャし、HTMLレンダリング画像として画像列へ埋め込む。
- `text`セクションには画像を要求せず、`image`と`image-and-text`には画像を必須とする。
- `script`、`style`、`template`要素の内容を説明本文へ含めない。
- `data-requirement-ids`と`data-source-evidence`をExcelまで引き継ぐ。
- `verify_xlsm.py`で入力セクションとマッピング列の値を行単位で照合し、VBA、シート、名前定義、結合セル、画像件数、書込許可範囲外の値・数式・書式を原本と比較する。

## Macro Safety

- Clineからマクロを実行しない。
- インターネット由来または信頼できない`.xlsm`を開かない。
- VBA署名は保存処理で無効になる可能性があるため、署名済みテンプレートは実ファイルで別途検証する。
- ActiveX、外部接続、Power Query、複雑な埋め込みオブジェクトを含む場合は、Excelで回帰確認する。
- LibreOfficeやプレビューだけでマクロ互換性を合格判定しない。

## Completion

- 原本テンプレートが変更されていない
- 出力が`.xlsm`
- VBAプロジェクトが存在し、原本と同一
- 全セクションが期待行へ出力されている
- 見出し階層、本文、出典が追跡可能
- 代表セルと数式を検査済み
- 必要な場合はExcelでマクロ動作を確認済み、または未確認と明記
