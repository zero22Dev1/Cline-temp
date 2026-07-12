---
name: template-commit-workflow
description: Commit and push Cline template changes safely. Use when the user asks to commit template updates, Cline skills, .clinerules, README, docs, memory-bank, usage docs, or starter/template files to Git using a local featureBranch such as feature#template#1 and matching remote featureBranch.
---

# Template Commit Workflow

Commit Cline template changes safely through a feature branch.

## Purpose

This skill is a narrower workflow than `git-commit-workflow`. Use it when the intended changes are template-level files for this Cline setup, not application source code.

Default flow:

```txt
local featureBranch -> remote featureBranch
```

Do not commit directly to `main` unless the user explicitly requests it.

## Template Scope

Template files commonly include:

- `.cline/skills/**` including `SKILL.md`, `scripts/`, `tests/`, `references/`, `docs/`, `templates/`, and `assets/`
- `.clinerules/**`
- `.clineignore`
- `README.md`
- `docs/skills-usage.md`
- `docs/workflows/**`
- `docs/ai/**`
- `docs/specs/**`
- `docs/reviews/**`
- `memory-bank/**`
- `templates/**`
- `outputs/**` when the output is part of the template deliverable

Do not include unrelated application source, secrets, local environment files, build artifacts, or editor cache files.

## Branch Naming

Use this format:

```txt
feature#template#<number>
```

Examples:

```txt
feature#template#1
feature#template#2
docs#template#1
```

If the user writes `/feature#template#1`, treat the leading `/` as chat notation and use `feature#template#1` as the actual Git branch name.

When selecting `<number>`, inspect existing local and remote branches with the same name prefix and use the next number.

## Process

1. Run `git status -sb`.
2. Inspect unstaged and staged diffs:
   - `git diff`
   - `git diff --staged`
3. Confirm changes are template-scope files.
4. Inspect untracked files under every changed Skill directory so support files are not omitted.
5. If unrelated files exist, ask which files should be included.
6. Confirm or choose the feature branch.
7. If on `main`, create a branch:
   - `git switch -c feature#template#<number>`
8. If already on the intended feature branch, stay there.
9. Stage only intended template files with explicit paths. For a changed Skill, stage the intended Skill directory rather than only its `SKILL.md`.
10. Re-check `git status -sb` and confirm no intended support file remains untracked or unstaged.
11. Commit with a concise template-focused message.
12. Push to the matching remote feature branch:
   - `git push -u origin feature#template#<number>`

## Suggested Commit Messages

Use messages like:

```txt
add cline template skills
update cline template usage docs
add loop engineering cline skills
update template commit workflow
```

Avoid vague messages:

```txt
update
fix
misc
changes
```

## Verification Before Commit

Check:

- Each new Skill has `.cline/skills/<name>/SKILL.md`.
- Every referenced `scripts/`, `tests/`, `references/`, `docs/`, `templates/`, and `assets/` file exists and is included when intended.
- Each `SKILL.md` has only `name` and `description` frontmatter.
- Skill directory name matches the `name`.
- README and `docs/skills-usage.md` list newly added Skills.
- `.clinerules/` references the relevant workflow rules.
- `.clineignore`, `templates/**`, and `docs/workflows/**` changes are included when they belong to the template update.
- `git status --short` contains no untracked file inside an intended changed Skill or Workflow directory.
- `memory-bank/progress.md` records meaningful template updates.

## Safety Rules

- Never use `git add -A` when unrelated files may exist.
- Prefer explicit paths.
- Do not include credentials, tokens, private keys, or local config.
- Do not force push.
- Do not overwrite user changes.
- Do not push directly to `main` unless explicitly requested.
- If remote contains new work, fetch and inspect before merging.

## Final Response Format

```md
## Template Git Result

- Branch:
- Commit:
- Remote:
- Push:
- Included files:
- Excluded files:
- Notes:
```
