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
) -> str:
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

**Lens plan:** none

{verify_block}**Last Verify:** {last_verify}
**Verify attempts:** 0

**Gate B veto:** {veto}

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
- **HITL Gate B:** auto
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
            notes="- tiny-contract-tweak — folded into design-review / Quality",
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


class TestNextAndDryRun(unittest.TestCase):
    def test_print_next_hint(self):
        text = _base(next_step="build", stage_id="gate-b", status="paused")
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "00-run.md").write_text(text, encoding="utf-8")
            rc = lint_run.print_next_hint(run_dir)
            self.assertEqual(rc, 0)

    def test_dry_run_seed(self):
        with tempfile.TemporaryDirectory() as td:
            parent = Path(td)
            slug_dir = parent / "20261013-dry-run-fixture"
            rc = lint_run.dry_run_seed(slug_dir, slug=None)
            self.assertEqual(rc, 0)
            self.assertTrue((slug_dir / "00-run.md").is_file())


if __name__ == "__main__":
    unittest.main()
