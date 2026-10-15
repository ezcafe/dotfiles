#!/usr/bin/env python3
"""Print base handoff block + one stage row from handoffs.md.

Usage:
  python {my-dev-flow}/scripts/handoff-for.py <stage-id>
  python {my-dev-flow}/scripts/handoff-for.py build --slug 20261013-fix-login
  python handoff-for.py build --skill-root /abs/path/to/my-dev-flow

Parses the Stage id → read / write markdown table in handoffs.md
(sibling of this script's parent package). Prefer this over loading
the whole handoffs table into context.

Resolve ``{my-dev-flow}`` per skills-path.md before launch. Optional
``--skill-root`` writes absolute skill paths into the base block.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
HANDOFFS = PACKAGE / "handoffs.md"  # alias for tests / callers

BASE_BLOCK = """Repo root: <absolute path>
Workflow slug: {slug}
Stage: {stage_id}
00-run.md: .my-docs/workflow/{slug}/00-run.md
Read only the artifacts listed for this stage (do not open others unless a listed file links to them).
Write only: <write list for stage>
Use simple plain words. Fresh context — do not assume prior chat or other agents' memory.
Honor artifact size caps in {handoffs_path}.
Resolve skill paths per {skills_path_path} ({{my-dev-flow}}, {{myplan}}, etc.).
Severity exit per {severity_path} (Critical/Major block clean; defer Enhancement).
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
        default=None,
        help="Path to handoffs.md (default: <skill-root>/handoffs.md)",
    )
    p.add_argument(
        "--skill-root",
        type=Path,
        default=None,
        help=(
            "Resolved absolute my-dev-flow skill root (skills-path.md). "
            "When set, base block uses absolute paths to handoffs / skills-path / severity"
        ),
    )
    args = p.parse_args()

    skill_root = (
        args.skill_root.resolve() if args.skill_root is not None else PACKAGE
    )
    handoffs_path = (
        args.handoffs.resolve()
        if args.handoffs is not None
        else (skill_root / "handoffs.md")
    )

    if not handoffs_path.is_file():
        print(f"error: missing {handoffs_path}", file=sys.stderr)
        return 2

    # Prefer absolute paths when --skill-root is set; else package-relative labels
    if args.skill_root is not None:
        handoffs_ref = str(skill_root / "handoffs.md")
        skills_path_ref = str(skill_root / "skills-path.md")
        severity_ref = str(skill_root / "severity.md")
    else:
        handoffs_ref = "my-dev-flow/handoffs.md"
        skills_path_ref = "my-dev-flow/skills-path.md"
        severity_ref = "my-dev-flow/severity.md"

    text = handoffs_path.read_text(encoding="utf-8")
    rows = _parse_stage_table(text)
    stage = args.stage_id.strip().strip("`")
    if stage not in rows:
        known = ", ".join(sorted(rows))
        print(f"error: unknown stage id {stage!r}", file=sys.stderr)
        print(f"known: {known}", file=sys.stderr)
        return 1

    read_cell, write_cell = rows[stage]
    print(
        BASE_BLOCK.format(
            slug=args.slug,
            stage_id=stage,
            handoffs_path=handoffs_ref,
            skills_path_path=skills_path_ref,
            severity_path=severity_ref,
        ).rstrip()
    )
    print()
    print(f"### Stage row: `{stage}`")
    print(f"Read: {read_cell}")
    print(f"Write: {write_cell}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
