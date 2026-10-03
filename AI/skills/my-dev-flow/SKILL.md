---
name: my-dev-flow
description: >-
  Orchestrates the full delivery pipeline by running my-design-subflow
  (Ideation → Gate A day-to-day auto-approve → light repo skim → Analyze →
  Grill design-tree + glossary/ADR with auto-settle → Design; no UI concept /
  Gate A2), my-design-review-subflow (until clean), optional TDD test-case
  review (only when planned tests exist), HITL-tiered Gate B, Build, smoke,
  my-review-subflow (lite/skip-review for simple; conditional SPM + API/DB
  lenses), full or lite my-test-subflow, then blocking Gate C (commit/push/PR/merge
  need explicit user approval — never auto). Soft HITL: auto / async-notify /
  blocking for Gate B only (Grill uses Gate B tier; prefer auto). On auto,
  user-first option picks. Classifies simple vs complex.
  Stage-scoped handoffs + Orchestrator card. Artifacts under .my-docs/workflow.
  Use when the user says run my-dev-flow, start my-dev-flow, run
  my-plan-flow / my-workflow (legacy), simple mode, ideate → build → merge,
  grill / stress-test this plan, or wants the AI-assisted delivery pipeline.
---

# my-dev-flow

End-to-end orchestrator. This skill **does not** re-implement most stages. It
reads and follows each subflow skill in order. **Grill** (design-tree
frontier + glossary/ADR) lives in this package: [grill.md](grill.md).

Practices: [AI-assisted engineering](https://newsletter.eng-leadership.com/p/how-to-do-ai-assisted-engineering) —
design-heavy, never ship first draft, generation ≠ verification.

## Package files

| File | Role |
|------|------|
| [SKILL.md](SKILL.md) | Orchestrator rules, Mode, HITL, models, pipeline |
| [stages.md](stages.md) | Step order + phase index into subflows |
| [templates.md](templates.md) | Artifact templates + stage-scoped handoffs |
| [grill.md](grill.md) | Grill rules (frontier rounds, glossary, sparse ADRs) |

## Sub-workflows

| Order | Skill | Role |
|-------|--------|------|
| 1 | [`my-design-subflow`](../my-design-subflow/SKILL.md) | Ideation → Gate A → skim → Analyze → Grill → Design (no UI concept / A2); also Update from design review |
| 2 | [`my-design-review-subflow`](../my-design-review-subflow/SKILL.md) | Review design gaps/issues → Fix ask until clean (isolated API/DB reviews when flagged) |
| 3 | [`my-code-subflow`](../my-code-subflow/SKILL.md) | Optional TDD test-case review (when tests planned) → Build with TDD (draft); also Fix from test failures |
| 4 | [`my-test-subflow`](../my-test-subflow/SKILL.md) | Smoke before review; full or **lite** test after review (per Review profile) |
| 5 | [`my-review-subflow`](../my-review-subflow/SKILL.md) | Adversarial → Quality → **Conditional lenses (SPM + API + DB)** + merge ⇄ Fix (or skip when profile skip-review) |
| 6 | [`my-merge-subflow`](../my-merge-subflow/SKILL.md) | Gate C (**blocking**) → commit/push/PR/merge only after explicit yes |

Each subflow can also run **alone** when its prerequisites are met.

## When to run

- **Default trigger:** `run my-dev-flow`, `start my-dev-flow`, `ideate → build → merge`, or any ask to run the delivery pipeline — **classify complexity first**, then pick Mode.
- **Legacy alias:** `run my-plan-flow` / `start my-plan-flow` / `run my-workflow` / `start my-workflow` → same as `my-dev-flow` (do not confuse with `my-code-subflow` Build).
- **Explicit override:** `run my-dev-flow simple` / `simple mode` → Mode **simple** (Review profile **lite** unless `skip-review`); `run my-dev-flow full` / `full mode` → Mode **full** (Review profile **full**); `skip-review` with simple → Review profile **skip-review**. Do not re-classify when the user already chose Mode.
- **Grill-only:** `grill`, `grill-with-docs`, or `stress-test this plan` → run Step 2g using [grill.md](grill.md) (needs Analyze / idea artifacts).

## Mode selection (required on trigger)

Before creating/updating `00-run.md` Mode, the **parent / main agent** classifies the requirement. Do **not** default to full without this check (unless resume — see below).

### Overrides (highest priority)

1. **Resume:** `00-run.md` already has **Mode** + **Last stage** → keep Mode and Review profile; resume next incomplete step.
2. **User named mode:** `simple` / `full` / `skip-review` in the trigger → set Mode and Review profile accordingly.
3. Otherwise → **classify** using the rules below; set Review profile (`full` / `lite` / `skip-review`).

### Simple vs complex

| Signal | Prefer **simple** | Prefer **full** (complex) |
|--------|-------------------|---------------------------|
| Scope | Bug fix, small tweak, copy/token, one helper, one field/API, one clear surface | New feature, multi-surface UX, new product concept |
| Clarity | Outcome and constraints already clear in the ask | Ambiguous problem; needs discovery / day-to-day / 80/20 |
| Framing | Framing already done (`01-idea` + Gate A / skim as needed), **or** a thin idea can be written from the ask alone | Needs Ideation, Gate A, skim, and discovery of *what* to build |
| Risk | Low blast radius; few files; no new auth/data-model shape | Cross-cutting (auth, schema, multiple apps/workspaces) |
| UI | No UI, copy/token-only, or tiny layout tweak matching existing patterns | New or redesigned multi-surface UX (specify in Design; no separate UI concept gate) |

**Rule of thumb:** if early framing (Ideation → Gate A → skim) would mostly rubber-stamp an already-clear ask → **simple**. If the team still needs to invent *what* to build → **full**.

**Ambiguous:** present **Decision N** (simple vs full) with What / Example / Pros / Cons / Recommendation — do not guess.

**Record in `00-run.md`:** `Mode: simple | full`, **Review profile**, plus Notes like `Complexity: simple — bug fix, clear outcome` or `Complexity: complex — new multi-surface feature`. Show one short line in chat: chosen Mode + Review profile + why.

### Review profile (set at Step 0)

| Profile | When | After smoke |
|---------|------|-------------|
| **full** | Mode **full** (default) | Adversarial → Quality → **Conditional lenses** → full test |
| **lite** | Mode **simple** default | Adversarial → Quality → **Conditional lenses** (often none) → **lite test** (targeted e2e; skip coverage / add-e2e Tasks unless tasks require new e2e) |
| **skip-review** | Mode **simple** + copy/token-only, docs-only, or user said `skip-review` | Skip code review + further tests → Gate C |


### HITL tiers for Gate B / Gate C

Parent sets **HITL Gate B** in `00-run.md`: `auto` | `async-notify` | `blocking`. Refine after Design.

**HITL Gate C is always `blocking`.** Never set Gate C to `auto` or `async-notify`. Never commit, push, open a PR, or merge without an explicit user yes in this chat.

| Tier | Behavior | Allowed for |
|------|----------|-------------|
| **auto** | Parent approves without waiting. Post a short **Gate digest** in chat + Run log. Apply **User-first auto picks**. | Gate B only |
| **async-notify** | Post Gate digest; **continue** unless human vetoes soon. Same user-first picks as auto. | Gate B only |
| **blocking** | Pause for human approve / reject. Still show Gate digest (≤4 bullets). | Gate B; **required** for Gate C |

**Default routing (soft) — Gate B only:**

| Prefer **auto** or **async-notify** when | Prefer **blocking** when |
|------------------------------------------|---------------------------|
| Mode **simple** + design-review **clean** + (04a **ok** or **skipped**) + Has API **no** + Has DB **no** | Mode **full**, or Has API/DB **yes**, or open Critical/Major in design/TDD review, or auth/PII/security clearly in scope |

**Git / remote (hard — all stages, all Modes):**

- Do **not** run `git commit`, `git push`, `gh pr create`, or `gh pr merge` unless the user **explicitly approved** that action in this chat.
- Gate C ask must name what will happen (commit / push / PR / merge). “Approve merge?” alone is not enough if commits or push are still pending — ask for those too.
- Reject / silence → stop. Do not treat Gate B auto, smoke-pass, or “continue the pipeline” as approval to commit or push.

**Gate digest (required on every Gate B pause or auto, and every Gate C pause):** (1) what ships, (2) top risks (≤3), (3) what already verified, (4) ask or auto-pick note (Gate B) / explicit commit-push-PR-merge ask (Gate C).

**Rubber-stamp note:** if Gate B is repeatedly approved with zero edits on simple runs, keep or raise auto thresholds; if post-merge defects rise after Gate B auto, force **blocking** Gate B for that risk class. Gate C stays blocking.

### User-first auto picks (required when auto / async-notify)

Whenever the agent **auto-approves** a gate or **selects** among Decision options without a human reply:

1. **Stand in the user’s shoes** — day-to-day parent / caregiver / operator value first.
2. **Then** system convenience (simpler code, fewer files, faster build).
3. Prefer the option that best serves the **primary user job** from Gate A / `01-idea` (#1/#2 when present).
4. Record in `00-run.md` Notes + Run log: `auto-pick — Decision N Option K — user-first: <one line>; system: <one line>`.
5. Do **not** pick the “cleverest” engineering option when it hurts the common user path.

### TDD test-case review (Step 4a) — only when tests are planned

Run `04a-tdd-test-review.md` **only if** `04-tasks.md` **creates** planned test cases (non-empty **Tests (TDD…)** / TDD bullets with real cases to write).

| Run 04a when | Skip 04a when |
|--------------|---------------|
| At least one task lists concrete unit/e2e/integration cases to add | No TDD sections, all tests marked N/A, docs-only tasks, or tasks say “no new tests” |
| Design explicitly requires new failing tests before Build | Copy/token-only with no behavior tests |

On skip: set Notes `04a skipped — no planned test cases`; do **not** invent `04a`; Gate B may proceed. Build still follows TDD when a task later adds tests.

### Has API (set early; refine after Design)

Parent sets **Has API** in `00-run.md` (`yes` / `no`). Prefer during Analyze / Design when contracts become clear; may set earlier if the ask is obviously API work.

| **Has API = yes** when | **Has API = no** when |
|------------------------|------------------------|
| New/changed REST or GraphQL endpoints, route handlers, server actions exposed as public API | Pure UI/copy/token with no contract change |
| Shared validators / input-output types at a system edge | Internal refactors with no public shape change |
| Module boundaries that cross client↔server or app↔app | Docs-only |

When **Has API = yes**:

1. **Design review** — launch a dedicated **API contract review** Task (isolated context) before or beside general design review — see `my-design-review-subflow`.
2. **Code review** — include **api** in **SPM plan** so an isolated **API** lens runs after Quality — see Conditional lenses below.

### Has DB (set early; refine after Design)

Parent sets **Has DB** in `00-run.md` (`yes` / `no`). Prefer during Analyze / Design when schema or query contracts become clear; may set earlier if the ask is obviously database work.

| **Has DB = yes** when | **Has DB = no** when |
|-----------------------|----------------------|
| New/changed tables, columns, indexes, constraints, or enums | Pure UI/copy/token with no data-model change |
| New or changed migrations / ORM schema files | Read-only use of existing columns with no new queries of note |
| New/changed writes, complex reads, transactions, or raw SQL touching persistence | Docs-only; client-only state with no server persistence |

When **Has DB = yes**:

1. **Design review** — launch a dedicated **DB design review** Task (isolated context) before or beside general design review — see `my-design-review-subflow`.
2. **Code review** — include **db** in **SPM plan** so an isolated **Database** lens runs after Quality — see Conditional lenses below.

**Has API** and **Has DB** are independent — a change can be yes/yes, yes/no, or no/yes.

### Conditional lenses / SPM plan (before code review)

Parent sets **SPM plan** in `00-run.md` from draft signals (do not always launch every lens). Field name stays **SPM plan** for compatibility; values may include **api**, **db**, plus security / perf / memory.

| Lens | Launch when |
|------|-------------|
| **API** | **Has API = yes**, or new/changed public HTTP/GraphQL/server-action contracts, edge validators, cross-boundary module APIs |
| **DB** | **Has DB = yes**, or new/changed migrations, schema, indexes, persistence queries, transactions |
| **Security** | auth, sessions/cookies, API routes, PII, uploads, SQL/raw queries, secrets, permissions |
| **Performance** | lists/tables, charts, data fetch, bundle-sensitive UI, heavy client compute |
| **Memory** | subscriptions, large client caches/state, websockets/realtime, media buffers |

- **none** → after Quality clean, skip lenses + Merge findings; go to test (per Review profile).
- **1 lens** → that lens only; parent copies Result into `05-review-log.md` Merged SPM (no Merge Task).
- **2+ lenses** → parallel those only → Merge findings Task.

**API lens** (isolated Task): follows [`api-and-interface-design`](../api-and-interface-design/SKILL.md) — contract vs implementation, typed I/O, one error shape, edge validation, pagination, additive fields, naming, idempotency. Writes `05-lens-api.md` only.

**DB lens** (isolated Task): follows [`database-and-data-model`](../database-and-data-model/SKILL.md) — schema/migration safety, indexes/uniques, ownership, transactions, safe SQL binds, bigint aggregates, design↔code match. Writes `05-lens-db.md` only.

### Full mode (complex requirement, or user forced full)

```
Ideation (set Has UI)
→ Gate A (day-to-day + 80/20; auto-approve when ok)
→ Light repo skim (02-skim.md)
→ Analyze → Grill (design tree + glossary/ADR; auto-settle by default) → Design
→ design-review loop
→ TDD test-case review only if planned tests exist in 04-tasks
→ Gate B (HITL tier: auto | async-notify | blocking; user-first when auto)
→ Build
→ Smoke (build + unit)
→ Code review (Adversarial → Quality → Conditional lenses incl. API when Has API, DB when Has DB ⇄ Fix)
→ Full test (coverage + e2e + runs) ↔ Fix
→ Gate C (**blocking** — explicit user approve) → merge only after yes
```

### Simple mode (start at Analyze)

Skip Ideation / Gate A / skim. Run Analyze → Design onward with **Review profile** `lite` or `skip-review`:

```
Analyze → Grill (or skip) → Design (one recommended design by default)
→ design-review loop
→ TDD test-case review only if planned tests exist
→ Gate B (HITL) → Build → Smoke
→ if skip-review: Gate C (**blocking**)
→ else lite review (Adversarial → Quality → Conditional lenses) → lite test ↔ Fix
→ Gate C (**blocking**) → merge only after yes
```

**When to use:** requirement classified **simple**, or framing already done, or user forced simple.

**Prerequisites:**

- `<slug>` + `00-run.md` with `Mode: simple`, **Review profile**, and **Has UI** set
- `01-idea.md` present — either from prior framing **or** parent **bootstrap** (thin idea from the user ask: Problem, Outcome, Scope, Non-goals, Has UI). Do **not** stop and force full mode only because framing was skipped.
- Prefer Gate A / `02-skim.md` when those already exist (resume / prior framing)
- When bootstrapping a new simple run: mark early gates skipped in Notes (e.g. `Gate A skipped — simple mode bootstrap`); do **not** invent `01a` / `01b` / `ui-refs`

**Do not** re-run Ideation / Gate A / skim in simple mode. **Do not** run UI concept or Gate A2 (removed).

## Principles

- **Formula:** rigorous design + AI build + aggressive review + many fast iterations.
- **Design is the main artifact.** Code is a draft until reviews and tests pass.
- **Design reuses patterns + UI/UX/mobile + OWASP** — see `my-design-subflow` / templates. `03-design.md` must include **System design** and **Design patterns used** (teach or `N/A`). Triggers: Has API/Has DB → System design Overview required; do not restate sequence/contracts; Build/Quality honor Best practices from those sections.
- **Design review before TDD review / code** (full + simple). Must be clean before optional TDD test-case review (or skip 04a when no planned tests).
- **Mode from complexity:** on trigger, classify simple vs complex (unless override/resume) → set `Mode` + **Review profile** in `00-run.md` before Stage 1 / Analyze.
- **Stage-scoped handoffs:** every Task uses templates **Stage-scoped handoff** for its stage id — never the full artifact catalog.
- **Orchestrator card:** parent keeps next-step fields in `00-run.md`; do **not** re-read full subflow `SKILL.md` every step (once per phase, or when Mode/profile changes). Next Task: card + that stage’s `stages.md` section only.
- **Artifact size caps:** honor templates caps (`02-skim` short, analysis bullets, Fix asks bounded).
- **Design options:** Mode **full** → two Decision options; Mode **simple** → one recommended design + ≤3-line rejected alternative (full Option 1/2 only if 2+ approaches still unsettled).
- **Has UI early:** Full: Ideation sets **Has UI** in `00-run.md` (`yes` / `no`). Simple: set Has UI when bootstrapping thin `01-idea.md` or keep existing. Do not wait for Gate A. UI behavior/layout is specified in **Analyze / Design** (match existing app patterns) — **no UI concept step, no Gate A2**.
- **Primary sources in Ideation:** Investigate the question against primary sources (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it. Record them in `01-idea.md` → Sources (primary). Same rule when parent bootstraps a thin idea in simple mode.
- **HITL soft tiering:** Gate B uses `auto` | `async-notify` | `blocking` (prefer auto on low-risk simple runs). **Gate C is always blocking** — no commit/push/PR/merge without explicit user approval.
- **User-first auto picks:** On auto/async-notify, stand in the user’s shoes; pick user value before system convenience; log rationale.
- **04a only when tests planned:** Skip TDD test-case review when `04-tasks.md` has no planned test cases.
- **Has API + isolated API review:** When **Has API = yes**, parent must launch **isolated** Tasks: (1) design-time **API contract review** (`my-design-review-subflow`), (2) code-time **API** lens (`my-review-subflow`). Do not fold API contract checks into the parent chat or into Quality alone. Skill: [`api-and-interface-design`](../api-and-interface-design/SKILL.md).
- **Has DB + isolated DB review:** When **Has DB = yes**, parent must launch **isolated** Tasks: (1) design-time **DB design review** (`my-design-review-subflow`), (2) code-time **DB** lens (`my-review-subflow`). Do not fold schema/migration/query checks into the parent chat or into Quality alone. Skill: [`database-and-data-model`](../database-and-data-model/SKILL.md).
- **Gate A after Ideation (full only):** **user-role** Task (fresh context) re-reviews `01-idea.md` for **day-to-day usage** + **80/20 UI**. **Auto-approve** Gate A when Result is **ok**; human only on escalate / max rounds.
- **Light repo skim after Gate A (full only):** short constraints pass (`02-skim.md`) before Analyze.
- **Grill after Analyze (before Design):** follow [grill.md](grill.md) — design-tree frontier + project glossary + sparse ADRs. Mode **full** always (unless already frontier-empty). Mode **simple** when frontier open or Has API/DB; else skip. Uses **HITL Gate B** tier; **prefer auto** user-first settle + Grill digest. Do not start Design on `needs-round`.
- **No UI concept / Gate A2:** do **not** write `01b-ui-concept.md`, do **not** create `ui-refs/` for look gates, do **not** serve :8765. When Has UI, specify UI in `03-design.md` / `04-tasks.md` using existing app chrome and Gate A 80/20. Legacy `01b`/`ui-refs` in old runs are ignored for new pipeline steps.
- **Build when Has UI:** match Design UI specs + live product patterns (size/positions/texts/chrome of **existing** controls reused). Do not invent a conflicting IA. Quality fails **Major** on clear drift from Design / Gate A #1/#2.
- **TDD test-case review before Gate B (conditional):** after design-review clean, run 04a **only if** planned tests exist in `04-tasks.md`. Then Gate B per **HITL Gate B**. When **blocking**, ask human to approve design + tasks (+ tests if any); skim **System design** + **Design patterns used**. When **auto**, user-first pick + Gate digest. **Build** only after Gate B checked (auto or human).
- **Smoke before code review:** after Build, run **build + unit** only. Do not start `my-review-subflow` on a draft that fails smoke (unless Review profile is **skip-review**, then smoke → Gate C **blocking**).
- **Conditional lenses:** set **SPM plan** before review (include **api** when Has API, **db** when Has DB); launch only matching lenses (see above).
- **Full / lite test after review:** profile **full** → coverage + e2e + runs; profile **lite** → targeted e2e only; Fix ↔ re-test until green.
- **Design review does not re-litigate Gate A 80/20** — check **alignment** with `01a` / Design UI specs; fail on UI drift from Gate A #1/#2 or Design. Fail Major if Design re-opens grill Settled decisions without new evidence, or Build-critical frontier was never grilled when Mode full.
- **Analyze + spike deep dive (required):** During **Analyze** and any **spike** (throwaway exploration, not production Build), always answer and record in `02-analysis.md` (and ask the user when unclear):
  1. **What is this?** — name the problem, surface, or change in plain words.
  2. **Why do we need this?** — user/business outcome; what fails if we skip it.
  3. **How to do this?** — proposed approach; **other ways**; **best practices** (repo patterns first, then industry). Prefer Decision options when 2+ approaches.
  Also fill **Design tree (frontier)** stub for Grill. Do not treat Analyze as a file list only. Spikes must write findings back into analysis; do not leave spike-only knowledge in chat.
- **Resume:** if `00-run.md` has **Last stage**, resume from the next incomplete step; do not redo completed Gate A / A2 / B unless artifacts changed.
- **Each subagent has its own context** — see below. **Usage limit on a Task** → parent runs **that** stage on the main thread; later stages still use subagents.
- **Code security review uses OWASP Top 10** — `my-review-subflow` Security lens (when SPM plan includes security).
- **API contract review uses api-and-interface-design** — design-time Task + code-time API lens (when Has API / SPM plan includes api).
- **DB design review uses database-and-data-model** — design-time Task + code-time DB lens (when Has DB / SPM plan includes db).
- **Grill uses [grill.md](grill.md)** — design-tree frontier + glossary/ADR before Design; prefer auto-settle.
- **Generation ≠ verification.** Test before merge (except skip-review after smoke). Test fail → code fix → re-test.
- Plain words. **Decision options** when 2+ choices. User rejects a gate → **stop the whole flow**.

## Gate names (canonical)

| Canonical | Legacy aliases (same meaning) | Who |
|-----------|-------------------------------|-----|
| **Gate A** | Gate 2-UI + Gate 1 | Auto when day-to-day review ok |
| **Gate B** | Gate 2 | HITL-tiered — design + tasks (+ tests if planned); skim System design / Design patterns; **user-first** when auto |
| **Gate C** | Gate 3 | **Always blocking** — commit / push / PR / merge need explicit user yes |

**Removed:** Gate A2 (UI look) and the UI concept step. Old docs mentioning A2 / `01b` / `ui-refs` are legacy.

Prefer **Gate A / B / C** in new docs. Treat legacy Gate A2 as skipped/N/A when resuming old runs.

## Subagent context (required)

Each Task / subagent runs in a **fresh, isolated context**. It does **not** see the parent chat, prior tool calls, or other subagents’ memory.

### Do

1. Launch **one new Task per stage** (no `resume` across different stages).
2. Put **everything** the agent needs in the Task `prompt`: **stage-scoped handoff** (templates stage id), stage rules from that `stages.md` section, and any user decisions — **not** the full artifact catalog.
3. Pass only the files and facts for **this** stage. Prefer absolute paths under `.my-docs/workflow/<slug>/`.
4. Treat the Task return as the only handoff back to the parent.
5. Parent: update **Orchestrator card** in `00-run.md` after each step; for the next Task read card + one `stages.md` section — do **not** re-ingest full subflow `SKILL.md` every step.

### Usage-limit fallback (retry once, then main thread for that Task only)

When a Task / subagent **fails or cannot start** because of a **usage limit** (rate limit, quota, “too many requests”, model/subagent capacity, or similar):

1. **Do not stop the pipeline.** Do not wait indefinitely or ask the user only to retry the same Task forever.
2. **Wait 5 seconds**, then **retry the same Task once** (same prompt, description, model). Log in `00-run.md` Notes + Run log: `usage-limit retry — <stage> — waited 5s`.
3. If the **retry succeeds** → continue the pipeline as usual (no main-thread fallback).
4. If the **retry still hits a usage limit** → **run that one stage on the main thread** (parent / main agent) using the same stage rules, stage-scoped handoff inputs, artifacts, and Result shape the Task would have produced.
5. **Record** in `00-run.md` Notes + Run log: `main-thread fallback — <stage> — usage limit after retry` (and the error snippet if useful).
6. **Resume subagents for later stages.** The fallback applies **only** to the blocked Task. The next stage still launches as a Task / subagent as usual.
7. If a later Task also hits a usage limit, apply the **same wait → retry once → main thread** sequence for **that** stage — still keep following stages on subagents when they can run.

**Do not** switch the rest of the run permanently to main-thread-only after one usage-limit hit. **Do not** retry more than once per stage hit before main-thread fallback.

### Do not

- Do **not** assume the subagent remembers Gate answers, earlier stages, or chat discussion.
- Do **not** use `resume` to chain unrelated stages (only resume the **same** stage if that stage’s skill says to continue).
- Do **not** use `resume: "self"` to dump the parent transcript into a stage agent.

## Decision options (required)

Whenever you present **2+ choices**, number the decision and each option:

1. **Decision N** — sequential index for this run (`Decision 1`, `Decision 2`, …).
2. **Option 1 / Option 2 / …** — numbered options (not A/B letters).
3. For **each** option, use plain words:
   - **What it is** — short explanation
   - **Example** — one concrete example
   - **Pros** — what you gain
   - **Cons** — what you give up or risk
4. After all options: **Recommendation** — which option number to pick and why.

### Chat / gate shape (copy this)

```markdown
## Decision 1: <short question>

### Option 1 — <short name>
- **What it is:** …
- **Example:** …
- **Pros:** …
- **Cons:** …

### Option 2 — <short name>
- **What it is:** …
- **Example:** …
- **Pros:** …
- **Cons:** …

### Recommendation
**Pick Option 1** because …
```

Next choice in the same run → **Decision 2**, and so on. Docs use the same numbered fields — see [templates.md](templates.md).

## Preferred models (resolve once)

| Tier | Used by | Preferred slug |
|------|---------|----------------|
| **High** | Analyze; Design; Update from design review | `claude-opus-5-thinking-high` |
| **Medium** | Ideation; Gate A; Light skim; Grill; Design review; API contract review; DB design review; TDD review (when run); Code review lenses — when Medium available | `gpt-5.6-sol-medium` |
| **Fast** (low) | Build / Fix; Smoke; Test; Merge; **mechanical Medium stages when Medium unavailable** | `composer-2.5-fast` |

**Mechanical stages** (prefer Fast when Medium missing): Gate A, skim, grill, design-review, API contract review, DB design review, TDD review, Adversarial, Quality, SPM/API/DB lenses, Merge findings.

### Model availability (auto fallback)

1. At start, check available Task model slugs.
2. For each tier, pick the **first available** slug in that tier’s fallback chain (do **not** stop to ask):

| Requested tier | Fallback order |
|----------------|----------------|
| **High** | preferred High → preferred Medium → preferred Fast → `inherit` |
| **Medium** | preferred Medium → preferred Fast → `inherit` |
| **Fast** | preferred Fast → `inherit` |

3. Write the **resolved** High / Medium / Fast slugs into `.my-docs/workflow/<slug>/00-run.md`, and note in **Notes** if a fallback was used (e.g. `High → Medium`).
4. **Mechanical → Fast:** If preferred Medium is unavailable, mechanical stages **must use Fast when Fast is available** — do not use `inherit` while Fast works.
5. Sub-workflows reuse those resolved slugs for the rest of the run.
6. Only ask the user (Decision N) if **no** Task models can be launched at all — not when a preferred slug is merely missing.

## Artifacts

All under `.my-docs/workflow/<slug>/` (templates in [templates.md](templates.md)):

- `00-run.md` — Mode, Review profile, Has UI, **Has API**, **Has DB**, **HITL Gate B/C**, SPM plan, models, Orchestrator card, gates, **Last stage**
- `01-idea.md` … `04-tasks.md` — design workflow (honor size caps); UI specs in Design when Has UI
- `01a-idea-ui-review.md` — Gate A user-role day-to-day review
- `02-skim.md` — light repo skim (≤ ~40 lines)
- `02-analysis.md` — Analyze (bullet-first; includes Design tree stub)
- `02b-grill.md` — Grill frontier + domain notes (or skip note in `00-run.md`)
- `03a-design-review-log.md` — design review (incl. API contract review when Has API; DB design review when Has DB)
- `04a-tdd-test-review.md` — TDD test-case review (**only when planned tests exist**)
- `05-review-log.md` — code review (incl. Merged SPM)
- `05-lens-*.md` — only for lenses in SPM plan (incl. `05-lens-api.md` when api; `05-lens-db.md` when db)
- `06-test-log.md` — smoke + full/lite test results

**Repo-durable (lazy, from Grill):** `GLOSSARY.md` (or mapped context glossary); sparse ADRs under `docs/decisions/` or existing ADR dir.

**Removed / legacy (do not create on new runs):** `01b-ui-concept.md`, `ui-refs/` look gates, Gate A2.

## Orchestrator pipeline

### Full mode (complex requirement, or user forced full)

```
1. Classify → Mode: full; Review profile: full; resolve models → 00-run.md (+ Orchestrator card + HITL defaults)
   If Last stage set → resume from next incomplete step
2. my-design-subflow: Ideation → Gate A → skim → Analyze → Grill → Design
3. Design-review loop (max 3)
4. TDD test-case review (04a) only if planned tests exist; else skip
5. Gate B — HITL tier (auto / async-notify / blocking); user-first when auto
6. Build (TDD)
7. Smoke. Fail → Fix → re-smoke
8. Set SPM plan (include **api** when Has API, **db** when Has DB) → my-review-subflow (Adversarial → Quality → Conditional lenses ⇄ Fix)
9. Full test. Fail → Fix → re-full (max 3)
10. Gate C — **blocking** (explicit approve commit/push/PR/merge) → merge only after yes
```

### Simple mode (simple requirement, or user forced simple)

```
1. Classify → Mode: simple; Review profile lite|skip-review; resolve models → 00-run.md (+ HITL)
   Ensure 01-idea.md (bootstrap if needed)
2. Analyze → Grill (or skip) → Design (one option by default)
3. Design-review loop (max 3)
4. TDD (if planned) → Gate B (HITL) → Build → Smoke
5. skip-review → Gate C (**blocking**); else lite review (Conditional lenses) → lite test → Gate C (**blocking**) → merge only after yes
```

## Orchestrator rules

- Do **not** paste old monolithic stage prompts. Prefer **Orchestrator card** + one `stages.md` section; load each subflow `SKILL.md` **once per phase** (or when Mode/profile changes) — not every step.
- Use **stage-scoped handoffs** only (templates stage id).
- One subflow at a time; honor gates and **Review profile**.
- Pass the same `<slug>` and resolved models; apply **mechanical → Fast** when Medium missing.
- After each stage: update Status + Last stage + Run log + **Orchestrator card**; show short summary + path.
- Post-step artifact check: **Result / Fix ask header only** (first ~40 lines) — do not re-read full `03-design.md` every step.
- **Full:** Gate A before skim; skim before Analyze; Grill frontier-empty|skipped before Design; design-review clean before TDD (or skip 04a); Gate B (HITL) before Build; smoke-pass before review; review clean before full test; full success before merge.
- **Simple:** never re-run Ideation→Gate A→skim. Grill when needed else skip. Honor Review profile (`lite` / `skip-review`). Design: one option by default. No UI concept / A2.
- **Gate B / Grill picks:** apply **HITL tiers** (Grill uses Gate B tier); Gate/Grill digest always; **user-first auto picks** when auto/async-notify.
- **Gate C / git:** always **blocking**. Never `git commit`, `git push`, `gh pr create`, or `gh pr merge` without explicit user approval in chat.
- On Gate A **needs update** (full only): update idea → re-run Gate A (max 3).
- On design-review needs update: Update mode → re-review.
- On smoke / test failure: Fix-from-tests → re-run that test mode.
- **Usage-limit fallback:** if a Task fails/cannot start due to usage limit → **wait 5s → retry once**; if still limited → parent runs **that** stage on the main thread; log it; **later stages still use Tasks**. Per-stage only — never permanently disable subagents for the rest of the run.
- Never commit secrets; never force-push.
- Never commit or push without explicit user approval (see **Git / remote** under HITL tiers).

## Progress visibility

Cursor shows live running status on each **Task/subagent card**.

### Show log after each step (required — main agent)

After **every** stage finishes (and before starting the next), the **parent / main agent** must:

1. **Read** only Result / Fix ask header of the step’s primary artifact (first ~40 lines) — not the full design docs.
2. **Show in the main chat only:** short summary (2–5 lines) + **full path**.
3. For **HITL auto/async:** show **Gate digest** + auto-pick rationale (user-first). For **blocking:** pause with Gate digest.
4. Update **Orchestrator card** in `00-run.md`. Then continue, or pause for a **human gate** / **decision**.

**Do not** paste full log/doc contents. Summary + path only (+ Gate digest when gating).

| Step | Summary + path (if any) |
|------|-------------------------|
| 0 Classify + resolve models | `00-run.md` (Mode + Review profile + Complexity) |
| 1 Ideation | `01-idea.md` |
| Gate A | `01a-idea-ui-review.md` |
| Ideation update | `01-idea.md` (+ `01a` if touched) |
| Light skim | `02-skim.md` |
| 2 Analyze | `02-analysis.md` |
| 2g Grill | `02b-grill.md` (or skip note) |
| 3 Design | `03-design.md` + `04-tasks.md` |
| Design review | `03a-design-review-log.md` |
| API contract review | `03a-design-review-log.md` (API section) |
| DB design review | `03a-design-review-log.md` (DB section) |
| Design update | touched `01`–`04` + `03a` |
| TDD test review | `04a-tdd-test-review.md` (or skip note in `00-run.md`) |
| Gate B | design/tasks/(04a if any) + HITL tier + Gate digest; System design / Design patterns skim when blocking |
| 4 Build | short draft summary + key paths |
| Smoke | `06-test-log.md` (smoke section) |
| 5–9 Review lenses | `05-review-log.md` (+ `05-lens-*.md` when SPM) |
| Merge findings | `05-review-log.md` (Merged SPM) |
| Fix · lens | `05-review-log.md` |
| 10–12 Full test | `06-test-log.md` |
| Test↔Code | `06-test-log.md` |
| Gate C / Merge | PR URL / merge result |

### Do

1. Launch every stage as a **Task** when the subflow says to (fresh context).
2. Set Task **`description`** from the map below (3–5 words).
3. After a Task finishes: **show short summary + path**, then continue or ask a gate/decision.
4. Write durable trail in `00-run.md` → Run log + **Last stage**.
5. If a Task hits a **usage limit**, **wait 5s → retry once**; if still limited, run **that** stage on the main thread (same artifacts/Result), log the fallback, then launch the **next** stage as a Task again — see **Usage-limit fallback**.

### Do not

- Do **not** post “now running…” / Live status banners.
- Chat **is** for: post-step summary + path, gates, decisions, stop, finish.
- Do **not** keep the whole remaining pipeline on the main thread after one usage-limit fallback.

### Task `description` map (card title)

| Step | Task `description` |
|------|--------------------|
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

### Step names (internal / file log only)

| # | Label | Parent phase |
|---|--------|--------------|
| 0 | Classify complexity + resolve models + create run folder | Setup |
| 1 | Ideation (set Has UI) | Design |
| — | Gate A — day-to-day + 80/20 (auto when ok) | Design |
| 1s | Light repo skim | Design |
| 2 | Analyze | Design |
| 2g | Grill (design tree + glossary/ADR; or skip) | Design |
| 3 | Design + tasks | Design |
| — | Design ↔ design-review (round n; + API contract review when Has API; + DB design review when Has DB) | Design |
| 4a | TDD test-case review (skip if no planned tests) | Code (before Gate B) |
| — | Gate B — HITL (design + tasks + tests if any) | after TDD or skip |
| 4 | Build (TDD) | Code |
| 4s | Smoke (build + unit) | Test (before review) |
| 5–9 | Review: Adversarial → Quality → Conditional lenses (SPM + API + DB) + merge (+ Fix) | Review |
| 10–12 | Full test (+ Test↔Code) | Test |
| — | Gate C — blocking commit/push/PR/merge | Merge |
| 13 | Push + PR + merge | Merge |

### File log (00-run.md only — not chat)

```markdown
- **HH:MM** · done · Step 1s — Light repo skim · ok
- **HH:MM** · done · Step 2 — Analyze · usage-limit retry — waited 5s
- **HH:MM** · done · Step 2g — Grill · frontier-empty · auto · user-first picks
- **HH:MM** · done · Step 2g — skipped — frontier empty (simple)
- **HH:MM** · done · Step 4a — TDD test-case review · ok
- **HH:MM** · done · Step 4a — skipped — no planned test cases
- **HH:MM** · done · Gate B — auto · user-first Option 1 · digest posted
- **HH:MM** · paused · Gate B — blocking — Design + tasks + tests
- **HH:MM** · done · Step 4s — Smoke · smoke-pass
- **HH:MM** · paused · Gate C — blocking — Approve commit + push + PR + merge?
```

### Gates (chat OK when human needed)

| Gate | When | Who | Ask / action |
|------|------|-----|----------------|
| Gate A | After Ideation | User-role Task (Medium) | Day-to-day + 80/20 → `01a`. Auto-check when **ok**. |
| Gate B | After design-review (+ 04a if tests planned); before Build | HITL tier | **blocking:** Approve design + tasks (+ tests)? Skim System design / Design patterns? **auto/async:** Gate digest + **user-first** pick; log rationale. |
| Gate C | Before any commit / push / PR / merge | **Always blocking** | Approve commit? push? PR? merge? Name each action. Never auto-continue. |

Use **Decision N** when 2+ choices. No status banner wrappers. **No Gate A2.**

## Start checklist

1. **Classify requirement** (simple vs complex) unless resume or user named Mode — see **Mode selection**. If ambiguous → Decision N.
2. Pick `<slug>`; create/update artifacts from templates; resolve High / Medium / Fast → `00-run.md`; record `Mode` + **Review profile** + Complexity + **HITL Gate B** + **HITL Gate C: blocking**; init **Orchestrator card**. If **Last stage** set, resume from next step.
3. If Mode **simple** and `01-idea.md` missing → parent bootstrap thin idea + Has UI; note skipped early gates. Set Review profile `lite` or `skip-review`. Do **not** create `01b` / `ui-refs` / Gate A2.
4. Run the matching pipeline; fresh Task + mapped `description` + **stage-scoped handoff**; after each step **short summary + path** + update Orchestrator card; honor HITL + user-first auto; 04a only when tests planned; chat for blocking gates / decisions / stop / finish. On Task **usage limit** → wait 5s → retry once → if still limited, main-thread for that stage only, then subagents again.
