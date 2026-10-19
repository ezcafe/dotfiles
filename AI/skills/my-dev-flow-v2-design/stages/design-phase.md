## design-phase — Design phase bundle (Architect) — High — Mode **simple** only

**When:** Mode **simple**. Replaces separate Analyze → Grill → Design Tasks. Mode **full** must use **analyze** → **grill** → **design** instead.

**Skills:** same as Analyze + Grill + Design.

**subagent_type:** `generalPurpose`  
**model:** resolved High  
**Task description:** `Design phase bundle`

**Done when:** `02-analysis.md` written; Grill **frontier-empty** or Notes skip; `03-design.md` + `04-tasks.md` ready for `design-verify-phase`.

**Task prompt:**

```
You are the Architect for my-dev-flow-v2-design **design-phase** (Mode simple bundle). Fresh context only. Do Analyze → Grill (or skip) → Design in this one Task. Do not write production code.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for design-phase>

Read 00-run.md (Mode simple, HITL Grill, Has UI), 01-idea.md, and 01a / 02-skim when present.

### A — Analyze
Write 02-analysis.md (template). Deep dive What / Why / How; Mode simple Solution branches stub OK. Design tree (Settled / Open / Blocked). Set **Has API**, **Has DB**, and **Has auth/PII/schema** yes/no. Confirm or propose **Verify commands**. State Grill: **yes** if open frontier or Has API/DB; else **no**.

### B — Grill (or skip)
If Grill no: Notes reason; Result skipped for grill; do not invent 02b drama.
If Grill yes: follow {my-dev-flow-v2}/grill.md; write 02b-grill.md; HITL Grill auto/async-notify → settle user-first now. Must reach frontier-empty before Design.

### C — Design
Write 03-design.md: one recommended design + ≤3-line rejected alternative. System design + Design patterns headings (N/A OK per templates). Sequence, API/DB contracts, OWASP, UI locks when Has UI. Write 04-tasks.md with acceptance (+ TDD notes or clear “no automated tests”).
Honor artifact size caps ([size-caps.md](../../my-dev-flow-v2/size-caps.md)). Confirm Has API/DB and Has auth/PII/schema again.

Return: Has API/DB + Has auth/PII/schema + Verify commands + Grill result + paths to 02-analysis, 02b (or skip), 03-design, 04-tasks.
```

**After:** Parent copies Has API/DB + Has auth/PII/schema + Verify commands into `00-run.md`. When any of Has API / Has DB / Has auth/PII/schema becomes **yes**, parent **MUST** set **HITL Gate B** = **blocking** per [gate-b.md](../../my-dev-flow-v2/gate-b.md) before Gate B/Build. Next: `design-verify-phase` (not separate Analyze/Grill/Design).

---
