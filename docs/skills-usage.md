# Cline Skills Usage

このドキュメントは、このリポジトリに入っている各Cline Skillの使い方をまとめたものです。

基本的には、Clineのチャット入力で `/` を入力し、対象Skillを選んでから依頼文を続けます。

`.clinerules/workflows/` のWorkflowは複数Skillを条件付きでつなぐ入口です。Workflowは `/ファイル名.md` で実行し、同名の親Skillが判定基準と詳細手順を提供します。

Workflowごとの使用例は [workflows/README.md](workflows/README.md) を参照してください。

## 基本フロー

```txt
/adaptive-deep-planning.md
  ↓
/context-window-management.md（長時間・複雑な場合）
  ↓
選択された調査・要件整理・実装Skill
  ↓
/review-loop
  ↓
/artifact-quality-gate.md
  ↓
/loop-verifier
  ↓
/memory-bank-updater
  ↓
/template-commit-workflow
  ↓
/git-commit-workflow
```

## Skill一覧

| Skill | 用途 | 主な出力 |
|---|---|---|
| `/adaptive-deep-planning` | 依頼を分類して必要な計画ルートとSkillを選ぶ | `docs/planning/`、選択ルート、次のアクション |
| `/artifact-quality-gate` | 生成成果物を分類して品質判定する | `docs/quality/artifact-quality-report.md` |
| `/ai-learning-curator` | 作業から再利用可能な学習を抽出・評価・昇格する | `docs/ai/learnings/`、`memory-bank/`、ADR、rule、Skill |
| `/harness-engineering-loop` | 成果物反復の環境・観測・評価・予算・学習を設計する | Loop contract、iteration log、harness improvements |
| `/context-window-manager` | 長時間作業の文脈を選別、段階読込、Checkpoint、再構成する | Context Contract、Context Checkpoint、handoff packet |
| `/cline-skill-builder` | Cline Skillの作成・変換・改善・レビュー | `.cline/skills/<name>/SKILL.md` |
| `/legacy-source-spec-writer` | 既存ソースから仕様書を作る | `docs/specs/<feature-name>.md` |
| `/unknown-list-extractor` | 不明点・確認事項を抽出する | `docs/ai/unknowns/YYYYMMDD-<topic>-unknowns.md` |
| `/grill-with-docs` | 実装前に要件を詰める | `memory-bank/`, `docs/ai/`, `docs/specs/` |
| `/implementation-loop` | 仕様と文脈を読んで実装する | ソース差分、テスト結果 |
| `/review-loop` | 実装せずに差分レビューする | 指摘、リスク、テスト不足 |
| `/html-artifact-checker` | HTML成果物の仕様反映漏れを確認する | `docs/reviews/YYYYMMDD-<artifact-name>-html-check.md` |
| `/loop-budget` | ループの予算・停止条件・検証条件を管理する | Loop budget / run log |
| `/loop-triage` | 複数の問題や候補を優先度順に整理する | 優先度付きnext action |
| `/loop-verifier` | 完了した作業を独立検証する | `APPROVE` / `REJECT` / `ESCALATE_HUMAN` |
| `/daily-triage` | CI、Issue、PR、commit、unknownを日次・定期で整理する | `docs/ai/triage/YYYYMMDD-daily-triage.md` |
| `/issue-triage` | Issueやfeature requestを優先度・label案つきで整理する | `docs/ai/triage/YYYYMMDD-issue-triage.md` |
| `/memory-bank-updater` | 長期文脈と進捗を更新する | `memory-bank/*.md` |
| `/template-commit-workflow` | Clineテンプレート変更をfeatureBranchでcommit/pushする | `feature#template#<number>` branch |
| `/git-commit-workflow` | featureBranchでcommit/pushする | `feature#<name>#<number>` branch |

## Workflow一覧

| Workflow | 配置 | 呼び出す主なSkill |
|---|---|---|
| `/adaptive-deep-planning.md` | `.clinerules/workflows/adaptive-deep-planning.md` | `grill-with-docs`、`unknown-list-extractor`、`legacy-source-spec-writer`、`review-loop`、`implementation-loop` |
| `/artifact-quality-gate.md` | `.clinerules/workflows/artifact-quality-gate.md` | `html-artifact-checker`、`review-loop`、`loop-verifier`、`implementation-loop`、`memory-bank-updater` |
| `/continuous-project-learning.md` | `.clinerules/workflows/continuous-project-learning.md` | `ai-learning-curator`、`memory-bank-updater`、`cline-skill-builder` |
| `/harness-engineering-loop.md` | `.clinerules/workflows/harness-engineering-loop.md` | `harness-engineering-loop`、`loop-budget`、`artifact-quality-gate`、`loop-verifier` |
| `/context-window-management.md` | `.clinerules/workflows/context-window-management.md` | `context-window-manager`、`memory-bank-updater`、`artifact-quality-gate`、`loop-verifier` |

## `/context-window-manager`

### 使うタイミング

- 長時間、複数モジュール、複数Skillの作業を行う
- 会話、ログ、調査結果が増え、古い前提が混ざりそう
- 作業を再開・引き継ぎする
- 同じ情報を再検索する、判断根拠を追えないなどの兆候がある

### 使用例

```txt
/context-window-management.md

最新の依頼からContext Contractを作成してください。
必要な資料だけを段階的に読み、工程境界で根拠付きCheckpointを更新してください。
圧縮後は正本とGit差分と検証結果を再確認してください。
```

### 期待する出力

- Context Contract
- 文脈の選別結果
- 根拠パス付きContext Checkpoint
- Unknown、矛盾、次の1アクション
- 再開・引き継ぎ用パケット

## `/adaptive-deep-planning`

### 使うタイミング

- 依頼が曖昧、または変更規模がまだ分からない
- 複数ファイル・複数層に影響する機能開発や移行を計画したい
- 既存の計画やタスクを再利用し、必要な工程だけ実行したい

### 使用例

```txt
/adaptive-deep-planning

この機能追加について、要件の明確さと変更規模を分類してください。
必要な調査・要件整理・計画・タスク分割だけを実行し、計画承認前は実装しないでください。
```

### 期待する出力

- 要件の明確さと変更規模
- 選択ルートとスキップ理由
- 必要な `docs/planning/` の成果物
- 仮定、Unknown、Blocking Question、次のアクション

## `/artifact-quality-gate`

### 使うタイミング

- Markdown、HTML、Excel、YAML、SQL、コード、テスト、図の完成判定をしたい
- 要件網羅性、既存仕様との整合、根拠、構文、自動テストをまとめて確認したい
- 問題を限定修正して再チェックしたい

### 使用例

```txt
/artifact-quality-gate

今回生成した成果物を分類し、要件対応表と自動検証結果を含む品質レポートを作成してください。
CriticalまたはMajorが残る場合は完了扱いにしないでください。
```

### 期待する出力

```txt
docs/quality/artifact-quality-report.md
Quality Gate: PASS | PASS WITH MINOR FIXES | NEEDS REVISION | FAIL
```

## `/ai-learning-curator`

### 使うタイミング

- 作業後に、次回も使える判断や手順を残したい
- 同じ失敗やユーザーからの訂正が繰り返された
- 新しいルールやSkillへ昇格すべき知識を整理したい
- memory-bank、用語集、ADR、ルールの内容が古くなっていないか確認したい

### 使用例

```txt
/ai-learning-curator

今回の実装、レビュー、テスト結果、ユーザーからの訂正を振り返ってください。
再利用できる学習だけを抽出し、根拠、Confidence、適用範囲、保存先を評価してください。
未検証の内容はルールやSkillへ昇格しないでください。
```

### 期待する出力

- 学習候補の評価表
- `Promote / Keep Candidate / Reject / Replace` の判定
- `docs/ai/learnings/YYYYMMDD-<topic>.md`
- 必要な `memory-bank/`、用語集、ADR、`.clinerules/`、Skillの更新
- 次回の検証条件

### `memory-bank-updater`との違い

- `/memory-bank-updater`: 現在の文脈、進捗、技術情報を整理する
- `/ai-learning-curator`: 作業結果を評価し、将来も再利用できる知識だけを昇格させる

## `/harness-engineering-loop`

### 使うタイミング

- 成果物を複数回のループで完成させたい
- 同じ失敗が繰り返され、環境や検証方法の改善が必要
- 反復回数、時間、停止条件を管理したい
- 性能や信頼性を計測しながら改善したい

### 使用例

```txt
/harness-engineering-loop.md

この成果物を最大3イテレーションで完成させてください。
各回で最優先の未達項目を1つだけ修正し、観測結果と品質判定を記録してください。
同じ失敗が続く場合は実装を再試行せず、不足しているハーネスを改善してください。
```

### 期待する出力

- Loop contractと予算
- イテレーション記録
- build、test、品質・性能の観測結果
- 失敗のGap分類
- 改善した環境、文脈、ツール、観測、制約、評価器
- 品質ゲートと独立検証の最終判定
- 継続学習へ渡す内容

## `/cline-skill-builder`

### 使うタイミング

- 新しいCline Skillを作りたい
- Claude/Cursor/Codex向けのSkillやルールをCline向けに変換したい
- 既存Skillの責務が広すぎないか確認したい
- `.clinerules` に入れすぎた内容をSkillへ分割したい

### 使用例

```txt
/cline-skill-builder

Gitのcommitとpushを安全に行うCline Skillを作成してください。
原則としてmainへ直接pushせず、feature#na#1 のようなfeatureBranchを作成して、
local featureBranchからremote featureBranchへpushする運用にしてください。
```

### 期待する出力

- 推奨配置
- `SKILL.md`
- 呼び出し例
- 他Skillとの責務の違い

## `/legacy-source-spec-writer`

### 使うタイミング

- 既存ソースから現在の仕様をMarkdown化したい
- リファクタや移行前に現行挙動を把握したい
- 古いコードの業務ロジックを文書化したい

### 使用例

```txt
/legacy-source-spec-writer

この機能の既存ソースを調査して、docs/specs/ にMarkdown仕様書を作成してください。
コード変更はしないでください。
仕様として断定できないものは Unknown にしてください。
```

### 期待する出力

```txt
docs/specs/<feature-name>.md
```

## `/unknown-list-extractor`

### 使うタイミング

- 仕様不明点を一覧化したい
- 実装前に確認事項を洗い出したい
- 既存仕様とソースの差分や曖昧さを確認したい

### 使用例

```txt
/unknown-list-extractor

この仕様書と既存ソースを見て、確認が必要な不明点を docs/ai/unknowns/ に一覧化してください。
Critical / High / Medium / Low で分類してください。
```

### 期待する出力

```txt
docs/ai/unknowns/YYYYMMDD-<topic>-unknowns.md
```

## `/grill-with-docs`

### 使うタイミング

- 実装前に要件を詰めたい
- 用語、判断、スコープ、受け入れ条件が曖昧
- 1問ずつ確認しながら仕様を固めたい

### 使用例

```txt
/grill-with-docs

この機能を実装したいです。
実装はまだしないでください。
1問ずつ質問して、要件、用語、判断、スコープ、受け入れ条件を詰めてください。
決まった内容は memory-bank/ と docs/ai/ に記録してください。
```

### 期待する出力

- `memory-bank/activeContext.md`
- `docs/ai/active-context.md`
- `docs/ai/glossary.md`
- `docs/specs/<feature-name>.md`
- 未解決なら `docs/ai/unknowns/`

## `/daily-triage`

### 使うタイミング

- 朝や作業開始時に、何を見るべきか整理したい
- CI、Issue、PR、commit、unknownをまとめて確認したい
- 自動修正はせず、report-onlyで優先順位だけ出したい

### 使用例

```txt
/daily-triage

現在のCI、Issue、PR、最近のcommit、docs/ai/unknowns、memory-bankを見て、
今日見るべきものをCritical / High / Medium / Lowに整理してください。
自動修正やlabel変更はしないでください。
```

### 期待する出力

```txt
docs/ai/triage/YYYYMMDD-daily-triage.md
```

## `/issue-triage`

### 使うタイミング

- Issueやfeature requestを整理したい
- 重複候補、優先度、label案、needs-infoを出したい
- Issue queueをきれいにしたいが、まだ自動label/closeはしたくない

### 使用例

```txt
/issue-triage

このIssue一覧を整理してください。
P0/P1/P2/P3、needs-info、possible duplicate、suggested labelsを出してください。
label適用やcloseはしないでください。
```

### 期待する出力

```txt
docs/ai/triage/YYYYMMDD-issue-triage.md
```

## `/implementation-loop`

### 使うタイミング

- 要件や仕様が固まった後に実装したい
- `memory-bank/` や `docs/ai/` を読んだうえで最小差分で変更したい
- 実装後にbuild/test/diff確認まで行いたい

### 使用例

```txt
/implementation-loop

memory-bank/ と docs/ai/ と docs/specs/ を読んでから実装してください。
変更は最小差分にしてください。
最後に build/test と git diff の確認結果を出してください。
```

### 期待する出力

- 変更ファイルの要約
- 実行した検証コマンド
- 残リスク
- 必要なら `memory-bank/progress.md` 更新

## `/review-loop`

### 使うタイミング

- 現在の差分をレビューしたい
- 実装はせず、リスクやバグだけ見つけたい
- 仕様破壊、テスト不足、不要変更を確認したい

### 使用例

```txt
/review-loop

現在の差分をレビューしてください。
実装はしないでください。
既存仕様破壊、テスト不足、不要な変更、リスクを確認してください。
```

### 期待する出力

- 重大度順の指摘
- ファイルパスと根拠
- テスト不足
- 未解決の確認事項

## `/html-artifact-checker`

### 使うタイミング

- 生成したHTML成果物が仕様を漏れなく反映しているか確認したい
- HTMLモック、HTMLドキュメント、納品物をレビューしたい
- フィールド、バリデーション、エラー、分岐、例外ケースの抜けを見たい

### 使用例

```txt
/html-artifact-checker

このHTML成果物が docs/specs/ の仕様を漏れなく反映できているか確認してください。
HTMLは修正せず、docs/reviews/ にレビュー結果を出してください。
```

### 期待する出力

```txt
docs/reviews/YYYYMMDD-<artifact-name>-html-check.md
```

## `/memory-bank-updater`

### 使うタイミング

- 作業後に長期文脈を更新したい
- 次回作業に引き継ぎたい決定や進捗がある
- `memory-bank/activeContext.md` や `progress.md` を最新化したい

### 使用例

```txt
/memory-bank-updater

今回の作業内容を memory-bank に反映してください。
現在の焦点、完了したこと、次にやることを更新してください。
```

### 期待する出力

```txt
memory-bank/projectbrief.md
memory-bank/activeContext.md
memory-bank/techContext.md
memory-bank/progress.md
```

## `/loop-budget`

### 使うタイミング

- 作業が複数ステップになりそう
- 何回まで試すか、どこで止めるかを決めたい
- 検証条件やrun logを明示したい

### 使用例

```txt
/loop-budget

この実装作業の予算を作ってください。
最大3イテレーション、テスト実行必須、仕様が曖昧なら停止する条件にしてください。
```

### 期待する出力

- Goal
- Scope
- Budget
- Stop Conditions
- Verification Gates
- Run Log

## `/loop-triage`

### 使うタイミング

- Issue、CI失敗、レビュー指摘、不明点が複数ある
- 何から着手するべきか決めたい
- 実装前に優先順位を整理したい

### 使用例

```txt
/loop-triage

このCI失敗ログとレビュー指摘を見て、Critical / High / Medium / Low に分類してください。
Do now / Defer / Escalate / Drop も付けて、次に実行すべきSkillを提案してください。
```

### 期待する出力

- Prioritized Items
- Escalations
- Unknowns
- Recommended Next Loop

## `/loop-verifier`

### 使うタイミング

- 実装やドキュメント更新が完了した後
- commit/push前に独立検証したい
- 通常レビューではなく、承認判断がほしい

### 使用例

```txt
/loop-verifier

今回の変更が目的を満たしているか独立検証してください。
APPROVE / REJECT / ESCALATE_HUMAN のいずれかで判断してください。
```

### 期待する出力

```txt
Decision: APPROVE | REJECT | ESCALATE_HUMAN
```

## `/template-commit-workflow`

### 使うタイミング

- `.cline/skills/` にSkillを追加・更新した
- `.clinerules/`、README、docs、memory-bankを更新した
- Clineテンプレートそのものの変更をGitにcommit/pushしたい
- アプリケーションコードではなく、テンプレート構成だけを安全にpushしたい

### branch命名

```txt
feature#template#<number>
```

例:

```txt
feature#template#1
feature#template#2
docs#template#1
```

### 使用例

```txt
/template-commit-workflow

今回のClineテンプレート変更を feature#template#1 にcommitして、
同名のremote featureBranchへpushしてください。
mainには直接pushしないでください。
```

### 期待する動き

```txt
git status -sb
git switch -c feature#template#1
git diff
git add .cline/skills/<skill>/SKILL.md .clinerules/... README.md docs/... memory-bank/...
git commit -m "add cline template skills"
git push -u origin feature#template#1
```

### 注意点

- template対象外のアプリケーションコードは含めない
- secretsやローカル設定は含めない
- `git add -A` は原則使わない
- force pushしない
- READMEと `docs/skills-usage.md` の更新漏れを確認する

## `/git-commit-workflow`

### 使うタイミング

- 変更内容をfeatureBranchにcommitしたい
- local featureBranchからremote featureBranchへpushしたい
- `main` に直接commit/pushせず、安全にGit運用したい

### branch命名

基本形式:

```txt
feature#<name>#<number>
```

例:

```txt
feature#na#1
feature#na#2
fix#login#1
docs#cline-rules#1
```

`<number>` は同じ `<name>` 内での連番です。

### 使用例

```txt
/git-commit-workflow

今回の変更を feature#na#1 にcommitして、同名のremote featureBranchへpushしてください。
mainには直接pushしないでください。
```

### 期待する動き

```txt
git status -sb
git switch -c feature#na#1
git diff
git add <intended-files>
git commit -m "<message>"
git push -u origin feature#na#1
```

### 注意点

- unrelated changesは勝手にstageしない
- `git add -A` は原則使わない
- `main` へ直接pushしない
- force pushしない
- 認証エラーやpush拒否は隠さず報告する
