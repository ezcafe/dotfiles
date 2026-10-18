"""Gate B lint checks for my-dev-flow.

Enforces hitl.md Gate B approved / veto / async-notify Build armed / design-backloop / Mode×HITL Gate B rules.
"""
from __future__ import annotations

import re

from lint_common import (
    BUILD_ARMED_RE,
    CARD_NEXT_RE,
    DESIGN_BACKLOOP_RE,
    DESIGN_BACKLOOP_RECOVERY_STAGES,
    GATE_B_APPROVED_RE,
    HAS_API_LINE_RE,
    HAS_DB_LINE_RE,
    HITL_GATE_B_RE,
    Issue,
    PARENT_TURN_GAP_RE,
    REQUIRED_FIELD_PATTERNS,
    VALID_GATE_B_VETO,
    VALID_HITL_TIER,
    VETO_WINDOW_RE,
    _card_next_stage_id,
    _first_token,
    _looks_like_template,
    _notes_blob,
    _parsed_yes_no,
    _run_log_blob,
)

def _parse_gate_b_approved(text: str) -> str | None:
    """Return primary Gate B approved token, or None if missing/template.

    Values: ``none`` (not settled), ``yes``, or a named pick (any non-none token).
    """
    m = GATE_B_APPROVED_RE.search(text)
    if not m:
        return None
    raw = m.group(1).strip()
    if _looks_like_template(raw):
        return None
    primary = re.split(r"\s+[—#–-]\s+|\s{2,}", raw, maxsplit=1)[0].strip()
    compact = primary.strip("`*_").lower()
    if compact in ("", "none", "n/a", "-", "—"):
        return "none"
    # Keep original primary (may be "yes" or named pick like "Option 2")
    return primary.strip("`*_")
def _gate_b_approved_ok(text: str) -> bool:
    """True when Gate B approved is yes or a named pick (not none/missing)."""
    val = _parse_gate_b_approved(text)
    if val is None or val.lower() == "none":
        return False
    return True
def _check_gate_b_approved(
    text: str, issues: list[Issue], *, before_build: bool
) -> None:
    """When HITL Gate B is blocking, require Gate B approved before Build."""
    enforce = before_build or _card_next_stage_id(text) == "build"
    if not enforce:
        return
    tier = _parse_hitl_gate_b(text)
    if tier != "blocking":
        return
    if _gate_b_approved_ok(text):
        return
    raw = _parse_gate_b_approved(text)
    if raw is None:
        issues.append(
            Issue(
                "error",
                "Gate B approved missing — set yes (or named pick) after "
                "blocking Gate B yes (hitl.md)",
            )
        )
    else:
        issues.append(
            Issue(
                "error",
                "Gate B approved is none — require yes (or named pick) before "
                "Build when HITL Gate B is blocking (hitl.md)",
            )
        )
def _check_design_backloop_gate_b(
    text: str, issues: list[Issue], *, before_build: bool = False
) -> None:
    """Notes design-backloop: error only when Build is armed; else soft warn.

    Error on ``--before-build`` or card Next=`build` (blocks Build even when
    HITL Gate B is soft). Default lint with Next in recovery stages → warn
    "recovery in progress". Clear token only after fresh Gate B settle
    (stages.md).
    """
    notes = _notes_blob(text)
    if not DESIGN_BACKLOOP_RE.search(notes):
        return
    next_id = _card_next_stage_id(text)
    if before_build or next_id == "build":
        issues.append(
            Issue(
                "error",
                "Notes design-backloop — do not Build; Next design-update → "
                "re-review → Gate B; clear Notes design-backloop only after "
                "fresh Gate B settle (stages.md)",
            )
        )
        return
    if next_id in DESIGN_BACKLOOP_RECOVERY_STAGES or not next_id:
        issues.append(
            Issue(
                "warn",
                "Notes design-backloop — recovery in progress "
                f"(Next `{next_id or 'unset'}`); clear token only after "
                "fresh Gate B settle (stages.md)",
            )
        )
        return
    issues.append(
        Issue(
            "warn",
            "Notes design-backloop present — prefer Next design-update → "
            "re-review → gate-b (not Build) until settle (stages.md)",
        )
    )
def _parse_hitl_gate_b(text: str) -> str | None:
    """Return HITL Gate B tier token, or None if missing/template."""
    m = HITL_GATE_B_RE.search(text)
    if not m:
        return None
    raw = m.group(1).strip()
    if _looks_like_template(raw):
        return None
    primary = re.split(r"\s+[—#–-]\s+|\s{2,}", raw, maxsplit=1)[0].strip()
    token = primary.strip("`*_").lower()
    # Allow "async-notify" as one token (may contain hyphen only)
    if token in VALID_HITL_TIER:
        return token
    # First whitespace token for "blocking (note)"
    first = primary.split()[0].strip("`*_").lower() if primary.split() else ""
    if first in VALID_HITL_TIER:
        return first
    return None
def _check_hitl_gate_b_mode(
    text: str, issues: list[Issue], mode_token: str | None
) -> None:
    """Mode full / simple+API/DB must use blocking Gate B (hitl.md)."""
    tier = _parse_hitl_gate_b(text)
    if tier is None:
        return
    if mode_token == "full" and tier in ("auto", "async-notify"):
        issues.append(
            Issue(
                "error",
                f"Mode full + HITL Gate B {tier!r} is forbidden — "
                "use blocking (hitl.md Default Gate B narrow async)",
            )
        )
        return
    if mode_token == "simple" and tier in ("auto", "async-notify"):
        has_api = _parsed_yes_no(text, HAS_API_LINE_RE)
        has_db = _parsed_yes_no(text, HAS_DB_LINE_RE)
        if has_api == "yes" or has_db == "yes":
            issues.append(
                Issue(
                    "error",
                    "Mode simple + Has API/DB yes + non-blocking HITL Gate B — "
                    "use blocking (hitl.md Default Gate B narrow async)",
                )
            )
def _check_async_gate_b_gap(text: str, issues: list[Issue], *, before_build: bool) -> None:
    """async-notify Gate B veto window / Build armed / parent turn gap."""
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    status = _first_token(status_m.group(1)) if status_m else ""
    notes = _notes_blob(text)
    run_log = _run_log_blob(text)
    notes_and_log = notes + "\n" + run_log
    veto_window = bool(VETO_WINDOW_RE.search(notes))
    build_armed = bool(BUILD_ARMED_RE.search(notes_and_log))
    next_m = CARD_NEXT_RE.search(text)
    next_step = (next_m.group(1).strip().lower() if next_m else "")
    next_is_build = next_step.startswith("build") or "build" in next_step.split()

    # Error: Status=running AND Notes still say veto window open (Build launched without clearing)
    if status == "running" and veto_window:
        issues.append(
            Issue(
                "error",
                "Status=running but Notes still say veto window open — "
                "clear window when Build starts (hitl.md)",
            )
        )

    if not before_build:
        return

    # Cannot Build while veto window open without Build armed
    if veto_window and not build_armed:
        issues.append(
            Issue(
                "error",
                "async-notify Gate B: Notes say veto window open but Build armed "
                "missing — set Build armed on next parent turn / resume before Build "
                "(hitl.md)",
            )
        )

    # paused + Next step build + veto window open → prefer gap evidence
    if status == "paused" and (veto_window or next_is_build) and VETO_WINDOW_RE.search(
        notes_and_log
    ):
        gap_ok = bool(PARENT_TURN_GAP_RE.search(notes_and_log))
        veto_m = REQUIRED_FIELD_PATTERNS["Gate B veto"].search(text)
        veto_ok = False
        if veto_m and not _looks_like_template(veto_m.group(1)):
            veto_ok = _first_token(veto_m.group(1)) in VALID_GATE_B_VETO
        if not gap_ok and not veto_ok:
            issues.append(
                Issue(
                    "error",
                    "async-notify Gate B: Status paused + veto window open — "
                    "add Run log/Notes parent turn gap observed, or set Gate B veto",
                )
            )
        elif not gap_ok:
            issues.append(
                Issue(
                    "warn",
                    "async-notify Gate B: prefer Run log line noting parent turn gap "
                    "before Build (hitl.md)",
                )
            )
