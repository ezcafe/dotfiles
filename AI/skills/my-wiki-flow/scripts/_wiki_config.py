#!/usr/bin/env python3
"""Minimal config.yaml helpers for my-wiki-flow shell scripts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def load_raw(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def upsert_project(cfg_path: Path, slug: str, workspace: str, profile: str) -> None:
    text = load_raw(cfg_path)
    if not text.strip():
        text = f"""root: {cfg_path.parent}
title: My Wiki
storage: local
github_wiki:
  repo: ""
  remote: ""
build:
  site_dir: site
  pagefind: true
nav:
  group_by: project
projects: {{}}
"""
    # Remove existing projects.<slug> block (2-space YAML)
    text = re.sub(
        rf"(?m)^  {re.escape(slug)}:\n(?:    .*\n)*",
        "",
        text,
    )
    block = f"  {slug}:\n    workspace: {workspace}\n    profile: {profile}\n"
    if re.search(r"(?m)^projects:\s*$", text):
        text = re.sub(r"(?m)^projects:\s*$", f"projects:\n{block.rstrip()}", text, count=1)
    elif re.search(r"(?m)^projects:\s*\{\}\s*$", text):
        text = re.sub(
            r"(?m)^projects:\s*\{\}\s*$",
            f"projects:\n{block.rstrip()}",
            text,
            count=1,
        )
    elif "projects:" in text:
        # projects: already has children
        text = re.sub(r"(?m)^projects:\s*\n", f"projects:\n{block}", text, count=1)
    else:
        text = text.rstrip() + f"\n\nprojects:\n{block}"
    cfg_path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def get_project_workspace(cfg_path: Path, slug: str) -> str:
    text = load_raw(cfg_path)
    m = re.search(
        rf"(?m)^  {re.escape(slug)}:\n((?:    .*\n)*)",
        text,
    )
    if not m:
        return ""
    wm = re.search(r"(?m)^\s{4}workspace:\s*(.+)$", m.group(1))
    return wm.group(1).strip().strip('"').strip("'") if wm else ""


def get_github_wiki(cfg_path: Path) -> tuple[str, str]:
    text = load_raw(cfg_path)
    repo = remote = ""
    m = re.search(r"(?m)^github_wiki:\n((?:  .*\n)*)", text)
    if m:
        block = m.group(1)
        rm = re.search(r"(?m)^\s{2}repo:\s*(.*)$", block)
        rem = re.search(r"(?m)^\s{2}remote:\s*(.*)$", block)
        if rm:
            repo = rm.group(1).strip().strip('"').strip("'")
        if rem:
            remote = rem.group(1).strip().strip('"').strip("'")
    return repo, remote


def title_case_slug(slug: str) -> str:
    return " ".join(p.capitalize() for p in slug.replace("_", "-").split("-") if p)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "upsert-project":
        upsert_project(Path(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
        print(f"ok projects.{sys.argv[3]}")
    elif cmd == "workspace":
        print(get_project_workspace(Path(sys.argv[2]), sys.argv[3]))
    elif cmd == "github-wiki":
        repo, remote = get_github_wiki(Path(sys.argv[2]))
        print(f"{repo}\t{remote}")
    elif cmd == "title":
        print(title_case_slug(sys.argv[2]))
    else:
        print(
            "Usage: _wiki_config.py upsert-project|workspace|github-wiki|title ...",
            file=sys.stderr,
        )
        raise SystemExit(2)
