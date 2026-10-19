## lens-api — API (when Lens plan includes api)

**Stage id:** `lens-api`  
**Skills:** `{api-and-interface-design}/SKILL.md` (+ `reference.md` when useful)  
**When:** Lens plan includes **api** (auto-added when Has API = yes **unless** tiny-tweak — `{my-dev-flow-v2}/lenses.md`).  
**Task description:** `API contract lens`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-v2-review API Contract Review. Fresh context only. You run in parallel with other lenses when present — write ONLY 05-lens-api.md; do not edit 05-review-log.md or other lens files. Do not fix code.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for lens-api>

Read {api-and-interface-design}/SKILL.md (and reference.md if needed).
Also read 03-design.md API/DB contracts and the draft route/handler/validator/schema files.

Review that public APIs follow best practices and match the design contracts:

- Typed input and output; create-input vs full entity
- One stable error shape; correct status codes
- Validate at system edges only (not re-validate trusted internals)
- Lists paginated; filters via query params; PATCH for partial updates where appropriate
- Additive fields; no silent breaking changes
- Naming consistent with the repo
- Mutating endpoints: idempotent or documented unsafe-to-retry
- Contract in 03-design matches what the code exposes (and vice versa)
- Do not leak internals in errors

Write .my-docs/workflow/<slug>/05-lens-api.md using the lens template (Lens: api).
Fill the API checklist table. Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow-v2}/results.md · severity.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-api.md.
```

**After:** Lens plan **2+** (parent parallel): wait sibling lenses → `merge-findings` (do **not** Fix yet — even on needs fix). Plan **1** lens: clean → test; needs fix → `fix-review`. Serial next unpaid `lens-*` only when parent launched serial ([derive-next.md](../../my-dev-flow-v2/derive-next.md) · [lenses-overview.md](lenses-overview.md)).
