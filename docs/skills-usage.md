# Cline Skills Usage

このドキュメントは、このリポジトリに入っている各Cline Skillの使い方をまとめたものです。

基本的には、Clineのチャット入力で `/` を入力し、対象Skillを選んでから依頼文を続けます。

## 基本フロー

```txt
/legacy-source-spec-writer
  ↓
/unknown-list-extractor
  ↓
/daily-triage
  ↓
/issue-triage
  ↓
/grill-with-docs
  ↓
/implementation-loop
  ↓
/review-loop
  ↓
/html-artifact-checker
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
