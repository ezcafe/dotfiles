#!/usr/bin/env python3
"""Fetch a URL into vault inbox as Markdown draft (best-effort HTML→text)."""

from __future__ import annotations

import argparse
import html
import re
import urllib.request
from datetime import date
from pathlib import Path


TAG_RE = re.compile(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", re.I)
BLOCK_RE = re.compile(r"</(p|div|h[1-6]|li|tr|br\s*/?)>", re.I)
STRIP_RE = re.compile(r"<[^>]+>")


def html_to_text(raw: str) -> str:
    raw = TAG_RE.sub("", raw)
    raw = BLOCK_RE.sub("\n", raw)
    raw = STRIP_RE.sub("", raw)
    raw = html.unescape(raw)
    lines = [ln.strip() for ln in raw.splitlines()]
    out: list[str] = []
    blank = False
    for ln in lines:
        if not ln:
            if not blank:
                out.append("")
            blank = True
            continue
        blank = False
        out.append(ln)
    return "\n".join(out).strip()


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return (s.strip("-") or "page")[:60]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--root", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--project", default="")
    args = ap.parse_args()
    root = Path(args.root or __import__("os").environ.get("WIKI_ROOT", "~/Documents/my-wiki")).expanduser()
    inbox = root / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(args.url, headers={"User-Agent": "my-wiki-flow/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        raw = resp.read().decode(charset, errors="replace")

    title_m = re.search(r"<title[^>]*>([^<]+)</title>", raw, re.I)
    title = args.title or (title_m.group(1).strip() if title_m else args.url)
    body = html_to_text(raw)
    slug = slugify(title)
    dest = inbox / f"{date.today().isoformat()}-{slug}.md"
    project_line = f"project: {args.project}\n" if args.project else ""
    dest.write_text(
        f"""---
title: {title}
{project_line}tags: [inbox, ingested]
source: {args.url}
updated: {date.today().isoformat()}
summary: Ingested from URL; distill per content-contract (move source to raw/, wikilinks, index.md).
---

# {title}

{body}
""",
        encoding="utf-8",
    )
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
