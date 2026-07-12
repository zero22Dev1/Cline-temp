# Context Window Management Workflow Usage

## 目的

長時間・複雑な作業で、必要な根拠を失わずにClineのworking setを小さく保ち、指示忘れ、古い前提の混入、無関係な大量読込を防ぐ。

## 使用するタイミング

- 複数モジュール、複数Skill、複数イテレーションを扱う
- 会話やツール出力が長くなった
- 作業を中断、再開、引き継ぎする
- 同じ情報を何度も探している
- 最新指示、仕様、コード、検証結果の関係が曖昧になった

## 実行例

```txt
/context-window-management.md

この作業のContext Contractを作成し、必要な情報を段階的に読み込んでください。
工程境界ごとに根拠付きCheckpointを更新し、長期保存すべき内容だけをmemory-bankへ渡してください。
```

## 長い実装での使用例

```txt
/adaptive-deep-planning.md
  -> /context-window-management.md
  -> Skill implementation-loop
  -> Context Checkpoint
  -> /artifact-quality-gate.md
  -> Skill loop-verifier
```

## 期待する出力

- Goal、Done、Scope、Sources、Constraintsを含むContext Contract
- `Keep / Retrieve / Summarize / Discard / Resolve`の選別
- 根拠パス付きContext Checkpoint
- 文脈の矛盾、仮定、Unknown
- 再開時の次の1アクション

## 注意

- 文脈を短くするためにテスト、受け入れ条件、安全制約を省略しない。
- memory-bankへ生ログや一時的な探索結果を保存しない。
- 圧縮後は正本、Git差分、最新の検証結果を再確認してから続行する。
