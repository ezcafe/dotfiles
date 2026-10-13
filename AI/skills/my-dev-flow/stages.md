# my-dev-flow stage index (canonical)

`my-dev-flow` is an **orchestrator only**. Stage prompts live in the subflows.
This file is the **source of truth** for pipeline order, Mode, HITL, lenses, models, and progress.

**Progress:** Cursor subagent card = live status (no “now running…” banners).  
**After each step:** ≤5 lines summary + full path; read Result header only (~40 lines); update Orchestrator card.  
**HITL:** Gate B `auto` | `async-notify` | `blocking`. **Gate C always blocking.** **HITL Grill** is independent of Gate B (defaults below). Gate digest ≤4 bullets. User-first picks on auto/async.  
**File also:** Run log + Last stage + Orchestrator card + Last Verify.  
**Chat OK:** post-step summary + path, human gates, Decision N, stop, finish.  
**Subagent context:** every Task starts fresh — [handoffs.md](handoffs.md) stage id only.  
**Verify / Fix:** [verify-and-fix.md](verify-and-fix.md).  
**Legacy removals:** [LEGACY.md](LEGACY.md).  
**Severity exit:** [severity.md](severity.md) (Critical/Major block clean; defer Enhancement).  
**Skill paths:** [skills-path.md](skills-path.md) — SoT `AI/skills/`; sync via `AI/skills/sync-to-cursor.sh`.

## Happy path (runtime SoT)

**Mode full:**

```
Step 0 → Ideation → Gate A → skim → Analyze → Grill → Design
  → API∥DB (parallel when both) → design-review clean → 04a?
  → Gate B → Build (verify-pass + Smoke section) → Smoke skip?
  → review clean → test-full → Gate C → merge
```

**Mode simple:**

```
Step 0 → design-phase → design-verify-phase clean → 04a? → Gate B
  → Build (verify-pass + Smoke section)
  → skip-review? → Gate C
  : else → code-review-phase → test-lite → Gate C → merge
```

After Build, always: **Smoke → review → test → Gate C** (unless skip-review jumps to Gate C on verify-pass + Smoke section).

If Build/Fix proves design wrong → [Design-backloop](#design-backloop-after-build).

---

## Skill inventory (not runtime order)

Parent SKILL.md lists skills as inventory. This table maps **phase → skill files** only — do **not** use row order as pipeline order (see Happy path above).

| Phase | Skill | Stages file | When in pipeline |
|-------|--------|-------------|------------------|
| Design | [`../my-dev-flow-design/SKILL.md`](../my-dev-flow-design/SKILL.md) | [`../my-dev-flow-design/stages.md`](../my-dev-flow-design/stages.md) | Before design-review / Build |
| Design review | [`../my-dev-flow-design-review/SKILL.md`](../my-dev-flow-design-review/SKILL.md) | [`../my-dev-flow-design-review/stages.md`](../my-dev-flow-design-review/stages.md) | After Design; again on design-backloop |
| Code | [`../my-dev-flow-code/SKILL.md`](../my-dev-flow-code/SKILL.md) | [`../my-dev-flow-code/stages.md`](../my-dev-flow-code/stages.md) | After Gate B; Fix anytime post-Build |
| Smoke (re-run) | [`../my-dev-flow-test/SKILL.md`](../my-dev-flow-test/SKILL.md) | [`../my-dev-flow-test/stages.md`](../my-dev-flow-test/stages.md) | Right after Build when Option B skipped |
| Review | [`../my-dev-flow-review/SKILL.md`](../my-dev-flow-review/SKILL.md) | [`../my-dev-flow-review/stages.md`](../my-dev-flow-review/stages.md) | After Smoke; **before** full/lite test |
| Full / lite test | [`../my-dev-flow-test/SKILL.md`](../my-dev-flow-test/SKILL.md) | [`../my-dev-flow-test/stages.md`](../my-dev-flow-test/stages.md) | After review clean |
| Merge | [`../my-dev-flow-merge/SKILL.md`](../my-dev-flow-merge/SKILL.md) | [`../my-dev-flow-merge/stages.md`](../my-dev-flow-merge/stages.md) | After Gate C yes |

---

## Slug

Format: **`YYYYMMDD-feature-x`** (UTC calendar date + short kebab-case feature).

Examples: `20261005-offline-care-log`, `20261005-fix-login-timeout`.

Folder: `.my-docs/workflow/<slug>/`.

---

## Cheap path matrix (classify faster)

| Ask looks like | Mode | Review profile |
|----------------|------|----------------|
| Copy / token / docs-only | simple | skip-review |
| Bug fix / one helper / one field / tiny UI match | simple | lite |
| Clear small feature, no new auth/schema | simple | lite |
| New/changed public API or persistence shape | full (or simple if tiny + clear) | full or lite; set Has API/DB |
| Ambiguous product / multi-surface / invent *what* | full | full |

Ambiguous → Decision N (simple vs full). Do not guess.

---

## Step 0 — Classify + resolve models + create run

Parent / main agent (no Task unless classifying is ambiguous):

1. **Overrides:** resume keeps Mode + Review profile; user said `simple` / `full` / `skip-review` → that Mode/profile.
2. Else **classify** (table below + cheap path matrix). Ambiguous → Decision N.
3. Create slug `YYYYMMDD-feature-x`; write `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md): Mode, Review profile, Complexity, Has UI/API/DB when known, **Lens plan: none**, resolve models, Orchestrator card, HITL Gate B (refine after Design), **HITL Grill** (full → async-notify; simple → auto), **HITL Gate C: blocking**. Verify commands may stay empty until skim/Analyze/`design-phase`.  
4. Chat one line: Mode + Review profile + why (+ note phase bundles when Mode simple).

### Mode selection

| Signal | Prefer **simple** | Prefer **full** |
|--------|-------------------|-----------------|
| Scope | Bug fix, small tweak, copy/token, one helper, one field/API | New feature, multi-surface UX, new product concept |
| Clarity | Outcome clear in the ask | Needs discovery / day-to-day / 80/20 |
| Framing | Thin idea can be written from the ask, or framing already done | Needs Ideation → Gate A → skim |
| Risk | Low blast radius; no new auth/data-model shape | Cross-cutting auth, schema, multiple apps |
| UI | No UI, copy/token, or tiny layout match | New or redesigned multi-surface UX (in Design; no UI concept step) |

**Rule of thumb:** if Ideation→Gate A→skim would rubber-stamp a clear ask → **simple**. If the team must invent *what* to build → **full**.

### Review profile

| Profile | When | After Build verify-pass |
|---------|------|-------------------------|
| **full** | Mode full | Smoke skip or re-run → Adversarial → Quality → Conditional lenses → **test-full** |
| **lite** | Mode simple default | Smoke skip or re-run → **must** `code-review-phase` (Lite combined) → **test-lite** |
| **skip-review** | Mode simple + copy/token/docs-only or user said skip-review | Gate C test bar = Build **verify-pass** (+ Smoke section); skip Smoke Task + code review + further tests → Gate C |

### Mid-run reclassify

If scope grows (Has API/DB flips to **yes**, auth/PII appears, multi-surface UX, or blast radius jumps):

1. Pause with **Decision N**: stay simple vs upgrade to **full** (optional reopen Gate A / skim).
2. Record pick in Notes + Run log. Do not silently stay on skip-review when contracts or persistence appear.

---

## HITL (Gate B / Gate C)

| Tier | Behavior | Allowed for |
|------|----------|-------------|
| **auto** | Approve without waiting. Gate digest + user-first picks. | Gate B only |
| **async-notify** | Post Gate digest + user-first pick; **continue immediately**. Human may veto in the **next user message**. If that message rejects/changes the pick → Status `stopped` or apply the veto and re-open Gate B. Silence after continue is **not** a veto. | Gate B only |
| **blocking** | Pause for approve / reject. Gate digest ≤4 bullets. | Gate B; **required** for Gate C |

**Default Gate B:** prefer **auto** or **async-notify** when Mode simple + design-review clean + (04a ok|skipped) + Has API no + Has DB no. Prefer **blocking** when Mode full, Has API/DB yes, open Critical/Major, or auth/PII/security in scope.

**Gate digest:** (1) what ships (2) top risks ≤3 (3) what verified (4) ask or auto-pick note / Gate C commit-push-PR-merge ask.

**User-first auto picks:** day-to-day user value first, then system convenience; log `auto-pick — Decision N Option K — user-first: …; system: …`.

**Git / remote (hard):** no `git commit` / `git push` / `gh pr create` / `gh pr merge` without explicit yes naming each action. Reject / silence at Gate C → stop. Gate B auto ≠ commit approval.

**async-notify example:** Gate B posts digest + auto-pick “Option 1 — ship thin API first”; pipeline continues to Build. User’s **next** message says “stop — use Option 2 instead” → Status `stopped` or re-open Gate B with veto; a later message that only says “looks good” is **not** a veto if the pipeline already moved on.

**async-notify veto after Build started:** Do not silently continue to review. Pause with **Decision N**:

| Option | What |
|--------|------|
| 1 | Discard draft; re-open Gate B with veto pick |
| 2 | Keep draft; re-open Gate B (amend design/tasks only) |
| 3 | Stop (Status `stopped`) |

**HITL Grill (independent of Gate B):**

| Mode | Default Grill tier |
|------|--------------------|
| **full** | `async-notify` (prefer human-visible picks; blocking when auth/PII/schema forks) |
| **simple** | `auto` |

Do **not** copy Gate B tier into Grill unless `00-run.md` explicitly sets them equal. See [grill.md](grill.md).

**Gate C test bar (before merge subflow):**

| Review profile | Required |
|----------------|----------|
| **skip-review** | Build **verify-pass** + Smoke section smoke-pass (no Smoke Task / full / lite required) |
| **lite** | `06-test-log.md` Result **success** after lite run |
| **full** | `06-test-log.md` Result **success** after full run |

Explicit user override may waive green tests; log override in Notes.

---

## Resume (mid-run)

When the user says **resume** / continues an existing slug:

1. Read `00-run.md` only: **Status**, **Last stage**, **Orchestrator card**, checked **Gates**, **Review profile**, **Mode**.
2. Do **not** re-classify Mode unless the user asked to reclassify or scope changed (Decision N).
3. Do **not** redo completed gates unless artifacts for that gate changed (e.g. new Fix ask after design-review).
4. Next step = first incomplete row in **Full/Simple pipeline order** below, or the card’s **Next step** if it matches.
5. Load **one** subflow `SKILL.md` for the current phase only; Task prompt = handoffs row + subflow `stages.md` section.
6. If Status is `stopped`, require a new user Decision before continuing.

---

## Has API / Has DB (force yes|no before design-review)

Set during Analyze/Design (or earlier if obvious). **Before design-review**, parent must set **yes|no** (not unknown):

- Unknown + Design has API contracts / public handlers → **Has API = yes**
- Unknown + Design has DB contracts / migrations / persistence writes → **Has DB = yes**
- Else → **no**

| Flag | Yes when | When yes, parent must |
|------|----------|------------------------|
| **Has API** | New/changed REST/GraphQL/routes/server actions, edge validators, cross-boundary public types | Full: isolated **API contract review** Task (∥ DB when both). Simple: include in **design-verify-phase**. Always include **api** in Lens plan |
| **Has DB** | New/changed tables/columns/indexes/migrations/ORM, notable writes/transactions/raw SQL | Full: isolated **DB design review** Task (∥ API when both). Simple: include in **design-verify-phase**. Always include **db** in Lens plan |

Independent flags. Skills: [`api-and-interface-design`](../api-and-interface-design/SKILL.md), [`database-and-data-model`](../database-and-data-model/SKILL.md).

---

## Conditional lenses / Lens plan

Before code review, set **Lens plan** in `00-run.md`. Launch only matching lenses. (Legacy: **SPM plan** / stage ids `spm-*` — prefer **Lens plan** / `lens-*`; see [LEGACY.md](LEGACY.md).)

**Default: `none`.** Start with **none**. Add a lens only when a signal below is clearly true (or Has API / Has DB forces api/db). Do not pre-load security/perf/memory “just in case.”

| Lens | Stage id | Launch when |
|------|----------|-------------|
| **API** | `lens-api` | Has API = yes, or new/changed public contracts / edge validators |
| **DB** | `lens-db` | Has DB = yes, or new/changed schema/migrations/persistence queries |
| **Security** | `lens-security` | auth, sessions, PII, uploads, SQL/raw, secrets, permissions |
| **Performance** | `lens-perf` | lists/tables, charts, fetch, bundle-sensitive UI, heavy client compute |
| **Memory** | `lens-memory` | subscriptions, large client caches, websockets/realtime, media buffers |

- **none** → after Quality / Lite combined clean, skip lenses → test per Review profile  
- **1 lens** → that lens only; parent copies Result into Merged lenses (no Merge Task)  
- **2+ lenses** → **must** launch in parallel → Merge findings Task  

API lens → `05-lens-api.md`. DB lens → `05-lens-db.md`.

---

## TDD test-case review (Step 4a)

Run `04a` **only if** `04-tasks.md` lists concrete tests to create. Else Notes `04a skipped — no planned test cases`; do not invent `04a`.

---

## Speed defaults (latency)

Keep quality rails; cut **Task cold starts**.

| Rule | Mode **simple** | Mode **full** |
|------|-----------------|---------------|
| Design chain | **One** Task `design-phase` (Analyze + Grill/skip + Design) | Separate Analyze → Grill → Design |
| Design verify | **One** Task `design-verify-phase` (general + API/DB sections when flagged) | Isolated API ∥ DB (**must** parallel when both) → then general design-review |
| Code review | **Must** `code-review-phase` / Lite combined when profile **lite** | Separate Adversarial → Quality → lenses |
| Full test | n/a (use lite test) | **One** Task `test-full` (coverage + add e2e + run) |
| Lens plan default | **none** (add only on signals) | **none** then add signals |
| Mechanical model | Prefer **Fast** (see Models) | Medium when available; Fast if Medium missing |

**API ∥ DB:** When both Has API and Has DB are yes, parent **must** launch both isolated Tasks in the **same** turn (parallel). Never serial API-then-DB. Mode simple folds them into `design-verify-phase` instead.

## Full pipeline order

1. Step 0 — Mode full; Review profile full; models + card + HITL; Lens plan default **none**  
2. Step 1 — Ideation (set Has UI)  
3. Gate A — day-to-day + 80/20 → `01a` (auto when ok; max 3 update rounds)  
4. Step 1s — Light skim → `02-skim.md`  
5. Steps 2–3 — Analyze → Grill (or skip) → Design (two options); refine Has API/DB; UI in Design  
6. Design ↔ review until clean — when Has API **and** Has DB: **must** parallel API ∥ DB, then general; max 3  
7. Step 4a — TDD only if planned tests  
8. Gate B — HITL tier + digest  
9. Step 4 — Build (**Verify gate** → `verify-pass`; write Smoke section; max 3 attempts)  
10. Step 4s — Smoke Task **skipped** when Build wrote smoke-pass (Option B); else Smoke re-run; fail → Fix → verify-pass → re-smoke  
11. Set Lens plan (default none) → Steps 5–9 review ⇄ Fix (**verify-pass** before re-review; max 3 Fix rounds)  
12. Step `test-full` — **one** Task (coverage + missing e2e + run) ⇄ Fix (max 3; Fix must **verify-pass** before re-test)  
13. Gate C — blocking → merge only after yes  

## Simple pipeline order

Starts at Analyze. Skip Ideation / Gate A / skim. Prefer **phase bundles** (fewer Tasks).

1. Step 0 — Mode simple; Review profile lite|skip-review; Lens plan default **none**; bootstrap `01-idea` if needed  
2. Step `design-phase` — Analyze + Grill (or skip) + Design (one recommended design); set Verify commands + Has API/DB  
3. Step `design-verify-phase` — design-review (+ API/DB sections when flagged) until clean; max 3 Update ↔ verify rounds  
4. 4a if planned → Gate B → Build (**verify-pass** + Smoke section)  
5. skip-review → Gate C (verify-pass + Smoke section bar); else Smoke skip → **must** `code-review-phase` (Lite combined) → lite test → Gate C  


### Build / Fix Verify gate

Canonical rules: [verify-and-fix.md](verify-and-fix.md).

- Set **Verify commands** on `00-run.md` before Build.  
- Build / Fix → **verify-pass** (max 3 attempts) before parent advances; persist Last Verify on card.  
- Build **writes** Smoke section on verify-pass → parent **skips Smoke Task** by default (Option B).  
- skip-review: Gate C bar = Build verify-pass (+ Smoke section).  
- full/lite after review remain independent verification for merge.  
- Task return **first line:** `Result: verify-pass | verify-fail`.

**Grill:** Mode full always (unless frontier-empty). Mode simple when frontier open or Has API/DB; else skip. HITL Grill independent of Gate B. See [grill.md](grill.md).

---

## Models (resolve once)

Resolve from the **current Task model allowlist** (not a frozen hardcoded list). Soft preferred hints may go stale — allowlist wins.

| Tier | Used by | How to pick from allowlist |
|------|---------|----------------------------|
| **High** | Analyze; Design; Update from design review; **simple** `design-phase` | First slug matching high/thinking-high preference; else any High-tier; else Medium → Fast → `inherit` |
| **Medium** | Ideation; Mode **full** judgment stages when available | First Medium-tier slug; else Fast → `inherit` |
| **Fast** | Build/Fix/Smoke/Test/Merge; **Mode simple** mechanical + lite review; mechanical when Medium missing | First Fast-tier slug (hint: `composer-2.5-fast` if listed); else `inherit` |

**Soft preferred hints** (use only when present in allowlist): High `claude-sonnet-5-5-high` → `claude-fable-5-1-thinking-high`; Medium `claude-opus-5-5-medium`; Fast `composer-2.5-fast`.

**Mechanical stages:** Gate A, skim, grill, design-review, design-verify-phase, API/DB contract review, TDD review, Adversarial, Quality, Lite combined / code-review-phase, lenses, Merge findings.

**Fast-on-simple:** When Mode is **simple**, mechanical stages and lite review **prefer Fast** even if Medium is on the allowlist (cut latency). Mode **full** still prefers Medium for those stages when available; use Fast only when Medium is missing.

**Mode full mechanical** (use Fast when Medium missing): same mechanical list as above.

At start: resolve once; write slugs into `00-run.md`; note fallbacks. Re-resolve if allowlist changes mid-run. Only ask user if **no** Task can launch.

### Usage-limit fallback (per stage)

When a Task hits a usage limit / rate limit / quota / capacity error:

1. Do **not** stop the pipeline.  
2. Wait **5 seconds** → retry **once** same model. Log `usage-limit retry — <stage> — waited 5s`.  
3. If still limited → retry **once** with model **`inherit`** (same prompt/description). Log `usage-limit retry — <stage> — inherit model`.  
4. If inherit succeeds → continue; later stages use resolved tier models again.  
5. If inherit still fails → **main-thread** for **that stage only**. Log `main-thread fallback — <stage> — usage limit after inherit`.  
6. Next stages still launch as Tasks. Do not permanently disable subagents.

---

## Abort / scope-change

- User rejects a gate → **stop the whole flow**. Status `stopped`.  
- User says stop / abort / cancel → Status `stopped`; Notes: frozen stage + reason.  
- User changes scope mid-run → Decision N (reclassify / new slug / continue with amended idea). Do **not** treat “continue the pipeline” as Gate C approval.  
- Silence at a **blocking** gate → stay paused (do not invent approval).
- Build/Fix cannot stay aligned with design → [Design-backloop](#design-backloop-after-build) (do not silently rewrite `03-design` inside Fix).

---

## Design-backloop after Build

**When (any of):**

- Fix ask / verify-fail shows the draft **cannot** stay aligned with `03-design.md` / `04-tasks.md` without changing contracts, IA, or acceptance.
- Review (or a lens) finds **Major/Critical** that requires design/contract change, not a local code patch.
- Parent or user says the approved design is wrong after Build started.

**Do not:** silently amend `03-design` / `04-tasks` inside Build or Fix; do not continue to Gate C.

**Pause with Decision N** (handoffs.md shape). Fixed options:

| Option | What it is | Example | Pros | Cons |
|--------|------------|---------|------|------|
| **1 — Amend design** | Update design docs → design-review (or design-verify-phase) until clean → re-open Gate B → then Fix or rebuild | API shape wrong; change `03-design` contracts first | Keeps design↔code lock | Extra rounds / latency |
| **2 — Fix-only** | Stay on current design; Fix code/tests only under existing contracts | Bug in implementation; design still right | Fast | Wrong if design is actually wrong |
| **3 — Stop** | Status `stopped`; freeze stage + reason | Scope unclear; need human rethink | Safe | Pipeline paused |

**Recommendation default:** Option **1** when contracts/IA/acceptance must change; Option **2** when only implementation drifts; Option **3** when the user rejects continuing.

**After Option 1:** Run log `design-backloop — amend design`; clear or amend Gate B check as needed; do **not** treat prior Gate B as still valid for the new design. Resume at design-update / design-review, then Gate B, then Fix or Build as appropriate.

**async-notify Gate B veto after Build** still uses the separate discard / keep / stop Decision in HITL (above). Design-backloop is for **design invalidation**, not Gate B veto alone.

---

## Subagent context

1. One new Task per **stage id** (no `resume` across different stage ids). Mode **simple** phase bundles (`design-phase`, `design-verify-phase`, `code-review-phase`) and Mode **full** `test-full` are single stage ids that cover multiple former micro-steps.  
2. Prompt = stage-scoped handoff + stage rules + user decisions.  
3. Absolute paths under `.my-docs/workflow/<slug>/`.  
4. Task return = only handoff back.  
5. Update Orchestrator card after each step. Optional: increment **Task count** in Run metrics.

---

## Decision options

Any 2+ choice: **Decision N** + Option 1/2… with What it is / Example / Pros / Cons / Recommendation — see [handoffs.md](handoffs.md).  
**Grill exception:** binary grill frontier Qs may use grill Q format alone when logged in `02b-grill.md` (see grill.md).

---

## Gates

| Gate | When | Who |
|------|------|-----|
| **Gate A** | After Ideation (full) | User-role Task → `01a`; auto when ok |
| **Gate B** | After design-review (+ 04a if any); before Build | HITL tier; skim System design / Design patterns when blocking |
| **Gate C** | Before commit/push/PR/merge | Always blocking; name each action |

---

## Progress visibility

After every stage: Result header only → **≤5 lines** summary + path → update card → continue or pause.

**Orchestrator card uses stage ids** (handoffs.md). Legacy Step labels below are aliases only.

| Stage id (prefer) | Alias | Path |
|-------------------|-------|------|
| (classify) | Step 0 | `00-run.md` |
| `ideation` | Step 1 | `01-idea.md` |
| `gate-a` | Gate A | `01a-idea-ui-review.md` |
| `skim` | Step 1s | `02-skim.md` |
| `analyze` / `design-phase` | Step 2 | `02-analysis.md` (+ design bundle on simple) |
| `grill` | Step 2g | `02b-grill.md` or skip note |
| `design` / `design-phase` | Step 3 | `03-design.md` + `04-tasks.md` |
| `design-review` / `api-contract-review` / `db-design-review` / `design-verify-phase` | — | `03a-*` |
| `tdd-review` | Step 4a | `04a-tdd-test-review.md` or skip note |
| Gate B | — | digest + HITL |
| `build` | Step 4 | key code paths |
| `smoke` | — | `06-test-log.md` Smoke (re-run only; usually skipped) |
| `adversarial` / `quality` / `code-review-phase` / `lens-*` / `merge-findings` | Steps 5–9 | `05-review-log.md` (+ `05-lens-*.md`) |
| `test-full` / `test-lite` | — | `06-test-log.md` (after review clean) |
| `merge` | Gate C | PR URL / result |

### Task `description` map (by stage id)

| Stage id | description |
|----------|-------------|
| (classify) | `Classify and resolve models` |
| `ideation` | `Ideation problem framing` |
| `gate-a` | `User day-to-day review` |
| `ideation-update` | `Update idea from review` |
| `skim` | `Light repo skim` |
| `analyze` | `Analyze codebase` (Mode full) |
| `grill` | `Grill design tree` (Mode full) |
| `design` | `Design and tasks` (Mode full) |
| `design-phase` | `Design phase bundle` (Mode simple — Analyze+Grill+Design) |
| `design-review` | `Design review` (Mode full general) |
| `api-contract-review` | `API contract review` (Mode full; parallel with DB when both) |
| `db-design-review` | `DB design review` (Mode full; parallel with API when both) |
| `design-verify-phase` | `Design verify phase` (Mode simple — general + API/DB when flagged) |
| `design-update` | `Update design docs` |
| `tdd-review` | `Review TDD test cases` |
| `build` | `Build with TDD` |
| `smoke` | `Smoke build and unit` (re-run only; usually skipped) |
| `adversarial` | `Adversarial test review` (Mode full) |
| `code-review-phase` | `Lite combined review` (**required** when profile lite) |
| `quality` | `Quality review` (Mode full) |
| `lens-security` | `Security review` |
| `lens-perf` | `Performance review` |
| `lens-memory` | `Memory review` |
| `lens-api` | `API contract lens` |
| `lens-db` | `Database review` |
| `merge-findings` | `Merge review findings` |
| `fix-review` | `Fix review findings` |
| `test-full` | `Full test suite` (coverage + e2e gaps + run — one Task) |
| `test-lite` | `Run build and tests` |
| `fix-tests` | `Fix from test log` |
| `merge` | `Push PR and merge` |

### File log examples (`00-run.md` only)

```markdown
- **HH:MM** · done · Step 2 — Analyze · usage-limit retry — waited 5s
- **HH:MM** · done · Step 2 — Analyze · usage-limit retry — inherit model
- **HH:MM** · done · Step 2 — Analyze · main-thread fallback — usage limit after inherit
- **HH:MM** · done · Gate B — auto · user-first Option 1 · digest posted
- **HH:MM** · paused · Gate C — blocking — Approve commit + push + PR + merge?
- **HH:MM** · stopped · user abort — frozen at Gate B
```

---

## Orchestrator rules (short)

- One subflow at a time; honor Review profile and gates. Use **Happy path** above — not the skill inventory table.  
- Full: Gate A → skim → Analyze → Grill settled → Design → API∥DB (must parallel when both) → design-review clean → 04a or skip → Gate B → Build (**verify-pass** + Smoke section) → Smoke skip → review clean → **test-full** (one Task) → Gate C.  
- Simple: never re-run Ideation→Gate A→skim; **design-phase** → **design-verify-phase**; one design option by default; lite → **must** code-review-phase; Fast-on-simple for mechanical.  
- Design-review needs update → Update mode → re-review. Smoke/test fail → Fix-from-tests (**verify-pass**) → re-run that mode.  
- Build / Fix: do **not** advance on **verify-fail**; max 3 attempts then Decision N ([verify-and-fix.md](verify-and-fix.md)).  
- Design invalid after Build → **Design-backloop** Decision N (amend design / Fix-only / stop).  
- Card **Next step** = stage id (+ Task description); do not rely on legacy Step numbers alone.  
- Optional metrics: Task count · design-review rounds · verify-fail count · smoke↔fix · Gate B / Grill HITL · inherit retries · main-thread fallbacks.
