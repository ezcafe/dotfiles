# my-dev-flow-design stages

Copy the **Task prompt** for the current stage. Fill bracketed paths. Use simple plain words.

Stage-scoped handoff: see `~/.cursor/skills/my-dev-flow/handoffs.md` → stage id table (`ideation`, `gate-a`, `skim`, `analyze`, `grill`, `design`, `design-update`, …).

Parent uses the **resolved** model for that stage’s tier (see `00-run.md`).

---

## 1. Ideation (PO) — Medium

**Skills:** `~/.cursor/skills/myplan/SKILL.md` (discovery + specify only).

**subagent_type:** `generalPurpose`  
**model:** resolved Medium

**Done when:** `01-idea.md` filled; **Has UI** set in `01-idea.md` and parent copies to `00-run.md`; ready for Gate A.

**Task prompt:**

```
You are the Product Owner for my-dev-flow-design Ideation. Fresh context only — do not assume prior chat.

Read and follow: ~/.cursor/skills/myplan/SKILL.md (discovery + specify only — no plan/code).

User idea / request:
<paste user request>

Mode hint from parent (if any): full | simple

Quick-scan the repo first (README, AGENTS.md, related features). Summarize the project shape in 1–3 short sentences.

Investigate the question against primary sources (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.

Then draft .my-docs/workflow/<slug>/01-idea.md using the template from ~/.cursor/skills/my-dev-flow/artifacts.md.

Must include:
- **Problem map (diagnose before framing):**
  - Mode **full:** Step 1 three WHAT branches (happening / missing-wrong / consequences, 3–5 each); Step 2 surface vs root + **Core problem** one sentence; visual text mind map with ★ top priority
  - Mode **simple:** stub OK — Core problem one line + `N/A — root cause clear`, or 3–5 bullets total
- Problem (one-line restatement of Core problem), User / audience, Outcome (align with ★), Metric
- **Has UI:** yes | no (required — parent will copy into 00-run.md before Gate A)
- Copy/token-only? UI notes for Design?
- 80/20 UI (if UI): main user goals; vital few; Important info/action #1 and #2 always visible with secondary in menus/expand/modal; top journey; sensible defaults; biggest usability risks first (or `N/A — no UI`)
- Non-goals, Assumptions to attack, Success criteria, Open questions
- **Sources (primary):** paths / URLs / APIs that own each material claim (not blog summaries of those sources)

Diagnose before Outcome — do not jump to solution framing until Core problem is written.
Ask blocking questions only if the idea cannot be reviewed without an answer. Prefer writing Open questions into 01-idea.md and continuing to Gate A.

Do not write code. Do not write the technical design yet.
Do not invent Solution branches here — those belong in Analyze.
Do not treat secondary write-ups (blogs, Stack Overflow, AI summaries of docs) as the authority when a primary source exists.
Return: short summary + path to 01-idea.md + Has UI value + any blocking questions (or none).
```

**After:** Parent sets **Has UI** in `00-run.md` from `01-idea.md`. If true blockers, pause; else continue to **Gate A**.

---

## 1b. Gate A — User-role day-to-day review (Medium)

**Role:** end user who would use this in day-to-day work (not PO, not architect).

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `User day-to-day review`

**Done when:** `01a-idea-ui-review.md` written with Result **ok** | **needs update** | **escalate**.

**Task prompt:**

```
You are an end user reviewing the product idea for day-to-day usage. Fresh context only — do not assume prior chat. You are NOT the Product Owner and NOT the Architect.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read only:
- .my-docs/workflow/<slug>/01-idea.md

Ignore technical design. Judge whether this idea would work in real daily use.

Also check **Problem map / Core problem** (product clarity, not engineering):
- Is the **Core problem** one clear sentence a real user would recognize?
- Does Outcome match the ★ top priority (when present)?
- Mode full: if Problem map is missing or Core problem is vague → Result **needs update** (Major).

**80/20 UI rule (required when the idea has UI)** — review and fill every section in the 01a template:

1. **Main user goals**
2. **Vital few**
3. **Core actions visually dominant** — Important info/action **#1** and **#2** always visible; secondary in menus/overflow/expand/modal
4. **Biggest usability problems first**
5. **Simplify**
6. **Top user journeys**
7. **Sensible defaults**
8. **Test, measure, repeat**

Also review for: convenience, easy to use, understanding, mobile usability (or n/a), eye reading flow.

Write .my-docs/workflow/<slug>/01a-idea-ui-review.md using the template from ~/.cursor/skills/my-dev-flow/artifacts.md.
Fill all 80/20 sections and set **80/20 overall pass?** yes/no.

Set Result:
- **ok** — no Critical/Major gaps; **80/20 overall pass**; day-to-day checklist acceptable → parent will auto-approve Gate A
- **needs update** — Fix ask lists concrete changes to 01-idea.md
- **escalate** — only if unsafe, unethical, or too unclear without a human

Do not write code. Do not rewrite 01-idea.md yourself.
Return: Result + short summary + path to 01a-idea-ui-review.md.
```

**After (parent):**

1. If Result **ok** → check **Gate A** in `00-run.md`; Run log `done · Gate A — ok · auto-approved`.
2. Confirm **Has UI** still matches `01-idea.md`.
3. Continue to **Light skim** (stage 1s).
4. If **needs update** → Ideation update → re-run Gate A (max 3). Then pause for human.
5. If **escalate** → pause for human.

---

## 1c. Ideation update from Gate A (Medium)

**When:** `01a` Result is **needs update**.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Update idea from review`

**Done when:** Fix-ask items addressed in `01-idea.md`.

**Task prompt:**

```
You are the Product Owner updating ideation from the user-role day-to-day review (Gate A). Fresh context only.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read 01a-idea-ui-review.md (Findings + Fix ask). Read 01-idea.md.

Rules:
- Update only listed Fix-ask items in 01-idea.md.
- Keep full **80/20 UI** when UI applies; keep **Has UI** accurate.
- Append a short note under 01a → Round notes.
- No production code. Simple plain words.

Return: what you updated in 01-idea.md.
```

**After:** Parent re-runs Gate A. Do not claim Gate A approved yet.

---

## 1s. Light repo skim (Medium)

**When:** After Gate A **ok**. Always run in full mode (short; constraints only).

**subagent_type:** `explore` or `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Light repo skim`

**Done when:** `02-skim.md` Result **done**.

**Task prompt:**

```
You are doing a light repo skim for my-dev-flow-design. Fresh context only. This is NOT full Analyze — constraints and reuse pointers only.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read 01-idea.md and 01a-idea-ui-review.md (Gate A ok).

Scan the repo for related screens, components, APIs, and hard constraints. Prefer concrete paths.

Write .my-docs/workflow/<slug>/02-skim.md using the template from ~/.cursor/skills/my-dev-flow/artifacts.md.

Must include: project shape (1–3 sentences), related UI paths, related APIs/data, hard constraints, risks if ignored, enough for Analyze/Design?

Do not write production code. Do not write full analysis or design.
Return: short summary + path to 02-skim.md.
```

**After:** Parent continues:

- Proceed to Analyze after skim (UI specs come later in Design).

---


## 2. Analyze + Q&A (Architect) — High

**Skills:** explore; if UI, `dev-decision-routing`.

**subagent_type:** `explore` or `generalPurpose`  
**model:** resolved High

**Done when:** `02-analysis.md` written with mandatory deep dive; builds on skim; honors Gate A / Design UI direction when Has UI.

**Mandatory deep dive** (feature + each major solution piece; ask user when unclear):

1. **What is this?** (align with Core problem)
2. **Why do we need this?**
3. **How to do this?** Other ways? Best practices?
4. **Solution branches** from Core problem: Quick wins / Systemic / Creative — Mode full required; Mode simple stub OK. Mark ★ priority; map to Design.

**Spike (optional):** throwaway exploration only — same What/Why/How; record findings in `02-analysis.md` Spike notes. Do not ship spike code.

**Task prompt:**

```
You are the Architect for my-dev-flow-design Analyze + Q&A. Fresh context only.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read 01-idea.md (Gate A ok) and 02-skim.md.
When Has UI, explore how to implement within Gate A 80/20 and existing app chrome; do not invent a conflicting IA.
Explore the codebase for related patterns, APIs, schemas, and UI. Expand skim — do not ignore skim hard constraints.

If front-end work, read ~/.cursor/skills/dev-decision-routing/SKILL.md.

Deep dive required — for the overall change and each major solution piece, fill in 02-analysis.md:
1. What is this? (plain words) — align with 01-idea Core problem / Problem map
2. Why do we need this? (outcome; cost of skipping) — use Consequences from Problem map when present
3. How to do this? List other ways. Note best practices (repo patterns first, then industry).
Also fill **Solution branches** (from Core problem):
- Branch 1 Quick wins (low effort, immediate)
- Branch 2 Systemic fixes (process / preventative / structural)
- Branch 3 Creative / lateral options
Mark ★ priority branch for this pass. Map branches to Design (full: Option 1/2 from systemic/creative; simple: one recommended; quick wins → early tasks or Non-goals if deferred).
Mode simple: one recommended branch + ≤2-line note on the other two (or `N/A — single clear path`).
If 2+ real approaches, use Decision N Option shape (What / Example / Pros / Cons / Recommendation).
Ask the user when any of these are unclear — do not guess.

Optional spike: throwaway exploration only to reduce uncertainty. Same What/Why/How before and after. Write Spike notes into 02-analysis.md. Do not leave findings only in chat. Do not treat spike as production Build.

Write 02-analysis.md (template) including Deep dive (+ Solution branches), **Design tree (frontier)** (Settled / Open frontier / Blocked), **Reusable patterns**, **System shape candidates**, and optional Spike notes.
Ask: “Are the instructions and reference files clear enough to design? Any gaps in What / Why / How?”

Also state whether this change touches public APIs / contracts (**Has API** yes/no) and whether it touches schema / migrations / persistence queries (**Has DB** yes/no) so the parent can set 00-run.md.
State whether Grill should run: **yes** if Open frontier or unsettled Decisions remain; **no** if frontier already empty (simple clear asks).

Do not write production code. Do not finalize design yet.
Return: short summary + deep-dive highlights + open questions + Design tree summary + Grill recommended? + Has API recommendation (yes/no) + Has DB recommendation (yes/no).
```

**After:** Parent may answer Q&A, sets/refines **Has API** and **Has DB** in `00-run.md` from Analyze return, then **Grill** (or skip per [`my-dev-flow/grill.md`](../my-dev-flow/grill.md) rules), then Design (or pause if blocked).

---

## 2g. Grill + domain modeling (Medium)

**When:** After Analyze. Mode **full** — always (unless `02b` already `frontier-empty` and artifacts unchanged). Mode **simple** — when Analyze Design tree has open frontier / unsettled Decisions, or Has API/DB; else skip.

**Rules:** `~/.cursor/skills/my-dev-flow/grill.md` + `documentation-and-adrs`.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Grill design tree`

**Done when:** `02b-grill.md` Result **frontier-empty** or **skipped**; glossary/ADR updated when terms/decisions qualify.

**HITL:** Honor **HITL Gate B** in `00-run.md`. Default **auto** / **async-notify** → apply user-first recommendations and settle the frontier in this Task (do not wait). **blocking** → write open frontier with recommendations; parent pauses for human answers, then re-run or parent applies answers.

**Task prompt:**

```
You are grilling the design tree for my-dev-flow-design. Fresh context only. Follow ~/.cursor/skills/my-dev-flow/grill.md and documentation-and-adrs.

<Stage-scoped handoff for stage id grill from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read 00-run.md (Mode, HITL Gate B, Has API/DB), 01-idea.md, 02-skim.md (if present), 02-analysis.md (especially Design tree + Blocking questions + Settled decisions).
Read repo GLOSSARY.md or GLOSSARY-MAP.md if present. Cross-check claims against code when needed — look up facts yourself; do not ask the user for look-up-able facts.

Build the design tree. Work the frontier in rounds:
- List only questions whose prerequisites are settled
- Each question: title, body, choices when 2+, Recommended answer with user-first one-liner
- Invent 1–3 concrete edge scenarios that stress domain boundaries; record outcomes
- If HITL is auto or async-notify (default): settle each recommended answer now; log auto-pick rationale
- If HITL is blocking: leave frontier open with recommendations; Result needs-round

Domain modeling:
- When a term resolves, update GLOSSARY.md (or mapped context glossary) immediately — definitions only, _Avoid_ aliases
- Offer/write an ADR only if hard-to-reverse AND surprising AND real trade-off (short 1–3 sentence form preferred). Else note ADR skipped.

Write .my-docs/workflow/<slug>/02b-grill.md using the template.
Also update 02-analysis.md Design tree + Settled decisions so frontier is empty when settled.

Do not write production feature code. Do not write 03-design yet. Do not re-litigate Gate A 80/20.
Return: Result (frontier-empty | needs-round | skipped) + Grill digest (≤4 bullets) + paths touched (02b, glossary, ADR).
```

**After (parent):**

1. If **skipped** → Notes `grill skipped — <reason>`; continue to Design.
2. If **frontier-empty** → post Grill digest; Run log `done · Step 2g — Grill · frontier-empty · auto` (or blocking settled); continue to Design.
3. If **needs-round** and HITL **blocking** → pause with digest; after human answers, re-run Grill or parent applies answers into `02b` then Design.
4. If **needs-round** under auto (should be rare) → parent user-first settles remaining frontier into `02b`, then Design.

---

## 3. Design (Architect) — High

**Skills:** myplan (plan), planning-and-task-breakdown, documentation-and-adrs, api-and-interface-design if APIs, database-and-data-model if DB, security-and-hardening (OWASP), UI skills when UI.

**subagent_type:** `generalPurpose`  
**model:** resolved High

**Done when:** `03-design.md` + `04-tasks.md` ready for design-review (TDD review + Gate B come after).

**Task prompt:**

```
You are the Architect for my-dev-flow-design Design. Fresh context only.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read 01-idea.md, 02-skim.md, 02-analysis.md, and 02b-grill.md when present. When Has UI, specify UI in design — align Gate A #1/#2 and existing chrome; **lock Build** to those Design UI specs.
Honor grill Settled decisions and glossary terms — do not re-open frontier-empty branches without new evidence.
Build on analysis Deep dive (What / Why / How + **Solution branches** + alternatives + best practices). Design Decision options should reflect Solution branches (systemic / creative) and analysis alternatives unless settled in analysis or grill. Quick wins → early tasks and/or Non-goals if deferred. Honor `01-idea` Core problem and ★ priority.
Follow myplan plan, planning-and-task-breakdown, documentation-and-adrs, api-and-interface-design if needed, database-and-data-model if DB, security-and-hardening (OWASP required), UI skills + DESIGN_GUIDE when UI.
If grill wrote an ADR path, link it in 03-design Domain / ADR notes; if ADR skipped with reason, keep that note.

Write 03-design.md:
- Mode **full:** Decision 1 with Option 1/2 (What / Example / Pros / Cons / Recommendation).
- Mode **simple:** one recommended design (Option 1) + ≤3-line rejected alternative (full Option 1/2 only if 2+ approaches still unsettled).
Also: **System design** (triggers in templates — Has API/DB → Overview required; else N/A OK; anti-dupe vs sequence/contracts; line budgets; optional Concept N), **Design patterns used** (code patterns only; teach shape or N/A; ≤3), sequence diagram, API/DB contracts, example queries, UI/UX/mobile when Has UI (align with Gate A / 01a — state Build must match Design UI specs; do not re-argue 80/20), OWASP table, aggressive challenges. Honor artifact size caps. Follow templates mini-example quality bar (do not paste the example verbatim).

**User-first:** Recommendation must prefer day-to-day user value over system convenience; say so in one line.

Write 04-tasks.md: S/M tasks with acceptance + TDD test notes when tests are needed; security + UI/mobile checks when applicable; when Has UI, acceptance must include Design UI locks. If no automated tests are planned, say so clearly (parent will skip 04a).

Ask: “Is this design clear? Which option do you approve? Any concerns before build?”
Confirm **Has API** yes/no (public HTTP/GraphQL/server-action/contracts changed?).
Confirm **Has DB** yes/no (schema / migrations / persistence queries changed?).
No production code.
Return: options summary + Recommendation + Has API (yes/no) + Has DB (yes/no) + path to design/tasks.
```

**After (standalone):** Prefer design-review → TDD → **Gate B** → Build.  
**After (parent my-dev-flow):** Parent sets/refines **Has API** and **Has DB** in `00-run.md`. Do **not** Gate B yet — design-review loop (with **API contract review** when Has API; **DB design review** when Has DB), then TDD, then Gate B, then Build.

---

## Update from design review (Architect) — High

**When:** `03a` Result is **needs update**.

**subagent_type:** `generalPurpose`  
**model:** resolved High  
**Task description:** `Update design docs`

**Done when:** Fix-ask items addressed; parent re-runs design-review.

**Task prompt:**

```
You are the Architect for Update from design review. Fresh context only. Repair only what 03a Fix ask lists; keep Gate A idea. Do not re-litigate Gate A 80/20 unless Fix ask requires it.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read 03a, 01-idea, 02-skim, 02-analysis, 02b-grill (if present), 03-design, 04-tasks.

Rules:
- Update only Fix-ask items.
- Keep Decision options shape, System design (triggers + teach or N/A; no dupe of contracts), diagram, contracts, Design patterns used (teach What/How/Why/Best practices or N/A), UI alignment with Gate A / Design specs when Has UI, OWASP accurate.
- Honor grill Settled decisions unless Fix ask re-opens a branch.
- If UI layout drifts from Gate A #1/#2 or Design UI locks, restore alignment.
- Append Round notes on 03a.
- No production code.

Return: what you updated, which files.
```

**After:** Parent re-runs `my-dev-flow-design-review`.

---

## Clarity check (parent)

Before Analyze and Design:

> Are the instructions, dependencies, and reference files clear enough to proceed?

Before Grill / Design, also confirm:

- `01-idea.md` **Problem map** — Mode full: Steps 1–2 + mind map + Core problem present; Mode simple: stub or Core problem line OK
- `02-analysis.md` Deep dive answers (or user-confirmed open questions for):
  1. **What is this?**
  2. **Why do we need this?**
  3. **How to do this?** (other ways + best practices + **Solution branches** when Mode full)

Before Design, confirm Grill is **frontier-empty** or **skipped** (see `02b-grill.md` / Notes). Do not start Design on `needs-round`.

If no → ask the user; do not launch the next stage.
