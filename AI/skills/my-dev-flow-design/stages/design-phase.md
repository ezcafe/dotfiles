## design-phase — Design phase bundle (Architect) — High — Mode **simple** only

**When:** Mode **simple**. Replaces separate Analyze → Grill → Design Tasks. Mode **full** must use **analyze** → **grill** → **design** instead.

**Skills:** same as Analyze + Grill + Design.

**subagent_type:** `generalPurpose`  
**model:** resolved High  
**Task description:** `Design phase bundle`

**Done when:** `02-analysis.md` written; Grill **frontier-empty** or Notes skip; `03-design.md` + `04-tasks.md` ready for `design-verify-phase`.

**Task prompt:**

```
You are the Architect for my-dev-flow-design **design-phase** (Mode simple bundle). Fresh context only. Do Analyze → Grill (or skip) → Design in this one Task. Do not write production code.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py design-phase>

Read 00-run.md (Mode simple, HITL Grill, Has UI), 01-idea.md, and 01a / 02-skim when present.

### A — Analyze
Write 02-analysis.md (template). Deep dive What / Why / How; Mode simple Solution branches stub OK. Design tree (Settled / Open / Blocked). Set **Has API** and **Has DB** yes/no. Confirm or propose **Verify commands**. State Grill: **yes** if open frontier or Has API/DB; else **no**.

### B — Grill (or skip)
If Grill no: Notes reason; Result skipped for grill; do not invent 02b drama.
If Grill yes: follow {my-dev-flow}/grill.md; write 02b-grill.md; HITL Grill auto/async-notify → settle user-first now. Must reach frontier-empty before Design.

### C — Design
Write 03-design.md: one recommended design + ≤3-line rejected alternative. System design + Design patterns headings (N/A OK per templates). Sequence, API/DB contracts, OWASP, UI locks when Has UI. Write 04-tasks.md with acceptance (+ TDD notes or clear “no automated tests”).
Honor artifact size caps ([size-caps.md](../../my-dev-flow/size-caps.md)). Confirm Has API/DB again.

Return: Has API/DB + Verify commands + Grill result + paths to 02-analysis, 02b (or skip), 03-design, 04-tasks.
```

**After:** Parent copies Has API/DB + Verify commands into `00-run.md`. Next: `design-verify-phase` (not separate Analyze/Grill/Design).

---
