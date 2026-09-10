# AI Assistance Log

Material AI-assisted work is recorded here in addition to pull-request
disclosure. Human review remains required under `ai-assisted-development.md`.

## 2026-09-10 — Published PDF downloads

Codex assisted with adding reader and print-booklet PDF downloads to the
collection, copying the checked-in PDFs into the Pages artifact during the web
build, and extending renderer coverage. Verification included contract checks,
renderer tests, a web-only build, responsive browser review, and live download
response checks. No PDF content or authored prose changed.

## 2026-09-10 — GitHub Pages collection MVP

Codex assisted with the collection homepage, story-to-collection navigation,
completion actions, compact mobile progress control, GitHub Pages workflow,
renderer tests, and publication documentation. The collection design extends
the existing grayscale field-guide system and uses relative links so it works
at the repository subpath. Verification included contract validation, renderer
tests, a web-only fixture build, narrow and desktop browser review, keyboard
interaction, and a missing-asset and console-error check. Authored teaching and
historical prose were not changed.

## 2026-09-09 — Static playable web edition

Codex assisted with the web-edition contract, Python renderer, responsive
HTML/CSS/JavaScript interface, build wiring, and automated tests. Verification
included contract validation, five web-renderer tests, a complete Artwork Fire fixture
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

## 2026-09-09 — Project stewardship setup

Codex assisted with adapting the issue forms, pull-request record checks,
human-operated GitHub issue helper, and stable project-plan convention from the
`knowledge-db` repository. The setup was tailored to this repository's contract
and visual-review workflow; project-specific synchronization credentials and
identifiers were not copied. No authored teaching or historical prose changed.

## 2026-09-09 — Contributor onboarding and project navigation

Codex assisted with restructuring the README around first-time use, local
builds, validation, architecture, and repository navigation. It also added a
role-based documentation index and aligned the development dependency list
with the PDF builder's ReportLab import. Setuptools package discovery was
disabled because this script-based proof of concept has no installable Python
package. Publication contracts, authored zine content, provenance, and
rendered artifacts were not changed.

## 2026-09-09 — Teaching fixture de-identification

At the project editor's direction, Codex assisted with removing a distinctive
animal/artwork reference from the teaching fixture and replacing its repository
name and build slug with the neutral `artwork-fire` identifier. The edit
preserved the fixture's provenance categories, evidence distinctions, decision
options, uncertainty, and historical outcomes. Verification included contract
validation, renderer tests, a complete fixture rebuild, and visual review of
the regenerated reader and booklet PDFs.
