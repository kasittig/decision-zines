# Design System Baseline

Status: grayscale laser-printer baseline pending physical print review.

## Character

The zine is an operational field guide with independent-editorial energy: direct, compact, grayscale-only, toner-conscious, and photocopy resilient. Graphic devices encode meaning. Decoration without a semantic job is excluded.

## Tokens

| Token | Prototype value | Purpose |
|---|---:|---|
| Ink | `#000000` | Type, rules, committed states |
| Paper | `#ffffff` | Page and reversed type |
| Pale gray | `#f2f2f2` | Quiet fields and commit bands |
| Light gray | `#d9d9d9` | Decision and teaching labels |
| Mid gray | `#999999` | Secondary rules |
| Dark gray | `#4d4d4d` | Compact committed labels; replaces large solid-black fills |
| Rule | `1pt` | Ordinary component boundary |
| Heavy rule | `3pt` | Part, decision, and teaching boundaries |
| Body minimum | `10.5pt` | Binding readability floor |
| Support minimum | `9pt` | Supporting prose and source entries |
| Label minimum | `8.5pt` | Short provenance and navigation labels only |

The reference PDF embeds DejaVu Sans and DejaVu Sans Bold exclusively. The prototype therefore bundles and uses those same faces. Font files and their license notice live under `assets/fonts/`. Final sizes remain subject to physical print review.

## Page grid

- Half-letter portrait reader page.
- Single-column content region with a target line length below 70 characters.
- Cover composition centered horizontally and placed slightly above the page's geometric midpoint for optical balance after folding.
- Running part/role header above a heavy rule.
- Scenario content in source order.
- Commit treatment above the running timeline.
- Folio centered below the timeline.

## Visual hierarchy

1. Decision or reveal headline.
2. Decision/commit and primary evidence.
3. Plan, context, and teaching interpretation.
4. Provenance, navigation, and running information.

The decision/commit axis is the expressive center. All other components remain rectilinear and disciplined.

## Component language

- **Content note:** heavy outlined field with the standard DejaVu warning-triangle glyph, a black reverse label, and a gray message cell. Conspicuous and familiar, not a normal heading.
- **Semantic card:** the single reusable component for provenance definitions and in-story evidence. Its HTML anatomy is always title plus body. The renderer supplies `kind`, `title`, and `body`; modifier classes parameterize title background, title color, outer rule style, and title-rule style through CSS custom properties.
- **Provenance vocabulary:** four full-width semantic cards in a single vertical reading sequence. All cards share one structure and identical width; the container controls only the one-column stack and spacing.
- **Context:** open text with a heavy left rule, representing present conditions and available knowledge.
- **Plan:** enclosed gray field explicitly glossed as what the system expected.
- **Decision:** one high-contrast skim landmark: a light-gray `WHAT DO YOU DO?` banner bounded by a heavy black rule, an enclosed option field, and compact dark-gray alphabetical markers with equal visual weight.
- **Boundary:** an attached gray commit footer separated by a heavy rule; it ends the reader page and completes the decision component.
- **Reveal:** headline followed by tabular evidence blocks.
- **Documented:** dark-gray provenance cell with reversed text.
- **Recollected:** light-gray title band above a white body inside a simple solid frame. The restrained fill treatment evokes a retained human account and stays distinct on a black-and-white laser printer without ranking the evidence as correct or incorrect.
- **Unknown:** unfilled white title and body with a heavier dashed perimeter and dashed separator, leaving the state visibly open and unresolved.
- **Teaching scenario:** pale-gray cell with a double boundary.
- **Teaching lesson:** a fully enclosed panel with a light-gray label band above a full-width interpretation body; the continuous outer border keeps the entire lesson visibly grouped without narrowing the teaching text. A second heading appears only when the author supplies a topic in `TEACHING LESSON - [topic]`; the bare form does not generate a redundant fallback heading.
- **Timeline:** the foundation chronology is a dedicated vertical five-step sequence with numbered nodes, a continuous rail, and distinct phase labels. Compact scenario navigation may use a horizontal rule; its active phase uses a filled node and bold label.

## Running timeline contract

The foundation timeline introduces the story phases on its own page, preserving each Markdown bullet as a separate chronological step. Scenario pages may repeat a compact running timeline with the current phase emphasized. It is navigational and must not name or imply an unrevealed outcome. Phase labels come from semantic timeline data rather than hard-coded stylesheet text.

## Grayscale output contract

All design tokens use equal red, green, and blue channels. When Ghostscript is available, the formatter additionally rewrites the reader PDF into the explicit `DeviceGray` color space before booklet imposition. Recollected content uses an unfilled field and a double black rule, avoiding color-managed gray and fragile halftone patterns entirely.

## Print review questions

- Does 9.5pt body text remain comfortable after duplex printing and folding?
- Do all four provenance states remain distinguishable in draft-quality grayscale printing?
- Are solid dark fills limited enough to avoid toner-heavy pages and curling?
- Is ordinary prose at least `10.5pt`, with support text at least `9pt` and short labels at least `8.5pt`?
- Do evidence and teaching components preserve a comfortable full-width reading measure?
- Is the alert tile friendly enough without trivializing the subject?
- Does the decision page provide useful writing/consideration space rather than accidental emptiness?
- Does the commit treatment remain visible near common printer non-printable margins?
