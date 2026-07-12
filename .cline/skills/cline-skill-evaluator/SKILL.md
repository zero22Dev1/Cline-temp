---
name: cline-skill-evaluator
description: 既存のCline Skillsを変更せずに独立評価し、発見性、トリガー精度、責務境界、手順の実行可能性、安全性、検証可能性、Workflow連携、コンテキスト効率、保守性、代表シナリオでの有効性を採点する。Skill単体または`.cline/skills/`全体の品質監査、重複・競合・参照切れ・テスト不足の検出、改善優先順位の作成に使用する。
---

# Cline Skill Evaluator

Cline Skillを評価するだけのreport-only Skill。対象Skill、Workflow、Rule、script、reference、usage文書を変更しない。

詳細な採点基準は[references/evaluation-rubric.md](references/evaluation-rubric.md)を読む。

Cline固有の構造・発火・制限を評価する場合は[references/cline-official-baseline.md](references/cline-official-baseline.md)を読み、公式仕様が更新されていないか確認する。

評価を始める前に[references/evaluation-contract.md](references/evaluation-contract.md)を使い、対象Skill固有の正解を定義する。Contractを確定できない場合は採点せず`ESCALATE_HUMAN`とする。

## Responsibility Boundary

- Skill `cline-skill-evaluator`: 独立評価、採点、問題と改善案の報告のみ
- Skill `cline-skill-builder`: 承認された指摘に基づく作成・修正・分割
- Skill `loop-verifier`: 実際の作業結果に対する最終承認判定
- Skill `artifact-quality-gate`: Skill以外も含む成果物の総合品質判定

評価依頼では対象ファイルを修正しない。修正依頼が追加された場合も、評価結果を確定してから別工程としてSkill `cline-skill-builder`へ渡す。

## Evaluation Modes

### Single

指定された1つのSkillを詳しく評価する。

### Portfolio

`.cline/skills/`全体を評価し、重複、責務の空白、競合、命名、Workflow接続、共通リスクを確認する。

### Change Review

基準commitまたは変更前との差分を対象に、Skill品質の回帰を評価する。

### Forward Test

事前に固定した入力例を使い、Skillが適切に選択・実行・停止・検証できるかを新しいClineタスクまたは隔離環境で確認する。

## Inputs

- 対象`.cline/skills/<name>/SKILL.md`
- 対象Skillの`scripts/`、`references/`、`assets/`
- `.clinerules/`と`.clinerules/workflows/`
- `docs/skills-usage.md`と`docs/workflows/`
- 関連するテスト、ログ、過去の失敗、ユーザー訂正
- 比較基準または期待する利用シナリオ
- ユーザー、仕様、既存の成功例など評価器から独立した正解根拠

## Evaluation Contract Gate

評価前に次を確定する。

- `Purpose`: Skillが達成すべき1つの目的
- `Required Inputs`: 必須入力と前提
- `Expected Outputs`: 成果物、形式、保存先
- `Allowed Actions`: 許可する読取、変更、実行、外部操作
- `Forbidden Actions`: 禁止する変更、破壊操作、外部送信
- `Acceptance Criteria`: 観測可能な完了条件
- `Oracle`: 合否を決めるユーザー決定、仕様、テスト、schema、既存成果物
- `Fixtures`: 固定した正常、境界、異常、非対象シナリオ
- `Evidence`: 必須ログ、diff、test結果、activation記録

評価器自身が目的、期待結果、Actualを同時に作らない。正解根拠が存在しない項目は`Unknown`、人間判断が必要なら`ESCALATE_HUMAN`とする。

## Process

### 1. Inventory

対象範囲を確定し、次を機械的に確認する。

- ディレクトリ名とfrontmatterの`name`が一致
- `name`と`description`が存在
- `name`がlowercase kebab-case
- `description`が1024文字以内
- `SKILL.md`本文が5k tokens未満
- 参照ファイルとscriptが存在
- usage、Rule、Workflowからの参照が有効
- scriptに構文チェックまたはテストがある
- 生成物、秘密情報、キャッシュが誤ってSkillへ含まれていない
- 対象SkillがClineで有効になっている
- 同名Global SkillがWorkspace Skillを上書きしていない

token数を測定できない場合は推測値でPASSにせず`NOT RUN`とする。

### 2. Trigger Evaluation

descriptionだけを読む静的確認と、実際のCline activation確認を分ける。

- 何をするSkillか判別できる
- いつ使用するかが具体的
- 類似Skillとの選択条件が分かる
- 広すぎて常時発火しない
- 狭すぎて必要時に発見されない

Evaluation Contractで、最低3つの`Should Trigger`と3つの`Should Not Trigger`fixtureを評価前に固定する。期待値はユーザー、仕様、Skill所有者、既存成功例のいずれかを根拠にし、評価器が実行後に書き換えない。

各fixtureを生成時の会話や意図を含まない新しいClineタスクで実行し、`use_skill`による実際のactivationを観測する。

- 期待どおり発火: `PASS`
- 期待どおり非発火: `PASS`
- 誤発火または未発火: `FAIL`
- 新しいClineタスクで観測不能: `NOT RUN`

activationを観測していない場合、`Discovery And Triggering`は満点不可かつ最終Decisionは最大`NEEDS_REVISION`とする。

### 3. Instruction Evaluation

- 入力、出力、手順、停止条件、完了条件が明確
- 手順が実際のツール・ファイル構成で実行可能
- 不明点を推測しない
- 変更禁止、report-only、承認点などの境界が明確
- 正常系だけでなく失敗、再試行、外部ブロッカーを扱う
- 既存Skillと矛盾または無限呼び出しを起こさない

### 4. Progressive Disclosure

- `SKILL.md`に中核手順だけがある
- 詳細資料は必要時に読むreferenceへ分離
- referenceが深くネストしていない
- 同じ説明をRule、Skill、usageへ重複保存していない
- 大量コンテキストを目的なく要求しない

### 5. Safety And Integrity

- destructive操作、Git push、本番変更、秘密情報、外部送信の安全条件
- テストや閾値の弱体化を成功条件にしていない
- 検証不能をPASSにしない
- ユーザー変更やテンプレート原本を保護する
- report-only Skillがファイルを変更しない
- scriptの入力検証、上書き、path、リソース解放、失敗時の原子性

### 6. Evidence And Tests

自己説明ではなく、次の証拠を確認する。

- YAML・構文検証
- 参照切れ検査
- script単体テスト
- 正常、境界、異常、安全性テスト
- 代表シナリオのdry-run
- 新しいClineタスクでのactivation記録
- 実成果物または過去実行ログ

実行できない項目は`NOT RUN`と理由を記録する。

### 7. Portfolio Analysis

複数Skillを評価する場合は次も確認する。

- 重複する責務
- どのSkillにも属さない責務
- 親Skillと個別Skillの境界
- Workflowから呼ばれない孤立Skill
- 相互参照ループ
- 同じ用語や判定値の不一致
- builder、evaluator、verifierの職務分離

### 8. Independent Evaluation

評価は可能な限り、対象Skillの生成会話、作成者の結論、想定点数を渡さない新しいClineタスクで行う。Evaluatorへ渡すのはEvaluation Contract、対象の生ファイル、固定fixture、実行結果だけとする。

同じ担当・同じ会話内で評価する場合は`Independent: No`と明記し、最終Decisionは最大`NEEDS_REVISION`とする。

### 9. Score And Decision

ルーブリックに従い100点で採点する。証拠がない項目へ満点を与えない。

- `90-100`: `APPROVE`
- `80-89`: `APPROVE_WITH_MINOR_FINDINGS`
- `60-79`: `NEEDS_REVISION`
- `0-59`: `REJECT`
- 人間の業務判断が必要: `ESCALATE_HUMAN`

点数に加えてSeverity Gateを適用する。

- Criticalが1つ以上: `REJECT`
- Majorが1つ以上: 最大`NEEDS_REVISION`
- Minorが1つ以上: 最大`APPROVE_WITH_MINOR_FINDINGS`
- `APPROVE`: Critical、Major、Minorがなく、必須検証がすべてPASS
- 人間の正解判断が必要: `ESCALATE_HUMAN`

点数とSeverity Gateで判定が異なる場合は、より厳しいDecisionを採用する。

## Finding Rules

指摘は、対象Skillの利用者または作成者が修正する可能性が高い、具体的で再現可能な問題だけを出す。

```md
| ID | Severity | Skill | Location | Evidence | Impact | Recommendation |
|---|---|---|---|---|---|---|
```

Severity:

- `Critical`: 危険な操作、データ損失、秘密漏えい、主要目的を実行不能
- `Major`: 誤発火、重要手順欠落、検証不能、重大な責務競合
- `Minor`: 限定条件での不明確さ、テスト不足、保守性低下
- `Suggestion`: 必須ではない改善

推測だけの指摘や好みの問題は出さない。

## Output

単体評価:

```txt
docs/reviews/YYYYMMDD-<skill-name>-skill-evaluation.md
```

全体評価:

```txt
docs/reviews/YYYYMMDD-cline-skills-portfolio-evaluation.md
```

レポートには次を含める。

- 対象と評価モード
- Evaluation ContractとOracle
- 実行した検査と証拠
- 採点内訳
- Triggerシナリオ結果
- Findings
- Skill間の重複・空白・競合
- 未実行検証と残存リスク
- `Independent: Yes / No`
- Decision
- 修正する場合の優先順位

## Prohibitions

- 評価中に対象Skillを修正しない。
- 対象Skillの自己評価を証拠にしない。
- テスト未実行をPASSとして扱わない。
- 点数だけを出して根拠を省略しない。
- 全Skillへ同じ改善を機械的に要求しない。
- 実行を伴うForward Testで破壊的操作、push、本番変更、外部送信を行わない。
