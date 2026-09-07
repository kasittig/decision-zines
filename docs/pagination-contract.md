# Pagination Contract

## Hard invariants

1. A decision and its reveal/follow-up never share a reader page.
2. The boundary is the final substantive component on the decision page.
3. The reveal/follow-up is the first substantive component on the next reader page.
4. Nothing is omitted, overlapped, clipped, or placed outside the content box.
5. Typography never falls below the frozen minimum tokens.

Headers, footers, folios, and continuation labels are not substantive components.

## Priority order

After hard invariants:

1. Keep a heading with one complete atomic child or at least two rendered lines of non-empty body text.
2. Keep atomic components together.
3. Keep `prefer atomic` components together when they fit on an otherwise empty page.
4. Split oversized splittable components using their component contract.
5. Prefer visually balanced pages.
6. Add pages freely.

## Page-map contract

Post-render inspection produces a page map recording the page containing every component fragment. Each decision entry records decision, boundary, and reveal/follow-up pages. Validation requires `decision_page == boundary_page` and `reveal_page == decision_page + 1` for v1.

## Blank pages

Reader blanks introduced for narrative layout are real pages. Booklet padding blanks are appended after the final reader page until the count is divisible by four. They contain no substantive content and are tagged as `imposition_padding` in build metadata.

## Determinism

With identical normalized source, styles, assets, renderer version, and build configuration, builds must have identical page counts, component page maps, and per-page extracted text. Raster comparisons may differ only within the configured antialiasing tolerance. Byte-identical PDFs are not required because metadata and object ordering may vary.

