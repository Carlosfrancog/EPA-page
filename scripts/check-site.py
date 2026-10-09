#!/usr/bin/env python3
"""Check that internal links and referenced static files resolve locally."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1] / "site"


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        key = {"a": "href", "link": "href", "script": "src", "img": "src", "object": "data"}.get(tag)
        if key and values.get(key):
            self.values.append(values[key] or "")


def main() -> int:
    errors: list[str] = []
    pages = list(ROOT.rglob("*.html"))
    for page in pages:
        parser = References()
        parser.feed(page.read_text(encoding="utf-8"))
        for value in parser.values:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if parsed.path.startswith("/"):
                errors.append(f"{page.relative_to(ROOT)}: absolute link {value}")
                continue
            target = (page.parent / unquote(parsed.path)).resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                errors.append(f"{page.relative_to(ROOT)}: missing {value}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(pages)} HTML pages; all internal links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
