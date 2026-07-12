# Skill Evaluation Contract

評価器から独立した正解と合否条件を、評価開始前に固定する。

## Contract

```md
# Evaluation Contract: <skill-name>

## Authority

- Owner:
- Approved by:
- Source of truth:
- Contract version/date:

## Purpose

## Required Inputs

## Expected Outputs

| Output | Format | Location | Required |
|---|---|---|---|

## Allowed Actions

## Forbidden Actions

## Acceptance Criteria

| AC-ID | Observable criterion | Oracle | Evidence | Required |
|---|---|---|---|---|

## Trigger Fixtures

| Fixture ID | Prompt | Expected | Oracle |
|---|---|---|---|
| TRG-001 | | Trigger | |
| TRG-002 | | Trigger | |
| TRG-003 | | Trigger | |
| NTR-001 | | Not Trigger | |
| NTR-002 | | Not Trigger | |
| NTR-003 | | Not Trigger | |

## Behavioral Fixtures

| Fixture ID | Type | Input | Expected result | Forbidden result | Oracle |
|---|---|---|---|---|---|
| BEH-001 | Normal | | | | |
| BEH-002 | Boundary | | | | |
| BEH-003 | Failure | | | | |

## Required Evidence

- Cline activation record
- Raw output or artifact
- Commands and exit status
- Tests and validation results
- Diff or proof of no modification

## Human Decision Points

## Contract Status

`READY / NEEDS_INPUT / BLOCKED`
```

## Rules

- `READY`以外では採点を開始しない。
- Evaluatorが実行結果を見た後にExpectedやOracleを変更しない。
- Oracleはユーザー決定、公式仕様、schema、テスト、既存の承認済み成果物など、Evaluatorの自己判断以外を使う。
- 正解が複数ある場合は許容範囲を事前定義する。
- Contract変更後はversionを更新し、影響するfixtureを再実行する。
