---
name: loop-verifier
description: Independently verify whether a completed loop is acceptable. Use after implementation, docs updates, skill changes, or artifact generation to check goal fit, scope control, tests, evidence, unresolved risks, and to return APPROVE, REJECT, or ESCALATE_HUMAN.
---

# Loop Verifier

Act as an independent verifier for completed loop work.

## Purpose

Check whether the completed work actually satisfies the stated goal, stayed in scope, and has enough evidence to accept.

This skill is stricter than a normal summary. It returns a decision.

## Use This Skill When

- A loop claims to be complete
- Implementation needs an independent acceptance check
- Skill or documentation changes need verification
- The user wants approve/reject/escalate decisioning
- A branch should be checked before commit, push, or handoff
- Verification evidence needs to be explicit

## Do Not Use This Skill For

- Implementing fixes
- Initial triage
- Requirement clarification
- Budget tracking
- Writing specs from source

Use `review-loop` for general code review and `implementation-loop` for fixes after rejection.

## Decision Values

- `APPROVE`: goal is met, scope is controlled, and evidence is sufficient
- `REJECT`: goal is not met, implementation is unsafe, or required verification failed
- `ESCALATE_HUMAN`: cannot decide safely because a human/domain decision is required

## Verification Checklist

Check:

- Original goal
- Files changed
- Scope boundaries
- Tests or validation evidence
- Documentation updates
- `memory-bank/` updates if context changed
- Unresolved unknowns
- Git status if commit/push is requested
- Whether any destructive or unrelated changes were introduced

## Process

1. Restate the goal in one sentence.
2. Inspect changed files and relevant docs.
3. Compare output against acceptance criteria or user request.
4. Check verification evidence.
5. Identify blockers, residual risks, and missing tests.
6. Return exactly one decision: `APPROVE`, `REJECT`, or `ESCALATE_HUMAN`.

## Output Format

```md
# Loop Verification

Decision: APPROVE | REJECT | ESCALATE_HUMAN

## Goal Checked

## Evidence Reviewed

## Findings

| Severity | Finding | Evidence | Required Action |
|---|---|---|---|

## Verification Gaps

## Final Notes
```

## Safety Rules

- Do not edit files during verification.
- Do not approve without evidence.
- Do not reject based only on style preference.
- Escalate when business intent, user acceptance, or external authority is required.

