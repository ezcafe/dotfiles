## Fix from tests (Senior) — Fast — TDD

**Stage id:** `fix-tests`

**When:** `06-test-log.md` Result is **smoke-fail** or **failure**.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Fix from test log`

**Done when:** fix-ask items addressed with TDD; **Verify gate pass**; Result **verify-pass** (first return line).

**Rules:** `{my-dev-flow-v2}/verify.md` — Fix rules + Verify gate (build+unit + cited failing tests); max 3 attempts.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-v2-code Fix from tests. Fresh context only. Repair only what the test log asks. You must pass the Verify gate before the parent re-runs tests.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for fix-tests>
Read {my-dev-flow-v2}/verify.md.

Read 00-run.md (Verify commands). Read 06-test-log.md (Failures + Fix ask). Read 03-design.md and 04-tasks.md.

Rules:
- Fix only listed failures / fix-ask items.
- TDD: Red → Green → Refactor → Verify.
- Update skeletons if you change UI layout.
- Append Round notes on 06-test-log.md.
- **Verify gate:** Use Verify commands from 00-run.md. Also re-run failing tests named in Failures / Fix ask. Max 3 attempts. Do not claim done on verify-fail.
- Do not merge or push. Do not `git commit` unless the user explicitly asked for a commit.
- If you cannot stay aligned with 03-design / 04-tasks → stop; return that design must change (parent Design-backloop). Do not silently rewrite design docs.

Return FIRST LINE exactly: Result: verify-pass | verify-fail
Then: what you fixed; commands + pass/fail; anything still out of scope.
```

**After:** On **verify-pass** → [derive-next-post.md](../../my-dev-flow-v2/derive-next-post.md) first-match: Prefer `smoke` if Smoke unpaid/fail (or Notes re-smoke); else if profile ≠ **skip-review** Prefer unpaid `test-*` (`test-full` / `test-lite`); else **skip-review** ordered recovery (Prefer paid → `merge` \| `gate-c` / Decision N — [verify.md](../../my-dev-flow-v2/verify.md) Prefer paid). Update Last Verify + `**Last verify-pass at:**` `<ISO-8601 Run-log local wall time>` (same SoT clock as Gate B settle expansion — [derive-next.md](../../my-dev-flow-v2/derive-next.md) Freshness). **Stale Notes:** skip-review → clear `review-stale`, Prefer unpaid Smoke for `test-stale`; lite/full → if prior review/test Results still look paid, Notes `- review-stale` / `- test-stale` ([verify.md](../../my-dev-flow-v2/verify.md) Stale). On **verify-fail** after 3 → Decision N.
