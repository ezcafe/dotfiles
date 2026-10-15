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
You are the Findings Arbiter for my-dev-flow-review. Fresh context only. You did NOT run the lens reviews and you do NOT fix code. Your job: merge the launched lens files into one ranked Fix ask and resolve conflicts.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py merge-findings>

Read only the lens files that exist for this round (any of):
- 05-lens-api.md
- 05-lens-db.md
- 05-lens-security.md
- 05-lens-performance.md
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
5. Result = **clean** only if no open **Critical** or **Major** remain after merge (Enhancements do **not** block clean — copy to Deferred per `{my-dev-flow}/severity.md`)
6. Result = **needs fix** if any Critical/Major remain — write numbered Fix ask (what to change, which files, which lens ids). If Fix needs design/contract change → parent Design-backloop (stages.md), not silent design rewrite.

Write/update 05-review-log.md section “Merged lenses” using the template shape:
- Round number
- Result: clean | needs fix
- Winners table (Severity, Sources, Finding, Decision) — Sources may include api/db/security/perf/memory
- Conflicts resolved (what lost and why)
- Fix ask (numbered) — empty if clean
- Round notes

Do not edit the 05-lens-*.md files. Do not write production code.
Return FIRST LINE exactly: Result: clean | needs fix
Then count of fix items + path to 05-review-log.md.
(If a lens file still says legacy **has findings**, treat as **needs fix** when Critical/Major remain.)
```

**After:**

- If **clean** → lens loop done (unless parent needs Adversarial recheck from a prior Fix).
- If **needs fix** → run **Fix** with merged Fix ask → then:
  - If Fix changed tests/behavior → re-run Adversarial once (Quality if structure changed)
  - Re-run Lens plan lenses (parallel) → Merge findings again (max 3 rounds, then Decision N)

---
