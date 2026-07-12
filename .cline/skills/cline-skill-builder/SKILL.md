---
name: cline-skill-builder
description: Create, convert, or improve Cline Skills after an evaluation or explicit creation request. Use when implementing accepted Skill findings, making a new Skill, converting Claude/Cursor/Codex instructions to Cline, fixing discovery issues, or splitting reusable procedures from Rules. Do not use for report-only Skill evaluation.
---

# Cline Skill Builder

Create focused Cline Skills that are easy to trigger and safe to maintain.

独立したreport-only評価には`cline-skill-evaluator`を使用する。このSkillは、評価後に承認されたSkillの作成・修正・分割を担当する。

## Valid Structure

A Cline Skill should use this structure:

```txt
.cline/
└─ skills/
   └─ skill-name/
      └─ SKILL.md
```

`SKILL.md` must start with YAML frontmatter:

```md
---
name: skill-name
description: Clear description of what this skill does and when Cline should use it.
---
```

The `name` must exactly match the parent directory name.

## Use This Skill When

- Creating a new Cline Skill
- Converting a prompt, rule, checklist, Claude Skill, Cursor rule, or Codex workflow into a Cline Skill
- Implementing accepted findings from `cline-skill-evaluator`
- Splitting a large `.clinerules` file into smaller Skills
- Designing supporting `docs/`, `templates/`, or `scripts/` for a Skill
- Fixing a Skill that is not discovered or does not activate for intended prompts

## Do Not Use This Skill For

- Always-on project constraints that belong in `.clinerules`
- Long-term project memory that belongs in `memory-bank/`
- One-time advice that does not need reuse
- Normal source code changes
- Report-only Skill evaluation; use `cline-skill-evaluator`

## Creation Process

1. Clarify the task the Skill performs.
2. Define when Cline should use it and when it should not.
3. Choose a lowercase kebab-case name.
4. Write a specific `description` with trigger phrases.
5. Keep `SKILL.md` focused and move detailed references to supporting files.
6. Include concrete examples for invocation and expected output.
7. Check that the path is `.cline/skills/<skill-name>/SKILL.md`.

## Output Format

When creating or updating a Skill, provide:

- Recommended location
- Final `SKILL.md`
- Optional supporting files
- Invocation examples
- Notes about overlap with existing Skills
