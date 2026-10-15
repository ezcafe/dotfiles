#!/usr/bin/env python3
"""Lint a my-dev-flow run folder (.my-docs/workflow/<slug>/).

Checks required 00-run.md fields with exact-token enums (reject template `|`),
Status, Mode, Review profile, Gate B veto, Pending parallel, Has API/DB,
stage ids, Verify commands before Build, skip-review+API/DB error
(--before-build, --before-design-review, or --check-skip-review),
Mode full+skip-review error, Mode simple+full error, Mode full + HITL Gate B
auto/async-notify error, Mode simple + Has API/DB yes + soft Gate B error,
Mode full API∥DB Pending parallel (simple keeps none),
async Gate B gap + Build armed, Gate C approved before merge
(auto when card Next=merge, or with --before-merge).

Also:
  --next              print next incomplete stage hint + companion / handoff
                      (no Task handoff when blocked / gate-b / gate-c /
                      merge without Gate C approved)
  --before-merge      require Gate C approved actions (also auto when Next=merge)
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
ARTIFACTS_00 = PACKAGE / "artifacts" / "00-run.md"
PARENT_NEXT_MD = PACKAGE / "parent-next.md"
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
FULL_ONLY_STAGES = frozenset(
    {
        "ideation",
        "gate-a",
        "ideation-update",
        "skim",
        "analyze",
        "design",
        "design-review",
        "api-contract-review",
        "db-design-review",
        "adversarial",
        "quality",
        "test-full",
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
GATE_C_APPROVED_RE = re.compile(
    r"^[-*]?\s*\*\*Gate C approved:\*\*\s*(.+)$", re.M | re.I
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
SOFT_TASK_CAP = 20


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


def _next_stage_legality_warns(
    stage_id: str, mode_token: str | None, review_token: str | None
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
    _check_gate_c_approved(text, issues, before_merge=before_merge)

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

    if before_build or before_design_review or check_skip_review:
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


def print_next_hint(run_dir: Path) -> int:
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
    if not stage_id:
        print("hint: set Orchestrator card Next step / Stage id")
        print(f"companion: {PARENT_NEXT_MD}")
        return 0
    print(f"next incomplete stage: {stage_id}")

    for msg in _next_stage_legality_warns(stage_id, mode_token, review_token):
        print(f"warn: {msg}")

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
    if stage_id in ("gate-b", "gate-c"):
        print(f"companion: hitl.md · parent-next.md (row for `{stage_id}`)")
        print("handoff: do-not-launch")
        if stage_id == "gate-b":
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

    print(f"companion: parent-next.md (row for `{stage_id}`)")
    print(f"handoff: python {PACKAGE / 'scripts' / 'handoff-for.py'} {stage_id}")
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
        help="Enforce Has API/DB yes|no + Mode full Pending parallel + skip-review ban",
    )
    p.add_argument(
        "--before-build",
        action="store_true",
        help="Enforce Verify commands + Gate B veto none + Build armed + async gap",
    )
    p.add_argument(
        "--before-merge",
        action="store_true",
        help=(
            "Require Gate C approved actions (commit|push|pr|merge); "
            "also auto-enforced when card Next=merge"
        )
    )
    p.add_argument(
        "--check-skip-review",
        action="store_true",
        help="Error if skip-review + Has API/DB yes (also implied by --before-build / --before-design-review)",
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

    if args.next:
        return print_next_hint(args.run_dir)

    run_md = args.run_dir / "00-run.md"
    if not run_md.is_file():
        print(f"error: missing {run_md}", file=sys.stderr)
        return 2

    text = run_md.read_text(encoding="utf-8")
    issues = lint_run_md(
        text,
        before_design_review=args.before_design_review,
        before_build=args.before_build,
        check_skip_review=args.check_skip_review,
        before_merge=args.before_merge,
        run_dir=args.run_dir,
    )

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
