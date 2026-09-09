# AI Assistance Log

Material AI-assisted work is recorded here in addition to pull-request
disclosure. Human review remains required under `ai-assisted-development.md`.

## 2026-09-09 — Static playable web edition

Codex assisted with the web-edition contract, Python renderer, responsive
HTML/CSS/JavaScript interface, build wiring, and automated tests. Verification
included contract validation, five web-renderer tests, a complete Goat fixture
build, desktop and 390-by-844-pixel browser review, interactive commit/reveal
testing, and browser console review. The existing print renderer and authored
teaching and historical prose were not rewritten.

The decision interaction was subsequently refined so `Submit response`
commits the selected option and advances directly to the related reveal.
Reveal screens were then extended with a neutral recap of the reader's exact
submitted option.
Committed decisions were subsequently made revisable: returning to a decision
preserves the prior selection while allowing the reader to submit a replacement.
Immediate post-reveal teaching questions and lessons were subsequently grouped
into the related reveal screen while sidebar-associated lessons stayed separate.
