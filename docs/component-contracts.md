# Component Contracts

| Component | Publication behavior | Split policy |
|---|---|---|
| Content note | Friendly warning callout with alert icon and compact label | Atomic |
| Roles | Compact de-identified cast cards | Splittable only when oversized |
| Timeline | Foundation orientation plus optional running navigation; must not reveal outcomes | Atomic |
| Part header | Announces part, progress, and reader role | Atomic; keep with following content |
| Context | Conditions and knowledge available at decision time | Splittable |
| Plan | Box communicating prior organizational expectation | Prefer atomic; oversized may split |
| Decision | Prompt and neutral options | Prefer atomic; split only if oversized |
| Boundary | Commit/page-turn treatment; never print source marker literally | Atomic; forced break after |
| Reveal | Historical record without implying correctness | Splittable; starts new page |
| Plan ends | Strong dark bar marking the plan's limit | Atomic |
| Unknown | Visibly unresolved uncertainty | Prefer atomic |
| Teaching lesson | Subordinate interpretation treatment | Splittable |
| Closing/backmatter | Reader reflection, lessons, privacy, and sources | Splittable |

## Continuations

When a permitted component splits, subsequent fragments receive a subtle running label such as `THE PLAN - continued`. The full heading is not repeated and the continuation must not be represented as a new semantic component in the page map.

## Running timeline

Scenario pages may repeat a compact timeline derived from the canonical timeline data. The current phase is emphasized. Labels must remain orienting rather than disclose an outcome the reader has not reached.

## Oversized atomic content

If an atomic component exceeds a full content box at minimum typography, emit `E401_OVERSIZED_ATOMIC_COMPONENT` and stop. The renderer must not clip, omit, scale below minimum type, or rewrite it. A `prefer atomic` component may split only after the renderer establishes it cannot fit on an otherwise empty page.

## Provenance

Only `documented`, `recollected`, `unknown`, and `teaching_scenario` are valid. Their labels must remain visibly distinct from body copy and ordinary headings. Multiple evidence types inside one reveal retain separate labels.
