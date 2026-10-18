## skim — Light repo skim (Medium)

**When:** After Gate A **ok**. Always run in full mode (short; constraints only).

**subagent_type:** `explore` or `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Light repo skim`

**Done when:** `02-skim.md` Result **done**.

**Task prompt:**

```
You are doing a light repo skim for my-dev-flow-design. Fresh context only. This is NOT full Analyze — constraints and reuse pointers only.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py skim>

Read 01-idea.md and 01a-idea-ui-review.md (Gate A ok).

Scan the repo for related screens, components, APIs, and hard constraints. Prefer concrete paths.

Write .my-docs/workflow/<slug>/02-skim.md using the template from {my-dev-flow}/artifacts/INDEX.md.

Must include: project shape (1–3 sentences), related UI paths, related APIs/data, hard constraints, risks if ignored, enough for Analyze/Design?

Also propose **Verify commands** for 00-run.md when obvious (cwd, build, unit, e2e — or N/A + reason). See {my-dev-flow}/verify-and-fix.md.

Do not write production code. Do not write full analysis or design.
Set 02-skim.md Result to **done** (or **skipped** only if parent already marked skim skipped).
Return FIRST LINE exactly: Result: done | skipped
Then short summary + path to 02-skim.md + proposed Verify commands.
```

**After:** Parent continues (advances on either token — [results.md](../../my-dev-flow/results.md)):

- Copy proposed Verify commands into `00-run.md` when clear.
- Proceed to Analyze after skim (UI specs come later in Design).

---
