# Cline Loop Engineering Rules

These rules are always active for this workspace.

## Response Language

- ユーザーへの出力は日本語で行う。
- コード、コマンド、ファイルパス、識別子、引用、ログ、エラーメッセージは原文のまま扱ってよい。
- 技術用語は必要に応じて英語を併記してよいが、説明文は日本語を基本にする。

## Core Operating Model

- Use `.cline/skills/` for repeatable task-specific workflows.
- Use `.clinerules/` only for always-on project rules.
- Use `memory-bank/` for durable project context across sessions.
- Use `docs/ai/` for AI-facing context, terminology, decisions, ADRs, and unknowns.
- Use `docs/specs/` for source-derived specifications.
- Use `docs/reviews/` for review results.
- Do not put large workflow instructions directly into `.clinerules/`; create or update a Skill instead.

## Skill Selection

- Use `/cline-skill-builder` when creating, converting, improving, or reviewing Cline Skills.
- Use `/legacy-source-spec-writer` when turning existing source code into Markdown specifications.
- Use `/unknown-list-extractor` when extracting unknowns, ambiguities, assumptions, risks, or confirmation items.
- Use `/grill-with-docs` when requirements are unclear and should be clarified before implementation.
- Use `/implementation-loop` when implementing approved or clearly specified changes.
- Use `/review-loop` when reviewing current diffs without making changes.
- Use `/html-artifact-checker` when checking HTML artifacts against specs, source behavior, fields, flows, validations, errors, and edge cases.
- Use `/memory-bank-updater` after meaningful planning, implementation, review, or decisions that should persist.

## Planning And Clarification

- Do not implement when business rules, acceptance criteria, or scope are materially unclear.
- If uncertainty can change behavior or cause rework, clarify first with `/grill-with-docs`.
- If uncertainty can be listed independently, record it with `/unknown-list-extractor`.
- Mark unresolved requirements as `Unknown`; do not guess.
- Separate confirmed decisions from assumptions.

## Documentation Rules

- Source-derived behavior belongs in `docs/specs/`.
- Questions and ambiguities belong in `docs/ai/unknowns/`.
- Shared terminology belongs in `docs/ai/glossary.md`.
- Current AI work context belongs in `docs/ai/active-context.md`.
- Durable project context belongs in `memory-bank/`.
- Review findings belong in `docs/reviews/`.
- Cite source files, specs, or user decisions when documenting behavior.

## Implementation Rules

- Read relevant `memory-bank/`, `docs/ai/`, and `docs/specs/` files before implementing.
- Keep implementation changes minimal and scoped.
- Prefer existing project patterns over new abstractions.
- Do not mix unrelated refactors with requested work.
- Add or update tests when behavior changes and a test framework exists.
- Run available build, lint, or test commands when feasible.
- Report any verification that could not be run.

## Review Rules

- For review-only requests, do not modify files.
- Lead review output with findings, ordered by severity.
- Focus on correctness, regressions, missing tests, spec violations, and delivery risk.
- Do not report speculative issues without evidence.
- If no issues are found, say so clearly and note remaining test gaps or residual risks.

## Memory Bank Rules

- Update `memory-bank/activeContext.md` when the current focus, decisions, blockers, or next steps change.
- Update `memory-bank/progress.md` after meaningful work is completed.
- Update `memory-bank/techContext.md` when technical constraints, commands, architecture, or conventions change.
- Update `memory-bank/projectbrief.md` only for stable project purpose or scope changes.
- Keep memory entries concise; do not paste raw logs, large diffs, secrets, or temporary scratch notes.

## Safety Rules

- Do not store secrets, tokens, credentials, private keys, or personal data in repository files.
- Do not overwrite user changes without explicit permission.
- Do not delete or reset files unless explicitly requested.
- When a task touches GitHub publishing, inspect `git status` and avoid staging unrelated changes.
- Prefer explicit file paths when staging changes.
