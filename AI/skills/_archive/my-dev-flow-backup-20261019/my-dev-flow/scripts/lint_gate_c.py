"""Gate C lint checks for my-dev-flow.

Enforces hitl.md Gate C approved / test bar / skip-review Build-writes-Smoke fail-closed · verify-and-fix.md stale tokens.
"""
from __future__ import annotations

import re
from pathlib import Path

from lint_common import (
    COMPLEXITY_RE,
    DOCS_ONLY_RE,
    GATE_C_APPROVED_RE,
    GATE_C_TEST_OVERRIDE_RE,
    HAS_API_LINE_RE,
    HAS_DB_LINE_RE,
    Issue,
    MODE_LAST_RUN_RE,
    REQUIRED_FIELD_PATTERNS,
    REVIEW_STALE_RE,
    RESULT_HEADER_RE,
    SMOKE_RESULT_RE,
    SMOKE_RERUN_DONE_RE,
    SMOKE_WAIVE_RE,
    TEST_STALE_RE,
    VALID_GATE_C_ACTIONS,
    VALID_REVIEW_PROFILE,
    _artifact_mtime,
    _card_next_stage_id,
    _first_token,
    _has_provenance,
    _looks_like_template,
    _notes_blob,
    _parse_last_verify_pass_at,
    _parse_result_token,
    _parsed_yes_no,
    _read_artifact,
)

def _parse_gate_c_approved(text: str) -> tuple[str | None, set[str]]:
    """Return (raw_primary, action_set). action_set empty when none/missing."""
    m = GATE_C_APPROVED_RE.search(text)
    if not m:
        return None, set()
    raw = m.group(1).strip()
    if _looks_like_template(raw):
        return raw, set()
    primary = re.split(r"\s+[—#–-]\s+|\s{2,}", raw, maxsplit=1)[0].strip()
    compact = primary.strip("`*_").lower()
    if compact in ("", "none", "n/a", "-", "—"):
        return "none", set()
    parts = [p.strip() for p in re.split(r"[,|/]+", compact) if p.strip()]
    actions = {p for p in parts if p in VALID_GATE_C_ACTIONS}
    return compact, actions
def _check_gate_c_approved(
    text: str, issues: list[Issue], *, before_merge: bool
) -> None:
    """Require durable Gate C approved + provenance when Next=merge / --before-merge."""
    enforce = before_merge or _card_next_stage_id(text) == "merge"
    if not enforce:
        return

    raw, actions = _parse_gate_c_approved(text)
    if raw is None:
        issues.append(
            Issue(
                "error",
                "Gate C approved missing — set comma-separated "
                "commit,push,pr,merge subset after user yes (hitl.md)",
            )
        )
        return
    if raw == "none" or not actions:
        issues.append(
            Issue(
                "error",
                "Gate C approved is none/empty — require explicit approved-actions "
                "before merge (hitl.md)",
            )
        )
        return
    unknown = {
        p.strip()
        for p in re.split(r"[,|/]+", raw)
        if p.strip() and p.strip() not in VALID_GATE_C_ACTIONS
    }
    if unknown:
        issues.append(
            Issue(
                "error",
                f"Gate C approved has unknown tokens {sorted(unknown)} — "
                f"use subset of {sorted(VALID_GATE_C_ACTIONS)}",
            )
        )
        return
    if not _has_provenance(text, "gate-c-approved"):
        issues.append(
            Issue(
                "error",
                "Gate C approved without provenance — Notes/Run log must have "
                '`provenance — gate-c-approved — user: "<quote>"` (hitl.md)',
            )
        )


def _check_waiver_provenance(text: str, issues: list[Issue]) -> None:
    """Reject inventable waiver tokens without provenance (hitl.md · R1)."""
    notes = _notes_blob(text)
    if GATE_C_TEST_OVERRIDE_RE.search(notes) and not _has_provenance(
        text, "gate-c-test-override"
    ):
        issues.append(
            Issue(
                "error",
                "Notes gate-c-test-override without provenance — require "
                '`provenance — gate-c-test-override — user: "<quote>"` (hitl.md)',
            )
        )
    if SMOKE_WAIVE_RE.search(notes) and not _has_provenance(text, "smoke-waive"):
        issues.append(
            Issue(
                "error",
                "Notes smoke-waive without provenance — require "
                '`provenance — smoke-waive — user: "<quote>"` (hitl.md)',
            )
        )
def _check_status_done_requires_merge(
    text: str, issues: list[Issue]
) -> None:
    """Status done only when merge ∈ Gate C approved (stages.md Done criteria)."""
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    if not status_m:
        return
    if _first_token(status_m.group(1)) != "done":
        return
    _raw, actions = _parse_gate_c_approved(text)
    if "merge" in actions:
        return
    issues.append(
        Issue(
            "error",
            "Status=done requires merge in Gate C approved — "
            "PR-only/commit-only stays paused; abort → stopped "
            "(stages.md · results.md · hitl.md)",
        )
    )
# Smoke section body (## Smoke … until next ##) — SoT for smoke-pass/fail tokens
_SMOKE_SECTION_RE = re.compile(
    r"(?ims)^##\s*Smoke\b[^\n]*\n(.*?)(?=^## |\Z)"
)
_SMOKE_FAIL_TOKENS = frozenset({"smoke-fail", "failure"})


def _smoke_evidence_tokens(blob: str) -> list[str]:
    """Smoke-section tokens only — never top-level test ``**Result:**``.

    Sources: ``**Smoke result:**`` (file-wide; lives under Smoke) and any
    ``**Result:**`` inside the ``## Smoke`` section body. Top-level
    ``**Result:** failure`` / ``success`` is test-full/lite, not smoke.
    """
    tokens: list[str] = []
    for m in SMOKE_RESULT_RE.finditer(blob):
        tok = _first_token(m.group(1))
        if tok:
            tokens.append(tok)
    sec_m = _SMOKE_SECTION_RE.search(blob)
    if sec_m:
        for m in RESULT_HEADER_RE.finditer(sec_m.group(1)):
            raw = (m.group(1) or m.group(2) or "").strip()
            if not raw or ("|" in raw and not re.match(
                r"^[a-z0-9 _-]+$", raw.lower().strip("`*_")
            )):
                continue
            primary = re.split(r"\s+[—#–-]\s+|\s{2,}", raw, maxsplit=1)[0].strip()
            if "|" in primary:
                continue
            tok = primary.strip("`*_").lower()
            if tok and tok not in ("", "none", "n/a", "-", "—"):
                tokens.append(tok)
    return tokens


def _smoke_fail_or_failure(run_dir: Path | None) -> bool:
    """True when 06 Smoke section shows smoke-fail or failure (Fix path).

    Smoke fail tokens only from Smoke section evidence (``**Smoke result:**``
    and/or ``**Result:**`` under ``## Smoke``). Top-level ``**Result:**
    failure`` is test Result → use ``_test_log_failure``, not this helper.
    Any Smoke-section fail token wins (M2 fail-closed vs conflicting pass).
    Missing 06 → False (fail-closed; jump-ahead still blocks fix-tests).
    """
    blob = _read_artifact(run_dir, "06-test-log.md")
    if not blob:
        return False
    return any(t in _SMOKE_FAIL_TOKENS for t in _smoke_evidence_tokens(blob))


def _smoke_pass(run_dir: Path | None) -> bool:
    """True when 06 Smoke evidence shows smoke-pass and no fail token (M2).

    Prefer ``**Smoke result:** smoke-pass`` (Build-writes-Smoke SoT). Also
    accepts ``**Result:** smoke-pass`` under ``## Smoke``. E1: when ``## Smoke``
    exists, do **not** fall back to top-level ``**Result:** smoke-pass`` —
    test-full/lite may overwrite top-level to failure/success without clearing
    Smoke; that must not flip unpaid-smoke. Legacy top-level fallback only when
    no ``## Smoke`` section (pre-Build-SoT logs).
    """
    blob = _read_artifact(run_dir, "06-test-log.md")
    if not blob:
        return False
    tokens = _smoke_evidence_tokens(blob)
    # M2: conflicting Smoke-section smoke-pass + smoke-fail|failure → unpaid
    if any(t in _SMOKE_FAIL_TOKENS for t in tokens):
        return False
    if any(t == "smoke-pass" for t in tokens):
        return True
    # E1: ## Smoke present → require Smoke evidence; no legacy top-level
    if _SMOKE_SECTION_RE.search(blob):
        return False
    # Legacy: top-level Result smoke-pass when only Smoke ran (no ## Smoke)
    top = _parse_result_token(blob)
    return top == "smoke-pass"
_TEST_RESULT_TOKENS = frozenset({"success", "failure", "pending"})


def _test_result_token(blob: str) -> str | None:
    """Test-full/lite Result: prefer outside ``## Smoke``, else test tokens.

    Smoke evidence uses ``**Smoke result:**`` and/or ``**Result:**`` under
    ``## Smoke``. Those must not mask top-level test ``failure`` / ``success``
    (E1 — prefer Smoke result; parse test Result outside Smoke).

    1. First ``**Result:**`` after stripping ``## Smoke`` (canonical).
    2. Else first ``success``|``failure``|``pending`` anywhere — so a trailing
       test Result still inside a Smoke section (no following ``##``) is not
       lost to an earlier Smoke-section ``smoke-pass``.
    """
    stripped = _SMOKE_SECTION_RE.sub("\n", blob)
    tok = _parse_result_token(stripped)
    if tok:
        return tok
    for m in RESULT_HEADER_RE.finditer(blob):
        raw = (m.group(1) or m.group(2) or "").strip()
        if not raw:
            continue
        if "|" in raw and not re.match(
            r"^[a-z0-9 _-]+$", raw.lower().strip("`*_")
        ):
            continue
        primary = re.split(r"\s+[—#–-]\s+|\s{2,}", raw, maxsplit=1)[0].strip()
        if "|" in primary:
            continue
        candidate = primary.strip("`*_").lower()
        if candidate in _TEST_RESULT_TOKENS:
            return candidate
    return None


def _test_log_failure(run_dir: Path | None) -> bool:
    """True when 06 top-level Result is ``failure`` (test-full/lite → Fix path).

    Reads first ``**Result:**`` outside ``## Smoke`` so Smoke-section
    ``**Result:** smoke-pass`` cannot mask test failure (E1). Missing 06 or
    other tokens → False (derive re-test / unpaid smoke instead).
    """
    blob = _read_artifact(run_dir, "06-test-log.md")
    if not blob:
        return False
    return _test_result_token(blob) == "failure"


def _test_log_success(run_dir: Path | None, *, expect_mode: str | None) -> bool:
    """True when Result success; if expect_mode set, Test path last run must match.

    Uses first ``**Result:**`` outside ``## Smoke`` (same as ``_test_log_failure``).
    Fail closed when expect_mode is full|lite and Test path last run is missing
    or mismatched (hitl.md Gate C test bar). Accepts legacy ``Mode last run``.
    """
    blob = _read_artifact(run_dir, "06-test-log.md")
    if not blob:
        return False
    if _test_result_token(blob) != "success":
        return False
    if expect_mode is None:
        return True
    m = MODE_LAST_RUN_RE.search(blob)
    if not m:
        return False  # fail closed — Test path last run required for full/lite bar
    mode = _first_token(m.group(1))
    return mode == expect_mode
def _last_verify_pass(text: str) -> bool:
    m = REQUIRED_FIELD_PATTERNS["Last Verify"].search(text)
    if not m:
        return False
    raw = m.group(1).strip()
    if _looks_like_template(raw):
        return False
    return _first_token(raw) == "verify-pass"
def _review_profile(text: str) -> str | None:
    rp_m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    if not rp_m or _looks_like_template(rp_m.group(1)):
        return None
    return _first_token(rp_m.group(1))
def _implied_review_stale(text: str, run_dir: Path | None) -> bool:
    """E2: 05 clean older than Last verify-pass at without Notes review-stale."""
    # Lazy import: _review_clean lives in lint_derive (avoids circular import).
    from lint_derive import _review_clean

    notes = _notes_blob(text)
    if REVIEW_STALE_RE.search(notes):
        return False
    if not _last_verify_pass(text):
        return False
    review = _review_profile(text)
    if review is None or review == "skip-review":
        return False
    if not _review_clean(run_dir, review):
        return False
    epoch = _parse_last_verify_pass_at(text)
    if epoch is None:
        return False
    mt = _artifact_mtime(run_dir, "05-review-log.md")
    if mt is None:
        return False
    return mt < epoch
def _implied_test_stale(text: str, run_dir: Path | None) -> bool:
    """E2: 06 success older than Last verify-pass at without Notes test-stale."""
    notes = _notes_blob(text)
    if TEST_STALE_RE.search(notes):
        return False
    if not _last_verify_pass(text):
        return False
    review = _review_profile(text)
    if review is None or review == "skip-review":
        return False
    expect = "full" if review == "full" else "lite" if review == "lite" else None
    if expect is None or not _test_log_success(run_dir, expect_mode=expect):
        return False
    epoch = _parse_last_verify_pass_at(text)
    if epoch is None:
        return False
    mt = _artifact_mtime(run_dir, "06-test-log.md")
    if mt is None:
        return False
    return mt < epoch
def _check_stale_before_merge(
    text: str,
    issues: list[Issue],
    *,
    before_merge: bool,
    run_dir: Path | None = None,
) -> None:
    """H1/E2: Notes stale tokens + unpaid-vs-clock on --before-merge / Next=merge.

    Independent of gate-c-test-override (stale invalidates prior clean/success).
    ``--next`` keeps do-not-launch (print_next_hint).
    """
    enforce = before_merge or _card_next_stage_id(text) == "merge"
    if not enforce:
        return
    notes = _notes_blob(text)
    if REVIEW_STALE_RE.search(notes):
        issues.append(
            Issue(
                "error",
                "Notes review-stale — re-enter review; clear token after fresh "
                "clean before merge (verify-and-fix.md · hitl.md)",
            )
        )
    elif _implied_review_stale(text, run_dir):
        issues.append(
            Issue(
                "error",
                "05-review-log clean older than Last verify-pass at — re-enter "
                "review (or Notes review-stale) before merge "
                "(verify-and-fix.md Stale · hitl.md)",
            )
        )
    if TEST_STALE_RE.search(notes):
        issues.append(
            Issue(
                "error",
                "Notes test-stale — re-enter test-full/test-lite; clear token "
                "after fresh success before merge (verify-and-fix.md · hitl.md)",
            )
        )
    elif _implied_test_stale(text, run_dir):
        issues.append(
            Issue(
                "error",
                "06-test-log success older than Last verify-pass at — re-enter "
                "test (or Notes test-stale) before merge "
                "(verify-and-fix.md Stale · hitl.md)",
            )
        )
def _independent_smoke_done(text: str) -> bool:
    """True when smoke-waive or smoke-pass-rerun **with** provenance (S5).

    Free-text Notes ``smoke-pass (re-run)`` alone is inventable — rejected.
    """
    notes = _notes_blob(text)
    if SMOKE_WAIVE_RE.search(notes) and _has_provenance(text, "smoke-waive"):
        return True
    if SMOKE_RERUN_DONE_RE.search(notes) and _has_provenance(
        text, "smoke-pass-rerun"
    ):
        return True
    return False
def _docs_only_marked(text: str) -> bool:
    """True when docs-only is marked **and** provenance is present (S5)."""
    notes = _notes_blob(text)
    marked = bool(DOCS_ONLY_RE.search(notes))
    if not marked:
        cm = COMPLEXITY_RE.search(text)
        marked = bool(cm and DOCS_ONLY_RE.search(cm.group(1)))
    if not marked:
        return False
    return _has_provenance(text, "docs-only")
def _check_skip_review_build_only_smoke(
    text: str,
    issues: list[Issue],
    *,
    before_merge: bool,
    run_dir: Path | None,
) -> None:
    """Fail-closed when skip-review merge relies only on Build-writes-Smoke.

    Escape: Notes smoke-waive / smoke-pass (re-run) / gate-c-test-override /
    docs-only — each **with** matching provenance (hitl.md · S5). Bare Notes
    tokens alone are inventable and rejected.
    """
    enforce = before_merge or _card_next_stage_id(text) == "merge"
    if not enforce:
        return
    notes = _notes_blob(text)
    # Override waives only with provenance (bare token is inventable — R1)
    if GATE_C_TEST_OVERRIDE_RE.search(notes) and _has_provenance(
        text, "gate-c-test-override"
    ):
        return
    rp_m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    if not rp_m:
        return
    review = _first_token(rp_m.group(1))
    if review != "skip-review" or _looks_like_template(rp_m.group(1)):
        return
    if not _last_verify_pass(text) or not _smoke_pass(run_dir):
        return  # bar errors cover missing verify/smoke
    if _independent_smoke_done(text):
        return
    if _docs_only_marked(text):
        issues.append(
            Issue(
                "warn",
                "skip-review merge: only Build-writes-Smoke with docs-only + "
                "provenance — warn/allow path (verify-and-fix.md · hitl.md)",
            )
        )
        return
    # Bare docs-only / smoke-pass (re-run) without provenance → error
    cm = COMPLEXITY_RE.search(text)
    bare_docs = bool(DOCS_ONLY_RE.search(notes)) or bool(
        cm and DOCS_ONLY_RE.search(cm.group(1))
    )
    if bare_docs and not _has_provenance(text, "docs-only"):
        issues.append(
            Issue(
                "error",
                "skip-review merge: Notes/Complexity `docs-only` without "
                'provenance — require `provenance — docs-only — user: "…"` '
                "(hitl.md)",
            )
        )
        return
    if SMOKE_RERUN_DONE_RE.search(notes) and not _has_provenance(
        text, "smoke-pass-rerun"
    ):
        issues.append(
            Issue(
                "error",
                "skip-review merge: Notes `smoke-pass (re-run)` without "
                "provenance — require "
                '`provenance — smoke-pass-rerun — user: "…"` (hitl.md)',
            )
        )
        return
    issues.append(
        Issue(
            "error",
            "skip-review merge: only Build-writes-Smoke — require Notes "
            "`smoke-waive` / `smoke-pass (re-run)` / `gate-c-test-override` / "
            "`docs-only` **each with provenance** before Gate C "
            "(verify-and-fix.md · hitl.md)",
        )
    )
def _check_gate_c_test_bar(
    text: str,
    issues: list[Issue],
    *,
    before_merge: bool,
    run_dir: Path | None,
) -> None:
    """Enforce hitl.md Gate C test bar from 00-run + 06-test-log.

    Notes ``gate-c-test-override`` / ``Gate C test override`` waives.
    """
    enforce = before_merge or _card_next_stage_id(text) == "merge"
    if not enforce:
        return

    notes = _notes_blob(text)
    if GATE_C_TEST_OVERRIDE_RE.search(notes) and _has_provenance(
        text, "gate-c-test-override"
    ):
        return

    rp_m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    if not rp_m:
        return
    review = _first_token(rp_m.group(1))
    if review not in VALID_REVIEW_PROFILE or _looks_like_template(rp_m.group(1)):
        return

    mode_m = REQUIRED_FIELD_PATTERNS["Mode"].search(text)
    mode = _first_token(mode_m.group(1)) if mode_m else None
    override_hint = (
        "or Notes gate-c-test-override + provenance "
        '(`provenance — gate-c-test-override — user: "…"`)'
    )

    if review == "full":
        if not _test_log_success(run_dir, expect_mode="full"):
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar (full): need 06-test-log.md Result success "
                    f"and Test path last run full (hitl.md) — {override_hint}",
                )
            )
        return

    if review == "lite":
        if not _test_log_success(run_dir, expect_mode="lite"):
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar (lite): need 06-test-log.md Result success "
                    f"and Test path last run lite (hitl.md) — {override_hint}",
                )
            )
        return

    if review == "skip-review":
        # Illegal skip-review already errors via _check_skip_review_api_db;
        # still require verify-pass + smoke-pass when profile is skip-review.
        if mode == "full":
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar: skip-review forbidden in Mode full "
                    "(lenses.md · hitl.md)",
                )
            )
            return
        if (
            _parsed_yes_no(text, HAS_API_LINE_RE) == "yes"
            or _parsed_yes_no(text, HAS_DB_LINE_RE) == "yes"
        ):
            # skip-review+API/DB already errored elsewhere; bar still fails
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar: skip-review forbidden when Has API/DB yes "
                    "(lenses.md · hitl.md)",
                )
            )
            return
        if not _last_verify_pass(text):
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar (skip-review): need Last Verify verify-pass "
                    f"(hitl.md) — {override_hint}",
                )
            )
        if not _smoke_pass(run_dir):
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar (skip-review): need 06-test-log Smoke "
                    f"result smoke-pass (hitl.md) — {override_hint}",
                )
            )
