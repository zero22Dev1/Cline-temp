# Teams Completion Notification Workflow

Clineの計画または実装が品質確認まで完了した時だけMicrosoft Teamsへ通知する。

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

## Rules

- Webhook URLは`TEAMS_WORKFLOW_WEBHOOK_URL`からだけ取得する。
- `PASS WITH MINOR FIXES`、`NOT RUN`、`Needs Revision`、`Blocked`では通知しない。
- dry-runを通知完了として扱わない。
- TeamsがHTTP 2xxを返した場合だけ通知完了とする。
- 通知失敗時は作業結果と通知結果を分けて報告する。
- 同じ成果物と更新時刻から作るNotification IDで多重通知を識別する。
