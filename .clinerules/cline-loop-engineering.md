# Cline Loop Engineering Rules

These rules are always active for this workspace.

## Response Language

- ユーザーへの出力は日本語で行う。
- コード、コマンド、ファイルパス、識別子、引用、ログ、エラーメッセージは原文のまま扱ってよい。
- 技術用語は必要に応じて英語を併記してよいが、説明文は日本語を基本にする。

## Core Operating Model

- Use `.cline/skills/` for repeatable task-specific workflows.
- Use `.clinerules/workflows/` for slash-command workflows that coordinate multiple Skills and conditional routes.
- Use `.clinerules/` only for always-on project rules.
- Use `memory-bank/` for durable project context across sessions.
- Use `docs/ai/` for AI-facing context, terminology, decisions, ADRs, and unknowns.
- Use `docs/specs/` for source-derived specifications.
- Use `docs/reviews/` for review results.
- Do not put large workflow instructions directly into `.clinerules/`; create or update a Skill instead.
- Keep files in `.clinerules/workflows/` focused on orchestration; keep detailed reusable checks in `.cline/skills/`.

## Skill Selection

- Use `/context-window-manager` when a task is long-running, crosses multiple modules or Skills, requires repeated iterations, is being resumed or handed off, or shows signs of stale, duplicated, or conflicting context.
- Use `/context-window-management.md` before and during complex work to establish a Context Contract, load evidence progressively, create checkpoints, and refresh from authoritative sources.
- Use `/adaptive-deep-planning` as the parent planning Skill when request clarity, change size, investigation depth, or task decomposition must be decided.
- Use `/artifact-quality-gate` after generating implementation or documentation artifacts when completion requires coverage, correctness, traceability, format, and automated validation checks.
- Use `/ai-learning-curator` after meaningful corrections, repeated failures, validated improvements, or completed workflows when reusable project learning should be evaluated and promoted.
- Use `/continuous-project-learning.md` after quality validation when reusable learning should become memory, ADRs, regression tests, performance baselines, rules, or Skills.
- Use `/harness-engineering-loop.md` when an artifact needs bounded repeated implementation, observation, evaluation, diagnosis, and harness improvement before completion.
- Use `/cline-skill-builder` when creating, converting, improving, or reviewing Cline Skills.
- Use `/legacy-source-spec-writer` when turning existing source code into Markdown specifications.
- Use `/unknown-list-extractor` when extracting unknowns, ambiguities, assumptions, risks, or confirmation items.
- Use `/grill-with-docs` when requirements are unclear and should be clarified before implementation.
- Use `/implementation-loop` when implementing approved or clearly specified changes.
- Use `/review-loop` when reviewing current diffs without making changes.
- Use `/html-artifact-checker` when checking HTML artifacts against specs, source behavior, fields, flows, validations, errors, and edge cases.
- Use `/memory-bank-updater` after meaningful planning, implementation, review, or decisions that should persist.
- Use `/git-commit-workflow` when creating a local featureBranch, staging intended files, committing there, and pushing to the matching remote featureBranch.
- Use `/loop-budget` when a task needs explicit iteration, time, tool, verification, or stop-condition limits.
- Use `/loop-triage` when issues, CI failures, unknowns, review findings, or task lists need priority and next-action classification.
- Use `/loop-verifier` after a loop claims completion and an independent APPROVE / REJECT / ESCALATE_HUMAN decision is needed.
- Use `/daily-triage` for report-only daily or sprint scans across CI, issues, PRs, commits, unknowns, and project state.
- Use `/issue-triage` for report-only issue, feature request, discussion, duplicate, priority, and label proposal workflows.
- Use `/template-commit-workflow` when committing and pushing Cline template files such as `.cline/skills/`, `.clinerules/`, `README.md`, `docs/`, or `memory-bank/`.

## Planning And Clarification

- Do not implement when business rules, acceptance criteria, or scope are materially unclear.
- If uncertainty can change behavior or cause rework, clarify first with `/grill-with-docs`.
- If uncertainty can be listed independently, record it with `/unknown-list-extractor`.
- Mark unresolved requirements as `Unknown`; do not guess.
- Separate confirmed decisions from assumptions.
- Start new loop patterns in report-only mode before enabling implementation, labeling, closing, merging, or pushing.

## Documentation Rules

- Source-derived behavior belongs in `docs/specs/`.
- Questions and ambiguities belong in `docs/ai/unknowns/`.
- Shared terminology belongs in `docs/ai/glossary.md`.
- Current AI work context belongs in `docs/ai/active-context.md`.
- Durable project context belongs in `memory-bank/`.
- Review findings belong in `docs/reviews/`.
- Cite source files, specs, or user decisions when documenting behavior.

## Implementation Rules

- For complex work, keep only the current contract, relevant evidence, unresolved items, latest verification, and next action in the active working set; retrieve other details from authoritative files when needed.
- Re-check the latest user request, source files, Git diff, and verification results after a checkpoint, resume, handoff, or context compression.
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
- Use `/loop-verifier` when the result needs an explicit approval decision rather than a normal review summary.

## Memory Bank Rules

- Update `memory-bank/activeContext.md` when the current focus, decisions, blockers, or next steps change.
- Update `memory-bank/progress.md` after meaningful work is completed.
- Update `memory-bank/techContext.md` when technical constraints, commands, architecture, or conventions change.
- Update `memory-bank/projectbrief.md` only for stable project purpose or scope changes.
- Keep memory entries concise; do not paste raw logs, large diffs, secrets, or temporary scratch notes.
- Do not promote unverified observations into permanent rules or Skills; evaluate them with `/ai-learning-curator` first.

## Safety Rules

- Do not store secrets, tokens, credentials, private keys, or personal data in repository files.
- Do not overwrite user changes without explicit permission.
- Do not delete or reset files unless explicitly requested.
- When a task touches GitHub publishing, inspect `git status` and avoid staging unrelated changes.
- Prefer explicit file paths when staging changes.
- For Git commits and pushes, use `/git-commit-workflow`; default to local featureBranch -> remote featureBranch, and never force push or run destructive Git commands without explicit approval.
- For template-only Git work, use `/template-commit-workflow`; default to `feature#template#<number>` and stage only template-scope files.
