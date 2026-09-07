# Decision-Based Teaching Zine Generator - Milestone 0

Status: contract baseline for review. This package deliberately stops before the production Google Docs adapter and full renderer.

[![Validate contracts](https://github.com/kasittig/decision-based-teaching-zine/actions/workflows/validate.yml/badge.svg)](https://github.com/kasittig/decision-based-teaching-zine/actions/workflows/validate.yml)

## Purpose

Milestone 0 fixes the semantic, validation, pagination, and publication contracts so an implementer does not have to invent product rules.

## Contents

- `docs/source-format.md` - Google Docs recognition and normalization rules
- `docs/ir-schema.md` - IR v1 conventions and relationships
- `docs/grammar.md` - legal document and decision-cycle ordering
- `docs/component-contracts.md` - publication behavior and splitting policy
- `docs/pagination-contract.md` - page-turn invariants and layout priorities
- `docs/validation-catalog.md` - stable error/warning codes
- `docs/rendering-environment.md` - provisional renderer and print contract
- `schema/teaching-zine-ir.schema.json` - executable JSON Schema
- `fixtures/` - canonical and malformed normalized-source examples
- `expected/` - expected IR, validation, and page-map examples
- `prototype/` - one-decision HTML/CSS print prototype
- `output/pdf/one-decision.pdf` - rendered half-letter prototype

## Quick start

```bash
python scripts/validate_contracts.py
```

Then open `output/pdf/one-decision.pdf` and print at 100% scale for the visual review. No production generator exists yet; see `docs/roadmap.md`.

## Contributing and AI assistance

See `CONTRIBUTING.md` for the change workflow, `AGENTS.md` for coding-agent instructions, and `docs/ai-assisted-development.md` for disclosure, privacy, verification, and human-review expectations.

## Normative hierarchy

If materials disagree, precedence is:

1. JSON Schema for data shape.
2. Grammar and component contracts for semantic legality.
3. Pagination contract for page placement.
4. Validation catalog for diagnostic severity.
5. Prototype for visual direction only.

## Frozen decisions

- Google Docs remains the editorial source of truth.
- Adapters emit normalized source; the publication core never reads Google Docs directly.
- Ambiguity produces diagnostics, not silent inference.
- Every standard decision has exactly one reveal container.
- A boundary ends the decision page; its reveal is the first substantive component on the next page.
- `DEVELOPMENT NOTES` is terminal and unpublished.
- Content is never shortened to solve pagination.

## Provisional decisions requiring physical review

- WeasyPrint is the candidate renderer and must be pinned after prototype approval.
- Exact fonts and sizes remain provisional until print review; hard minimums are binding.
- Booklet duplex is landscape Letter, left fold, flip on short edge, pending the numbered physical test.
