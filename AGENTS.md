# Agent Working Agreement

This repository is designed for careful collaboration between human editors, developers, and AI coding agents.

## Read first

Before changing behavior, read `README.md` and every contract in `docs/`. Normative precedence is documented in the README. Do not infer publication rules from the visual prototype.

## Non-negotiable invariants

- Preserve authored teaching and historical claims verbatim.
- Never alter provenance to simplify implementation or layout.
- Never place a reveal on the same reader page as its decision.
- Treat `DECISION BOUNDARY` as a transformed semantic marker, not printable source text.
- Treat `DEVELOPMENT NOTES` and everything following it as unpublished editorial content.
- Do not silently guess when Google Docs structure is ambiguous; emit a diagnostic.
- Keep Google Docs integration behind an adapter boundary.
- Treat `.zine.md` as the canonical publication-core input and preserve canonical serialization.
- Ensure builds from normalized Markdown require neither Google credentials nor network access.

## Change workflow

1. Identify the contract affected by the requested change.
2. Update or add a fixture that demonstrates the behavior.
3. Update expected IR, diagnostics, or page maps.
4. Implement the smallest conforming behavior.
5. Run `python scripts/validate_contracts.py` and relevant renderer tests.
6. Render PDFs and visually inspect every changed page.
7. Record material AI assistance as described in `docs/ai-assisted-development.md`.

Do not regenerate approved visual baselines without explaining why the output changed. Never solve overflow by deleting, summarizing, or silently shrinking source material below minimum typography.

## Scope discipline

Milestone 0 contains contracts and a proof of concept. Production parsing, rendering, Google APIs, and booklet imposition belong in later milestones. Propose contract changes explicitly rather than smuggling policy decisions into code.
