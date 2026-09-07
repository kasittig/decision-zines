# Roadmap

## Milestone 0 - Contracts

- Approve the source, IR, grammar, component, pagination, and validation contracts.
- Print and review the one-decision prototype.
- Select and pin the rendering engine and fonts.
- Print, fold, and approve an eight-page imposition fixture.

## Milestone 1 - Local publishing core

- Parse canonical `.zine.md` fixtures into IR.
- Build directly from normalized Markdown without credentials or network access.
- Validate structural and relationship rules.
- Render deterministic reader PDFs from the shared component library.
- Generate page maps, contact sheets, and booklet-imposed PDFs.
- Add the Severe Weather and Safety regression fixtures.

## Milestone 2 - Google Docs adapter

- Read heading styles, paragraphs, lists, and source positions.
- Emit canonical, versioned `.zine.md` plus a source-map sidecar.
- Make repeated imports stable and reviewable in Git diffs.
- Produce actionable diagnostics linked to source locations.
- Confirm that adapter behavior does not leak into the publication core.

## Milestone 3 - Editorial workflow

- Add review reports and visual-regression approval.
- Define schema migrations and compatibility guarantees.
- Package the `zine build` command for reproducible local and CI use.
