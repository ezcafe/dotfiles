## Smoke — build + unit only — Fast

**Stage id:** `smoke`

**When:** Smoke **re-run** when Build did not leave smoke-pass, commands mismatch Verify commands, Notes `smoke re-run`, **or** Mode **full** + Review profile **full** ([verify.md](../../my-dev-flow-v2/verify.md) Independent Smoke / E1). Mode **simple** / Mode **full** + profile **lite**: after Build verify-pass with matching Smoke section, **parent may skip** this Task (Build-writes-Smoke). Under **skip-review** when Smoke is unpaid/fail: Prefer unpaid independent Smoke ([verify.md](../../my-dev-flow-v2/verify.md) Skip-review + Smoke; parent sets Notes `smoke re-run` once — [handoffs.md](../../my-dev-flow-v2/handoffs.md)). Do **not** launch `test-full` / `test-lite` while skip-review stays legal; else Gate C only when bar met ([gate-c.md](../../my-dev-flow-v2/gate-c.md)) or drop skip-review → lite.

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
- On smoke-pass: set **Smoke source: Smoke-Task** on `06` only (do **not** write Notes).
- Result = smoke-pass only if all non-N/A Verify build/unit steps are green.
- Otherwise Result = smoke-fail and fill Fix ask for my-dev-flow-v2-code.
- Do not fix product code. Do not merge or push.
- Simple plain words.

Return FIRST LINE exactly: Result: smoke-pass | smoke-fail
Then short summary + path to 06-test-log.md ({my-dev-flow-v2}/results.md).
```

**After:** Parent markdown-only:

1. **E1 smoke-pass** (Mode **full** + profile **full**): confirm Task set **Smoke source: Smoke-Task** on `06`; parent Notes + provenance per [verify.md](../../my-dev-flow-v2/verify.md) Independent Smoke / E1. Then → `my-dev-flow-v2-review`.
2. **skip-review smoke-pass** (legal **skip-review**): same parent Notes + provenance; then escape / Prefer paid ([verify.md](../../my-dev-flow-v2/verify.md) Skip-review + Smoke · [gate-c.md](../../my-dev-flow-v2/gate-c.md)). Escape / Prefer paid applies **only** on this bullet — not on (3).
3. **Other profiles** — after Smoke Task **or** Build-writes-Smoke skip (Mode simple / profile lite): → review / test per profile (`code-review-phase` or Adv/Quality, then lenses / test). Do **not** open Gate C from this bullet (Smoke Task or skip ≠ an escape Notes↔provenance pair).
4. On **smoke-fail**: Next via [derive-next.md](../../my-dev-flow-v2/derive-next.md) → `fix-tests` → verify-pass → re-smoke.

Do not open Gate C / merge from this skill except via bullet (2) (escape Notes↔provenance + verify-pass + smoke-pass).
