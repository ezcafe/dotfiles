## code-review-phase

**Stage id:** `code-review-phase`

**When:** Review profile **lite** (any Mode, including Mode full). **Required** (not optional). Covers Adversarial + Quality in one Task. Review profile **full** uses `adversarial` then `quality` instead. Never launch separate Adv+Quality under lite.

**subagent_type:** `generalPurpose`  
**model:** Fast preferred (Fast-on-simple)  
**Task description:** `Lite combined review`

**Done when:** `05-review-log.md` Adversarial + Quality sections clean (zero Critical/Major), or Fix ask listed.

**Task prompt:**

```
You are the Senior Verifier for my-dev-flow-review **Lite combined review** (code-review-phase). Fresh context only. Generation ≠ verification — you did not write this draft. Do not fix code in this Task.

<Stage-scoped handoff for stage id code-review-phase from {my-dev-flow}/handoffs.md>

Read 00-run.md (Lens plan — default none), 01-idea, 03-design, 04-tasks, draft code/tests.
Read {code-review-and-quality}/SKILL.md for the Quality pass.

### Pass A — Adversarial tests
Check mock theater, missing edges/negatives, flaky patterns, missing failure-mode coverage vs 04-tasks. Append “Adversarial test review” to 05-review-log.md.

### Pass B — Quality
Multi-axis quality vs idea/design/tasks. Has UI → fail Major on Design UI / Gate A #1/#2 drift. Defer deep API/DB contract issues to lenses when Lens plan includes api/db. Append “Quality” section.

### Optional — single non-api/db lens
If Lens plan has exactly **one** lens and it is **not** api/db, you may run that checklist in this same Task and write the matching 05-lens-*.md; else leave lenses to parent.
**api/db:** When Lens plan includes api/db and Notes are **not** `tiny-contract-tweak`, do **not** deep-fold contracts here — parent launches isolated `lens-api` / `lens-db`. Tiny-tweak: fold contract checks into Quality (no forced api/db lens).

Clean only if zero Critical/Major in Adv + Quality ({my-dev-flow}/severity.md). Else Fix ask ≤15 bullets Critical/Major only.
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-review-log.md.
```

**If findings:** Fix → re-run this stage until clean → then lenses per Lens plan (api/db isolated when listed and not tiny-tweak; 2+ → parallel + Merge).

---
