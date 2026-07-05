# Cline-temp

clineのテンプレート。

## Cline Loop Engineering

Clineで既存ソース解析、仕様整理、実装、レビューを安全に回すためのテンプレートです。

## 構成

- `.clinerules/`: 常時有効なプロジェクトルール
- `.cline/skills/`: 必要な時だけ呼び出すCline Skills
- `memory-bank/`: 長期文脈と進捗
- `docs/ai/`: 用語、判断、ADR、AI作業ログ
- `docs/specs/`: 既存ソースから作った仕様書
- `docs/reviews/`: レビュー結果
- `docs/skills-usage.md`: 各Skillの使用方法

## 基本フロー

1. `/legacy-source-spec-writer` で既存仕様を作る
2. `/unknown-list-extractor` で不明点を出す
3. `/grill-with-docs` で要件を詰める
4. `/implementation-loop` で実装する
5. `/review-loop` で差分を確認する
6. `/html-artifact-checker` でHTML成果物を確認する

詳しい使い方は [docs/skills-usage.md](docs/skills-usage.md) を参照してください。

## 導入済みSkills

| Command | Purpose |
|---|---|
| `/cline-skill-builder` | Cline用Skillの作成・変換・改善・レビュー |
| `/legacy-source-spec-writer` | 既存ソースからMarkdown仕様書を作成 |
| `/unknown-list-extractor` | 不明点、曖昧さ、前提、リスク、確認事項を抽出 |
| `/html-artifact-checker` | HTML成果物の仕様反映漏れを確認 |
| `/git-commit-workflow` | `feature#na#1` のようなローカルfeatureBranchを作成し、同名remote featureBranchへcommit/push |
| `/loop-budget` | ループの回数・時間・検証・停止条件を管理 |
| `/loop-triage` | Issue、CI失敗、unknown、レビュー指摘を優先度順に整理 |
| `/loop-verifier` | 完了した作業を独立検証し、APPROVE / REJECT / ESCALATE_HUMAN を返す |
| `/daily-triage` | CI、Issue、PR、commit、unknownを日次・定期でreport-only整理 |
| `/issue-triage` | Issueやfeature requestを重複・優先度・label案つきで整理 |
| `/template-commit-workflow` | Clineテンプレート変更を `feature#template#<number>` でcommit/push |

## 運用ルール

- `.clinerules` に詰め込みすぎない
- 繰り返す作業は `.cline/skills/` に分ける
- 長期文脈は `memory-bank/` に残す
- 仕様、用語、判断は `docs/ai/` に残す
- 既存ソース由来の仕様は `docs/specs/` に残す
- 実装前に曖昧な仕様を潰す
- 実装後は必ず差分レビューする
- HTML成果物は仕様・既存挙動との対応漏れを確認する
