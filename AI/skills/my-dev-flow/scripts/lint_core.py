"""Orchestrator lint checks + CLI helpers for my-dev-flow.

Enforces invariants.md pre-launch checklist pieces (clarity-check, pending parallel, skip-review ban, Verify commands) and stages.md card Next / --next do-not-launch.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

from lint_common import (
    ARTIFACTS_00,
    BUILD_ARMED_RE,
    CALIBRATION_FRICTION_RE,
    CALIBRATION_MODE_OK_RE,
    CALIBRATION_PROFILE_OK_RE,
    CARD_NEXT_RE,
    CARD_STAGE_RE,
    CLARITY_CHECK_HIGH_RISK,
    CLARITY_CHECK_STAGES,
    CODE_REVIEW_ENTRY_STAGES,
    DESIGN_BACKLOOP_RE,
    FIX_ASK_RE,
    FOLD_API_DB_RE,
    HAS_API_LINE_RE,
    HAS_DB_LINE_RE,
    IN_REVIEW_DERIVED,
    Issue,
    JUMP_AHEAD_FROM_PRE_BUILD,
    JUMP_AHEAD_FROM_REVIEW,
    LEGACY_STATUS_HINTS,
    LENS_JUMP_AHEAD_CARDS,
    LENS_PLAN_RE,
    MAIN_THREAD_RE,
    PACKAGE,
    PARENT_NEXT_MD,
    PENDING_PARALLEL_RE,
    POST_GATE_A_STAGES,
    PRE_BUILD_DERIVED,
    PRE_LENS_DERIVED,
    REQUIRED_FIELD_PATTERNS,
    REVIEW_ENTRY_DERIVED,
    REVIEW_STALE_RE,
    SMOKE_RERUN_RE,
    SOFT_MAIN_THREAD_CAP,
    SOFT_TASK_CAP,
    TASK_COUNT_RE,
    TEST_STALE_RE,
    TINY_TWEAK_RE,
    UNPAID_LENS_BLOCK_STAGES,
    VALID_GATE_B_VETO,
    VALID_MODE,
    VALID_PENDING_PARALLEL,
    VALID_REVIEW_PROFILE,
    VALID_STAGE_IDS,
    VALID_STATUS,
    VALID_YES_NO,
    VERIFY_BLOCK_RE,
    VERIFY_FAIL_RE,
    VETO_WINDOW_RE,
    _artifact_exists,
    _card_next_stage_id,
    _card_override_ok,
    _check_yes_no_flag,
    _clarity_boundaries_logged,
    _exact_enum_token,
    _extract_stage_token,
    _first_token,
    _has_provenance,
    _looks_like_template,
    _notes_blob,
    _parsed_yes_no,
    _parse_lens_plan_tokens,
    _parse_result_token,
    _read_artifact,
    _run_log_blob,
    _write_async_gap_sidecar,
)
from lint_derive import (
    _design_review_result,
    _lens_plan_entries,
    _merged_lenses_result,
    _next_stage_legality_warns,
    _unpaid_lens_stages,
    check_results,
    derive_expected_next,
)
from lint_gate_b import (
    _async_gap_pending_digest_ts,
    _async_turn_gap_ok,
    _check_async_gate_b_gap,
    _check_design_backloop_gate_b,
    _check_gate_b_approved,
    _check_hitl_gate_b_mode,
    _gate_b_approved_ok,
    _parse_hitl_gate_b,
)
from lint_gate_c import (
    _check_gate_c_approved,
    _check_gate_c_test_bar,
    _check_skip_review_build_only_smoke,
    _check_stale_before_merge,
    _check_status_done_requires_merge,
    _check_waiver_provenance,
    _implied_review_stale,
    _implied_test_stale,
    _parse_gate_c_approved,
)
from lint_stage_ids import check_stage_id_registry

def _check_lens_plan_api_db(
    text: str, issues: list[Issue], *, before_code_review: bool
) -> None:
    """Require Lens plan api/db when Has API/DB yes (not tiny-tweak / Notes fold)."""
    next_id = _card_next_stage_id(text)
    enforce = before_code_review or next_id in CODE_REVIEW_ENTRY_STAGES
    if not enforce:
        return

    has_api = _parsed_yes_no(text, HAS_API_LINE_RE)
    has_db = _parsed_yes_no(text, HAS_DB_LINE_RE)
    needs_api = has_api == "yes"
    needs_db = has_db == "yes"
    if not needs_api and not needs_db:
        return

    notes = _notes_blob(text)
    if TINY_TWEAK_RE.search(notes) or FOLD_API_DB_RE.search(notes):
        return

    tokens = _parse_lens_plan_tokens(text)
    missing: list[str] = []
    if needs_api and "api" not in tokens:
        missing.append("api")
    if needs_db and "db" not in tokens:
        missing.append("db")
    if not missing:
        return
    issues.append(
        Issue(
            "error",
            "Lens plan missing "
            + "+".join(missing)
            + " — Has API/DB yes requires api/db in Lens plan "
            "(or Notes tiny-contract-tweak / fold) before code review (lenses.md)",
        )
    )
def _parse_pending_parallel(text: str, issues: list[Issue]) -> str | None:
    m = PENDING_PARALLEL_RE.search(text)
    if not m:
        return None
    return _exact_enum_token(
        m.group(1), VALID_PENDING_PARALLEL, "Pending parallel", issues
    )
def _check_skip_review_api_db(text: str, issues: list[Issue]) -> None:
    rp = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    if not rp:
        return
    raw = rp.group(1).strip()
    if _looks_like_template(raw):
        return
    token = _first_token(raw)
    if token != "skip-review":
        return
    if _parsed_yes_no(text, HAS_API_LINE_RE) == "yes":
        issues.append(
            Issue("error", "skip-review not allowed when Has API = yes — reclassify")
        )
    if _parsed_yes_no(text, HAS_DB_LINE_RE) == "yes":
        issues.append(
            Issue("error", "skip-review not allowed when Has DB = yes — reclassify")
        )
def _check_pending_parallel(
    text: str,
    issues: list[Issue],
    *,
    before_design_review: bool,
    run_dir: Path | None,
    mode_token: str | None,
) -> None:
    """H4: Pending parallel for Mode full API∥DB only.

    Mode simple keeps Pending parallel ``none`` (API/DB fold into
    design-verify-phase). Do not require ``api|db`` in simple.
    """
    pending = _parse_pending_parallel(text, issues)

    # Mode simple: none is correct even when Has API+DB are yes
    if mode_token == "simple":
        if pending in ("api|db", "api", "db"):
            issues.append(
                Issue(
                    "warn",
                    "Mode simple: Pending parallel should be none "
                    "(API/DB fold into design-verify-phase) — "
                    f"got {pending}",
                )
            )
        return

    if mode_token != "full":
        return

    has_api = _parsed_yes_no(text, HAS_API_LINE_RE)
    has_db = _parsed_yes_no(text, HAS_DB_LINE_RE)
    notes = _notes_blob(text)
    tiny = bool(TINY_TWEAK_RE.search(notes))

    needs_parallel = (
        has_api == "yes" and has_db == "yes" and not tiny
    )
    if not needs_parallel:
        return

    api_done = _artifact_exists(run_dir, "03a-api-contract-review.md")
    db_done = _artifact_exists(run_dir, "03a-db-design-review.md")
    both_done = api_done and db_done
    one_only = api_done != db_done

    if before_design_review or needs_parallel:
        if pending is None and PENDING_PARALLEL_RE.search(text) is None:
            if not both_done:
                issues.append(
                    Issue(
                        "error" if before_design_review else "warn",
                        "Pending parallel missing — set api|db until both "
                        "03a-api and 03a-db exist (or Notes tiny-contract-tweak / skipped)",
                    )
                )
        elif pending == "none" and not both_done:
            issues.append(
                Issue(
                    "error" if before_design_review else "warn",
                    "Pending parallel is none but Has API+DB and isolated reviews "
                    "not both done — set api|db until both exist",
                )
            )
        elif pending == "api|db" and both_done:
            issues.append(
                Issue(
                    "warn",
                    "Pending parallel still api|db but both 03a-api and 03a-db exist — set none",
                )
            )

    if one_only and (pending in (None, "api|db", "api", "db") or pending == "none"):
        missing = "03a-db-design-review.md" if api_done else "03a-api-contract-review.md"
        present = "03a-api-contract-review.md" if api_done else "03a-db-design-review.md"
        issues.append(
            Issue(
                "error",
                f"{present} exists without {missing} while Pending parallel is "
                f"{pending or 'missing'} — keep api|db and finish the other, or Notes skip",
            )
        )
def _check_isolated_api_db_files(
    text: str,
    issues: list[Issue],
    *,
    before_design_review: bool,
    run_dir: Path | None,
    mode_token: str | None,
) -> None:
    """H1: Mode full + Has API/DB yes (not tiny) → require matching 03a-* file.

    Skip when card Next is the matching isolated stage (file not written yet).
    """
    if not before_design_review or mode_token != "full":
        return
    notes = _notes_blob(text)
    if TINY_TWEAK_RE.search(notes):
        return
    next_id = _card_next_stage_id(text)
    has_api = _parsed_yes_no(text, HAS_API_LINE_RE)
    has_db = _parsed_yes_no(text, HAS_DB_LINE_RE)
    if has_api == "yes" and next_id != "api-contract-review":
        if not _artifact_exists(run_dir, "03a-api-contract-review.md"):
            issues.append(
                Issue(
                    "error",
                    "Has API = yes requires 03a-api-contract-review.md before "
                    "design-review (or Notes tiny-contract-tweak) — lenses.md",
                )
            )
    if has_db == "yes" and next_id != "db-design-review":
        if not _artifact_exists(run_dir, "03a-db-design-review.md"):
            issues.append(
                Issue(
                    "error",
                    "Has DB = yes requires 03a-db-design-review.md before "
                    "design-review (or Notes tiny-contract-tweak) — lenses.md",
                )
            )
def _clarity_check_logged(text: str, *, stage_id: str = "") -> bool:
    """True when clarity-check token satisfies soft or hard rule for stage.

    Soft (design/analyze/grill/tdd-review): presence-any once-per-run.
    Hard (build / fix-* / merge): boundary must match Next (parent-next.md · R3).
    """
    boundaries = _clarity_boundaries_logged(text)
    if not boundaries:
        return False
    target = (stage_id or "").strip().lower()
    if not target or target not in CLARITY_CHECK_HIGH_RISK:
        return True  # soft: any token unlocks
    return target in boundaries


def _review_profile_token(text: str) -> str | None:
    m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    if not m:
        return None
    return _first_token(m.group(1))


def _notes_allow_review_entry_sidepath(card: str, text: str) -> bool:
    """True when Notes unlock smoke / fix-tests during review-entry (T2)."""
    notes = _notes_blob(text)
    if card == "smoke" and SMOKE_RERUN_RE.search(notes):
        return True
    if card == "fix-tests" and FIX_ASK_RE.search(notes):
        return True
    return False


def _unsafe_card_derive_mismatch(
    card: str, derived: str, text: str, run_dir: Path | None
) -> str | None:
    """Return reason when card vs derived mismatch is unsafe (R4/S3/T1/T2/U1), else None.

    Soft warn only for peer/parallel or minor reorder. Jump-ahead to
    review/test/fix/merge while derived is still pre-Build or pre-verify,
    post-Build jump past unfinished review, or soft lens / merge-findings
    before Adv/Quality / lite / Fix, is **unsafe** → do-not-launch unless
    card-override + provenance (or skip-review for post-review jumps).
    Legitimate lens cards when derived is that lens (Lens plan unpaid path)
    match at ``card == derived`` and are not unsafe.
    """
    if not card or not derived or card == derived:
        return None
    if "||" in derived:
        parts = derived.split("||")
        if card in parts:
            return None
        return None  # parallel hint stays warn-only
    if card == "merge" and derived not in ("merge", "gate-c"):
        return f"card Next `merge` while derived `{derived}`"
    if card == "build":
        design = _design_review_result(run_dir)
        if design != "clean":
            return (
                "card Next `build` while design not clean "
                f"(03a Result is {design or 'missing'})"
            )
        if derived in PRE_BUILD_DERIVED or derived.startswith("design"):
            return f"card Next `build` while derived `{derived}`"
    # S3: review/test/fix/merge while still pre-Build or awaiting Build
    if derived in PRE_BUILD_DERIVED or derived == "build":
        if card in JUMP_AHEAD_FROM_PRE_BUILD:
            return (
                f"card Next `{card}` while derived `{derived}` "
                "(pre-Build / pre-verify jump-ahead)"
            )
    # T2: Quality (and peers) before Adversarial
    if card == "quality" and derived == "adversarial":
        return (
            "card Next `quality` while derived `adversarial` "
            "(Adv before Quality)"
        )
    # T2: smoke / fix-tests while still at review entry
    if derived in REVIEW_ENTRY_DERIVED and card in ("smoke", "fix-tests"):
        if not _notes_allow_review_entry_sidepath(card, text):
            return (
                f"card Next `{card}` while derived `{derived}` "
                "(review-entry; need Notes smoke re-run / Fix ask, "
                "or card-override + provenance)"
            )
    # U1: lens-* / merge-findings while still Adv / Quality / lite / Fix
    if derived in PRE_LENS_DERIVED and card in LENS_JUMP_AHEAD_CARDS:
        return (
            f"card Next `{card}` while derived `{derived}` "
            "(lens / merge-findings before Adv/Quality / pre-lens)"
        )
    # T1: test / gate-c / merge while derived still in review pipeline
    if derived in IN_REVIEW_DERIVED and card in JUMP_AHEAD_FROM_REVIEW:
        if _review_profile_token(text) == "skip-review":
            return None
        # fix-tests at review-entry already handled above with Notes exception;
        # Fix ask also unlocks fix-tests later in the review pipeline
        if card == "fix-tests" and FIX_ASK_RE.search(_notes_blob(text)):
            return None
        return (
            f"card Next `{card}` while derived `{derived}` "
            "(post-Build review still unpaid)"
        )
    return None
def _calibration_blob(run_dir: Path | None) -> str:
    """Read workflow ``_calibration.md`` (parent of slug) or run-dir copy."""
    if run_dir is None:
        return ""
    for path in (run_dir.parent / "_calibration.md", run_dir / "_calibration.md"):
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return ""
def _calibration_evidence(text: str, run_dir: Path | None) -> bool:
    """Notes Mode OK? / profile OK? / friction, or same in ``_calibration.md``."""
    for blob in (_notes_blob(text), _calibration_blob(run_dir)):
        if not blob:
            continue
        if (
            CALIBRATION_MODE_OK_RE.search(blob)
            and CALIBRATION_PROFILE_OK_RE.search(blob)
            and CALIBRATION_FRICTION_RE.search(blob)
        ):
            return True
    return False
def _check_calibration_on_done(
    text: str, issues: list[Issue], *, run_dir: Path | None
) -> None:
    """Warn when Status=done lacks calibration evidence (stages.md)."""
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    if not status_m:
        return
    if _first_token(status_m.group(1)) != "done":
        return
    if _calibration_evidence(text, run_dir):
        return
    issues.append(
        Issue(
            "warn",
            "Status=done without calibration evidence — add Mode OK? / "
            "Review profile OK? / Biggest friction stage? Notes (≤3) and "
            "append _calibration.md (stages.md)",
        )
    )
def _check_clarity_check_logged(
    text: str, issues: list[Issue], *, before_build: bool
) -> None:
    """Error when clarity-check token missing / mismatched before boundaries.

    Soft stages: presence-any. High-risk (build/fix-*/merge): boundary-matched.
    """
    next_id = _card_next_stage_id(text)
    if before_build:
        target = "build"
    elif next_id in CLARITY_CHECK_STAGES:
        target = next_id
    else:
        return
    if _clarity_check_logged(text, stage_id=target):
        return
    if target in CLARITY_CHECK_HIGH_RISK:
        issues.append(
            Issue(
                "error",
                f"clarity-check ok — {target} missing from Notes/Run log "
                f"(boundary-matched required for high-risk Next) — do not launch "
                "(parent-next.md · invariants.md)",
            )
        )
    else:
        issues.append(
            Issue(
                "error",
                f"clarity-check ok — <boundary> missing from Notes/Run log "
                f"before `{target}` — do not launch "
                "(parent-next.md · invariants.md)",
            )
        )
def _check_design_review_clean_before_build(
    text: str,
    issues: list[Issue],
    *,
    before_build: bool,
    run_dir: Path | None,
) -> None:
    """Require 03a-design-review-log Result clean before Build (SKILL.md)."""
    enforce = before_build or _card_next_stage_id(text) == "build"
    if not enforce:
        return
    result = _design_review_result(run_dir)
    if result == "clean":
        return
    mode_m = REQUIRED_FIELD_PATTERNS["Mode"].search(text)
    mode = _first_token(mode_m.group(1)) if mode_m else None
    stage_name = (
        "design-verify-phase" if mode == "simple" else "design-review"
    )
    detail = result or "missing"
    issues.append(
        Issue(
            "error",
            f"{stage_name} Result must be clean before Build "
            f"(03a-design-review-log.md Result is {detail}) — "
            "SKILL.md · stages.md",
        )
    )
def _check_task_count_budget(text: str, issues: list[Issue], mode_token: str | None) -> None:
    """M2: soft warn when Mode full Task count >= 20 and Status running."""
    if mode_token != "full":
        return
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    status = _first_token(status_m.group(1)) if status_m else ""
    if status != "running":
        return
    m = TASK_COUNT_RE.search(text)
    if not m or m.group(1) is None:
        return
    count = int(m.group(1))
    if count >= SOFT_TASK_CAP:
        issues.append(
            Issue(
                "warn",
                f"Task count {count} >= {SOFT_TASK_CAP} (Mode full soft cap) — "
                "Decision N: continue / reclassify / stop (invariants.md)",
            )
        )
def _check_main_thread_fallbacks(text: str, issues: list[Issue]) -> None:
    """Soft warn when main-thread fallbacks >= 3 and Status running."""
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    status = _first_token(status_m.group(1)) if status_m else ""
    if status != "running":
        return
    m = MAIN_THREAD_RE.search(text)
    if not m or m.group(1) is None:
        return
    count = int(m.group(1))
    if count >= SOFT_MAIN_THREAD_CAP:
        issues.append(
            Issue(
                "warn",
                f"main-thread fallbacks {count} >= {SOFT_MAIN_THREAD_CAP} — "
                "Decision N soft pause (invariants.md)",
            )
        )
def lint_run_md(
    text: str,
    *,
    before_design_review: bool,
    before_build: bool,
    check_skip_review: bool = False,
    before_merge: bool = False,
    before_code_review: bool = False,
    run_dir: Path | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    mode_token: str | None = None
    review_token: str | None = None

    for name, pat in REQUIRED_FIELD_PATTERNS.items():
        m = pat.search(text)
        if not m:
            issues.append(Issue("error", f"missing required field **{name}**"))
            continue
        raw = m.group(1).strip()
        if name == "Status":
            token = _exact_enum_token(raw, VALID_STATUS, "Status", issues)
            if token is None and not _looks_like_template(raw):
                t = _first_token(raw)
                if t in LEGACY_STATUS_HINTS:
                    if issues and "Status must be one of" in issues[-1].message:
                        issues[-1] = Issue(
                            "error",
                            f"Status {t!r} is a stage/bucket — use "
                            f"running|paused|stopped|done; put position on Orchestrator card Stage id",
                        )
        elif name == "Mode":
            mode_token = _exact_enum_token(raw, VALID_MODE, "Mode", issues)
        elif name == "Review profile":
            review_token = _exact_enum_token(
                raw, VALID_REVIEW_PROFILE, "Review profile", issues
            )
        elif name == "Gate B veto":
            _exact_enum_token(raw, VALID_GATE_B_VETO, "Gate B veto", issues)

    if HAS_API_LINE_RE.search(text):
        _check_yes_no_flag(text, HAS_API_LINE_RE, "Has API", issues)
    if HAS_DB_LINE_RE.search(text):
        _check_yes_no_flag(text, HAS_DB_LINE_RE, "Has DB", issues)

    if mode_token == "full" and review_token == "skip-review":
        issues.append(
            Issue(
                "error",
                "Mode full + Review profile skip-review is forbidden — "
                "use full/lite review or Mode simple",
            )
        )

    if mode_token == "simple" and review_token == "full":
        issues.append(
            Issue(
                "error",
                "Mode simple + Review profile full is forbidden — "
                "use lite/skip-review or Mode full",
            )
        )

    _check_hitl_gate_b_mode(text, issues, mode_token)
    _check_gate_b_approved(text, issues, before_build=before_build)
    _check_design_backloop_gate_b(text, issues, before_build=before_build)
    _check_gate_c_approved(text, issues, before_merge=before_merge)
    _check_waiver_provenance(text, issues)
    _check_stale_before_merge(
        text, issues, before_merge=before_merge, run_dir=run_dir
    )
    _check_gate_c_test_bar(
        text, issues, before_merge=before_merge, run_dir=run_dir
    )
    _check_skip_review_build_only_smoke(
        text, issues, before_merge=before_merge, run_dir=run_dir
    )
    _check_status_done_requires_merge(text, issues)
    _check_calibration_on_done(text, issues, run_dir=run_dir)
    _check_clarity_check_logged(text, issues, before_build=before_build)
    _check_design_review_clean_before_build(
        text, issues, before_build=before_build, run_dir=run_dir
    )
    _check_lens_plan_api_db(text, issues, before_code_review=before_code_review)

    cm = CARD_STAGE_RE.search(text)
    if cm:
        stage_raw = cm.group(1).strip()
        stage_id = re.split(r"[\s(]", stage_raw.strip())[0].strip("`*_")
        placeholders = {
            "",
            "(required",
            "e.g.",
            "required",
            "—",
            "-",
            "n/a",
            "handoffs.md",
        }
        if stage_id.lower() not in placeholders and stage_id not in VALID_STAGE_IDS:
            issues.append(
                Issue("warn", f"Orchestrator card Stage id {stage_id!r} not in known stage ids")
            )

    if before_design_review:
        if not HAS_API_LINE_RE.search(text):
            issues.append(Issue("error", "Has API must be yes|no before design-review"))
        if not HAS_DB_LINE_RE.search(text):
            issues.append(Issue("error", "Has DB must be yes|no before design-review"))

    _check_pending_parallel(
        text,
        issues,
        before_design_review=before_design_review,
        run_dir=run_dir,
        mode_token=mode_token,
    )
    _check_isolated_api_db_files(
        text,
        issues,
        before_design_review=before_design_review,
        run_dir=run_dir,
        mode_token=mode_token,
    )
    _check_async_gate_b_gap(
        text, issues, before_build=before_build, run_dir=run_dir
    )
    _check_task_count_budget(text, issues, mode_token)
    _check_main_thread_fallbacks(text, issues)

    if before_build:
        vb = VERIFY_BLOCK_RE.search(text)
        if not vb:
            issues.append(Issue("error", "Verify commands block missing before Build"))
        else:
            block = vb.group(0)
            for key in ("cwd:", "build:", "unit:", "e2e:"):
                if key not in block.lower() and f"**{key}**" not in block.lower():
                    if f"**{key.rstrip(':')}:**" not in block and key not in block:
                        issues.append(Issue("warn", f"Verify commands may be missing {key}"))
            if re.search(r"\*\*build:\*\*\s*$", block, re.M) or (
                "**build:**" in block
                and re.search(r"\*\*build:\*\*\s*(\n|<)", block)
            ):
                issues.append(Issue("warn", "Verify commands build line looks empty"))

        vm = REQUIRED_FIELD_PATTERNS["Gate B veto"].search(text)
        if vm and not _looks_like_template(vm.group(1)):
            veto = _first_token(vm.group(1))
            if veto == "pending":
                issues.append(Issue("error", "Gate B veto is pending — do not Build"))

    # M1: always ban skip-review + Has API/DB on default lint (and explicit flags)
    if (
        before_build
        or before_design_review
        or check_skip_review
        or review_token == "skip-review"
    ):
        _check_skip_review_api_db(text, issues)

    metrics_present = bool(
        re.search(r"(?i)Run metrics", text)
        or TASK_COUNT_RE.search(text)
        or VERIFY_FAIL_RE.search(text)
        or MAIN_THREAD_RE.search(text)
    )
    if metrics_present:
        for label, pat in (
            ("Task count", TASK_COUNT_RE),
            ("verify-fail count", VERIFY_FAIL_RE),
            ("main-thread fallbacks", MAIN_THREAD_RE),
        ):
            m = pat.search(text)
            if not m:
                issues.append(Issue("warn", f"required metric missing: {label}"))
            elif m.group(1) is None:
                issues.append(Issue("warn", f"required metric empty: {label}"))

    if re.search(r"(?i)\*\*Complexity:\*\*", text) is None and re.search(
        r"(?i)## Required", text
    ):
        issues.append(Issue("warn", "Complexity one-line reason missing under Required"))

    return issues


def print_next_hint(run_dir: Path, *, derive: bool = False) -> int:
    """Read 00-run.md card; print next stage + companion + handoff hint."""
    run_md = run_dir / "00-run.md"
    if not run_md.is_file():
        print(f"error: missing {run_md}", file=sys.stderr)
        return 2
    text = run_md.read_text(encoding="utf-8")
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    status = _first_token(status_m.group(1)) if status_m else "?"
    mode_m = REQUIRED_FIELD_PATTERNS["Mode"].search(text)
    mode_token = _first_token(mode_m.group(1)) if mode_m else None
    rp_m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    review_token = _first_token(rp_m.group(1)) if rp_m else None
    next_m = CARD_NEXT_RE.search(text)
    stage_m = CARD_STAGE_RE.search(text)
    next_raw = next_m.group(1).strip() if next_m else ""
    stage_raw = stage_m.group(1).strip() if stage_m else ""
    stage_id = _extract_stage_token(next_raw) or _extract_stage_token(stage_raw)
    notes = _notes_blob(text)
    veto_window = bool(VETO_WINDOW_RE.search(notes))
    build_armed = bool(BUILD_ARMED_RE.search(notes + "\n" + _run_log_blob(text)))

    print(f"Status: {status}")
    print(f"Stage id (card): {stage_raw or '(empty)'}")
    print(f"Next step (card): {next_raw or '(empty)'}")

    derived: str | None = None
    if derive:
        derived = derive_expected_next(text, run_dir)
        print(f"derived next: {derived or '(indeterminate)'}")
        # H3: parallel hint when derived uses ||
        if derived and "||" in derived:
            parts = derived.split("||")
            print(
                "warn: derived next is parallel — launch "
                + " ∥ ".join(f"`{p}`" for p in parts)
                + " same parent turn (stages.md · lenses.md)"
            )
            if stage_id and stage_id not in parts:
                print(
                    f"warn: card Next `{stage_id}` differs from derived `{derived}` "
                    "— confirm or update card (parent-next.md · resume-abort.md)"
                )
        elif derived and stage_id and derived != stage_id:
            unsafe = _unsafe_card_derive_mismatch(
                stage_id, derived, text, run_dir
            )
            if unsafe and not _card_override_ok(text):
                print(
                    f"error: unsafe card vs derived — {unsafe} — "
                    "do-not-launch unless Notes `card-override — <reason>` "
                    "+ `provenance — card-override — user: \"…\"` "
                    "(+ optional Decision N) (stages.md · parent-next.md · R4/S7)"
                )
                print("companion: stages.md · parent-next.md")
                print("handoff: do-not-launch")
                print(
                    "next action: set card Next to derived, or Notes "
                    "`card-override — <reason>` + provenance card-override "
                    "then re-run --next --derive"
                )
                return 1
            if unsafe and _card_override_ok(text):
                print(
                    f"warn: card Next `{stage_id}` differs from derived "
                    f"`{derived}` — Notes card-override + provenance present "
                    "(R4/S7)"
                )
            else:
                print(
                    f"warn: card Next `{stage_id}` differs from derived "
                    f"`{derived}` — confirm or update card "
                    "(parent-next.md · resume-abort.md)"
                )

    # Terminal lifecycle: do not launch further pipeline Tasks
    if status in ("done", "stopped"):
        print("companion: stages.md · results.md (Done / abort)")
        print("handoff: do-not-launch")
        if status == "done":
            print(
                "next action: run finished — new work needs a new slug "
                "(or explicit Decision to re-open)"
            )
        else:
            print(
                "next action: run stopped — freeze stage; require Decision "
                "to resume or new slug"
            )
        return 1

    if not stage_id:
        print("hint: set Orchestrator card Next step / Stage id")
        if derived:
            print(f"hint: derived suggests `{derived}`")
        print(f"companion: {PARENT_NEXT_MD}")
        return 0
    print(f"next incomplete stage: {stage_id}")

    for msg in _next_stage_legality_warns(
        stage_id, mode_token, review_token, notes=notes
    ):
        print(f"warn: {msg}")

    # H4: Mode full + Next past Gate A while 01a ≠ ok → fail-closed (same as derive)
    if mode_token == "full" and stage_id in POST_GATE_A_STAGES:
        idea_ui = _parse_result_token(
            _read_artifact(run_dir, "01a-idea-ui-review.md")
        )
        if idea_ui != "ok":
            print(
                f"warn: Gate A fail-closed — 01a Result is "
                f"{idea_ui or 'missing'} (need ok) before `{stage_id}` "
                "(stages.md · results.md)"
            )
            print("companion: stages.md · parent-next.md (row for `gate-a`)")
            print("handoff: do-not-launch")
            print(
                "next action: set Next gate-a or ideation-update until "
                "01a Result ok, then re-run --next"
            )
            return 1

    # H2: unpaid Lens plan → do not launch test / gate-c / merge
    if stage_id in UNPAID_LENS_BLOCK_STAGES:
        unpaid = _unpaid_lens_stages(text, run_dir)
        entries = _lens_plan_entries(text)
        merge_needed = (
            len(entries) >= 2 and _merged_lenses_result(run_dir) != "clean"
        )
        review_stale = bool(REVIEW_STALE_RE.search(notes))
        test_stale = bool(TEST_STALE_RE.search(notes))
        implied_review = _implied_review_stale(text, run_dir)
        implied_test = _implied_test_stale(text, run_dir)
        if unpaid or merge_needed:
            reason = (
                f"unpaid lenses {unpaid}"
                if unpaid
                else "merge-findings not clean (2+ lenses)"
            )
            print(
                f"error: Lens plan unpaid — {reason}; do not advance to "
                f"`{stage_id}` (lenses.md)"
            )
            print("companion: lenses.md · parent-next.md")
            print("handoff: do-not-launch")
            print(
                "next action: launch unpaid lens-* "
                + ("∥ same turn; " if len(unpaid) >= 2 else "")
                + ("then merge-findings; " if len(entries) >= 2 else "")
                + "then re-run --next"
            )
            return 1
        if (review_stale or implied_review) and stage_id in ("gate-c", "merge"):
            if review_stale:
                print(
                    "warn: Notes review-stale — re-run review before "
                    f"`{stage_id}` (verify-and-fix.md)"
                )
            else:
                print(
                    "warn: 05-review-log clean older than Last verify-pass at — "
                    f"re-run review before `{stage_id}` "
                    "(verify-and-fix.md Stale)"
                )
            print("companion: verify-and-fix.md · lenses.md")
            print("handoff: do-not-launch")
            print(
                "next action: clear review-stale after review clean; re-run --next"
            )
            return 1
        if (test_stale or implied_test) and stage_id in ("gate-c", "merge"):
            if test_stale:
                print(
                    "warn: Notes test-stale — re-run test before "
                    f"`{stage_id}` (verify-and-fix.md)"
                )
            else:
                print(
                    "warn: 06-test-log success older than Last verify-pass at — "
                    f"re-run test before `{stage_id}` "
                    "(verify-and-fix.md Stale)"
                )
            print("companion: verify-and-fix.md · hitl.md")
            print("handoff: do-not-launch")
            print(
                "next action: clear test-stale after test success; re-run --next"
            )
            return 1

    # Design-backloop: redirect Build only — gate-b after re-review is settle path
    # (token stays until settle; do not redirect Next=gate-b → design-update)
    if DESIGN_BACKLOOP_RE.search(notes) and stage_id == "build":
        print(
            "warn: Notes design-backloop — do not Build; Next design-update "
            "until re-review, then gate-b settle (stages.md)"
        )
        print("companion: stages.md · parent-next.md (row for `design-update`)")
        print("handoff: do-not-launch")
        print(
            "next action: set Next design-update (or gate-b after re-review); "
            "clear design-backloop only after fresh Gate B settle"
        )
        return 1

    # Clarity-check: soft presence-any; hard boundary-matched for high-risk
    if stage_id in CLARITY_CHECK_STAGES and not _clarity_check_logged(
        text, stage_id=stage_id
    ):
        if stage_id in CLARITY_CHECK_HIGH_RISK:
            print(
                f"error: clarity-check ok — {stage_id} missing "
                "(boundary-matched required) (parent-next.md · invariants.md)"
            )
        else:
            print(
                f"error: clarity-check ok — <boundary> missing before `{stage_id}` "
                "(parent-next.md · invariants.md)"
            )
        print("companion: parent-next.md · invariants.md")
        print("handoff: do-not-launch")
        print(
            "next action: run clarity-check; log `clarity-check ok — "
            f"{stage_id}` on Notes/Run log; then re-run --next"
        )
        return 1

    # M2: design-review / design-verify-phase must be clean before Build
    if stage_id == "build":
        design_token = _design_review_result(run_dir)
        if design_token != "clean":
            stage_name = (
                "design-verify-phase"
                if mode_token == "simple"
                else "design-review"
            )
            detail = design_token or "missing"
            print(
                f"error: {stage_name} Result must be clean before Build "
                f"(03a-design-review-log.md Result is {detail}) — "
                "SKILL.md · stages.md"
            )
            print("companion: stages.md · parent-next.md · SKILL.md")
            print("handoff: do-not-launch")
            print(
                f"next action: finish {stage_name} to Result clean "
                "(or design-update), then re-run --next"
            )
            return 1

    # Parent gates / blocked async gap: never emit Task handoff (S1/S2)
    if stage_id == "build":
        hitl_tier = _parse_hitl_gate_b(text)
        async_path = veto_window or hitl_tier == "async-notify"
        if async_path and (veto_window or build_armed):
            gap_ok = _async_turn_gap_ok(text, run_dir)
            if veto_window and not build_armed:
                digest_ts = _async_gap_pending_digest_ts(text)
                if digest_ts:
                    _write_async_gap_sidecar(run_dir, digest_ts)
                    print(f"async-gap-pending — {digest_ts}")
                print(
                    "blocked: veto window open — copy async-gap-pending into "
                    "Notes, end turn, then set Build armed with later HH:MM "
                    "(hitl.md)"
                )
                print("companion: hitl.md · parent-next.md")
                print("handoff: do-not-launch")
                print(
                    "next action: Notes `async-gap-pending — <digest-ts>` "
                    "+ Run log Build armed (later HH:MM); re-run --next"
                )
                return 1
            if build_armed and not gap_ok:
                digest_ts = _async_gap_pending_digest_ts(text)
                if digest_ts:
                    _write_async_gap_sidecar(run_dir, digest_ts)
                    print(f"async-gap-pending — {digest_ts}")
                print(
                    "blocked: async Gate B gap incomplete — need arm HH:MM "
                    "strictly later than digest + Notes async-gap-pending "
                    "matching digest (+ `.lint-async-gap` from prior --next) "
                    "(hitl.md)"
                )
                print("companion: hitl.md · parent-next.md")
                print("handoff: do-not-launch")
                print(
                    "next action: fix two-timestamp gap + pending token; "
                    "re-run --next"
                )
                return 1
        if hitl_tier == "blocking" and not _gate_b_approved_ok(text):
            print("companion: hitl.md · parent-next.md (row for `build`)")
            print("handoff: do-not-launch")
            print(
                "next action: blocking Gate B — set Gate B approved "
                "yes (or named pick) + provenance, then re-run --next"
            )
            return 1
        if hitl_tier == "blocking" and _gate_b_approved_ok(text) and not _has_provenance(
            text, "gate-b-approved"
        ):
            print(
                "error: Gate B approved without provenance "
                '(need `provenance — gate-b-approved — user: "…"`) (hitl.md)'
            )
            print("companion: hitl.md · parent-next.md")
            print("handoff: do-not-launch")
            print(
                "next action: add provenance quoting the user Gate B yes; "
                "re-run --next"
            )
            return 1
    if stage_id in ("gate-b", "gate-c"):
        print(f"companion: hitl.md · parent-next.md (row for `{stage_id}`)")
        print("handoff: do-not-launch")
        if stage_id == "gate-b":
            if DESIGN_BACKLOOP_RE.search(notes):
                print(
                    "next action: Gate B digest + settle while design-backloop "
                    "present — clear Notes token on settle (stages.md); "
                    "blocking → set approved; auto may leave approved none"
                )
            else:
                print("next action: Gate B digest + HITL (no Task) — hitl.md")
        else:
            print(
                "next action: Gate C blocking ask; set Gate C approved "
                "before merge — hitl.md"
            )
        return 1
    if stage_id == "merge":
        _gc_raw, gc_actions = _parse_gate_c_approved(text)
        if _gc_raw is None or _gc_raw == "none" or not gc_actions:
            print("companion: hitl.md · parent-next.md (row for `merge`)")
            print("handoff: do-not-launch")
            print(
                "next action: Gate C blocking ask; set Gate C approved "
                "(non-empty commit|push|pr|merge subset) + provenance, "
                "then re-run --next"
            )
            return 1
        if not _has_provenance(text, "gate-c-approved"):
            print(
                "error: Gate C approved without provenance "
                '(need `provenance — gate-c-approved — user: "…"`) (hitl.md)'
            )
            print("companion: hitl.md · parent-next.md")
            print("handoff: do-not-launch")
            print(
                "next action: add provenance quoting the user Gate C yes; "
                "re-run --next"
            )
            return 1
        bar_issues: list[Issue] = []
        _check_waiver_provenance(text, bar_issues)
        _check_gate_c_test_bar(
            text, bar_issues, before_merge=True, run_dir=run_dir
        )
        _check_skip_review_build_only_smoke(
            text, bar_issues, before_merge=True, run_dir=run_dir
        )
        bar_errors = [i for i in bar_issues if i.severity == "error"]
        if bar_errors:
            for i in bar_errors:
                print(f"error: {i.message}")
            print("companion: hitl.md · parent-next.md (row for `merge`)")
            print("handoff: do-not-launch")
            print(
                "next action: meet Gate C test bar (or Notes gate-c-test-override / "
                "smoke-waive / smoke-pass-rerun / docs-only each with provenance), "
                "then re-run --next"
            )
            return 1

    print(f"companion: parent-next.md (row for `{stage_id}`)")
    print(
        f"handoff: python3 {PACKAGE / 'scripts' / 'handoff-for.py'} {stage_id}"
    )
    return 0
def dry_run_seed(run_dir: Path, *, slug: str | None) -> int:
    """Create slug dir, seed 00-run.md from artifact template, lint, stop."""
    if slug:
        target = run_dir / slug if run_dir.name != slug else run_dir
    else:
        target = run_dir
    if not ARTIFACTS_00.is_file():
        print(f"error: missing template {ARTIFACTS_00}", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    dest = target / "00-run.md"
    if dest.exists():
        print(f"error: already exists {dest}", file=sys.stderr)
        return 2
    # Copy fenced template body if present; else whole file
    raw = ARTIFACTS_00.read_text(encoding="utf-8")
    m = re.search(r"```markdown\n(.*?)```", raw, re.S)
    body = m.group(1) if m else raw
    date = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d")
    feature = target.name if re.match(r"^\d{8}-", target.name) else f"{date}-dry-run"
    body = body.replace("<slug>", feature).replace("YYYYMMDD-feature-x", feature)
    dest.write_text(body, encoding="utf-8")
    print(f"seeded: {dest}")
    print("note: template enums may still fail lint until filled — expected for dry-run")
    text = dest.read_text(encoding="utf-8")
    issues = lint_run_md(
        text, before_design_review=False, before_build=False, run_dir=target
    )
    for i in issues:
        print(f"{i.severity}: {i.message}")
    if not issues:
        print("ok: 00-run.md lint clean")
    print("dry-run-seed: stop (no pipeline)")
    return 0
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "run_dir",
        type=Path,
        nargs="?",
        help="Path to .my-docs/workflow/<slug>/",
    )
    p.add_argument(
        "--before-design-review",
        action="store_true",
        help=(
            "Enforce Has API/DB yes|no + Mode full Pending parallel + "
            "isolated 03a-* when Has API/DB yes (not tiny) + skip-review ban"
        ),
    )
    p.add_argument(
        "--before-build",
        action="store_true",
        help=(
            "Enforce Verify commands + Gate B veto none + Build armed + async gap "
            "+ Gate B approved when HITL Gate B is blocking"
        ),
    )
    p.add_argument(
        "--before-merge",
        action="store_true",
        help=(
            "Require Gate C approved actions + Gate C test bar (hitl.md); "
            "also auto-enforced when card Next=merge; "
            "also runs --check-results (warn-only)"
        ),
    )
    p.add_argument(
        "--before-code-review",
        action="store_true",
        help=(
            "Require Lens plan api/db when Has API/DB yes "
            "(unless Notes tiny-contract-tweak / fold); "
            "also auto when card Next is adversarial or code-review-phase"
        ),
    )
    p.add_argument(
        "--check-skip-review",
        action="store_true",
        help=(
            "Error if skip-review + Has API/DB yes "
            "(also on default lint when profile is skip-review; "
            "and --before-build / --before-design-review)"
        ),
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )
    p.add_argument(
        "--next",
        action="store_true",
        help="Print next incomplete stage id + companion + handoff-for.py hint",
    )
    p.add_argument(
        "--derive",
        action="store_true",
        help="With --next: also derive expected next from Mode/profile + artifacts",
    )
    p.add_argument(
        "--dry-run-seed",
        action="store_true",
        help="Create run dir, seed 00-run.md from artifacts/00-run.md, lint, stop",
    )
    p.add_argument(
        "--check-stage-ids",
        action="store_true",
        help="Check stage-id registry alignment (handoffs / parent-next / VALID_STAGE_IDS / stages/*.md); run_dir optional",
    )
    p.add_argument(
        "--check-results",
        action="store_true",
        help="Scan artifact Result headers + soft-warn oversize bodies (size-caps.md)",
    )
    p.add_argument(
        "--slug",
        default=None,
        help="With --dry-run-seed: slug under run_dir (default: run_dir itself)",
    )
    args = p.parse_args()

    if args.check_stage_ids:
        issues = check_stage_id_registry()
        for i in issues:
            print(f"{i.severity}: {i.message}")
        if not issues:
            print("ok: stage-id registry aligned")
        return 1 if issues else 0

    if args.run_dir is None:
        p.error("run_dir is required")

    if args.dry_run_seed:
        return dry_run_seed(args.run_dir, slug=args.slug)

    if args.derive and not args.next:
        p.error("--derive requires --next")

    if args.next:
        return print_next_hint(args.run_dir, derive=args.derive)

    if args.check_results:
        issues = check_results(args.run_dir)
        for i in issues:
            print(f"{i.severity}: {i.message}")
        if not issues:
            print("ok: Result headers + size caps soft-check clean")
        return 1 if (args.strict and issues) else 0

    run_md = args.run_dir / "00-run.md"
    if not run_md.is_file():
        print(f"error: missing {run_md}", file=sys.stderr)
        return 2

    text = run_md.read_text(encoding="utf-8")
    before_merge = args.before_merge or _card_next_stage_id(text) == "merge"
    issues = lint_run_md(
        text,
        before_design_review=args.before_design_review,
        before_build=args.before_build,
        check_skip_review=args.check_skip_review,
        before_merge=before_merge,
        before_code_review=args.before_code_review,
        run_dir=args.run_dir,
    )

    # N9: --check-results (warn-only) with --before-merge / Next=merge
    if before_merge:
        issues.extend(check_results(args.run_dir))

    errors = [i for i in issues if i.severity == "error"]
    warns = [i for i in issues if i.severity == "warn"]

    for i in issues:
        print(f"{i.severity}: {i.message}")

    if not issues:
        print("ok: 00-run.md lint clean")

    if errors or (args.strict and warns):
        return 1
    return 0
