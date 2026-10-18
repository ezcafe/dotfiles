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
    r"(?i)\bsmoke\s*-?\s*waive\b|\bwaive\s+(?:independent\s+)?smoke\b"
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
    r"(?i)\bgate-c-test-override\b|\bGate C test override\b"
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
def _artifact_exists(run_dir: Path | None, name: str) -> bool:
    if run_dir is None:
        return False
    return (run_dir / name).is_file()
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
