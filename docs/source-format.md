# Source Format Contract

## Pipeline boundary

The Google Docs adapter converts a Google Doc into versioned normalized Markdown (`.zine.md`). Local fixtures and direct-authored Markdown enter at that same boundary. Downstream stages must not depend on Google APIs, document styles, or editor-specific identifiers. The complete Markdown syntax is defined in `normalized-markdown.md`.

Normalized Markdown is persisted as a build artifact rather than passed as an invisible in-memory representation. It can be inspected, diffed, committed, validated, and rebuilt independently of Google Docs. Shared boilerplate is omitted from this artifact and injected from the exact template version declared in front matter.

## Recognition hierarchy

1. Google Docs heading styles identify candidate structural headings.
2. Normalized, exact heading text selects the semantic component.
3. Paragraph prefixes identify provenance and decision options.
4. Reserved semantic markers remain authoritative even when styled incorrectly.

Text normalization trims outer whitespace, collapses internal runs of ordinary spaces, normalizes line endings, and compares reserved labels case-insensitively. It does not rewrite published prose.

If style and recognized text disagree, preserve the recognized semantic meaning and emit `W101_STYLE_TEXT_MISMATCH`. Unrecognized heading-like text emits `W102_UNKNOWN_HEADING`; it is never silently mapped to the nearest component.

## Reserved headings and markers

Foundation: title, `A Decision-Based Teaching Reconstruction`, `HOW TO READ THIS`, `PROVENANCE VOCABULARY`, optional `CONTENT NOTE`, `INTENT`, `WHO ARE YOU?`, `ROLES IN THIS STORY`, and `TIMELINE`.

Scenario: `PART [number] - YOU ARE [role]`, `CONTEXT`, `CONTEXT - [topic]`, `THE PLAN`, `THE PLAN - [topic]`, `WHAT DO YOU DO?`, `TEACHING DECISION - [topic]`, `DECISION BOUNDARY`, `WHAT THE RECORD SHOWS`, `WHAT THE RECORD SHOWS - [outcome]`, `THE PLAN ENDS HERE`, `UNKNOWN`, `TEACHING LESSON - [topic]`, and `TEACHING QUESTION`.

Closing: `LOOK BACK AT YOUR DECISIONS`, `LESSONS - [theme]`, `PRIVACY, SOURCES & CONTRIBUTIONS`, and `SOURCES`.

Optional supporting headings are those listed in the project brief. Unknown additions receive diagnostics and require an explicit contract change before publication.

## Paragraph prefixes

- Provenance: `DOCUMENTED:`, `RECOLLECTED:`, `UNKNOWN:`, `TEACHING SCENARIO:`.
- Options: `A.`, `B.`, `C.` and subsequent single Latin letters followed by a period.
- Optional pinned ID metadata: `[ID: decision-stable-name]`. This line is metadata and is not published.

Options must be consecutive paragraphs immediately following a decision prompt. At least one labeled option or one explicit free-response instruction is required. Visual styling must not privilege any option.

## Stable identifiers

An explicit pinned ID wins. Otherwise, a decision ID is `decision-` plus the slug of its identifying title or prompt. Duplicate slugs receive deterministic suffixes `-2`, `-3`, and so on within the document. Inserting unrelated earlier content does not alter a unique slug. Editing the identifying text may alter an unpinned ID.

IDs match `^[a-z][a-z0-9-]*$` and are unique document-wide.

## Source locations

Every normalized node retains, when available: document ID, structural-element index, paragraph index, UTF-16 text start/end offsets, observed style, and recognized heading. Local fixtures retain file path and 1-based line numbers.

## Publication classes

- `published`: emitted verbatim except typographic normalization explicitly approved by editorial policy.
- `transform`: semantic marker converted to reader-facing treatment, such as a boundary.
- `metadata`: IDs, relationships, and source locations.
- `editorial`: excluded from publication.

`DEVELOPMENT NOTES` is terminal. It and every following element are editorial and excluded. The adapter should warn if required closing sections occur only after that marker.
