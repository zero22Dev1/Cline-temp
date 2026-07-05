---
name: grill-with-docs
description: Clarify requirements before implementation by asking focused questions and recording decisions. Use when a feature, migration, fix, or artifact request is ambiguous and should be specified before coding.
---

# Grill With Docs

Clarify requirements before implementation and record the resulting decisions.

## Purpose

Turn an unclear request into documented requirements, terminology, scope, assumptions, and acceptance criteria.

This skill should avoid implementation until the user approves or requirements are clear enough to proceed.

## Use This Skill When

- The user asks to clarify a feature before coding
- Requirements are ambiguous
- Business rules are missing
- Existing behavior must be preserved but is not fully described
- A migration or refactor needs scope control
- Acceptance criteria need to be written
- Terms, fields, statuses, or flows need definitions

## Do Not Use This Skill For

- Straightforward implementation with clear requirements
- Review-only tasks
- Unknown-only extraction from existing docs
- HTML artifact coverage checking

Use `unknown-list-extractor` when the main output should be an unknown list. Use `implementation-loop` when the user is ready to implement.

## Inputs To Check

When available, read:

- `README.md`
- `.clinerules/`
- `memory-bank/projectbrief.md`
- `memory-bank/activeContext.md`
- `memory-bank/techContext.md`
- `docs/ai/glossary.md`
- `docs/ai/active-context.md`
- `docs/specs/`
- Relevant tickets, docs, or source files

## Questioning Rules

- Ask one focused question at a time when user input is required.
- Prefer concrete choices when possible.
- Do not ask questions that can be answered from existing files.
- Record decisions as they are made.
- Separate confirmed decisions from assumptions.
- Stop asking when the remaining uncertainty is low enough to implement safely.

## Clarification Areas

Cover these as needed:

- Goal
- Users or actors
- Current behavior
- Desired behavior
- Inputs and outputs
- Data fields
- Statuses and transitions
- Validation rules
- Error handling
- Edge cases
- Non-goals
- Acceptance criteria
- Rollout or migration constraints

## Documentation Outputs

Update or create:

```txt
memory-bank/activeContext.md
docs/ai/active-context.md
docs/ai/glossary.md
docs/specs/<feature-name>.md
```

If unresolved items remain, create:

```txt
docs/ai/unknowns/YYYYMMDD-<topic>-unknowns.md
```

## Spec Template

```md
# <Feature Name> Requirements

## Goal
## Background
## Confirmed Decisions
## Scope
## Non-Goals
## Terms
## User Flow
## Inputs
## Outputs
## Validation Rules
## Error Handling
## Edge Cases
## Acceptance Criteria
## Open Questions
## Implementation Notes
```

## Final Response Format

```md
## Confirmed

## Still Open

## Docs Updated

## Recommended Next Step
```

## Safety Rules

- Do not implement until requirements are clear or the user explicitly asks.
- Do not guess business rules.
- Mark unresolved items as unknown.
- Keep docs concise and useful for implementation.

