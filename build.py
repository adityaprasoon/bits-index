"""Build the static site: injects links from links.json into src/index.html -> dist/."""

import json
import shutil
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
DEFAULT_SECTION = "General"


def load_links():
    data = json.loads((ROOT / "links.json").read_text(encoding="utf-8"))
    if not isinstance(data, list):
        sys.exit("links.json must contain a JSON list")

    sections = {}
    for i, item in enumerate(data):
        label = str(item.get("label", "")).strip()
        link = str(item.get("link", "")).strip()
        if not label or not link:
            sys.exit(f"links.json entry {i} is missing 'label' or 'link'")
        if urlparse(link).scheme not in ("http", "https"):
            sys.exit(f"links.json entry {i} has an invalid URL: {link}")
        description = str(item.get("description") or "").strip()
        section = str(item.get("section") or DEFAULT_SECTION).strip()
        sections.setdefault(section, []).append((label, link, description))
    return sections


def render(sections):
    parts = []
    for name, links in sections.items():
        items = "\n".join(
            f'        <li><a href="{escape(link)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a>'
            + (f' <span class="desc">{escape(desc)}</span>' if desc else "")
            + "</li>"
            for label, link, desc in links
        )
        parts.append(
            f'    <section class="section" data-section="{escape(name)}">\n'
            f"      <h2>{escape(name)}</h2>\n"
            f"      <ul>\n{items}\n      </ul>\n"
            f"    </section>"
        )
    return "\n".join(parts)


def main():
    sections = load_links()
    template = (SRC / "index.html").read_text(encoding="utf-8")
    html = template.replace("<!-- LINKS -->", render(sections)).replace(
        "<!-- BUILD_DATE -->", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    )

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST)
    (DIST / "index.html").write_text(html, encoding="utf-8")

    total = sum(len(v) for v in sections.values())
    print(f"Built dist/index.html with {total} links in {len(sections)} sections")


if __name__ == "__main__":
    main()
