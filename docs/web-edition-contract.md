# Static Web Edition Contract

Status: v1 web-renderer baseline. This contract supplements the semantic and
component contracts; it does not change source authority or narrative order.

## Build boundary

The static web edition is a second rendering target of the same validated,
template-expanded semantic document used by print. A web build requires no
credentials, network access, server, or database. It emits portable HTML, CSS,
JavaScript, and bundled font assets.

The renderer must not rewrite authored prose, change provenance, manufacture
component relationships, or publish editorial content. Web-only interface copy
is renderer chrome and must remain separate from authored publication copy.

## Reader screens

A reader screen is the web equivalent of a reader page: exactly one visible
semantic reading state inside the stage. Responsive reflow within that state
does not create additional semantic screens.

- A decision and its reveal/follow-up occupy different screens.
- The transformed boundary is the final substantive element on a decision
  screen.
- Its reveal/follow-up is the next semantic screen.
- A reveal screen is unavailable through ordinary navigation until the reader
  selects a response and explicitly commits it.
- Submitting a response advances directly to its reveal; no second navigation
  action is required.
- A teaching question or teaching lesson immediately following a reveal is
  rendered in that reveal screen, in source order. A lesson associated with a
  separate sidebar or supporting component remains a separate screen.
- Backward navigation never changes a committed response by itself or exposes
  a future reveal. On returning to a decision, the prior response remains
  selected, all responses remain available, and explicitly submitting a new
  response replaces the stored choice before returning to the reveal.
- A reader may deliberately restart the edition to clear all progress.
- Static assets cannot make source inspection a security boundary. Reveal
  gating is a reader-experience invariant, not access control.

## Choice state

Choice state is stored only in the reader's browser. It records the selected
option label and text for each decision plus the furthest unlocked screen.
Storage failure must not prevent play during the current session. No choice
data is transmitted by the generated site.

Each unlocked reveal displays the exact option label and text the reader
submitted for its related decision. This recap is reader state, remains
visually subordinate to the record, and does not imply that the response was
correct or recommended.

## Responsive and accessibility behavior

- The edition must remain usable at 320 CSS pixels without horizontal page
  scrolling.
- Controls meet a 44 CSS-pixel minimum touch target.
- Reading order and interaction order match semantic source order.
- All functions are keyboard operable, focus is visible, and status changes
  are announced without moving focus unexpectedly.
- The active screen is the only screen exposed for ordinary reading and focus.
- Reduced-motion preferences disable nonessential page transitions.
- Print-only minimum typography does not bind reflowed screens; web body text
  must be at least 16 CSS pixels at the narrowest supported viewport.

## Build manifest

Each edition embeds a machine-readable manifest containing the document title,
screen order and kinds, decision/reveal relationships, and renderer version.
Automated validation requires every reveal to immediately follow its decision
and use a distinct screen identifier.
