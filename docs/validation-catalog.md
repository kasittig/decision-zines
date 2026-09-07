# Validation Catalog

Errors stop publication. Warnings permit a draft build and require review. Advisories are non-blocking layout observations.

| Code | Severity | Condition |
|---|---|---|
| E001_SCHEMA_INVALID | Error | IR fails its versioned JSON Schema |
| E101_REQUIRED_FOUNDATION_MISSING | Error | Required foundation component absent |
| E102_REQUIRED_CLOSING_MISSING | Error | Required closing component absent |
| E201_DECISION_PROMPT_MISSING | Error | Decision has no prompt |
| E202_DECISION_RESPONSE_MISSING | Error | Decision has neither options nor free-response mechanism |
| E203_BOUNDARY_MISSING | Error | Decision has no boundary |
| E204_REVEAL_MISSING | Error | Historical decision has no reveal |
| E205_REVEAL_BEFORE_BOUNDARY | Error | Reveal occurs before its boundary |
| E206_MULTIPLE_PRIMARY_REVEALS | Error | Historical decision has more than one reveal container |
| E207_TEACHING_FOLLOWUP_MISSING | Error | Teaching-only decision lacks teaching follow-up |
| E208_INTERVENING_CONTENT | Error | Substantive content occurs between decision/boundary or boundary/reveal |
| E301_UNKNOWN_PROVENANCE | Error | Provenance is outside the standardized vocabulary |
| E302_RELATIONSHIP_INVALID | Error | Referenced decision/plan ID is absent or wrong type |
| E401_OVERSIZED_ATOMIC_COMPONENT | Error | Atomic component cannot fit at minimum typography |
| E501_PAGE_TURN_VIOLATION | Error | Decision/boundary/reveal page-map invariant fails |
| E502_CONTENT_OVERFLOW | Error | Content leaves page bounds, overlaps, or clips |
| W101_STYLE_TEXT_MISMATCH | Warning | Google style and recognized text disagree |
| W102_UNKNOWN_HEADING | Warning | Heading-like source text has no registered component |
| W201_PLAN_ENDS_WITHOUT_PLAN | Warning | Plan-end marker has no earlier relevant plan |
| W301_DEVELOPMENT_NOTES_PREMATURE | Warning | Required content appears only after terminal development notes |
| W401_BAD_COMPONENT_SPLIT | Warning | Split is legal but violates preferred fragmentation |
| A401_ORPHAN_RISK | Advisory | Heading lacks the required following visual content |
| A402_DENSE_PAGE | Advisory | Occupied-area threshold exceeds configured review level |
| A403_SPARSE_PAGE | Advisory | Non-purposeful page falls below configured occupied-area threshold |

Each diagnostic contains `code`, `severity`, `message`, `component_id` when known, and the richest available source location. Threshold values for density and raster tolerance belong to a versioned build configuration and must be recorded in build metadata.

