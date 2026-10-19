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
Honor artifact size caps already inlined/pasted in this handoff (link optional — open `{my-dev-flow-v2}/size-caps.md` only if a needed cap is missing from the paste). Confirm Has API/DB and Has auth/PII/schema again.

Return: Has API/DB + Has auth/PII/schema + Verify commands + Grill result + paths to 02-analysis, 02b (or skip), 03-design, 04-tasks.
```

**After:** Parent copies Has API/DB + Has auth/PII/schema + Verify commands into `00-run.md`.

1. **Grill gate:** advance only when Grill Result is **`frontier-empty`** or **`skipped`** (or Notes grill-skip). On Grill open **and** (design artifacts present **or** `02b` Result **`needs-round`**) → Expected Next = **`grill`** (Task or parent apply into `02b`; card Next stays `grill` until Grill closed). Do **not** Prefer re-`design-phase` while that Prefer matches; do **not** launch `design-verify-phase`. Prefer `design-phase` on Grill open **only** for true cold start: no `02b` **needs-round** **and** no design artifacts — [derive-next-pre.md](../../my-dev-flow-v2/derive-next-pre.md) · [grill.md](../../my-dev-flow-v2/grill.md).
2. **Has flip:** when any of Has API / Has DB / Has auth/PII/schema becomes **yes**, parent **MUST** drop Review profile **skip-review** → **lite** (or Decision N reclassify to full) **and** set **HITL Gate B** = **blocking** per [gate-b.md](../../my-dev-flow-v2/gate-b.md) · [lenses.md](../../my-dev-flow-v2/lenses.md) before Gate B/Build. Also apply [lenses.md](../../my-dev-flow-v2/lenses.md) Has flip settle clear + **Has flip → Design/Verify unpaid** (invalidate overall `03a` to **`pending`**, **or** Prefer `design-verify-phase` / API∥DB → `design-review`).
3. When Grill closed: Next = `design-verify-phase` (not separate Analyze/Grill/Design).

---
