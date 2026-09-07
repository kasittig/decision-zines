# Contributing

Thank you for helping build a reliable publishing system for decision-based teaching material.

## Before opening a change

- Read the contract documents in `docs/`.
- Open an issue for changes to grammar, provenance, pagination, or source authority.
- Keep editorial claims separate from renderer behavior.
- Use synthetic or permission-cleared material in public fixtures.

## Pull requests

A pull request should state:

1. The problem being solved.
2. The contract and fixture affected.
3. Whether pagination or visual output changes.
4. Validation commands run.
5. Whether AI assistance was used and how the result was verified.

Semantic changes require a fixture and expected result. Visual changes require before/after page images or a contact sheet. Contract changes require an explicit rationale and must not be bundled invisibly with implementation work.

## Commit style

Use short imperative subjects, such as:

- `Define mixed-provenance reveal contract`
- `Add missing-boundary validation fixture`
- `Prevent reveal placement on decision page`

## Reporting issues

Include the smallest source example that reproduces the problem, expected and actual diagnostics, renderer/version information, and affected page numbers. Remove private or identifying information before submission.

