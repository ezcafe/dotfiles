#!/usr/bin/env python3
"""Lint a my-dev-flow run folder (.my-docs/workflow/<slug>/).

Checks required 00-run.md fields with exact-token enums (reject template `|`),
Status, Mode, Review profile, Gate B veto, Gate B approved, Pending parallel,
Has API/DB, stage ids, Verify commands before Build, skip-review+API/DB error
(always on default lint when profile is skip-review; also --before-build /
--before-design-review / --check-skip-review),
Mode full isolated 03a-* when Has API/DB yes not tiny (--before-design-review),
Mode full+skip-review error, Mode simple+full error, Mode full + HITL Gate B
auto/async-notify error, Mode simple + Has API/DB yes + soft Gate B error,
Mode full API∥DB Pending parallel (simple keeps none),
async Gate B gap + Build armed, Gate B approved when HITL Gate B is blocking
(--before-build / --next), Notes design-backloop → error until cleared after
fresh Gate B settle (blocks Build even when Gate B soft / approved none),
Gate C approved before merge (auto when card Next=merge, or with --before-merge),
Gate C test bar from hitl.md (full/lite success + Mode last run matching
profile; skip-review verify+smoke; Notes gate-c-test-override waives;
Mode last run missing → fail closed),
Notes review-stale / test-stale → error on --before-merge / Next=merge
(same Gate C bar; --next keeps do-not-launch),
unpaid 05 clean / 06 success vs Last verify-pass at (mtime older than
clock, no matching Notes stale token) → same merge / --next / --derive
blocks (verify-and-fix.md Stale; missing clock → Notes-only),
skip-review + only Build-writes-Smoke → warn on --before-merge unless
Notes smoke-waive / smoke-pass (re-run) / gate-c-test-override,
Notes design-backloop → error only --before-build / Next=build; else warn
recovery when Next is design-update / re-review / gate-b / …,
Lens plan api/db before code review (--before-code-review or Next in
adversarial / code-review-phase),
design-review / design-verify-phase 03a Result clean before Build
(--before-build / Next=build / --next do-not-launch),
--next --derive returns tdd-review after design clean until 04a exists or
Notes ``04a skipped``,
Status=done warn without calibration evidence (Mode OK? / profile OK? /
friction or ``_calibration.md``),
clarity-check ok — <boundary> soft-warn before design-phase / build /
related Next targets.

Also:
  --next              print next incomplete stage hint + companion / handoff
                      (no Task handoff when Status done|stopped / blocked /
                      gate-b / gate-c / Build without Gate B approved when
                      blocking / Build without 03a clean / merge without
                      Gate C approved / Gate C bar fail / review-stale|test-stale)
  --next --derive     also compute expected next from Mode/profile + artifacts;
                      warn when card Next differs (card remains launch override);
                      optional 04a gate after design clean
  Status=done         error unless merge ∈ Gate C approved; warn if no
                      calibration evidence
  --before-merge      require Gate C approved + Gate C test bar + stale-token
                      errors (also auto when Next=merge); also runs
                      --check-results (warn-only); skip-review Build-only
                      smoke → warn
  --before-code-review  require Lens plan api/db when Has API/DB yes (not tiny/fold)
  --check-results     scan artifact Result headers + soft warn oversize bodies
  --dry-run-seed      create slug dir, seed 00-run.md from template, lint, stop
  --check-stage-ids   verify stage-id registry (handoffs / parent-next / VALID_STAGE_IDS / stages/*.md)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
SKILLS_ROOT = PACKAGE.parent
HANDOFFS_MD = PACKAGE / "handoffs.md"
SIZE_CAPS_MD = PACKAGE / "size-caps.md"
ARTIFACTS_00 = PACKAGE / "artifacts" / "00-run.md"
PARENT_NEXT_MD = PACKAGE / "parent-next.md"
RESULTS_MD = PACKAGE / "results.md"
SUBFLOW_DIRS = (
    SKILLS_ROOT / "my-dev-flow-design",
    SKILLS_ROOT / "my-dev-flow-design-review",
    SKILLS_ROOT / "my-dev-flow-code",
    SKILLS_ROOT / "my-dev-flow-review",
    SKILLS_ROOT / "my-dev-flow-test",
    SKILLS_ROOT / "my-dev-flow-merge",
)
SOFT_MAIN_THREAD_CAP = 3

VALID_STATUS = frozenset({"running", "paused", "stopped", "done"})
VALID_MODE = frozenset({"simple", "full"})
VALID_REVIEW_PROFILE = frozenset({"full", "lite", "skip-review"})
VALID_GATE_B_VETO = frozenset({"none", "pending"})
VALID_YES_NO = frozenset({"yes", "no"})
VALID_HITL_TIER = frozenset({"auto", "async-notify", "blocking"})
VALID_GATE_C_ACTIONS = frozenset({"commit", "push", "pr", "merge"})
# Exact enum for Pending parallel (H4)
VALID_PENDING_PARALLEL = frozenset({"none", "api", "db", "api|db"})

# Mode × profile Happy-path legality for --next (warn only)
# grill + Analyze→Design peers are Mode full standalone (simple uses design-phase)
FULL_ONLY_STAGES = frozenset(
    {
        "ideation",
        "gate-a",
        "ideation-update",
        "skim",
        "analyze",
        "grill",
        "design",
        "design-review",
        "api-contract-review",
        "db-design-review",
        "adversarial",
        "quality",
        "test-full",
    }
)
CODE_REVIEW_ENTRY_STAGES = frozenset({"adversarial", "code-review-phase"})
SIMPLE_BUNDLE_STAGES = frozenset({"design-phase", "design-verify-phase"})
PROFILE_FULL_ONLY_STAGES = frozenset({"adversarial", "quality", "test-full"})
PROFILE_LITE_PATH_STAGES = frozenset({"code-review-phase", "test-lite"})
SKIP_REVIEW_FORBIDDEN_STAGES = frozenset(
    {
        "adversarial",
        "quality",
        "code-review-phase",
        "test-full",
        "test-lite",
        "merge-findings",
        "fix-review",
        "lens-security",
        "lens-perf",
        "lens-memory",
        "lens-api",
        "lens-db",
        "smoke",
    }
)

# Stage ids from handoffs.md Task description map
VALID_STAGE_IDS = frozenset(
    {
        "ideation",
        "gate-a",
        "ideation-update",
        "skim",
        "analyze",
        "grill",
        "design",
        "design-phase",
        "design-review",
        "api-contract-review",
        "db-design-review",
        "design-verify-phase",
        "design-update",
        "tdd-review",
        "build",
        "smoke",
        "adversarial",
        "quality",
        "code-review-phase",
        "lens-security",
        "lens-perf",
        "lens-memory",
        "lens-api",
        "lens-db",
        "merge-findings",
        "fix-review",
        "test-full",
        "test-lite",
        "fix-tests",
        "merge",
        "gate-b",
        "gate-c",
    }
)

LEGACY_STATUS_HINTS = frozenset(
    {
        "ideation",
        "gate-a",
        "skim",
        "analyze",
        "grill",
        "design",
        "design-phase",
        "design-review",
        "design-verify-phase",
        "tdd-review",
        "gate-b",
        "build",
        "smoke",
        "code-review-phase",
        "review",
        "test-full",
        "test-lite",
        "test",
        "gate-c",
    }
)

REQUIRED_FIELD_PATTERNS = {
    "Status": re.compile(r"^\*\*Status:\*\*\s*(.+)$", re.M),
    "Mode": re.compile(r"^\*\*Mode:\*\*\s*(.+)$", re.M),
    "Review profile": re.compile(r"^\*\*Review profile:\*\*\s*(.+)$", re.M),
    "Gate B veto": re.compile(r"^\*\*Gate B veto:\*\*\s*(.+)$", re.M),
    "Last Verify": re.compile(r"^\*\*Last Verify:\*\*\s*(.+)$", re.M),
}

PENDING_PARALLEL_RE = re.compile(
    r"^\*\*Pending parallel:\*\*\s*(.+)$", re.M | re.I
)
HAS_API_LINE_RE = re.compile(r"^[-*]?\s*\*\*Has API:\*\*\s*(.+)$", re.M | re.I)
HAS_DB_LINE_RE = re.compile(r"^[-*]?\s*\*\*Has DB:\*\*\s*(.+)$", re.M | re.I)
HITL_GATE_B_RE = re.compile(r"^[-*]?\s*\*\*HITL Gate B:\*\*\s*(.+)$", re.M | re.I)
GATE_B_APPROVED_RE = re.compile(
    r"^[-*]?\s*\*\*Gate B approved:\*\*\s*(.+)$", re.M | re.I
)
GATE_C_APPROVED_RE = re.compile(
    r"^[-*]?\s*\*\*Gate C approved:\*\*\s*(.+)$", re.M | re.I
)
LENS_PLAN_RE = re.compile(r"^\*\*Lens plan:\*\*\s*(.+)$", re.M | re.I)
SMOKE_RERUN_RE = re.compile(r"(?i)\bsmoke\s+re-?run\b")
# Explicit Notes waive of independent Smoke preference (skip-review merge)
SMOKE_WAIVE_RE = re.compile(
    r"(?i)\bsmoke\s*-?\s*waive\b|\bwaive\s+(?:independent\s+)?smoke\b"
)
# Evidence independent Smoke Task re-run completed (not Build-writes-Smoke only)
SMOKE_RERUN_DONE_RE = re.compile(
    r"(?i)smoke-pass\s*\(\s*re-?run\s*\)|"
    r"smoke\s+re-?run\s+(?:done|pass|ok|complete)|"
    r"independent\s+smoke\s+(?:pass|ok|done)"
)
FOLD_API_DB_RE = re.compile(
    r"(?i)(?:fold|folded).{0,40}(?:api|db|contract)|"
    r"(?:api|db|contract).{0,40}(?:fold|folded).{0,40}"
    r"(?:quality|code-review-phase|lite)"
)
NOTES_SECTION_RE = re.compile(
    r"### Notes\s*\n(.*?)(?=\n### |\n## |\Z)", re.M | re.S
)
RUN_LOG_SECTION_RE = re.compile(
    r"### Run log\s*\n(.*?)(?=\n### |\n## |\Z)", re.M | re.S
)
CARD_NEXT_RE = re.compile(
    r"\|\s*Next step\s*\|\s*([^|\n]+)\s*\|", re.M | re.I
)
VERIFY_BLOCK_RE = re.compile(
    r"\*\*Verify commands:\*\*.*?(?=^\*\*[A-Z]|\n## |\Z)", re.M | re.S
)
CARD_STAGE_RE = re.compile(
    r"\|\s*Stage id\s*\|\s*([^|\n]+)\s*\|", re.M | re.I
)
TASK_COUNT_RE = re.compile(r"(?i)Task count:\s*(\d+)?")
VERIFY_FAIL_RE = re.compile(r"(?i)verify-fail count:\s*(\d+)?")
MAIN_THREAD_RE = re.compile(r"(?i)main-thread fallbacks:\s*(\d+)?")

VETO_WINDOW_RE = re.compile(
    r"(?i)veto window open|async-notify posted"
)
BUILD_ARMED_RE = re.compile(r"(?i)\bbuild armed\b")
PARENT_TURN_GAP_RE = re.compile(
    r"(?i)parent turn gap|turn gap observed|async-notify gap|one[- ]turn gap"
)
TINY_TWEAK_RE = re.compile(r"(?i)tiny-contract-tweak")
# Active Notes bullet only (not doc pointers like "Design-backloop: stages.md")
DESIGN_BACKLOOP_RE = re.compile(
    r"(?i)(?:^|\n)\s*[-*]\s*`?design-backloop`?(?:\s*$|\s*[—#–-]|\s*\n)"
)
# After rebuild / design-backloop Option 1 — derive honors before gate-c (verify-and-fix.md)
REVIEW_STALE_RE = re.compile(
    r"(?i)(?:^|\n)\s*[-*]\s*`?review-stale`?(?:\s*$|\s*[—#–-]|\s*\n)"
)
TEST_STALE_RE = re.compile(
    r"(?i)(?:^|\n)\s*[-*]\s*`?test-stale`?(?:\s*$|\s*[—#–-]|\s*\n)"
)
LAST_VERIFY_PASS_AT_RE = re.compile(
    r"^\*\*Last verify-pass at:\*\*\s*(.+)$", re.M | re.I
)
GATE_C_TEST_OVERRIDE_RE = re.compile(
    r"(?i)\bgate-c-test-override\b|\bGate C test override\b"
)
# Mode full stages that require 01a Result ok (Gate A fail-closed on --next)
POST_GATE_A_STAGES = frozenset(
    {
        "skim",
        "analyze",
        "grill",
        "design",
        "design-review",
        "api-contract-review",
        "db-design-review",
        "design-update",
        "tdd-review",
        "gate-b",
        "build",
        "smoke",
        "adversarial",
        "quality",
        "code-review-phase",
        "lens-security",
        "lens-perf",
        "lens-memory",
        "lens-api",
        "lens-db",
        "merge-findings",
        "fix-review",
        "test-full",
        "test-lite",
        "fix-tests",
        "gate-c",
        "merge",
    }
)
# Lens plan token → (stage id, artifact filename) — lenses.md
LENS_PLAN_MAP: dict[str, tuple[str, str]] = {
    "api": ("lens-api", "05-lens-api.md"),
    "db": ("lens-db", "05-lens-db.md"),
    "security": ("lens-security", "05-lens-security.md"),
    "perf": ("lens-perf", "05-lens-performance.md"),
    "performance": ("lens-perf", "05-lens-performance.md"),
    "memory": ("lens-memory", "05-lens-memory.md"),
}
UNPAID_LENS_BLOCK_STAGES = frozenset(
    {"test-full", "test-lite", "gate-c", "merge", "fix-tests"}
)
GRILL_SKIP_RE = re.compile(r"(?i)\bgrill\s+skipped\b")
# Optional 04a: Notes skip or artifact present (lenses.md · stages.md Step 4a)
TDD_04A_SKIP_RE = re.compile(r"(?i)\b04a\s+skipped\b")
# Logged clarity-check at design/code boundaries (parent-next.md · invariants.md)
CLARITY_CHECK_OK_RE = re.compile(
    r"(?i)clarity-check\s+ok\s*[—–-]\s*\S+"
)
CLARITY_CHECK_STAGES = frozenset(
    {
        "design-phase",
        "analyze",
        "grill",
        "design",
        "tdd-review",
        "build",
        "fix-review",
        "fix-tests",
    }
)
# Calibration after done (stages.md) — Notes lines or _calibration.md block
CALIBRATION_MODE_OK_RE = re.compile(r"(?i)\bMode\s+OK\?")
CALIBRATION_PROFILE_OK_RE = re.compile(r"(?i)\bReview\s+profile\s+OK\?")
CALIBRATION_FRICTION_RE = re.compile(
    r"(?i)\bBiggest\s+friction(?:\s+stage)?\?|\bfriction\s+stage\b"
)
RESULT_HEADER_RE = re.compile(
    r"(?im)^\*\*Result:\*\*\s*(.+)$|^Result:\s*(.+)$"
)
SMOKE_RESULT_RE = re.compile(
    r"(?im)^\*\*Smoke result:\*\*\s*(.+)$"
)
MODE_LAST_RUN_RE = re.compile(
    r"(?im)^\*\*Mode last run:\*\*\s*(.+)$"
)
LAST_STAGE_RE = re.compile(r"^\*\*Last stage:\*\*\s*(.+)$", re.M | re.I)
SOFT_TASK_CAP = 20
# Design-backloop recovery Next values → warn (not error) on default lint
DESIGN_BACKLOOP_RECOVERY_STAGES = frozenset(
    {
        "design-update",
        "design-review",
        "design-verify-phase",
        "api-contract-review",
        "db-design-review",
        "tdd-review",
        "gate-b",
    }
)

# Domain → allowed Result tokens (results.md). Soft check via --check-results.
RESULT_TOKENS_BY_ARTIFACT: dict[str, frozenset[str]] = {
    "01a-idea-ui-review.md": frozenset({"ok", "needs update", "escalate"}),
    "02-skim.md": frozenset({"done", "skipped"}),
    "02b-grill.md": frozenset({"frontier-empty", "needs-round", "skipped"}),
    "03a-design-review-log.md": frozenset({"clean", "needs update", "skipped"}),
    "03a-api-contract-review.md": frozenset({"clean", "needs update", "skipped"}),
    "03a-db-design-review.md": frozenset({"clean", "needs update", "skipped"}),
    "04a-tdd-test-review.md": frozenset({"clean", "needs more tests"}),
    "05-review-log.md": frozenset({"clean", "needs fix"}),
    "05-lens-api.md": frozenset({"clean", "needs fix", "has findings"}),
    "05-lens-db.md": frozenset({"clean", "needs fix", "has findings"}),
    "05-lens-security.md": frozenset({"clean", "needs fix", "has findings"}),
    "05-lens-performance.md": frozenset({"clean", "needs fix", "has findings"}),
    "05-lens-memory.md": frozenset({"clean", "needs fix", "has findings"}),
    "06-test-log.md": frozenset(
        {"success", "failure", "smoke-pass", "smoke-fail", "pending"}
    ),
}

# Soft line caps for whole-file body (size-caps.md approximations)
SIZE_CAP_LINES: dict[str, int] = {
    "02-skim.md": 40,
    "01-idea.md": 80,
    "02-analysis.md": 120,
    "02b-grill.md": 60,
    "03-design.md": 200,
}


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


def _parse_lens_plan_tokens(text: str) -> set[str]:
    """Return lowercase lens tokens from Lens plan (empty if missing/none)."""
    m = LENS_PLAN_RE.search(text)
    if not m:
        return set()
    raw = m.group(1).strip()
    if _looks_like_template(raw):
        return set()
    primary = re.split(r"\s+[—#–-]\s+|\s{2,}", raw, maxsplit=1)[0].strip()
    compact = primary.strip("`*_").lower()
    if compact in ("", "none", "n/a", "-", "—"):
        return set()
    parts = re.split(r"[,|+/]+", compact)
    return {p.strip() for p in parts if p.strip()}


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

    return issues


@dataclass
class Issue:
    severity: str  # error | warn
    message: str


def _first_token(raw: str) -> str:
    return raw.strip().split()[0].strip("|`*_").lower() if raw.strip() else ""


def _looks_like_template(raw: str) -> bool:
    """Unfilled template values contain | or multiple alternative tokens."""
    s = raw.strip()
    if not s:
        return True
    if "|" in s:
        # Pending parallel allows literal api|db as a single enum value
        compact = s.strip().lower().strip("`*_")
        if compact in VALID_PENDING_PARALLEL:
            return False
        return True
    parts = [p for p in re.split(r"[\s,/]+", s) if p and p not in ("—", "-", "–")]
    return len(parts) > 1 and any(
        p.lower().strip("`*_") in VALID_STATUS
        | VALID_MODE
        | VALID_REVIEW_PROFILE
        | VALID_GATE_B_VETO
        | VALID_YES_NO
        for p in parts
    )


def _exact_enum_token(
    raw: str, allowed: frozenset[str], field: str, issues: list[Issue]
) -> str | None:
    """Require a single exact enum token; reject templates and multi-token values."""
    s = raw.strip()
    # Special-case Pending parallel: allow api|db as one token
    compact = s.lower().strip("`*_")
    primary_pp = re.split(r"\s+[—#–-]\s+|\s{2,}", compact, maxsplit=1)[0].strip()
    if field == "Pending parallel" and primary_pp in allowed:
        return primary_pp

    if _looks_like_template(s):
        issues.append(
            Issue(
                "error",
                f"{field} still looks like a template ({s!r}) — "
                f"set exactly one of {sorted(allowed)}",
            )
        )
        return None
    primary = re.split(r"\s+[—#–-]\s+|\s{2,}", s, maxsplit=1)[0].strip()
    tokens = primary.split()
    if len(tokens) != 1:
        issues.append(
            Issue(
                "error",
                f"{field} must be a single token from {sorted(allowed)} (got {s!r})",
            )
        )
        return None
    token = tokens[0].strip("`*_").lower()
    if token not in allowed:
        issues.append(
            Issue(
                "error",
                f"{field} must be one of {sorted(allowed)} (got {token!r})",
            )
        )
        return None
    return token


def _check_yes_no_flag(
    text: str, line_re: re.Pattern[str], field: str, issues: list[Issue]
) -> str | None:
    m = line_re.search(text)
    if not m:
        return None
    return _exact_enum_token(m.group(1), VALID_YES_NO, field, issues)


def _parsed_yes_no(text: str, line_re: re.Pattern[str]) -> str | None:
    """Return yes/no only when exact single token; None for missing/template/invalid."""
    m = line_re.search(text)
    if not m:
        return None
    s = m.group(1).strip()
    if _looks_like_template(s):
        return None
    primary = re.split(r"\s+[—#–-]\s+|\s{2,}", s, maxsplit=1)[0].strip()
    tokens = primary.split()
    if len(tokens) != 1:
        return None
    token = tokens[0].strip("`*_").lower()
    if token not in VALID_YES_NO:
        return None
    return token


def _notes_blob(text: str) -> str:
    m = NOTES_SECTION_RE.search(text)
    return m.group(1) if m else text


def _run_log_blob(text: str) -> str:
    m = RUN_LOG_SECTION_RE.search(text)
    return m.group(1) if m else ""


def _parse_pending_parallel(text: str, issues: list[Issue]) -> str | None:
    m = PENDING_PARALLEL_RE.search(text)
    if not m:
        return None
    return _exact_enum_token(
        m.group(1), VALID_PENDING_PARALLEL, "Pending parallel", issues
    )


def _artifact_exists(run_dir: Path | None, name: str) -> bool:
    if run_dir is None:
        return False
    return (run_dir / name).is_file()


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


def _card_next_stage_id(text: str) -> str:
    """Orchestrator card Next step token (empty if missing)."""
    next_m = CARD_NEXT_RE.search(text)
    if not next_m:
        return ""
    return _extract_stage_token(next_m.group(1))


def _last_stage_id(text: str) -> str:
    """Last stage field token (empty if missing)."""
    m = LAST_STAGE_RE.search(text)
    if not m:
        return ""
    return _extract_stage_token(m.group(1))


def _check_gate_c_approved(
    text: str, issues: list[Issue], *, before_merge: bool
) -> None:
    """Require durable Gate C approved when Next=merge or --before-merge."""
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


def _tdd_04a_settled(text: str, run_dir: Path | None) -> bool:
    """True when 04a artifact exists or Notes say ``04a skipped``."""
    if _artifact_exists(run_dir, "04a-tdd-test-review.md"):
        return True
    return bool(TDD_04A_SKIP_RE.search(_notes_blob(text)))


def _clarity_check_logged(text: str) -> bool:
    """True when Notes or Run log has ``clarity-check ok — <boundary>``."""
    blob = _notes_blob(text) + "\n" + _run_log_blob(text)
    return bool(CLARITY_CHECK_OK_RE.search(blob))


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
    """Soft-warn when clarity-check token missing before design/code boundaries."""
    next_id = _card_next_stage_id(text)
    if not (before_build or next_id in CLARITY_CHECK_STAGES):
        return
    if _clarity_check_logged(text):
        return
    label = next_id or "build"
    issues.append(
        Issue(
            "warn",
            f"clarity-check ok — <boundary> missing from Notes/Run log "
            f"before `{label}` (parent-next.md · invariants.md)",
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


def _parse_result_token(blob: str) -> str | None:
    """Primary Result token from artifact body (first matching header)."""
    m = RESULT_HEADER_RE.search(blob)
    if not m:
        return None
    raw = (m.group(1) or m.group(2) or "").strip()
    if not raw:
        return None
    # Template alternatives like "pending | smoke-pass | …"
    if "|" in raw and not re.match(r"^[a-z0-9 _-]+$", raw.lower().strip("`*_")):
        return None
    # Take first alternative before | for filled single tokens only
    primary = re.split(r"\s+[—#–-]\s+|\s{2,}", raw, maxsplit=1)[0].strip()
    if "|" in primary:
        return None
    token = primary.strip("`*_").lower()
    if token in ("", "none", "n/a", "-", "—"):
        return None
    return token


def _read_artifact(run_dir: Path | None, name: str) -> str:
    if run_dir is None:
        return ""
    path = run_dir / name
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _smoke_pass(run_dir: Path | None) -> bool:
    blob = _read_artifact(run_dir, "06-test-log.md")
    if not blob:
        return False
    m = SMOKE_RESULT_RE.search(blob)
    if m and _first_token(m.group(1)) == "smoke-pass":
        return True
    # Top-level Result may be smoke-pass when only Smoke ran
    top = _parse_result_token(blob)
    return top == "smoke-pass"


def _test_log_success(run_dir: Path | None, *, expect_mode: str | None) -> bool:
    """True when Result success; if expect_mode set, Mode last run must match.

    Fail closed when expect_mode is full|lite and Mode last run is missing
    or mismatched (hitl.md Gate C test bar).
    """
    blob = _read_artifact(run_dir, "06-test-log.md")
    if not blob:
        return False
    if _parse_result_token(blob) != "success":
        return False
    if expect_mode is None:
        return True
    m = MODE_LAST_RUN_RE.search(blob)
    if not m:
        return False  # fail closed — Mode last run required for full/lite bar
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


def _parse_last_verify_pass_at(text: str) -> float | None:
    """Unix timestamp from **Last verify-pass at:** ISO-8601, or None."""
    m = LAST_VERIFY_PASS_AT_RE.search(text)
    if not m:
        return None
    raw = m.group(1).strip().strip("`*")
    if not raw or _looks_like_template(raw):
        return None
    token = _first_token(raw).lower()
    if token in ("none", "n/a", "-", "—", "pending"):
        return None
    # Allow trailing notes after ISO (e.g. "2026-10-18T12:00:00Z — rebuild")
    iso = raw.split()[0] if raw.split() else raw
    try:
        dt = _dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_dt.timezone.utc)
    return dt.timestamp()


def _artifact_mtime(run_dir: Path | None, name: str) -> float | None:
    if run_dir is None:
        return None
    path = run_dir / name
    if not path.is_file():
        return None
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def _review_profile(text: str) -> str | None:
    rp_m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    if not rp_m or _looks_like_template(rp_m.group(1)):
        return None
    return _first_token(rp_m.group(1))


def _implied_review_stale(text: str, run_dir: Path | None) -> bool:
    """E2: 05 clean older than Last verify-pass at without Notes review-stale."""
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
    """True when Notes/Smoke field show independent re-run or explicit waive."""
    notes = _notes_blob(text)
    if SMOKE_WAIVE_RE.search(notes):
        return True
    if SMOKE_RERUN_DONE_RE.search(notes):
        return True
    if SMOKE_RERUN_DONE_RE.search(text):
        return True
    return False


def _check_skip_review_build_only_smoke(
    text: str,
    issues: list[Issue],
    *,
    before_merge: bool,
    run_dir: Path | None,
) -> None:
    """E5: warn when skip-review merge relies only on Build-writes-Smoke.

    Prefer warn (fast path still legal). No warn when Notes smoke-waive /
    smoke-pass (re-run) evidence / gate-c-test-override.
    """
    enforce = before_merge or _card_next_stage_id(text) == "merge"
    if not enforce:
        return
    notes = _notes_blob(text)
    if GATE_C_TEST_OVERRIDE_RE.search(notes):
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
    issues.append(
        Issue(
            "warn",
            "skip-review merge: only Build-writes-Smoke — prefer Notes "
            "`smoke re-run` (independent once) or Notes smoke-waive / "
            "gate-c-test-override before Gate C (verify-and-fix.md · hitl.md)",
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
    if GATE_C_TEST_OVERRIDE_RE.search(notes):
        return

    rp_m = REQUIRED_FIELD_PATTERNS["Review profile"].search(text)
    if not rp_m:
        return
    review = _first_token(rp_m.group(1))
    if review not in VALID_REVIEW_PROFILE or _looks_like_template(rp_m.group(1)):
        return

    mode_m = REQUIRED_FIELD_PATTERNS["Mode"].search(text)
    mode = _first_token(mode_m.group(1)) if mode_m else None

    if review == "full":
        if not _test_log_success(run_dir, expect_mode="full"):
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar (full): need 06-test-log.md Result success "
                    "and Mode last run full (hitl.md) — or Notes "
                    "gate-c-test-override",
                )
            )
        return

    if review == "lite":
        if not _test_log_success(run_dir, expect_mode="lite"):
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar (lite): need 06-test-log.md Result success "
                    "and Mode last run lite (hitl.md) — or Notes "
                    "gate-c-test-override",
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
                    "(hitl.md) — or Notes gate-c-test-override",
                )
            )
        if not _smoke_pass(run_dir):
            issues.append(
                Issue(
                    "error",
                    "Gate C test bar (skip-review): need 06-test-log Smoke "
                    "result smoke-pass (hitl.md) — or Notes gate-c-test-override",
                )
            )


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
    _check_async_gate_b_gap(text, issues, before_build=before_build)
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


def _extract_stage_token(raw: str) -> str:
    s = raw.strip().strip("`*_")
    if not s:
        return ""
    return re.split(r"[\s(/]", s)[0].strip("`*_").lower()


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
                    "— card remains launch override; confirm or update card "
                    "(parent-next.md · stages.md Resume)"
                )
        elif derived and stage_id and derived != stage_id:
            print(
                f"warn: card Next `{stage_id}` differs from derived `{derived}` "
                "— card remains launch override; confirm or update card "
                "(parent-next.md · stages.md Resume)"
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
        return 0

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
            return 0

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
                f"warn: Lens plan unpaid — {reason}; do not advance to "
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
            return 0
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
            return 0
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
            return 0

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
        return 0

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
                f"warn: {stage_name} Result must be clean before Build "
                f"(03a-design-review-log.md Result is {detail}) — "
                "SKILL.md · stages.md"
            )
            print("companion: stages.md · parent-next.md · SKILL.md")
            print("handoff: do-not-launch")
            print(
                f"next action: finish {stage_name} to Result clean "
                "(or design-update), then re-run --next"
            )
            return 0

    # Parent gates / blocked async gap: never emit Task handoff
    if stage_id == "build" and veto_window and not build_armed:
        print(
            "blocked: veto window open — set Build armed on this turn "
            "(hitl.md), then Build"
        )
        print("companion: hitl.md · parent-next.md")
        print("handoff: do-not-launch")
        print("next action: set Notes/Run log Build armed (parent turn gap), re-run --next")
        return 0
    if stage_id == "build":
        hitl_tier = _parse_hitl_gate_b(text)
        if hitl_tier == "blocking" and not _gate_b_approved_ok(text):
            print("companion: hitl.md · parent-next.md (row for `build`)")
            print("handoff: do-not-launch")
            print(
                "next action: blocking Gate B — set Gate B approved "
                "yes (or named pick), then re-run --next"
            )
            return 0
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
        return 0
    if stage_id == "merge":
        _gc_raw, gc_actions = _parse_gate_c_approved(text)
        if _gc_raw is None or _gc_raw == "none" or not gc_actions:
            print("companion: hitl.md · parent-next.md (row for `merge`)")
            print("handoff: do-not-launch")
            print(
                "next action: Gate C blocking ask; set Gate C approved "
                "(non-empty commit|push|pr|merge subset), then re-run --next"
            )
            return 0
        bar_issues: list[Issue] = []
        _check_gate_c_test_bar(
            text, bar_issues, before_merge=True, run_dir=run_dir
        )
        bar_errors = [i for i in bar_issues if i.severity == "error"]
        if bar_errors:
            for i in bar_errors:
                print(f"warn: {i.message}")
            print("companion: hitl.md · parent-next.md (row for `merge`)")
            print("handoff: do-not-launch")
            print(
                "next action: meet Gate C test bar (or Notes gate-c-test-override), "
                "then re-run --next"
            )
            return 0

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


if __name__ == "__main__":
    sys.exit(main())
