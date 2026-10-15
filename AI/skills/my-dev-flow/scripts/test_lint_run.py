#!/usr/bin/env python3
"""Unit tests for lint-run.py — run from this directory:

  python -m pytest test_lint_run.py -q
  # or
  python -m unittest test_lint_run.py
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
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
    notes: str = "- ok",
    task_count: str = "1",
    next_step: str = "design-phase",
    stage_id: str = "design-phase",
    verify: bool = True,
    hitl_gate_b: str | None = None,
    gate_b_approved: str | None = None,
    gate_c_approved: str = "none",
    lens_plan: str = "none",
) -> str:
    if hitl_gate_b is None:
        hitl_gate_b = "blocking" if mode == "full" else "auto"
    if gate_b_approved is None:
        # Blocking Gate B needs durable yes before Build; keep fixtures green
        gate_b_approved = "yes" if hitl_gate_b == "blocking" else "none"
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
**Verify attempts:** 0

**Gate B veto:** {veto}

**Gate B approved:** {gate_b_approved}

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
- **Gate C approved:** {gate_c_approved}

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

- **12:00** · running · {stage_id} · fixture
"""


def _errors(issues) -> list[str]:
    return [i.message for i in issues if i.severity == "error"]


def _warns(issues) -> list[str]:
    return [i.message for i in issues if i.severity == "warn"]


class TestLintRun(unittest.TestCase):
    def test_legal_skip_review(self):
        text = _base(review="skip-review", has_api="no", has_db="no")
        issues = lint_run_md(
            text, before_design_review=False, before_build=True, check_skip_review=True
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

    def test_pending_parallel_api_db_until_both_done(self):
        text = _base(
            mode="full",
            review="full",
            has_api="yes",
            has_db="yes",
            pending_parallel="api|db",
        )
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "03a-api-contract-review.md").write_text("ok", encoding="utf-8")
            issues = lint_run_md(
                text,
                before_design_review=True,
                before_build=False,
                run_dir=run_dir,
            )
            self.assertTrue(
                any("without" in e and "03a-db" in e for e in _errors(issues))
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
        text = _base(
            status="paused",
            notes=(
                "- async-notify posted — veto window open until Build starts\n"
                "- Build armed\n"
                "- parent turn gap observed"
            ),
            next_step="build",
            stage_id="gate-b",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertFalse(
            any("Build armed" in e for e in _errors(issues))
        )

    def test_task_count_soft_cap_warn(self):
        text = _base(mode="full", review="full", task_count="20", status="running")
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
                handoffs_path=str(skill_root / "handoffs.md"),
                skills_path_path=str(skill_root / "skills-path.md"),
                severity_path=str(skill_root / "severity.md"),
            )
            self.assertIn(str(skill_root / "handoffs.md"), block)
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

    def test_default_lint_next_merge_with_approved_ok(self):
        text = _base(
            next_step="merge",
            stage_id="gate-c",
            gate_c_approved="commit,push",
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
            from io import StringIO
            import contextlib

            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                rc = lint_run.print_next_hint(run_dir)
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Gate B approved", out)

    def test_design_backloop_with_stale_approved_errors(self):
        """H1: design-backloop Notes → error regardless of approved."""
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
        self.assertTrue(
            any("design-backloop" in e for e in _errors(issues))
        )

    def test_design_backloop_with_approved_none_errors(self):
        """H1: design-backloop + approved none still errors (blocks soft Gate B)."""
        text = _base(
            mode="full",
            review="full",
            hitl_gate_b="blocking",
            gate_b_approved="none",
            next_step="design-update",
            stage_id="build",
            notes="- design-backloop\n- prior Gate B invalid",
        )
        issues = lint_run_md(
            text, before_design_review=False, before_build=False
        )
        self.assertTrue(
            any("design-backloop" in e for e in _errors(issues))
        )

    def test_design_backloop_soft_gate_b_before_build_errors(self):
        """H1: auto + design-backloop + approved none → error under --before-build."""
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
        issues = lint_run_md(
            text, before_design_review=False, before_build=True
        )
        self.assertTrue(
            any("design-backloop" in e for e in _errors(issues))
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
            self.assertEqual(rc, 0)
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
            self.assertEqual(rc, 0)
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
        text = _base(next_step="build", stage_id="gate-b", status="paused")
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
            notes="- async-notify posted — veto window open until Build starts",
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
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Build armed", out)
            self.assertNotIn("handoff-for.py build", out)

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
            self.assertEqual(rc, 0)
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
            self.assertEqual(rc, 0)
            self.assertIn("handoff: do-not-launch", out)
            self.assertIn("Gate C approved", out)
            self.assertNotIn("handoff-for.py merge", out)

    def test_print_next_hint_merge_with_gate_c_emits_handoff(self):
        text = _base(
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
            self.assertEqual(rc, 0)
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
            self.assertEqual(rc, 0)
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


if __name__ == "__main__":
    unittest.main()
