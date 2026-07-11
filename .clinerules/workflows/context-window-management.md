# Context Window Management Workflow

長時間・複雑な作業の文脈を、品質を維持したまま選別、段階読込、Checkpoint、再構成する。

## Step 1: Load Parent Skill

Skill `context-window-manager`を読み込み、Context Contractを作る。最新のユーザー依頼を最優先し、Goal、Done、Scope、Sources、Constraints、Unknowns、Verification、Current Stepを確定する。

## Step 2: Build A Context Map

最初はREADME、ディレクトリ、関連Skill、memory-bank、仕様・ADRの索引、主要設定だけを確認する。検索結果から必要なコード、テスト、文書へ段階的に進む。

読み込む理由を説明できない大量ファイル、ログ、履歴は読み込まない。

## Step 3: Select Working Set

情報を`Keep / Retrieve / Summarize / Discard / Resolve`へ分類する。現在の作業に必要なContract、根拠、未解決事項、直近の検証、次の1アクションだけをworking setに残す。

## Step 4: Execute With Checkpoints

次の境界でContext Checkpointを更新する。

- 調査完了
- 計画承認
- 実装開始・完了
- 品質検証開始・完了
- 仮説変更または重要な失敗
- Skill切替
- 引き継ぎ・再開

Checkpointには結論だけでなく、根拠パス、変更ファイル、検証コマンドと結果を含める。

## Step 5: Detect Context Degradation

次の兆候があれば作業を止め、正本から再構成する。

- 最新指示と古い指示が混在する
- 同じファイルや説明を繰り返し探す
- 判断根拠を示せない
- Scope外の変更が増える
- 解決済みUnknownが再登場する
- テスト結果と要約が矛盾する

## Step 6: Persist Only Durable Context

セッションを越えて必要な情報だけを`/memory-bank-updater`へ渡す。仕様は`docs/specs/`、判断はADR、不明点は`docs/ai/unknowns/`、学習候補は`/continuous-project-learning.md`へ分離する。

## Step 7: Final Context Audit

完了前に最新依頼、Git差分、完了条件、検証結果、未解決事項を照合する。成果物の品質は`/artifact-quality-gate.md`と`/loop-verifier`で判定し、Context Checkpointの自己申告だけで完了にしない。

## Final Output

- Context Contract
- 読み込んだ正本と選定理由
- 省略・退避した情報と再取得先
- 最新Context Checkpoint
- 文脈の矛盾・Unknown
- 次のアクションまたは最終検証結果
