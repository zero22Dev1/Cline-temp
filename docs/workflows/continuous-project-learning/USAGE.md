# Continuous Project Learning Usage

## 概要

`/continuous-project-learning.md` は、完了した作業から検証済みの知識を抽出し、Clineのプロジェクト理解と、保守性・性能・品質を継続的に改善するWorkflowである。

AIモデル自体を再学習するものではなく、リポジトリに残す文脈、ADR、Rule、Skill、テスト、計測方法を改善する。

## 使用するタイミング

- 実装と品質確認が完了した後
- ユーザーから重要な訂正を受けた後
- 同じ失敗やレビュー指摘が繰り返された後
- 障害対応、性能改善、移行作業が完了した後
- リリース、スプリント、マイルストーンの振り返り

再利用できる学習がない小規模作業では省略できる。

## 基本的な呼び出し方

```txt
/continuous-project-learning.md

今回の実装、レビュー、品質ゲート、テスト結果から再利用可能な学習を抽出してください。
保守性、性能、品質、信頼性の観点で評価し、根拠のある内容だけを適切な保存先へ昇格してください。
```

## 使用例

### 実装後の振り返り

```txt
/continuous-project-learning.md

今回の機能追加で確定した設計、繰り返し使える実装パターン、回帰防止策を整理してください。
単発の情報や未検証の推測は保存しないでください。
```

### 性能改善後

```txt
/continuous-project-learning.md

今回の性能改善について、変更前後の測定値、測定条件、トレードオフを確認してください。
再利用できる計測方法と性能基準をtechContextまたはADRへ記録してください。
基準値がない主張は学習候補として保留してください。
```

### 障害対応後

```txt
/continuous-project-learning.md

今回の障害について、原因、検出できなかった理由、有効だった修正、再発防止策を整理してください。
可能なら回帰テスト、監視、チェックリストへ変換してください。
```

### Rule・Skillの改善候補を探す

```txt
/continuous-project-learning.md

最近繰り返した手順とレビュー指摘を確認してください。
常時適用する短い原則はRule、専門的な反復手順はSkillとして昇格候補を提示してください。
```

## 評価する品質観点

| 観点 | 内容 |
|---|---|
| Correctness | 仕様、境界値、例外、回帰 |
| Maintainability | 責務、重複、命名、依存、テスト容易性 |
| Performance | レイテンシ、CPU、メモリ、I/O、DBクエリ |
| Reliability | 再試行、冪等性、タイムアウト、復旧 |
| Security | 認証、認可、入力、秘密情報、依存関係 |
| Operability | ログ、監視、リリース、ロールバック |
| Developer Experience | build、test、lint、調査手順 |
| Domain Knowledge | 用語、業務ルール、仕様判断 |

## 主な保存先

- `docs/ai/learnings/YYYYMMDD-<topic>.md`
- `memory-bank/*.md`
- `docs/ai/glossary.md`
- `docs/ai/adr/`
- `docs/ai/unknowns/`
- `.clinerules/`
- `.cline/skills/`
- 回帰テスト、ベンチマーク、品質チェック

## 完了時の出力

- 学習候補数と品質観点
- `Promote / Keep Candidate / Reject / Replace` の結果
- 根拠、Confidence、適用範囲
- 更新ファイル
- 追加した回帰防止策
- 残るUnknownと次回の検証条件

## 注意点

- 未検証の成功や性能向上を確定事項にしない。
- 会話全文、秘密情報、個人情報、巨大なログを保存しない。
- 一度成功しただけの手順をすぐ新規Skillへ昇格しない。
- 既存RuleやSkillの意味を大きく変更する場合は、理由と影響を明示する。
- 古い知識と矛盾する場合は、単純追記ではなく置換またはUnknown化する。
