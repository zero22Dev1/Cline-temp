---
name: loop-budget
description: Track and enforce loop budgets for Cline work. Use when planning or auditing a loop with token/time/tool limits, stop conditions, run logs, verification gates, or when the user asks whether a task is still within budget before continuing.
---

# Loop Budget

Keep Cline loops bounded, auditable, and honest about cost.

## Purpose

Before or during a loop, define the work budget, stopping conditions, and verification gates. After the loop, report what was spent and what remains.

This skill is not for estimating money exactly. It is for keeping work from drifting without a visible budget.

## Use This Skill When

- A task may take multiple steps or repeated passes
- The user asks to keep work bounded
- The user asks for a run log or budget report
- A loop should stop after a fixed number of attempts
- Verification gates should be explicit before implementation
- Work is at risk of expanding beyond the requested scope

## Do Not Use This Skill For

- One-shot small edits
- Pure code review without repeated work
- Feature implementation itself
- Git commits or pushes

Use `implementation-loop` for implementation, `review-loop` for review, and `git-commit-workflow` for featureBranch commit/push.

## Budget Fields

Track these when relevant:

- Goal
- Scope
- Max iterations
- Time budget
- Token/context budget if known
- Tool call budget if known
- Files allowed to change
- Stop conditions
- Verification commands
- Escalation conditions

## Loop Budget Template

```md
# Loop Budget: <Task>

## Goal

## Scope

## Budget

| Item | Limit | Current | Notes |
|---|---:|---:|---|
| Iterations | | | |
| Time | | | |
| Tool calls | | | |
| Files changed | | | |

## Stop Conditions

## Verification Gates

## Escalation Conditions

## Run Log

| Step | Action | Result | Next |
|---|---|---|---|

## Final Status
```

## Process

1. Define the goal and allowed scope.
2. Set practical stop conditions.
3. Identify verification gates before changes begin.
4. During the loop, append concise run-log entries.
5. Stop when the goal is met, the budget is exhausted, or risk exceeds the scope.
6. Report the final status clearly.

## Safety Rules

- Do not use the budget as a reason to hide incomplete work.
- Do not continue after a stop condition without user approval.
- Do not expand scope silently.
- Report blockers and verification gaps directly.

