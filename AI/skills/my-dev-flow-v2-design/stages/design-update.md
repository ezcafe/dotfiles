## design-update — Update from design review (Architect) — High

**When:** `03a` Result is **needs update**, **or** Notes `- design-backloop` after Decision N Option 1 (Amend design) — no prior `03a` Fix ask required for backloop entry.

**subagent_type:** `generalPurpose`  
**model:** resolved High  
**Task description:** `Update design docs`

**Done when:** Fix-ask items addressed (or Decision N amend scope when backloop); Mode **full:** parent Prefer unpaid isolated while unpaid (even if files exist) → else `design-review`; Mode **simple:** parent Prefer `design-verify-phase` only (do **not** Prefer isolated stages).

**Task prompt:**

```
You are the Architect for Update from design review. Fresh context only. Repair only what 03a Fix ask lists (or Decision N / Notes design-backloop amend scope when no 03a Fix ask); keep Gate A idea. Do not re-litigate Gate A 80/20 unless Fix ask / Decision N requires it.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for design-update>

Read 00-run Notes (design-backloop / Decision N if present), 03a (if present), 01-idea, 02-skim, 02-analysis, 02b-grill (if present), 03-design, 04-tasks.

Rules:
- Update only Fix-ask items, or Decision N amend scope when Notes say design-backloop and 03a has no Fix ask.
- Keep Decision options shape, System design (triggers + teach or N/A; no dupe of contracts), diagram, contracts, Design patterns used (teach What/How/Why/Best practices or N/A), UI alignment with Gate A / Design specs when Has UI, OWASP accurate.
- Honor grill Settled decisions unless Fix ask / Decision N re-opens a branch.
- If UI layout drifts from Gate A #1/#2 or Design UI locks, restore alignment.
- Append Round notes on 03a when 03a exists; else log Round on 00-run Notes.
- No production code.

Return: what you updated, which files.
```

**After:** Mode **full:** Prefer unpaid `api-contract-review` / `db-design-review` while **Isolated API/DB unpaid** (Has yes, not tiny; Prefer even if files exist) → else `design-review`. Mode **simple:** Prefer `design-verify-phase` only (do **not** Prefer isolated stages). (`{my-dev-flow-v2}/derive-next-pre.md` · `{my-dev-flow-v2}/design-backloop.md` · `{my-dev-flow-v2}/handoffs.md` design-update After). **Has flip:** drop skip-review → lite\|reclassify → HITL Gate B **blocking** → settle clear (**Gate B approved: none** / **Build armed: none** / veto-window / `async-gap-pending` / `gate-b auto`) → Notes `has-flip — <flags> — <HH:MM>` → invalidate-or-Prefer-re-run when API/DB newly yes (`{my-dev-flow-v2}/lenses.md` Has flip · `{my-dev-flow-v2}/derive-next.md` Settle freshness).

---
