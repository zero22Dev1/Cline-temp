---
name: teams-completion-notifier
description: Clineの計画モードまたは実行モードが品質ゲートまで完了した時に、Microsoft Teams Workflows webhookへ完了通知を送る。計画作成とPlan Review完了、またはコード実装・テスト・レビュー・品質確認完了をTeamsへ通知し、未完了や失敗状態で誤通知しないために使用する。
---

# Teams Completion Notifier

作業開始や生成直後ではなく、定義済みの完了ゲートをすべて通過した時だけTeamsへ通知する。旧Office 365 Connectorではなく、Teams Workflowsの`When a Teams webhook request is received`で発行したURLを使用する。

## Opt-in Contract

- Workflow開始時に`Teams通知: 有効 / 無効`を選択する。
- ユーザーが明示しない場合は`無効`とする。
- `有効`を選択した現在のWorkflow実行だけを通知対象にする。次回へ暗黙に引き継がない。
- Python実行時も`--notification-choice enabled`を必須とし、Workflow側の選択だけに依存しない。
- `無効`の場合は通知Skillを呼び出さず、Teams未通知を正常な完了として扱う。

## Secrets Contract

- Webhook URLは環境変数`TEAMS_WORKFLOW_WEBHOOK_URL`からだけ読む。
- URLを`.env`、Rule、Skill、ログ、通知証跡、Gitへ保存しない。
- 通知本文へソースコード、秘密情報、生ログ、個人情報を含めない。

## Completion Gates

### Plan Mode

次をすべて満たす場合だけ通知する。

- 計画成果物が存在する
- Plan Reviewが`Ready`または`Ready with Assumptions`
- 計画成果物のQuality Gateが`PASS`
- Blocking Questionがない

### Implementation Mode

次をすべて満たす場合だけ通知する。

- 対象コードの実装が完了
- 必要なテストコードが作成または更新済み
- build、lint、testなど必須検証が`PASS`
- Skill `review-loop`のCritical／Major指摘が解消済み
- `/artifact-quality-gate.md`が`PASS`
- Skill `loop-verifier`が`APPROVE`

`PASS WITH MINOR FIXES`、`NOT RUN`、未解決Critical／Majorは通知条件を満たさない。

### Workflow Mode

PDF、XLSM、Harness、Context、Learningなど、計画・コード実装以外のWorkflowで使用する。

- 対象Workflow固有の完了条件をすべて満たす
- 必要な成果物品質ゲートが`PASS`
- Skill `loop-verifier`が`APPROVE`
- 未実行の必須検証、Blocking事項、Critical／Majorがない

## Command

計画完了:

```bash
python3 .cline/skills/teams-completion-notifier/scripts/notify_teams.py \
  --mode plan \
  --notification-choice enabled \
  --title "認証機能の実装計画" \
  --summary "計画作成と品質確認が完了" \
  --plan-review Ready \
  --quality-result PASS \
  --evidence docs/planning/implementation-plan.md \
  --receipt docs/notifications/latest-plan-notification.json
```

実装完了:

```bash
python3 .cline/skills/teams-completion-notifier/scripts/notify_teams.py \
  --mode implementation \
  --notification-choice enabled \
  --title "認証機能" \
  --summary "実装、テスト、レビュー、品質確認が完了" \
  --build-result PASS \
  --test-result PASS \
  --review-result PASS \
  --quality-result PASS \
  --verifier-result APPROVE \
  --evidence docs/quality/artifact-quality-report.md \
  --receipt docs/notifications/latest-implementation-notification.json
```

その他のWorkflow完了:

```bash
python3 .cline/skills/teams-completion-notifier/scripts/notify_teams.py \
  --mode workflow \
  --notification-choice enabled \
  --title "PDFコンテキスト変換" \
  --summary "変換、品質確認、独立検証が完了" \
  --quality-result PASS \
  --verifier-result APPROVE \
  --evidence docs/quality/artifact-quality-report.md \
  --receipt docs/notifications/pdf-context-conversion.json
```

初回は`--dry-run`でpayloadとゲート判定を確認する。dry-runは送信完了として扱わない。

## Failure Handling

- ゲート不足: 送信せず終了コード2
- Webhook未設定: 送信せず終了コード3
- HTTP／通信失敗: 最大3回の指数バックオフ後、終了コード4
- 成功: HTTP 2xxを確認し、Webhook URLを含まないreceiptを保存
- 通知失敗を作業品質の失敗へ置き換えないが、通知完了とは報告しない

## Completion

- モード固有の完了ゲートがすべてPASS
- TeamsからHTTP 2xxを受信
- URLを含まない通知証跡が保存されている
- 同じ完了イベントの多重通知を避けている
