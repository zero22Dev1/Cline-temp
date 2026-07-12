# Cline Skill Evaluation Rubric

## Scoring

| Category | Points | Full-score evidence |
|---|---:|---|
| Discovery And Triggering | 15 | name、description、発火・非発火シナリオが明確 |
| Scope And Responsibility | 15 | 単一責務、対象外、類似Skillとの境界が明確 |
| Procedure And Executability | 15 | 入出力、手順、停止・完了条件が実行可能 |
| Safety And Integrity | 15 | 破壊操作、上書き、秘密、失敗時の保護が十分 |
| Validation And Evidence | 15 | 構文、参照、テスト、成果物の客観的証拠がある |
| Workflow Integration | 10 | Rule、Workflow、usage、関連Skillとの接続が正しい |
| Context Efficiency | 10 | 簡潔、段階読込、重複なし、不要な大量読込なし |
| Maintainability | 5 | 命名、構造、再利用、変更箇所、所有境界が明確 |
| **Total** | **100** | |

## Rating Guidance

各カテゴリは次の割合を目安にする。

- `100%`: 客観的証拠があり、重要な欠落なし
- `75%`: 実用可能だが限定的な欠落あり
- `50%`: 重要な曖昧さまたは検証不足あり
- `25%`: 大部分が未定義または実行困難
- `0%`: 存在しない、矛盾する、危険

証拠がない場合、説明が良くても`Validation And Evidence`を満点にしない。

## N/A And Normalization

各チェックを`PASS / PARTIAL / FAIL / N/A / NOT RUN`で記録する。

- `N/A`: Skillの責務上、適用する必要がない。理由と責務根拠が必要
- `NOT RUN`: 適用対象だが検証していない。未検証として減点する
- scriptを持たないSkillのscriptテストは`N/A`
- Workflowへ接続する必要がない独立SkillのWorkflow接続は`N/A`

N/A項目を0点または満点として扱わず、適用可能な配点だけで正規化する。

```txt
Normalized Category Score
  = Earned Applicable Points / Applicable Maximum Points * Category Weight
```

カテゴリ内の全項目が`N/A`の場合は、そのカテゴリ配点を総分母から除外して全体を100点へ再正規化する。ただしDiscovery、Scope、Procedure、Safetyは全Skillに必須で`N/A`にできない。

`NOT RUN`はN/Aに変換しない。必須検証が`NOT RUN`の場合、最終Decisionは最大`NEEDS_REVISION`とする。

## Critical Reject Conditions

- YAML frontmatterが不正でSkillとして読み込めない
- directory名と`name`が一致しない
- 必須参照またはscriptが存在せず、主要手順を実行不能
- destructive操作、force push、本番変更、秘密送信を安全条件なしで実行
- report-onlyを宣言しながら変更を行う
- 検証失敗やUnknownを成功として扱う
- 無制限ループまたは停止不能
- 対象SkillとRule・Workflowの重大な矛盾

## Severity Decision Gate

| Highest finding | Maximum decision |
|---|---|
| Critical | `REJECT` |
| Major | `NEEDS_REVISION` |
| Minor | `APPROVE_WITH_MINOR_FINDINGS` |
| Suggestion only | `APPROVE` |
| No finding | `APPROVE` |

点数によるDecisionよりSeverity Gateを優先する。

## Trigger Scenario Template

```md
| Fixture ID | Scenario | Oracle | Expected | Actual Activation | Evidence | Result |
|---|---|---|---|---|---|---|
| TRG-001 | 明確に対象 | ユーザー決定・仕様 | Trigger | Observed | Cline task / use_skill log | PASS / FAIL / NOT RUN |
```

## Portfolio Matrix

```md
| Capability | Primary Skill | Related Skills | Workflow | Overlap | Gap | Action |
|---|---|---|---|---|---|---|
```

## Minimum Evaluation Set

単体Skill:

1. frontmatterと構造
2. Evaluation ContractとOracle
3. Cline公式制約と有効状態・Global Skill競合
4. 参照切れ
5. 3件以上の発火fixtureと実activation
6. 3件以上の非発火fixtureと実activation
7. 正常系dry-run
8. 失敗または境界シナリオ
9. 安全性確認
10. 関連Workflow・usageとの整合
11. Severity GateとN/A正規化

全体評価:

1. 全Skillのfrontmatter
2. Skill一覧とusage記載
3. Rule・Workflowからの参照
4. 重複・空白・孤立
5. scriptとテストの対応
6. 共通の安全基準
7. コンテキスト肥大化と重複
8. 優先度付き改善ロードマップ
