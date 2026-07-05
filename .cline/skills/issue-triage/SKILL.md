---
name: issue-triage
description: Triage issues, feature requests, discussions, and bug reports into duplicate candidates, priority, labels, needs-info, and next actions. Use when the user wants a clean actionable issue queue, top issues, proposed labels, or report-only GitHub issue triage.
---

# Issue Triage

Turn incoming issues and discussions into a clean, actionable queue.

## Purpose

Discover, summarize, deduplicate, prioritize, and propose labels for issues. Default to report-only.

Do not auto-label, close, or comment unless the user explicitly asks.

## Use This Skill When

- The user asks to triage issues
- Open issues need priority and labels
- Duplicates or stale issues need review
- Feature requests and bug reports need classification
- Daily triage needs an issue-specific feeder report
- A top issue queue is needed

## Do Not Use This Skill For

- Implementing issue fixes
- Closing or labeling issues without explicit approval
- General CI triage
- Full project daily triage

Use `daily-triage` for cross-signal daily scans, `loop-triage` for generic prioritization, and `implementation-loop` for fixes.

## Inputs To Check

Use what is available:

- User-provided issue list
- GitHub issue URLs or exported issue text
- Existing labels
- Comments, reactions, linked PRs, age, reproduction details
- `docs/ai/unknowns/`
- `memory-bank/activeContext.md`
- `docs/specs/`

## Issue Buckets

- `P0`: security, data loss, production breakage, auth/payment risk
- `P1`: high impact and clear action
- `P2`: important but not urgent
- `P3`: low priority or cleanup
- `Needs Info`: not enough reproduction or requirements
- `Possible Duplicate`: likely duplicate, human should confirm
- `Needs Human`: ambiguous decision, product call, or sensitive area

## Suggested Labels

Suggest labels, but do not apply them automatically:

- `bug`
- `feature`
- `docs`
- `needs-info`
- `needs-repro`
- `duplicate-candidate`
- `priority:p0`
- `priority:p1`
- `priority:p2`
- `priority:p3`
- `area:<area>`

## Process

1. Read the issue input and existing project context.
2. Summarize each issue in one sentence.
3. Detect possible duplicates conservatively.
4. Identify missing reproduction steps or missing requirements.
5. Assign priority and proposed labels.
6. Separate report-only suggestions from actions requiring approval.
7. Recommend the next action or next Skill.

## Output Location

If asked to save state, write to:

```txt
docs/ai/triage/YYYYMMDD-issue-triage.md
```

For unresolved issue questions, write or update:

```txt
docs/ai/unknowns/YYYYMMDD-issue-triage-unknowns.md
```

## Output Format

```md
# Issue Triage: YYYY-MM-DD

## Summary

## Top Queue

| Priority | Issue | Summary | Suggested Labels | Evidence | Next Action |
|---|---|---|---|---|---|

## Needs Info

## Possible Duplicates

## Needs Human

## Proposed Label Changes

## Recommended Next Skill
```

## Safety Rules

- Do not auto-label in first-pass triage.
- Do not close duplicates without human confirmation.
- Do not mark security/auth/payment issues as routine.
- Do not invent reproduction steps.
- Preserve issue IDs, URLs, and evidence when available.

