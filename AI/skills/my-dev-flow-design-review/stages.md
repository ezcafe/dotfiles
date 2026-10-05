# my-dev-flow-design-review stages

Stage-scoped handoff: `~/.cursor/skills/my-dev-flow/handoffs.md` → stage id `api-contract-review`, `db-design-review`, or `design-review`.  
Log template: same file → “03a-design-review-log.md”.

---

## 0a. API contract review (Verifier) — Medium — when Has API

**When:** `00-run.md` **Has API = yes**, or `03-design.md` defines new/changed public API contracts and Has API is unknown (treat as yes).

**Generation ≠ verification:** you did not write these contracts. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium (Fast if Medium unavailable)  
**Task description:** `API contract review`

**Done when:** `03a-design-review-log.md` → **API contract review** section has Result **clean** or **needs update** with findings. Overall round stays **needs update** if this section is not clean.

**Task prompt:**

```
You are a Senior API designer verifier for my-dev-flow-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find contract gaps; do not rewrite 01–04 yourself.

<Stage-scoped handoff for stage id api-contract-review from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read ~/.cursor/skills/api-and-interface-design/SKILL.md (and reference.md if needed).
Read 02-analysis.md, 03-design.md (API/DB contracts + sequence), 04-tasks.md, and 02-skim.md if present.
Also read project AGENTS.md / docs/ARCHITECTURE.md / existing route patterns when present.

Review API contracts against best practices:

- Contract first: typed operations, inputs, outputs, failure modes
- One error strategy and stable body shape
- Validate at edges only
- Lists: pagination from day one; clear filters
- Addition over modification; no silent breaks
- Predictable naming matching the repo
- Idempotency for state-changing endpoints (or explicit unsafe-to-retry)
- Auth / ownership / trust boundaries called out for each mutating path
- Sequence diagram covers main path + key failure returns for APIs in scope
- Tasks include acceptance that would catch contract mistakes

Write/update ONLY the “API contract review” section in 03a-design-review-log.md:
- Result: clean | needs update
- Findings table (Area: contracts / practice)
- Short API checklist notes
- Contribute numbered Fix ask items for my-dev-flow-design (API-related only)

Rules:
- Clean only if zero Critical, Major, and Enhancement in this section.
- Simple plain words.
- Do not edit 01–04. Do not write production code.
- Do not run the general design review or DB design review — those are separate Tasks.

Return: clean | needs update, and path to 03a-design-review-log.md.
```

**If needs update:** parent may run design Update for API Fix ask items, then re-run this stage before or with general design review.

**If Has API = no:** skip this stage; set API section Result to **skipped**.

---

## 0b. DB design review (Verifier) — Medium — when Has DB

**When:** `00-run.md` **Has DB = yes**, or `03-design.md` defines new/changed Database contracts / migrations and Has DB is unknown (treat as yes).

**Generation ≠ verification:** you did not write these contracts. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium (Fast if Medium unavailable)  
**Task description:** `DB design review`

**Done when:** `03a-design-review-log.md` → **DB design review** section has Result **clean** or **needs update** with findings. Overall round stays **needs update** if this section is not clean.

**Task prompt:**

```
You are a Senior Database designer verifier for my-dev-flow-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find schema/migration/query gaps; do not rewrite 01–04 yourself.

<Stage-scoped handoff for stage id db-design-review from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read ~/.cursor/skills/database-and-data-model/SKILL.md.
Read 02-analysis.md, 03-design.md (Database contracts + example queries + sequence), 04-tasks.md, and 02-skim.md if present.
Also read project AGENTS.md (Database / Drizzle section when present), docs/ARCHITECTURE.md, and existing db/schema + migration patterns when present.

Review database design against best practices:

- Schema contract: tables/columns typed; nullability/defaults clear
- Indexes / uniques match real filters, joins, and idempotency needs
- Write owner + read owners documented per table
- Migrations additive or expand→migrate→contract for breaks; backfill plan if needed
- Multi-step writes: transaction or compensating path
- Example queries use safe binds (no bad JS-array → ::type[]; prefer inArray / sql.join)
- Money/large aggregates stay bigint — no SUM → ::int
- Lists bounded; no obvious N+1 in the designed access path
- Tenant/ownership filters on mutating and sensitive reads
- Tasks include acceptance that would catch missing migration, wrong nullability, or missing unique
- Sequence diagram covers main DB reads/writes + key failure returns when DB is in scope

Write/update ONLY the “DB design review” section in 03a-design-review-log.md:
- Result: clean | needs update
- Findings table (Area: schema / migration / query / ownership / practice)
- Short DB checklist notes
- Contribute numbered Fix ask items for my-dev-flow-design (DB-related only)

Rules:
- Clean only if zero Critical, Major, and Enhancement in this section.
- Simple plain words.
- Do not edit 01–04. Do not write production code.
- Do not run the general design review or API contract review — those are separate Tasks.

Return: clean | needs update, and path to 03a-design-review-log.md.
```

**If needs update:** parent may run design Update for DB Fix ask items, then re-run this stage before or with general design review.

**If Has DB = no:** skip this stage; set DB section Result to **skipped**.

---

## 1. Design review (Verifier) — Medium

**Generation ≠ verification:** you did not write this design. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Design review`

**Done when:** `03a-design-review-log.md` has overall Result **clean** or **needs update** with a concrete Fix ask. When Has API, overall clean requires API section already **clean**. When Has DB, overall clean requires DB section already **clean**.

**Task prompt:**

```
You are a Senior Architect verifier for my-dev-flow-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find gaps; do not rewrite 01–04 yourself.

<Stage-scoped handoff for design-review from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read 01-idea.md, 01a-idea-ui-review.md (if present), 02-skim.md (if present), 02-analysis.md, 02b-grill.md (if present), 03-design.md, 04-tasks.md.
Also read project AGENTS.md / docs/ARCHITECTURE.md / GLOSSARY.md when present.
Follow useful bits from myplan, planning-and-task-breakdown, documentation-and-adrs, security-and-hardening (OWASP required), and UI skills when UI.

If Has API = yes: an isolated API contract review Task already filled the “API contract review” section. Do NOT deep-re-review API contracts; you may flag only obvious cross-cutting gaps (e.g. tasks missing API acceptance) and must not clear an unclean API section.

If Has DB = yes: an isolated DB design review Task already filled the “DB design review” section. Do NOT deep-re-review schema/migrations/queries; you may flag only obvious cross-cutting gaps (e.g. tasks missing migration acceptance) and must not clear an unclean DB section.

Review against real-world best practices. Check at least:

Gaps / clarity
- Missing success criteria, non-goals, or open questions that still block build
- **Problem map missing or thin** — Mode **full:** `01-idea.md` must have Steps 1–2 (happening / missing / consequences → surface vs root → Core problem one sentence) + mind map with ★ priority; fail Major if skipped or hand-wavy. Mode **simple:** Core problem line or stub OK
- **Analyze deep dive missing or thin** — `02-analysis.md` must answer What / Why / How (other ways + best practices) for overall change and major solution pieces; Mode **full** also requires **Solution branches** (Quick wins / Systemic / Creative) tied to Core problem; fail Major if skipped or hand-wavy
- **Grill** — Mode full: `02b-grill.md` should be frontier-empty (or explicitly skipped with reason in Notes). Fail **Major** if Build-critical open frontier remains, or Design re-opens Settled grill decisions without new evidence. Mode simple: ok if grill skipped when frontier was empty.
- Spike notes (if any) must not contradict deep dive without explanation; spike must not be treated as shipped design without Design update
- Vague contracts (API/DB) or missing error / auth / ownership — if Has API and API section already reviewed, note “see API contract review”; if Has DB and DB section already reviewed, note “see DB design review”
- Sequence diagram missing actors, main path, or key failure returns
- Tasks too big, no acceptance, or no TDD “what turns red first”
- Missing or thin **System design** — heading required. Overview required when Has API or Has DB (or Mode full + new boundary); else `N/A` with reason OK. Fail **Major** if Overview required but missing/N/A wrongly, hand-wavy, invents a shape that conflicts with `docs/ARCHITECTURE.md` / skim without saying why, or **restates** sequence/contracts field-by-field. Fail **Enhancement** if name-drops without teaching when Overview is present.
- Missing or thin **Design patterns used** — heading required. Teach each pattern (What / How here / Why / Best practices + anti-patterns / Reference), or `N/A` with reason. Fail **Major** if invent-new when a repo pattern exists. Fail **Enhancement** if section only name-drops without teaching (Mode full + patterns claimed). Fail **Major** in Mode full when Analysis listed reusable patterns and Design skipped them without reason.
- Domain / ADR notes — if Design claims a hard-to-reverse surprising trade-off with no ADR and no “ADR skipped” reason → Enhancement (or Major when Has API/DB architecture fork)
- Skim hard constraints ignored
- Same concept dumped in both System design and Design patterns without saying which lens → Enhancement

Correctness / fit
- Conflicts with repo patterns, system architecture, or analysis reference files
- System design / Design patterns **Best practices** ignored by tasks (tasks contradict taught practices) → Major
- Design options ignore analysis Solution branches / alternatives without reason (Mode simple: one option + short rejected alternative is OK)
- Over-building vs idea outcome / Core problem; under-specified failure modes
- Data model / indexes / uniques that will hurt later — if Has DB and DB section reviewed, note “see DB design review” instead of duplicating

UI / UX / mobile (when UI is in scope)
- **Alignment only with Gate A / 01a / Design UI** — do NOT re-argue 80/20 goals if Gate A was ok
- Fail (Critical/Major) if 03-design layout/IA **drifts** from Gate A #1/#2 or Design UI locks when Has UI
- When Has UI: fail Major if Design/tasks lack clear UI locks for Build
- Loading / empty / error / success; skeleton parity; mobile ≥44px; no hover-only; a11y basics

Security / OWASP (always)
- Trust boundaries + abuse cases; OWASP Top 10 table complete
- Primary reference: https://owasp.org/Top10/

Improvements
- Concrete, practical suggestions

Write 03a-design-review-log.md:
- Overall Result: clean | needs update — **clean only if** API section is clean|skipped AND DB section is clean|skipped AND this review has zero Critical/Major/Enhancement
- Findings table: Severity, Area, Finding, Suggestion
  Area tags may include: idea / ui / skim / analysis / grill / design / tasks / contracts / diagram / system-design / pattern / ui-ux / security-owasp / practice / api-contract / db-design / glossary-adr
- Fix ask for my-dev-flow-design: numbered, actionable (merge with any open API / DB Fix ask items)
- Round notes

Rules:
- Clean only if zero Critical, Major, and Enhancement (including API section when Has API and DB section when Has DB).
- Simple plain words.
- Do not edit 01–04. Do not write production code.

Return: clean | needs update, and path to 03a-design-review-log.md.
```

**If needs update:** parent runs `my-dev-flow-design` Update, then **re-runs** from API contract review (when Has API) and/or DB design review (when Has DB), then this stage.

**If clean:** parent continues (TDD → Gate B → Build → Smoke → review/test per Review profile). Ensure **Lens plan** will include **api** when Has API and **db** when Has DB.

---

## Parent loop hint (my-dev-flow)

```
my-dev-flow-design (Ideation → Gate A → skim → Analyze → Grill → Design; set Has API + Has DB)
→ my-dev-flow-design-review
   → if Has API: API contract review Task
   → if Has DB: DB design review Task
   → Design review Task
→ if needs update → Update → re-review (max 3)
→ my-dev-flow-code (TDD review only)
→ Gate B
→ my-dev-flow-code (Build)
→ my-dev-flow-test (Smoke)
→ my-dev-flow-review (include api lens when Has API; db lens when Has DB)
→ my-dev-flow-test (Full|lite)
→ Gate C → merge
```
