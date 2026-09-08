#!/usr/bin/env python3
"""Build a reader HTML/PDF and booklet PDF from semantic teaching Markdown.

This v1 formatter intentionally accepts the heading-based semantic Markdown
produced by the Google Doc formatting guide. It expands standard-v1 template
copy and enforces decision-boundary/reveal ordering.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
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
            cls = label.lower().replace(" ", "-")
            chunks.append(f'<div class="evidence-inline {cls}"><b>{label}</b><p>{inline(text)}</p></div>')
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
        cls = label.lower().replace(" ", "-")
        parts.append(f'<div class="provenance-row {cls}"><b>{label}</b><p>{inline(tpl[key].split(":",1)[-1].strip())}</p></div>')
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
    ap=argparse.ArgumentParser(); ap.add_argument('source',type=Path); ap.add_argument('--slug',default='zine'); ap.add_argument('--chrome',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    args=ap.parse_args(); title,sections=parse(args.source)
    errors=validate(sections)
    if errors:
        print("\n".join("ERROR: "+x for x in errors),file=sys.stderr); return 1
    html_dir=ROOT/'output'/'html'; pdf_dir=ROOT/'output'/'pdf'; html_dir.mkdir(parents=True,exist_ok=True); pdf_dir.mkdir(parents=True,exist_ok=True)
    html_path=html_dir/f'{args.slug}-reader.html'; reader=pdf_dir/f'{args.slug}-reader.pdf'; booklet=pdf_dir/f'{args.slug}-booklet.pdf'
    html_path.write_text(render(title,sections),encoding='utf-8')
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
    convert_to_device_gray(reader)
    impose(reader,booklet)
    print(reader); print(booklet); return 0


if __name__=='__main__': raise SystemExit(main())
