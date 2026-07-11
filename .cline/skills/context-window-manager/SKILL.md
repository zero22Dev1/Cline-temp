---
name: context-window-manager
description: Clineの長時間・複雑な作業で、品質に必要な情報を選別し、段階的に読み込み、古い文脈を退避し、圧縮後も根拠と作業状態を復元できるようにする。調査対象が広い、複数Skillや反復ループを使う、会話が長い、引き継ぎや再開が必要、同じ情報を読み直す、指示忘れや文脈混線が起きそうな場合に使用する。
---

# Context Window Manager

コンテキスト量ではなく、現在の判断に必要な情報の密度・鮮度・根拠を管理する。会話履歴を正本にせず、リポジトリ内の仕様、ADR、コード、テスト、作業記録から復元可能にする。

詳細な選別基準が必要な場合は [references/context-principles.md](references/context-principles.md) を読む。

## Context Contract

作業開始時に次を短く確定する。

- `Goal`: 今回達成する結果
- `Done`: 検証可能な完了条件
- `Scope`: 変更対象と変更禁止範囲
- `Sources`: 正本となる仕様、ADR、コード、テスト
- `Constraints`: 品質、性能、セキュリティ、互換性
- `Unknowns`: 未解決事項と仮定
- `Verification`: 実行するbuild、lint、test、計測、レビュー
- `Current Step`: 現在の1つの作業

不明点が完了条件や挙動を変える場合は、読み込みを増やす前に`/adaptive-deep-planning.md`または`/grill-with-docs`を使う。

## Context Layers

必要な層だけを順番に読み込む。

1. `L0 Contract`: 依頼、完了条件、制約、現在の作業
2. `L1 Map`: README、ディレクトリ一覧、索引、関連Skill、主要設定
3. `L2 Evidence`: 対象仕様、ADR、関連コード、型、テスト
4. `L3 Detail`: 呼び出し先、履歴、ログ、外部資料
5. `L4 Raw`: 大量ログ、生成物全体、広範な履歴

最初から`L3`や`L4`を読み込まない。検索、シンボル、差分、テスト失敗などの根拠がある場合だけ深掘りする。

## Workflow

### 1. Select

情報を次へ分類する。

- `Keep`: 現在の判断に必須
- `Retrieve`: 必要時にファイルから再取得可能
- `Summarize`: 詳細を根拠リンク付きで圧縮
- `Discard`: 重複、古い仮説、無関係、再現可能な生出力
- `Resolve`: 矛盾または不明点として解決が必要

### 2. Load Progressively

- `rg`、ファイル一覧、見出し、シンボルから対象を絞る。
- 全文より関連範囲を優先する。
- 外部資料は必要な主張を支える箇所だけ読む。
- 大きなログはエラー、前後の文脈、再現条件を抽出する。
- 変更前に対象ファイルの現状と関連テストを読む。

### 3. Maintain Working Set

アクティブな文脈には次だけを残す。

- Context Contract
- 現在の仮説または判断
- 直接関係するファイル・シンボル
- 未解決事項
- 直近の検証結果
- 次の1アクション

探索結果や完了済み工程は、根拠パスを残してCheckpointへ圧縮する。

### 4. Checkpoint

工程境界、重要判断後、失敗後、引き継ぎ前、または文脈混線の兆候がある時に作成する。

```md
## Context Checkpoint
- Goal:
- Done:
- Current Step:
- Decisions:
- Evidence:
- Changed Files:
- Verification:
- Unknowns / Blockers:
- Next Action:
- Safe To Omit:
```

長期的に必要な内容だけを`/memory-bank-updater`へ渡す。一時的なCheckpointをmemory-bankへ大量保存しない。

### 5. Refresh

次の場合は古い要約を信用せず、正本を再読する。

- ユーザーが要件を変更した
- 対象ファイルが変更された
- テスト結果が仮説と矛盾した
- 別Skill、別担当、別セッションから再開した
- 同じ失敗を2回繰り返した
- 引用元や判断根拠を説明できない

### 6. Handoff

再開パケットにはContext Checkpoint、必要ファイル、再現コマンド、未解決事項、次の1アクションだけを含める。結論だけでなく、第三者が検証できる根拠を残す。

## Quality Guardrails

- トークン残量の推測値だけで重要情報を捨てない。
- ユーザーの最新指示、完了条件、安全制約を圧縮で失わない。
- 未検証の要約を確定仕様として扱わない。
- コード全体、ログ全体、Git履歴全体を目的なく読み込まない。
- 同じ内容を会話、memory-bank、docsへ重複保存しない。
- 要約後もファイルパス、シンボル、コマンド、結果へ追跡可能にする。
- 品質を下げて文脈を節約しない。必要なら作業を分割し、各単位を独立検証する。

## Completion

- 現在のGoal、Done、Current Stepを説明できる
- 各重要判断に正本または観測結果がある
- 古い仮説と最新指示が混在していない
- 未解決事項と仮定が分離されている
- 次の担当が再現・検証・再開できる
- 最終品質判定は要約ではなく成果物と検証結果に基づく
