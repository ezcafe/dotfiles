# my-dev-flow-test stages

Stage-scoped handoff: `{my-dev-flow}/handoffs.md` → stage id table.  
Test log template: same file → “06-test-log.md”.

---

## Smoke — build + unit only — Fast

**When:** Smoke **re-run** only — Build did not leave smoke-pass, commands mismatch Verify commands, or Notes `smoke re-run`. Default after Build verify-pass: **parent skips this Task** (Option B — see `{my-dev-flow}/verify-and-fix.md`).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Smoke build and unit`

**Done when:** Smoke section filled; Result **smoke-pass** or **smoke-fail**.

**Task prompt:**

```
You are the runner for my-dev-flow-test Smoke (build + unit only). Fresh context only. Do not run e2e. Do not start code review here.

<Stage-scoped handoff for stage id smoke from {my-dev-flow}/handoffs.md>

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

Return: smoke-pass | smoke-fail, and path to 06-test-log.md.
```

**After:** Parent: smoke-pass → `my-dev-flow-review` (or Gate C if skip-review). smoke-fail → Fix-from-tests → verify-pass → re-smoke.

---


## Lite test (Fast) — stage id `test-lite`

**When:** Review profile **lite** after review clean (or parent asks lite).

**Task description:** `Run build and tests`

**Done when:** targeted e2e (and unit if needed) green; Result success|failure in `06-test-log.md`.

**Task prompt:**

```
You run lite verification for my-dev-flow-test. Fresh context only.

<Stage-scoped handoff for test-lite from {my-dev-flow}/handoffs.md>

Read 04-tasks.md for required e2e. Run the repo’s unit (if not already smoke-pass) and only e2e that match this change / tasks.
Do NOT run a coverage Task. Do NOT add broad missing e2e unless 04-tasks explicitly requires a new e2e file.
Write results into 06-test-log.md. Result: success | failure. On failure include Fix ask.
Return: Result + short summary + path.
```

---
## Full test suite — Fast — stage id `test-full` (one Task)

**When:** Review profile **full** after review clean. **One Task** covers coverage check + add missing e2e + run suite. Do **not** launch separate coverage / add-e2e / run Tasks on new runs (legacy names accepted on resume — see LEGACY.md).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Full test suite`

**Done when:** `06-test-log.md` has Coverage + Runs filled; Result **success** | **failure**.

**Task prompt:**

```
You run **full** verification for my-dev-flow-test in **one** Task (coverage + gaps + suite). Fresh context only. Do not fix product behavior here (except adding e2e for MISSING flows). Do not merge or push.

<Stage-scoped handoff for stage id test-full from {my-dev-flow}/handoffs.md>
Read {my-dev-flow}/verify-and-fix.md for Verify commands rules.

### 1 — Coverage
Read 03-design.md (success criteria, flows) and 04-tasks.md. Scan existing e2e + how to run them.
Map each main flow → covered (file + test name) or MISSING. Note stack or “no e2e stack”.
Write 06-test-log.md Coverage section. Mode last run: full.

### 2 — Add missing e2e
If MISSING items exist **and** an e2e stack exists: add tests only for those flows using repo patterns. Do not change product behavior. If a gap cannot be automated safely, mark blocked with why.
If no e2e stack: skip add; note in Coverage; parent may mark failure if e2e was required.

### 3 — Run suite
Read 00-run.md **Verify commands**. Use those cwd/build/unit/e2e only (N/A → skip with note).
Run in order: build → unit → e2e (when not N/A).
Capture exit codes + short failure excerpts.
Result = **success** only if all non-N/A Verify steps are green AND no open required MISSING/blocked gaps.
Else Result = **failure** + Fix ask for my-dev-flow-code.
Update 06-test-log.md Runs + Result.

Return: success | failure + path to 06-test-log.md.
```

**After:** success → Gate C. failure → Fix-from-tests (verify-pass) → re-run `test-full`.

---

## Parent loop hint (my-dev-flow)

```
After Build verify-pass (+ Smoke section written)
  → Skip Smoke Task (Option B) unless smoke re-run needed
  → skip-review → Gate C
  → else → my-dev-flow-review
Smoke re-run fail → Fix (verify-pass) → re-smoke
After review clean → test-full (one Task) | test-lite
  On failure → Fix (verify-pass) → re-test
  On success → Gate C → my-dev-flow-merge
After 3 test↔code rounds per mode → pause (Decision N)
```