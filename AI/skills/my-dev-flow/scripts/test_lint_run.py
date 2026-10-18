#!/usr/bin/env python3
"""Unit tests for lint-run.py — run from this directory:

  python3 -m pytest test_lint_run.py -q
  # or
  python3 -m unittest test_lint_run.py
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
import tempfile
import time
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    path = SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # required for dataclasses on Python 3.9
    spec.loader.exec_module(mod)
    return mod


lint_run = _load("lint_run", "lint-run.py")
handoff_for = _load("handoff_for", "handoff-for.py")
lint_run_md = lint_run.lint_run_md


def _prov(kind: str, quote: str = "fixture yes proceed") -> str:
    return f'- provenance — {kind} — user: "{quote}"'


def _async_armed_notes_and_log(
    *,
    digest_ts: str = "14:00",
    arm_ts: str = "14:05",
) -> tuple[str, str]:
    """Notes + Run log for a complete async Gate B turn-boundary gap."""
    notes = (
        "- async-notify posted — veto window open until Build starts\n"
        "- Build armed\n"
        f"- async-gap-pending — {digest_ts}"
    )
    run_log = (
        f"- **{digest_ts}** · paused · gate-b · async-notify posted — "
        "veto window open\n"
        f"- **{arm_ts}** · paused · gate-b · Build armed"
    )
    return notes, run_log


def _write_async_gap_sidecar(run_dir: Path, digest_ts: str = "14:00") -> None:
    (run_dir / ".lint-async-gap").write_text(f"{digest_ts}\n", encoding="utf-8")


def _base(
    *,
    status: str = "running",
    mode: str = "simple",
    review: str = "lite",
    veto: str = "none",
    has_api: str = "no",
    has_db: str = "no",
    pending_parallel: str | None = "none",
    last_verify: str = "pending",
    last_verify_pass_at: str | None = None,
    notes: str = "- ok",
    task_count: str = "1",
    next_step: str = "design-phase",
    stage_id: str = "design-phase",
    verify: bool = True,
    hitl_gate_b: str | None = None,
    gate_b_approved: str | None = None,
    gate_c_approved: str = "none",
    lens_plan: str = "none",
    clarity_ok: bool = True,
    run_log: str | None = None,
    auto_provenance: bool = True,
) -> str:
    if hitl_gate_b is None:
        hitl_gate_b = "blocking" if mode == "full" else "auto"
    if gate_b_approved is None:
        # Blocking Gate B needs durable yes before Build; keep fixtures green
        gate_b_approved = "yes" if hitl_gate_b == "blocking" else "none"
    # Soft: presence-any; hard (tdd-review/build/fix-*/merge): boundary-matched
    if clarity_ok and not re.search(r"(?i)clarity-check\s+ok", notes):
        boundary = (
            next_step
            if next_step in lint_run.CLARITY_CHECK_STAGES
            else "build"
        )
        notes = f"{notes}\n- clarity-check ok — {boundary}"
    if auto_provenance:
        # Inject provenance so green fixtures stay green under R1
        if (
            hitl_gate_b == "blocking"
            and gate_b_approved
            and gate_b_approved.lower() not in ("none", "")
            and "gate-b-approved" not in notes
        ):
            notes = f"{notes}\n{_prov('gate-b-approved')}"
        if (
            gate_c_approved
            and gate_c_approved.lower() not in ("none", "")
            and "gate-c-approved" not in notes
        ):
            notes = f"{notes}\n{_prov('gate-c-approved')}"
        if re.search(r"(?i)gate-c-test-override", notes) and (
            "provenance — gate-c-test-override" not in notes.lower()
        ):
            notes = f"{notes}\n{_prov('gate-c-test-override', 'waive green tests now')}"
        if re.search(r"(?i)smoke\s*-?\s*waive", notes) and (
            "provenance — smoke-waive" not in notes.lower()
        ):
            notes = f"{notes}\n{_prov('smoke-waive', 'waive independent smoke check')}"
        if re.search(r"(?i)\bdocs-only\b", notes) and (
            "provenance — docs-only" not in notes.lower()
        ):
            notes = f"{notes}\n{_prov('docs-only', 'docs-only copy tweak only')}"
        if re.search(r"(?i)smoke-pass\s*\(\s*re-?run\s*\)", notes) and (
            "provenance — smoke-pass-rerun" not in notes.lower()
        ):
            notes = f"{notes}\n{_prov('smoke-pass-rerun', 'smoke re-run already passed')}"
        if re.search(r"(?i)card-override", notes) and (
            "provenance — card-override" not in notes.lower()
        ):
            notes = f"{notes}\n{_prov('card-override', 'user insisted on this next')}"
    if run_log is None:
        run_log = f"- **12:00** · running · {stage_id} · fixture"
    pp = (
        f"**Pending parallel:** {pending_parallel}\n"
        if pending_parallel is not None
        else ""
    )
    verify_block = (
        """**Verify commands:** (required before Build)
- **cwd:** /tmp/repo
- **build:** npm run build
- **unit:** npm test
- **e2e:** N/A — none

"""
        if verify
        else ""
    )
    return f"""# Workflow run: test-slug

## Required

**Status:** {status}

**Mode:** {mode}

**Complexity:** test fixture

**Slug:** `20261013-test`

**Review profile:** {review}

**Lens plan:** {lens_plan}

{verify_block}**Last Verify:** {last_verify}
**Last verify-pass at:** {last_verify_pass_at if last_verify_pass_at is not None else "none"}
**Verify attempts:** 0

**Gate B veto:** {veto}

**Gate B approved:** {gate_b_approved}

**Gate C approved:** {gate_c_approved}

{pp}**Last stage:** {stage_id}

**Run metrics:**
- Task count: {task_count}
- verify-fail count: 0
- main-thread fallbacks: 0

## Optional / when known

### Repo

- **Has UI:** no
- **Has API:** {has_api}
- **Has DB:** {has_db}
- **HITL Gate B:** {hitl_gate_b}
- **HITL Grill:** auto
- **HITL Gate C:** blocking

### Orchestrator card (parent — avoid re-ingest)

| Field | Value |
|-------|-------|
| Phase | design |
| Stage id | {stage_id} |
| Next step | {next_step} |
| Task description | test |
| Model tier | Fast |
| Last Verify | {last_verify} |
| Gate B veto | {veto} |

### Notes

{notes}

### Run log

{run_log}
"""


def _errors(issues) -> list[str]:
    return [i.message for i in issues if i.severity == "error"]


def _warns(issues) -> list[str]:
    return [i.message for i in issues if i.severity == "warn"]


def _write_03a_clean(run_dir: Path) -> None:
    (run_dir / "03a-design-review-log.md").write_text(
        "**Result:** clean\n", encoding="utf-8"
    )


class TestLintRun(unittest.TestCase):
    def test_legal_skip_review(self):
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="build",
            stage_id="build",
            notes="- clarity-check ok — build",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                check_skip_review=True,
                run_dir=run_dir,
            )
            self.assertEqual(_errors(issues), [])

    def test_illegal_skip_review_plus_api(self):
        text = _base(review="skip-review", has_api="yes", has_db="no")
        issues = lint_run_md(
            text, before_design_review=False, before_build=True, check_skip_review=True
        )
        self.assertTrue(
            any("skip-review not allowed when Has API" in e for e in _errors(issues))
        )

    def test_illegal_skip_review_before_design_review(self):
        text = _base(review="skip-review", has_api="yes", has_db="no")
        issues = lint_run_md(
            text, before_design_review=True, before_build=False, check_skip_review=False
        )
        self.assertTrue(
            any("skip-review not allowed when Has API" in e for e in _errors(issues))
        )

    def test_mode_full_skip_review(self):
        text = _base(mode="full", review="skip-review", has_api="no", has_db="no")
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("Mode full + Review profile skip-review" in e for e in _errors(issues))
        )

    def test_mode_simple_full_review(self):
        text = _base(mode="simple", review="full", has_api="no", has_db="no")
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("Mode simple + Review profile full" in e for e in _errors(issues))
        )

    def test_bad_status_as_stage(self):
        text = _base(status="build")
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("stage/bucket" in e or "Status must be one of" in e for e in _errors(issues))
        )

    def test_gate_b_veto_pending_before_build(self):
        text = _base(veto="pending")
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertTrue(
            any("Gate B veto is pending" in e for e in _errors(issues))
        )

    def test_pending_parallel_required_before_design_review(self):
        text = _base(
            mode="full",
            review="full",
            has_api="yes",
            has_db="yes",
            pending_parallel=None,
        )
        issues = lint_run_md(
            text, before_design_review=True, before_build=False
        )
        self.assertTrue(
            any("Pending parallel missing" in e for e in _errors(issues))
        )

    def test_pending_parallel_one_present_api_db_warn_only(self):
        """T1: default lint — one 03a-* + api|db = valid resume serialize (warn, not error)."""
        text = _base(
            mode="full",
            review="full",
            has_api="yes",
            has_db="yes",
            pending_parallel="api|db",
            stage_id="api-contract-review",
            next_step="db-design-review",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03a-api-contract-review.md").write_text("ok", encoding="utf-8")
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("without" in e for e in _errors(issues)),
                msg=_errors(issues),
            )
            self.assertFalse(
                any("Pending parallel" in e for e in _errors(issues)),
                msg=_errors(issues),
            )
            self.assertTrue(
                any(
                    "resume serialize" in w and "finish the other" in w
                    for w in _warns(issues)
                ),
                msg=_warns(issues),
            )

    def test_pending_parallel_one_present_none_errors(self):
        """T1: one 03a-* + Pending parallel none → error (must keep api|db)."""
        text = _base(
            mode="full",
            review="full",
            has_api="yes",
            has_db="yes",
            pending_parallel="none",
            stage_id="api-contract-review",
            next_step="db-design-review",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03a-api-contract-review.md").write_text("ok", encoding="utf-8")
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("without" in e and "03a-db" in e for e in _errors(issues)),
                msg=_errors(issues),
            )

    def test_pending_parallel_none_when_both_needed_errors(self):
        text = _base(
            mode="full",
            review="full",
            has_api="yes",
            has_db="yes",
            pending_parallel="none",
        )
        issues = lint_run_md(
            text, before_design_review=True, before_build=False
        )
        self.assertTrue(
            any("Pending parallel is none" in e for e in _errors(issues))
        )

    def test_pending_parallel_tiny_tweak_skips(self):
        text = _base(
            mode="full",
            review="full",
            has_api="yes",
            has_db="yes",
            pending_parallel="none",
            notes="- tiny-contract-tweak — Notes fold into Quality / code-review-phase",
        )
        issues = lint_run_md(
            text, before_design_review=True, before_build=False
        )
        self.assertFalse(
            any("Pending parallel" in e for e in _errors(issues))
        )

    def test_mode_simple_both_api_db_pending_none_clean(self):
        """Mode simple + both yes + pending none must stay clean (--before-design-review)."""
        text = _base(
            mode="simple",
            review="lite",
            has_api="yes",
            has_db="yes",
            pending_parallel="none",
        )
        issues = lint_run_md(
            text, before_design_review=True, before_build=False
        )
        self.assertFalse(
            any("Pending parallel" in e for e in _errors(issues))
        )
        self.assertFalse(
            any("Pending parallel" in w for w in _warns(issues))
        )

    def test_mode_simple_pending_api_db_warns(self):
        text = _base(
            mode="simple",
            review="lite",
            has_api="yes",
            has_db="yes",
            pending_parallel="api|db",
        )
        issues = lint_run_md(
            text, before_design_review=True, before_build=False
        )
        self.assertFalse(
            any("Pending parallel is none" in e for e in _errors(issues))
        )
        self.assertFalse(
            any("Pending parallel missing" in e for e in _errors(issues))
        )
        self.assertTrue(
            any(
                "Mode simple" in w and "Pending parallel" in w
                for w in _warns(issues)
            )
        )

    def test_veto_window_open_while_running_errors(self):
        text = _base(
            status="running",
            notes="- async-notify posted — veto window open until Build starts",
            next_step="build",
            stage_id="build",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertTrue(
            any("veto window open" in e for e in _errors(issues))
        )

    def test_veto_window_without_build_armed_errors(self):
        text = _base(
            status="paused",
            notes="- async-notify posted — veto window open until Build starts",
            next_step="build",
            stage_id="gate-b",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertTrue(
            any("Build armed" in e for e in _errors(issues))
        )

    def test_veto_window_with_build_armed_ok_for_armed_rule(self):
        notes, run_log = _async_armed_notes_and_log()
        text = _base(
            status="paused",
            notes=notes,
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            run_log=run_log,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            _write_async_gap_sidecar(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertFalse(
            any("Build armed" in e for e in _errors(issues))
        )
        self.assertFalse(
            any("async-notify Gate B:" in e for e in _errors(issues))
        )

    def test_async_gap_invented_parent_turn_gap_errors(self):
        """R2: inventing parent turn gap observed without turn-boundary → error."""
        text = _base(
            status="paused",
            notes=(
                "- async-notify posted — veto window open until Build starts\n"
                "- Build armed\n"
                "- parent turn gap observed"
            ),
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            run_log="- **14:00** · paused · gate-b · fixture only",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertTrue(
            any("async-notify Gate B:" in e for e in _errors(issues))
        )

    def test_async_gap_same_turn_dual_hhmm_without_pending_errors(self):
        """S2: distinct HH:MM alone without async-gap-pending → error."""
        text = _base(
            status="paused",
            notes=(
                "- async-notify posted — veto window open until Build starts\n"
                "- Build armed"
            ),
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            run_log=(
                "- **14:00** · paused · gate-b · async-notify posted — veto window open\n"
                "- **14:05** · paused · gate-b · Build armed"
            ),
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            _write_async_gap_sidecar(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertTrue(
            any("async-gap-pending" in e or "async-notify Gate B:" in e for e in _errors(issues))
        )

    def test_async_gap_arm_not_later_than_digest_errors(self):
        """S2: arm HH:MM not strictly later than digest → error."""
        notes, _ = _async_armed_notes_and_log(digest_ts="14:05", arm_ts="14:00")
        # Force arm earlier than digest in run log
        run_log = (
            "- **14:05** · paused · gate-b · async-notify posted — veto window open\n"
            "- **14:00** · paused · gate-b · Build armed"
        )
        notes = (
            "- async-notify posted — veto window open until Build starts\n"
            "- Build armed\n"
            "- async-gap-pending — 14:05"
        )
        text = _base(
            status="paused",
            notes=notes,
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            run_log=run_log,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            _write_async_gap_sidecar(run_dir, "14:05")
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertTrue(
            any("async-notify Gate B:" in e for e in _errors(issues))
        )

    def test_async_gap_default_lint_next_build_errors(self):
        """S1: default lint with Next=build enforces async gap (parity)."""
        text = _base(
            status="paused",
            notes=(
                "- async-notify posted — veto window open until Build starts\n"
                "- Build armed"
            ),
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            run_log=(
                "- **14:00** · paused · gate-b · async-notify posted — veto window open\n"
                "- **14:05** · paused · gate-b · Build armed"
            ),
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                run_dir=run_dir,
            )
        self.assertTrue(
            any("async-notify Gate B:" in e for e in _errors(issues))
        )

    def test_task_count_soft_cap_warn(self):
        text = _base(mode="full", review="full", task_count="25", status="running")
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("soft cap" in w for w in _warns(issues))
        )

    def test_main_thread_fallbacks_soft_pause_warn(self):
        text = _base(status="running")
        text = text.replace("main-thread fallbacks: 0", "main-thread fallbacks: 3")
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("main-thread fallbacks" in w and "Decision N" in w for w in _warns(issues))
        )


class TestHandoffFor(unittest.TestCase):
    def test_handoff_for_build(self):
        rows = handoff_for._parse_stage_table(
            handoff_for.HANDOFFS.read_text(encoding="utf-8")
        )
        self.assertIn("build", rows)
        self.assertIn("00-run.md", rows["build"][0])
        self.assertIn("verify-pass", rows["build"][1])
        self.assertIn("verify-fail", rows["build"][1])
        self.assertIn("design-phase", rows)
        self.assertIn("merge", rows)

    def test_handoff_for_skill_root_absolute_paths(self):
        from io import StringIO
        import contextlib

        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            # Simulate CLI via main pieces
            skill_root = handoff_for.PACKAGE
            handoffs_path = skill_root / "handoffs.md"
            rows = handoff_for._parse_stage_table(
                handoffs_path.read_text(encoding="utf-8")
            )
            self.assertIn("build", rows)
            block = handoff_for.BASE_BLOCK.format(
                slug="s",
                stage_id="build",
                write_list="code + Smoke section",
                size_caps_path=str(skill_root / "size-caps.md"),
                skills_path_path=str(skill_root / "skills-path.md"),
                severity_path=str(skill_root / "severity.md"),
            )
            self.assertIn(str(skill_root / "size-caps.md"), block)
            self.assertTrue(str(skill_root).startswith("/"))


class TestValidStageIdsSync(unittest.TestCase):
    def test_valid_stage_ids_match_handoffs(self):
        from_h = lint_run.stage_ids_from_handoffs()
        self.assertEqual(
            lint_run.VALID_STAGE_IDS,
            from_h,
            msg=(
                "VALID_STAGE_IDS drift vs handoffs.md — "
                f"only_in_lint={sorted(lint_run.VALID_STAGE_IDS - from_h)} "
                f"only_in_handoffs={sorted(from_h - lint_run.VALID_STAGE_IDS)}"
            ),
        )

    def test_check_stage_id_registry_clean(self):
        issues = lint_run.check_stage_id_registry()
        self.assertEqual(
            issues,
            [],
            msg="; ".join(f"{i.severity}: {i.message}" for i in issues),
        )

    def test_check_stage_ids_cli_exit_0_when_clean(self):
        """T3: --check-stage-ids loads handoff-for.py via importlib; exit 0 when clean."""
        import subprocess

        rc = subprocess.run(
            [sys.executable, str(SCRIPTS / "lint-run.py"), "--check-stage-ids"],
            cwd=str(SCRIPTS),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            rc.returncode,
            0,
            msg=f"stdout={rc.stdout!r} stderr={rc.stderr!r}",
        )
        self.assertIn("ok: stage-id registry aligned", rc.stdout)
        self.assertNotIn("could not check Task description map", rc.stdout)


class TestHitlGateBAndGateC(unittest.TestCase):
    def test_mode_full_async_notify_gate_b_errors(self):
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="async-notify",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any(
                "Mode full + HITL Gate B" in e and "async-notify" in e
                for e in _errors(issues)
            )
        )

    def test_mode_full_auto_gate_b_errors(self):
        text = _base(mode="full", review="full", hitl_gate_b="auto")
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("Mode full + HITL Gate B" in e for e in _errors(issues))
        )

    def test_mode_full_blocking_gate_b_ok(self):
        text = _base(mode="full", review="full", hitl_gate_b="blocking")
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("HITL Gate B" in e for e in _errors(issues))
        )

    def test_mode_simple_api_yes_soft_gate_b_errors(self):
        text = _base(
            mode="simple",
            review="lite",
            has_api="yes",
            hitl_gate_b="async-notify",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any(
                "Has API/DB yes" in e and "non-blocking" in e
                for e in _errors(issues)
            )
        )
        self.assertFalse(
            any(
                "Has API/DB yes" in w and "non-blocking" in w
                for w in _warns(issues)
            )
        )

    def test_mode_simple_api_yes_soft_gate_b_before_build_errors(self):
        text = _base(
            mode="simple",
            review="lite",
            has_api="yes",
            hitl_gate_b="auto",
            next_step="build",
            stage_id="gate-b",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertTrue(
            any(
                "Has API/DB yes" in e and "non-blocking" in e
                for e in _errors(issues)
            )
        )

    def test_before_merge_requires_gate_c_approved(self):
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="none",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=True,
        )
        self.assertTrue(
            any("Gate C approved" in e for e in _errors(issues))
        )

    def test_default_lint_next_merge_requires_gate_c_approved(self):
        """N2: plain lint errors when Next=merge and approved is none."""
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="none",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=False,
        )
        self.assertTrue(
            any("Gate C approved" in e for e in _errors(issues))
        )

    def test_default_lint_non_merge_allows_gate_c_none(self):
        text = _base(
            next_step="test-lite",
            stage_id="code-review-phase",
            gate_c_approved="none",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=False,
        )
        self.assertFalse(
            any("Gate C approved" in e for e in _errors(issues))
        )

    def test_before_merge_with_approved_actions_ok(self):
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            notes="- gate-c-test-override — fixture waive",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=True,
        )
        self.assertFalse(
            any("Gate C approved" in e for e in _errors(issues))
        )
        self.assertFalse(
            any("Gate C test bar" in e for e in _errors(issues))
        )

    def test_default_lint_next_merge_with_approved_ok(self):
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push",
            notes="- gate-c-test-override — fixture waive",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=False,
        )
        self.assertFalse(
            any("Gate C approved" in e for e in _errors(issues))
        )


class TestStatusDoneRequiresMerge(unittest.TestCase):
    """E2: Status=done requires merge ∈ Gate C approved."""

    def test_status_done_without_merge_errors(self):
        text = _base(
            status="done",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="commit,push,pr",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any(
                "Status=done requires merge" in e for e in _errors(issues)
            )
        )

    def test_status_done_with_merge_ok(self):
        text = _base(
            status="done",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="commit,push,pr,merge",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("Status=done requires merge" in e for e in _errors(issues))
        )

    def test_status_paused_pr_only_ok(self):
        text = _base(
            status="paused",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="commit,push,pr",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("Status=done requires merge" in e for e in _errors(issues))
        )


class TestGateBApprovedAndSkipReviewDefault(unittest.TestCase):
    """H1/E2/E5: Gate B approved; M1: skip-review on default lint."""

    def test_blocking_gate_b_approved_none_before_build_errors(self):
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            next_step="build",
            stage_id="gate-b",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertTrue(
            any("Gate B approved" in e for e in _errors(issues))
        )

    def test_blocking_gate_b_approved_yes_before_build_ok(self):
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            next_step="build",
            stage_id="gate-b",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertFalse(
            any("Gate B approved" in e for e in _errors(issues))
        )

    def test_auto_gate_b_allows_none_approved(self):
        text = _base(
            mode="simple",
            review="lite",
            hitl_gate_b="auto",
            gate_b_approved="none",
            next_step="build",
            stage_id="gate-b",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertFalse(
            any("Gate B approved" in e for e in _errors(issues))
        )

    def test_default_lint_skip_review_plus_api_errors(self):
        """M1: default lint (no --check-skip-review) bans skip-review+API."""
        text = _base(review="skip-review", has_api="yes", has_db="no")
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            check_skip_review=False,
        )
        self.assertTrue(
            any("skip-review not allowed when Has API" in e for e in _errors(issues))
        )

    def test_print_next_hint_blocking_without_gate_b_approved(self):
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            next_step="build",
            stage_id="gate-b",
            status="paused",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            # H4: Gate A fail-closed needs 01a ok before later stages
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** ok\n", encoding="utf-8"
            )
            _write_03a_clean(run_dir)
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Gate B approved", out)

    def test_design_backloop_recovery_next_warns(self):
        """N5: design-backloop + Next design-update → warn recovery (not error)."""
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            next_step="design-update",
            stage_id="build",
            notes="- design-backloop\n- prior Gate B invalid",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("design-backloop" in e for e in _errors(issues))
        )
        self.assertTrue(
            any(
                "design-backloop" in w and "recovery in progress" in w
                for w in _warns(issues)
            )
        )

    def test_design_backloop_next_build_errors(self):
        """N5: design-backloop + Next=build → error even without --before-build."""
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            next_step="build",
            stage_id="design-update",
            notes="- design-backloop\n- prior Gate B invalid",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("design-backloop" in e for e in _errors(issues))
        )

    def test_design_backloop_soft_gate_b_before_build_errors(self):
        """N5: auto + design-backloop → error under --before-build."""
        text = _base(
            mode="simple",
            review="lite",
            hitl_gate_b="auto",
            gate_b_approved="none",
            next_step="design-update",
            stage_id="design-update",
            notes="- design-backloop\n- prior Gate B invalid",
            has_api="no",
            has_db="no",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertTrue(
            any("design-backloop" in e for e in _errors(issues))
        )

    def test_design_backloop_gate_b_next_warns(self):
        """N5: design-backloop + Next gate-b → warn recovery (settle path)."""
        text = _base(
            mode="simple",
            review="lite",
            hitl_gate_b="auto",
            gate_b_approved="none",
            next_step="gate-b",
            stage_id="design-verify-phase",
            notes="- design-backloop\n- prior Gate B invalid",
            has_api="no",
            has_db="no",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("design-backloop" in e for e in _errors(issues))
        )
        self.assertTrue(
            any("recovery in progress" in w for w in _warns(issues))
        )

    def test_design_backloop_next_redirects_build_to_design_update(self):
        """H1: --next with design-backloop + Next build → redirect / do-not-launch."""
        text = _base(
            mode="simple",
            review="lite",
            hitl_gate_b="auto",
            gate_b_approved="none",
            next_step="build",
            stage_id="design-update",
            notes="- design-backloop\n- prior Gate B invalid",
            has_api="no",
            has_db="no",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("design-update", out)
            self.assertIn("do not Build", out)

    def test_design_backloop_next_gate_b_allows_settle(self):
        """H1: --next with design-backloop + Next gate-b → digest/settle, no redirect."""
        text = _base(
            mode="simple",
            review="lite",
            hitl_gate_b="auto",
            gate_b_approved="none",
            next_step="gate-b",
            stage_id="design-verify-phase",
            notes="- design-backloop\n- prior Gate B invalid",
            has_api="no",
            has_db="no",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("settle while design-backloop", out)
            self.assertNotIn("Next should be design-update", out)
            self.assertNotIn("set Next design-update", out)
            # Must not claim gate-b should become design-update
            self.assertIn("next incomplete stage: gate-b", out)

    def test_design_backloop_cleared_after_reapprove_ok(self):
        """H1/M2: after re-settle, clear Notes token (blocking sets approved)."""
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            next_step="build",
            stage_id="gate-b",
            notes="- Gate B re-approved after design update",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertFalse(
            any("design-backloop" in e for e in _errors(issues))
        )

    def test_design_backloop_cleared_auto_approved_none_ok(self):
        """M2: auto settle clears token; approved may stay none."""
        text = _base(
            mode="simple",
            review="lite",
            hitl_gate_b="auto",
            gate_b_approved="none",
            next_step="build",
            stage_id="gate-b",
            notes="- Gate B digest settled after design-update",
            has_api="no",
            has_db="no",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertFalse(
            any("design-backloop" in e for e in _errors(issues))
        )


class TestLensPlanAndSmokeSkipReview(unittest.TestCase):
    """M3/M4/E5: Lens plan api/db; smoke re-run under skip-review."""

    def test_before_code_review_requires_api_in_lens_plan(self):
        text = _base(
            mode="simple",
            review="lite",
            has_api="yes",
            lens_plan="none",
            next_step="code-review-phase",
            stage_id="build",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_code_review=True,
        )
        self.assertTrue(
            any("Lens plan missing" in e and "api" in e for e in _errors(issues))
        )

    def test_before_code_review_ok_with_api_lens(self):
        text = _base(
            mode="simple",
            review="lite",
            has_api="yes",
            lens_plan="api",
            next_step="code-review-phase",
            stage_id="build",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_code_review=True,
        )
        self.assertFalse(
            any("Lens plan" in e for e in _errors(issues))
        )

    def test_tiny_tweak_skips_lens_plan_api_db(self):
        text = _base(
            mode="simple",
            review="lite",
            has_api="yes",
            has_db="yes",
            lens_plan="none",
            notes="- tiny-contract-tweak — Notes fold into Quality / code-review-phase",
            next_step="code-review-phase",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_code_review=True,
        )
        self.assertFalse(
            any("Lens plan" in e for e in _errors(issues))
        )

    def test_default_lint_next_adversarial_requires_lens_plan(self):
        text = _base(
            mode="full",
            review="full",
            has_api="yes",
            has_db="yes",
            lens_plan="none",
            next_step="adversarial",
            stage_id="build",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("Lens plan missing" in e for e in _errors(issues))
        )

    def test_skip_review_smoke_without_notes_warns(self):
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="smoke",
            stage_id="build",
            notes="- ok",
        )
        warns = lint_run._next_stage_legality_warns(
            "smoke", "simple", "skip-review", notes="- ok"
        )
        self.assertTrue(any("smoke" in w and "smoke re-run" in w for w in warns))

    def test_skip_review_smoke_with_notes_allowed(self):
        notes = "- smoke re-run — one independent Smoke Task"
        warns = lint_run._next_stage_legality_warns(
            "smoke", "simple", "skip-review", notes=notes
        )
        self.assertFalse(any("smoke" in w for w in warns))


class TestModeSimpleFullOnlyStages(unittest.TestCase):
    """M6: grill (and full-only peers) illegal under Mode simple --next."""

    def test_grill_in_full_only_stages(self):
        self.assertIn("grill", lint_run.FULL_ONLY_STAGES)

    def test_print_next_hint_grill_warns_on_simple(self):
        text = _base(
            mode="simple",
            review="lite",
            next_step="grill",
            stage_id="design-phase",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("warn:", out)
            self.assertIn("grill", out)


class TestNextAndDryRun(unittest.TestCase):
    def test_print_next_hint(self):
        text = _base(next_step="design-phase", stage_id="ideation", status="running")
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            rc = lint_run.print_next_hint(run_dir)
            self.assertEqual(rc, 0)

    def test_print_next_hint_blocked_async_omits_handoff(self):
        text = _base(
            status="paused",
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            notes="- async-notify posted — veto window open until Build starts",
            run_log=(
                "- **14:00** · paused · gate-b · async-notify posted — "
                "veto window open"
            ),
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            _write_03a_clean(run_dir)
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Build armed", out)
            self.assertIn("async-gap-pending — 14:00", out)
            self.assertTrue((run_dir / ".lint-async-gap").is_file())
            self.assertNotIn("handoff-for.py build", out)

    def test_print_next_hint_async_armed_incomplete_gap_do_not_launch(self):
        """S1: --next with Build armed but incomplete gap → do-not-launch."""
        text = _base(
            status="paused",
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            notes=(
                "- async-notify posted — veto window open until Build starts\n"
                "- Build armed"
            ),
            run_log=(
                "- **14:00** · paused · gate-b · async-notify posted — "
                "veto window open\n"
                "- **14:05** · paused · gate-b · Build armed"
            ),
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            _write_03a_clean(run_dir)
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("async Gate B gap incomplete", out)
            self.assertNotIn("handoff-for.py build", out)

    def test_print_next_hint_async_gap_complete_emits_handoff(self):
        """S1/S2: complete turn-boundary gap → handoff build."""
        notes, run_log = _async_armed_notes_and_log()
        text = _base(
            status="paused",
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="async-notify",
            gate_b_approved="none",
            notes=notes,
            run_log=run_log,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            _write_03a_clean(run_dir)
            _write_async_gap_sidecar(run_dir)
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("handoff-for.py build", out)
            self.assertNotIn("handoff: do-not-launch", out)

    def test_print_next_hint_gate_b_no_task_handoff(self):
        text = _base(next_step="gate-b", stage_id="design-verify-phase")
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertNotIn("handoff-for.py gate-b", out)

    def test_print_next_hint_merge_without_gate_c_no_handoff(self):
        """N1: Next=merge + Gate C approved none → do-not-launch."""
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="none",
            status="paused",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Gate C approved", out)
            self.assertNotIn("handoff-for.py merge", out)

    def test_print_next_hint_merge_with_gate_c_emits_handoff(self):
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            status="paused",
            notes="- gate-c-test-override — fixture waive",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("handoff-for.py merge", out)
            self.assertNotIn("handoff: do-not-launch", out)

    def test_print_next_hint_status_done_do_not_launch(self):
        """E3: Status done → handoff do-not-launch (no Task)."""
        text = _base(
            status="done",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="commit,push,pr,merge",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("run finished", out.lower())
            self.assertNotIn("handoff-for.py", out)

    def test_print_next_hint_status_stopped_do_not_launch(self):
        """E3: Status stopped → handoff do-not-launch (no Task)."""
        text = _base(
            status="stopped",
            next_step="build",
            stage_id="build",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("stopped", out.lower())
            self.assertNotIn("handoff-for.py", out)

    def test_print_next_hint_mode_profile_illegality_warn(self):
        text = _base(
            mode="simple",
            review="lite",
            next_step="adversarial",
            stage_id="build",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("warn:", out)
            self.assertIn("adversarial", out)

    def test_dry_run_seed(self):
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            slug_dir = parent / "20261013-dry-run-fixture"
            rc = lint_run.dry_run_seed(slug_dir, slug=None)
            self.assertEqual(rc, 0)
            self.assertTrue((slug_dir / "00-run.md").is_file())


class TestGateCTestBar(unittest.TestCase):
    """R2: Gate C test bar from hitl.md via --before-merge / Next=merge."""

    def test_lite_bar_requires_success(self):
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("Gate C test bar (lite)" in e for e in _errors(issues))
            )

    def test_lite_bar_ok_with_success_log(self):
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            last_verify="verify-pass",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Result:** success\n**Mode last run:** lite\n"
                "**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("Gate C test bar" in e for e in _errors(issues))
            )

    def test_lite_bar_fail_closed_without_mode_last_run(self):
        """N4: Result success without Mode last run → Gate C bar fail."""
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            last_verify="verify-pass",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Result:** success\n"
                "**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("Gate C test bar (lite)" in e for e in _errors(issues))
            )

    def test_full_bar_fail_closed_mismatched_mode(self):
        """N4: Mode last run lite when profile full → fail."""
        text = _base(
            mode="full",
            review="full",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Result:** success\n**Mode last run:** lite\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("Gate C test bar (full)" in e for e in _errors(issues))
            )

    def test_skip_review_bar_needs_verify_and_smoke(self):
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="pending",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            errs = _errors(issues)
            self.assertTrue(any("verify-pass" in e for e in errs))
            self.assertTrue(any("smoke-pass" in e for e in errs))

    def test_skip_review_bar_ok(self):
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Result:** smoke-pass\n"
                "**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("Gate C test bar" in e for e in _errors(issues))
            )

    def test_override_waives_bar(self):
        text = _base(
            review="full",
            mode="full",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            notes="- gate-c-test-override — user waived",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=True,
        )
        self.assertFalse(
            any("Gate C test bar" in e for e in _errors(issues))
        )

    def test_before_merge_errors_on_review_stale(self):
        """H1: review-stale blocks --before-merge even when 06 success present."""
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            last_verify="verify-pass",
            notes="- review-stale — rebuild invalidated prior review",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Result:** success\n**Mode last run:** lite\n"
                "**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("review-stale" in e for e in _errors(issues))
            )
            self.assertFalse(
                any("Gate C test bar" in e for e in _errors(issues))
            )

    def test_before_merge_errors_on_test_stale(self):
        """H1: test-stale blocks --before-merge even when 06 success present."""
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            last_verify="verify-pass",
            notes="- test-stale — rebuild invalidated prior test",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Result:** success\n**Mode last run:** lite\n"
                "**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("test-stale" in e for e in _errors(issues))
            )

    def test_stale_not_waived_by_gate_c_override(self):
        """H1: gate-c-test-override does not clear review-stale/test-stale."""
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            notes=(
                "- gate-c-test-override — user waived\n"
                "- review-stale — still invalid"
            ),
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=True,
        )
        self.assertTrue(any("review-stale" in e for e in _errors(issues)))
        self.assertFalse(
            any("Gate C test bar" in e for e in _errors(issues))
        )

    def test_skip_review_build_only_smoke_errors(self):
        """E5/R7: skip-review + Build-writes-Smoke only → error on --before-merge."""
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Result:** smoke-pass\n"
                "**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(any("Gate C test bar" in e for e in _errors(issues)))
            self.assertTrue(
                any("Build-writes-Smoke" in e for e in _errors(issues))
            )

    def test_skip_review_docs_only_smoke_warns(self):
        """R7/S5: docs-only + provenance → warn/allow for Build-only smoke."""
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            notes="- docs-only — copy tweak",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("Build-writes-Smoke" in e for e in _errors(issues))
            )
            self.assertTrue(
                any("docs-only" in w for w in _warns(issues))
            )

    def test_skip_review_docs_only_without_provenance_errors(self):
        """S5: bare docs-only Notes without provenance → error."""
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            notes=(
                "- docs-only — copy tweak\n"
                + _prov("gate-c-approved", "merge this docs-only change")
            ),
            auto_provenance=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("docs-only" in e and "provenance" in e for e in _errors(issues))
            )

    def test_skip_review_smoke_waive_no_error(self):
        """E5: Notes smoke-waive clears fail-closed Build-only smoke error."""
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            notes="- smoke-waive — user accepts Build-writes-Smoke",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("Build-writes-Smoke" in e for e in _errors(issues)),
                "smoke-waive must clear fail-closed Build-writes-Smoke error",
            )

    def test_skip_review_smoke_rerun_done_no_error(self):
        """E5: smoke-pass (re-run) evidence clears fail-closed Build-only smoke error."""
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            notes="- Smoke: smoke-pass (re-run)",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("Build-writes-Smoke" in e for e in _errors(issues)),
                "smoke-pass (re-run) must clear fail-closed Build-writes-Smoke error",
            )

    def test_next_merge_blocks_on_bar(self):
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            status="paused",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("error: Gate C test bar", out)
            self.assertNotIn("warn: Gate C test bar", out)


class TestDeriveAndCheckResults(unittest.TestCase):
    """R3/R6: --next --derive and --check-results."""

    def test_derive_differs_from_card(self):
        """R4: unsafe card merge vs derived design-phase → error + do-not-launch."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="merge",
            stage_id="design-phase",
            status="running",
            notes="- gate-c-test-override",
            gate_c_approved="merge",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("derived next:", out)
            self.assertIn("unsafe card vs derived", out)
            self.assertIn("handoff: do-not-launch", out)

    def test_derive_design_phase_when_no_design(self):
        text = _base(mode="simple", review="lite", next_step="design-phase")
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "design-phase")

    def test_derive_design_backloop_gate_b_not_design_update(self):
        """N1: design-backloop + Next gate-b → derive gate-b."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-b",
            stage_id="design-verify-phase",
            notes="- design-backloop\n- prior Gate B invalid",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "gate-b")

    def test_derive_design_backloop_pre_update(self):
        """N1: design-backloop still pre-update → design-update."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="design-update",
            notes="- design-backloop",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "design-update")

    def test_derive_needs_update_to_design_update(self):
        """N3: 03a Result needs update → design-update."""
        text = _base(mode="simple", review="lite", next_step="design-verify-phase")
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** needs update\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "design-update")

    def test_derive_missing_03a_to_first_review(self):
        """N3: design present, 03a missing → design-verify-phase / design-review."""
        text = _base(mode="simple", review="lite", next_step="design-phase")
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "design-verify-phase")

    def test_derive_full_only_idea_to_gate_a(self):
        """N2: Mode full with only 01-idea → gate-a (not analyze)."""
        text = _base(
            mode="full",
            review="full",
            next_step="ideation",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "01-idea.md").write_text("# idea\n", encoding="utf-8")
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "gate-a")

    def test_derive_full_walk_skim_then_analyze(self):
        """N2: after 01a ok, missing skim → skim; then analyze."""
        text = _base(
            mode="full",
            review="full",
            next_step="gate-a",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "01-idea.md").write_text("# idea\n", encoding="utf-8")
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** ok\n", encoding="utf-8"
            )
            self.assertEqual(
                lint_run.derive_expected_next(text, run_dir), "skim"
            )
            (run_dir / "02-skim.md").write_text(
                "**Result:** done\n", encoding="utf-8"
            )
            self.assertEqual(
                lint_run.derive_expected_next(text, run_dir), "analyze"
            )

    def test_derive_full_gate_a_escalate_holds(self):
        """N2: 01a Result escalate → hold gate-a (do not advance to skim)."""
        text = _base(
            mode="full",
            review="full",
            next_step="gate-a",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "01-idea.md").write_text("# idea\n", encoding="utf-8")
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** escalate\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "gate-a")

    def test_derive_full_gate_a_pending_holds(self):
        """G1: 01a Result pending → hold gate-a (fail closed; not skim)."""
        text = _base(
            mode="full",
            review="full",
            next_step="gate-a",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "01-idea.md").write_text("# idea\n", encoding="utf-8")
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** pending\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "gate-a")

    def test_derive_full_gate_a_missing_result_holds(self):
        """G1: 01a present but Result missing → hold gate-a (fail closed)."""
        text = _base(
            mode="full",
            review="full",
            next_step="gate-a",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "01-idea.md").write_text("# idea\n", encoding="utf-8")
            (run_dir / "01a-idea-ui-review.md").write_text(
                "# Gate A review\n\nNo Result header yet.\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "gate-a")

    def test_derive_full_gate_a_ok_to_skim(self):
        """G1: 01a Result exactly ok → skim when 02-skim missing."""
        text = _base(
            mode="full",
            review="full",
            next_step="gate-a",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "01-idea.md").write_text("# idea\n", encoding="utf-8")
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** ok\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "skim")

    def test_derive_pending_parallel_both_missing_parallel(self):
        """H3: both 03a-* missing → parallel hint (not api-first serialize)."""
        text = _base(
            mode="full",
            review="full",
            next_step="design-review",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            has_api="yes",
            has_db="yes",
            pending_parallel="api|db",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            for name in (
                "01-idea.md",
                "01a-idea-ui-review.md",
                "02-skim.md",
                "02-analysis.md",
                "02b-grill.md",
                "03-design.md",
                "04-tasks.md",
            ):
                body = (
                    "**Result:** ok\n"
                    if name == "01a-idea-ui-review.md"
                    else (
                        "**Result:** frontier-empty\n"
                        if name == "02b-grill.md"
                        else (
                            "**Result:** done\n"
                            if name == "02-skim.md"
                            else "# x\n"
                        )
                    )
                )
                (run_dir / name).write_text(body, encoding="utf-8")
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(
                derived, "api-contract-review||db-design-review"
            )

    def test_derive_pending_parallel_db_after_api(self):
        """G5: Pending parallel api|db + api done → db-design-review."""
        text = _base(
            mode="full",
            review="full",
            next_step="db-design-review",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            has_api="yes",
            has_db="yes",
            pending_parallel="api|db",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            for name in (
                "01-idea.md",
                "01a-idea-ui-review.md",
                "02-skim.md",
                "02-analysis.md",
                "02b-grill.md",
                "03-design.md",
                "04-tasks.md",
            ):
                body = (
                    "**Result:** ok\n"
                    if name == "01a-idea-ui-review.md"
                    else (
                        "**Result:** frontier-empty\n"
                        if name == "02b-grill.md"
                        else (
                            "**Result:** done\n"
                            if name == "02-skim.md"
                            else "# x\n"
                        )
                    )
                )
                (run_dir / name).write_text(body, encoding="utf-8")
            (run_dir / "03a-api-contract-review.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "db-design-review")

    def test_derive_pending_parallel_both_done_to_design_review(self):
        """G5: Pending parallel api|db + both 03a-* → design-review."""
        text = _base(
            mode="full",
            review="full",
            next_step="design-review",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            has_api="yes",
            has_db="yes",
            pending_parallel="api|db",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            for name in (
                "01-idea.md",
                "01a-idea-ui-review.md",
                "02-skim.md",
                "02-analysis.md",
                "02b-grill.md",
                "03-design.md",
                "04-tasks.md",
            ):
                body = (
                    "**Result:** ok\n"
                    if name == "01a-idea-ui-review.md"
                    else (
                        "**Result:** frontier-empty\n"
                        if name == "02b-grill.md"
                        else (
                            "**Result:** done\n"
                            if name == "02-skim.md"
                            else "# x\n"
                        )
                    )
                )
                (run_dir / name).write_text(body, encoding="utf-8")
            (run_dir / "03a-api-contract-review.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "03a-db-design-review.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "design-review")

    def test_derive_verify_pass_without_smoke(self):
        """N6: verify-pass but not smoke-pass → smoke (lite/full)."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="code-review-phase",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "smoke")

    def test_derive_skip_review_smoke_gap_prefers_build(self):
        """N6: skip-review + verify-pass without smoke → build."""
        text = _base(
            mode="simple",
            review="skip-review",
            next_step="gate-c",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            has_api="no",
            has_db="no",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "build")

    def test_before_merge_composes_check_results(self):
        """N9: --before-merge / Next=merge also runs check-results (warn-only)."""
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            notes="- gate-c-test-override — fixture",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n**Result:** bogon\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            issues.extend(lint_run.check_results(run_dir))
            self.assertTrue(
                any("bogon" in i.message for i in issues if i.severity == "warn")
            )

    def test_check_results_warns_bad_token(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n**Result:** bogon\n",
                encoding="utf-8",
            )
            issues = lint_run.check_results(run_dir)
            self.assertTrue(
                any("bogon" in i.message for i in issues)
            )

    def test_check_results_size_soft_warn(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            lines = ["# skim"] + [f"- line {i}" for i in range(50)]
            (run_dir / "02-skim.md").write_text(
                "\n".join(lines) + "\n", encoding="utf-8"
            )
            issues = lint_run.check_results(run_dir)
            self.assertTrue(
                any("02-skim.md" in i.message and "soft cap" in i.message for i in issues)
            )

    def test_handoff_design_update_write_map(self):
        rows = handoff_for._parse_stage_table(
            handoff_for.HANDOFFS.read_text(encoding="utf-8")
        )
        read_cell, write_cell = rows["design-update"]
        self.assertIn("if present", read_cell)
        self.assertIn("03-design.md", write_cell)
        self.assertIn("04-tasks.md", write_cell)
        self.assertIn("00-run.md", write_cell)

    def test_handoff_build_honors_hitl_verify(self):
        rows = handoff_for._parse_stage_table(
            handoff_for.HANDOFFS.read_text(encoding="utf-8")
        )
        read_cell, write_cell = rows["build"]
        self.assertIn("hitl.md", read_cell)
        self.assertIn("verify-and-fix.md", write_cell)

    def test_handoff_base_substitutes_write_list(self):
        rows = handoff_for._parse_stage_table(
            handoff_for.HANDOFFS.read_text(encoding="utf-8")
        )
        _read, write_cell = rows["build"]
        block = handoff_for.BASE_BLOCK.format(
            slug="s",
            stage_id="build",
            write_list=write_cell,
            size_caps_path="size-caps.md",
            skills_path_path="skills-path.md",
            severity_path="severity.md",
        )
        self.assertIn(write_cell, block)
        self.assertNotIn("<write list for stage>", block)

    def test_handoff_base_points_at_size_caps(self):
        self.assertIn("{size_caps_path}", handoff_for.BASE_BLOCK)
        self.assertNotIn("{handoffs_path}", handoff_for.BASE_BLOCK)


def _seed_full_pre_design(run_dir: Path) -> None:
    for name in (
        "01-idea.md",
        "01a-idea-ui-review.md",
        "02-skim.md",
        "02-analysis.md",
        "02b-grill.md",
        "03-design.md",
        "04-tasks.md",
    ):
        body = (
            "**Result:** ok\n"
            if name == "01a-idea-ui-review.md"
            else (
                "**Result:** frontier-empty\n"
                if name == "02b-grill.md"
                else (
                    "**Result:** done\n"
                    if name == "02-skim.md"
                    else "# x\n"
                )
            )
        )
        (run_dir / name).write_text(body, encoding="utf-8")


class TestH1H7Findings(unittest.TestCase):
    """H1–H7: single-flag API/DB, unpaid lenses, parallel, Gate A --next, stale, Adv/Quality."""

    def test_h1_derive_single_flag_api_when_pending_none(self):
        text = _base(
            mode="full",
            review="full",
            next_step="design-review",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            has_api="yes",
            has_db="no",
            pending_parallel="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _seed_full_pre_design(run_dir)
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "api-contract-review")

    def test_h1_derive_single_flag_db_when_pending_none(self):
        text = _base(
            mode="full",
            review="full",
            next_step="design-review",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            has_api="no",
            has_db="yes",
            pending_parallel="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _seed_full_pre_design(run_dir)
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "db-design-review")

    def test_h1_lint_before_design_review_missing_api_file(self):
        text = _base(
            mode="full",
            review="full",
            next_step="design-review",
            has_api="yes",
            has_db="no",
            pending_parallel="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            issues = lint_run_md(
                text,
                before_design_review=True,
                before_build=False,
                run_dir=run_dir,
            )
            self.assertTrue(
                any(
                    "03a-api-contract-review.md" in e for e in _errors(issues)
                )
            )

    def test_h1_lint_skips_when_next_is_api_contract_review(self):
        text = _base(
            mode="full",
            review="full",
            next_step="api-contract-review",
            has_api="yes",
            has_db="no",
            pending_parallel="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            issues = lint_run_md(
                text,
                before_design_review=True,
                before_build=False,
                run_dir=run_dir,
            )
            self.assertFalse(
                any(
                    "03a-api-contract-review.md" in e for e in _errors(issues)
                )
            )

    def test_h1_tiny_tweak_skips_isolated_file_requirement(self):
        text = _base(
            mode="full",
            review="full",
            next_step="design-review",
            has_api="yes",
            has_db="no",
            pending_parallel="none",
            notes="- tiny-contract-tweak — Notes fold into Quality / code-review-phase",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            issues = lint_run_md(
                text,
                before_design_review=True,
                before_build=False,
                run_dir=run_dir,
            )
            self.assertFalse(
                any(
                    "03a-api-contract-review.md" in e for e in _errors(issues)
                )
            )

    def test_h2_derive_unpaid_lens_before_test(self):
        text = _base(
            mode="simple",
            review="lite",
            next_step="test-lite",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            lens_plan="api",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "lens-api")

    def test_h2_derive_merge_findings_when_2_lenses_clean(self):
        text = _base(
            mode="simple",
            review="lite",
            next_step="test-lite",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            lens_plan="api,security",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n**Result:** clean\n\n"
                "## Merged lenses\n\n**Result:** pending\n",
                encoding="utf-8",
            )
            (run_dir / "05-lens-api.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "05-lens-security.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "merge-findings")

    def test_h2_next_do_not_launch_test_when_unpaid(self):
        text = _base(
            mode="simple",
            review="lite",
            next_step="test-lite",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            lens_plan="security",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            import io
            from contextlib import redirect_stdout

            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=False)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("unpaid", out.lower())

    def test_h3_pending_none_both_flags_still_parallel(self):
        """H1+H3: both Has API/DB yes + pending none + both missing → parallel."""
        text = _base(
            mode="full",
            review="full",
            next_step="design-review",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            has_api="yes",
            has_db="yes",
            pending_parallel="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _seed_full_pre_design(run_dir)
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(
                derived, "api-contract-review||db-design-review"
            )

    def test_h4_next_gate_a_fail_closed_before_skim(self):
        text = _base(
            mode="full",
            review="full",
            next_step="skim",
            stage_id="skim",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "01-idea.md").write_text("# idea\n", encoding="utf-8")
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** needs update\n", encoding="utf-8"
            )
            import io
            from contextlib import redirect_stdout

            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Gate A fail-closed", out)

    def test_h5_derive_review_stale_reenters_review(self):
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-c",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            notes="- review-stale — rebuild invalidated prior review",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n"
                "**Result:** success\n"
                "**Mode last run:** lite\n",
                encoding="utf-8",
            )
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "code-review-phase")

    def test_h5_derive_test_stale_reenters_test(self):
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-c",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            notes="- test-stale — rebuild invalidated prior test",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n"
                "**Result:** success\n"
                "**Mode last run:** lite\n",
                encoding="utf-8",
            )
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "test-lite")

    def test_h6_derive_adv_needs_fix_not_quality(self):
        text = _base(
            mode="full",
            review="full",
            next_step="quality",
            stage_id="adversarial",
            last_verify="verify-pass",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _seed_full_pre_design(run_dir)
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n"
                "## Adversarial test review\n\n"
                "**Result:** needs fix\n\n"
                "## Quality\n\n"
                "**Result:** pending\n\n"
                "**Result:** needs fix\n",
                encoding="utf-8",
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "fix-review")

    def test_h6_derive_quality_needs_fix_after_adv_clean(self):
        text = _base(
            mode="full",
            review="full",
            next_step="fix-review",
            stage_id="quality",
            last_verify="verify-pass",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _seed_full_pre_design(run_dir)
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n"
                "**Result:** needs fix\n\n"
                "## Adversarial test review\n\n"
                "**Result:** clean\n\n"
                "## Quality\n\n"
                "**Result:** needs fix\n",
                encoding="utf-8",
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "fix-review")

    def test_i1_full_adv_clean_quality_missing_not_review_ok(self):
        """I1: first section Result clean must not false-pass full review."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n"
                "## Adversarial test review\n\n"
                "**Result:** clean\n",
                encoding="utf-8",
            )
            self.assertFalse(lint_run._review_clean(run_dir, "full"))
            text = _base(
                mode="full",
                review="full",
                next_step="test-full",
                stage_id="adversarial",
                last_verify="verify-pass",
                hitl_gate_b="blocking",
                gate_b_approved="yes",
            )
            _seed_full_pre_design(run_dir)
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "quality")

    def test_i1_full_adv_clean_quality_needs_fix_not_review_ok(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n"
                "## Adversarial test review\n\n"
                "**Result:** clean\n\n"
                "## Quality\n\n"
                "**Result:** needs fix\n",
                encoding="utf-8",
            )
            self.assertFalse(lint_run._review_clean(run_dir, "full"))
            text = _base(
                mode="full",
                review="full",
                next_step="test-full",
                stage_id="quality",
                last_verify="verify-pass",
                hitl_gate_b="blocking",
                gate_b_approved="yes",
            )
            _seed_full_pre_design(run_dir)
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "fix-review")

    def test_i1_full_both_sections_clean_review_ok(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n"
                "## Adversarial test review\n\n"
                "**Result:** clean\n\n"
                "## Quality\n\n"
                "**Result:** clean\n",
                encoding="utf-8",
            )
            self.assertTrue(lint_run._review_clean(run_dir, "full"))
            text = _base(
                mode="full",
                review="full",
                next_step="gate-c",
                stage_id="quality",
                last_verify="verify-pass",
                hitl_gate_b="blocking",
                gate_b_approved="yes",
            )
            _seed_full_pre_design(run_dir)
            (run_dir / "03a-design-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n"
                "**Result:** success\n"
                "**Mode last run:** full\n",
                encoding="utf-8",
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "gate-c")

    def test_i1_lite_overall_result_still_review_ok(self):
        """Lite keeps single overall Result when sections are absent."""
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            self.assertTrue(lint_run._review_clean(run_dir, "lite"))


class TestE2UnpaidVsVerifyClock(unittest.TestCase):
    """E2: unpaid 05/06 vs Last verify-pass at without Notes stale tokens."""

    @staticmethod
    def _clock_iso(offset_sec: float = 0.0) -> str:
        import datetime as dt

        return dt.datetime.fromtimestamp(
            time.time() + offset_sec, tz=dt.timezone.utc
        ).isoformat()

    def _seed_paid_lite(self, run_dir: Path) -> None:
        (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
        (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
        (run_dir / "03a-design-review-log.md").write_text(
            "**Result:** clean\n", encoding="utf-8"
        )
        (run_dir / "05-review-log.md").write_text(
            "**Result:** clean\n", encoding="utf-8"
        )
        (run_dir / "06-test-log.md").write_text(
            "**Smoke result:** smoke-pass\n"
            "**Result:** success\n"
            "**Mode last run:** lite\n",
            encoding="utf-8",
        )

    def test_before_merge_errors_when_review_older_than_clock(self):
        # Clock = now; 05 older → unpaid review
        clock = self._clock_iso(0)
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            self._seed_paid_lite(run_dir)
            old = time.time() - 3600
            os.utime(run_dir / "05-review-log.md", (old, old))
            os.utime(run_dir / "06-test-log.md", (time.time(), time.time()))
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            errs = _errors(issues)
            self.assertTrue(
                any("Last verify-pass at" in e and "05-review-log" in e for e in errs)
            )

    def test_before_merge_errors_when_test_older_than_clock(self):
        clock = self._clock_iso(0)
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            self._seed_paid_lite(run_dir)
            # Fresh review after rebuild; stale test file
            os.utime(run_dir / "05-review-log.md", (time.time(), time.time()))
            old = time.time() - 3600
            os.utime(run_dir / "06-test-log.md", (old, old))
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            errs = _errors(issues)
            self.assertTrue(
                any("Last verify-pass at" in e and "06-test-log" in e for e in errs)
            )
            self.assertFalse(
                any("05-review-log" in e for e in errs)
            )

    def test_before_merge_ok_when_artifacts_newer_than_clock(self):
        # Clock in the past; fresh 05/06 after re-review/re-test
        clock = self._clock_iso(-3600)
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            self._seed_paid_lite(run_dir)
            fresh = time.time()
            os.utime(run_dir / "05-review-log.md", (fresh, fresh))
            os.utime(run_dir / "06-test-log.md", (fresh, fresh))
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            errs = _errors(issues)
            self.assertFalse(any("Last verify-pass at" in e for e in errs))
            self.assertFalse(any("review-stale" in e for e in errs))
            self.assertFalse(any("test-stale" in e for e in errs))

    def test_no_clock_skips_auto_detect(self):
        """Missing Last verify-pass at → Notes-only (no implied error)."""
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            last_verify_pass_at="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            self._seed_paid_lite(run_dir)
            old = time.time() - 7200
            os.utime(run_dir / "05-review-log.md", (old, old))
            os.utime(run_dir / "06-test-log.md", (old, old))
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("Last verify-pass at" in e for e in _errors(issues))
            )

    def test_notes_stale_still_errors_without_double_implied(self):
        clock = self._clock_iso(0)
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
            notes="- review-stale — rebuild",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            self._seed_paid_lite(run_dir)
            old = time.time() - 3600
            os.utime(run_dir / "05-review-log.md", (old, old))
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            errs = _errors(issues)
            review_msgs = [e for e in errs if "review-stale" in e or "05-review-log" in e]
            self.assertEqual(len(review_msgs), 1)
            self.assertTrue(any("Notes review-stale" in e for e in review_msgs))

    def test_derive_reenters_review_when_implied_stale(self):
        clock = self._clock_iso(0)
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-c",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            self._seed_paid_lite(run_dir)
            old = time.time() - 3600
            os.utime(run_dir / "05-review-log.md", (old, old))
            os.utime(run_dir / "06-test-log.md", (time.time(), time.time()))
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "code-review-phase")

    def test_derive_reenters_test_when_implied_stale(self):
        clock = self._clock_iso(0)
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-c",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            self._seed_paid_lite(run_dir)
            os.utime(run_dir / "05-review-log.md", (time.time(), time.time()))
            old = time.time() - 3600
            os.utime(run_dir / "06-test-log.md", (old, old))
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "test-lite")

    def test_next_do_not_launch_merge_on_implied_review_stale(self):
        clock = self._clock_iso(0)
        text = _base(
            review="lite",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="merge",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            self._seed_paid_lite(run_dir)
            old = time.time() - 3600
            os.utime(run_dir / "05-review-log.md", (old, old))
            import io
            from contextlib import redirect_stdout

            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=False)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Last verify-pass at", out)

    def test_skip_review_ignores_implied_review_stale(self):
        clock = self._clock_iso(0)
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            last_verify_pass_at=clock,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n"
                "**Result:** smoke-pass\n",
                encoding="utf-8",
            )
            old = time.time() - 3600
            os.utime(run_dir / "05-review-log.md", (old, old))
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("05-review-log" in e for e in _errors(issues))
            )


class TestM1M2E1E2Findings(unittest.TestCase):
    """Fresh-review M1/M2/E1/E2: 04a derive, 03a before Build, calibration, clarity."""

    def test_derive_tdd_review_after_design_clean_no_04a(self):
        """M1: design clean + no 04a / skip Notes → tdd-review (not gate-b/build)."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-b",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "tdd-review")

    def test_derive_gate_b_when_04a_skipped_notes(self):
        """M1: Notes 04a skipped → gate-b/build (auto → build)."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-b",
            notes="- 04a skipped — no planned test cases",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "build")

    def test_derive_gate_b_when_04a_artifact_exists(self):
        """M1: 04a-tdd-test-review.md present → past optional 04a."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="gate-b",
            hitl_gate_b="blocking",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            (run_dir / "04a-tdd-test-review.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "gate-b")

    def test_derive_full_tdd_review_after_design_clean(self):
        """M1: Mode full design clean without 04a → tdd-review."""
        text = _base(
            mode="full",
            review="full",
            next_step="gate-b",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            has_api="no",
            has_db="no",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            for name in (
                "01-idea.md",
                "01a-idea-ui-review.md",
                "02-skim.md",
                "02-analysis.md",
                "02b-grill.md",
                "03-design.md",
                "04-tasks.md",
            ):
                body = (
                    "**Result:** ok\n"
                    if name == "01a-idea-ui-review.md"
                    else (
                        "**Result:** frontier-empty\n"
                        if name == "02b-grill.md"
                        else (
                            "**Result:** done\n"
                            if name == "02-skim.md"
                            else "# x\n"
                        )
                    )
                )
                (run_dir / name).write_text(body, encoding="utf-8")
            _write_03a_clean(run_dir)
            derived = lint_run.derive_expected_next(text, run_dir)
            self.assertEqual(derived, "tdd-review")

    def test_before_build_requires_03a_clean(self):
        """M2: --before-build errors when 03a Result ≠ clean."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="auto",
            notes="- 04a skipped — no planned test cases",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any(
                    "design-verify-phase Result must be clean" in e
                    for e in _errors(issues)
                )
            )

    def test_before_build_ok_when_03a_clean(self):
        """M2: --before-build passes design gate when 03a clean."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="build",
            stage_id="gate-b",
            hitl_gate_b="auto",
            notes="- 04a skipped — no planned test cases\n"
            "- clarity-check ok — build",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
            self.assertFalse(
                any("Result must be clean before Build" in e for e in _errors(issues))
            )

    def test_next_build_do_not_launch_without_03a_clean(self):
        """M2: --next on build → do-not-launch when 03a not clean."""
        text = _base(
            mode="full",
            review="full",
            next_step="build",
            stage_id="gate-b",
            status="paused",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** ok\n", encoding="utf-8"
            )
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("error: design-review Result must be clean", out)

    def test_status_done_warns_without_calibration(self):
        """E1: Status=done without calibration evidence → warn."""
        text = _base(
            status="done",
            gate_c_approved="merge",
            notes="- finished",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("calibration evidence" in w for w in _warns(issues))
        )

    def test_status_done_ok_with_calibration_notes(self):
        """E1: Mode OK? / profile OK? / friction Notes clear calibration warn."""
        text = _base(
            status="done",
            gate_c_approved="merge",
            notes=(
                "- Mode OK? yes — simple fit\n"
                "- Review profile OK? yes — lite enough\n"
                "- Biggest friction stage? `build` — verify flaky"
            ),
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("calibration evidence" in w for w in _warns(issues))
        )

    def test_clarity_check_error_before_design_phase(self):
        """R2: Next design-phase without clarity-check token → error."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="design-phase",
            stage_id="design-phase",
            notes="- ok",
            clarity_ok=False,
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("clarity-check ok" in e for e in _errors(issues))
        )

    def test_clarity_check_ok_logged_no_error(self):
        """Soft: once-per-run presence-any clears soft-boundary error."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="design-phase",
            stage_id="design-phase",
            notes="- clarity-check ok — design-phase",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("clarity-check ok" in e and "missing" in e for e in _errors(issues))
        )

    def test_clarity_check_soft_token_does_not_unlock_build(self):
        """R3: soft design-phase token does not satisfy high-risk build."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="build",
            stage_id="build",
            notes="- clarity-check ok — design-phase",
            hitl_gate_b="auto",
            gate_b_approved="none",
            clarity_ok=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertTrue(
            any(
                "boundary-matched" in e or "clarity-check ok — build" in e
                for e in _errors(issues)
            )
        )

    def test_clarity_check_soft_token_does_not_unlock_tdd_review(self):
        """S2: soft design-phase token does not satisfy high-risk tdd-review."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="tdd-review",
            stage_id="tdd-review",
            notes="- clarity-check ok — design-phase",
            clarity_ok=False,
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any(
                "boundary-matched" in e or "clarity-check ok — tdd-review" in e
                for e in _errors(issues)
            )
        )

    def test_clarity_check_boundary_matched_tdd_review_ok(self):
        """S2: clarity-check ok — tdd-review unlocks Next tdd-review."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="tdd-review",
            stage_id="tdd-review",
            notes="- clarity-check ok — tdd-review",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertFalse(
            any("clarity-check ok" in e and "missing" in e for e in _errors(issues))
        )

    def test_clarity_check_boundary_matched_build_ok(self):
        """R3: clarity-check ok — build unlocks Next build."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="build",
            stage_id="build",
            notes="- clarity-check ok — build",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertFalse(
            any("clarity-check" in e for e in _errors(issues))
        )

    def test_clarity_check_next_do_not_launch(self):
        """--next emits error + do-not-launch when clarity-check missing."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="design-phase",
            stage_id="design-phase",
            notes="- ok",
            clarity_ok=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("error: clarity-check", out)

    def test_gate_c_approved_without_provenance_errors(self):
        """R1: Gate C approved without provenance → error."""
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push,pr,merge",
            notes="- gate-c-test-override — fixture waive\n"
            + _prov("gate-c-test-override", "waive"),
            auto_provenance=False,
        )
        # Has override provenance but not gate-c-approved provenance
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=True,
        )
        self.assertTrue(
            any(
                "Gate C approved without provenance" in e for e in _errors(issues)
            )
        )

    def test_gate_b_approved_without_provenance_errors(self):
        """R1: blocking Gate B approved without provenance → error."""
        text = _base(
            mode="full",
            review="full",
            next_step="build",
            stage_id="build",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            notes="- clarity-check ok — build",
            auto_provenance=False,
            clarity_ok=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertTrue(
            any(
                "Gate B approved without provenance" in e for e in _errors(issues)
            )
        )

    def test_waiver_token_without_provenance_errors(self):
        """R1: bare gate-c-test-override without provenance → error."""
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            notes="- gate-c-test-override — invented\n"
            + _prov("gate-c-approved"),
            auto_provenance=False,
        )
        issues = lint_run_md(
            text,
            before_design_review=False,
            before_build=False,
            before_merge=True,
        )
        self.assertTrue(
            any(
                "gate-c-test-override without provenance" in e
                for e in _errors(issues)
            )
        )

    def test_derive_unsafe_merge_do_not_launch(self):
        """R4: card merge while derived earlier → do-not-launch without override."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="merge",
            notes="- gate-c-test-override — fixture\n- clarity-check ok — merge",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            # No design → derive expects design-phase
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("unsafe card vs derived", out)

    def test_derive_unsafe_with_card_override_allows_warn(self):
        """R4/S7: card-override + provenance permits unsafe mismatch (warn only)."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="merge",
            notes=(
                "- gate-c-test-override — fixture\n"
                "- clarity-check ok — merge\n"
                "- card-override — user insisted on merge now"
            ),
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "06-test-log.md").write_text(
                "**Result:** success\n**Mode last run:** lite\n"
                "**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("card-override + provenance present", out)
            # May still do-not-launch for other Gate C bar reasons; override
            # only clears the unsafe-derive block.

    def test_derive_unsafe_card_override_without_provenance_blocks(self):
        """S7: card-override Notes without provenance → still do-not-launch."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="merge",
            stage_id="merge",
            gate_c_approved="merge",
            notes=(
                "- gate-c-test-override — fixture\n"
                "- clarity-check ok — merge\n"
                "- card-override — user insisted on merge now\n"
                + _prov("gate-c-approved", "commit push PR and merge please")
                + "\n"
                + _prov("gate-c-test-override", "waive green tests now")
            ),
            auto_provenance=False,
            clarity_ok=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("unsafe card vs derived", out)

    def test_derive_jump_ahead_review_pre_build_unsafe(self):
        """S3: card code-review-phase while derived pre-Build → do-not-launch."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="code-review-phase",
            stage_id="code-review-phase",
            notes="- clarity-check ok — design-phase",
            clarity_ok=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            # No design → derive design-phase
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("pre-Build / pre-verify jump-ahead", out)

    def test_derive_jump_ahead_test_while_review_unsafe(self):
        """T1: card test-lite while derived still in review → do-not-launch."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="test-lite",
            stage_id="test-lite",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            # No 05 → derive code-review-phase
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("derived next: code-review-phase", out)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("post-Build review still unpaid", out)

    def test_derive_jump_ahead_test_review_override_allows(self):
        """T1: card-override + provenance unlocks test while review unpaid."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="test-lite",
            stage_id="test-lite",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            notes="- card-override — skip review for fixture",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertIn("card-override + provenance present", out)
            self.assertNotIn("unsafe card vs derived", out)

    def test_derive_quality_before_adversarial_unsafe(self):
        """T2: card quality while derived adversarial → do-not-launch."""
        text = _base(
            mode="full",
            review="full",
            next_step="quality",
            stage_id="quality",
            last_verify="verify-pass",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            notes="- 04a skipped — no planned test cases",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            _seed_full_pre_design(run_dir)
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            # No 05 → derive adversarial
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("derived next: adversarial", out)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Adv before Quality", out)

    def test_derive_smoke_while_review_entry_unsafe(self):
        """T2: card smoke while derived review-entry → do-not-launch."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="smoke",
            stage_id="smoke",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("derived next: code-review-phase", out)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("review-entry", out)

    def test_derive_smoke_review_entry_with_rerun_notes_ok(self):
        """T2: Notes smoke re-run unlocks smoke during review-entry."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="smoke",
            stage_id="smoke",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            notes="- smoke re-run — independent Smoke Task",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertNotIn("unsafe card vs derived", out)
            self.assertNotIn("review-entry", out)

    def test_derive_lens_before_adversarial_unsafe(self):
        """U1: card lens-api while derived adversarial → do-not-launch."""
        text = _base(
            mode="full",
            review="full",
            next_step="lens-api",
            stage_id="lens-api",
            last_verify="verify-pass",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            lens_plan="api",
            notes="- 04a skipped — no planned test cases",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            _seed_full_pre_design(run_dir)
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            # No 05 → derive adversarial
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("derived next: adversarial", out)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("pre-lens", out)

    def test_derive_merge_findings_before_quality_unsafe(self):
        """U1: card merge-findings while derived quality → do-not-launch."""
        text = _base(
            mode="full",
            review="full",
            next_step="merge-findings",
            stage_id="merge-findings",
            last_verify="verify-pass",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            lens_plan="api,security",
            notes="- 04a skipped — no planned test cases",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            _seed_full_pre_design(run_dir)
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            # Adv clean, Quality unpaid → derive quality
            (run_dir / "05-review-log.md").write_text(
                "# Review\n\n## Adversarial\n\n**Result:** clean\n\n"
                "## Quality\n\n**Result:** pending\n",
                encoding="utf-8",
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("derived next: quality", out)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("pre-lens", out)

    def test_derive_lens_pre_lens_override_allows(self):
        """U1: card-override + provenance unlocks lens while pre-lens."""
        text = _base(
            mode="full",
            review="full",
            next_step="lens-api",
            stage_id="lens-api",
            last_verify="verify-pass",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            lens_plan="api",
            notes=(
                "- 04a skipped — no planned test cases\n"
                "- card-override — run api lens early for fixture"
            ),
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            _seed_full_pre_design(run_dir)
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertIn("card-override + provenance present", out)
            self.assertNotIn("unsafe card vs derived", out)

    def test_derive_lens_when_derived_is_that_lens_ok(self):
        """U1: card lens-api when derived lens-api (paid path) is safe."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="lens-api",
            stage_id="lens-api",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            lens_plan="api",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "03-design.md").write_text("# d\n", encoding="utf-8")
            (run_dir / "04-tasks.md").write_text("# t\n", encoding="utf-8")
            _write_03a_clean(run_dir)
            (run_dir / "06-test-log.md").write_text(
                "**Smoke result:** smoke-pass\n", encoding="utf-8"
            )
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=True)
            out = buf.getvalue()
            self.assertIn("derived next: lens-api", out)
            self.assertNotIn("unsafe card vs derived", out)
            self.assertNotIn("pre-lens", out)

    def test_h2_next_unpaid_lens_emits_error_label(self):
        """U6: unpaid-lens do-not-launch prints error: not warn:."""
        text = _base(
            mode="simple",
            review="lite",
            next_step="test-lite",
            last_verify="verify-pass",
            hitl_gate_b="auto",
            gate_b_approved="none",
            lens_plan="security",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            (run_dir / "05-review-log.md").write_text(
                "**Result:** clean\n", encoding="utf-8"
            )
            buf = __import__("io").StringIO()
            with __import__("contextlib").redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir, derive=False)
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("error: Lens plan unpaid", out)
            self.assertNotIn("warn: Lens plan unpaid", out)

    def test_provenance_filler_quote_rejected(self):
        """S4: short/filler provenance quote does not count."""
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="yes",
            next_step="build",
            stage_id="gate-b",
            notes=(
                '- provenance — gate-b-approved — user: "yes"\n'
                "- clarity-check ok — build"
            ),
            auto_provenance=False,
            clarity_ok=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "01a-idea-ui-review.md").write_text(
                "**Result:** ok\n", encoding="utf-8"
            )
            _write_03a_clean(run_dir)
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=True,
                run_dir=run_dir,
            )
        self.assertTrue(
            any("Gate B approved without provenance" in e for e in _errors(issues))
        )

    def test_skip_review_smoke_rerun_without_provenance_errors(self):
        """S5: smoke-pass (re-run) Notes without provenance → error."""
        text = _base(
            review="skip-review",
            has_api="no",
            has_db="no",
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="merge",
            last_verify="verify-pass",
            notes=(
                "- Smoke: smoke-pass (re-run)\n"
                + _prov("gate-c-approved", "merge after smoke re-run ok")
            ),
            auto_provenance=False,
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "06-test-log.md").write_text(
                "# Test log\n\n**Smoke result:** smoke-pass\n",
                encoding="utf-8",
            )
            issues = lint_run_md(
                text,
                before_design_review=False,
                before_build=False,
                before_merge=True,
                run_dir=run_dir,
            )
            self.assertTrue(
                any(
                    "smoke-pass-rerun" in e or "smoke-pass (re-run)" in e
                    for e in _errors(issues)
                )
            )


class TestHandoffDescription(unittest.TestCase):
    def test_handoff_emits_description(self):
        """R5: handoff-for.py prints Description from Task description map."""
        from io import StringIO
        import contextlib

        buf = StringIO()
        err = StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            # Call main via argparse path
            old = sys.argv
            try:
                sys.argv = ["handoff-for.py", "build"]
                rc = handoff_for.main()
            finally:
                sys.argv = old
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("Description:", out)
        self.assertIn("Build with TDD", out)

    def test_handoff_check_descriptions(self):
        """R5: --check-descriptions passes on live handoffs.md."""
        from io import StringIO
        import contextlib

        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            old = sys.argv
            try:
                sys.argv = ["handoff-for.py", "build", "--check-descriptions"]
                rc = handoff_for.main()
            finally:
                sys.argv = old
        self.assertEqual(rc, 0)
        self.assertIn("ok:", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
