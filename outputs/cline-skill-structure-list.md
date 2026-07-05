# Cline向け構成一覧

Source chat: https://chatgpt.com/share/6a4a39d4-6dd4-83ee-ad94-f70eaa58b7dd

## 目的

この一覧は、共有チャット「Cline Loop Engineering」の内容をClineに導入しやすい形で整理したものです。

主な狙いは次の3つです。

- 既存ソースを調査して仕様化する
- 不明点や確認事項を一覧化する
- 生成したHTML成果物が仕様を漏れなく反映しているか確認する

## 推奨ディレクトリ構成

```txt
.
├─ .clinerules/
├─ .cline/
│  └─ skills/
│     ├─ cline-skill-builder/
│     │  └─ SKILL.md
│     ├─ legacy-source-spec-writer/
│     │  └─ SKILL.md
│     ├─ unknown-list-extractor/
│     │  └─ SKILL.md
│     └─ html-artifact-checker/
│        └─ SKILL.md
├─ memory-bank/
│  ├─ projectbrief.md
│  ├─ activeContext.md
│  ├─ techContext.md
│  └─ progress.md
├─ docs/
│  ├─ ai/
│  │  ├─ active-context.md
│  │  ├─ glossary.md
│  │  ├─ adr/
│  │  └─ unknowns/
│  ├─ specs/
│  └─ reviews/
└─ README.md
```

## Cline Skill一覧

| Slash command | 配置 | 役割 | 主な出力 | 優先度 |
|---|---|---|---|---|
| `/cline-skill-builder` | `.cline/skills/cline-skill-builder/SKILL.md` | Cline用Skillを作成・変換・改善・レビューするメタSkill | 新規Skill案、変換済みSKILL.md、レビュー結果 | 高 |
| `/legacy-source-spec-writer` | `.cline/skills/legacy-source-spec-writer/SKILL.md` | 既存ソースから現在の仕様をMarkdown化する | `docs/specs/<feature-name>.md` | 高 |
| `/unknown-list-extractor` | `.cline/skills/unknown-list-extractor/SKILL.md` | 仕様不明点、曖昧さ、前提、リスク、確認事項を抽出する | `docs/ai/unknowns/YYYYMMDD-<topic>-unknowns.md` | 高 |
| `/html-artifact-checker` | `.cline/skills/html-artifact-checker/SKILL.md` | HTML成果物が仕様・既存挙動を漏れなく反映しているか確認する | `docs/reviews/YYYYMMDD-<artifact-name>-html-check.md` | 高 |
| `/grill-with-docs` | `.cline/skills/grill-with-docs/SKILL.md` | 実装前に1問ずつ質問し、要件・用語・判断・受け入れ条件を詰める | `memory-bank/`, `docs/ai/` | 中 |
| `/implementation-loop` | `.cline/skills/implementation-loop/SKILL.md` | `memory-bank/` と `docs/ai/` を読んで最小差分で実装する | ソース差分、build/test結果、git diff確認 | 中 |
| `/review-loop` | `.cline/skills/review-loop/SKILL.md` | 現在の差分を実装せずにレビューする | リスク、テスト不足、仕様破壊、不要変更の指摘 | 中 |
| `/memory-bank-updater` | `.cline/skills/memory-bank-updater/SKILL.md` | 長期文脈を軽量に更新する | `memory-bank/*.md` | 低 |

## Skillではないが必要な領域

| 領域 | 用途 | メモ |
|---|---|---|
| `.clinerules/` | 常時守るプロジェクトルール | Skillに詰め込みすぎない |
| `memory-bank/` | 長期文脈、現在の作業状態、技術背景、進捗 | 実装前後に更新する |
| `docs/ai/` | AI作業用の用語、判断、ADR、active context | 仕様判断の根拠置き場 |
| `docs/specs/` | 既存ソースから作った仕様書 | `legacy-source-spec-writer` の主出力 |
| `docs/ai/unknowns/` | 確認が必要な不明点リスト | `unknown-list-extractor` の主出力 |
| `docs/reviews/` | HTML成果物や差分のレビュー結果 | `html-artifact-checker` の主出力 |
| `README.md` | Cline運用ルールと推奨手順の入口 | チーム共有用 |

## 推奨実行順

### 1. 既存仕様を作る

```txt
/legacy-source-spec-writer

この機能の既存ソースを調査して、docs/specs/ にMarkdown仕様書を作成してください。
コード変更はしないでください。
仕様として断定できないものは Unknown にしてください。
```

### 2. 不明点を一覧化する

```txt
/unknown-list-extractor

この仕様書と既存ソースを見て、確認が必要な不明点を docs/ai/unknowns/ に一覧化してください。
Critical / High / Medium / Low で分類してください。
```

### 3. 要件を詰める

```txt
/grill-with-docs

この機能を実装したいです。
実装はまだしないでください。
1問ずつ質問して、要件、用語、判断、スコープ、受け入れ条件を詰めてください。
決まった内容は memory-bank/ と docs/ai/ に記録してください。
```

### 4. 実装する

```txt
/implementation-loop

memory-bank/ と docs/ai/ を読んでから実装してください。
変更は最小差分にしてください。
最後に build/test と git diff の確認結果を出してください。
```

### 5. 差分をレビューする

```txt
/review-loop

現在の差分をレビューしてください。
実装はしないでください。
既存仕様破壊、テスト不足、不要な変更、リスクを確認してください。
```

### 6. HTML成果物を確認する

```txt
/html-artifact-checker

このHTML成果物が docs/specs/ の仕様を漏れなく反映できているか確認してください。
HTMLは修正せず、docs/reviews/ にレビュー結果を出してください。
```

## READMEに載せる最小説明

```md
# Cline Loop Engineering

Clineで既存ソース解析、仕様整理、実装、レビューを安全に回すためのテンプレートです。

## 構成

- `.clinerules/`: 常時有効なプロジェクトルール
- `.cline/skills/`: 必要な時だけ呼び出すCline Skills
- `memory-bank/`: 長期文脈と進捗
- `docs/ai/`: 用語、判断、ADR、AI作業ログ
- `docs/specs/`: 既存ソースから作った仕様書
- `docs/reviews/`: レビュー結果

## 基本フロー

1. `/legacy-source-spec-writer` で既存仕様を作る
2. `/unknown-list-extractor` で不明点を出す
3. `/grill-with-docs` で要件を詰める
4. `/implementation-loop` で実装する
5. `/review-loop` で差分を確認する
6. `/html-artifact-checker` でHTML成果物を確認する
```

## 運用ルール

- `.clinerules` に詰め込みすぎない
- 繰り返す作業は `.cline/skills/` に分ける
- 長期文脈は `memory-bank/` に残す
- 仕様、用語、判断は `docs/ai/` に残す
- 既存ソース由来の仕様は `docs/specs/` に残す
- 実装前に曖昧な仕様を潰す
- 実装後は必ず差分レビューする
- HTML成果物は仕様・既存挙動との対応漏れを確認する

## 導入優先順位

1. `cline-skill-builder`
2. `legacy-source-spec-writer`
3. `unknown-list-extractor`
4. `html-artifact-checker`
5. `grill-with-docs`
6. `implementation-loop`
7. `review-loop`
8. `memory-bank-updater`

