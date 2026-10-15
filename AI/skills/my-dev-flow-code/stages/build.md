## Build (Senior) — Fast — TDD

**Stage id:** `build`

**When:** After Gate B. Skip until Gate B is checked.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Build with TDD`

**Done when:** **Gate B veto** was `none`; if Notes had veto window open, **Build armed** was present; tasks implemented with TDD; `04a` Fix ask addressed; when Has UI, draft UI matches Design UI specs (+ Gate A #1/#2 when `01a` present); **Verify gate pass**; Smoke section written; Result **verify-pass** (or `blocked — …`).

**Rules:** Follow `{my-dev-flow}/verify-and-fix.md` (veto + Build armed check first, Verify commands, max 3 attempts, Smoke on pass). Async window: `{my-dev-flow}/hitl.md`.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-code Build. Fresh context only. First output is a DRAFT. You must pass the Verify gate and write the Smoke section before the parent advances.

<Stage-scoped handoff for stage id build from {my-dev-flow}/handoffs.md>
Read {my-dev-flow}/verify-and-fix.md (Gate B veto / Build armed + Verify gate + Smoke after Build). See {my-dev-flow}/hitl.md for async-notify window.

FIRST: Read 00-run.md **Gate B veto** and Notes.
- If veto pending → stop; return first line `Result: blocked — Gate B veto`; do not change code.
- If Notes say veto window open AND **Build armed** is missing → stop; return first line `Result: blocked — Build armed missing`; do not change code.
Then read Verify commands (required). Read 03-design.md and 04-tasks.md (Gate B approved). Read 04a-tdd-test-review.md if present — implement Fix ask tests (Red) with matching tasks.
When Has UI: follow Design UI locks in 03/04 and existing app chrome; if 01a-idea-ui-review.md is present, honor Gate A #1/#2 visibility.
Follow project AGENTS.md / design guide. For UI: frontend-ui-engineering, clean-minimal-ui, vercel-react-best-practices as needed.
Honor **System design** and **Design patterns used** in 03-design: follow their Best practices / anti-patterns (if not N/A). Do not invent a conflicting architecture or module shape.

Rules:
- TDD per task: Red → Green → Refactor → Verify.
- Cover real + edge cases from 04a.
- Update skeletons if you change UI layout.
- **Build when Has UI:** shipped UI **must match** Design UI specs + reused live chrome on **size**, **positions**, **texts**. Do not invent a conflicting layout.
- **Verify gate:** Use Verify commands from 00-run.md only (do not invent commands). Max 3 attempts. On pass: write 06-test-log.md Smoke section (build/unit rows + Smoke result smoke-pass). On fail after 3: Result verify-fail.
- Do not merge or push. Do not `git commit` unless the user explicitly asked for a commit. Do not claim ready to ship.

Return FIRST LINE exactly: Result: verify-pass | verify-fail | blocked — Gate B veto | blocked — Build armed missing
Then: what shipped; commands + pass/fail; Smoke section path; remaining risks; if UI, HTML match (yes/no + intentional delta).
```

**After:** Parent advances **only** on **verify-pass**. Update card Last Verify + attempts. **Skip Smoke Task** when Smoke section is smoke-pass (Option B). On **verify-fail** after 3 attempts → Decision N. **Legal** skip-review → Gate C only in **Mode simple** when Has API=no **and** Has DB=no; Mode full or Has API/DB = **yes** → must **not** be skip-review — take review path. If Build cannot stay aligned with `03`/`04` → parent **Design-backloop** (never silently rewrite design).
