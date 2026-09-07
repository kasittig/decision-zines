# Design System Baseline

Status: prototype baseline pending physical print review and final font selection.

## Character

The zine is an operational field guide with independent-editorial energy: direct, compact, monochrome, and photocopy resilient. Graphic devices encode meaning. Decoration without a semantic job is excluded.

## Tokens

| Token | Prototype value | Purpose |
|---|---:|---|
| Ink | `#000000` | Type, rules, committed states |
| Paper | `#ffffff` | Page and reversed type |
| Wash | `#eeeeeb` | Plans and caution fields |
| Mid | `#a6a6a1` | Secondary rules |
| Rule | `1pt` | Ordinary component boundary |
| Heavy rule | `3pt` | Part, decision, and teaching boundaries |
| Body minimum | `9.5pt` | Binding readability floor |
| Small minimum | `8pt` | Provenance and support labels |

The reference PDF embeds DejaVu Sans and DejaVu Sans Bold exclusively. The prototype therefore bundles and uses those same faces. Font files and their license notice live under `assets/fonts/`. Final sizes remain subject to physical print review.

## Page grid

- Half-letter portrait reader page.
- Narrow single-column content region.
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

- **Content note:** gray horizontal field with a slightly rotated black alert tile. Friendly and conspicuous, not a normal heading.
- **Context:** open text with a heavy left rule, representing present conditions and available knowledge.
- **Plan:** enclosed gray field explicitly glossed as what the system expected.
- **Decision:** large compressed headline followed by evenly weighted ruled options.
- **Boundary:** heavy rules and direct commit language; it ends the reader page.
- **Reveal:** headline followed by tabular evidence blocks.
- **Documented:** solid black provenance cell.
- **Recollected:** diagonal-line provenance cell. It remains distinct in grayscale without ranking the evidence as correct or incorrect.
- **Teaching lesson:** black semantic rail beside a separate interpretation body; it never masquerades as evidence.
- **Timeline:** a persistent five-phase navigation rule. The active phase uses a filled node and bold label.

## Running timeline contract

The foundation timeline introduces the story phases. Scenario pages may repeat a compact running timeline with the current phase emphasized. It is navigational and must not name or imply an unrevealed outcome. Phase labels come from semantic timeline data rather than hard-coded stylesheet text.

## Print review questions

- Does 9.5pt body text remain comfortable after duplex printing and folding?
- Does the Recollected hatch reproduce cleanly on ordinary office copiers?
- Is the alert tile friendly enough without trivializing the subject?
- Does the decision page provide useful writing/consideration space rather than accidental emptiness?
- Does the commit treatment remain visible near common printer non-printable margins?
