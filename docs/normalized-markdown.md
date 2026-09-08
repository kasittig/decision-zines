# Normalized Markdown Contract

Normalized Markdown is the canonical, durable input to the publication core. It is a first-class build artifact: human-readable, versioned, diffable, independently buildable, and suitable for regression fixtures. It contains zine-specific semantic content; shared publication boilerplate belongs to a versioned template.

```text
Google Doc -> adapter -> normalized Markdown --+-- template expansion -> IR -> HTML/CSS -> PDF
                            ^                  |
Direct Markdown authoring ---+       versioned template
```

The Google Doc remains the editorial source of truth when one exists. The normalized Markdown file records exactly what the adapter understood. Editing it does not silently update its source Google Doc.

## File requirements

- UTF-8 text with LF line endings.
- Extension `.zine.md`.
- YAML front matter containing `format`, `version`, `template`, `template_version`, `id`, and `title`.
- ATX headings (`#`) only; no setext headings.
- Semantic blocks use fenced directives beginning with at least three colons. A directive containing nested directives must use a longer outer fence than its children.
- Raw HTML is forbidden.
- Reserved semantics must be explicit; prose is never scanned to infer components.

```markdown
---
format: decision-teaching-zine
version: "1.0"
id: sudden-change
title: A Sudden Change
template: standard
template_version: "1.0"
source:
  adapter: google_docs
  document_id: example-id
---
```

The standard subtitle is supplied by the template. An input may override a template field only when the template explicitly marks it as overridable.

## Shared versus zine-specific content

Do not repeat these standard-template components in input Markdown:

- subtitle;
- `HOW TO READ THIS`;
- provenance vocabulary definitions;
- decision-boundary reader copy;
- the default `Choose another response.` option;
- `PLAY AGAIN` copy;
- shared privacy/source/contribution language;
- the standard Sources introduction.

Input Markdown supplies the content that varies: title, content-note details, intent/core question, identity, roles, timeline phases, scenario components, lessons, zine-specific source entries, and special privacy or contribution disclosures.

Zine-specific sources use a `specific-sources` directive. During expansion, its entries are appended to the template-provided `sources` component; `specific-sources` does not survive as a separate IR component.

Template expansion produces the complete IR. A duplicated fixed component in the input is an error rather than a second copy in the output.

## Component syntax

Published components use named directives:

```markdown
::: context {#changing-conditions}
Conditions have changed quickly.
:::

::: plan {#pause-plan}
The duty lead pauses activity when conditions become unsafe.
:::
```

Attributes are enclosed in braces on the opening line. `#name` sets the stable component ID. Quoted key/value attributes carry relationships or topics.

## Decision cycle

```markdown
::: decision {#operational-step mode="historical"}
## What do you do?

Choose the next operational step.

A. Pause all activity.
B. Continue while gathering information.
C. Choose another response.
:::

::: boundary {decision="operational-step"}
:::

:::: reveal {#operational-step-record decision="operational-step"}
::: evidence {provenance="documented"}
The team paused activity and reassessed conditions.
:::
::::
```

The boundary directive must have no body. It is transformed into the commit/page-turn treatment and never printed literally.

Teaching-only decisions use `mode="teaching_only"` and are followed by `teaching-followup` rather than `reveal`.

## Provenance

Provenance is permitted only on `evidence` directives, with one of:

- `documented`
- `recollected`
- `unknown`
- `teaching_scenario`

A mixed-provenance reveal contains multiple evidence directives. Its outer reveal fence therefore uses four colons while its evidence blocks use three. Provenance prefixes from Google Docs are converted to these attributes; the publication core does not parse prefixes.

## Source mapping

Adapter-generated files may attach source references to directives using opaque `source_ref` attributes. A sidecar named `<document>.zine.map.json` maps those references to Google Docs structural positions. The sidecar is metadata, not publication content, and travels with the normalized Markdown artifact.

Direct-authored Markdown uses its file path and line/column positions directly and does not require a sidecar.

## Canonical serialization

The adapter emits components in source order, uses lowercase directive names and attributes, quotes attribute values, inserts one blank line between blocks, and preserves published prose without reflow. Canonical output makes repeated imports stable and reviewable.

## Build behavior

`zine build example.zine.md` must work without Google credentials or network access. A Google import and a direct Markdown build converge at the same Markdown-to-IR parser. The build resolves the exact template ID/version from front matter, expands defaults, and then validates the complete IR. Generated Markdown should normally be committed alongside approved source snapshots used for publication or regression testing.
