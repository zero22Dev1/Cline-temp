---
name: implementation-loop
description: Implement requested changes using project context, specs, and memory-bank notes. Use when the user asks to code, fix, refactor, or complete a feature with minimal safe changes and verification.
---

# Implementation Loop

Implement requested changes with minimal, focused edits and explicit verification.

## Purpose

Use project context to make a correct, scoped implementation. Prefer existing patterns and avoid unrelated refactors.

## Use This Skill When

- Implementing a requested feature
- Fixing a bug
- Applying an approved review finding
- Refactoring within a clear scope
- Updating tests for changed behavior
- Completing work described in `docs/specs/`, `docs/ai/`, or `memory-bank/`

## Do Not Use This Skill For

- Review-only tasks
- Requirement clarification without implementation
- HTML artifact coverage checks
- Unknown-only extraction
- Source-to-spec documentation only

Use `grill-with-docs` when requirements are unclear before implementation. Use `review-loop` when the user only wants review.

## Inputs To Read

When relevant, read:

- `README.md`
- `.clinerules/`
- `memory-bank/projectbrief.md`
- `memory-bank/activeContext.md`
- `memory-bank/techContext.md`
- `memory-bank/progress.md`
- `docs/ai/active-context.md`
- `docs/ai/glossary.md`
- `docs/ai/adr/`
- `docs/specs/`
- Existing source and tests around the target area

## Implementation Process

1. Confirm the concrete task from the user request.
2. Inspect relevant project context and existing code patterns.
3. Identify the smallest safe change.
4. Edit only files needed for the task.
5. Add or update tests when behavior changes.
6. Run available formatting, build, and tests when feasible.
7. Inspect the final diff.
8. Update `memory-bank/progress.md` or `docs/ai/active-context.md` if the project context changed materially.

## Change Rules

- Keep changes scoped to the request.
- Preserve existing style and architecture.
- Do not invent new abstractions unless they reduce real complexity.
- Do not rewrite unrelated files.
- Do not hide uncertainty; list it.
- Do not proceed on ambiguous business rules when the result would be risky.

## Verification

Prefer project-native commands, such as:

```txt
npm test
npm run build
npm run lint
pnpm test
pnpm build
pytest
go test ./...
cargo test
```

If verification cannot run, report why.

## Final Response Format

```md
## Changes

## Verification

## Notes
```

Mention files changed, commands run, and any remaining risks.

