## fix-review

**Stage id:** `fix-review`

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Fix review findings`

**When:**

- After Adversarial or Quality findings (sequential lenses), OR
- After Merge findings Result **needs fix** (use merged Fix ask only)

**Done when:** Fix-ask items addressed; **Verify gate pass** per `{my-dev-flow}/verify-and-fix.md` (unless docs-only); Result **verify-pass** (first return line).

**Verify gate (blocking):** Use Verify commands from `00-run.md`; max 3 attempts. On **verify-fail**, parent must **not** re-run verifiers — re-launch Fix or Decision N.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-review Fix. You fix listed findings only. You do not self-approve — verifiers will re-check. You must pass the Verify gate before the parent re-runs review.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py fix-review>
Read {my-dev-flow}/verify-and-fix.md.

Mode: <adversarial-tests | quality | merged-lenses>
Findings / Fix ask to apply:
<paste findings or merged Fix ask>

Rules:
- TDD: for behavior bugs, add/adjust a failing test first (Red), then fix (Green), refactor, verify.
- Pure docs/comments: note “TDD skipped — no behavior” in 05-review-log.md; Verify skipped when no code/tests changed.
- Use Verify commands from 00-run.md. Do not expand scope.
- Update 05-review-log.md Fix notes with what you fixed.
- For merged-lenses: only apply the Merged lenses Fix ask winners — do not revive deferred losers unless needed for a winner.
- **Verify gate:** Max 3 attempts. Do not claim done on verify-fail.
- If you cannot stay aligned with 03-design / 04-tasks → stop; parent Design-backloop. Do not silently rewrite design docs.

Return FIRST LINE exactly: Result: verify-pass | verify-fail
Then: list of fixes; commands + pass/fail; whether tests/behavior changed (yes/no).
```

**After Fix:**

- Advance only on Result **verify-pass** (or docs-only skip noted). On **verify-fail** after 3 → Decision N; else re-launch Fix.
- Mode adversarial-tests → re-run Adversarial until clean.
- Mode quality → re-run Quality until clean.
- Mode merged-lenses → if tests/behavior changed, Adversarial once (Quality if structure changed); then re-run Lens plan lenses → Merge findings (if 2+).

---
