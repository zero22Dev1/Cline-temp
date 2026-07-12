---
name: legacy-source-spec-writer
description: Create Markdown specifications from existing source code. Use when documenting current behavior, reverse-engineering features, summarizing legacy source, or preparing specs before migration or refactoring.
---

# Legacy Source Spec Writer

Create accurate Markdown specifications from existing source code.

## Purpose

Reverse-engineer current behavior from source code and produce a clear specification document. This skill is for documentation only. Do not modify source code.

## Use This Skill When

- Creating a specification from existing source code
- Understanding current behavior before refactoring
- Documenting legacy code
- Preparing for migration
- Explaining business logic from source
- Creating handover documentation
- Creating specs for VB.NET, Java, BHT BASIC, JavaScript, TypeScript, SQL, batch files, or server configuration

## Do Not Use This Skill For

- Code implementation
- Refactoring
- Bug fixes
- Test creation
- HTML artifact checking
- Unknown-only extraction

For unknown-only extraction, use the `unknown-list-extractor` skill behavior.

## Inputs To Check

- Source files related to the requested feature
- README and existing docs
- `memory-bank/projectbrief.md`
- `memory-bank/activeContext.md`
- `memory-bank/techContext.md`
- `memory-bank/progress.md`
- `docs/ai/glossary.md`
- `docs/ai/active-context.md`
- `docs/ai/adr/`

## Output Location

Write specs under:

```txt
docs/specs/
```

Recommended filename:

```txt
docs/specs/<feature-name>.md
```

## Spec Template

Use this structure:

```md
# <Feature Name> Specification

## 1. Overview
## 2. Source Files Reviewed
## 3. Requirement Traceability

| REQ-ID | Category | Confirmed Behavior | Source Evidence | Confidence |
|---|---|---|---|---|

## 4. Current Behavior
## 5. User Flow
## 6. Inputs
## 7. Outputs
## 8. Data Model
## 9. Validation Rules
## 10. Error Handling
## 11. External Dependencies
## 12. Edge Cases
## 13. Known Unknowns
## 14. Business Rules
## 15. Notes For Future Implementation
```

## Evidence Rules

- Cite file paths and function/class names when possible.
- Assign stable `REQ-<number>` IDs to confirmed behavior and keep the same IDs in downstream HTML, manifests, tests, and review matrices.
- Record one or more source file and symbol references for each REQ-ID.
- Mark uncertain behavior as `Unknown`.
- Do not invent requirements that are not visible in source or docs.
- Separate observed behavior from inferred intent.

## Final Response

Report:

- Spec file created or updated
- Files reviewed
- Unknowns found
- Recommended next step
