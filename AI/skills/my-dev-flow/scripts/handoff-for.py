#!/usr/bin/env python3
"""Print base handoff block + one stage row from handoffs.md.

Usage:
  python handoff-for.py <stage-id>
  python handoff-for.py build --slug 20261013-fix-login

Parses the Stage id → read / write markdown table in handoffs.md
(sibling of this script's parent package). Prefer this over loading
the whole handoffs table into context.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HANDOFFS = Path(__file__).resolve().parent.parent / "handoffs.md"

BASE_BLOCK = """Repo root: <absolute path>
Workflow slug: {slug}
Stage: {stage_id}
00-run.md: .my-docs/workflow/{slug}/00-run.md
Read only the artifacts listed for this stage (do not open others unless a listed file links to them).
Write only: <write list for stage>
Use simple plain words. Fresh context — do not assume prior chat or other agents' memory.
Honor artifact size caps in my-dev-flow/handoffs.md.
Resolve skill paths per my-dev-flow/skills-path.md ({{my-dev-flow}}, {{myplan}}, etc.).
Severity exit per my-dev-flow/severity.md (Critical/Major block clean; defer Enhancement).
"""


def _parse_stage_table(text: str) -> dict[str, tuple[str, str]]:
    """Return stage_id -> (read, write) from the Stage id → read / write table."""
    # Find the table under "## Stage-scoped handoff" / "### Stage id → read / write"
    start = text.find("| Stage id |")
    if start < 0:
        start = text.find("| Stage id | Read")
    if start < 0:
        raise SystemExit("error: could not find Stage id table in handoffs.md")

    rows: dict[str, tuple[str, str]] = {}
    for line in text[start:].splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        if re.match(r"\|[-:\s|]+\|", line):
            continue
        if line.startswith("| Stage id |"):
            continue
        # Protect escaped pipes inside cells (e.g. verify-pass \| verify-fail)
        protected = line.replace("\\|", "\0")
        parts = [p.strip().replace("\0", "|") for p in protected.strip().strip("|").split("|")]
        if len(parts) < 3:
            continue
        stage_cell, read_cell, write_cell = parts[0], parts[1], parts[2]
        # Stage id may be wrapped in backticks: `build`
        m = re.search(r"`([^`]+)`", stage_cell)
        if not m:
            continue
        stage_id = m.group(1).strip()
        rows[stage_id] = (read_cell, write_cell)
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("stage_id", help="Stage id from handoffs.md (e.g. build, design-phase)")
    p.add_argument(
        "--slug",
        default="<slug>",
        help="Workflow slug for path expansion (default: <slug>)",
    )
    p.add_argument(
        "--handoffs",
        type=Path,
        default=HANDOFFS,
        help="Path to handoffs.md (default: package handoffs.md)",
    )
    args = p.parse_args()

    if not args.handoffs.is_file():
        print(f"error: missing {args.handoffs}", file=sys.stderr)
        return 2

    text = args.handoffs.read_text(encoding="utf-8")
    rows = _parse_stage_table(text)
    stage = args.stage_id.strip().strip("`")
    if stage not in rows:
        known = ", ".join(sorted(rows))
        print(f"error: unknown stage id {stage!r}", file=sys.stderr)
        print(f"known: {known}", file=sys.stderr)
        return 1

    read_cell, write_cell = rows[stage]
    print(BASE_BLOCK.format(slug=args.slug, stage_id=stage).rstrip())
    print()
    print(f"### Stage row: `{stage}`")
    print(f"Read: {read_cell}")
    print(f"Write: {write_cell}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
