# my-test-subflow stages

Stage-scoped handoff: `~/.cursor/skills/my-dev-flow/templates.md` → stage id table.  
Test log template: same file → “06-test-log.md”.

---

## Smoke — build + unit only — Fast

**When:** After Build; **before** `my-review-subflow`. Parent Step 4s / `run my-test-subflow smoke`.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Smoke build and unit`

**Done when:** Smoke section filled; Result **smoke-pass** or **smoke-fail**.

**Task prompt:**

```
You are the runner for my-test-subflow Smoke (build + unit only). Fresh context only. Do not run e2e. Do not start code review here.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/templates.md>

Discover build and unit commands from package.json / project docs.

Run in order:
1. Build
2. Unit tests

Rules:
- Update 06-test-log.md → Smoke section + Mode last run: smoke.
- Result = smoke-pass only if build + unit both green.
- Otherwise Result = smoke-fail and fill Fix ask for my-code-subflow.
- Do not fix product code. Do not merge or push.
- Simple plain words.

Return: smoke-pass | smoke-fail, and path to 06-test-log.md.
```

**After:** Parent: smoke-pass → `my-review-subflow`. smoke-fail → Fix-from-tests → re-smoke.

---


## Lite test (Fast) — stage id `test-lite`

**When:** Review profile **lite** after review clean (or parent asks lite).

**Task description:** `Run build and tests`

**Done when:** targeted e2e (and unit if needed) green; Result success|failure in `06-test-log.md`.

**Task prompt:**

```
You run lite verification for my-test-subflow. Fresh context only.

<Stage-scoped handoff for test-lite from ~/.cursor/skills/my-dev-flow/templates.md>

Read 04-tasks.md for required e2e. Run the repo’s unit (if not already smoke-pass) and only e2e that match this change / tasks.
Do NOT run a coverage Task. Do NOT add broad missing e2e unless 04-tasks explicitly requires a new e2e file.
Write results into 06-test-log.md. Result: success | failure. On failure include Fix ask.
Return: Result + short summary + path.
```

---
## Coverage check — Fast

**When:** Full mode only (after review clean).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast

**Done when:** `06-test-log.md` lists covered vs missing e2e against design success criteria / main user flows.

**Task prompt:**

```
You are the verifier for my-test-subflow Coverage check. Generation ≠ verification — you judge gaps; you do not rewrite product features.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/templates.md>

Read 03-design.md (success criteria, flows) and 04-tasks.md. Scan the repo for existing e2e tests and how they are run (package.json scripts, playwright/cypress/etc.).

Rules:
- Map each success criterion / main user flow to existing e2e coverage (file + test name) or mark MISSING.
- Do not invent a new e2e framework. Note the repo’s stack, or “no e2e stack found”.
- Simple plain words.

Update 06-test-log.md → Coverage section only. Mode last run: full.

Return: covered count, missing list, e2e command if known.
```

---

## Add missing e2e — Fast

**Only if** Coverage check listed MISSING items **and** an e2e stack exists. Full mode only.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast

**Done when:** new e2e tests exist for each MISSING item (or explicitly blocked with reason).

**Task prompt:**

```
You are the Senior Developer for my-test-subflow Add missing e2e.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/templates.md>

Read 06-test-log.md Coverage section and 03-design.md / 04-tasks.md.

Rules:
- Add e2e tests only for listed MISSING flows, using the repo’s existing e2e patterns and helpers.
- Do not change product behavior here. Do not rewrite unrelated tests.
- If a gap cannot be automated safely, mark it blocked in 06-test-log.md with why.
- Simple plain words in comments.

Return: files added, which gaps closed, any still blocked.
```

If **no e2e stack**: skip this stage; parent marks failure / asks user (see SKILL.md).

---

## Run suite — Fast (full mode)

**When:** Full mode after coverage (+ optional add e2e).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast

**Done when:** build, unit, and e2e commands have been run (or skipped with explicit reason) and `06-test-log.md` Result is **success** or **failure**.

**Task prompt:**

```
You are the runner for my-test-subflow Run suite (full).

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/templates.md>

Discover commands from package.json / project docs (build, unit test, e2e). Prefer project scripts over ad-hoc commands.

Run in order:
1. Build
2. Unit tests
3. E2E tests (if stack + script exist)

Rules:
- Capture exit codes and short failure excerpts (trim huge logs).
- Update 06-test-log.md → Runs + Result. Mode last run: full.
- Result = success only if build + unit + e2e all green AND Coverage has no open MISSING/blocked required gaps.
- Otherwise Result = failure and fill “Fix ask for my-code-subflow”.
- Do not fix product code in this stage. Do not merge or push.
- Simple plain words.

Return: success | failure, and paths to log sections.
```

---

## Parent loop hint (my-dev-flow)

```
After Build → Smoke
  On smoke-fail → my-code-subflow Fix → re-smoke
  On smoke-pass → my-review-subflow
After review clean → Full test
  On failure → my-code-subflow Fix → re-full
  On success → Gate C → my-merge-subflow
After 3 test↔code rounds per mode → pause and ask the user.
```
