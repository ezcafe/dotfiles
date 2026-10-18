"""Gate B lint checks for my-dev-flow.

Enforces hitl.md Gate B approved / veto / async-notify Build armed / design-backloop / Mode×HITL Gate B rules.
"""
from __future__ import annotations

import re

from pathlib import Path

from lint_common import (
    ASYNC_NOTIFY_REQUESTED_RE,
    BUILD_ARMED_RE,
    CARD_NEXT_RE,
    DESIGN_BACKLOOP_RE,
    DESIGN_BACKLOOP_RECOVERY_STAGES,
    GATE_B_APPROVED_RE,
    HAS_API_LINE_RE,
    HAS_AUTH_LINE_RE,
    HAS_DB_LINE_RE,
    HITL_GATE_B_RE,
    Issue,
    REQUIRED_FIELD_PATTERNS,
    VALID_HITL_TIER,
    VETO_WINDOW_RE,
    _async_arm_timestamps,
    _async_digest_timestamps,
    _async_gap_pending_tokens,
    _card_next_stage_id,
    _first_token,
    _has_provenance,
    _hhmm_to_minutes,
    _looks_like_template,
    _notes_blob,
    _parsed_yes_no,
    _provenance_quote_ok,
    _read_async_gap_sidecar,
    _run_log_blob,
    _run_log_timestamped_entries,
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
    """When HITL Gate B is blocking, require Gate B approved + provenance."""
    enforce = before_build or _card_next_stage_id(text) == "build"
    if not enforce:
        return
    tier = _parse_hitl_gate_b(text)
    if tier != "blocking":
        return
    if not _gate_b_approved_ok(text):
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
        return
    if not _has_provenance(text, "gate-b-approved"):
        issues.append(
            Issue(
                "error",
                "Gate B approved without provenance — Notes/Run log must have "
                '`provenance — gate-b-approved — user: "<quote>"` (hitl.md)',
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
def _async_notify_requested_ok(text: str) -> bool:
    """True when Notes have quality ``async-notify requested — user: "…"`` (E4)."""
    blob = _notes_blob(text) + "\n" + _run_log_blob(text)
    for m in ASYNC_NOTIFY_REQUESTED_RE.finditer(blob):
        if _provenance_quote_ok(m.group("quote")):
            return True
    return False


def _check_async_notify_requested(text: str, issues: list[Issue]) -> None:
    """HITL Gate B async-notify requires explicit user request Notes (E4).

    Template seeds HITL Gate B **auto**. Switching to async-notify needs
    ``async-notify requested — user: "<quote ≥12, non-filler>"`` (shape only —
    not chat-proof).
    """
    if _parse_hitl_gate_b(text) != "async-notify":
        return
    if _async_notify_requested_ok(text):
        return
    issues.append(
        Issue(
            "error",
            "HITL Gate B async-notify without Notes "
            '`async-notify requested — user: "<quote ≥12 chars>"` — '
            "seed defaults to auto; only set async-notify after user asks "
            "for a veto window (hitl-gate-b.md · E4)",
        )
    )


def _check_hitl_gate_b_mode(
    text: str, issues: list[Issue], mode_token: str | None
) -> None:
    """Mode full / simple+API/DB/auth must use blocking Gate B (hitl-gate-b.md)."""
    tier = _parse_hitl_gate_b(text)
    if tier is None:
        return
    if mode_token == "full" and tier in ("auto", "async-notify"):
        issues.append(
            Issue(
                "error",
                f"Mode full + HITL Gate B {tier!r} is forbidden — "
                "use blocking (hitl-gate-b.md Default Gate B narrow async)",
            )
        )
        return
    if mode_token == "simple" and tier in ("auto", "async-notify"):
        has_api = _parsed_yes_no(text, HAS_API_LINE_RE)
        has_db = _parsed_yes_no(text, HAS_DB_LINE_RE)
        has_auth = _parsed_yes_no(text, HAS_AUTH_LINE_RE)
        if has_api == "yes" or has_db == "yes" or has_auth == "yes":
            parts: list[str] = []
            if has_api == "yes" or has_db == "yes":
                parts.append("Has API/DB yes")
            if has_auth == "yes":
                parts.append("Has auth/PII/schema yes")
            which = " + ".join(parts)
            issues.append(
                Issue(
                    "error",
                    f"Mode simple + {which} + non-blocking HITL Gate B — "
                    "use blocking (hitl-gate-b.md Default Gate B narrow async)",
                )
            )
    _check_async_notify_requested(text, issues)
def _async_turn_gap_ok(text: str, run_dir: Path | None = None) -> bool:
    """True when async arm evidence meets turn-boundary bar (hitl.md · S2).

    Requires: (1) arm HH:MM strictly later than a digest HH:MM,
    (2) Notes ``async-gap-pending — <digest-ts>`` matching that digest,
    (3) when ``run_dir`` is set, sidecar ``.lint-async-gap`` from a prior
    ``--next`` do-not-launch matching the same digest.

    Inventing Notes ``parent turn gap observed`` alone is **not** enough.
    Residual: without chat integration, a determined agent can still forge
    sidecar + token + later HH:MM in one edit.
    """
    digest_times = _async_digest_timestamps(text)
    arm_times = _async_arm_timestamps(text)
    if not digest_times or not arm_times:
        return False
    pending = _async_gap_pending_tokens(text)
    if not pending:
        return False
    # Digest ts must appear in both Run log digest lines and pending token
    matched_digests = digest_times & pending
    if not matched_digests:
        return False
    if run_dir is not None:
        side = _read_async_gap_sidecar(run_dir)
        if side is None or side not in matched_digests:
            return False
        matched_digests = {side}
    # At least one arm minute strictly later than a matched digest
    for d_ts in matched_digests:
        d_min = _hhmm_to_minutes(d_ts)
        if d_min is None:
            continue
        for a_ts in arm_times:
            a_min = _hhmm_to_minutes(a_ts)
            if a_min is not None and a_min > d_min:
                return True
    return False


def _async_gap_pending_digest_ts(text: str) -> str | None:
    """Best digest timestamp to emit as ``async-gap-pending — HH:MM``."""
    digests = _async_digest_timestamps(text)
    if not digests:
        return None
    # Prefer earliest digest (first post)
    return min(digests, key=lambda t: _hhmm_to_minutes(t) or 0)


def _check_async_gate_b_gap(
    text: str,
    issues: list[Issue],
    *,
    before_build: bool,
    run_dir: Path | None = None,
) -> None:
    """async-notify Gate B veto window / Build armed / machine-checkable turn gap.

    Enforced on ``--before-build`` **or** card Next=`build` (parity with Gate B
    approved — S1).
    """
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    status = _first_token(status_m.group(1)) if status_m else ""
    notes = _notes_blob(text)
    run_log = _run_log_blob(text)
    notes_and_log = notes + "\n" + run_log
    veto_window = bool(VETO_WINDOW_RE.search(notes))
    build_armed = bool(BUILD_ARMED_RE.search(notes_and_log))
    hitl_async = _parse_hitl_gate_b(text) == "async-notify"
    next_m = CARD_NEXT_RE.search(text)
    next_step = (next_m.group(1).strip().lower() if next_m else "")
    next_is_build = next_step.startswith("build") or "build" in next_step.split()
    enforce = before_build or next_is_build

    # Error: Status=running AND Notes still say veto window open (Build launched without clearing)
    if status == "running" and veto_window:
        issues.append(
            Issue(
                "error",
                "Status=running but Notes still say veto window open — "
                "clear window when Build starts (hitl.md)",
            )
        )

    if not enforce:
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

    # Fail-closed turn gap: arm later than digest + pending token (+ sidecar)
    needs_gap = (veto_window or hitl_async) and (
        build_armed or next_is_build or status == "paused"
    )
    if needs_gap and build_armed and not _async_turn_gap_ok(text, run_dir):
        detail = (
            "need arm HH:MM strictly later than digest, Notes "
            "`async-gap-pending — <digest-ts>` matching Run log digest"
        )
        if run_dir is not None and _read_async_gap_sidecar(run_dir) is None:
            detail += (
                ", and `.lint-async-gap` sidecar from a prior `--next` "
                "do-not-launch"
            )
        elif run_dir is not None:
            detail += " (sidecar digest mismatch or missing pending token)"
        issues.append(
            Issue(
                "error",
                f"async-notify Gate B: {detail} — inventing "
                "`parent turn gap observed` or same-turn dual HH:MM is not "
                "enough (hitl.md)",
            )
        )
    elif needs_gap and veto_window and not build_armed:
        pass  # already errored above on missing Build armed
    elif (
        status == "paused"
        and veto_window
        and next_is_build
        and not _async_turn_gap_ok(text, run_dir)
        and not build_armed
    ):
        # Waiting for arm turn — require digest log entry at least once posted
        entries = _run_log_timestamped_entries(text)
        has_digest = any(
            VETO_WINDOW_RE.search(n) or "async-notify" in n.lower() for _, n in entries
        )
        if not has_digest:
            issues.append(
                Issue(
                    "error",
                    "async-notify Gate B: Status paused + veto window open — "
                    "add timestamped Run log entry for digest post (hitl.md)",
                )
            )
