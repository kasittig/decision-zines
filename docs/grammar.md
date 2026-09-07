# Document Grammar

The notation `?`, `*`, and `+` means optional, zero-or-more, and one-or-more.

```text
document = foundation part+ closing

foundation = title subtitle how_to_read provenance_vocabulary
             content_note? intent identity roles timeline

part = part_header part_component*

part_component = context | plan | plan_ends | supporting
               | historical_cycle | teaching_cycle

historical_cycle = decision boundary reveal post_reveal_component*
teaching_cycle = teaching_decision boundary teaching_followup post_reveal_component*

post_reveal_component = teaching_lesson | teaching_question | supporting

closing = reflection lessons privacy_sources_contributions sources
```

## Decision-cycle rules

- A part may contain multiple decision cycles.
- A historical decision has exactly one boundary and exactly one reveal.
- A reveal may contain multiple evidence blocks.
- An unknown outcome is still a reveal.
- A teaching-only decision has exactly one boundary, no historical reveal, and a clearly identified teaching follow-up.
- No substantive component may occur between a decision and its boundary or between a boundary and its reveal/follow-up.
- A lesson cannot precede the reveal or teaching follow-up for its cycle.
- A part ends at the next part header or the first closing component.
- Closing components occur once and in the declared order.

## Plan relationship

`plan_ends` should reference the relevant earlier plan when the association is not unambiguous within its part. Absence of an earlier relevant plan is a warning, not a fabrication opportunity.

## Non-content markers

A boundary is a transform-class node. Pinned IDs are metadata. Development notes are editorial. None may be printed verbatim by a conforming renderer.

