# Rendering and Print Environment

## Candidate renderer

WeasyPrint is the Milestone 0 candidate because it supports paged-media CSS and integrates with Python. Its adoption is provisional until the prototype demonstrates fixed half-letter pages, embedded fonts, deterministic pagination, fragmentation behavior, and page-turn invariants. The accepted exact version is then pinned in the build lockfile and metadata.

## Reader contract

- Trim size: 5.5 by 8.5 inches, portrait.
- Content box, folios, and running matter are controlled by print CSS.
- Fonts are distributable files bundled with the build; environment fonts are forbidden.
- Body type is never below 9.5 pt.
- Provenance/small type is never below 8 pt.
- Text line height is never below 1.2.
- Reader PDFs embed their fonts and record renderer/style versions in metadata.

The prototype uses broadly available fallback fonts only to test geometry. Font family and final type scale are not approved until a printed prototype is reviewed.

## Booklet contract

Provisional physical configuration:

- Sheet: US Letter, 11 by 8.5 inches, landscape.
- Placement: two half-letter portrait reader pages per side.
- Binding: left fold.
- Duplex: flip on short edge.
- Scale: 100%; never fit-to-page.
- Padding: append blanks until reader page count is divisible by four.

An eight-page fixture numbered prominently on both faces must be printed, duplexed, folded, and read in order. The verified orientation and imposition sequence become normative. Creep, bleed, crop marks, and printer-specific non-printable margins are out of scope for v1 unless physical testing makes one necessary.

## Build identity

A reproducible build records input digest, schema version, style digest, renderer and Python versions, font digests, page count, page map, and validation results. Determinism means equivalent pagination and rendered content, not necessarily byte-identical PDF serialization.

