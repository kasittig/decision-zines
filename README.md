# Decision-Based Teaching Zine Generator

[![Validate contracts](https://github.com/kasittig/decision-zines/actions/workflows/validate.yml/badge.svg)](https://github.com/kasittig/decision-zines/actions/workflows/validate.yml)

Turn a structured teaching scenario into two reader experiences:

- a responsive, playable website that reveals the historical record only after a reader commits to a choice;
- printable half-letter reader and booklet PDFs designed for grayscale printing.

The project is currently an early, contract-first proof of concept. It includes a working renderer for the Artwork Fire fixture, but not yet the planned production parser or Google Docs importer. See the [roadmap](docs/roadmap.md) for that progression.

The current product scope and definition of done are recorded in
[`PROJECT_PLAN.md`](PROJECT_PLAN.md). GitHub issues track focused implementation
work and validation.

## Try the example

Visit the published collection at
[kasittig.github.io/decision-zines/](https://kasittig.github.io/decision-zines/),
or explore the checked-in output without installing anything:

- Open [`output/site/index.html`](output/site/index.html) for the collection homepage.
- Open [`output/site/artwork-fire/index.html`](output/site/artwork-fire/index.html) in a browser for the playable edition.
- Open [`output/pdf/artwork-fire-reader.pdf`](output/pdf/artwork-fire-reader.pdf) for the reader PDF.
- Print [`output/pdf/artwork-fire-booklet.pdf`](output/pdf/artwork-fire-booklet.pdf) at 100% scale, landscape, duplex, flipping on the short edge.

The web edition runs entirely in the browser. Choices stay in local browser storage and are not transmitted.

To preview the collection through a local web server after building it:

```bash
python -m http.server 8000 --directory output/site
```

Then open `http://localhost:8000/`. Serving the directory, rather than opening
the HTML file directly, matches GitHub Pages routing more closely.

## Build it locally

Requirements:

- Python 3.11 or newer;
- Google Chrome for PDF rendering;
- Ghostscript (recommended) for explicit grayscale PDF output.

Create an environment and install the development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Build the included Artwork Fire example:

```bash
python scripts/build_zine.py fixtures/artwork-fire/source.md --slug artwork-fire
```

This writes the collection homepage and story website alongside the print output:

```text
output/
├── html/artwork-fire-reader.html   # print-oriented intermediate HTML
├── pdf/artwork-fire-reader.pdf     # half-letter reader PDF
├── pdf/artwork-fire-booklet.pdf    # imposed Letter-size booklet PDF
└── site/
    ├── index.html                  # collection homepage
    └── artwork-fire/               # portable playable website
```

To build only the website—without Chrome or the PDF dependencies—run:

```bash
python scripts/build_zine.py fixtures/artwork-fire/source.md \
  --slug artwork-fire \
  --web-only
```

On macOS, the PDF command uses Chrome’s standard application path. Elsewhere, pass the executable explicitly:

```bash
python scripts/build_zine.py fixtures/artwork-fire/source.md \
  --slug artwork-fire \
  --chrome /path/to/chrome
```

## Publish the website

The `Publish GitHub Pages` workflow validates the contracts, runs the renderer
tests, rebuilds every included web edition, and deploys `output/site/` after a
push to `main`. GitHub Pages must use **GitHub Actions** as its source in the
repository settings. The workflow can also be run manually from the Actions
tab.

## Validate changes

Run the contract checks and renderer tests before submitting a change:

```bash
python scripts/validate_contracts.py
python -m unittest discover -s tests -v
```

Changes that affect PDF layout also require a fresh build and visual inspection of every changed page. The full workflow is in [CONTRIBUTING.md](CONTRIBUTING.md).

## How the project fits together

```text
Authored source
    │
    ├── Google Doc ── planned adapter ──┐
    │                                  │
    └── direct authoring ───────────────┤
                                       ▼
                              canonical .zine.md
                                       │
                              template expansion
                                       │
                                       ▼
                              validated semantic IR
                                  ┌────┴────┐
                                  ▼         ▼
                              print/PDF    static web
```

Current proof-of-concept note: `scripts/build_zine.py` accepts the heading-based fixture format used by `fixtures/artwork-fire/source.md`. The canonical `.zine.md` parser and Google Docs adapter are later milestones.

## Repository guide

| Path | What belongs there |
|---|---|
| `docs/` | Normative contracts, author guidance, roadmap, and AI policy |
| `fixtures/` | Valid and malformed source examples used for regression work |
| `expected/` | Expected semantic IR, diagnostics, and page maps |
| `schema/` | Executable JSON Schema for the semantic IR |
| `templates/` | Versioned shared publication copy and defaults |
| `renderer/` | Print and web styles plus browser interaction code |
| `scripts/` | Validation and proof-of-concept build commands |
| `tests/` | Automated renderer tests |
| `prototype/` | Visual prototype material; direction only, not policy |
| `output/` | Checked-in example builds for review |
| `assets/` | Bundled fonts and licenses used for reproducible output |

Start with the [documentation index](docs/README.md) if you are authoring content, implementing the pipeline, or reviewing publication behavior.

## Core publication guarantees

- Authored teaching and historical claims remain verbatim.
- Provenance is never changed to simplify implementation or layout.
- A reveal never appears on the same reader page or screen as its decision.
- `DECISION BOUNDARY` is transformed into reader-facing commit behavior and is never printed literally.
- `DEVELOPMENT NOTES` and everything after it remain unpublished.
- Shared copy lives in versioned templates rather than being duplicated in each zine.
- Canonical Markdown builds require neither Google credentials nor network access.
- Ambiguous Google Docs structure produces a diagnostic instead of a guess.

## Contract precedence

When project materials disagree, use this order:

1. JSON Schema for data shape.
2. Grammar and component contracts for semantic legality.
3. Pagination contract for page placement.
4. Validation catalog for diagnostic severity.
5. Prototype for visual direction only.

See [AGENTS.md](AGENTS.md) for the working agreement and [the AI-assisted development policy](docs/ai-assisted-development.md) for disclosure and review expectations.
