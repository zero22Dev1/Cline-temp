# Teams Completion Notification 使用方法

## Teams側の準備

1. 通知先チャネルのメニューから`Workflows`を開く。
2. webhookを受信してチャネルへ投稿するテンプレートを選ぶ。
3. Workflowに共同所有者を設定する。
4. 発行されたURLをローカル環境変数へ設定する。

```bash
export TEAMS_WORKFLOW_WEBHOOK_URL='<Teams Workflows webhook URL>'
```

URLを`.env`やGit管理ファイルへ保存しない。

## 計画モード

```txt
/teams-completion-notification.md

planモードで実行してください。
計画の作成、レビュー、品質ゲートが完了し、実装可能と判定された場合だけTeamsへ通知してください。
```

## 実装モード

```txt
/teams-completion-notification.md

implementationモードで実行してください。
コード、必要なテストコード、build、test、差分レビュー、品質ゲート、独立検証がすべて完了した場合だけTeamsへ通知してください。
```

## 初回確認

最初に`teams-completion-notifier` Skillを`--dry-run`で実行し、通知本文に秘密情報や不要なコードが含まれないことを確認する。実際のTeams送信は外部副作用なので、Webhook設定後に明示的に実施する。
