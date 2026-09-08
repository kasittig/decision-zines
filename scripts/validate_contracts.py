#!/usr/bin/env python3
"""Fast, dependency-free checks for Milestone 0 contract artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def main() -> int:
    json_files = sorted(ROOT.rglob("*.json"))
    for path in json_files:
        load_json(path)

    schema = load_json(ROOT / "schema" / "teaching-zine-ir.schema.json")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("Schema must declare JSON Schema 2020-12")

    ir = load_json(ROOT / "expected" / "minimal-valid.ir.json")
    if ir.get("schema_version") != "1.0":
        fail("Expected IR must use schema version 1.0")
    if (ir["document"].get("template"), ir["document"].get("template_version")) != ("standard", "1.0"):
        fail("Expected IR must record standard template version 1.0")

    components = ir["document"]["components"]
    ids = [component["id"] for component in components]
    if len(ids) != len(set(ids)):
        fail("Component IDs must be unique")
    for component_id in ids:
        if not ID_PATTERN.fullmatch(component_id):
            fail(f"Invalid component ID: {component_id}")

    types = {component["type"] for component in components}
    required = {
        "how_to_read", "provenance_vocabulary", "intent", "identity",
        "roles", "timeline", "part", "decision", "boundary", "reveal",
        "reflection", "lessons", "play_again", "privacy_sources_contributions", "sources",
    }
    missing = sorted(required - types)
    if missing:
        fail(f"Expected IR is missing component types: {missing}")

    by_id = {component["id"]: component for component in components}
    for component in components:
        decision_id = component.get("decision_id")
        if decision_id and by_id.get(decision_id, {}).get("type") != "decision":
            fail(f"{component['id']} references invalid decision {decision_id}")

    page_map = load_json(ROOT / "expected" / "minimal-valid.page-map.json")
    for decision_id, placement in page_map["decisions"].items():
        if decision_id not in by_id:
            fail(f"Page map references unknown decision {decision_id}")
        if placement["decision_page"] != placement["boundary_page"]:
            fail(f"Boundary moved off decision page for {decision_id}")
        if placement["reveal_page"] != placement["decision_page"] + 1:
            fail(f"Reveal is not on the next page for {decision_id}")

    markdown = (ROOT / "fixtures" / "minimal-valid" / "document.zine.md").read_text(encoding="utf-8")
    if not markdown.startswith("---\nformat: decision-teaching-zine\n"):
        fail("Normalized Markdown fixture lacks canonical front matter")
    for directive in ("decision", "boundary", "evidence"):
        if f"::: {directive} " not in markdown:
            fail(f"Normalized Markdown fixture lacks {directive} directive")
    if ":::: reveal " not in markdown:
        fail("Normalized Markdown fixture lacks nested reveal directive")
    if 'decision="decision-choose-the-next-operational-step"' not in markdown:
        fail("Normalized Markdown fixture lacks explicit decision relationships")
    for injected in ("::: how-to-read", "::: provenance-vocabulary", "::: privacy-sources-contributions"):
        if injected in markdown:
            fail(f"Normalized Markdown duplicates template component: {injected}")
    if "::: specific-sources " not in markdown:
        fail("Normalized Markdown fixture lacks zine-specific sources")
    template = (ROOT / "templates" / "standard-v1.yaml").read_text(encoding="utf-8")
    for required_text in ("template_id: standard", 'template_version: "1.0"', "HOW TO READ THIS", "PROVENANCE VOCABULARY", "PRIVACY, SOURCES & CONTRIBUTIONS", "SOURCES"):
        if required_text not in template:
            fail(f"Standard template lacks required content: {required_text}")

    print(f"Validated {len(json_files)} JSON files, normalized Markdown, and core Milestone 0 invariants.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
