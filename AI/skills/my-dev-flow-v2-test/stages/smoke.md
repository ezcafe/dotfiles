## Smoke — build + unit only — Fast

**Stage id:** `smoke`

**When:** Smoke **re-run** when Build did not leave smoke-pass, commands mismatch Verify commands, Notes `smoke re-run`, **or** Mode **full** + Review profile **full** ([verify.md](../../my-dev-flow-v2/verify.md) Independent Smoke / E1 — Build-writes-Smoke alone blocked before Adv). Mode **simple** / Mode **full** + profile **lite**: after Build verify-pass with matching Smoke section, **parent may skip** this Task (Build-writes-Smoke). Under **skip-review**: do **not** launch `test-full` / `test-lite`; allow this Task **only** with Notes `smoke re-run` ([verify.md](../../my-dev-flow-v2/verify.md) Skip-review + Smoke ordered recovery); else Gate C when escape + provenance met ([gate-c.md](../../my-dev-flow-v2/gate-c.md) · [hitl.md](../../my-dev-flow-v2/hitl.md)) or drop skip-review → lite.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Smoke build and unit`

**Done when:** Smoke section filled; Result **smoke-pass** or **smoke-fail**.

**Task prompt:**

```
You are the runner for my-dev-flow-v2-test Smoke (build + unit only). Fresh context only. Do not run e2e. Do not start code review here.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for smoke>

Read 00-run.md **Verify commands** (required). Use those commands and cwd only — do not invent a different stack. N/A unit → run build only (see verify.md).

Run in order:
1. Build (if not N/A)
2. Unit tests (if not N/A)

Rules:
- Update 06-test-log.md → Smoke section + Test path last run: smoke (LEGACY alias Mode last run on resume only).
- Result = smoke-pass only if all non-N/A Verify build/unit steps are green.
- Otherwise Result = smoke-fail and fill Fix ask for my-dev-flow-v2-code.
- Do not fix product code. Do not merge or push.
- Simple plain words.

Return FIRST LINE exactly: Result: smoke-pass | smoke-fail
Then short summary + path to 06-test-log.md ({my-dev-flow-v2}/results.md).
```

**After:** Parent markdown-only:

- On **smoke-pass** (Mode **full** + profile **full**): Notes `smoke-pass (re-run)`; clear Notes `smoke re-run`. Confirm Run log stage `smoke` and/or `06` Smoke section updated after `Last verify-pass at` ([verify.md](../../my-dev-flow-v2/verify.md) Independent Smoke / E1). Optional habit: Run log `parent consent write — smoke-pass-rerun` ([hitl.md](../../my-dev-flow-v2/hitl.md)). Then → `my-dev-flow-v2-review`.
- Under legal **skip-review**: same Notes + provenance `smoke-pass-rerun` (+ optional consent ack) before Gate C escape only ([gate-c.md](../../my-dev-flow-v2/gate-c.md) · [hitl.md](../../my-dev-flow-v2/hitl.md) · [verify.md](../../my-dev-flow-v2/verify.md) Skip-review + Smoke). Gate C escapes live **only** on this bullet — not on the Else skip path.
- Else (Mode simple / profile lite Build-writes-Smoke skip path) → review / test only (`code-review-phase` or Adv/Quality per profile, then lenses / test). Do **not** open Gate C from this Else (skipping the Smoke Task ≠ Gate C escape).
- On **smoke-fail**: Next via [derive-next.md](../../my-dev-flow-v2/derive-next.md) → `fix-tests` → verify-pass → re-smoke.

Do not open Gate C / merge from this skill except via the legal **skip-review** bullet above.
