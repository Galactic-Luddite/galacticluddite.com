#!/usr/bin/env python3
"""Check that every page parses and every local link, image and stylesheet resolves."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

PAGES = ("index.html", "privacy/index.html", "support/index.html")


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and name in {"href", "src"}:
                self.urls.append(value)
            elif value and name == "srcset":
                self.urls.extend(item.strip().split()[0] for item in value.split(",") if item.strip())


def verify(root):
    root = root.resolve()
    failures = []
    for page in PAGES:
        source = root / page
        if not source.is_file():
            failures.append(f"missing page: {page}")
            continue
        parser = References()
        parser.feed(source.read_text())
        for reference in parser.urls:
            url = urlsplit(reference)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            target = (root / path.lstrip("/") if path.startswith("/") else source.parent / path).resolve()
            if not target.is_relative_to(root):
                failures.append(f"local reference escapes site: {page}: {reference}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                failures.append(f"missing local reference: {page}: {reference}")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        failures = verify(args.site_root)
    except (OSError, ValueError) as error:
        print(f"FAIL: site validation could not complete: {error}")
        return 1
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        return 1
    print(f"PASS: {len(PAGES)} pages parse and every local reference resolves")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
