# Documentation Guide

Use this page to find the right document without needing to understand the whole publishing pipeline first.

## For authors and editors

1. [Google Doc formatting guide](google-doc-formatting-guide.md) — prepare source material without rewriting authored claims.
2. [Source format contract](source-format.md) — understand recognized headings, markers, provenance, and publication classes.
3. [Normalized Markdown contract](normalized-markdown.md) — directly author or review the canonical build input.

## For implementers

Read these in order before changing pipeline behavior:

1. [Normalized Markdown contract](normalized-markdown.md)
2. [IR schema conventions](ir-schema.md) and the executable [`schema/teaching-zine-ir.schema.json`](../schema/teaching-zine-ir.schema.json)
3. [Document grammar](grammar.md)
4. [Component contracts](component-contracts.md)
5. [Pagination contract](pagination-contract.md)
6. [Validation catalog](validation-catalog.md)

The [rendering environment](rendering-environment.md), [design system](design-system.md), and [static web edition contract](web-edition-contract.md) define output-specific behavior.

## For reviewers and contributors

- [Roadmap](roadmap.md) — current scope and planned milestones.
- [AI-assisted development policy](ai-assisted-development.md) — appropriate use, disclosure, and human-review requirements.
- [AI assistance log](ai-assistance-log.md) — material AI-supported changes already recorded in the repository.
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — change, test, and pull-request workflow.

## Authority and scope

The root [README](../README.md#contract-precedence) defines normative precedence. The visual prototype is reference material only; it cannot override semantic, pagination, provenance, or validation contracts.

The project is still staged by milestone. Contracts and the working Artwork Fire renderer are present today. A production canonical Markdown parser, Google Docs adapter, packaged CLI, and full editorial workflow remain roadmap work unless their status is explicitly updated.
