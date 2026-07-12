---
name: adaptive-deep-planning
description: 開発依頼を要件の明確さ、変更規模、既存成果物、コード調査の必要性で分類し、必要なCline Skillだけを選んで計画・レビュー・タスク分割まで進める親Skill。曖昧または中規模以上の機能開発、移行、調査、実装計画で使用する。
---

# Adaptive Deep Planning

依頼ごとに必要な工程だけを選択し、計画承認前には実装しない。

## Phase 0: 依頼分類

最初に次を判定する。

### 要件の明確さ

- `明確`: 目的、対象、期待結果、完了条件、主な制約が判明している
- `一部不明`: 入出力、業務ルール、異常系、範囲、完了条件の一部が不足している
- `不明確`: 複数解釈が可能、目的と手段が混同、完了条件がない

### 変更規模

- `Small`: 1〜2ファイル程度、既存設計を変えず、DB・外部連携変更なし
- `Medium`: 複数ファイルまたは複数層、APIや画面を変更し、回帰確認が必要
- `Large`: 新機能、DB・認証・外部連携・移行・複数モジュールに影響

### 追加判定

- 既存の仕様書、計画書、タスク一覧、Issue、DDL、テスト仕様があるか
- 変更対象、既存挙動、類似機能、影響範囲をコード調査する必要があるか
- 依頼が実装、調査のみ、計画のみ、レビューのみのどれか

既存成果物は作り直さず、不足と現在コードとの差分だけを補う。

## Phase 1: ルート選択

### Route A: Direct Plan

要件が明確でSmallの場合に使用する。

1. 対象ファイルと影響範囲を確認する。
2. 変更内容、テスト方法、完了条件を簡潔に整理する。
3. Skill `review-loop` の観点で計画を確認する。

成果物は原則として会話内の簡潔な計画とし、必要な場合だけ `docs/planning/implementation-plan.md` を作る。

### Route B: Requirement Grill

要件が一部不明または不明確な場合に使用する。

1. Skill `grill-with-docs` で目的、利用者、入出力、正常系、異常系、業務ルール、非機能要件、対象外、完了条件を整理する。
2. Skill `unknown-list-extractor` で事実、仮定、Unknown、Blocking Questionを分離する。
3. SmallならRoute A、MediumまたはLargeならRoute Cへ進む。

コードで確認できることは質問しない。回答なしでも安全に進められる内容は仮定として記録する。

### Route C: Deep Investigation And Planning

Medium、Large、またはコード調査が必要な場合に使用する。

1. README、ルール、memory-bank、ビルド設定、構成、テスト方法を確認する。
2. Skill `legacy-source-spec-writer` を必要に応じて使い、関連コードと現行挙動を調査する。
3. 呼び出し元・先、DB、API、画面、認証、ログ、テスト、運用への影響を `High / Medium / Low` で整理する。
4. Skill `unknown-list-extractor` で未確認事項を分類する。
5. 複数案が実在する場合だけ比較し、推奨案と根拠を示す。
6. 実装計画を作成する。

必要な成果物だけを作る。

- `docs/planning/requirements.md`
- `docs/planning/codebase-analysis.md`
- `docs/planning/impact-analysis.md`
- `docs/planning/open-questions.md`
- `docs/planning/implementation-plan.md`

計画には対象外、変更ファイル、DB/API/画面変更、例外、認証、ログ、テスト、移行、ロールバック、リスク、完了条件を含める。

### Route D: Task Decomposition

Largeまたは1タスクでは安全に完了できない場合に使用する。

各タスクを、目的が1つ、独立検証可能、対象と完了条件が明確、依存関係が明確な単位にする。各タスクには目的、前提、対象、対象外、ファイル、手順、完了条件、テスト、依存、リスク、参照資料を記載する。

成果物:

- `docs/planning/tasks.md`
- 必要なら `docs/planning/tasks/task-<number>.md`

### Route E: Plan Review

実装前に次を確認する。

- 要件と設計の対応、異常系、対象外、検証可能な完了条件
- 既存設計との整合、過剰変更や不要な抽象化の有無
- DB、APIの互換性、認証・認可、入力検証、機密ログ
- 正常・境界・異常・権限・回帰テスト
- リリース、監視、ロールバック

判定は `Ready / Ready with Assumptions / Needs Revision / Blocked` とする。Blocking Questionが残る場合は実装へ進まない。

### Route F: Implementation Handoff

計画が承認され、分割タスクを別コンテキストへ渡す場合に使用する。

引き継ぐのは全体目的、今回の範囲、対象外、対象ファイル、手順、完了条件、テスト、依存、リスク、仮定、参照資料、変更禁止範囲だけとする。承認前に実装を始めない。

## 適応ルール

- 明確・Small: `A -> E`
- 不明確・Small: `B -> A -> E`
- 明確・Medium: `C -> E`
- 不明確・Medium: `B -> C -> E`
- 明確・Large: `C -> D -> E -> F`
- 不明確・Large: `B -> C -> D -> E -> F`
- 計画あり: 計画を現在コードと照合し、`E -> 必要ならD -> F`
- タスクあり: 計画との整合確認後に対象タスクを選び、`F`
- 調査のみ: 必要なBとCの調査部分だけ実施し、実装しない
- 計画のみ: 必要なB、C、D、Eだけ実施し、実装とFは行わない

作業中にDB、認証、共通部品、複数画面、外部連携、移行への影響が判明したら規模を再分類する。

## 停止条件

- データの正しさ、削除、金額、権限、セキュリティ、外部契約、移行を確定できない
- 依頼、コード、仕様書が重大に矛盾し、安全な判断ができない
- 検証方法を1つも定義できない

停止時は事実、矛盾、仮定、Blocking Question、推奨する次の行動を報告する。

## 完了時の出力

- 要件の明確さ、変更規模、選択ルート、スキップした工程と理由
- 作成・更新したファイル
- 確定事項、仮定、Unknown、Blocking Question
- 次のアクション

成果物を生成または実装した後は Skill `artifact-quality-gate` を実行する。
