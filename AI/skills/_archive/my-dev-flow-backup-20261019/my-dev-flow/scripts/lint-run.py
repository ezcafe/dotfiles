#!/usr/bin/env python3
"""Lint a my-dev-flow run folder (.my-docs/workflow/<slug>/).

Thin CLI facade. Implementation modules (each docstring points at SoT):
  lint_common.py · lint_stage_ids.py · lint_gate_b.py · lint_gate_c.py ·
  lint_derive.py · lint_core.py

Public flags and behavior match the pre-split CLI (see scripts/README.md).
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure sibling modules import when loaded via importlib / direct path
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

# Re-export public + test-facing API (tests load this file via importlib)
from lint_common import *  # noqa: F403
from lint_common import (  # noqa: F401
    check_consent_writes,
    snapshot_consent,
    _full_profile_independent_smoke,
)
from lint_stage_ids import (  # noqa: F401
    check_stage_id_registry,
    stage_ids_from_handoffs,
    stage_ids_from_parent_next,
    stage_ids_from_stages_files,
)
from lint_gate_b import (  # noqa: F401
    _async_gap_pending_digest_ts,
    _async_notify_requested_ok,
    _async_turn_gap_ok,
    _check_async_gate_b_gap,
    _check_async_notify_requested,
    _check_design_backloop_gate_b,
    _check_gate_b_approved,
    _check_hitl_gate_b_mode,
    _gate_b_approved_ok,
    _parse_gate_b_approved,
    _parse_hitl_gate_b,
)
from lint_gate_c import (  # noqa: F401
    _check_gate_c_approved,
    _check_gate_c_test_bar,
    _check_skip_review_build_only_smoke,
    _check_stale_before_merge,
    _check_status_done_requires_merge,
    _check_waiver_provenance,
    _docs_only_marked,
    _implied_review_stale,
    _implied_test_stale,
    _independent_smoke_done,
    _last_verify_pass,
    _parse_gate_c_approved,
    _review_profile,
    _smoke_fail_or_failure,
    _smoke_pass,
    _test_log_failure,
    _test_log_success,
)
from lint_derive import (  # noqa: F401
    _design_review_clean,
    _design_review_result,
    _lenses_complete,
    _next_stage_legality_warns,
    _review_clean,
    _unpaid_lens_stages,
    check_results,
    derive_expected_next,
)
from lint_core import (  # noqa: F401
    _phase_gate_flags,
    _unsafe_card_derive_mismatch,
    dry_run_seed,
    lint_run_md,
    main,
    print_next_hint,
)

if __name__ == "__main__":
    raise SystemExit(main())
