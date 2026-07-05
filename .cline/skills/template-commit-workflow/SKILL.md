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

- `.cline/skills/**/SKILL.md`
- `.clinerules/**`
- `README.md`
- `docs/skills-usage.md`
- `docs/ai/**`
- `docs/specs/**`
- `docs/reviews/**`
- `memory-bank/**`
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
4. If unrelated files exist, ask which files should be included.
5. Confirm or choose the feature branch.
6. If on `main`, create a branch:
   - `git switch -c feature#template#<number>`
7. If already on the intended feature branch, stay there.
8. Stage only intended template files with explicit paths.
9. Re-check `git status -sb`.
10. Commit with a concise template-focused message.
11. Push to the matching remote feature branch:
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
- Each `SKILL.md` has only `name` and `description` frontmatter.
- Skill directory name matches the `name`.
- README and `docs/skills-usage.md` list newly added Skills.
- `.clinerules/` references the relevant workflow rules.
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

