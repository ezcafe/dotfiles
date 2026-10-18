# Verify gate + Fix rules (shared)

**This file is SoT for:** Verify gate, Smoke after Build (Build-writes-Smoke), Fix rules.  
Used by [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) (Build, Fix-from-tests) and
[`my-dev-flow-review`](../my-dev-flow-review/SKILL.md) (Fix).  
Pipeline pointer: [stages.md](stages.md). Parent checklist: [invariants.md](invariants.md).  
Gate B veto before Build: [hitl.md](hitl.md). Hard stops: [failure-playbook.md](failure-playbook.md).  
**Lint (required) before Build:** `scripts/lint-run.py <run-dir> --before-build`.

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

## Gate B veto check (before Build coding)

Build Task **first action:** read `00-run.md` **Gate B veto**, **Gate B approved**, and Notes. Full async rules: [hitl.md](hitl.md). Aligns with [`my-dev-flow-code/stages/build.md`](../my-dev-flow-code/stages/build.md).

| Condition | Action |
|-----------|--------|
| `Gate B veto: pending` | Stop; first return line `Result: blocked — Gate B veto`; do not change code |
| HITL Gate B is **blocking** and **Gate B approved** is `none`/missing | Stop; first return line `Result: blocked — Gate B approved`; do not change code |
| Notes say veto window open **and** **Build armed** missing | Stop; first return line `Result: blocked — Build armed missing`; do not change code |
| Notes match `design-backloop` | Stop; first return line `Result: blocked — design-backloop`; do not change code |
| `Gate B veto: none` and (blocking → approved settled; auto may leave approved `none`) and (no open veto window, or **Build armed** present) and no `design-backloop` | Continue Build |

Parent must not launch Build while veto is `pending`, while blocking Gate B lacks **Gate B approved**, while veto window is open without **Build armed**, or while Notes say `design-backloop`. Lint: `scripts/lint-run.py <run-dir> --before-build`.

## Verify gate (blocking)

**When:** End of Build; end of Fix-from-tests; end of review Fix when code/tests changed.

**Pass (`verify-pass`):** Listed **build** and **unit** commands that are not N/A both exit 0. N/A steps skipped. Fix-from-tests also re-runs tests named in Failures / Fix ask until green.

**Fail (`verify-fail`):** Any required command red after the attempt budget.

**Attempt budget:** Max **3** Verify attempts per stage entry (Build or one Fix launch). Each attempt = run commands + optional in-Task fix. After 3 still red → Result **verify-fail**; parent pauses with **Decision N** ([invariants.md](invariants.md) verify-fail shape). Do not infinite-loop.

**Return (first line of Task return — required):**

```
Result: verify-pass | verify-fail
```

Then: commands run + pass/fail; what changed; risks / out of scope.

**Parent:** Advance **only** on **verify-pass**. On **verify-fail** → re-launch same stage (if attempts remain) or Decision N. Persist on Orchestrator card: Last Verify, Verify attempts, commands.

**Docs-only Fix (review):** If no code/test files changed → note `TDD skipped — no behavior` and `Verify skipped — docs only`; treat as verify-pass for advance.

## Stale review / test after rebuild (Notes tokens)

When Build **verify-pass** rewrites a draft that already had review/test Results, **or** design-backloop Option 1 invalidates prior Gate B work, parent must not treat old `05`/`06` as paid:

| Notes bullet | Meaning | Derive / `--next` / `--before-merge` |
|--------------|---------|--------------------------------------|
| `- review-stale` | Prior `05-review-log` clean (and lenses) is invalid | Re-enter review path; block gate-c/merge until cleared |
| `- test-stale` | Prior `06` success / Mode last run is invalid | Re-enter test-full/test-lite; block gate-c/merge until cleared |

Clear each token only after a fresh clean/success. Same bullet style as `design-backloop` / `tiny-contract-tweak` ([stages.md](stages.md) Design-backloop · [build.md](../my-dev-flow-code/stages/build.md)).

**Clock (fail-closed):** On verify-pass, set durable `**Last verify-pass at:**` ISO-8601 on `00-run.md` (Build After). Lint treats `05` clean / `06` success as **unpaid** when the artifact file mtime is older than that timestamp and Notes lack the matching stale token — same `--before-merge` **error** / `--next` `do-not-launch` / `--derive` re-entry as explicit Notes. Fresh re-review / re-test (file mtime ≥ clock) clears the unpaid state; then clear Notes tokens. Missing clock → Notes tokens only (no auto-detect). Not waived by `gate-c-test-override`.

**Lint:** `--next` → `handoff: do-not-launch` on gate-c/merge while either token is present **or** unpaid-vs-clock. `--before-merge` (also when Next=`merge`) → **error** for each. Playbook: [failure-playbook.md](failure-playbook.md).

## Smoke after Build (Build-writes-Smoke)

On Build **verify-pass**, Build **writes** `06-test-log.md` Smoke section (commands, exits, **Smoke result: smoke-pass**) using Verify commands.

Parent then:

| Condition | Action |
|-----------|--------|
| Smoke section complete + smoke-pass + commands match Verify commands | **Skip Smoke Task** — treat as smoke-pass; continue (review or Gate C) |
| Smoke incomplete, mismatch, or Notes `smoke re-run` | Launch Smoke Task (independent re-run) — see **skip-review ordered recovery** below |
| Review profile **skip-review** (legality: [lenses.md](lenses.md)) | Gate C test bar = Build verify-pass (+ Smoke section). Before Gate C: Notes `smoke-waive` / `smoke-pass (re-run)` / `gate-c-test-override`, **or** Complexity/Notes `docs-only` (warn/allow). Else Lint `--before-merge` **errors** when only Build-writes-Smoke (fail-closed) |

### Skip-review + Smoke ordered recovery (SoT)

When Review profile is **skip-review** and Smoke is incomplete / mismatched / needs re-proof, parent uses this order (lint `--next` aligns):

1. **Prefer re-Build** — rewrites Smoke section; stay on legal skip-review → Gate C path.
2. **Or** Notes `smoke re-run` → allow **one** Smoke Task under skip-review (exception; clear the Notes token after smoke-pass). Prefer this independent re-run once before Gate C when Build-writes-Smoke feels thin.
3. **Or** drop skip-review → **lite** → `code-review-phase` → `test-lite` → Gate C.

Do **not** launch `smoke` under skip-review without Notes `smoke re-run` (lint warn). Explicit Notes `smoke-waive` / `smoke-pass (re-run)` / `gate-c-test-override`, or Complexity/Notes `docs-only`, may skip the independent-Smoke requirement. After an independent re-run, record `smoke-pass (re-run)` (Notes or Smoke field) and clear the `smoke re-run` token. Lint `--before-merge` **errors** when skip-review has only Build-writes-Smoke without those tokens (`docs-only` → warn/allow). Independent verification for merge remains: **full** / **lite** test after review (or smoke-pass alone for Mode simple legal skip-review when waived).

## Fix rules (TDD)

- Fix only listed Fix-ask / Failures items; stay aligned with `03-design.md` / `04-tasks.md` (+ Design UI when Has UI).
- Behavior: Red → Green → Refactor → Verify, then Verify gate.
- Docs/comments only: TDD skipped note; Verify skipped when no code/tests changed.
- Append Round notes on the log being updated (`06-test-log.md` or `05-review-log.md`).
- No merge/push/commit unless user explicitly asked.
- Max **3** Fix↔re-verify cycles per mode (smoke / full / review lens), then pause.
- If Fix **cannot** stay aligned with design (contracts / IA / acceptance must change) → stop Fix; parent runs **Design-backloop** Decision N in [stages.md](stages.md) / [invariants.md](invariants.md). Do **not** silently rewrite `03-design` / `04-tasks` inside Fix.

## Orchestrator card fields (persist)

Update after every Build/Fix return:

| Field | Value |
|-------|-------|
| Last Verify | verify-pass \| verify-fail \| pending |
| Verify attempts | 0–3 (this stage entry) |
| Verify commands | short copy or “see Repo section” |
