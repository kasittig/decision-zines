# IR v1 Contract

The IR is an ordered semantic document. Its JSON representation must validate against `schema/teaching-zine-ir.schema.json`.

## Required document fields

- `schema_version`: exactly `1.0` for this contract.
- `document`: stable document ID, title, subtitle, and ordered components.
- `source`: adapter name plus normalized Markdown path and optional upstream document ID.

The Markdown-to-IR parser is the only production entry point to IR. Google Docs import ends when it emits canonical `.zine.md` and its optional source-map sidecar.

## Component invariants

Every component has a unique `id`, a recognized `type`, a `publication_class`, and a source location. Published prose is represented as blocks rather than raw HTML. Renderers must escape text and must not infer semantics from prose.

Relationships are explicit:

```yaml
- id: decision-investigate
  type: decision
  mode: historical
- id: boundary-investigate
  type: boundary
  decision_id: decision-investigate
- id: reveal-investigate
  type: reveal
  decision_id: decision-investigate
```

The parser may construct IDs, but the renderer may not. Component order remains authoritative for narrative order; relationship fields remain authoritative for association.

## Reveal contents

A reveal is one container with one or more evidence blocks. Each evidence block independently declares one standardized provenance value. Mixed provenance therefore does not require multiple reveal containers.

`UNKNOWN` may be represented as a reveal whose only evidence block has `provenance: unknown`. A teaching-only decision omits a reveal and instead references a teaching follow-up.

## Evolution

Additive optional fields may appear in a 1.x schema. Breaking changes require a new major schema version and migration. Unknown component types fail v1 validation rather than falling back to generic prose.
