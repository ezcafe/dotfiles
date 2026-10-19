## merge-findings

**Stage id:** `merge-findings`

**When:** After all **launched** lens files for this round exist (not always all five). **Only when 2+ lenses ran.**

**Role:** merge, dedupe, resolve conflicts, pick winners. Does **not** fix code. Does **not** re-review the codebase from scratch.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Merge review findings`

**Done when:** `05-review-log.md` → **Merged lenses** section updated with Result **clean** | **needs fix** and a concrete Fix ask (or empty if clean).

**Task prompt:**

```
You are the Findings Arbiter for my-dev-flow-v2-review. Fresh context only. You did NOT run the lens reviews and you do NOT fix code. Your job: merge the launched lens files into one ranked Fix ask and resolve conflicts.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for merge-findings>

Read only the lens files that exist for this round (any of):
- 05-lens-api.md
- 05-lens-db.md
- 05-lens-security.md
- 05-lens-perf.md
- 05-lens-memory.md
Also read 05-review-log.md (prior Merged lenses / Fix notes if any).
Optionally skim 03-design.md if a conflict needs product intent.

Rules for merging:
1. Deduplicate near-duplicate findings across lenses (keep the clearest wording; note source lenses).
2. Conflict priority (pick winners):
   - Security Critical / Major beats Performance or Memory asks that weaken security
   - API contract / DB correctness / data-integrity beats micro-optimizations
   - Quality beats Perf/Memory Enhancements when they conflict on clarity/correctness tradeoffs
   - When Performance vs Memory clash: prefer measured or clearly bounded wins; drop speculative cache growth that risks leaks; document tradeoff
3. Drop or demote to Nit/FYI: vague nits, speculative micro-opts without evidence, duplicates
4. Rank remaining Fix ask: Critical → Major (Enhancements → Deferred; do not put in Fix ask)
5. Result = **clean** only if no open **Critical** or **Major** remain after merge (Enhancements do **not** block clean — copy to Deferred per `{my-dev-flow-v2}/severity.md`)
6. Result = **needs fix** if any Critical/Major remain — write numbered Fix ask (what to change, which files, which lens ids). If Fix needs design/contract change → parent Design-backloop ([design-backloop.md](../../my-dev-flow-v2/design-backloop.md)), not silent design rewrite.

Write/update 05-review-log.md section “Merged lenses” using the template shape:
- Result: clean | needs fix
- Winners table (Severity, Sources, Finding, Decision) — Sources may include api/db/security/perf/memory
- Conflicts resolved (what lost and why)
- Fix ask (numbered) — empty if clean
- Round notes (Merged lenses section only — do **not** invent or bump file-top **Round**; parent increments on re-entry)

Do not edit the 05-lens-*.md files. Do not write production code.
Return FIRST LINE exactly: Result: clean | needs fix
Then count of fix items + path to 05-review-log.md.
(If a lens file still says legacy **has findings**, treat as **needs fix** when Critical/Major remain.)
```

**After:**

- If **clean** → lens loop done (unless parent needs a profile-branched recheck from a prior Fix: **lite** → `code-review-phase`; **full** → Adversarial / Quality). Advance to `test-*` only when Merged is **clean** ([preflight.md](../../my-dev-flow-v2/preflight.md)).
- If **needs fix** → `fix-review` Mode `merged-lenses` → on **verify-pass**, parent Prefer ([derive-next.md](../../my-dev-flow-v2/derive-next.md)): mark planned `05-lens-*` + Merged unpaid → re-run Lens plan lenses → Merge findings again (max 3 rounds, then Decision N). If Fix changed tests/behavior: **lite** Prefer `code-review-phase` once first; **full** Prefer Adversarial once (Quality if structure changed) first.

---
