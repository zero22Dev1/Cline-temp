# Continuous Project Learning Workflow

検証済みの作業結果から再利用可能な知識を抽出し、Clineのプロジェクト理解と、コードの保守性・性能・品質を継続的に改善する。

## Workflow Rules

- AIモデル自体を再学習するWorkflowではない。リポジトリ内の文脈、判断、ルール、Skillを改善する。
- 会話全文や一時的な情報を保存しない。
- 根拠のない成功・失敗を学習として昇格しない。
- 性能改善は計測結果を伴う場合だけ確定事項にする。
- 既存ルールやSkillを無断で大幅変更しない。
- ユーザーへの説明と出力は日本語で行う。

## Step 1: 学習元を収集する

今回の作業に存在するものだけを確認する。

- ユーザーからの訂正、承認、明示的な好み
- 実装差分と `git diff`
- build、lint、test、型検査、静的解析の結果
- `/review-loop`、`/loop-verifier`、`/artifact-quality-gate.md` の結果
- 障害、失敗、再試行と有効だった修正
- 性能測定、プロファイル、クエリ計画、処理時間、メモリ使用量
- 運用上の問題、ログ、再現手順、ロールバック結果

秘密情報、個人情報、巨大なログは取り込まない。

## Step 2: 改善観点で分類する

- `Correctness`: 仕様、境界値、例外、回帰
- `Maintainability`: 責務、重複、命名、依存、テスト容易性
- `Performance`: レイテンシ、スループット、CPU、メモリ、I/O、DBクエリ
- `Reliability`: 再試行、冪等性、タイムアウト、障害復旧、監視
- `Security`: 認証、認可、入力検証、秘密情報、依存関係
- `Operability`: ログ、メトリクス、リリース、ロールバック、手順
- `Developer Experience`: build、test、lint、ローカル実行、調査手順
- `Domain Knowledge`: 用語、業務ルール、仕様判断

## Step 3: `ai-learning-curator`で評価する

Skill `ai-learning-curator` を使用し、各候補へConfidence、Scope、Action、Evidence、Destinationを付ける。

性能候補には、変更前後の測定値、測定条件、改善率または悪化率、正確性や保守性とのトレードオフを記録する。基準値がない性能主張は `Keep Candidate` とする。

## Step 4: 保存先へ昇格する

`High`かつ低リスクの候補だけを反映する。

- 作業状態: `memory-bank/activeContext.md`
- 完了・検証状態: `memory-bank/progress.md`
- 技術構成、コマンド、性能基準: `memory-bank/techContext.md`
- 用語: `docs/ai/glossary.md`
- 設計・性能・運用判断: `docs/ai/adr/`
- 未確定事項: `docs/ai/unknowns/`
- 評価記録: `docs/ai/learnings/YYYYMMDD-<topic>.md`
- 常時有効な短い原則: `.clinerules/`
- 繰り返し利用する専門手順: `.cline/skills/`

Skillを新規作成・変更する場合は `/cline-skill-builder` を使用する。

## Step 5: 退行防止へ変換する

- 再現した不具合: 回帰テスト
- 性能問題: ベンチマーク、閾値、計測手順
- 構文・形式問題: lint、schema、validator
- 運用事故: チェックリスト、監視、アラート、ロールバック手順
- 繰り返すレビュー指摘: RuleまたはSkill
- 設計判断: ADRと見直し条件

新しい検証を追加した場合は実際に実行し、動作を確認する。

## Step 6: 矛盾と陳腐化を整理する

- 新しい確定事項が古い内容を置き換える場合は古い記述を更新する。
- 未解決の矛盾は `Unknown` として残す。
- 一時的な回避策には期限または見直し条件を付ける。
- 使用されないRuleやSkillは削除候補として報告し、無断削除しない。

## Step 7: Learning Quality Gate

- 根拠を追跡できる
- 再利用場面を説明できる
- 適用範囲が広すぎない
- 既存仕様、Rule、Skillと矛盾しない
- 未検証の性能・品質主張を確定事項にしていない
- 秘密情報、個人情報、巨大なログを含まない
- 保存先が適切で重複していない

満たさない候補は昇格せず、保留または却下する。

## Step 8: Final Learning Report

- 収集した学習候補数と観点別件数
- 昇格、保留、却下、置換した項目
- 更新ファイル
- 追加した回帰テスト、性能測定、品質チェック
- 残るUnknownと次回の検証条件

## 推奨実行タイミング

- `/artifact-quality-gate.md` がPASSした後
- `/harness-engineering-loop.md` が完了または重要な失敗パターンを発見した後
- ユーザーから重要な訂正を受けた後
- 同じ失敗が2回以上発生した後
- 障害対応、性能改善、移行作業の完了後
- リリースまたはスプリントの振り返り時

再利用可能な学習がない小規模作業ではスキップしてよい。
