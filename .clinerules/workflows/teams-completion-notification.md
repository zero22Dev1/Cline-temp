# Teams Completion Notification Workflow

Clineの計画または実装が品質確認まで完了した時だけMicrosoft Teamsへ通知する。

## Notification Choice

Workflow開始時に次を選択する。

- `有効`: 今回のWorkflowが完了条件を満たした場合だけTeamsへ通知する
- `無効`: Teamsへ通知しない

ユーザーが選択していない場合は`無効`とする。選択は今回の実行だけに適用し、次回へ引き継がない。`有効`の場合だけ以降の通知処理を実行する。

## Mode: Plan

1. `/adaptive-deep-planning.md`で計画を作成する。
2. 計画をSkill `review-loop`でレビューする。
3. 計画成果物を`/artifact-quality-gate.md`で検証する。
4. Plan Reviewが`Ready`または`Ready with Assumptions`、Quality Gateが`PASS`、Blocking Questionなしであることを確認する。
5. Skill `teams-completion-notifier`を`plan`モードで実行する。

## Mode: Implementation

1. 承認済み計画からSkill `implementation-loop`でコードと必要なテストコードを実装する。
2. 必須のbuild、lint、testを実行する。
3. Skill `review-loop`で差分をレビューし、Critical／Majorを解消する。
4. `/artifact-quality-gate.md`を実行する。
5. Skill `loop-verifier`が`APPROVE`であることを確認する。
6. すべてPASSの場合だけSkill `teams-completion-notifier`を`implementation`モードで実行する。

## Mode: Workflow

1. 呼び出し元Workflow固有の完了条件を確認する。
2. 必要な成果物を`/artifact-quality-gate.md`で検証する。
3. Skill `loop-verifier`が`APPROVE`であることを確認する。
4. 必須検証の`NOT RUN`、Blocking事項、Critical／Majorがないことを確認する。
5. すべてPASSの場合だけSkill `teams-completion-notifier`を`workflow`モードで実行する。

## Rules

- Webhook URLは`TEAMS_WORKFLOW_WEBHOOK_URL`からだけ取得する。
- Python実行時に`--notification-choice enabled`を渡す。`disabled`では送信しない。
- `PASS WITH MINOR FIXES`、`NOT RUN`、`Needs Revision`、`Blocked`では通知しない。
- dry-runを通知完了として扱わない。
- TeamsがHTTP 2xxを返した場合だけ通知完了とする。
- 通知失敗時は作業結果と通知結果を分けて報告する。
- 同じ成果物と更新時刻から作るNotification IDで多重通知を識別する。
