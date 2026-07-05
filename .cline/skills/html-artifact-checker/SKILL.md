---
name: html-artifact-checker
description: Check whether an HTML artifact correctly covers existing specifications, source-derived behavior, fields, flows, validations, errors, and edge cases. Use when reviewing generated HTML docs, mockups, or artifacts for missing requirements.
---

# HTML Artifact Checker

Check HTML artifacts against source code, specifications, and project context.

## Purpose

Verify that an HTML artifact does not miss important information from the source specification or existing implementation. This skill is for review and gap detection. Do not rewrite the HTML unless the user explicitly asks.

## Use This Skill When

- Checking an HTML artifact for missing specifications
- Comparing HTML output with Markdown specs
- Verifying whether generated HTML covers source-derived behavior
- Reviewing a mockup or HTML document before delivery
- Finding gaps between code/spec and HTML
- Checking whether labels, fields, validations, errors, branches, and edge cases are represented

## Do Not Use This Skill For

- Full source-to-spec documentation
- Unknown-only extraction
- Code implementation
- UI redesign unless explicitly requested

For source-to-spec documentation, use the `legacy-source-spec-writer` skill behavior. For unknown-only extraction, use the `unknown-list-extractor` skill behavior.

## Inputs To Check

1. HTML artifact
2. `docs/specs/`
3. `docs/ai/`
4. Relevant source files
5. README or tickets
6. `memory-bank/`

## Output Location

Write reviews under:

```txt
docs/reviews/
```

Recommended filename:

```txt
docs/reviews/YYYYMMDD-<artifact-name>-html-check.md
```

## Review Checklist

- Required fields are present
- Labels match domain terminology
- User flows are represented
- Validation rules are represented
- Error states are represented
- Business rules are represented
- Edge cases are represented
- Source-derived behavior is not contradicted
- Unknowns are listed instead of guessed

## Output Template

```md
# HTML Artifact Check: <Artifact Name>

## Summary

## Coverage Result

| Area | Status | Evidence | Notes |
|---|---|---|---|

## Missing Items

| Severity | Missing Item | Source Evidence | Recommended Fix |
|---|---|---|---|

## Contradictions

| Severity | HTML Behavior | Expected Behavior | Evidence |
|---|---|---|---|

## Unknowns

## Recommended Fix Order

## Recommended Next Step
```

## Safety Rules

- Do not modify the HTML unless explicitly asked.
- Do not assume a missing requirement is intentionally omitted.
- Mark unclear items as unknown.
- Prioritize source/spec contradictions over visual preferences.

