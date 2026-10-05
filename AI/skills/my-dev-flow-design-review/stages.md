# my-dev-flow-design-review stages

Stage-scoped handoff: `{my-dev-flow}/handoffs.md` → stage id `api-contract-review`, `db-design-review`, or `design-review`. Resolve paths per `{my-dev-flow}/skills-path.md`.  
Templates: `{my-dev-flow}/artifacts/03a-api-contract-review.md`, `03a-db-design-review.md`, `03a-design-review-log.md`. Severity: `{my-dev-flow}/severity.md`.

---

## 0a. API contract review (Verifier) — Medium — when Has API

**When:** `00-run.md` **Has API = yes**, or `03-design.md` defines new/changed public API contracts and Has API is unknown (treat as yes).

**Generation ≠ verification:** you did not write these contracts. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium (Fast if Medium unavailable)  
**Task description:** `API contract review`

**Done when:** `03a-api-contract-review.md` has Result **clean** or **needs update**. Overall round stays **needs update** if this file is not clean.

**Task prompt:**

```
You are a Senior API designer verifier for my-dev-flow-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find contract gaps; do not rewrite 01–04 yourself.

<Stage-scoped handoff for stage id api-contract-review from {my-dev-flow}/handoffs.md>

Read {api-and-interface-design}/SKILL.md (and reference.md if needed).
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

Write/update ONLY 03a-api-contract-review.md (template: {my-dev-flow}/artifacts/03a-api-contract-review.md).

Rules:
- Clean only if zero Critical and Major ({my-dev-flow}/severity.md). Defer Enhancement to Round notes.
- Simple plain words.
- Do not edit 01–04 or 03a-design-review-log.md. Do not write production code.
- Do not run the general design review or DB design review — those are separate Tasks.

Return: clean | needs update, and path to 03a-api-contract-review.md.
```

**If needs update:** parent may run design Update for API Fix ask items, then re-run this stage before or with general design review.

**If Has API = no:** skip this stage; do not create `03a-api-contract-review.md` or set Result **skipped** in Notes.

---

## 0b. DB design review (Verifier) — Medium — when Has DB

**When:** `00-run.md` **Has DB = yes**, or `03-design.md` defines new/changed Database contracts / migrations and Has DB is unknown (treat as yes).

**Generation ≠ verification:** you did not write these contracts. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium (Fast if Medium unavailable)  
**Task description:** `DB design review`

**Done when:** `03a-db-design-review.md` has Result **clean** or **needs update**. Overall round stays **needs update** if this file is not clean.

**Task prompt:**

```
You are a Senior Database designer verifier for my-dev-flow-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find schema/migration/query gaps; do not rewrite 01–04 yourself.

<Stage-scoped handoff for stage id db-design-review from {my-dev-flow}/handoffs.md>

Read {database-and-data-model}/SKILL.md.
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

Write/update ONLY 03a-db-design-review.md (template: {my-dev-flow}/artifacts/03a-db-design-review.md).

Rules:
- Clean only if zero Critical and Major ({my-dev-flow}/severity.md). Defer Enhancement to Round notes.
- Simple plain words.
- Do not edit 01–04 or 03a-design-review-log.md. Do not write production code.
- Do not run the general design review or API contract review — those are separate Tasks.

Return: clean | needs update, and path to 03a-db-design-review.md.
```

**If needs update:** parent may run design Update for DB Fix ask items, then re-run this stage before or with general design review.

**If Has DB = no:** skip this stage; do not create `03a-db-design-review.md` or set Result **skipped** in Notes.

---

## 1. Design review (Verifier) — Medium

**Generation ≠ verification:** you did not write this design. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Design review`

**Done when:** `03a-design-review-log.md` has overall Result **clean** or **needs update**. When Has API, `03a-api-contract-review.md` must be **clean** first. When Has DB, `03a-db-design-review.md` must be **clean** first.

**Task prompt:**

```
You are a Senior Architect verifier for my-dev-flow-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find gaps; do not rewrite 01–04 yourself.

<Stage-scoped handoff for design-review from {my-dev-flow}/handoffs.md>

Read 01-idea.md, 01a-idea-ui-review.md (if present), 02-skim.md (if present), 02-analysis.md, 02b-grill.md (if present), 03-design.md, 04-tasks.md.
Also read project AGENTS.md / docs/ARCHITECTURE.md / GLOSSARY.md when present.
Follow useful bits from myplan, planning-and-task-breakdown, documentation-and-adrs, security-and-hardening (OWASP required), and UI skills when UI.

If Has API = yes: read `03a-api-contract-review.md`. Do NOT deep-re-review API contracts; flag only cross-cutting gaps (e.g. tasks missing API acceptance). If that file is **needs update**, overall Result stays **needs update**.

If Has DB = yes: read `03a-db-design-review.md`. Do NOT deep-re-review schema/migrations/queries; flag only cross-cutting gaps. If that file is **needs update**, overall Result stays **needs update**.

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

Security / OWASP (design — light pass)
- Trust boundaries + abuse cases; OWASP table in `03-design.md` covers **design-time** risks (not code audit)
- Do not duplicate the full OWASP grid — spot gaps only; code OWASP is the **security lens** after Build
- Primary reference: https://owasp.org/Top10/

Improvements
- Concrete, practical suggestions

Write 03a-design-review-log.md (template: {my-dev-flow}/artifacts/03a-design-review-log.md):
- Overall Result: clean | needs update — **clean only if** API/DB isolated files are clean|skipped AND zero Critical/Major in this log ({my-dev-flow}/severity.md)
- Findings table: Severity, Area, Finding, Suggestion
- Fix ask for my-dev-flow-design: Critical/Major only; merge pointers to API/DB Fix ask files when those are open
- **Deferred Enhancements:** optional bullet list (do not block clean)
- Round notes

Rules:
- Clean only if zero Critical and Major (Enhancements → Deferred).
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
