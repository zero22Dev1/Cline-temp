---
name: daily-triage
description: Produce a report-only daily or periodic triage of CI status, issues, PRs, recent commits, unknowns, and project state. Use when the user wants a prioritized morning scan, active sprint scan, top risks, next actions, or a daily loop report without auto-fixing.
---

# Daily Triage

Create a prioritized daily view of what needs attention.

## Purpose

Start a work period with a clear picture of CI failures, issues, PRs, recent changes, unknowns, and blocked work.

Default to report-only. Do not implement fixes unless the user explicitly asks after triage.

## Use This Skill When

- The user asks what needs attention today
- The user asks for daily triage
- CI, issues, PRs, and recent commits need a single prioritized report
- A sprint or active work period needs a status scan
- `memory-bank/` and `docs/ai/` should be used to orient the next action

## Do Not Use This Skill For

- Implementing fixes
- Applying labels or closing issues automatically
- Detailed unknown extraction only
- Independent approval decisions

Use `loop-triage` for generic prioritization, `unknown-list-extractor` for detailed unknowns, `implementation-loop` for fixes, and `loop-verifier` for approval decisions.

## Inputs To Check

Check what is available:

- `README.md`
- `.clinerules/`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `docs/ai/active-context.md`
- `docs/ai/unknowns/`
- `docs/specs/`
- Current `git status -sb`
- Recent commits
- CI output, issue list, PR list, or user-provided logs

## Triage Buckets

- `Critical`: blocks delivery, CI red on protected branch, security/auth/payment risk
- `High`: should be handled next
- `Medium`: important but not blocking
- `Low`: cleanup, watch, or later
- `Noise / Ignore`: not relevant this run
- `Needs Human`: requires a user or domain decision

## Process

1. Read current project context from `memory-bank/` and `docs/ai/`.
2. Inspect available signals: CI, issues, PRs, commits, unknowns, current git status.
3. Group related signals.
4. Prioritize by severity, recency, and unblock value.
5. Recommend the next Skill to run.
6. Record unresolved handoffs and false positives.
7. Do not auto-fix during first-pass triage.

## Output Location

If asked to save the report, write to:

```txt
docs/ai/triage/YYYYMMDD-daily-triage.md
```

If the current working context changes materially, update:

```txt
memory-bank/activeContext.md
memory-bank/progress.md
```

## Output Format

```md
# Daily Triage: YYYY-MM-DD

## Summary

## Critical

| Item | Evidence | Impact | Next Action |
|---|---|---|---|

## High

| Item | Evidence | Impact | Next Action |
|---|---|---|---|

## Medium / Low

## Needs Human

## Noise / Ignore

## Recommended Next Skill

## Post-Run Critique
```

## Safety Rules

- Do not implement during triage.
- Do not auto-label, close, merge, or push.
- Mark uncertain items as `Needs Human` or `Unknown`.
- Escalate security, auth, payment, infra, and multi-file refactor decisions.
- If signal quality is poor, say so instead of inventing priorities.

