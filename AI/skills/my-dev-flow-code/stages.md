# my-dev-flow-code stages

Stage-scoped handoff: `{my-dev-flow}/handoffs.md` → stage id table.  
Shared Verify / Fix rules: `{my-dev-flow}/verify-and-fix.md` (read once per Build/Fix).

Each Task starts with a **fresh context**. Put all paths and rules in the prompt.

---

## TDD test-case review — Medium

**When:** After design-review clean; **before Gate B**. Skip in Fix-from-tests mode (unless parent asks).

**subagent_type:** `generalPurpose`  
**model:** resolved Medium

**When to run:** only if `04-tasks.md` has planned test cases; else parent skips this stage.

**Done when:** `04a-tdd-test-review.md` written; Result **clean** or Fix ask lists gaps for Build.

**Task prompt:**

```
You are the Test Case Reviewer for my-dev-flow-code. Fresh context only.

<Stage-scoped handoff for this stage id from {my-dev-flow}/handoffs.md>

Read 03-design.md and 04-tasks.md (design-review clean; Gate B comes after this review). Optionally skim existing test files listed in tasks.

Your job: review planned TDD test cases from 04-tasks.md (this stage runs only because planned tests exist) for:

1. **Real scenarios** — happy path, user-visible failures, empty/loading/permission when relevant.
2. **Edge scenarios** — boundaries, invalid input, double-submit / idempotency, races/partial data when implied.

Write 04a-tdd-test-review.md (template).

Rules:
- Do not implement product code.
- Prefer few strong tests over a long weak list.
- Map gaps to task numbers and suggested test names/assertions.
- Result **clean** only if real + important edges are covered; else **needs more tests** + Fix ask.

Return: Result, top gaps, path to 04a-tdd-test-review.md.
```

**After:** Parent: fold Fix ask into `04-tasks.md` when practical → **Gate B**. Do not Build yet when parent is `my-dev-flow`.

---

## Build (Senior) — Fast — TDD

**When:** After Gate B. Skip until Gate B is checked.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast

**Done when:** tasks implemented with TDD; `04a` Fix ask addressed; when Has UI, draft UI matches Design UI specs; **Verify gate pass**; Smoke section written in `06-test-log.md`; Result **verify-pass** (first return line).

**Rules:** Follow `{my-dev-flow}/verify-and-fix.md` (Verify commands from `00-run.md`, max 3 attempts, missing unit/build N/A rules, write Smoke section on pass).

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-code Build. Fresh context only. First output is a DRAFT. You must pass the Verify gate and write the Smoke section before the parent advances.

<Stage-scoped handoff for stage id build from {my-dev-flow}/handoffs.md>
Read {my-dev-flow}/verify-and-fix.md (Verify gate + Smoke after Build).

Read 00-run.md (Verify commands — required). Read 03-design.md and 04-tasks.md (Gate B approved). Read 04a-tdd-test-review.md if present — implement Fix ask tests (Red) with matching tasks.
When Has UI: follow Design UI locks in 03/04 and existing app chrome.
Follow project AGENTS.md / design guide. For UI: frontend-ui-engineering, clean-minimal-ui, vercel-react-best-practices as needed.
Honor **System design** and **Design patterns used** in 03-design: follow their Best practices / anti-patterns (if not N/A). Do not invent a conflicting architecture or module shape.

Rules:
- TDD per task: Red → Green → Refactor → Verify.
- Cover real + edge cases from 04a.
- Update skeletons if you change UI layout.
- **Build when Has UI:** shipped UI **must match** Design UI specs + reused live chrome on **size**, **positions**, **texts**. Do not invent a conflicting layout.
- **Verify gate:** Use Verify commands from 00-run.md only (do not invent commands). Max 3 attempts. On pass: write 06-test-log.md Smoke section (build/unit rows + Smoke result smoke-pass). On fail after 3: Result verify-fail.
- Do not merge or push. Do not `git commit` unless the user explicitly asked for a commit. Do not claim ready to ship.

Return FIRST LINE exactly: Result: verify-pass | verify-fail
Then: what shipped; commands + pass/fail; Smoke section path; remaining risks; if UI, HTML match (yes/no + intentional delta).
```

**After:** Parent advances **only** on **verify-pass**. Update card Last Verify + attempts. **Skip Smoke Task** when Smoke section is smoke-pass (Option B). On **verify-fail** after 3 attempts → Decision N. skip-review → Gate C bar met by verify-pass.

---

## Fix from tests (Senior) — Fast — TDD

**When:** `06-test-log.md` Result is **smoke-fail** or **failure**.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast

**Done when:** fix-ask items addressed with TDD; **Verify gate pass**; Result **verify-pass** (first return line).

**Rules:** `{my-dev-flow}/verify-and-fix.md` — Fix rules + Verify gate (build+unit + cited failing tests); max 3 attempts.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-code Fix from tests. Fresh context only. Repair only what the test log asks. You must pass the Verify gate before the parent re-runs tests.

<Stage-scoped handoff for stage id fix-tests from {my-dev-flow}/handoffs.md>
Read {my-dev-flow}/verify-and-fix.md.

Read 00-run.md (Verify commands). Read 06-test-log.md (Failures + Fix ask). Read 03-design.md and 04-tasks.md.

Rules:
- Fix only listed failures / fix-ask items.
- TDD: Red → Green → Refactor → Verify.
- Update skeletons if you change UI layout.
- Append Round notes on 06-test-log.md.
- **Verify gate:** Use Verify commands from 00-run.md. Also re-run failing tests named in Failures / Fix ask. Max 3 attempts. Do not claim done on verify-fail.
- Do not merge or push. Do not `git commit` unless the user explicitly asked for a commit.

Return FIRST LINE exactly: Result: verify-pass | verify-fail
Then: what you fixed; commands + pass/fail; anything still out of scope.
```

**After:** Parent re-runs the same test mode **only** on **verify-pass**. On **verify-fail** after 3 → Decision N.

---

## Clarity check (parent)

Before TDD review, Build, or Fix:

> Are the instructions, dependencies, and reference files clear enough to proceed?

If no → ask the user; do not launch the Task.  
If Verify commands missing before Build → set them (or ask) first.
