## design-update — Update from design review (Architect) — High

**When:** `03a` Result is **needs update**.

**subagent_type:** `generalPurpose`  
**model:** resolved High  
**Task description:** `Update design docs`

**Done when:** Fix-ask items addressed; parent re-runs design-review.

**Task prompt:**

```
You are the Architect for Update from design review. Fresh context only. Repair only what 03a Fix ask lists; keep Gate A idea. Do not re-litigate Gate A 80/20 unless Fix ask requires it.

<Stage-scoped handoff for this stage id from {my-dev-flow}/handoffs.md>

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

**After:** Parent re-runs `my-dev-flow-design-review` (full: isolated API/DB when present and not tiny-tweak, then general; simple: design-verify-phase).

---
