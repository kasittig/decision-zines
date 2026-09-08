# Google Doc Formatting Guide

Use this guide to prepare an editorial Google Doc for import into the Decision-Based Teaching Zine Generator. The Google Doc encodes zine-specific meaning; it does not reproduce shared boilerplate or final visual design.

## Copy-paste prompt for ChatGPT

Attach or link the Google Doc with editing access, then send:

```text
Format the attached Google Doc as zine-specific semantic source for the
Decision-Based Teaching Zine Generator.

This is a structural-formatting task, not a rewriting task. Preserve all
substantive prose, teaching claims, historical claims, provenance assignments,
uncertainty, decision options, and narrative order. You may normalize a
heading to the exact registered vocabulary when its intended semantic role is
unambiguous. Do not rewrite its body text.

SHARED TEMPLATE COPY

Do not add or duplicate any of the following. The publication template injects
them automatically:

- “A Decision-Based Teaching Reconstruction” subtitle
- HOW TO READ THIS
- provenance vocabulary definitions
- default “Choose another response.” option
- reader-facing commit/page-turn instructions
- PLAY AGAIN copy
- shared PRIVACY, SOURCES & CONTRIBUTIONS language
- SOURCES heading and standard Sources introduction
- page numbers, running headers, and timeline footer

If the draft already contains shared boilerplate, do not delete it silently.
Identify it in the audit report as content to remove or reconcile with the
standard template.

GOOGLE DOCS STYLES

1. Apply Google Docs “Title” to the document title.

2. Apply “Heading 1” to these zine-specific major sections:

   CONTENT NOTE
   INTENT
   WHO ARE YOU?
   ROLES IN THIS STORY
   TIMELINE
   PART [#] — YOU ARE [ROLE]
   LOOK BACK AT YOUR DECISIONS
   LESSONS — [THEME]
   SOURCE ENTRIES
   DEVELOPMENT NOTES

3. Apply “Heading 2” to scenario components:

   CONTEXT
   CONTEXT — [TOPIC]
   THE PLAN
   THE PLAN — [TOPIC]
   DECISION [#] — [TOPIC]
   WHAT DO YOU DO?
   TEACHING DECISION — [TOPIC]
   DECISION BOUNDARY
   WHAT THE RECORD SHOWS
   WHAT THE RECORD SHOWS — [OUTCOME]
   THE PLAN ENDS HERE
   UNKNOWN
   TEACHING LESSON
   TEACHING LESSON — [TOPIC]
   TEACHING QUESTION
   SIDEBAR — [TOPIC]
   TEACHING EXAMPLE — [TOPIC]
   CAPACITY LIMIT
   DURING THE EVENT
   AFTER THE EVENT
   EPILOGUE — [PHASE]
   LONGER-TERM FOLLOW-UP — [TOPIC]

4. Apply “Normal text” to body paragraphs. Preserve paragraph boundaries. Do
   not treat short, bold, or uppercase prose as a heading unless its semantic
   role is clear.

DECISIONS

- Keep each option as its own paragraph immediately following WHAT DO YOU DO?
- Use bare `TEACHING LESSON` when the label alone is sufficient. Use `TEACHING LESSON — [TOPIC]` only when the panel needs a meaningful topic heading; the formatter will not invent an additional heading for the bare form.
- Preserve explicit A., B., C., etc. prefixes.
- Do not emphasize or recommend an option.
- Do not add “Choose another response.”; the template supplies it when absent.
- Preserve it if the draft already includes it.
- Every historical decision must end with a standalone DECISION BOUNDARY after
  its final option and before its reveal.
- Apply Heading 2 to DECISION BOUNDARY.
- Do not replace that marker with reader-facing instructions.

PROVENANCE

Evidence paragraphs must begin with exactly one of:

DOCUMENTED:
RECOLLECTED:
UNKNOWN:
TEACHING SCENARIO:

Bold the prefix including its colon. Keep the evidence in the same paragraph.
Normalize an em dash after a recognized provenance label to a colon. Never
change the provenance category itself. Flag any unrecognized provenance-like
label.

ZINE-SPECIFIC SOURCES

Do not add a SOURCES heading. The template owns it.

If the draft provides actual source citations, document titles, links, archival
references, or a source inventory, place them under the optional Heading 1:

SOURCE ENTRIES

Preserve those entries exactly. Do not invent missing titles, dates, links,
authors, or citations. If no specific entries are supplied, omit SOURCE ENTRIES;
the build will use the standard Sources text and emit a review warning.

DEVELOPMENT NOTES

DEVELOPMENT NOTES is terminal editorial material. Apply Heading 1. Do not move
it or publish it. Everything after it remains editorial-only.

STRUCTURAL CHECK

Zine-specific foundation content should normally include:

- optional CONTENT NOTE
- INTENT
- WHO ARE YOU?
- ROLES IN THIS STORY
- TIMELINE
- one or more scenario parts or decision cycles

Write TIMELINE as an ordered sequence of Markdown bullets whose bold opening
labels orient the reader without revealing outcomes. The formatter uses those
labels for the running footer and maps them to numbered decision cycles in
source order.

Historical decision cycles must follow:

context and supporting material
→ optional plan
→ WHAT DO YOU DO?
→ options
→ DECISION BOUNDARY
→ WHAT THE RECORD SHOWS or UNKNOWN
→ optional teaching lesson/question/supporting material

Nothing substantive may occur between DECISION BOUNDARY and its reveal. A
teaching lesson cannot precede its reveal.

The zine-specific closing content should include:

- LOOK BACK AT YOUR DECISIONS
- LESSONS — [THEME]
- optional SOURCE ENTRIES

VISUAL RESTRAINT

Do not make the Google Doc resemble the final zine. Do not add layout tables,
columns, text boxes, decorative borders, custom fonts, colors, icons, manual
page breaks, headers, footers, or page numbers. The renderer owns presentation.

FINAL AUDIT

After formatting, report:

1. Structural errors that prevent publication.
2. Missing zine-specific foundation or closing material.
3. Missing decision boundaries or reveals.
4. Unknown headings or provenance labels.
5. Existing text that appears to duplicate template boilerplate.
6. Whether SOURCE ENTRIES were supplied.
7. Every heading normalization you performed.
8. Whether any substantive body text changed; the expected answer is no.

Do not resolve genuine semantic ambiguity without asking me.
```

## Follow-up audit prompt

```text
Audit the formatted document against the zine formatting specification again.
Do not make further changes. List each problem with its nearest heading and
quote only the minimum text needed to locate it.
```

## What the importer does next

The Google Docs adapter emits sparse normalized Markdown. The build resolves the declared template version, injects shared components, merges `SOURCE ENTRIES` into the template-owned Sources component, validates the expanded IR, and only then renders the zine.
