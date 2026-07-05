---
name: review-loop
description: Review current code changes without implementing fixes. Use when checking diffs for regressions, missing tests, spec violations, unnecessary changes, risks, or readiness before delivery.
---

# Review Loop

Review the current workspace changes and report actionable findings. This skill is for review only.

## Purpose

Find bugs, regressions, missing tests, unclear behavior, unnecessary changes, and risks before implementation is delivered.

Do not modify files unless the user explicitly asks for fixes after the review.

## Use This Skill When

- Reviewing current diffs
- Checking whether an implementation matches specs
- Looking for regressions or behavior changes
- Checking missing tests
- Checking unnecessary or unrelated changes
- Preparing a handoff review
- Reviewing before commit, PR, or delivery

## Do Not Use This Skill For

- Implementing fixes
- Refactoring
- Writing new specs
- Generating HTML artifact reviews only

For HTML artifact coverage review, use the `html-artifact-checker` skill behavior.

## Review Inputs

Check these when available:

- Current git diff
- Relevant source files
- Existing tests
- `docs/specs/`
- `docs/ai/`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`

## Review Process

1. Identify changed files.
2. Read the relevant diff.
3. Read surrounding code for behavior context.
4. Compare changes against specs and project context.
5. Check whether tests cover the changed behavior.
6. Separate real findings from style preferences.
7. Report findings by severity.

## Severity

- `Critical`: likely data loss, security issue, production outage, or unusable feature.
- `High`: likely user-facing regression or incorrect behavior.
- `Medium`: meaningful maintainability, test, or edge-case risk.
- `Low`: minor issue worth addressing but not blocking.

## Output Format

Lead with findings:

```md
# Review Findings

## Findings

| Severity | File | Issue | Evidence | Recommendation |
|---|---|---|---|---|

## Open Questions

## Test Gaps

## Summary
```

If there are no findings, say that clearly and list any remaining test gaps or residual risks.

## Safety Rules

- Do not edit files during review.
- Do not report speculative issues without evidence.
- Prefer file paths and line references when possible.
- Focus on behavior, correctness, risks, and missing tests.
- Keep summaries secondary to findings.

