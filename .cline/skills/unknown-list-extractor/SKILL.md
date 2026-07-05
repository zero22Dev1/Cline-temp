---
name: unknown-list-extractor
description: Extract unknowns, ambiguities, assumptions, risks, and confirmation items from source code, specs, diffs, requirements, or generated documents. Use when creating an unknown list, review checklist, or clarification list.
---

# Unknown List Extractor

Extract and organize unknowns, ambiguities, assumptions, risks, and confirmation items.

## Purpose

Create a structured list of items that must be confirmed before implementation, migration, documentation, or delivery. This skill does not resolve unknowns by guessing.

## Use This Skill When

- Creating an unknown list
- Extracting confirmation items
- Reviewing unclear specifications
- Finding missing requirements
- Identifying assumptions
- Checking risks before implementation
- Preparing questions for a customer, senior engineer, or reviewer
- Reviewing generated specs for gaps
- Reviewing existing source before migration

## Do Not Use This Skill For

- Full specification writing
- Code implementation
- HTML artifact checking only
- Refactoring
- Bug fixing

For full source-to-spec documentation, use the `legacy-source-spec-writer` skill behavior. For HTML coverage checking, use the `html-artifact-checker` skill behavior.

## Inputs To Check

- README
- Existing docs
- `memory-bank/`
- `docs/ai/`
- `docs/specs/`
- Relevant source files
- Current diffs, if present

## Output Location

Write unknown lists under:

```txt
docs/ai/unknowns/
```

Recommended filename:

```txt
docs/ai/unknowns/YYYYMMDD-<topic>-unknowns.md
```

## Severity Levels

- `Critical`: Blocks implementation or may cause major data loss, security, or business failure.
- `High`: Likely to cause rework or incorrect behavior.
- `Medium`: Should be clarified, but work can continue with a documented assumption.
- `Low`: Nice to clarify, mostly wording, naming, or minor edge behavior.

## Output Template

```md
# Unknowns: <Topic>

## Summary

## Critical

| ID | Unknown | Evidence | Impact | Question | Owner |
|---|---|---|---|---|---|

## High

| ID | Unknown | Evidence | Impact | Question | Owner |
|---|---|---|---|---|---|

## Medium

| ID | Unknown | Evidence | Impact | Question | Owner |
|---|---|---|---|---|---|

## Low

| ID | Unknown | Evidence | Impact | Question | Owner |
|---|---|---|---|---|---|

## Assumptions Not Yet Confirmed

## Recommended Next Step
```

## Evidence Rules

- Include source paths, spec sections, or diff references.
- Do not resolve unknowns by guessing.
- Separate unknowns from assumptions.
- Prefer concrete questions that can be answered.

