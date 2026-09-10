# Decision-Based Teaching Zines — Project Plan

## Project status

The project is an early, contract-first proof of concept with a working print
and static web renderer for the Artwork Fire fixture. The current product focus is
an MVP public web collection: make the existing playable edition easy to find,
publish, and navigate without expanding the canonical publishing pipeline.

The roadmap remains authoritative for milestone sequencing, and the contracts
in `docs/` remain authoritative for publication behavior. GitHub issues record
the scope and validation of individual changes.

## Current outcome

Publish a small collection of decision-based teaching stories at a memorable
GitHub Pages URL. A reader should be able to choose a story, complete it without
encountering an unrevealed outcome early, and return to the collection.

## MVP scope

- Rename the GitHub repository to `decision-zines` for the shorter default URL
  `https://kasittig.github.io/decision-zines/`.
- Publish `output/site/` through GitHub Pages and GitHub Actions.
- Add a collection homepage listing available stories.
- Add a persistent route from each story back to the collection.
- Preserve the existing Back/Next and decision/commit/reveal interaction.
- Add completion actions to replay a story or return to the collection.
- Keep collection and story navigation usable on narrow screens and by keyboard.

## Explicit non-goals for this MVP

- Accounts, analytics, a server, or a database.
- Collection-level saved progress, “Continue” cards, or cross-story state.
- Search, filtering, tags, achievements, or recommendations.
- A custom domain.
- Production parsing, Google Docs import, or changes to authored claims.

The existing story renderer may continue to use browser-local choice state as
required by the web-edition contract. The collection must not depend on or
summarize that state.

## Definition of done

1. The collection homepage and every included story load from the repository
   subpath on GitHub Pages with no missing local assets.
2. A reader can enter a story, navigate it, return to the collection, replay it,
   and complete decision/reveal cycles without bypassing reveal gates.
3. The collection and story navigation work at 320 CSS pixels and with a
   keyboard, visible focus, and appropriate landmarks and labels.
4. A push to `main` validates contracts and tests before publishing the static
   artifact.
5. Deployment and local preview instructions are documented.
