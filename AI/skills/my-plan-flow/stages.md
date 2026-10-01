# my-plan-flow stage index

`my-plan-flow` is an **orchestrator only**. Stage prompts live in the subflows.

**Progress:** Cursor **subagent card** = live running status (no “now running…” chat banners).  
**After each step (required):** short summary + path; read Result header only (~40 lines); update Orchestrator card.  
**HITL:** honor **HITL Gate B** tier in `00-run.md` (`auto` | `async-notify` | `blocking`). **Gate C is always blocking** — never commit/push/PR/merge without explicit user yes. Grill frontier picks use the **Gate B** tier (prefer **auto**). On human pause, show a **Gate digest** (≤4 bullets). On Gate B **auto**, stand in the **user’s shoes** — pick user-day-to-day value first, then system convenience; record pick + rationale.  
**File also:** Run log + **Last stage** + Orchestrator card.  
**Chat OK:** post-step summary + path, human gates (when blocking), decision options, stop reasons, final PR/merge result.

**Subagent context:** every Task starts **fresh** — use **stage-scoped handoff** (templates); no parent-chat memory.

**Usage-limit fallback:** if a Task / subagent hits a usage limit → **wait 5 seconds → retry the same Task once**. If the retry still hits a usage limit, the **parent runs that one stage on the main thread** (same rules + artifacts), logs `main-thread fallback — <stage> — usage limit after retry` in `00-run.md`, then **keeps using Tasks for later stages**. Do not permanently switch the run to main-thread-only.

**Parent:** load each subflow `SKILL.md` once per phase; next Task = Orchestrator card + one `stages.md` section. When entering Grill, also load [grill.md](grill.md) once.

**Decision options:** any 2+ choice must use **Decision N** + **Option 1 / Option 2 / …** with What it is / Example / Pros / Cons / Recommendation — see `SKILL.md`. When HITL is **auto** (or agent picks without waiting), apply **user-first pick** (see my-plan-flow **User-first auto picks**).

**Gates:** Gate A (auto) → Gate B (HITL-tiered) → Gate C (**always blocking**). **No Gate A2 / UI concept step.** Legacy: Gate 2-UI/Gate 1 ≈ A; Gate 2 ≈ B; Gate 3 ≈ C.

| Phase | Skill | Stages file |
|-------|--------|-------------|
| Design | [`../my-design-subflow/SKILL.md`](../my-design-subflow/SKILL.md) | [`../my-design-subflow/stages.md`](../my-design-subflow/stages.md) |
| Design review | [`../my-design-review-subflow/SKILL.md`](../my-design-review-subflow/SKILL.md) | [`../my-design-review-subflow/stages.md`](../my-design-review-subflow/stages.md) |
| Code | [`../my-code-subflow/SKILL.md`](../my-code-subflow/SKILL.md) | [`../my-code-subflow/stages.md`](../my-code-subflow/stages.md) |
| Smoke / full test | [`../my-test-subflow/SKILL.md`](../my-test-subflow/SKILL.md) | [`../my-test-subflow/stages.md`](../my-test-subflow/stages.md) |
| Review | [`../my-review-subflow/SKILL.md`](../my-review-subflow/SKILL.md) | [`../my-review-subflow/stages.md`](../my-review-subflow/stages.md) |
| Merge | [`../my-merge-subflow/SKILL.md`](../my-merge-subflow/SKILL.md) | [`../my-merge-subflow/stages.md`](../my-merge-subflow/stages.md) |

Stage-scoped handoffs + templates: [templates.md](templates.md).

## Step 0 — Classify complexity + resolve models

Parent / main agent (no Task required unless classifying is ambiguous):

1. **Overrides first:** resume keeps Mode; user said `simple` / `full` / `skip-review` → that Mode/profile.
2. Else **classify** (see `SKILL.md` → **Mode selection**). Ambiguous → Decision N.
3. Create/update `00-run.md`: Mode, **Review profile**, Complexity, **Has UI** / **Has API** / **Has DB** when known, resolve High/Medium/Fast (**mechanical → Fast** if Medium missing), init **Orchestrator card**, init **HITL Gate B** (refine after Design / before Gate B); set **HITL Gate C: blocking** always.
4. Chat: one short line — Mode + Review profile + why.

## Order when running full `my-plan-flow`

1. **Step 0** — Mode: full; Review profile: full; models + Orchestrator card + HITL defaults
2. **Step 1** — Ideation (set **Has UI**)
3. **Gate A** — day-to-day + 80/20 → `01a` (auto-approve when ok)
4. **Step 1s** — Light skim → `02-skim.md` (≤ ~40 lines)
5. **Steps 2–3** — Analyze → Grill (or skip) → Design (two options in full); set/refine **Has API** and **Has DB**; UI specs live in Design (no UI concept / Gate A2)
6. **Design ↔ review** until clean (**API contract review** when Has API; **DB design review** when Has DB)
7. **Step 4a** — TDD review → `04a` **only if** `04-tasks.md` has planned test cases; else skip and note in `00-run.md`
8. **Gate B** — per **HITL Gate B** (`auto` / `async-notify` / `blocking`); user-first picks when auto; Gate digest when human
9. **Step 4** — Build (match `03-design` / `04-tasks` + existing app patterns when Has UI)
10. **Step 4s** — Smoke
11. Set **SPM plan** (include **api** when Has API, **db** when Has DB) → **Steps 5–9** Conditional lenses ⇄ Fix
12. **Steps 10–12** — Full test; Fix loop if needed
13. **Gate C** — **blocking** ask (commit / push / PR / merge) → merge only after explicit yes

## Order when running simple `my-plan-flow`

Starts at **Analyze**. Skip Ideation → Gate A / skim. Review profile **lite** or **skip-review**.

1. **Step 0** — Mode: simple; Review profile lite|skip-review; models + Orchestrator card + HITL
   - Ensure `01-idea.md` (bootstrap if needed); set **Has API** / **Has DB** when the ask changes contracts or persistence
2. **Steps 2–3** — Analyze → Grill (or skip) → Design (**one** recommended design by default); refine Has API / Has DB
3. **Design ↔ review** until clean (**API contract review** when Has API; **DB design review** when Has DB)
4. **Step 4a** — TDD **only if test cases planned** → **Gate B** (HITL) → Build → Smoke
5. **skip-review** → Gate C (**blocking**); else lite review (Conditional lenses; **api** when Has API; **db** when Has DB) → lite test → Gate C (**blocking**) → merge only after yes

## Has API / API contract review

When **Has API = yes** in `00-run.md`:

- Design phase: isolated Task `API contract review` (stage id `api-contract-review`) — see `my-design-review-subflow/stages.md`.
- Review phase: include **api** in SPM plan → isolated Task `API contract lens` (stage id `spm-api`) — see `my-review-subflow/stages.md`.
- Skill: `api-and-interface-design`. Do not rely on parent chat or Quality alone for contract checks.

## Has DB / DB design review

When **Has DB = yes** in `00-run.md`:

- Design phase: isolated Task `DB design review` (stage id `db-design-review`) — see `my-design-review-subflow/stages.md`.
- Review phase: include **db** in SPM plan → isolated Task `Database review` (stage id `spm-db`) — see `my-review-subflow/stages.md`.
- Skill: `database-and-data-model`. Do not rely on parent chat or Quality alone for schema/migration/query checks.
