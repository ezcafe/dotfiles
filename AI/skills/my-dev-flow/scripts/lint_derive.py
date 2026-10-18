"""Next-stage derivation for my-dev-flow lint.

Enforces stages.md Happy path + lenses.md derive / unpaid lenses / parent-next.md --next --derive.
"""
from __future__ import annotations

import re
from pathlib import Path

from lint_common import (
    CODE_REVIEW_ENTRY_STAGES,
    DESIGN_BACKLOOP_RE,
    FULL_ONLY_STAGES,
    GRILL_SKIP_RE,
    HAS_API_LINE_RE,
    HAS_DB_LINE_RE,
    Issue,
    LENS_PLAN_MAP,
    LENS_PLAN_RE,
    PROFILE_FULL_ONLY_STAGES,
    PROFILE_LITE_PATH_STAGES,
    REQUIRED_FIELD_PATTERNS,
    RESULT_HEADER_RE,
    RESULT_TOKENS_BY_ARTIFACT,
    REVIEW_STALE_RE,
    SIMPLE_BUNDLE_STAGES,
    SIZE_CAP_LINES,
    SIZE_CAPS_MD,
    SKIP_REVIEW_FORBIDDEN_STAGES,
    SMOKE_RERUN_RE,
    TDD_04A_SKIP_RE,
    TEST_STALE_RE,
    TINY_TWEAK_RE,
    VALID_MODE,
    VALID_REVIEW_PROFILE,
    _artifact_exists,
    _card_next_stage_id,
    _first_token,
    _last_stage_id,
    _notes_blob,
    _parse_lens_plan_tokens,
    _parse_result_token,
    _parsed_yes_no,
    _read_artifact,
)
from lint_gate_b import (
    _gate_b_approved_ok,
    _parse_hitl_gate_b,
)
from lint_gate_c import (
    _implied_review_stale,
    _implied_test_stale,
    _last_verify_pass,
    _review_profile,
    _smoke_pass,
    _test_log_success,
)

def _tdd_04a_settled(text: str, run_dir: Path | None) -> bool:
    """True when 04a artifact exists or Notes say ``04a skipped``."""
    if _artifact_exists(run_dir, "04a-tdd-test-review.md"):
        return True
    return bool(TDD_04A_SKIP_RE.search(_notes_blob(text)))
def _review_clean(run_dir: Path | None, review: str | None = None) -> bool:
    """True when 05-review-log shows review complete for the profile.

    Review profile **full**: Adv + Quality section Results both ``clean``
    (fail closed if either section Result is missing or not clean). Do not
    trust the first file-level ``**Result:**`` alone — Adv often writes
    ``clean`` before Quality runs.

    Review profile **lite** (default): overall / code-review-phase Result
    ``clean``; when both Adv and Quality section Results are present,
    require both ``clean`` instead.
    """
    blob = _read_artifact(run_dir, "05-review-log.md")
    if not blob:
        return False
    adv = _section_result(blob, r"Adversarial")
    qual = _section_result(blob, r"Quality")
    if review == "full":
        return adv == "clean" and qual == "clean"
    if adv is not None and qual is not None:
        return adv == "clean" and qual == "clean"
    return _parse_result_token(blob) == "clean"
def _section_result(blob: str, heading_pat: str) -> str | None:
    """Primary Result token under a ## section matching heading_pat (until next ##)."""
    sec = re.search(
        rf"(?ims)^##[^\n]*{heading_pat}[^\n]*\n(.*?)(?=^## |\Z)",
        blob,
    )
    if not sec:
        return None
    return _parse_result_token(sec.group(1))
def _merged_lenses_result(run_dir: Path | None) -> str | None:
    blob = _read_artifact(run_dir, "05-review-log.md")
    if not blob:
        return None
    return _section_result(blob, r"Merged lenses")
def _adv_vs_quality_reentry(run_dir: Path | None, last_id: str) -> str:
    """H6: needs fix after Adv → adversarial/fix-review; after Quality → quality."""
    blob = _read_artifact(run_dir, "05-review-log.md")
    if not blob:
        return "adversarial"
    adv = _section_result(blob, r"Adversarial")
    qual = _section_result(blob, r"Quality")

    if last_id == "fix-review":
        if qual == "needs fix":
            return "quality"
        return "adversarial"

    if last_id == "adversarial":
        if adv == "needs fix":
            return "fix-review"
        if adv == "clean":
            return "quality"
        return "adversarial"

    if last_id == "quality":
        if qual == "needs fix":
            return "fix-review"
        if qual == "clean":
            return "quality"  # overall may still need lenses
        return "quality"

    # Section-based (no useful Last stage)
    if adv == "needs fix":
        return "adversarial"
    if adv != "clean":
        return "adversarial"
    if qual == "needs fix" or qual != "clean":
        return "quality"
    return "quality"
def _lens_plan_entries(text: str) -> list[tuple[str, str, str]]:
    """Return [(token, stage_id, artifact), ...] for Lens plan (skip none/unknown)."""
    out: list[tuple[str, str, str]] = []
    for tok in sorted(_parse_lens_plan_tokens(text)):
        mapped = LENS_PLAN_MAP.get(tok)
        if mapped:
            stage_id, artifact = mapped
            out.append((tok, stage_id, artifact))
    return out
def _lens_artifact_clean(run_dir: Path | None, name: str) -> bool:
    blob = _read_artifact(run_dir, name)
    if not blob:
        return False
    return _parse_result_token(blob) == "clean"
def _unpaid_lens_stages(text: str, run_dir: Path | None) -> list[str]:
    """H2: Lens plan stages whose 05-lens-*.md is missing or not clean."""
    unpaid: list[str] = []
    for _tok, stage_id, artifact in _lens_plan_entries(text):
        if not _lens_artifact_clean(run_dir, artifact):
            unpaid.append(stage_id)
    return unpaid
def _lenses_complete(text: str, run_dir: Path | None) -> bool:
    """True when Lens plan is none, or all lens files clean (+ merge when 2+)."""
    entries = _lens_plan_entries(text)
    if not entries:
        return True
    if _unpaid_lens_stages(text, run_dir):
        return False
    if len(entries) >= 2:
        return _merged_lenses_result(run_dir) == "clean"
    return True
def _design_review_result(run_dir: Path | None) -> str | None:
    """Primary Result from 03a-design-review-log.md, or None if missing."""
    blob = _read_artifact(run_dir, "03a-design-review-log.md")
    if not blob:
        return None
    return _parse_result_token(blob)
def _design_review_clean(run_dir: Path | None, _mode: str | None = None) -> bool:
    return _design_review_result(run_dir) == "clean"
def _any_03a_needs_update(run_dir: Path | None) -> bool:
    """True when any present 03a* Result is needs update."""
    for name in (
        "03a-design-review-log.md",
        "03a-api-contract-review.md",
        "03a-db-design-review.md",
    ):
        blob = _read_artifact(run_dir, name)
        if blob and _parse_result_token(blob) == "needs update":
            return True
    return False
def _grill_done(text: str, run_dir: Path | None) -> bool:
    """True when Notes grill skipped or 02b Result is frontier-empty|skipped."""
    if GRILL_SKIP_RE.search(_notes_blob(text)):
        return True
    blob = _read_artifact(run_dir, "02b-grill.md")
    if not blob:
        return False
    return _parse_result_token(blob) in ("frontier-empty", "skipped")
def derive_expected_next(text: str, run_dir: Path | None) -> str | None:
    """Best-effort next stage from Mode/profile + artifacts (card is override).

    Returns None when indeterminate (e.g. mid Gate B settle).
    """
    status_m = REQUIRED_FIELD_PATTERNS["Status"].search(text)
    status = _first_token(status_m.group(1)) if status_m else ""
    if status in ("done", "stopped"):
        return None

    notes = _notes_blob(text)
    mode_m = REQUIRED_FIELD_PATTERNS["Mode"].search(text)
    mode = _first_token(mode_m.group(1)) if mode_m else None
    rp_m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    review = _first_token(rp_m.group(1)) if rp_m else None

    has_design = _artifact_exists(run_dir, "03-design.md")
    has_tasks = _artifact_exists(run_dir, "04-tasks.md")
    design_result = _design_review_result(run_dir)
    design_ok = design_result == "clean"
    verify_ok = _last_verify_pass(text)
    smoke_ok = _smoke_pass(run_dir)
    review_ok = _review_clean(run_dir, review)
    test_ok_full = _test_log_success(run_dir, expect_mode="full")
    test_ok_lite = _test_log_success(run_dir, expect_mode="lite")
    next_id = _card_next_stage_id(text)
    last_id = _last_stage_id(text)

    # N1: design-backloop — mirror --next (never force design-update over gate-b)
    if DESIGN_BACKLOOP_RE.search(notes):
        if next_id == "gate-b" or last_id == "gate-b":
            return "gate-b"
        if design_ok:
            return "gate-b"  # re-review clean → awaiting Gate B settle
        return "design-update"

    def _gate_b_or_build() -> str:
        tier = _parse_hitl_gate_b(text)
        if tier == "blocking" and not _gate_b_approved_ok(text):
            return "gate-b"
        return "build"

    def _after_verify_smoke_then_review() -> str | None:
        """N6: verify-pass without smoke-pass → smoke (or build under skip-review).

        H2: unpaid Lens plan before test/gate-c.
        H5: Notes review-stale / test-stale invalidate prior clean/success.
        E2: unpaid clean/success vs Last verify-pass at (same as Notes stale).
        H6: Adv vs Quality re-entry from sections / Last stage.
        """
        review_stale = bool(REVIEW_STALE_RE.search(notes)) or _implied_review_stale(
            text, run_dir
        )
        test_stale = bool(TEST_STALE_RE.search(notes)) or _implied_test_stale(
            text, run_dir
        )
        if not smoke_ok:
            if review == "skip-review":
                return "build"  # ordered recovery prefers re-Build
            return "smoke"
        if review == "skip-review":
            return "gate-c"
        effective_review_ok = review_ok and not review_stale
        if not effective_review_ok:
            if review == "lite":
                return "code-review-phase"
            if not _artifact_exists(run_dir, "05-review-log.md"):
                return "adversarial"
            return _adv_vs_quality_reentry(run_dir, last_id)
        # H2: Lens plan unpaid → matching lens-* (parallel hint when 2+ unpaid)
        unpaid = _unpaid_lens_stages(text, run_dir)
        if unpaid:
            if len(unpaid) >= 2:
                return "||".join(unpaid)
            return unpaid[0]
        entries = _lens_plan_entries(text)
        if len(entries) >= 2 and _merged_lenses_result(run_dir) != "clean":
            return "merge-findings"
        if review == "lite":
            if test_stale or not test_ok_lite:
                return "test-lite"
            return "gate-c"
        # profile full
        if test_stale or not test_ok_full:
            return "test-full"
        return "gate-c"

    if mode == "simple":
        if not (has_design and has_tasks):
            return "design-phase"
        # N3: needs update → design-update; missing → first review stage
        if _any_03a_needs_update(run_dir) or design_result == "needs update":
            return "design-update"
        if design_result is None:
            return "design-verify-phase"
        if not design_ok:
            return "design-verify-phase"
        # M1: optional 04a after design clean, before Gate B / Build
        if not verify_ok:
            if not _tdd_04a_settled(text, run_dir):
                return "tdd-review"
            return _gate_b_or_build()
        return _after_verify_smoke_then_review()

    if mode == "full":
        # N2: walk Gate A → skim → Analyze → Grill → Design (artifact presence)
        if not _artifact_exists(run_dir, "01-idea.md"):
            return "ideation"
        if not _artifact_exists(run_dir, "01a-idea-ui-review.md"):
            return "gate-a"
        idea_ui = _parse_result_token(
            _read_artifact(run_dir, "01a-idea-ui-review.md")
        )
        if idea_ui == "needs update":
            return "ideation-update"
        # Fail closed: advance to skim only on exact ok; escalate / pending /
        # missing / other → hold gate-a (results.md)
        if idea_ui != "ok":
            return "gate-a"
        if not _artifact_exists(run_dir, "02-skim.md"):
            return "skim"
        if not _artifact_exists(run_dir, "02-analysis.md"):
            return "analyze"
        if not _grill_done(text, run_dir):
            return "grill"
        if not has_design:
            return "design"
        # N3
        if _any_03a_needs_update(run_dir) or design_result == "needs update":
            return "design-update"
        # H1/H3: isolated API/DB before general design-review (even if Pending parallel none)
        tiny = bool(TINY_TWEAK_RE.search(notes))
        has_api = _parsed_yes_no(text, HAS_API_LINE_RE)
        has_db = _parsed_yes_no(text, HAS_DB_LINE_RE)
        api_done = _artifact_exists(run_dir, "03a-api-contract-review.md")
        db_done = _artifact_exists(run_dir, "03a-db-design-review.md")
        needs_api = has_api == "yes" and not tiny
        needs_db = has_db == "yes" and not tiny
        if needs_api and needs_db:
            # H3: both missing → parallel hint; one exists → serialize resume
            if not api_done and not db_done:
                return "api-contract-review||db-design-review"
            if not api_done:
                return "api-contract-review"
            if not db_done:
                return "db-design-review"
        elif needs_api and not api_done:
            return "api-contract-review"
        elif needs_db and not db_done:
            return "db-design-review"
        if design_result is None:
            return "design-review"
        if not design_ok:
            return "design-review"
        # M1: optional 04a after design clean, before Gate B / Build
        if not verify_ok:
            if not _tdd_04a_settled(text, run_dir):
                return "tdd-review"
            return _gate_b_or_build()
        return _after_verify_smoke_then_review()

    return None
def check_results(run_dir: Path) -> list[Issue]:
    """Scan known artifact Result headers; soft-warn oversize bodies."""
    issues: list[Issue] = []
    for name, allowed in RESULT_TOKENS_BY_ARTIFACT.items():
        path = run_dir / name
        if not path.is_file():
            continue
        blob = path.read_text(encoding="utf-8")
        token = _parse_result_token(blob)
        if token is None:
            if "Result:" in blob or "**Result:**" in blob:
                issues.append(
                    Issue(
                        "warn",
                        f"{name}: Result header present but token empty/template "
                        f"(results.md)",
                    )
                )
            continue
        allowed_l = {a.lower() for a in allowed}
        if token not in allowed_l:
            issues.append(
                Issue(
                    "warn",
                    f"{name}: Result {token!r} not in {sorted(allowed)} "
                    f"(results.md)",
                )
            )

    for name, cap in SIZE_CAP_LINES.items():
        path = run_dir / name
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        # Skip leading comment / copy-from template lines lightly
        body_lines = [ln for ln in lines if ln.strip()]
        if len(body_lines) > cap:
            issues.append(
                Issue(
                    "warn",
                    f"{name}: ~{len(body_lines)} non-empty lines > soft cap "
                    f"~{cap} (size-caps.md)",
                )
            )
    return issues
def _next_stage_legality_warns(
    stage_id: str,
    mode_token: str | None,
    review_token: str | None,
    notes: str = "",
) -> list[str]:
    """Warn messages when Next stage is illegal for Mode × Review profile."""
    warns: list[str] = []
    if not stage_id:
        return warns
    if mode_token == "full" and review_token == "skip-review":
        warns.append(
            "Mode full + Review profile skip-review is forbidden — "
            "use full/lite or Mode simple (stages.md)"
        )
    if mode_token == "simple" and review_token == "full":
        warns.append(
            "Mode simple + Review profile full is forbidden — "
            "use lite/skip-review or Mode full (stages.md)"
        )
    if mode_token == "simple" and stage_id in FULL_ONLY_STAGES:
        warns.append(
            f"Next `{stage_id}` is Mode full Happy-path only — "
            "reclassify or pick a simple-pipeline stage (stages.md)"
        )
    if mode_token == "full" and stage_id in SIMPLE_BUNDLE_STAGES:
        warns.append(
            f"Next `{stage_id}` is Mode simple bundle — "
            "Mode full uses Analyze→Grill→Design / design-review (stages.md)"
        )
    if review_token == "lite" and stage_id in PROFILE_FULL_ONLY_STAGES:
        warns.append(
            f"Next `{stage_id}` requires Review profile full — "
            "lite path uses code-review-phase / test-lite (stages.md)"
        )
    if review_token == "full" and stage_id in PROFILE_LITE_PATH_STAGES:
        warns.append(
            f"Next `{stage_id}` is Review profile lite path — "
            "profile full uses Adv→Quality→test-full (stages.md)"
        )
    if review_token == "skip-review" and stage_id in SKIP_REVIEW_FORBIDDEN_STAGES:
        # M3: smoke allowed once when Notes say smoke re-run; else prefer re-Build
        if stage_id == "smoke" and SMOKE_RERUN_RE.search(notes or ""):
            return warns
        if stage_id == "smoke":
            warns.append(
                "Next `smoke` illegal under skip-review without Notes "
                "`smoke re-run` — prefer re-Build to rewrite Smoke, or Notes "
                "`smoke re-run` once, or drop skip-review → lite "
                "(verify-and-fix.md)"
            )
        else:
            warns.append(
                f"Next `{stage_id}` illegal under skip-review — "
                "legal path is Gate C after Build verify-pass (lenses.md · hitl.md)"
            )
    return warns
