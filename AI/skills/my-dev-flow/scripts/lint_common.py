"""Shared constants, parsers, and helpers for my-dev-flow lint.

Enforces field tokens and path helpers used across Gate B/C / derive /
stage-id checks. Policy SoT: hitl.md · stages.md · parent-next.md · invariants.md.
"""
from __future__ import annotations

import datetime as _dt
import json
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
MAX_ROUND_CAP = 3
ROUND_HEADER_RE = re.compile(r"^\*\*Round:\*\*\s*(\d+)\s*$", re.M | re.I)
VERIFY_ATTEMPTS_RE = re.compile(
    r"^\*\*Verify attempts:\*\*\s*(\d+)\s*$", re.M | re.I
)
TEST_FIX_ROUNDS_RE = re.compile(
    r"(?i)smoke↔fix\s*/\s*test↔fix\s*rounds:\s*(\d+)"
)
# Match ONLY "review fix rounds:" — never design-review rounds (H1)
REVIEW_FIX_ROUNDS_RE = re.compile(
    r"(?i)review\s+fix\s+rounds:\s*(\d+)"
)
# Decision N raise-cap unlock (invariants.md · M2)
# Shape: max-round-cap — <domain> — <N> — user: "…"
MAX_ROUND_CAP_DOMAINS = frozenset(
    {
        "design-review",
        "gate-a",
        "verify",
        "review-fix",
        "test-fix",
    }
)
MAX_ROUND_CAP_RE = re.compile(
    r"(?im)(?:^|\n)\s*[-*]?\s*`?max-round-cap`?\s*[—–-]\s*"
    r"(?P<domain>design-review|gate-a|verify|review-fix|test-fix)"
    r"\s*[—–-]\s*(?P<n>\d+)\s*[—–-]\s*"
    r"user:\s*\"(?P<quote>[^\"]+)\""
)
FIX_ASK_SECTION_RE = re.compile(
    r"(?im)^##\s*Fix ask\b",
)

VALID_STATUS = frozenset({"running", "paused", "stopped", "done"})
VALID_MODE = frozenset({"simple", "full"})
VALID_REVIEW_PROFILE = frozenset({"full", "lite", "skip-review"})
VALID_GATE_B_VETO = frozenset({"none", "pending"})
VALID_YES_NO = frozenset({"yes", "no"})
VALID_HITL_TIER = frozenset({"auto", "async-notify", "blocking"})
VALID_GATE_C_ACTIONS = frozenset({"commit", "push", "pr", "merge"})
VALID_PENDING_PARALLEL = frozenset({"none", "api", "db", "api|db"})
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
# Mode full + profile full E1: independent Smoke before these (verify-and-fix.md)
# fix-tests: fail-closed when Build smoke-pass unpaid; smoke-fail→Fix exempt
# (lint_core · _check_smoke_pass_before_post_smoke / jump-ahead exception)
FULL_PROFILE_E1_GATE_STAGES = frozenset(
    {
        "adversarial",
        "quality",
        "code-review-phase",
        "fix-review",
        "merge-findings",
        "lens-security",
        "lens-perf",
        "lens-memory",
        "lens-api",
        "lens-db",
        "test-full",
        "fix-tests",
        "merge",
        "gate-c",
    }
)
# --before-design-review auto when card Next ∈ this set (MDF-R1)
DESIGN_REVIEW_PHASE_STAGES = frozenset(
    {
        "design-review",
        "design-verify-phase",
        "api-contract-review",
        "db-design-review",
    }
)
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
HAS_AUTH_LINE_RE = re.compile(
    r"^[-*]?\s*\*\*Has auth/PII/schema:\*\*\s*(.+)$", re.M | re.I
)
HITL_GATE_B_RE = re.compile(r"^[-*]?\s*\*\*HITL Gate B:\*\*\s*(.+)$", re.M | re.I)
GATE_B_APPROVED_RE = re.compile(
    r"^[-*]?\s*\*\*Gate B approved:\*\*\s*(.+)$", re.M | re.I
)
GATE_C_APPROVED_RE = re.compile(
    r"^[-*]?\s*\*\*Gate C approved:\*\*\s*(.+)$", re.M | re.I
)
LENS_PLAN_RE = re.compile(r"^\*\*Lens plan:\*\*\s*(.+)$", re.M | re.I)
SMOKE_RERUN_RE = re.compile(r"(?i)\bsmoke\s+re-?run\b")
SMOKE_WAIVE_RE = re.compile(
    r"(?im)(?:^|\n)\s*[-*]\s*`?smoke\s*-?\s*waive`?(?:\s*$|\s*[—#–-]|\s*\n)|"
    r"(?im)(?:^|\n)\s*[-*]\s*`?waive\s+(?:independent\s+)?smoke`?"
    r"(?:\s*$|\s*[—#–-]|\s*\n)"
)
SMOKE_RERUN_DONE_RE = re.compile(
    r"(?i)smoke-pass\s*\(\s*re-?run\s*\)|"
    r"smoke\s+re-?run\s+(?:done|pass|ok|complete)|"
    r"independent\s+smoke\s+(?:pass|ok|done)"
)
# Run log: - **HH:MM** · status · smoke · note (stage column = smoke)
RUN_LOG_SMOKE_STAGE_RE = re.compile(
    r"(?im)^\s*[-*]\s*\*\*\d{1,2}:\d{2}(?::\d{2})?\*\*\s*·\s*[^\n·]+·\s*smoke\s*·"
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
DESIGN_BACKLOOP_RE = re.compile(
    r"(?i)(?:^|\n)\s*[-*]\s*`?design-backloop`?(?:\s*$|\s*[—#–-]|\s*\n)"
)
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
    r"(?im)(?:^|\n)\s*[-*]\s*`?(?:gate-c-test-override|Gate C test override)`?"
    r"(?:\s*$|\s*[—#–-]|\s*\n)"
)
DOCS_ONLY_RE = re.compile(r"(?i)\bdocs-only\b")
COMPLEXITY_RE = re.compile(r"^\*\*Complexity:\*\*\s*(.+)$", re.M | re.I)
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
TDD_04A_SKIP_RE = re.compile(r"(?i)\b04a\s+skipped\b")
CLARITY_CHECK_OK_RE = re.compile(
    r"(?i)clarity-check\s+ok\s*[—–-]\s*(\S+)"
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
        "merge",
    }
)
# All clarity Next stages: boundary-matched token required (parent-next.md · M1)
CLARITY_CHECK_HIGH_RISK = frozenset(CLARITY_CHECK_STAGES)
# Prefer new Gate A artifact; accept legacy filename for one resume cycle (E5)
GATE_A_ARTIFACT_PREFERRED = "01a-gate-a.md"
GATE_A_ARTIFACT_LEGACY = "01a-idea-ui-review.md"
GATE_A_ARTIFACT_NAMES = (GATE_A_ARTIFACT_PREFERRED, GATE_A_ARTIFACT_LEGACY)
# Consent / waiver provenance (hitl.md · R1) — quote length ≥ N, not filler
PROVENANCE_MIN_QUOTE_LEN = 12
PROVENANCE_FILLER_QUOTES = frozenset(
    {
        "yes",
        "ok",
        "okay",
        "yep",
        "yup",
        "sure",
        "fine",
        "lgtm",
        "approved",
        "approve",
        "accepted",
        "accept",
        "merge",
        "ship",
        "go",
        "proceed",
        "ship it",
        "looks good",
        "good",
        "done",
        "confirmed",
        "confirm",
        "agree",
        "agreed",
    }
)
PROVENANCE_KINDS = frozenset(
    {
        "gate-b-approved",
        "gate-c-approved",
        "gate-c-test-override",
        "smoke-waive",
        "docs-only",
        "smoke-pass-rerun",
        "card-override",
    }
)
PROVENANCE_RE = re.compile(
    r"(?im)(?:^|\n)\s*[-*]?\s*`?provenance`?\s*[—–-]\s*"
    r"(gate-b-approved|gate-c-approved|gate-c-test-override|smoke-waive|"
    r"docs-only|smoke-pass-rerun|card-override)"
    r"\s*[—–-]\s*user:\s*\"([^\"]+)\"",
)
CARD_OVERRIDE_RE = re.compile(
    r"(?im)(?:^|\n)\s*[-*]?\s*`?card-override`?\s*[—–-]\s*\S+"
)
# Turn-boundary token from prior --next do-not-launch (hitl.md · S2)
ASYNC_GAP_PENDING_RE = re.compile(
    r"(?im)(?:^|\n)\s*[-*]?\s*`?async-gap-pending`?\s*[—–-]\s*"
    r"(\d{1,2}:\d{2}(?::\d{2})?)"
)
ASYNC_GAP_SIDECAR = ".lint-async-gap"
CONSENT_SNAP_SIDECAR = ".lint-consent-snap"
# Parent Run-log ack when consent fields change after a Task (hitl.md · M1)
PARENT_CONSENT_WRITE_RE = re.compile(
    r"(?i)\bparent\s+consent\s+write\b"
)
# Mode simple async-notify requires explicit user request (hitl-gate-b.md · E4)
ASYNC_NOTIFY_REQUESTED_RE = re.compile(
    r"(?im)(?:^|\n)\s*[-*]?\s*`?async-notify\s+requested`?\s*[—–-]\s*"
    r"user:\s*\"(?P<quote>[^\"]+)\""
)
# Optional parent-only consent scratchpad (Tasks never Write) — hitl.md · H1
CONSENT_SIDECAR = ".consent.md"
FIX_REVIEW_RUN_LOG_RE = re.compile(
    r"(?i)·\s*(?:done|running|paused)\s*·\s*fix-review\b"
)
REVIEW_RESULT_RANK = {
    "needs fix": 3,
    "has findings": 3,
    "pending": 2,
    "clean": 1,
}
# Run log line: - **HH:MM** · status · stage · note
RUN_LOG_ENTRY_RE = re.compile(
    r"(?im)^\s*[-*]\s*\*\*(\d{1,2}:\d{2}(?::\d{2})?)\*\*\s*·\s*[^\n·]+·\s*[^\n·]+·\s*(.+)$"
)
# Stages that are "earlier" than Build (unsafe card=build when derived here)
PRE_BUILD_DERIVED = frozenset(
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
        "gate-b",
    }
)
# Jump-ahead while derived is still pre-Build / pre-verify → unsafe (S3)
JUMP_AHEAD_FROM_PRE_BUILD = frozenset(
    {
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
# Derived still in review pipeline (post-Build) — test/gate-c/merge jump is unsafe (T1)
IN_REVIEW_DERIVED = frozenset(
    {
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
    }
)
# Cards that skip remaining review work while derived ∈ IN_REVIEW_DERIVED
JUMP_AHEAD_FROM_REVIEW = frozenset(
    {
        "test-full",
        "test-lite",
        "fix-tests",
        "gate-c",
        "merge",
    }
)
# Pre-lens review (Adv / Quality / lite / Fix) — lens-* / merge-findings jump unsafe (U1)
PRE_LENS_DERIVED = frozenset(
    {
        "adversarial",
        "quality",
        "code-review-phase",
        "fix-review",
    }
)
LENS_JUMP_AHEAD_CARDS = frozenset(
    {
        "lens-security",
        "lens-perf",
        "lens-memory",
        "lens-api",
        "lens-db",
        "merge-findings",
    }
)
# H1: verify-fail + Last stage post-Build → Fix / same-stage (not build)
# smoke/test-* → fix-tests; review pipeline → fix-review; already fix-* → same
VERIFY_FAIL_FIX_TESTS_STAGES = frozenset(
    {"smoke", "test-lite", "test-full", "fix-tests"}
)
VERIFY_FAIL_FIX_REVIEW_STAGES = frozenset(
    {
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
    }
)
# Jump-ahead while Smoke unpaid (derived=smoke) → unsafe (M1 · same class as merge)
# Derive returns fix-tests on smoke-fail|failure (incl. skip-review) until Last
# stage=fix-tests + verify-pass → re-smoke. JUMP_AHEAD allows Next=fix-tests
# on smoke-fail ONLY when Last stage ≠ fix-tests (before Fix unlock). After Fix
# verify-pass, derived=smoke|test-* + Next=fix-tests → unsafe do-not-launch.
# Unpaid/missing → derived=smoke (or build under skip-review) blocks fix-tests.
# gate-c vs derived=smoke fail-closed (E1).
JUMP_AHEAD_FROM_SMOKE = frozenset(
    {
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
    }
)
# Review entry (Adv / lite combined) — smoke / fix-tests blocked unless Notes (T2)
REVIEW_ENTRY_DERIVED = frozenset({"adversarial", "code-review-phase"})
FIX_ASK_RE = re.compile(r"(?i)\bfix\s+ask\b")
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
# Prefer "Test path last run"; accept legacy "Mode last run" (M2 · LEGACY.md)
TEST_PATH_LAST_RUN_RE = re.compile(
    r"(?im)^\*\*(?:Test path last run|Mode last run):\*\*\s*(.+)$"
)
MODE_LAST_RUN_RE = TEST_PATH_LAST_RUN_RE  # alias for callers / one resume cycle
LAST_STAGE_RE = re.compile(r"^\*\*Last stage:\*\*\s*(.+)$", re.M | re.I)
SOFT_TASK_CAP = 25
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
RESULT_TOKENS_BY_ARTIFACT: dict[str, frozenset[str]] = {
    "01a-gate-a.md": frozenset({"ok", "needs update", "escalate"}),
    "01a-idea-ui-review.md": frozenset({"ok", "needs update", "escalate"}),  # LEGACY
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
SIZE_CAP_LINES: dict[str, int] = {
    "02-skim.md": 40,
    "01-idea.md": 80,
    "02-analysis.md": 120,
    "02b-grill.md": 60,
    "03-design.md": 200,
}
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
def _normalize_provenance_quote(quote: str) -> str:
    """Lowercase + collapse whitespace for filler checks."""
    return re.sub(r"\s+", " ", (quote or "").strip().lower())


def _provenance_quote_ok(quote: str) -> bool:
    """True when quote meets length + non-filler bar (hitl.md · S4)."""
    q = (quote or "").strip()
    if len(q) < PROVENANCE_MIN_QUOTE_LEN:
        return False
    norm = _normalize_provenance_quote(q)
    if not norm or norm in PROVENANCE_FILLER_QUOTES:
        return False
    return True


def _provenance_kinds(text: str) -> set[str]:
    """Return provenance kinds with quality user quotes in Notes or Run log."""
    blob = _notes_blob(text) + "\n" + _run_log_blob(text)
    found: set[str] = set()
    for m in PROVENANCE_RE.finditer(blob):
        kind = m.group(1).strip().lower()
        quote = (m.group(2) or "").strip()
        if kind in PROVENANCE_KINDS and _provenance_quote_ok(quote):
            found.add(kind)
    return found
def _has_provenance(text: str, kind: str) -> bool:
    return kind.lower() in _provenance_kinds(text)
def _clarity_boundaries_logged(text: str) -> set[str]:
    """Return boundary tokens from ``clarity-check ok — <boundary>`` lines."""
    blob = _notes_blob(text) + "\n" + _run_log_blob(text)
    return {
        m.group(1).strip().strip("`*_").lower()
        for m in CLARITY_CHECK_OK_RE.finditer(blob)
        if m.group(1) and m.group(1).strip()
    }
def _card_override_logged(text: str) -> bool:
    """True when Notes have ``card-override — <reason>`` (stages.md · R4)."""
    return bool(CARD_OVERRIDE_RE.search(_notes_blob(text)))


def _card_override_ok(text: str) -> bool:
    """True when card-override Notes + provenance unlock unsafe derive (S7)."""
    return _card_override_logged(text) and _has_provenance(text, "card-override")


def _hhmm_to_minutes(ts: str) -> int | None:
    """Parse HH:MM or HH:MM:SS to minutes-from-midnight; None if invalid."""
    parts = (ts or "").strip().split(":")
    if len(parts) not in (2, 3):
        return None
    try:
        h, m = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    if not (0 <= h <= 23 and 0 <= m <= 59):
        return None
    return h * 60 + m


def _async_digest_timestamps(text: str) -> set[str]:
    """Run log timestamps for async-notify / veto-window digest lines."""
    out: set[str] = set()
    for ts, note in _run_log_timestamped_entries(text):
        low = note.lower()
        if VETO_WINDOW_RE.search(note) or "async-notify" in low:
            out.add(ts)
    return out


def _async_arm_timestamps(text: str) -> set[str]:
    """Run log timestamps for Build armed lines."""
    return {
        ts
        for ts, note in _run_log_timestamped_entries(text)
        if BUILD_ARMED_RE.search(note)
    }


def _async_gap_pending_tokens(text: str) -> set[str]:
    """Timestamps from Notes/Run log ``async-gap-pending — HH:MM`` lines."""
    blob = _notes_blob(text) + "\n" + _run_log_blob(text)
    return {m.group(1).strip() for m in ASYNC_GAP_PENDING_RE.finditer(blob)}


def _async_gap_sidecar_path(run_dir: Path | None) -> Path | None:
    if run_dir is None:
        return None
    return run_dir / ASYNC_GAP_SIDECAR


def _read_async_gap_sidecar(run_dir: Path | None) -> str | None:
    path = _async_gap_sidecar_path(run_dir)
    if path is None or not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8").strip().splitlines()
    return raw[0].strip() if raw else None


def _write_async_gap_sidecar(run_dir: Path | None, digest_ts: str) -> None:
    path = _async_gap_sidecar_path(run_dir)
    if path is None or not digest_ts:
        return
    path.write_text(f"{digest_ts.strip()}\n", encoding="utf-8")


def _consent_fingerprint(text: str) -> dict[str, object]:
    """Stable fingerprint of parent-only consent / waiver fields (hitl.md · M1)."""
    notes = _notes_blob(text)
    run_log = _run_log_blob(text)
    notes_and_log = notes + "\n" + run_log
    gate_b_m = GATE_B_APPROVED_RE.search(text)
    gate_c_m = GATE_C_APPROVED_RE.search(text)
    gate_b = (
        _first_token(gate_b_m.group(1)) if gate_b_m else ""
    )
    gate_c = (
        gate_c_m.group(1).strip() if gate_c_m else ""
    )
    build_armed = bool(BUILD_ARMED_RE.search(notes_and_log))
    waivers: list[str] = []
    if GATE_C_TEST_OVERRIDE_RE.search(notes):
        waivers.append("gate-c-test-override")
    if SMOKE_WAIVE_RE.search(notes):
        waivers.append("smoke-waive")
    cm = COMPLEXITY_RE.search(text)
    if DOCS_ONLY_RE.search(notes) or (
        cm is not None and DOCS_ONLY_RE.search(cm.group(1))
    ):
        waivers.append("docs-only")
    # Notes section only — Run-log DONE alone must not flip the fingerprint
    if SMOKE_RERUN_DONE_RE.search(notes):
        waivers.append("smoke-pass-rerun")
    if CARD_OVERRIDE_RE.search(notes):
        waivers.append("card-override")
    # Count occurrences for change detection (line may repeat)
    ack_count = len(PARENT_CONSENT_WRITE_RE.findall(run_log))
    return {
        "gate_b_approved": gate_b.lower(),
        "gate_c_approved": gate_c.lower(),
        "build_armed": build_armed,
        "provenance_kinds": sorted(_provenance_kinds(text)),
        "waivers": sorted(waivers),
        "parent_consent_ack_count": ack_count,
    }


def _consent_fields_changed(
    before: dict[str, object], after: dict[str, object]
) -> bool:
    """True when Gate B/C / Build armed / provenance / waivers differ."""
    keys = (
        "gate_b_approved",
        "gate_c_approved",
        "build_armed",
        "provenance_kinds",
        "waivers",
    )
    return any(before.get(k) != after.get(k) for k in keys)


def _consent_snap_path(run_dir: Path | None) -> Path | None:
    if run_dir is None:
        return None
    return run_dir / CONSENT_SNAP_SIDECAR


def snapshot_consent(run_dir: Path) -> int:
    """Write ``.lint-consent-snap`` before Task launch. Exit 0 on success."""
    run_md = run_dir / "00-run.md"
    if not run_md.is_file():
        print(f"error: missing {run_md}", file=sys.stderr)
        return 2
    text = run_md.read_text(encoding="utf-8")
    fp = _consent_fingerprint(text)
    path = _consent_snap_path(run_dir)
    assert path is not None
    path.write_text(json.dumps(fp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"consent-snap: wrote {path.name}")
    return 0


def check_consent_writes(
    run_dir: Path, *, require_snap: bool = True
) -> list[Issue]:
    """Error if consent fields changed since snap without parent Run-log ack.

    Habit: ``--snapshot-consent`` before Task; ``--check-consent-writes`` after.
    Machine path (``--next`` / ``--before-build`` / ``--before-merge``): call with
    ``require_snap=False`` so missing snap is a no-op; dirty snap still errors.
    Residual: a Task can still forge both fields and a fake Run-log ack —
    raises cost only (hitl.md).
    """
    issues: list[Issue] = []
    path = _consent_snap_path(run_dir)
    run_md = run_dir / "00-run.md"
    if path is None or not path.is_file():
        if require_snap:
            issues.append(
                Issue(
                    "error",
                    "missing .lint-consent-snap — run --snapshot-consent before Task "
                    "(hitl.md Parent-only consent · M1)",
                )
            )
        return issues
    if not run_md.is_file():
        if require_snap:
            issues.append(Issue("error", f"missing {run_md.name} for consent check"))
        return issues
    try:
        before = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(
            Issue("error", f"unreadable .lint-consent-snap: {exc}")
        )
        return issues
    text = run_md.read_text(encoding="utf-8")
    after = _consent_fingerprint(text)
    if not _consent_fields_changed(before, after):
        return issues
    before_acks = int(before.get("parent_consent_ack_count") or 0)
    after_acks = int(after.get("parent_consent_ack_count") or 0)
    if after_acks > before_acks:
        return issues
    issues.append(
        Issue(
            "error",
            "consent fields changed since --snapshot-consent without new Run log "
            "`parent consent write` line — parent must record Gate B/C / Build "
            "armed / provenance / waivers (never from Task returns) (hitl.md · M1)",
        )
    )
    return issues


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


def _run_log_has_smoke_stage(text: str) -> bool:
    """True when Run log has a line with stage column ``smoke``."""
    return bool(RUN_LOG_SMOKE_STAGE_RE.search(_run_log_blob(text)))


def _smoke_section_after_verify_pass(
    text: str, run_dir: Path | None
) -> bool:
    """True when 06 Smoke result is smoke-pass and mtime > Last verify-pass at."""
    if run_dir is None:
        return False
    blob = _read_artifact(run_dir, "06-test-log.md")
    if not blob:
        return False
    m = SMOKE_RESULT_RE.search(blob)
    ok = bool(m and _first_token(m.group(1)) == "smoke-pass")
    if not ok:
        ok = _parse_result_token(blob) == "smoke-pass"
    if not ok:
        return False
    epoch = _parse_last_verify_pass_at(text)
    if epoch is None:
        return False
    mt = _artifact_mtime(run_dir, "06-test-log.md")
    if mt is None:
        return False
    return mt > epoch


def _full_profile_independent_smoke(
    text: str, run_dir: Path | None = None
) -> bool:
    """True when Notes show smoke-pass (re-run) **and** Smoke-stage evidence.

    Mode full + Review profile full (verify-and-fix.md E1):

    1. Notes section must contain ``smoke-pass (re-run)`` (or equivalent).
       Do **not** accept the token anywhere else in ``00-run.md`` (Run log
       alone is forgeable).
    2. Separate Smoke-stage evidence (must **not** be satisfied solely by the
       same Notes/DONE line):

       - Run log line with stage ``smoke``, and/or
       - ``06-test-log.md`` Smoke section mtime after **Last verify-pass at**
         with Result smoke-pass

    Provenance is **not** required here (provenance is the skip-review Gate C
    escape — Mode full never uses skip-review).
    """
    notes = _notes_blob(text)
    if not SMOKE_RERUN_DONE_RE.search(notes):
        return False
    if _run_log_has_smoke_stage(text):
        return True
    if _smoke_section_after_verify_pass(text, run_dir):
        return True
    return False


def _run_log_timestamped_entries(text: str) -> list[tuple[str, str]]:
    """Return [(HH:MM, note), ...] from Run log (machine-checkable turn sep)."""
    blob = _run_log_blob(text)
    if not blob:
        return []
    return [
        (m.group(1).strip(), m.group(2).strip())
        for m in RUN_LOG_ENTRY_RE.finditer(blob)
    ]
def _artifact_exists(run_dir: Path | None, name: str) -> bool:
    if run_dir is None:
        return False
    return (run_dir / name).is_file()


def _gate_a_artifact_exists(run_dir: Path | None) -> bool:
    """True when prefer ``01a-gate-a.md`` or legacy ``01a-idea-ui-review.md`` exists."""
    return any(_artifact_exists(run_dir, n) for n in GATE_A_ARTIFACT_NAMES)


def _gate_a_both_filenames_exist(run_dir: Path | None) -> bool:
    """True when preferred and LEGACY Gate A files both exist (E9)."""
    if run_dir is None:
        return False
    return _artifact_exists(run_dir, GATE_A_ARTIFACT_PREFERRED) and _artifact_exists(
        run_dir, GATE_A_ARTIFACT_LEGACY
    )


def _read_gate_a_artifact(run_dir: Path | None) -> str:
    """Read Gate A Result artifact; prefer new name, then legacy (E5)."""
    for name in GATE_A_ARTIFACT_NAMES:
        blob = _read_artifact(run_dir, name)
        if blob:
            return blob
    return ""


def _extract_stage_token(raw: str) -> str:
    s = raw.strip().strip("`*_")
    if not s:
        return ""
    return re.split(r"[\s(/]", s)[0].strip("`*_").lower()


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


def _parse_round(blob: str) -> int | None:
    """Parse **Round:** N from an artifact body.

    Prefer a top-of-file Round (before the first ``##``) so multi-section
    ``05-review-log.md`` is reliable (invariants.md · M2). Fall back to the
    first ``**Round:**`` anywhere in the file.
    """
    if not blob:
        return None
    top = blob.split("\n## ", 1)[0]
    m = ROUND_HEADER_RE.search(top)
    if m:
        return int(m.group(1))
    m = ROUND_HEADER_RE.search(blob)
    if not m:
        return None
    return int(m.group(1))


def _parse_review_overall_result(blob: str) -> str | None:
    """Overall / worst-section Result for multi-section ``05-review-log.md``.

    Prefer top-level Result (before first ``##``). Else take the worst among
    section Results (``needs fix`` / ``has findings`` > ``pending`` > ``clean``).
    """
    if not blob:
        return None
    top = blob.split("\n## ", 1)[0]
    top_r = _parse_result_token(top)
    section_results: list[str] = []
    for m in re.finditer(
        r"(?ims)^##[^\n]+\n(.*?)(?=^## |\Z)", blob
    ):
        tok = _parse_result_token(m.group(1))
        if tok:
            section_results.append(tok)
    candidates = [t for t in ([top_r] if top_r else []) + section_results if t]
    if not candidates:
        # Legacy single Result anywhere in file
        return _parse_result_token(blob)
    return max(
        candidates,
        key=lambda t: REVIEW_RESULT_RANK.get(t, 0),
    )


def _count_fix_review_cycles(text: str) -> int:
    """Count ``fix-review`` stage lines in Run log (max-round fallback · M2)."""
    return len(FIX_REVIEW_RUN_LOG_RE.findall(_run_log_blob(text)))


def _count_run_log_stage_cycles(text: str, stage_id: str) -> int:
    """Count Run log lines whose stage column matches ``stage_id``."""
    if not stage_id:
        return 0
    pat = re.compile(
        rf"(?im)·\s*(?:done|running|paused)\s*·\s*{re.escape(stage_id)}\b"
    )
    return len(pat.findall(_run_log_blob(text)))


# Stage id → artifact for Round-stuck-at-1 warn (invariants.md · M3)
_ROUND_STUCK_CHECKS: tuple[tuple[str, str], ...] = (
    ("design-review", "03a-design-review-log.md"),
    ("design-verify-phase", "03a-design-review-log.md"),
    ("api-contract-review", "03a-api-contract-review.md"),
    ("db-design-review", "03a-db-design-review.md"),
)


def _round_stuck_at_one_warns(text: str, run_dir: Path | None) -> list[str]:
    """Warn when ≥3 same-stage Run-log cycles but artifact Round still 1.

    Cheap habit check — does not block. Parent must bump Round on re-entry
    so max-round lint can fire (invariants.md).
    """
    if run_dir is None:
        return []
    msgs: list[str] = []
    warned_artifacts: set[str] = set()
    for stage_id, artifact in _ROUND_STUCK_CHECKS:
        cycles = _count_run_log_stage_cycles(text, stage_id)
        if cycles < MAX_ROUND_CAP:
            continue
        if artifact in warned_artifacts:
            continue
        blob = _read_artifact(run_dir, artifact)
        if not blob:
            continue
        if _parse_round(blob) == 1:
            msgs.append(
                f"Run log has ≥{MAX_ROUND_CAP} `{stage_id}` cycles but "
                f"{artifact} Round still 1 — bump Round on re-entry "
                "(invariants.md)"
            )
            warned_artifacts.add(artifact)
    ga_cycles = _count_run_log_stage_cycles(text, "gate-a")
    if ga_cycles >= MAX_ROUND_CAP:
        ga = _read_gate_a_artifact(run_dir)
        if ga and _parse_round(ga) == 1:
            msgs.append(
                f"Run log has ≥{MAX_ROUND_CAP} `gate-a` cycles but 01a "
                "Round still 1 — bump Round on re-entry (invariants.md)"
            )
    return msgs


def _parse_verify_attempts(text: str) -> int | None:
    m = VERIFY_ATTEMPTS_RE.search(text)
    if not m:
        return None
    return int(m.group(1))


def _raised_max_round_cap(text: str, domain: str) -> int | None:
    """Return raised cap N for domain when Notes have quality max-round-cap.

    Shape (invariants.md): ``max-round-cap — <domain> — <N> — user: "…"``
    Quote quality matches provenance (≥12 chars, non-filler). Lint checks
    shape only — parent habit binds the quote to the latest user message.
    """
    if domain not in MAX_ROUND_CAP_DOMAINS:
        return None
    best: int | None = None
    for m in MAX_ROUND_CAP_RE.finditer(text):
        if m.group("domain").lower() != domain:
            continue
        if not _provenance_quote_ok(m.group("quote")):
            continue
        n = int(m.group("n"))
        if n < MAX_ROUND_CAP:
            continue
        if best is None or n > best:
            best = n
    return best


def _effective_max_round(text: str, domain: str) -> int:
    """Default MAX_ROUND_CAP, or raised N from max-round-cap Notes."""
    raised = _raised_max_round_cap(text, domain)
    return raised if raised is not None else MAX_ROUND_CAP


def _max_round_block_reason(text: str, run_dir: Path | None) -> str | None:
    """Return Decision N reason when a max-round cap is hit (invariants.md).

    Parent must increment Round / Run metrics after each cycle so this can fire.
    Notes ``max-round-cap — <domain> — <N> — user: "…"`` raises the effective
    cap for that domain (M2).
    """
    if run_dir is None:
        return None

    # design-review / design-verify: Round ≥ cap + needs update
    design_blob = _read_artifact(run_dir, "03a-design-review-log.md")
    if design_blob:
        d_round = _parse_round(design_blob)
        d_result = _parse_result_token(design_blob)
        d_cap = _effective_max_round(text, "design-review")
        if (
            d_round is not None
            and d_round >= d_cap
            and d_result == "needs update"
        ):
            return (
                f"design-review Round {d_round} >= {d_cap} with "
                "Result needs update — Decision N (invariants.md)"
            )

    # Gate A: Round ≥ cap + non-ok
    gate_a = _read_gate_a_artifact(run_dir)
    if gate_a:
        ga_round = _parse_round(gate_a)
        ga_result = _parse_result_token(gate_a)
        ga_cap = _effective_max_round(text, "gate-a")
        if (
            ga_round is not None
            and ga_round >= ga_cap
            and ga_result is not None
            and ga_result != "ok"
        ):
            return (
                f"Gate A Round {ga_round} >= {ga_cap} with Result "
                f"{ga_result} — Decision N (invariants.md)"
            )

    # Verify attempts ≥ cap + verify-fail
    attempts = _parse_verify_attempts(text)
    last_m = REQUIRED_FIELD_PATTERNS["Last Verify"].search(text)
    last_verify = _first_token(last_m.group(1)) if last_m else ""
    v_cap = _effective_max_round(text, "verify")
    if (
        attempts is not None
        and attempts >= v_cap
        and last_verify == "verify-fail"
    ):
        return (
            f"Verify attempts {attempts} >= {v_cap} with "
            "verify-fail — Decision N (invariants.md)"
        )

    # review Fix: Round ≥ cap on 05 with not clean, or metrics, or Run log
    # cycles when Round missing (metrics key is "review fix rounds" only —
    # not design-review rounds). Result = overall / worst-section (M2).
    review_blob = _read_artifact(run_dir, "05-review-log.md")
    r_cap = _effective_max_round(text, "review-fix")
    if review_blob:
        r_round = _parse_round(review_blob)
        r_result = _parse_review_overall_result(review_blob)
        not_clean = r_result is not None and r_result != "clean"
        if r_round is not None and r_round >= r_cap and not_clean:
            return (
                f"review Round {r_round} >= {r_cap} "
                f"(Result {r_result}) — Decision N (invariants.md)"
            )
        # Round missing: count fix-review cycles from Run log when feasible
        if r_round is None and not_clean:
            cycles = _count_fix_review_cycles(text)
            if cycles >= r_cap:
                return (
                    f"review fix-review Run log cycles {cycles} >= {r_cap} "
                    "(Round missing on 05) — Decision N (invariants.md)"
                )
    m_rev = REVIEW_FIX_ROUNDS_RE.search(text)
    if m_rev:
        if int(m_rev.group(1)) >= r_cap:
            return (
                f"review fix rounds {m_rev.group(1)} >= {r_cap} — "
                "Decision N (invariants.md)"
            )

    # test↔fix: Round ≥ cap on 06 with not success, or metrics
    test_blob = _read_artifact(run_dir, "06-test-log.md")
    if test_blob:
        t_round = _parse_round(test_blob)
        t_result = _parse_result_token(test_blob)
        t_cap = _effective_max_round(text, "test-fix")
        if (
            t_round is not None
            and t_round >= t_cap
            and t_result is not None
            and t_result not in ("success", "smoke-pass", "pending")
        ):
            return (
                f"test Round {t_round} >= {t_cap} "
                f"(Result {t_result}) — Decision N (invariants.md)"
            )
    m_tf = TEST_FIX_ROUNDS_RE.search(text)
    if m_tf:
        t_cap = _effective_max_round(text, "test-fix")
        if int(m_tf.group(1)) >= t_cap:
            return (
                f"test↔fix rounds {m_tf.group(1)} >= {t_cap} — "
                "Decision N (invariants.md)"
            )

    return None


def _read_artifact(run_dir: Path | None, name: str) -> str:
    if run_dir is None:
        return ""
    path = run_dir / name
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")
