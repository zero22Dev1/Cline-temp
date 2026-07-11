# Cline-temp

clineのテンプレート。

## Cline Loop Engineering

Clineで既存ソース解析、仕様整理、実装、レビューを安全に回すためのテンプレートです。

## 構成

- `.clinerules/`: 常時有効なプロジェクトルール
- `.clinerules/workflows/`: 複数Skillを順番・条件付きで実行するCline Workflows
- `.cline/skills/`: 必要な時だけ呼び出すCline Skills
- `memory-bank/`: 長期文脈と進捗
- `docs/ai/`: 用語、判断、ADR、AI作業ログ
- `docs/specs/`: 既存ソースから作った仕様書
- `docs/reviews/`: レビュー結果
- `docs/skills-usage.md`: 各Skillの使用方法
- `docs/workflows/`: Cline Workflowごとの使用方法

## 基本フロー

1. `/adaptive-deep-planning.md` Workflowで依頼を分類し、必要な計画工程を選ぶ
2. 長時間・複雑な作業は `/context-window-management.md` で文脈を管理する
3. 選択された調査・要件整理・実装Skillを実行する
4. `/artifact-quality-gate.md` Workflowで成果物を検証する
5. `/memory-bank-updater` で長期文脈を更新する
6. 学習候補がある場合は `/continuous-project-learning.md` で再発防止へ変換する
7. Git用SkillでfeatureBranchへcommit/pushする

複数回の反復が必要な成果物では、実装から品質判定までを `/harness-engineering-loop.md` で制御します。

詳しい使い方は [docs/skills-usage.md](docs/skills-usage.md) を参照してください。
Workflowの使用例は [docs/workflows/README.md](docs/workflows/README.md) を参照してください。

## 導入済みWorkflows

| Command | Purpose |
|---|---|
| `/adaptive-deep-planning.md` | 依頼を分類し、必要な計画・調査・レビューSkillを選択 |
| `/artifact-quality-gate.md` | 成果物を分類し、品質チェック・修正ループ・完了判定を実行 |
| `/continuous-project-learning.md` | 検証済みの学習を蓄積し、保守性・性能・品質の再発防止へ変換 |
| `/harness-engineering-loop.md` | 予算・観測・評価・停止条件を持つ成果物反復ループを実行 |
| `/context-window-management.md` | 必要な根拠を段階的に読み込み、Checkpointと再構成で文脈品質を維持 |

## 導入済みSkills

| Command | Purpose |
|---|---|
| `/adaptive-deep-planning` | 要件の明確さと変更規模から必要な計画ルートを選択 |
| `/artifact-quality-gate` | 成果物を分類し、要件網羅性・正確性・追跡性・形式を品質判定 |
| `/ai-learning-curator` | 作業結果から再利用可能な学習を抽出し、memory・ADR・rule・Skillへ昇格 |
| `/harness-engineering-loop` | 成果物ループの環境、ツール、観測、制約、評価器、学習還元を設計 |
| `/context-window-manager` | 長時間作業のworking set、段階読込、圧縮、Checkpoint、引き継ぎを管理 |
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
