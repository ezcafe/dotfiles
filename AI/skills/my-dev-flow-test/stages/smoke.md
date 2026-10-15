## Smoke — build + unit only — Fast

**Stage id:** `smoke`

**When:** Smoke **re-run** only — Build did not leave smoke-pass, commands mismatch Verify commands, or Notes `smoke re-run`. Default after Build verify-pass: **parent skips this Task** (Build-writes-Smoke — see `{my-dev-flow}/verify-and-fix.md`).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Smoke build and unit`

**Done when:** Smoke section filled; Result **smoke-pass** or **smoke-fail**.

**Task prompt:**

```
You are the runner for my-dev-flow-test Smoke (build + unit only). Fresh context only. Do not run e2e. Do not start code review here.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py smoke>

Read 00-run.md **Verify commands** (required). Use those commands and cwd only — do not invent a different stack. N/A unit → run build only (see verify-and-fix.md).

Run in order:
1. Build (if not N/A)
2. Unit tests (if not N/A)

Rules:
- Update 06-test-log.md → Smoke section + Mode last run: smoke.
- Result = smoke-pass only if all non-N/A Verify build/unit steps are green.
- Otherwise Result = smoke-fail and fill Fix ask for my-dev-flow-code.
- Do not fix product code. Do not merge or push.
- Simple plain words.

Return FIRST LINE exactly: Result: smoke-pass | smoke-fail
Then short summary + path to 06-test-log.md ({my-dev-flow}/results.md).
```

**After:** Parent: smoke-pass → `my-dev-flow-review` (or Gate C if **legal** skip-review — **Mode simple** + Has API/DB = **no** only; else must not be skip-review). smoke-fail → Fix-from-tests → verify-pass → re-smoke. Do not open Gate C/merge from this skill.
