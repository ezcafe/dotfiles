# my-dev-flow stage index (canonical)

`my-dev-flow` is an **orchestrator only**. Stage prompts live in the subflows.
This file is the **source of truth** for pipeline order, Mode, HITL, lenses, models, and progress.

**Progress:** Cursor subagent card = live status (no “now running…” banners).  
**After each step:** ≤5 lines summary + full path; read Result header only (~40 lines); update Orchestrator card.  
**HITL:** Gate B `auto` | `async-notify` | `blocking`. **Gate C always blocking.** Grill uses Gate B tier (prefer auto). Gate digest ≤4 bullets. User-first picks on auto/async.  
**File also:** Run log + Last stage + Orchestrator card.  
**Chat OK:** post-step summary + path, human gates, Decision N, stop, finish.  
**Subagent context:** every Task starts fresh — [handoffs.md](handoffs.md) stage id only.  
**Legacy removals:** [LEGACY.md](LEGACY.md).  
**Severity exit:** [severity.md](severity.md) (Critical/Major block clean; defer Enhancement).  
**Skill paths:** [skills-path.md](skills-path.md) (`{my-dev-flow}` placeholders in Task prompts).

| Phase | Skill | Stages file |
|-------|--------|-------------|
| Design | [`../my-dev-flow-design/SKILL.md`](../my-dev-flow-design/SKILL.md) | [`../my-dev-flow-design/stages.md`](../my-dev-flow-design/stages.md) |
| Design review | [`../my-dev-flow-design-review/SKILL.md`](../my-dev-flow-design-review/SKILL.md) | [`../my-dev-flow-design-review/stages.md`](../my-dev-flow-design-review/stages.md) |
| Code | [`../my-dev-flow-code/SKILL.md`](../my-dev-flow-code/SKILL.md) | [`../my-dev-flow-code/stages.md`](../my-dev-flow-code/stages.md) |
| Smoke / full test | [`../my-dev-flow-test/SKILL.md`](../my-dev-flow-test/SKILL.md) | [`../my-dev-flow-test/stages.md`](../my-dev-flow-test/stages.md) |
| Review | [`../my-dev-flow-review/SKILL.md`](../my-dev-flow-review/SKILL.md) | [`../my-dev-flow-review/stages.md`](../my-dev-flow-review/stages.md) |
| Merge | [`../my-dev-flow-merge/SKILL.md`](../my-dev-flow-merge/SKILL.md) | [`../my-dev-flow-merge/stages.md`](../my-dev-flow-merge/stages.md) |

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
3. Create slug `YYYYMMDD-feature-x`; write `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md): Mode, Review profile, Complexity, Has UI/API/DB when known, resolve models, Orchestrator card, HITL Gate B (refine after Design), **HITL Gate C: blocking**.
4. Chat one line: Mode + Review profile + why.

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

| Profile | When | After smoke |
|---------|------|-------------|
| **full** | Mode full | Adversarial → Quality → Conditional lenses → full test |
| **lite** | Mode simple default | Same review lenses (often none) → **lite test** (targeted e2e) |
| **skip-review** | Mode simple + copy/token/docs-only or user said skip-review | Skip code review + further tests → Gate C |

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

**Gate C test bar (before merge subflow):**

| Review profile | `06-test-log.md` Result required |
|----------------|----------------------------------|
| **skip-review** | **smoke-pass** (no full/lite suite) |
| **lite** | **success** after lite run |
| **full** | **success** after full run |

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
| **Has API** | New/changed REST/GraphQL/routes/server actions, edge validators, cross-boundary public types | Isolated **API contract review** Task + include **api** in Lens plan |
| **Has DB** | New/changed tables/columns/indexes/migrations/ORM, notable writes/transactions/raw SQL | Isolated **DB design review** Task + include **db** in Lens plan |

Independent flags. Skills: [`api-and-interface-design`](../api-and-interface-design/SKILL.md), [`database-and-data-model`](../database-and-data-model/SKILL.md).

---

## Conditional lenses / Lens plan

Before code review, set **Lens plan** in `00-run.md`. Launch only matching lenses. (Legacy field name **SPM plan** — see [LEGACY.md](LEGACY.md).)

| Lens | Launch when |
|------|-------------|
| **API** | Has API = yes, or new/changed public contracts / edge validators |
| **DB** | Has DB = yes, or new/changed schema/migrations/persistence queries |
| **Security** | auth, sessions, PII, uploads, SQL/raw, secrets, permissions |
| **Performance** | lists/tables, charts, fetch, bundle-sensitive UI, heavy client compute |
| **Memory** | subscriptions, large client caches, websockets/realtime, media buffers |

- **none** → after Quality clean, skip lenses → test per Review profile  
- **1 lens** → that lens only; parent copies Result into Merged lenses (no Merge Task)  
- **2+ lenses** → parallel → Merge findings Task  

API lens → `05-lens-api.md`. DB lens → `05-lens-db.md`.

---

## TDD test-case review (Step 4a)

Run `04a` **only if** `04-tasks.md` lists concrete tests to create. Else Notes `04a skipped — no planned test cases`; do not invent `04a`.

---

## Full pipeline order

1. Step 0 — Mode full; Review profile full; models + card + HITL  
2. Step 1 — Ideation (set Has UI)  
3. Gate A — day-to-day + 80/20 → `01a` (auto when ok; max 3 update rounds)  
4. Step 1s — Light skim → `02-skim.md`  
5. Steps 2–3 — Analyze → Grill (or skip) → Design (two options); refine Has API/DB; UI in Design  
6. Design ↔ review until clean (API contract review when Has API; DB when Has DB); max 3  
7. Step 4a — TDD only if planned tests  
8. Gate B — HITL tier + digest  
9. Step 4 — Build  
10. Step 4s — Smoke (fail → Fix → re-smoke)  
11. Set Lens plan → Steps 5–9 review ⇄ Fix  
12. Steps 10–12 — Full test ⇄ Fix (max 3)  
13. Gate C — blocking → merge only after yes  

## Simple pipeline order

Starts at Analyze. Skip Ideation / Gate A / skim.

1. Step 0 — Mode simple; Review profile lite|skip-review; bootstrap `01-idea` if needed  
2. Steps 2–3 — Analyze → Grill (or skip) → Design (one recommended design by default)  
3. Design ↔ review until clean (API/DB Tasks when flagged)  
4. 4a if planned → Gate B → Build → Smoke  
5. skip-review → Gate C; else lite review → lite test → Gate C  

**Grill:** Mode full always (unless frontier-empty). Mode simple when frontier open or Has API/DB; else skip. See [grill.md](grill.md).

---

## Models (resolve once)

| Tier | Used by | Preferred (first present in Task allowlist) |
|------|---------|-----------------------------------------------|
| **High** | Analyze; Design; Update from design review | `claude-sonnet-5-5-high` → `claude-fable-5-1-thinking-high` → Medium → Fast → `inherit` |
| **Medium** | Ideation; judgment stages when available | `claude-opus-5-5-medium` → Fast → `inherit` |
| **Fast** | Build/Fix/Smoke/Test/Merge; mechanical when Medium missing | `composer-2.5-fast` → `inherit` |

**Mechanical stages** (use Fast when Medium missing): Gate A, skim, grill, design-review, API/DB contract review, TDD review, Adversarial, Quality, lenses, Merge findings.

At start: pick first available slug per tier; write into `00-run.md`; note fallbacks. Only ask user if **no** Task can launch.

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

---

## Subagent context

1. One new Task per stage (no `resume` across different stages).  
2. Prompt = stage-scoped handoff + stage rules + user decisions.  
3. Absolute paths under `.my-docs/workflow/<slug>/`.  
4. Task return = only handoff back.  
5. Update Orchestrator card after each step.

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

| Step | Path |
|------|------|
| 0 Classify | `00-run.md` |
| 1 Ideation | `01-idea.md` |
| Gate A | `01a-idea-ui-review.md` |
| 1s Skim | `02-skim.md` |
| 2 Analyze | `02-analysis.md` |
| 2g Grill | `02b-grill.md` or skip note |
| 3 Design | `03-design.md` + `04-tasks.md` |
| Design review / API / DB | `03a-design-review-log.md` + `03a-api-contract-review.md` + `03a-db-design-review.md` when flagged |
| 4a | `04a-tdd-test-review.md` or skip note |
| Gate B | digest + HITL |
| 4 Build | key paths |
| Smoke / test | `06-test-log.md` |
| Review | `05-review-log.md` (+ `05-lens-*.md`) |
| Gate C / Merge | PR URL / result |

### Task `description` map

| Step | description |
|------|-------------|
| 0 | `Classify and resolve models` |
| 1 | `Ideation problem framing` |
| Gate A | `User day-to-day review` |
| Ideation update | `Update idea from review` |
| Light skim | `Light repo skim` |
| 2 | `Analyze codebase` |
| 2g | `Grill design tree` |
| 3 | `Design and tasks` |
| Design review | `Design review` |
| API contract review | `API contract review` |
| DB design review | `DB design review` |
| Design update | `Update design docs` |
| TDD test review | `Review TDD test cases` |
| 4 | `Build with TDD` |
| Smoke | `Smoke build and unit` |
| 5 | `Adversarial test review` |
| 5-lite | `Lite combined review` (optional — profile lite, Lens plan none or one) |
| 6 | `Quality review` |
| 7 | `Security review` |
| 8 | `Performance review` |
| 9 | `Memory review` |
| API lens | `API contract lens` |
| DB lens | `Database review` |
| Merge findings | `Merge review findings` |
| Fix · lens | `Fix review findings` |
| 10 | `Test coverage check` |
| 11 | `Add missing e2e` |
| 12 | `Run build and tests` |
| Test↔Code | `Fix from test log` |
| 13 | `Push PR and merge` |

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

- One subflow at a time; honor Review profile and gates.  
- Full: Gate A → skim → Analyze → Grill settled → Design → design-review clean → 04a or skip → Gate B → Build → smoke-pass → review clean → full test → Gate C.  
- Simple: never re-run Ideation→Gate A→skim; one design option by default.  
- Design-review needs update → Update mode → re-review. Smoke/test fail → Fix-from-tests → re-run that mode.  
- Optional Notes metrics: design-review rounds · Gate B auto vs blocking · inherit retries · main-thread fallbacks.
