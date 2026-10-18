"""Shared constants, parsers, and helpers for my-dev-flow lint.

Enforces field tokens and path helpers used across Gate B/C / derive /
stage-id checks. Policy SoT: hitl.md · stages.md · parent-next.md · invariants.md.
"""
from __future__ import annotations

import datetime as _dt
import re
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
def _read_artifact(run_dir: Path | None, name: str) -> str:
    if run_dir is None:
        return ""
    path = run_dir / name
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")
