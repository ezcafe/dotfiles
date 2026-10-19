"""Stage-id registry checks for my-dev-flow lint.

Enforces handoffs.md / parent-next.md / stages/*.md registry drift (skills-path.md stage-id check).
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

from lint_common import (
    HANDOFFS_MD,
    Issue,
    PACKAGE,
    PARENT_NEXT_MD,
    SUBFLOW_DIRS,
    VALID_STAGE_IDS,
)


def _load_handoff_for() -> ModuleType:
    """Load scripts/handoff-for.py (hyphenated filename — not a normal import)."""
    path = PACKAGE / "scripts" / "handoff-for.py"
    # Prefer already-loaded module (e.g. unit tests) when present and complete
    existing = sys.modules.get("handoff_for")
    if existing is not None and hasattr(existing, "_missing_description_ids"):
        return existing
    spec = importlib.util.spec_from_file_location("handoff_for", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load handoff-for.py from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["handoff_for"] = mod
    spec.loader.exec_module(mod)
    return mod

def stage_ids_from_handoffs(text: str | None = None) -> frozenset[str]:
    """Parse stage ids from handoffs.md Stage id → read / write table."""
    raw = text if text is not None else HANDOFFS_MD.read_text(encoding="utf-8")
    start = raw.find("| Stage id |")
    if start < 0:
        return frozenset()
    ids: set[str] = set()
    for line in raw[start:].splitlines():
        if not line.startswith("|"):
            if ids:
                break
            continue
        if re.match(r"\|[-:\s|]+\|", line) or line.startswith("| Stage id |"):
            continue
        m = re.search(r"`([^`]+)`", line)
        if m:
            ids.add(m.group(1).strip())
    # Parent-only gate ids used on Orchestrator card
    ids.update({"gate-b", "gate-c"})
    return frozenset(ids)
def stage_ids_from_parent_next(text: str | None = None) -> frozenset[str]:
    """Parse stage ids from parent-next.md Stage id / Next table."""
    raw = text if text is not None else PARENT_NEXT_MD.read_text(encoding="utf-8")
    start = raw.find("| Stage id / Next |")
    if start < 0:
        return frozenset()
    ids: set[str] = set()
    for line in raw[start:].splitlines():
        if not line.startswith("|"):
            if ids:
                break
            continue
        if re.match(r"\|[-:\s|]+\|", line) or line.startswith("| Stage id / Next |"):
            continue
        cell = line.split("|")[1].strip() if "|" in line else ""
        # Skip Step 0 / classify row and lens-* wildcard row
        if "Step 0" in cell or cell.startswith("(") or "lens-*" in cell:
            continue
        for m in re.finditer(r"`([^`]+)`", cell):
            token = m.group(1).strip()
            # Drop parenthetical notes like build (armed)
            token = re.split(r"\s+", token)[0]
            if token and token != "lens-*":
                ids.add(token)
    return frozenset(ids)
def stage_ids_from_stages_files() -> frozenset[str]:
    """Collect stem names from subflow stages/*.md (prompt files)."""
    ids: set[str] = set()
    for d in SUBFLOW_DIRS:
        stages = d / "stages"
        if not stages.is_dir():
            continue
        for p in stages.glob("*.md"):
            stem = p.stem
            # Index / overview helpers are not stage ids
            if stem in ("lenses-overview", "parent-loop-hint", "clarity-check"):
                continue
            ids.add(stem)
    return frozenset(ids)
def check_stage_id_registry() -> list[Issue]:
    """Fail when handoffs / parent-next / VALID_STAGE_IDS / stages/*.md drift."""
    issues: list[Issue] = []
    from_h = stage_ids_from_handoffs()
    from_pn = stage_ids_from_parent_next()
    from_files = stage_ids_from_stages_files()
    # Parent gates live on card but have no stages/*.md prompt
    parent_only = frozenset({"gate-b", "gate-c"})

    if VALID_STAGE_IDS != from_h:
        issues.append(
            Issue(
                "error",
                "VALID_STAGE_IDS drift vs handoffs.md — "
                f"only_in_lint={sorted(VALID_STAGE_IDS - from_h)} "
                f"only_in_handoffs={sorted(from_h - VALID_STAGE_IDS)}",
            )
        )

    # handoffs ids not in parent-next (lens-* covered by wildcard row)
    not_in_pn = from_h - from_pn - parent_only
    not_in_pn = {i for i in not_in_pn if not i.startswith("lens-")}
    if not_in_pn:
        issues.append(
            Issue(
                "error",
                f"handoffs stage ids missing from parent-next.md: {sorted(not_in_pn)}",
            )
        )
    extra_pn = from_pn - from_h
    if extra_pn:
        issues.append(
            Issue(
                "error",
                f"parent-next.md stage ids not in handoffs.md: {sorted(extra_pn)}",
            )
        )

    # stages/*.md must match handoffs minus parent-only gates
    expected_files = from_h - parent_only
    if from_files != expected_files:
        issues.append(
            Issue(
                "error",
                "stages/*.md drift vs handoffs.md — "
                f"only_in_files={sorted(from_files - expected_files)} "
                f"only_in_handoffs={sorted(expected_files - from_files)}",
            )
        )

    # R5: every R/W stage id needs a Task description row
    try:
        handoff_for = _load_handoff_for()
        h_text = HANDOFFS_MD.read_text(encoding="utf-8")
        rw = handoff_for._parse_stage_table(h_text)
        desc = handoff_for._parse_description_table(h_text)
        missing_desc = handoff_for._missing_description_ids(rw, desc)
        if missing_desc:
            issues.append(
                Issue(
                    "error",
                    "handoffs.md R/W stage ids missing Task description rows: "
                    f"{missing_desc}",
                )
            )
    except Exception as exc:  # pragma: no cover — import/parse failure
        issues.append(
            Issue(
                "warn",
                f"could not check Task description map: {exc}",
            )
        )

    return issues
