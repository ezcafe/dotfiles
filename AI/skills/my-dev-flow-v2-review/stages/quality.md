## quality

**Stage id:** `quality`

**When:** Review profile **full** (after Adversarial clean). Profile **lite** uses **code-review-phase** instead.

**FIRST (Mode full × profile full):** Require `Smoke source: Smoke-Task` (required; optionally ALSO Run log / `06` after `Last verify-pass at`) — [verify.md](../../my-dev-flow-v2/verify.md) Independent Smoke (SoT / E1). Notes `smoke-pass (re-run)` is companion provenance, not the unlock predicate. Do **not** unlock from Run-log alone or Notes alone. Missing → `Result: blocked — E1 smoke re-run unpaid` (do not start Quality; same bar as Adv if Adv was skipped).

**Skills:** `{code-review-and-quality}/SKILL.md`  
Bugbot only if the user asked.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Quality review`

**Done when:** zero Critical/Major for Quality.

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-v2-review Quality Review. Generation ≠ verification — you did not write this draft.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for quality>

FIRST (Mode full × profile full): Require `Smoke source: Smoke-Task` (required; optionally ALSO Run log / `06` after `Last verify-pass at`) — see {my-dev-flow-v2}/verify.md Independent Smoke (SoT / E1). Notes `smoke-pass (re-run)` is companion provenance, not the unlock predicate. Do not unlock from Run-log alone or Notes alone. Missing → stop; return first line `Result: blocked — E1 smoke re-run unpaid`; do not start Quality (same bar as Adv if Adv was skipped).

Read {code-review-and-quality}/SKILL.md and follow it.
Review uncommitted / branch changes against 01-idea, 03-design, and 04-tasks.
When Has UI: also compare draft UI to Design UI specs in 03-design / 04-tasks + Gate A #1/#2 — fail **Major** if shipped look drifts on **size**, **positions**, **texts**, or chrome.
When 03-design **System design** or **Design patterns used** is not N/A: check draft code honors their Best practices / anti-patterns and does not invent a conflicting shape (Architecture axis). Flag design↔code gaps as Major when clear.

Do NOT deep-review API contracts here when Lens plan includes **api** — that is the dedicated API lens. Tiny-tweak / no api in plan: fold light contract checks into Quality.
Do NOT deep-review schema/migrations/persistence queries here when Lens plan includes **db** — that is the dedicated DB lens. Tiny-tweak / no db in plan: fold light checks into Quality.

Label every finding Critical / Major / Enhancement (Nit/FYI ok).
Append to 05-review-log.md under heading “Quality”.
Under that same heading write **Result:** clean | needs fix (section Result only — feeds **Review clean** with Adv; Adv clean alone must not advance; **overall Result** is separate and may also include Merged when Lens plan **2+** — do **not** equate this section / file-top with overall; file-top may stay **pending** — do **not** update file-top Result).

Section Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow-v2}/results.md · severity.md · derive-next.md Definitions).
Do not fix.
Return FIRST LINE exactly: Result: clean | needs fix | blocked — E1 smoke re-run unpaid
Then finding table, clean status, or blocked reason.
```

**After:** SoT → [derive-next.md](../../my-dev-flow-v2/derive-next.md) · [parent-loop-hint.md](parent-loop-hint.md). clean → parent launches unpaid `lens-*` per Lens plan (2+ → parallel → `merge-findings`) → `test-full`. needs fix → Next=`fix-review` (Fix Mode quality); then Prefer re-run this dirty stage.

---
