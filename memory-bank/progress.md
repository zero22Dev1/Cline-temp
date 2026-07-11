# Progress

## Done

- Created Cline workspace directory structure.
- Added initial Cline Skills:
  - `cline-skill-builder`
  - `legacy-source-spec-writer`
  - `unknown-list-extractor`
  - `html-artifact-checker`
- Added initial `memory-bank/` files.
- Added `docs/ai/`, `docs/specs/`, and `docs/reviews/` structure.
- Added workflow-specific always-on rules in `.clinerules/cline-loop-engineering.md`.
- Added `git-commit-workflow` skill for `feature#na#1` style local featureBranch to remote featureBranch commit/push workflow.
- Added `docs/skills-usage.md` with usage examples for each Cline Skill.
- Added `loop-budget`, `loop-triage`, and `loop-verifier` skills adapted for Cline loop workflows.
- Added `daily-triage` and `issue-triage` skills adapted from loop-engineering patterns for report-only Cline workflows.
- Added `template-commit-workflow` skill for committing Cline template updates via `feature#template#<number>` branches.
- Added `adaptive-deep-planning` as a parent Skill that classifies requests and routes only the necessary planning Skills.
- Added `artifact-quality-gate` as a parent Skill for artifact-specific checks, scoring, repair loops, and completion decisions.
- Added matching Cline Workflows in `.clinerules/workflows/` for adaptive planning and artifact quality gating.
- Added mirrored Workflow usage documentation under `docs/workflows/`.
- Added `ai-learning-curator` for evidence-based continuous project learning and safe promotion into memory, ADRs, rules, and Skills.
- Added `continuous-project-learning` Workflow to convert validated lessons into maintainability, performance, reliability, and quality improvements.
- Added harness engineering knowledge, Skill, Workflow, and usage guidance for bounded artifact iteration with observable feedback and durable learning.
- Added context window management knowledge, Skill, Workflow, and usage guidance for progressive loading, evidence-preserving checkpoints, context refresh, and reliable handoffs.

## Pending

- Validate Skill discovery in Cline.
- Add real project specs and unknown lists.
