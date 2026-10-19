## adversarial

**Stage id:** `adversarial`

**When:** Review profile **full**. Profile **lite** uses **code-review-phase** instead.

**FIRST (Mode full × profile full):** Require `Smoke source: Smoke-Task` (required; optionally ALSO Run log / `06` after `Last verify-pass at`) — [verify.md](../../my-dev-flow-v2/verify.md) Independent Smoke (SoT / E1). Notes `smoke-pass (re-run)` is companion provenance, not the unlock predicate. Do **not** unlock from Run-log alone or Notes alone. Missing → `Result: blocked — E1 smoke re-run unpaid` (do not start Adv).

**Generation ≠ verification:** different pass from Build.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Adversarial test review`

**Done when:** zero Critical/Major on test quality.

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-v2-review Adversarial Test Review. You did NOT write this code. Do not rewrite features unless needed to describe a finding.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for adversarial>

FIRST (Mode full × profile full): Require `Smoke source: Smoke-Task` (required; optionally ALSO Run log / `06` after `Last verify-pass at`) — see {my-dev-flow-v2}/verify.md Independent Smoke (SoT / E1). Notes `smoke-pass (re-run)` is companion provenance, not the unlock predicate. Do not unlock from Run-log alone or Notes alone. Missing → stop; return first line `Result: blocked — E1 smoke re-run unpaid`; do not start Adv.

Review tests and how they map to 04-tasks.md and the behavior in the draft.

Check:
- Tests that only assert mocks are mocks (“mock theater”)
- Missing edge cases and negative cases
- Non-deterministic or flaky patterns
- Missing failure-mode coverage for critical paths
- Prefer readable, deterministic tests tied to real failure modes

Append findings to 05-review-log.md under heading “Adversarial test review” with severity Critical / Major / Enhancement (and Nit/FYI if useful).
Under that same heading write **Result:** clean | needs fix (section Result only — feeds **Review clean** with Quality; **overall Result** is separate and may also include Merged when Lens plan **2+** — do **not** equate this section / file-top with overall; file-top may stay **pending** — do **not** update file-top Result).

Section Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow-v2}/results.md · severity.md · derive-next.md Definitions).
If not clean: list findings with file:line when possible. Do not fix them yourself.
Return FIRST LINE exactly: Result: clean | needs fix | blocked — E1 smoke re-run unpaid
Then finding table, clean status, or blocked reason.
```

**After:** SoT → [derive-next.md](../../my-dev-flow-v2/derive-next.md) · [parent-loop-hint.md](parent-loop-hint.md). clean → `quality`. needs fix → Next=`fix-review` (Fix Mode adversarial-tests); then Prefer re-run this dirty stage.

---
