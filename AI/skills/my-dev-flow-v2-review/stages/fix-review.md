## fix-review

**Stage id:** `fix-review`

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Fix review findings`

**When:**

- After Adversarial or Quality findings (profile **full**), OR
- After `code-review-phase` findings (profile **lite**), OR
- After Merge findings Result **needs fix** (use merged Fix ask only) — Mode `merged-lenses`, OR
- After Lens plan **1** Result **needs fix** (parent copied that `05-lens-*` into Merged; use that Fix ask) — Mode `plan-1-lens`

**Done when:** Fix-ask items addressed; **Verify gate pass** per `{my-dev-flow-v2}/verify.md` (unless docs-only); Result **verify-pass** (first return line).

**Docs-only:** Pure docs/comments (no code/tests changed) still return first-line **`Result: verify-pass`**. Note in `05-review-log.md` Fix notes and parent Notes: `TDD/Verify skipped — docs-only` (not a separate Result token — [results.md](../../my-dev-flow-v2/results.md)).

**Verify gate (blocking):** Use Verify commands from `00-run.md`; max 3 attempts. On **verify-fail**, parent must **not** re-run verifiers — re-launch Fix or Decision N.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-v2-review Fix. You fix listed findings only. You do not self-approve — verifiers will re-check. You must pass the Verify gate before the parent re-runs review.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for fix-review>
Read {my-dev-flow-v2}/verify.md.

Mode: <adversarial-tests | quality | code-review-phase | merged-lenses | plan-1-lens>
Findings / Fix ask to apply:
<paste findings or merged Fix ask>

Rules:
- TDD: for behavior bugs, add/adjust a failing test first (Red), then fix (Green), refactor, verify.
- Pure docs/comments: note “TDD/Verify skipped — docs-only” in 05-review-log.md; still return Result: verify-pass (parent may mirror Notes).
- Use Verify commands from 00-run.md. Do not expand scope.
- Update 05-review-log.md Fix notes with what you fixed.
- For merged-lenses: only apply the Merged lenses Fix ask winners — do not revive deferred losers unless needed for a winner.
- For plan-1-lens: only apply the plan-1 Fix ask (parent-copied Merged / that `05-lens-*`) — same winner rule as merged-lenses when Merged was copied.
- **Verify gate:** Max 3 attempts. Do not claim done on verify-fail.
- If you cannot stay aligned with 03-design / 04-tasks → stop; parent Design-backloop. Do not silently rewrite design docs.

Return FIRST LINE exactly: Result: verify-pass | verify-fail
Then: list of fixes; commands + pass/fail; whether tests/behavior changed (yes/no) — informational only; does **not** override Prefer dirty.
```

## After Fix

- Advance only on Result **verify-pass** (docs-only uses the same token + Notes annotation). On **verify-fail** after 3 → Decision N; else re-launch Fix.
- On **verify-pass**: update Last Verify + set `**Last verify-pass at:**` `<ISO-8601 Run-log local wall time>` (same SoT clock as Gate B settle expansion — [derive-next.md](../../my-dev-flow-v2/derive-next.md) Freshness) — same parent line as Build / fix-tests.
- Parent Prefer ([derive-next.md](../../my-dev-flow-v2/derive-next.md)) is Expected-Next SoT: re-run **dirty** verifier first; if already clean → else continue table. Examples: [fix-review-rereview.md](../../my-dev-flow-v2/examples/fix-review-rereview.md) · [fix-review-relens.md](../../my-dev-flow-v2/examples/fix-review-relens.md).
- Branch on Fix Mode / **Review profile** (no Adv/lite-first Prefer override when tests/behavior changed):
  - **lite** — Mode `code-review-phase` → Prefer `code-review-phase` until clean. Mode `merged-lenses` \| `plan-1-lens` → mark planned `05-lens-*` + Merged unpaid → Prefer re-run Lens plan lenses → `merge-findings` if 2+.
  - **full** — Mode `adversarial-tests` → Prefer Adversarial until clean. Mode `quality` → Prefer Quality until clean. Both dirty/unclear → Adv then Quality. Mode `merged-lenses` \| `plan-1-lens` → mark planned `05-lens-*` + Merged unpaid → Prefer re-run Lens plan lenses → `merge-findings` if 2+.

---
