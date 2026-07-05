---
name: memory-bank-updater
description: Update memory-bank files with concise project context, current work, technical notes, and progress. Use after meaningful planning, implementation, review, decisions, or context changes that should persist across sessions.
---

# Memory Bank Updater

Update `memory-bank/` so project context stays useful across sessions.

## Purpose

Record durable project context without bloating prompts or mixing temporary notes into source files.

This skill is for memory maintenance. Keep updates concise, factual, and easy to scan.

## Use This Skill When

- Updating long-term project context
- Recording current focus after planning or implementation
- Capturing technical constraints or project conventions
- Recording completed work and next steps
- Summarizing decisions that affect future work
- Cleaning stale memory-bank entries
- Preparing context before handing off work

## Do Not Use This Skill For

- Writing source-derived specifications
- Extracting unknown lists
- Reviewing code changes
- Implementing features
- Storing large logs, raw diffs, or temporary notes

Use `legacy-source-spec-writer` for specs, `unknown-list-extractor` for unknowns, `review-loop` for review, and `implementation-loop` for implementation.

## Files To Maintain

Use these files by default:

```txt
memory-bank/projectbrief.md
memory-bank/activeContext.md
memory-bank/techContext.md
memory-bank/progress.md
```

## File Responsibilities

### `projectbrief.md`

Use for stable project purpose and scope:

- Project goal
- Business or workflow purpose
- Main users or actors
- Stable non-goals
- High-level constraints

### `activeContext.md`

Use for current working state:

- Current focus
- Recently made decisions
- Active assumptions
- Immediate next steps
- Current blockers

### `techContext.md`

Use for technical background:

- Architecture notes
- Frameworks, languages, and tools
- Commands for build/test/lint
- Important conventions
- Integration constraints

### `progress.md`

Use for work status:

- Completed tasks
- Pending tasks
- Known gaps
- Follow-up items
- Verification status

## Update Process

1. Read existing `memory-bank/` files before editing.
2. Identify what changed materially.
3. Update only the relevant sections.
4. Remove stale statements when they are contradicted by new information.
5. Keep entries concise.
6. Prefer dated or status-oriented notes when useful.
7. Do not duplicate the same fact across all files unless each file needs it.

## Writing Rules

- Write durable context, not chat transcripts.
- Keep facts traceable to user decisions, source files, docs, or completed work.
- Mark uncertain items as assumptions or unknowns.
- Do not invent decisions.
- Do not store secrets, credentials, tokens, private keys, or personal data.
- Avoid large pasted outputs.

## Suggested Section Format

Use this shape when adding new notes:

```md
## Current Focus

## Recent Decisions

## Completed

## Pending

## Blockers

## Notes
```

## Final Response Format

```md
## Updated

## Key Context Saved

## Still Open
```

Report which memory-bank files changed and the most important context saved.

