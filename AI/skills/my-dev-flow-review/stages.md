# my-dev-flow-review stages

Stage-scoped handoff: `~/.cursor/skills/my-dev-flow/handoffs.md` → stage id (`adversarial`, `quality`, `spm-api`, `spm-db`, `spm-security`, `spm-perf`, `spm-memory`, `merge-findings`, `fix-review`).

---

## 1. Adversarial test review (Verifier) — Medium

**Generation ≠ verification:** different pass from Build.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Adversarial test review`

**Done when:** zero Critical/Major/Enhancement on test quality.

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Adversarial Test Review. You did NOT write this code. Do not rewrite features unless needed to describe a finding.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Review tests and how they map to 04-tasks.md and the behavior in the draft.

Check:
- Tests that only assert mocks are mocks (“mock theater”)
- Missing edge cases and negative cases
- Non-deterministic or flaky patterns
- Missing failure-mode coverage for critical paths
- Prefer readable, deterministic tests tied to real failure modes

Append findings to 05-review-log.md under “Adversarial test review” with severity Critical / Major / Enhancement (and Nit/FYI if useful).

If clean: say “Adversarial test review: clean.”
If not: list findings with file:line when possible. Do not fix them yourself.
Return: finding table or clean status.
```

**If findings:** run **Fix** (lens = adversarial-tests) → re-run this lens until clean → then Quality.

---

## 2. Quality review (Verifier) — Medium

**Skills:** `~/.cursor/skills/code-review-and-quality/SKILL.md`  
Bugbot only if the user asked.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Quality review`

**Done when:** zero Critical/Major/Enhancement for Quality.

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Quality Review. Generation ≠ verification — you did not write this draft.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read ~/.cursor/skills/code-review-and-quality/SKILL.md and follow it.
Review uncommitted / branch changes against 01-idea, 03-design, and 04-tasks.
When Has UI: also compare draft UI to Design UI specs in 03-design / 04-tasks + Gate A #1/#2 — fail **Major** if shipped look drifts on **size**, **positions**, **texts**, or chrome.
When 03-design **System design** or **Design patterns used** is not N/A: check draft code honors their Best practices / anti-patterns and does not invent a conflicting shape (Architecture axis). Flag design↔code gaps as Major when clear.

Do NOT deep-review API contracts here when Has API / Lens plan includes api — that is the dedicated API lens. You may note “defer to API lens” for contract-shaped issues.
Do NOT deep-review schema/migrations/persistence queries here when Has DB / Lens plan includes db — that is the dedicated DB lens. You may note “defer to DB lens” for data-model issues.

Label every finding Critical / Major / Enhancement (Nit/FYI ok).
Append to 05-review-log.md under “Quality”.
Do not fix. Return finding table or “Quality review: clean.”
```

**If findings:** run **Fix** (lens = quality) → re-run Quality until clean → then Conditional lenses (per Lens plan).

---

## 3. Conditional lenses — API / DB / Security / Performance / Memory (Medium|Fast)

**When:** After Quality is clean **and** `00-run.md` **Lens plan** is not `none`. Parent launches **only** lenses listed in Lens plan (parallel when 2+). If plan is `none`, skip section 3–4 and go to test.

If **Has API = yes** and plan omits **api**, parent adds **api** before launching.
If **Has DB = yes** and plan omits **db**, parent adds **db** before launching.

Wait for launched lenses. Merge findings only if **2+** lenses; if **1** lens, parent copies into Merged SPM (no Merge Task).

Each lens writes **only** its own file (do not edit `05-review-log.md` here — avoids parallel write races):

| Lens | Output file |
|------|-------------|
| API | `.my-docs/workflow/<slug>/05-lens-api.md` |
| DB | `.my-docs/workflow/<slug>/05-lens-db.md` |
| Security | `.my-docs/workflow/<slug>/05-lens-security.md` |
| Performance | `.my-docs/workflow/<slug>/05-lens-performance.md` |
| Memory | `.my-docs/workflow/<slug>/05-lens-memory.md` |

Overwrite the lens file each round. Use the lens template in `~/.cursor/skills/my-dev-flow/artifacts.md` → “05-lens-*.md”.

### 3a. API (required when Has API)

**Skills:** `~/.cursor/skills/api-and-interface-design/SKILL.md` (+ `reference.md` when useful)

**When:** Lens plan includes **api** (always when Has API = yes).

**Task description:** `API contract lens`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review API Contract Review. Fresh context only. You run in parallel with other SPM lenses when present — write ONLY 05-lens-api.md; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for stage id spm-api from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read ~/.cursor/skills/api-and-interface-design/SKILL.md (and reference.md if needed).
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
Fill the API checklist table. Set Result: clean | has findings.
Return: Result + path to 05-lens-api.md.
```

### 3a2. DB (required when Has DB)

**Skills:** `~/.cursor/skills/database-and-data-model/SKILL.md`

**When:** Lens plan includes **db** (always when Has DB = yes).

**Task description:** `Database review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Database Review. Fresh context only. You run in parallel with other SPM lenses when present — write ONLY 05-lens-db.md; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for stage id spm-db from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read ~/.cursor/skills/database-and-data-model/SKILL.md.
Also read 03-design.md Database contracts + example queries, 04-tasks.md, and the draft schema / migration / query / server persistence files.
Also read project AGENTS.md Database / Drizzle section when present.

Review that persistence follows best practices and matches the design contracts:

- Typed columns / nullability; indexes and uniques match real queries and idempotency
- Write owner + read owners respected in code paths
- Migrations additive or expand/contract; journal/meta consistent; backfill safe if present
- Safe SQL binds — prefer query builder / inArray / sql.join; no bad JS-array → ::type[]
- No bigint / SUM → ::int on money or large aggregates
- Lists bounded; no obvious N+1
- Tenant/ownership filters on mutating and sensitive reads
- Multi-step writes transactional or compensating
- Contract in 03-design matches schema + migrations + queries (and vice versa)

Write .my-docs/workflow/<slug>/05-lens-db.md using the lens template (Lens: db).
Fill the DB checklist table. Set Result: clean | has findings.
Return: Result + path to 05-lens-db.md.
```

### 3b. Security

**Skills:** `~/.cursor/skills/security-and-hardening/SKILL.md`  
`~/.cursor/skills-cursor/review-security/SKILL.md` when appropriate.

**Task description:** `Security review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Security Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read ~/.cursor/skills/security-and-hardening/SKILL.md (including OWASP Top 10 section).
Follow ~/.cursor/skills-cursor/review-security/SKILL.md to run the security-review subagent on branch changes when you can; otherwise review authz, injection, secrets, untrusted input yourself.

Required: check the change against OWASP Top 10 (A01–A10). For each category mark pass / fail / N/A with a short note. Failures become Critical or Major findings. Primary source: https://owasp.org/Top10/

Also compare against 03-design.md Security / OWASP section when present — flag design↔code gaps.

Write .my-docs/workflow/<slug>/05-lens-security.md using the lens template (Lens: security).
Include findings table + OWASP mini-table. Set Result: clean | has findings.
Return: Result + path to 05-lens-security.md.
```

### 3c. Performance

**Skills:** `~/.cursor/skills/performance-optimization/SKILL.md`  
+ `vercel-react-best-practices` if React/Next.

**Task description:** `Performance review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Performance Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read ~/.cursor/skills/performance-optimization/SKILL.md.
If React/Next UI changed, also read ~/.cursor/skills/vercel-react-best-practices/SKILL.md.

Look for N+1, unbounded fetches, missing pagination, waterfalls, hot-path waste, bundle bloat.
Write .my-docs/workflow/<slug>/05-lens-performance.md using the lens template (Lens: performance).
Set Result: clean | has findings.
Return: Result + path to 05-lens-performance.md.
```

### 3d. Memory

**Task description:** `Memory review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Memory Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Checklist:
- Listener / subscription / timer leaks; missing cleanup
- Unbounded caches or in-memory lists
- Large retained closures or growing module-level state
- Holding whole result sets when streaming/pagination is needed
- Bad casts on money/sum columns (e.g. bigint SUM forced to int4)
- Unnecessary retained references in long-lived objects

Write .my-docs/workflow/<slug>/05-lens-memory.md using the lens template (Lens: memory).
Set Result: clean | has findings.
Return: Result + path to 05-lens-memory.md.
```

**After launched lenses return:** Parent launches **Merge findings** when **2+** lenses (do not Fix yet).

---

## 4. Merge findings (Arbiter) — Medium

**When:** After all **launched** lens files for this round exist (not always all four).

**Role:** merge, dedupe, resolve conflicts, pick winners. Does **not** fix code. Does **not** re-review the codebase from scratch.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Merge review findings`

**Done when:** `05-review-log.md` → **Merged SPM** section updated with Result **clean** | **needs fix** and a concrete Fix ask (or empty if clean).

**Task prompt:**

```
You are the Findings Arbiter for my-dev-flow-review. Fresh context only. You did NOT run the lens reviews and you do NOT fix code. Your job: merge the launched lens files into one ranked Fix ask and resolve conflicts.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Read only the lens files that exist for this round (any of):
- 05-lens-api.md
- 05-lens-db.md
- 05-lens-security.md
- 05-lens-performance.md
- 05-lens-memory.md
Also read 05-review-log.md (prior Merged SPM / Fix notes if any).
Optionally skim 03-design.md if a conflict needs product intent.

Rules for merging:
1. Deduplicate near-duplicate findings across lenses (keep the clearest wording; note source lenses).
2. Conflict priority (pick winners):
   - Security Critical / Major beats Performance or Memory asks that weaken security
   - API contract / DB correctness / data-integrity beats micro-optimizations
   - When Performance vs Memory clash: prefer measured or clearly bounded wins; drop speculative cache growth that risks leaks; document tradeoff
3. Drop or demote to Nit/FYI: vague nits, speculative micro-opts without evidence, duplicates
4. Rank remaining Fix ask: Critical → Major → Enhancement
5. Result = **clean** only if no open Critical, Major, or Enhancement remain after merge
6. Result = **needs fix** if any Critical/Major/Enhancement remain — write numbered Fix ask (what to change, which files, which lens ids)

Write/update 05-review-log.md section “Merged SPM” using the template shape:
- Round number
- Result: clean | needs fix
- Winners table (Severity, Sources, Finding, Decision) — Sources may include api/db/security/perf/memory
- Conflicts resolved (what lost and why)
- Fix ask (numbered) — empty if clean
- Round notes

Do not edit the 05-lens-*.md files. Do not write production code.
Return: Result + count of fix items + path to 05-review-log.md.
```

**After:**

- If **clean** → lens loop done (workflow review phase complete, unless parent needs Adversarial recheck from a prior Fix — usually none).
- If **needs fix** → run **Fix** with merged Fix ask → then:
  - If Fix changed tests/behavior → re-run Adversarial once (Quality if structure changed)
  - Re-run SPM-plan lenses (parallel) → Merge findings again (max 3 rounds, then pause)

---

## 5. Fix (Senior) — Fast — TDD

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Fix review findings`

**When:**

- After Adversarial or Quality findings (sequential lenses), OR
- After Merge findings Result **needs fix** (use merged Fix ask only)

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-review Fix. You fix listed findings only. You do not self-approve — verifiers will re-check.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

Mode: <adversarial-tests | quality | merged-spm>
Findings / Fix ask to apply:
<paste findings or merged Fix ask>

Rules:
- TDD: for behavior bugs, add/adjust a failing test first (Red), then fix (Green), refactor, verify.
- Pure docs/comments: note “TDD skipped — no behavior” in 05-review-log.md.
- Use existing test stack. Do not expand scope.
- Update 05-review-log.md Fix notes with what you fixed.
- For merged-spm: only apply the Merged SPM Fix ask winners — do not revive deferred losers unless needed for a winner.

Return: list of fixes + tests run + whether tests/behavior changed (yes/no).
```

**After Fix:**

- Mode adversarial-tests → re-run Adversarial until clean.
- Mode quality → re-run Quality until clean.
- Mode merged-spm → if tests/behavior changed, Adversarial once (Quality if structure changed); then re-run SPM-plan lenses → Merge findings (if 2+).

---

## Parent loop hint (my-dev-flow)

```
Adversarial ⇄ Fix until clean
→ Quality ⇄ Fix until clean
→ Loop (max 3):
    [API when Has API] ‖ [DB when Has DB] ‖ Security ‖ Performance ‖ Memory  (only lenses in Lens plan)
    → Merge findings (if 2+)
    → if clean → done
    → Fix (merged) → optional Adversarial/Quality recheck → repeat
→ my-dev-flow-test full|lite
```
