#!/usr/bin/env python3
"""One-shot preflight / launch pack for a my-dev-flow run directory.

Runs ``lint-run.py <run-dir> --next --derive`` and prints a single **launch pack**:
card snippet + Open paths (soft-cap) + clarity gate + lint exit + always
``--snapshot-consent`` (hitl.md · M1).

Optional Step 0 / parent habit — does not replace per-Task ``--next --derive``.

Usage:
  python3 {my-dev-flow}/scripts/preflight.py <run-dir>
  python3 preflight.py .my-docs/workflow/<slug>/
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
PACKAGE = SCRIPTS.parent
LINT_RUN = SCRIPTS / "lint-run.py"
PARENT_NEXT = PACKAGE / "parent-next.md"
# Soft-cap companion opens in the launch pack (E1 · load budget)
MAX_OPEN_PATHS = 2

CARD_STAGE_RE = re.compile(r"\|\s*Stage id\s*\|\s*([^|\n]+)\s*\|", re.M | re.I)
CARD_NEXT_RE = re.compile(r"\|\s*Next step\s*\|\s*([^|\n]+)\s*\|", re.M | re.I)
CLARITY_STAGES = frozenset(
    {
        "design-phase",
        "analyze",
        "grill",
        "design",
        "tdd-review",
        "build",
        "fix-review",
        "fix-tests",
        "merge",
    }
)


def _first_token(raw: str) -> str:
    return re.split(r"[\s(]", raw.strip().strip("`*_"))[0].strip("`*_").lower()


def _card_snippet(text: str) -> tuple[str, str]:
    sm = CARD_STAGE_RE.search(text)
    nm = CARD_NEXT_RE.search(text)
    stage = _first_token(sm.group(1)) if sm else "(unset)"
    nxt = _first_token(nm.group(1)) if nm else "(unset)"
    return stage, nxt


def _open_paths_for(next_id: str) -> list[str]:
    """Best-effort Open (1–2) from parent-next.md table (soft-cap)."""
    if not PARENT_NEXT.is_file():
        return ["parent-next.md (row for Next)"]
    body = PARENT_NEXT.read_text(encoding="utf-8")
    # Match a table row whose stage cell mentions the next id in backticks
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        if f"`{next_id}`" not in line and next_id not in line.lower():
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        open_cell = parts[1]
        # Extract markdown links / backtick paths
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", open_cell)
        paths = [href for _label, href in links]
        if not paths:
            # bare backtick paths
            paths = re.findall(r"`([^`]+)`", open_cell)
        if paths:
            return paths[:MAX_OPEN_PATHS]
    return [f"parent-next.md (row for `{next_id}`)"]


def _clarity_line(next_id: str) -> str:
    if next_id in CLARITY_STAGES:
        return (
            f"clarity: required — parent writes `clarity-check ok — {next_id}` "
            f"(Tasks must not); open clarity file (parent-next.md)"
        )
    return "clarity: n/a for this Next (not a clarity boundary)"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "run_dir",
        type=Path,
        help="Path to .my-docs/workflow/<slug>/ (must contain 00-run.md)",
    )
    args = p.parse_args()
    run_dir = args.run_dir.resolve()
    run_md = run_dir / "00-run.md"
    if not run_md.is_file():
        print(f"error: missing {run_md}", file=sys.stderr)
        return 2
    if not LINT_RUN.is_file():
        print(f"error: missing {LINT_RUN}", file=sys.stderr)
        return 2

    text = run_md.read_text(encoding="utf-8")
    stage, nxt = _card_snippet(text)
    opens = _open_paths_for(nxt)

    print("=== launch pack ===")
    print(f"run: {run_dir}")
    print(f"card: Stage id={stage} · Next={nxt}")
    print(f"open ({len(opens)}/{MAX_OPEN_PATHS}):")
    for o in opens:
        print(f"  - {o}")
    print(_clarity_line(nxt))
    print(
        f"handoff: python3 {PACKAGE / 'scripts' / 'handoff-for.py'} {nxt}"
        if nxt not in ("(unset)", "gate-b", "gate-c")
        else f"handoff: parent-only for Next={nxt} (no Task) — hitl-gate-b/c.md"
    )
    print("--- lint: lint-run.py --next --derive ---")
    proc = subprocess.run(
        [sys.executable, str(LINT_RUN), str(run_dir), "--next", "--derive"],
        check=False,
    )
    print(f"lint exit: {proc.returncode}")
    # M1: always snapshot consent on launch pack (fail-closed path uses snap later)
    print("--- consent: lint-run.py --snapshot-consent ---")
    snap = subprocess.run(
        [sys.executable, str(LINT_RUN), str(run_dir), "--snapshot-consent"],
        check=False,
    )
    print(f"consent-snap exit: {snap.returncode}")
    if snap.returncode != 0 and proc.returncode == 0:
        print(
            "preflight: blocked — --snapshot-consent failed "
            "(hitl.md Parent-only consent · M1)"
        )
        print("=== end launch pack ===")
        return snap.returncode
    if proc.returncode == 0:
        print(
            "preflight: ok — Task handoff allowed "
            "(consent snap written; after Task run --check-consent-writes)"
        )
    elif proc.returncode == 1:
        print(
            "preflight: blocked — fix do-not-launch / Decision N before launch "
            "(invariants.md · hitl.md · parent-next.md)"
        )
    else:
        print(f"preflight: lint exited {proc.returncode}")
    print("=== end launch pack ===")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
