#!/usr/bin/env python3
"""Build a reader HTML/PDF and booklet PDF from semantic teaching Markdown.

This v1 formatter intentionally accepts the heading-based semantic Markdown
produced by the Google Doc formatting guide. It expands standard-v1 template
copy and enforces decision-boundary/reveal ordering.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
DECISION_HEADING = re.compile(r"^DECISION\s+(\d+)\s+[—-]\s+(.+)$", re.I)
PROVENANCE = re.compile(r"^\*\*(DOCUMENTED|RECOLLECTED|UNKNOWN|TEACHING SCENARIO):\*\*\s*(.*)$", re.I)
OPTION = re.compile(r"^([A-Z])\.\s+(.+)$")


@dataclass
class Section:
    heading: str
    lines: list[str]


def parse(path: Path) -> tuple[str, list[Section]]:
    title = ""
    sections: list[Section] = []
    current: Section | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = HEADING.match(raw)
        if match:
            level, heading = len(match.group(1)), match.group(2).strip()
            if level == 1 and not title:
                title = heading
                continue
            if level == 2:
                current = Section(heading=heading, lines=[])
                sections.append(current)
                continue
        if current is not None:
            current.lines.append(raw)
    if not title:
        raise ValueError("A level-1 document title is required")
    return title, sections


def inline(text: str) -> str:
    value = html.escape(text, quote=False)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*(.+?)\*(?!\*)", r"<em>\1</em>", value)
    return value


def semantic_card(kind: str, title: str, body: str) -> str:
    """Render the shared provenance/evidence component."""
    modifier = kind.lower().replace(" ", "-")
    return (
        f'<section class="semantic-card semantic-card--{modifier}">'
        f'<h3 class="semantic-card__title">{inline(title)}</h3>'
        f'<div class="semantic-card__body"><p>{inline(body)}</p></div>'
        '</section>'
    )


def paragraphs(lines: list[str]) -> list[str]:
    out: list[str] = []
    buffer: list[str] = []
    def flush() -> None:
        if buffer:
            out.append(" ".join(x.strip() for x in buffer))
            buffer.clear()
    for line in lines:
        if not line.strip():
            flush()
        elif line.lstrip().startswith("- "):
            # A Markdown list does not require blank lines between items. Flush
            # surrounding prose and preserve each bullet as its own block.
            flush()
            out.append(line.strip())
        else:
            buffer.append(line)
    flush()
    return out


def body_html(lines: list[str], evidence=True) -> str:
    chunks: list[str] = []
    list_items: list[str] = []
    def flush_list() -> None:
        if list_items:
            chunks.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in list_items) + "</ul>")
            list_items.clear()
    for para in paragraphs(lines):
        if para.startswith("- "):
            list_items.append(para[2:])
            continue
        flush_list()
        pm = PROVENANCE.match(para)
        if evidence and pm:
            label, text = pm.group(1).upper(), pm.group(2)
            chunks.append(semantic_card(label, label, text))
        else:
            chunks.append(f"<p>{inline(para)}</p>")
    flush_list()
    return "".join(chunks)


def timeline_html(lines: list[str]) -> str:
    items: list[str] = []
    for para in paragraphs(lines):
        if not para.startswith("- "):
            continue
        content = para[2:].strip()
        match = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", content)
        if match:
            label, description = match.groups()
            items.append(
                f'<li><div class="timeline-copy"><h3>{inline(label)}</h3>'
                f'<p>{inline(description)}</p></div></li>'
            )
        else:
            items.append(f'<li><div class="timeline-copy"><p>{inline(content)}</p></div></li>')
    if not items:
        return body_html(lines)
    return '<ol class="story-timeline">' + "".join(items) + "</ol>"


def timeline_phase_labels(lines: list[str]) -> list[str]:
    """Return the author-supplied timeline labels in source order."""
    labels: list[str] = []
    for para in paragraphs(lines):
        if not para.startswith("- "):
            continue
        content = para[2:].strip()
        match = re.match(r"^\*\*(.+?):\*\*", content)
        labels.append(match.group(1).strip() if match else content)
    return labels


def add_running_timeline(reader_path: Path, labels: list[str], decision_topics: dict[int, str]) -> None:
    """Stamp phase navigation and folios into the reserved bottom margin."""
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    if not labels:
        return

    font_name = "ZineDejaVuSans"
    bold_name = "ZineDejaVuSansBold"
    pdfmetrics.registerFont(TTFont(font_name, str(ROOT / "assets" / "fonts" / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont(bold_name, str(ROOT / "assets" / "fonts" / "DejaVuSans-Bold.ttf")))

    reader = PdfReader(str(reader_path))
    writer = PdfWriter()
    active_phase: int | None = None
    foundation_timeline_seen = False
    decision_pattern = re.compile(r"\bDECISION\s+([1-9]\d*)\b", re.I)
    closing_pattern = re.compile(r"\bLOOK BACK AT YOUR DECISIONS\b", re.I)
    timeline_heading_pattern = re.compile(r"(^|\n)TIMELINE\s*($|\n)", re.I)

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        normalized_page_text = re.sub(r"\s+", " ", page_text).upper()
        is_foundation_timeline = bool(timeline_heading_pattern.search(page_text))
        if closing_pattern.search(page_text):
            active_phase = None
        if foundation_timeline_seen and not is_foundation_timeline:
            for phase, topic in decision_topics.items():
                normalized_topic = re.sub(r"\s+", " ", topic).upper()
                if normalized_topic in normalized_page_text:
                    active_phase = phase if phase <= len(labels) else None
                    break
            decision_match = decision_pattern.search(page_text)
            if decision_match:
                candidate = int(decision_match.group(1))
                active_phase = candidate if candidate <= len(labels) else None

        if active_phase is not None:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            overlay_bytes = BytesIO()
            overlay = canvas.Canvas(overlay_bytes, pagesize=(width, height))

            left = 30.24
            right = width - 30.24
            rail_y = 46
            node_radius = 5
            step = (right - left) / (len(labels) - 1) if len(labels) > 1 else 0

            overlay.setStrokeColorRGB(0, 0, 0)
            overlay.setFillColorRGB(1, 1, 1)
            overlay.setLineWidth(0.75)
            overlay.line(left, rail_y, right, rail_y)

            for index in range(1, len(labels) + 1):
                x = left + (index - 1) * step
                selected = index == active_phase
                overlay.setFillColorRGB(0, 0, 0) if selected else overlay.setFillColorRGB(1, 1, 1)
                overlay.setStrokeColorRGB(0, 0, 0)
                overlay.setLineWidth(1)
                overlay.circle(x, rail_y, node_radius, stroke=1, fill=1)
                overlay.setFillColorRGB(1, 1, 1) if selected else overlay.setFillColorRGB(0, 0, 0)
                overlay.setFont(bold_name, 7.5)
                overlay.drawCentredString(x, rail_y - 2.7, str(index))

            active_label = f"{active_phase} / {len(labels)}  {labels[active_phase - 1]}"
            overlay.setFillColorRGB(0, 0, 0)
            overlay.setFont(bold_name, 8.5)
            overlay.drawCentredString(width / 2, 28.5, active_label)
            overlay.setFont(font_name, 8.5)
            overlay.drawCentredString(width / 2, 17.5, str(page_number))
            overlay.save()

            overlay_bytes.seek(0)
            page.merge_page(PdfReader(overlay_bytes).pages[0])
        writer.add_page(page)
        if is_foundation_timeline:
            foundation_timeline_seen = True

    stamped_path = reader_path.with_name(reader_path.stem + "-running.pdf")
    with stamped_path.open("wb") as stream:
        writer.write(stream)
    stamped_path.replace(reader_path)


def options_html(lines: list[str]) -> tuple[str, list[str]]:
    intro: list[str] = []
    options: list[tuple[str, str]] = []
    for para in paragraphs(lines):
        match = OPTION.match(para)
        if match:
            options.append((match.group(1), match.group(2)))
        else:
            intro.append(para)
    if not options:
        raise ValueError("WHAT DO YOU DO? requires A./B./C. option paragraphs")
    rendered = "".join(f'<li value="{ord(label)-64}">{inline(text)}</li>' for label, text in options)
    return "".join(f"<p>{inline(x)}</p>" for x in intro) + f'<ol type="A">{rendered}</ol>', [x[1] for x in options]


def template_text() -> dict[str, str]:
    text = (ROOT / "templates" / "standard-v1.yaml").read_text(encoding="utf-8")
    values = re.findall(r"^\s+text:\s+(.+)$", text, flags=re.M)
    values = [v.strip().strip('"') for v in values]
    return {
        "how": values[0], "documented": values[1], "recollected": values[2],
        "unknown": values[3], "scenario": values[4], "play": values[5],
        "privacy": values[6], "sources": values[7],
    }


def validate(sections: list[Section]) -> list[str]:
    headings = [s.heading.upper() for s in sections]
    required = ["INTENT", "WHO ARE YOU?", "ROLES IN THIS STORY", "TIMELINE", "LOOK BACK AT YOUR DECISIONS"]
    errors = [f"Missing required zine-specific section: {x}" for x in required if x not in headings]
    decisions = sum(bool(DECISION_HEADING.match(h)) for h in headings)
    boundaries = headings.count("DECISION BOUNDARY")
    reveals = headings.count("WHAT THE RECORD SHOWS") + sum(h.startswith("WHAT THE RECORD SHOWS —") for h in headings)
    if not decisions:
        errors.append("At least one DECISION [#] heading is required")
    if boundaries != decisions:
        errors.append(f"Found {decisions} decisions but {boundaries} boundaries")
    if reveals != decisions:
        errors.append(f"Found {decisions} decisions but {reveals} reveals")
    for i, h in enumerate(headings):
        if h == "DECISION BOUNDARY" and (i + 1 >= len(headings) or not headings[i + 1].startswith("WHAT THE RECORD SHOWS")):
            errors.append("Every DECISION BOUNDARY must be immediately followed by WHAT THE RECORD SHOWS")
    return errors


def render(title: str, sections: list[Section]) -> str:
    by_heading = {s.heading.upper(): s for s in sections}
    tpl = template_text()
    parts: list[str] = ["<!doctype html><html><head><meta charset='utf-8'>", "<title>" + html.escape(title) + "</title>", "<link rel='stylesheet' href='../../renderer/zine.css'></head><body>"]
    parts.append(f'<section class="cover"><div class="kicker">A DECISION-BASED TEACHING RECONSTRUCTION</div><h1>{inline(title)}</h1><p class="subtitle">Governance, evidence, authority, and uncertainty</p><p class="deck">A private decision game about what the evidence establishes, what action it justifies, and when an organization should stop looking.</p></section>')
    parts.append('<main class="foundation"><h1 class="foundation-title">HOW TO USE THIS ZINE</h1>')
    parts.append(f'<section><h2>HOW TO READ THIS</h2><p>{inline(tpl["how"])}</p></section>')
    parts.append('<section><h2>PROVENANCE VOCABULARY</h2><div class="provenance-grid">')
    for label,key in (("DOCUMENTED","documented"),("RECOLLECTED","recollected"),("UNKNOWN","unknown"),("TEACHING SCENARIO","scenario")):
        parts.append(semantic_card(label, label, tpl[key].split(":",1)[-1].strip()))
    parts.append('</div></section>')
    for heading, cls in (("INTENT","intent"),("WHO ARE YOU?","identity"),("ROLES IN THIS STORY","roles"),("TIMELINE","timeline-intro")):
        sec=by_heading[heading]
        content = timeline_html(sec.lines) if heading == "TIMELINE" else body_html(sec.lines)
        parts.append(f'<section class="{cls}"><h2>{heading}</h2>{content}</section>')
    parts.append('</main>')

    i=0
    while i < len(sections):
        sec=sections[i]; upper=sec.heading.upper(); dm=DECISION_HEADING.match(sec.heading)
        if dm:
            number, topic=dm.groups()
            parts.append(f'<article class="decision-unit"><h1 class="decision-unit-title">DECISION {number}<br>{inline(topic)}</h1><div class="context-block">{body_html(sec.lines)}</div>')
            i += 1
            while i < len(sections) and sections[i].heading.upper() != "WHAT DO YOU DO?":
                extra=sections[i]; parts.append(f'<section><h2 class="section-label">{inline(extra.heading)}</h2>{body_html(extra.lines)}</section>'); i += 1
            if i >= len(sections): raise ValueError(f"Decision {number} lacks WHAT DO YOU DO?")
            decision=sections[i]; option_markup,_=options_html(decision.lines)
            parts.append(f'<div class="choice-cycle"><section class="decision"><h2><span>WHAT DO YOU DO?</span><small>DECISION {number}</small></h2>{option_markup}</section>'); i += 1
            if i >= len(sections) or sections[i].heading.upper() != "DECISION BOUNDARY": raise ValueError(f"Decision {number} lacks boundary")
            parts.append('<div class="boundary"><b>COMMIT BEFORE YOU CONTINUE.</b><span>Mark your choice, then turn the page.</span></div></div></article>'); i += 1
            reveal=sections[i]
            parts.append(f'<article class="reveal"><h2>{inline(reveal.heading)}</h2><h3>{inline(topic)}</h3>{body_html(reveal.lines)}</article>'); i += 1
            continue
        if upper.startswith("TEACHING LESSON"):
            topic_match = re.match(r"^TEACHING LESSON\s+[—-]\s+(.+)$", sec.heading, re.I)
            topic_heading = f'<h2>{inline(topic_match.group(1).strip())}</h2>' if topic_match else ""
            parts.append(f'<section class="lesson"><div class="lesson-label">TEACHING LESSON</div><div class="lesson-body">{topic_heading}{body_html(sec.lines)}</div></section>')
        elif upper.startswith("SIDEBAR"):
            parts.append(f'<aside class="sidebar"><h2>{inline(sec.heading)}</h2>{body_html(sec.lines)}</aside>')
        i += 1

    reflection=by_heading.get("LOOK BACK AT YOUR DECISIONS")
    lessons=next((s for s in sections if s.heading.upper().startswith("LESSONS —") or s.heading.upper().startswith("LESSONS -")), None)
    sources=by_heading.get("SOURCE ENTRIES")
    parts.append('<main class="closing">')
    if reflection: parts.append(f'<section><h2>LOOK BACK AT YOUR DECISIONS</h2>{body_html(reflection.lines)}</section>')
    if lessons: parts.append(f'<section><h2>{inline(lessons.heading)}</h2>{body_html(lessons.lines)}</section>')
    parts.append(f'<section><h2>PLAY AGAIN</h2><p>{inline(tpl["play"])}</p></section>')
    parts.append(f'<section><h2>PRIVACY, SOURCES &amp; CONTRIBUTIONS</h2><p>{inline(tpl["privacy"])}</p></section>')
    parts.append(f'<section><h2>SOURCES</h2><p>{inline(tpl["sources"])}</p>')
    if sources: parts.append('<div class="source-list">'+body_html(sources.lines, evidence=False)+'</div>')
    parts.append('</section></main></body></html>')
    return "".join(parts)


def web_options_html(lines: list[str], decision_id: str) -> str:
    intro: list[str] = []
    options: list[tuple[str, str]] = []
    for para in paragraphs(lines):
        match = OPTION.match(para)
        if match:
            options.append((match.group(1), match.group(2)))
        else:
            intro.append(para)
    if not options:
        raise ValueError("WHAT DO YOU DO? requires A./B./C. option paragraphs")
    rendered: list[str] = []
    for label, text in options:
        input_id = f"{decision_id}-option-{label.lower()}"
        rendered.append(
            f'<li class="choice"><input type="radio" id="{input_id}" '
            f'name="{decision_id}" value="{label}" data-text="{html.escape(text, quote=True)}">'
            f'<label for="{input_id}"><span class="choice__letter">{label}</span>'
            f'<span>{inline(text)}</span></label></li>'
        )
    return (
        "".join(f"<p>{inline(item)}</p>" for item in intro)
        + '<ol class="choice-list">' + "".join(rendered) + "</ol>"
    )


def render_web(title: str, sections: list[Section], slug: str) -> tuple[str, dict[str, object]]:
    """Render one semantic state at a time from the same parsed source as print."""
    by_heading = {section.heading.upper(): section for section in sections}
    tpl = template_text()
    screens: list[dict[str, str]] = []

    def add_screen(screen_id: str, kind: str, label: str, content: str, **extra: str) -> None:
        screens.append({"id": screen_id, "kind": kind, "label": label, "content": content, **extra})

    add_screen(
        "cover", "cover", "Cover",
        f'<div class="cover__kicker">A DECISION-BASED TEACHING RECONSTRUCTION</div>'
        f'<h1>{inline(title)}</h1><p class="cover__subtitle">Governance, evidence, authority, and uncertainty</p>'
        '<p class="cover__subtitle">Make a choice, commit it, then turn the page to see what the record shows.</p>'
    )
    add_screen("how-to-read", "foundation", "How to read", f'<h2>HOW TO READ THIS</h2><p>{inline(tpl["how"])}</p>')
    provenance = '<h2>PROVENANCE VOCABULARY</h2><div class="provenance-grid">'
    for label, key in (("DOCUMENTED", "documented"), ("RECOLLECTED", "recollected"), ("UNKNOWN", "unknown"), ("TEACHING SCENARIO", "scenario")):
        provenance += semantic_card(label, label, tpl[key].split(":", 1)[-1].strip())
    add_screen("provenance", "foundation", "Provenance", provenance + "</div>")
    for heading, screen_id, label in (
        ("INTENT", "intent", "Intent"),
        ("WHO ARE YOU?", "identity", "Your role"),
        ("ROLES IN THIS STORY", "roles", "Roles"),
    ):
        section = by_heading[heading]
        add_screen(screen_id, "foundation", label, f"<h2>{heading}</h2>{body_html(section.lines)}")
    timeline = by_heading["TIMELINE"]
    add_screen("timeline", "timeline", "Timeline", f"<h2>TIMELINE</h2>{timeline_html(timeline.lines)}")

    reserved = {"INTENT", "WHO ARE YOU?", "ROLES IN THIS STORY", "TIMELINE", "LOOK BACK AT YOUR DECISIONS", "SOURCE ENTRIES"}
    i = 0
    while i < len(sections):
        section = sections[i]
        upper = section.heading.upper()
        match = DECISION_HEADING.match(section.heading)
        if match:
            number, topic = match.groups()
            decision_id = f"decision-{number}"
            content = (
                f'<p class="section-label">DECISION {number}</p><h1>{inline(topic)}</h1>'
                f'<div class="context-block">{body_html(section.lines)}</div>'
            )
            i += 1
            while i < len(sections) and sections[i].heading.upper() != "WHAT DO YOU DO?":
                extra = sections[i]
                content += f'<section><h2 class="section-label">{inline(extra.heading)}</h2>{body_html(extra.lines)}</section>'
                i += 1
            if i >= len(sections):
                raise ValueError(f"Decision {number} lacks WHAT DO YOU DO?")
            decision = sections[i]
            content += f'<section><h2>WHAT DO YOU DO?</h2>{web_options_html(decision.lines, decision_id)}</section>'
            i += 1
            if i >= len(sections) or sections[i].heading.upper() != "DECISION BOUNDARY":
                raise ValueError(f"Decision {number} lacks boundary")
            content += (
                '<div class="boundary"><div><strong>Commit before you continue.</strong>'
                '<div class="committed" data-committed hidden></div></div>'
                '<button class="commit" type="button" data-commit disabled>Submit response</button></div>'
            )
            add_screen(decision_id, "decision", f"Decision {number}", content, decision_id=decision_id)
            i += 1
            if i >= len(sections) or not sections[i].heading.upper().startswith("WHAT THE RECORD SHOWS"):
                raise ValueError(f"Decision {number} lacks reveal")
            reveal = sections[i]
            reveal_id = f"reveal-{number}"
            reveal_content = (
                f'<p class="section-label">WHAT THE RECORD SHOWS</p><h1>{inline(topic)}</h1>'
                f'<aside class="response-recap" data-response-recap="{decision_id}" hidden>'
                '<div class="response-recap__label">YOU CHOSE</div>'
                '<p><strong data-response-label></strong> <span data-response-text></span></p></aside>'
                f'{body_html(reveal.lines)}'
            )
            i += 1
            while i < len(sections):
                followup = sections[i]
                followup_upper = followup.heading.upper()
                if followup_upper == "TEACHING QUESTION":
                    reveal_content += (
                        f'<section class="teaching-question"><h2>{inline(followup.heading)}</h2>'
                        f'{body_html(followup.lines)}</section>'
                    )
                    i += 1
                    continue
                if followup_upper.startswith("TEACHING LESSON"):
                    topic_match = re.match(r"^TEACHING LESSON\s+[—-]\s+(.+)$", followup.heading, re.I)
                    lesson_heading = f'<h2>{inline(topic_match.group(1).strip())}</h2>' if topic_match else ""
                    reveal_content += (
                        '<section class="lesson"><div class="lesson-label">TEACHING LESSON</div>'
                        f'<div class="lesson-body">{lesson_heading}{body_html(followup.lines)}</div></section>'
                    )
                    i += 1
                    continue
                break
            add_screen(
                reveal_id, "reveal", f"The record · {number}",
                reveal_content,
                decision_id=decision_id,
            )
            continue
        if upper.startswith("TEACHING LESSON"):
            topic_match = re.match(r"^TEACHING LESSON\s+[—-]\s+(.+)$", section.heading, re.I)
            topic = topic_match.group(1).strip() if topic_match else "Teaching lesson"
            heading = f"<h2>{inline(topic)}</h2>" if topic_match else ""
            add_screen(
                f"lesson-{len(screens)}", "lesson", topic,
                f'<div class="lesson"><div class="lesson-label">TEACHING LESSON</div>'
                f'<div class="lesson-body">{heading}{body_html(section.lines)}</div></div>',
            )
        elif upper.startswith("SIDEBAR") or upper in {"TEACHING QUESTION", "THE PLAN ENDS HERE"}:
            add_screen(f"support-{len(screens)}", "supporting", section.heading.title(), f"<h2>{inline(section.heading)}</h2>{body_html(section.lines)}")
        elif upper not in reserved and not upper.startswith("LESSONS —") and not upper.startswith("LESSONS -") and upper != "DECISION BOUNDARY" and upper != "WHAT DO YOU DO?" and not upper.startswith("WHAT THE RECORD SHOWS"):
            # Other registered supporting components retain their authored label and body.
            if i > 0 and any(DECISION_HEADING.match(item.heading) for item in sections[:i]):
                add_screen(f"support-{len(screens)}", "supporting", section.heading.title(), f"<h2>{inline(section.heading)}</h2>{body_html(section.lines)}")
        i += 1

    reflection = by_heading.get("LOOK BACK AT YOUR DECISIONS")
    lessons = next((s for s in sections if s.heading.upper().startswith("LESSONS —") or s.heading.upper().startswith("LESSONS -")), None)
    sources = by_heading.get("SOURCE ENTRIES")
    if reflection:
        add_screen("reflection", "closing", "Look back", f"<h2>LOOK BACK AT YOUR DECISIONS</h2>{body_html(reflection.lines)}")
    if lessons:
        add_screen("lessons", "closing", "Lessons", f"<h2>{inline(lessons.heading)}</h2>{body_html(lessons.lines)}")
    add_screen(
        "play-again", "closing", "Play again",
        f'<h2>PLAY AGAIN</h2><p>{inline(tpl["play"])}</p>'
        '<div class="completion-actions">'
        '<button class="commit" type="button" data-restart>Replay story</button>'
        '<a class="secondary-action" href="../">Return to all stories</a></div>',
    )
    source_content = f'<h2>PRIVACY, SOURCES &amp; CONTRIBUTIONS</h2><p>{inline(tpl["privacy"])}</p><h2>SOURCES</h2><p>{inline(tpl["sources"])}</p>'
    if sources:
        source_content += '<div class="source-list">' + body_html(sources.lines, evidence=False) + "</div>"
    add_screen("sources", "closing", "Sources", source_content)

    manifest_screens = [{key: value for key, value in item.items() if key != "content"} for item in screens]
    manifest: dict[str, object] = {"renderer_version": "web-v1", "document": slug, "title": title, "screens": manifest_screens}
    trail = "".join(f'<li data-trail-step>{html.escape(item["label"])}</li>' for item in screens)
    screen_markup: list[str] = []
    for index, item in enumerate(screens):
        classes = f'screen screen--{item["kind"]}'
        attributes = f'id="{item["id"]}" class="{classes}" tabindex="-1" data-screen-index="{index}"'
        if item["kind"] == "decision":
            attributes += f' data-decision="{item["decision_id"]}"'
        screen_markup.append(f'<article {attributes} hidden>{item["content"]}</article>')
    manifest_json = json.dumps(manifest, ensure_ascii=False).replace("<", "\\u003c")
    document = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<title>{html.escape(title)} · Playable edition</title><link rel="icon" href="../favicon.svg">'
        '<link rel="stylesheet" href="web.css"></head>'
        f'<body data-edition="{html.escape(slug, quote=True)}"><a class="skip-link" href="#reader">Skip to the zine</a>'
        '<div class="app"><aside class="trail" aria-label="Reading progress">'
        '<a class="all-stories" href="../">All stories</a>'
        f'<h1 class="trail__title">{html.escape(title)}</h1><p class="trail__meta">Playable edition</p>'
        f'<hr class="trail__rule"><details class="trail__contents" open><summary>Contents and progress</summary>'
        f'<ol class="trail__steps">{trail}</ol></details></aside>'
        f'<main class="reader" id="reader"><div class="stage">{"".join(screen_markup)}</div></main></div>'
        '<nav class="controls" aria-label="Page navigation"><button type="button" data-previous>Back</button>'
        '<span class="counter" data-counter></span><button type="button" data-next>Next</button></nav>'
        '<div class="status" role="status" aria-live="polite" data-status></div>'
        f'<script type="application/json" id="zine-manifest">{manifest_json}</script>'
        '<script src="web.js"></script></body></html>'
    )
    return document, manifest


def validate_web_manifest(manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    screens = manifest.get("screens")
    if not isinstance(screens, list):
        return ["Web manifest screens must be a list"]
    ids = [screen.get("id") for screen in screens if isinstance(screen, dict)]
    if len(ids) != len(screens) or len(ids) != len(set(ids)):
        errors.append("Web screen identifiers must be present and unique")
    for index, screen in enumerate(screens):
        if not isinstance(screen, dict) or screen.get("kind") != "reveal":
            continue
        if index == 0 or not isinstance(screens[index - 1], dict):
            errors.append(f'Reveal {screen.get("id")} has no preceding decision screen')
            continue
        previous = screens[index - 1]
        if previous.get("kind") != "decision" or previous.get("decision_id") != screen.get("decision_id"):
            errors.append(f'Reveal {screen.get("id")} must immediately follow its related decision')
        if previous.get("id") == screen.get("id"):
            errors.append(f'Reveal {screen.get("id")} must use a distinct screen identifier')
    return errors


def write_web_edition(title: str, sections: list[Section], slug: str) -> Path:
    site_dir = ROOT / "output" / "site" / slug
    font_dir = site_dir / "fonts"
    font_dir.mkdir(parents=True, exist_ok=True)
    document, manifest = render_web(title, sections, slug)
    manifest_errors = validate_web_manifest(manifest)
    if manifest_errors:
        raise ValueError("; ".join(manifest_errors))
    (site_dir / "index.html").write_text(document, encoding="utf-8")
    (site_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.copy2(ROOT / "renderer" / "web.css", site_dir / "web.css")
    shutil.copy2(ROOT / "renderer" / "web.js", site_dir / "web.js")
    for font in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
        shutil.copy2(ROOT / "assets" / "fonts" / font, font_dir / font)
    write_collection_index()
    return site_dir / "index.html"


def write_collection_index() -> Path:
    site_root = ROOT / "output" / "site"
    entries: list[str] = []
    for manifest_path in sorted(site_root.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        slug = manifest_path.parent.name
        title = str(manifest.get("title", slug))
        screen_count = len(manifest.get("screens", []))
        download_dir = manifest_path.parent / "downloads"
        download_links: list[str] = []
        for suffix, label in (("reader", "Reader PDF"), ("booklet", "Print booklet")):
            source_pdf = ROOT / "output" / "pdf" / f"{slug}-{suffix}.pdf"
            if not source_pdf.is_file():
                continue
            download_dir.mkdir(exist_ok=True)
            destination = download_dir / source_pdf.name
            shutil.copy2(source_pdf, destination)
            download_links.append(
                f'<a class="download" href="{html.escape(slug, quote=True)}/downloads/'
                f'{html.escape(source_pdf.name, quote=True)}" download>{label}</a>'
            )
        entries.append(
            '<li class="story"><div class="story__number" aria-hidden="true">'
            f'{len(entries) + 1:02d}</div><div class="story__body"><h2>{html.escape(title)}</h2>'
            f'<p>{screen_count} steps · choices stay in your browser</p>'
            '<div class="story__actions">'
            f'<a class="start" href="{html.escape(slug, quote=True)}/">Start story</a>'
            f'{"".join(download_links)}</div></div></li>'
        )
    document = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Decision Zines</title><link rel="icon" href="favicon.svg">'
        '<link rel="stylesheet" href="collection.css"></head><body>'
        '<a class="skip-link" href="#stories">Skip to stories</a><header class="masthead">'
        '<p class="masthead__mark" aria-hidden="true">?</p><div><h1>Decision Zines</h1>'
        '<p>Choose what you would do. Commit to it. Then see what the record shows.</p></div></header>'
        f'<main id="stories"><ol class="story-list">{"".join(entries)}</ol></main>'
        '<footer><p>Interactive teaching stories about making decisions with incomplete information.</p></footer>'
        '</body></html>'
    )
    index_path = site_root / "index.html"
    index_path.write_text(document, encoding="utf-8")
    shutil.copy2(ROOT / "renderer" / "collection.css", site_root / "collection.css")
    shutil.copy2(ROOT / "renderer" / "favicon.svg", site_root / "favicon.svg")
    font_dir = site_root / "fonts"
    font_dir.mkdir(exist_ok=True)
    for font in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
        shutil.copy2(ROOT / "assets" / "fonts" / font, font_dir / font)
    return index_path


def impose(reader_path: Path, booklet_path: Path) -> None:
    from pypdf import PdfReader, PdfWriter, Transformation, PageObject
    reader=PdfReader(str(reader_path)); pages=list(reader.pages)
    while len(pages)%4: pages.append(PageObject.create_blank_page(width=396,height=612))
    n=len(pages); writer=PdfWriter()
    def sheet(left, right):
        out=PageObject.create_blank_page(width=792,height=612)
        out.merge_transformed_page(pages[left-1],Transformation().translate(tx=0,ty=0))
        out.merge_transformed_page(pages[right-1],Transformation().translate(tx=396,ty=0))
        writer.add_page(out)
    for offset in range(0,n//2,2):
        sheet(n-offset,1+offset)
        sheet(2+offset,n-1-offset)
    with booklet_path.open('wb') as f: writer.write(f)


def convert_to_device_gray(pdf_path: Path) -> None:
    """Rewrite a neutral PDF using an explicit grayscale color space."""
    ghostscript = shutil.which("gs")
    if not ghostscript:
        print("WARNING: Ghostscript not found; PDF remains neutral RGB.", file=sys.stderr)
        return
    gray_path = pdf_path.with_name(pdf_path.stem + "-device-gray.pdf")
    subprocess.run([
        ghostscript,
        "-q",
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.7",
        "-dAutoRotatePages=/None",
        "-sColorConversionStrategy=Gray",
        "-dProcessColorModel=/DeviceGray",
        f"-sOutputFile={gray_path}",
        str(pdf_path),
    ], check=True)
    if not gray_path.exists() or gray_path.stat().st_size < 1024:
        raise RuntimeError("Ghostscript did not produce a valid DeviceGray PDF")
    gray_path.replace(pdf_path)


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('source',type=Path); ap.add_argument('--slug',default='zine'); ap.add_argument('--chrome',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'); ap.add_argument('--web-only', action='store_true', help='Build the portable static edition without rendering PDFs')
    args=ap.parse_args(); title,sections=parse(args.source)
    errors=validate(sections)
    if errors:
        print("\n".join("ERROR: "+x for x in errors),file=sys.stderr); return 1
    html_dir=ROOT/'output'/'html'; pdf_dir=ROOT/'output'/'pdf'; html_dir.mkdir(parents=True,exist_ok=True); pdf_dir.mkdir(parents=True,exist_ok=True)
    html_path=html_dir/f'{args.slug}-reader.html'; reader=pdf_dir/f'{args.slug}-reader.pdf'; booklet=pdf_dir/f'{args.slug}-booklet.pdf'
    html_path.write_text(render(title,sections),encoding='utf-8')
    site_path = write_web_edition(title, sections, args.slug)
    if args.web_only:
        print(site_path)
        return 0
    reader.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix=f'{args.slug}-chrome-', dir='/private/tmp') as profile:
        command = [args.chrome,'--headless','--disable-gpu','--disable-background-networking','--disable-component-update','--no-first-run','--no-default-browser-check','--no-pdf-header-footer',f'--user-data-dir={profile}',f'--print-to-pdf={reader}',html_path.resolve().as_uri()]
        try:
            subprocess.run(command, check=True, timeout=20)
        except subprocess.TimeoutExpired:
            # Some macOS Chrome builds leave helper processes alive after the
            # print job completes. The requested PDF is still authoritative.
            if not reader.exists() or reader.stat().st_size < 1024:
                raise
    timeline_section = next(section for section in sections if section.heading.upper() == "TIMELINE")
    decision_topics = {
        int(match.group(1)): match.group(2)
        for section in sections
        if (match := DECISION_HEADING.match(section.heading))
    }
    add_running_timeline(reader, timeline_phase_labels(timeline_section.lines), decision_topics)
    convert_to_device_gray(reader)
    impose(reader,booklet)
    print(reader); print(booklet); print(site_path); return 0


if __name__=='__main__': raise SystemExit(main())
