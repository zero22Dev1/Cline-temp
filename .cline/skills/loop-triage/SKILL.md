---
name: loop-triage
description: Triage loop inputs into prioritized work. Use when sorting issues, CI failures, diffs, bugs, unknowns, review findings, or task lists into severity, priority, next action, owner, and whether to implement, defer, escalate, or stop.
---

# Loop Triage

Turn noisy inputs into a prioritized next-action list.

## Purpose

Classify incoming work before implementation. Separate urgent blockers from follow-ups, unknowns, and noise.

This skill decides what should happen next. It does not implement fixes.

## Use This Skill When

- Multiple issues, CI failures, or review comments need sorting
- The user asks what to do first
- A loop has too many possible next steps
- Unknowns and blockers need classification
- Work should be split into implement, defer, escalate, or ignore
- A task list needs severity and priority

## Do Not Use This Skill For

- Writing full specifications
- Implementing fixes
- Review-only code inspection
- Budget tracking
- HTML artifact coverage checking

Use `unknown-list-extractor` for detailed unknown lists, `review-loop` for code review, and `implementation-loop` for implementation.

## Triage Categories

- `Do now`: blocks progress or is high confidence and high value
- `Defer`: useful but not needed for the current goal
- `Escalate`: needs user, domain owner, or maintainer decision
- `Drop`: out of scope, duplicate, or unsupported by evidence
- `Unknown`: cannot be classified safely without more evidence

## Severity

- `Critical`: blocks delivery or may cause major failure
- `High`: likely user-facing breakage or costly rework
- `Medium`: meaningful risk, but work can proceed with care
- `Low`: minor or cleanup-level item

## Process

1. Read the provided issues, logs, diffs, specs, or notes.
2. Remove duplicates.
3. Group related items.
4. Assign severity and action category.
5. Identify the smallest next action.
6. Mark anything uncertain as `Unknown` instead of guessing.
7. Recommend the next loop to run.

## Output Format

```md
# Loop Triage: <Topic>

## Summary

## Prioritized Items

| Priority | Severity | Action | Item | Evidence | Next Step |
|---:|---|---|---|---|---|

## Escalations

## Unknowns

## Recommended Next Loop
```

## Safety Rules

- Do not implement during triage.
- Do not classify unsupported guesses as facts.
- Preserve evidence links, file paths, logs, or issue IDs when available.
- If everything is low priority, say so.

