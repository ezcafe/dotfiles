## design — Design (Architect) — High

**Skills:** myplan (plan), planning-and-task-breakdown, documentation-and-adrs, api-and-interface-design if APIs, database-and-data-model if DB, security-and-hardening (OWASP), UI skills when UI.

**subagent_type:** `generalPurpose`  
**model:** resolved High

**Done when:** `03-design.md` + `04-tasks.md` ready for design-review (TDD review + Gate B come after).

**Task prompt:**

```
You are the Architect for my-dev-flow-design Design. Fresh context only.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py design>

Read 01-idea.md, 02-skim.md, 02-analysis.md, and 02b-grill.md when present. When Has UI, specify UI in design — align Gate A #1/#2 and existing chrome; **lock Build** to those Design UI specs.
Honor grill Settled decisions and glossary terms — do not re-open frontier-empty branches without new evidence.
Build on analysis Deep dive (What / Why / How + **Solution branches** + alternatives + best practices). Design Decision options should reflect Solution branches (systemic / creative) and analysis alternatives unless settled in analysis or grill. Quick wins → early tasks and/or Non-goals if deferred. Honor `01-idea` Core problem and ★ priority.
Follow myplan plan, planning-and-task-breakdown, documentation-and-adrs, api-and-interface-design if needed, database-and-data-model if DB, security-and-hardening (OWASP required), UI skills + DESIGN_GUIDE when UI.
If grill wrote an ADR path, link it in 03-design Domain / ADR notes; if ADR skipped with reason, keep that note.

Write 03-design.md:
- Mode **full:** Decision 1 with Option 1/2 (What / Example / Pros / Cons / Recommendation).
- Mode **simple:** one recommended design (Option 1) + ≤3-line rejected alternative (full Option 1/2 only if 2+ approaches still unsettled).
Also: **System design** (triggers in templates — Has API/DB → Overview required; else N/A OK; anti-dupe vs sequence/contracts; line budgets; optional Concept N), **Design patterns used** (code patterns only; teach shape or N/A; ≤3), sequence diagram, API/DB contracts, example queries, UI/UX/mobile when Has UI (align with Gate A / 01a — state Build must match Design UI specs; do not re-argue 80/20), OWASP table, aggressive challenges. Honor artifact size caps ([size-caps.md](../../my-dev-flow/size-caps.md)). Follow templates mini-example quality bar (do not paste the example verbatim).

**User-first:** Recommendation must prefer day-to-day user value over system convenience; say so in one line.

Write 04-tasks.md: S/M tasks with acceptance + TDD test notes when tests are needed; security + UI/mobile checks when applicable; when Has UI, acceptance must include Design UI locks. If no automated tests are planned, say so clearly (parent will skip 04a).

Ask: “Is this design clear? Which option do you approve? Any concerns before build?”
Confirm **Has API** yes/no (public HTTP/GraphQL/server-action/contracts changed?).
Confirm **Has DB** yes/no (schema / migrations / persistence queries changed?).
No production code.
Return: options summary + Recommendation + Has API (yes/no) + Has DB (yes/no) + path to design/tasks.
```

**After (standalone):** Prefer design-review → TDD → **Gate B** → Build.  
**After (parent my-dev-flow):** Parent sets/refines **Has API** and **Has DB** in `00-run.md`. Do **not** Gate B yet — design-review loop (with **API contract review** when Has API **and** not Notes `tiny-contract-tweak`; **DB design review** when Has DB **and** not Notes `tiny-contract-tweak`; tiny-tweak folds into general design-review / design-verify-phase — `{my-dev-flow}/lenses.md`), then TDD, then Gate B, then Build.

---
