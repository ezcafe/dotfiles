## api-contract-review (0a) — API contract review (Verifier) — Medium — when Has API

**When:** Mode **full** and (`00-run.md` **Has API = yes**, or `03-design.md` defines new/changed public API contracts and Has API is unknown — treat as yes), **unless** Notes `tiny-contract-tweak` (`{my-dev-flow}/lenses.md` fold). Mode **simple** uses **design-verify-phase** instead.

**Generation ≠ verification:** you did not write these contracts. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium (Fast if Medium unavailable)  
**Task description:** `API contract review`

**Done when:** `03a-api-contract-review.md` has Result **clean** or **needs update**. Overall round stays **needs update** if this file is not clean. Do **not** require this file when Has API = no or Notes `tiny-contract-tweak`.

**Task prompt:**

```
You are a Senior API designer verifier for my-dev-flow-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find contract gaps; do not rewrite 01–04 yourself.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py api-contract-review>

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

Return FIRST LINE exactly: Result: clean | needs update | skipped
Then short summary + path to 03a-api-contract-review.md ({my-dev-flow}/results.md).
```

**If needs update:** parent may run design Update for API Fix ask items, then re-run this stage before or with general design review (re-run isolated only when present and not tiny-tweak).

**If Has API = no:** skip this stage — Notes skip only; **never** invent an empty `03a-api-contract-review.md`.

---
