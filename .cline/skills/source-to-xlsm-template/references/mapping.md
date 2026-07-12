# XLSM Mapping

マッピングはJSONで管理し、Pythonコードを案件ごとに書き換えない。

```json
{
  "sheet": "Sections",
  "start_row": 2,
  "clear_existing": true,
  "clear_to_row": 1000,
  "copy_style_from_row": 2,
  "columns": {
    "index": "A",
    "level": "B",
    "heading": "C",
    "content": "D",
    "source_file": "E",
    "source_location": "F",
    "selector": "G",
    "render_mode": "H",
    "requirement_ids": "I",
    "source_evidence": "J"
  },
  "image": {
    "column": "K",
    "width": 960,
    "height": 540,
    "row_height_points": 300,
    "required": true
  }
}
```

## Fields

| Field | Required | Meaning |
|---|---|---|
| `sheet` | Yes | 書き込み先シート |
| `start_row` | Yes | データ開始行 |
| `clear_existing` | No | 既存値を消去してから出力するか |
| `clear_to_row` | Conditional | 消去する最終行 |
| `copy_style_from_row` | No | 新しい行へ複製する書式の見本行 |
| `columns` | Yes | セクション属性とExcel列の対応 |

使用可能な列属性:

- `index`
- `level`
- `heading`
- `content`
- `source_file`
- `source_location`
- `selector`
- `render_mode`
- `requirement_ids`
- `source_evidence`

## Screenshot Manifest

ブラウザで各`<section>`をキャプチャし、次のmanifestを作成する。

```json
{
  "sections": [
    {
      "source_file": "outputs/html/mock.html",
      "selector": "#account-form",
      "render_mode": "image-and-text",
      "requirement_ids": "REQ-001,REQ-002",
      "source_evidence": "src/account/service.ts:createAccount",
      "image": "screenshots/account-form.png"
    },
    {
      "source_file": "outputs/html/mock.html",
      "selector": "#business-rules",
      "render_mode": "text"
    }
  ]
}
```

`render_mode`は次のいずれかを指定する。

| Mode | Excelへの出力 | 画像 |
|---|---|---|
| `text` | 見出し、説明、出典 | 不要 |
| `image` | 見出し、HTMLレンダリング画像、出典 | 必須 |
| `image-and-text` | 見出し、説明、HTMLレンダリング画像、出典 | 必須 |

manifestにないセクションは`text`として扱う。`image`または`image-and-text`で画像がない場合はエラーにする。

HTML側にも追跡情報を保持できる。

```html
<section
  id="account-form"
  data-requirement-ids="REQ-001,REQ-002"
  data-source-evidence="src/account/service.ts:createAccount">
</section>
```

manifestに`requirement_ids`または`source_evidence`がある場合はHTML属性を上書きする。

セル結合、固定帳票セル、セクション種別ごとの別シートなどが必要な場合は、テンプレート固有のマッピング仕様を追加し、未定義の推測で書き込まない。

既存出力を置換する場合は、マッピングではなくコマンドの`--overwrite`で明示する。生成または検証に失敗した場合、既存出力は保持される。
