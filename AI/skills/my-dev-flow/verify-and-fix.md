# Verify gate + Fix rules (shared)

**This file is SoT for:** Verify gate, Smoke after Build (Build-writes-Smoke), Fix rules.  
Used by [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) (Build, Fix-from-tests) and
[`my-dev-flow-review`](../my-dev-flow-review/SKILL.md) (Fix).  
Pipeline pointer: [stages.md](stages.md). Launch-time checklist: [orchestrator-rules.md](orchestrator-rules.md). Decision shapes / detailed checklist body: [invariants.md](invariants.md).  
Gate B veto before Build: [hitl-gate-b.md](hitl-gate-b.md). Gate C bar: [hitl-gate-c.md](hitl-gate-c.md). Hard stops: [failure-playbook.md](failure-playbook.md).  
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

Build Task **first action:** read `00-run.md` **Gate B veto**, **Gate B approved**, and Notes. Full async rules: [hitl-gate-b.md](hitl-gate-b.md). Aligns with [`my-dev-flow-code/stages/build.md`](../my-dev-flow-code/stages/build.md).

| Condition | Action |
|-----------|--------|
| `Gate B veto: pending` | Stop; first return line `Result: blocked — Gate B veto`; do not change code |
| HITL Gate B is **blocking** and (**Gate B approved** is `none`/missing **or** provenance `gate-b-approved` missing/weak) | Stop; first return line `Result: blocked — Gate B approved`; do not change code |
| Notes say veto window open **and** **Build armed** missing | Stop; first return line `Result: blocked — Build armed missing`; do not change code |
| Notes veto window + **Build armed** but async gap incomplete (arm not later than digest / missing `async-gap-pending` / no `.lint-async-gap`) | Stop; first return line `Result: blocked — async gap incomplete`; do not change code |
| Notes match `design-backloop` | Stop; first return line `Result: blocked — design-backloop`; do not change code |
| `Gate B veto: none` and (blocking → approved settled **+ quality provenance**; auto may leave approved `none`) and (no open veto window, or **Build armed** + complete async gap) and no `design-backloop` | Continue Build |

Parent must not launch Build while veto is `pending`, while blocking Gate B lacks **Gate B approved** **+ quality provenance**, while veto window is open without **Build armed**, or while Notes say `design-backloop`. Lint: `scripts/lint-run.py <run-dir> --before-build`.

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

**Parent:** Advance **only** on **verify-pass**. On **verify-fail** → re-launch same stage (if attempts remain) or Decision N. Persist on Orchestrator card: Last Verify, Verify attempts, commands. **Lint derive (H1):** when Last Verify ≠ `verify-pass` and Last stage is **not** Build / pre-Build, `--derive` must **not** return `build` / `gate-b`. Map post-Build Last stage → Fix / same-stage (same-stage retry — [resume-abort.md](resume-abort.md)):

| Last stage | Derive |
|------------|--------|
| `fix-tests` / `fix-review` | same stage |
| `smoke` / `test-lite` / `test-full` | `fix-tests` |
| `adversarial` / `quality` / `code-review-phase` / `lens-*` / `merge-findings` | `fix-review` |
| Build / pre-Build (`tdd-review`, `gate-b`, design… ) | existing pre-Build fall-through |

Pre-Build fall-through applies only when Last stage is Build / pre-Build.

**Docs-only Fix (review):** If no code/test files changed → note `TDD skipped — no behavior` and `Verify skipped — docs only`; treat as verify-pass for advance.

## Stale review / test after rebuild (Notes tokens)

When Build **verify-pass** rewrites a draft that already had review/test Results, **or** design-backloop Option 1 invalidates prior Gate B work, parent must not treat old `05`/`06` as paid:

| Notes bullet | Meaning | Derive / `--next` / `--before-merge` |
|--------------|---------|--------------------------------------|
| `- review-stale` | Prior `05-review-log` clean (and lenses) is invalid | Re-enter review path; block gate-c/merge until cleared |
| `- test-stale` | Prior `06` success / Test path last run is invalid | Re-enter test-full/test-lite; block gate-c/merge until cleared |

Clear each token only after a fresh clean/success. Same bullet style as `design-backloop` / `tiny-contract-tweak` ([design-backloop.md](design-backloop.md) · [build.md](../my-dev-flow-code/stages/build.md)).

**Clock (fail-closed):** On verify-pass, set durable `**Last verify-pass at:**` ISO-8601 on `00-run.md` (Build After). Lint treats `05` clean / `06` success as **unpaid** when the artifact file mtime is older than that timestamp and Notes lack the matching stale token — same `--before-merge` **error** / `--next` `do-not-launch` / `--derive` re-entry as explicit Notes. Fresh re-review / re-test (file mtime ≥ clock) clears the unpaid state; then clear Notes tokens. Missing clock → Notes tokens only (no auto-detect). Not waived by `gate-c-test-override`.

**Lint:** `--next` → `handoff: do-not-launch` on gate-c/merge while either token is present **or** unpaid-vs-clock. `--before-merge` (also when Next=`merge`) → **error** for each. Playbook: [failure-playbook.md](failure-playbook.md).

## Smoke after Build (Build-writes-Smoke)

### Build-writes-Smoke claim

On Build **verify-pass**, Build **writes** `06-test-log.md` Smoke section (commands, exits, **Smoke result: smoke-pass**) **and** **Test path last run:** `smoke` (same field the Smoke Task sets — [smoke.md](../my-dev-flow-test/stages/smoke.md)) using Verify commands.

Build-writes-Smoke is a **claim from the Build Task**, not an independent Smoke Task (generation ≠ verification). Keep the skip habit for tiny / Mode simple / Mode full + Review profile **lite**. Do **not** rename Build’s Smoke section to `smoke-claim` (breaks skip-review fail-closed contracts). Mode full forbids skip-review.

### Mode full + profile full (E1 independent Smoke)

Lint **requires** an independent Smoke path before Adv / `code-review-phase`:

1. Parent adds Notes `smoke re-run` **once** → `--next --derive` returns `smoke` → launch Smoke Task
2. Smoke Task updates `06-test-log.md` Smoke section (Result smoke-pass) **after** Build verify-pass / **Last verify-pass at**; parent logs Run log stage `smoke`
3. Parent records Notes `smoke-pass (re-run)` → clear `smoke re-run` → continue Adv → Quality → `test-full`

Provenance `smoke-pass-rerun` is **not** required for this E1 path (that kind is skip-review Gate C only — [hitl.md](hitl.md)). Writing Notes `smoke-pass (re-run)` still flips the consent fingerprint — append Run log `parent consent write` when a snap exists. Bare Notes alone are forgeable and **do not** unlock Adv / Quality / `test-full` / `fix-tests` / `gate-c`. Presence of `05-review-log` does **not** waive E1.

### Lint / evidence rules (E1)

- **When:** `--next` / `--before-code-review` (**auto** only when Next ∈ Adv / `code-review-phase` — [scripts/README.md](scripts/README.md)) **error** if Mode full + profile full + verify-pass + Build smoke-pass **without** independent Smoke evidence. E1 also applies when Next ∈ `FULL_PROFILE_E1_GATE_STAGES` (Quality / lenses / `test-full` / `fix-tests` / `merge` / `gate-c` / …).
- **Derive:** returns `smoke` until Notes `smoke-pass (re-run)` **and** Smoke-stage evidence (Run log stage `smoke` and/or 06 Smoke section mtime after **Last verify-pass at** with Result smoke-pass).
- **Smoke-pass evidence:** prefer `**Smoke result:** smoke-pass`. When `## Smoke` exists, do **not** treat top-level `**Result:** smoke-pass` as paid. Legacy top-level fallback only when no `## Smoke` section.
- **Test Result:** first `**Result:**` **outside** `## Smoke` — Smoke-section `**Result:** smoke-pass` must not mask top-level `failure`.
- **M1 smoke-fail:** `06` Smoke Result `smoke-fail`|`failure` → derive `fix-tests` (not `smoke` / not `build` under skip-review). Unpaid/missing Smoke → `smoke` (or `build` under skip-review). Top-level test `failure` with Smoke `smoke-pass` → `fix-tests` via test-failure path.
- **After Fix:** Last stage=`fix-tests` + Last Verify=`verify-pass` unlocks re-smoke / re-test even if 06 still holds failure tokens. Next=`fix-tests` while derived is `smoke`/`test-*` → **unsafe** / `do-not-launch`. Smoke-fail→`fix-tests` JUMP_AHEAD exception only when Last stage ≠ `fix-tests`.
- **M2 conflict:** Smoke-section smoke-pass + smoke-fail|failure → fail-closed. Card Next ∈ jump-ahead-from-smoke while derived=`smoke` → **unsafe** ([parent-next.md](parent-next.md)), except legitimate smoke-fail→Fix.

### Parent action table

| Condition | Action |
|-----------|--------|
| Smoke section complete + smoke-pass + commands match Verify commands | **Skip Smoke Task** when Mode simple / Mode full + profile **lite** / tiny — continue (review or Gate C). **Exception:** Mode full + profile full → independent Smoke first (above) |
| Smoke incomplete, mismatch, Notes `smoke re-run`, or Mode full + profile full E1 unpaid | Launch Smoke Task — see skip-review recovery below when profile is skip-review |
| Review profile **skip-review** (legality: [lenses.md](lenses.md)) | Gate C escape **with provenance** — [hitl-gate-c.md](hitl-gate-c.md). Bare waiver tokens rejected. Else `--before-merge` **errors** on Build-writes-Smoke alone |

### Skip-review + Smoke ordered recovery (SoT)

When Review profile is **skip-review** and Smoke is incomplete / mismatched / needs re-proof **or** Gate C needs independent proof (lint `--next` aligns; [stages.md](stages.md) Simple (a)):

1. **Prefer Notes `smoke re-run` once** — one Smoke Task under skip-review; clear token after smoke-pass. Do this **before** re-Build or Gate C waivers when Build-writes-Smoke alone is thin.
2. **Or re-Build** — rewrites Smoke section; stay on legal skip-review → Gate C (after step 1 if still needed).
3. **Or** drop skip-review → **lite** → `code-review-phase` → `test-lite` → Gate C.
4. **Waivers last** — Notes `smoke-waive` / `gate-c-test-override` / `docs-only` **each with parent-written provenance** ([hitl.md](hitl.md)).

**smoke-fail → Fix vs re-Build:** `06` Smoke Result `smoke-fail`|`failure` → derive `fix-tests` (not `build`) even under skip-review ([results.md](results.md)). Parent may still **choose** re-Build from ordered recovery. Unpaid/missing Smoke under skip-review still derives `build`.

Do **not** launch `smoke` under skip-review without Notes `smoke re-run` (`--next` → `do-not-launch`). Do **not** launch `test-full` / `test-lite` under legal skip-review. Escapes that skip independent Smoke must match [hitl-gate-c.md](hitl-gate-c.md) / [hitl.md](hitl.md) Provenance. After independent re-run: **parent** records `smoke-pass (re-run)` **plus** provenance `smoke-pass-rerun`, then clear `smoke re-run`. Lint `--before-merge` **errors** when skip-review has only Build-writes-Smoke without those escapes; `docs-only` warn/allow only after provenance. Independent verification for merge: **full** / **lite** test after review (or Gate C escape + provenance for Mode simple legal skip-review).

## Fix rules (TDD)

- Fix only listed Fix-ask / Failures items; stay aligned with `03-design.md` / `04-tasks.md` (+ Design UI when Has UI).
- Behavior: Red → Green → Refactor → Verify, then Verify gate.
- Docs/comments only: TDD skipped note; Verify skipped when no code/tests changed.
- Append Round notes on the log being updated (`06-test-log.md` or `05-review-log.md`).
- No merge/push/commit unless user explicitly asked.
- Max **3** Fix↔re-verify cycles per mode (smoke / full / review lens), then pause.
- If Fix **cannot** stay aligned with design (contracts / IA / acceptance must change) → stop Fix; parent runs **Design-backloop** Decision N in [design-backloop.md](design-backloop.md) / [invariants.md](invariants.md). Do **not** silently rewrite `03-design` / `04-tasks` inside Fix.

## Orchestrator card fields (persist)

Update after every Build/Fix return:

| Field | Value |
|-------|-------|
| Last Verify | verify-pass \| verify-fail \| pending |
| Verify attempts | 0–3 (this stage entry) |
| Verify commands | short copy or “see Repo section” |
