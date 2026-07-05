---
name: cline-skill-builder
description: Create, convert, improve, or review Cline Skills. Use when making a new Cline skill, converting Claude/Cursor/Codex skills to Cline, fixing skill discovery issues, or designing reusable workflows as Cline skills.
---

# Cline Skill Builder

Create focused Cline Skills that are easy to trigger and safe to maintain.

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
- Reviewing whether a Skill is too broad, vague, or heavy
- Splitting a large `.clinerules` file into smaller Skills
- Designing supporting `docs/`, `templates/`, or `scripts/` for a Skill
- Fixing a Skill that does not appear or appears with the wrong slash command

## Do Not Use This Skill For

- Always-on project constraints that belong in `.clinerules`
- Long-term project memory that belongs in `memory-bank/`
- One-time advice that does not need reuse
- Normal source code changes

## Creation Process

1. Clarify the task the Skill performs.
2. Define when Cline should use it and when it should not.
3. Choose a lowercase kebab-case name.
4. Write a specific `description` with trigger phrases.
5. Keep `SKILL.md` focused and move detailed references to supporting files.
6. Include concrete examples for invocation and expected output.
7. Check that the path is `.cline/skills/<skill-name>/SKILL.md`.

## Output Format

When creating or reviewing a Skill, provide:

- Recommended location
- Final `SKILL.md`
- Optional supporting files
- Invocation examples
- Notes about overlap with existing Skills

