# Verify gate + Fix rules (shared)

Used by [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) (Build, Fix-from-tests) and
[`my-dev-flow-review`](../my-dev-flow-review/SKILL.md) (Fix). Parent rules in
[stages.md](stages.md) **Build / Fix Verify gate**.

## Verify commands (00-run.md)

Before first Build (set during skim/Analyze when known; refine before Build):

```markdown
**Verify commands:**
- **cwd:** <repo root or package dir>
- **build:** `<command>` | N/A — <reason>
- **unit:** `<command>` | N/A — <reason>
- **e2e:** `<command>` | N/A — <reason>
```

Discovery: prefer project scripts in `package.json` / docs / `AGENTS.md`. Do not invent a new test stack. Monorepo: set **cwd** to the package touched by the change.

**Missing unit:** If no unit script/suite → `unit: N/A — <reason>`. Verify gate then requires **build** green only (when build exists). Do not invent a unit runner.

**Missing build:** If no build script (e.g. docs-only) → `build: N/A — <reason>`. Verify on unit only when unit exists; else verify-pass with both N/A and note in Round notes (skip-review / docs path).

Build, Fix, Smoke, and full/lite test **must** use these commands (same cwd). Do not rediscover conflicting commands.

## Verify gate (blocking)

**When:** End of Build; end of Fix-from-tests; end of review Fix when code/tests changed.

**Pass (`verify-pass`):** Listed **build** and **unit** commands that are not N/A both exit 0. N/A steps skipped. Fix-from-tests also re-runs tests named in Failures / Fix ask until green.

**Fail (`verify-fail`):** Any required command red after the attempt budget.

**Attempt budget:** Max **3** Verify attempts per stage entry (Build or one Fix launch). Each attempt = run commands + optional in-Task fix. After 3 still red → Result **verify-fail**; parent pauses with **Decision N** (narrow scope / user waive / stop). Do not infinite-loop.

**Return (first line of Task return — required):**

```
Result: verify-pass | verify-fail
```

Then: commands run + pass/fail; what changed; risks / out of scope.

**Parent:** Advance **only** on **verify-pass**. On **verify-fail** → re-launch same stage (if attempts remain) or Decision N. Persist on Orchestrator card: Last Verify, Verify attempts, commands.

**Docs-only Fix (review):** If no code/test files changed → note `TDD skipped — no behavior` and `Verify skipped — docs only`; treat as verify-pass for advance.

## Smoke after Build (Option B)

On Build **verify-pass**, Build **writes** `06-test-log.md` Smoke section (commands, exits, **Smoke result: smoke-pass**) using Verify commands.

Parent then:

| Condition | Action |
|-----------|--------|
| Smoke section complete + smoke-pass + commands match Verify commands | **Skip Smoke Task** — treat as smoke-pass; continue (review or Gate C) |
| Smoke incomplete, mismatch, or Notes `smoke re-run` | Launch Smoke Task (independent re-run) |
| Review profile **skip-review** | Gate C test bar = Build verify-pass (+ Smoke section). No Smoke Task required |

Independent verification for merge remains: **full** / **lite** test after review (or smoke-pass alone for skip-review).

## Fix rules (TDD)

- Fix only listed Fix-ask / Failures items; stay aligned with `03-design.md` / `04-tasks.md` (+ Design UI when Has UI).
- Behavior: Red → Green → Refactor → Verify, then Verify gate.
- Docs/comments only: TDD skipped note; Verify skipped when no code/tests changed.
- Append Round notes on the log being updated (`06-test-log.md` or `05-review-log.md`).
- No merge/push/commit unless user explicitly asked.
- Max **3** Fix↔re-verify cycles per mode (smoke / full / review lens), then pause.

## Orchestrator card fields (persist)

Update after every Build/Fix return:

| Field | Value |
|-------|-------|
| Last Verify | verify-pass \| verify-fail \| pending |
| Verify attempts | 0–3 (this stage entry) |
| Verify commands | short copy or “see Repo section” |
