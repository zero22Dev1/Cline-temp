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

- Skills are selected automatically from their frontmatter descriptions and loaded through Cline's Skill mechanism. Do not treat Skill names as Slash Commands.
- Slash Commands in this repository are only the `.md` files under `.clinerules/workflows/`, invoked as `/<workflow-name>.md`.
- For report-only Skill evaluation, use Skill `cline-skill-evaluator`; for an accepted creation or repair, use Skill `cline-skill-builder` in a separate step.
- For normal code review, use Skill `review-loop`; use Skill `loop-verifier` only when an explicit acceptance decision is required.
- For the complete source-to-HTML-to-XLSM flow, invoke `/source-to-verified-xlsm.md`; use `/source-to-xlsm-template.md` only when the HTML and mapping inputs are already ready.
- For large PDF evidence, invoke `/pdf-context-conversion.md`, read its index first, and load only relevant chunks; keep the original PDF as the source of truth.
- For Teams completion alerts, invoke `/teams-completion-notification.md` only after its plan or implementation completion gates pass; never store the webhook URL in repository files.
- For template Git publication, use Skill `template-commit-workflow`; use Skill `git-commit-workflow` for other feature-branch commits.
- Use a parent Workflow when several Skills must run in a fixed order. Otherwise, describe the task naturally and allow Cline to activate the matching Skill.

## Planning And Clarification

- Do not implement when business rules, acceptance criteria, or scope are materially unclear.
- If uncertainty can change behavior or cause rework, clarify first with Skill `grill-with-docs`.
- If uncertainty can be listed independently, record it with Skill `unknown-list-extractor`.
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
- Use Skill `loop-verifier` when the result needs an explicit approval decision rather than a normal review summary.

## Memory Bank Rules

- Update `memory-bank/activeContext.md` when the current focus, decisions, blockers, or next steps change.
- Update `memory-bank/progress.md` after meaningful work is completed.
- Update `memory-bank/techContext.md` when technical constraints, commands, architecture, or conventions change.
- Update `memory-bank/projectbrief.md` only for stable project purpose or scope changes.
- Keep memory entries concise; do not paste raw logs, large diffs, secrets, or temporary scratch notes.
- Do not promote unverified observations into permanent rules or Skills; evaluate them with Skill `ai-learning-curator` first.

## Safety Rules

- Do not store secrets, tokens, credentials, private keys, or personal data in repository files.
- Do not overwrite user changes without explicit permission.
- Do not delete or reset files unless explicitly requested.
- When a task touches GitHub publishing, inspect `git status` and avoid staging unrelated changes.
- Prefer explicit file paths when staging changes.
- For Git commits and pushes, use Skill `git-commit-workflow`; default to local featureBranch -> remote featureBranch, and never force push or run destructive Git commands without explicit approval.
- For template-only Git work, use Skill `template-commit-workflow`; default to `feature#template#<number>` and stage only template-scope files.
