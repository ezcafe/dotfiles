## Build (Senior) — Fast — TDD

**Stage id:** `build`

**When:** After Gate B. Skip until Gate B is checked. **Gate B approved** means the durable `00-run.md` field is settled (`yes` / named pick when HITL Gate B is **blocking**) **plus** provenance `gate-b-approved` with a quality user quote — not “design docs look approved.” Async-notify uses **Build armed** + turn-boundary gap (not Gate B approved). See `{my-dev-flow-v2}/gate-b.md` · provenance `{my-dev-flow-v2}/hitl.md`.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Build with TDD`

**Done when:** **Gate B veto** was `none`; if HITL Gate B was **blocking**, **Gate B approved** was `yes`/named pick **+ provenance**; if Notes had veto window open, **Build armed** + async gap (later HH:MM + `async-gap-pending`) were present; Notes had no `design-backloop`; tasks implemented with TDD; `04a` Fix ask addressed; when Has UI, draft UI matches Design UI specs (+ Gate A #1/#2 when `01a` present); **Verify gate pass**; Smoke section written with **Test path last run:** `smoke`; Result **verify-pass** (or `blocked — …`).

**Rules:** Follow `{my-dev-flow-v2}/verify.md` (veto + Gate B approved + provenance + Build armed / async gap + design-backloop check first, Verify commands, max 3 attempts, Smoke on pass). Async window: `{my-dev-flow-v2}/gate-b.md`.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-v2-code Build. Fresh context only. First output is a DRAFT. You must pass the Verify gate and write the Smoke section before the parent advances.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for build>
Read {my-dev-flow-v2}/verify.md (Gate B veto / Build armed + Verify gate + Smoke after Build). See {my-dev-flow-v2}/gate-b.md for async-notify window.

FIRST: Read 00-run.md **Gate B veto**, **Gate B approved** (durable field — not design-doc approval), Notes provenance, and async gap tokens.
- If veto pending → stop; return first line `Result: blocked — Gate B veto`; do not change code.
- If HITL Gate B is blocking and **Gate B approved** is none/missing **or** provenance `gate-b-approved` is missing/weak → stop; return first line `Result: blocked — Gate B approved`; do not change code.
- If Notes say veto window open AND **Build armed** ≠ `yes` (including `none`) → stop; return first line `Result: blocked — Build armed not yes`; do not change code. Do not write **Build armed**.
- If Notes veto window + **Build armed: yes** but async gap incomplete → stop; return first line `Result: blocked — async gap incomplete`; do not change code.
- If Notes match `design-backloop` → stop; return first line `Result: blocked — design-backloop`; do not change code.
Then read Verify commands (required). Read 03-design.md and 04-tasks.md. Read 04a-tdd-test-review.md if present — implement Fix ask tests (Red) with matching tasks.
When Has UI: follow Design UI locks in 03/04 and existing app chrome; if 01a-gate-a.md is present (or LEGACY `01a-idea-ui-review.md` on resume), honor Gate A #1/#2 visibility.
Follow project AGENTS.md / design guide. For UI: frontend-ui-engineering, clean-minimal-ui, vercel-react-best-practices as needed.
Honor **System design** and **Design patterns used** in 03-design: follow their Best practices / anti-patterns (if not N/A). Do not invent a conflicting architecture or module shape.

Rules:
- TDD per task: Red → Green → Refactor → Verify.
- Cover real + edge cases from 04a.
- Update skeletons if you change UI layout.
- **Build when Has UI:** shipped UI **must match** Design UI specs + reused live chrome on **size**, **positions**, **texts**. Do not invent a conflicting layout.
- **Verify gate:** Use Verify commands from 00-run.md only (do not invent commands). Max 3 attempts. On pass: write 06-test-log.md Smoke section (build/unit rows + Smoke result smoke-pass) **and** **Test path last run:** `smoke`. On fail after 3: Result verify-fail.
- Do not merge or push. Do not `git commit` unless the user explicitly asked for a commit. Do not claim ready to ship.

Return FIRST LINE exactly: Result: verify-pass | verify-fail | blocked — Gate B veto | blocked — Gate B approved | blocked — Build armed not yes | blocked — async gap incomplete | blocked — design-backloop
Then: what shipped; commands + pass/fail; Smoke section path; remaining risks; if UI, HTML match (yes/no + intentional delta).
```

**After:** Parent advances **only** on **verify-pass**. Checklist:

1. Set **Build armed: none**; clear veto-window / `async-gap-pending` Notes ([gate-b.md](../../my-dev-flow-v2/gate-b.md) step 5) — Task must not write **Build armed**.
2. Update Last Verify + attempts; set `**Last verify-pass at:**` (ISO-8601) on `00-run.md`.
3. Post-Build Next per [stages.md](../../my-dev-flow-v2/stages.md) Mode × Review profile · [verify.md](../../my-dev-flow-v2/verify.md) (E1 Independent Smoke · Skip-review ordered recovery · Build-writes-Smoke skip rules).
4. Prior review/test looked paid → Notes `review-stale` / `test-stale` ([verify.md](../../my-dev-flow-v2/verify.md) Stale).
5. verify-fail ×3 → Decision N; design mismatch → [design-backloop.md](../../my-dev-flow-v2/design-backloop.md). Parent-only consent / waiver / provenance.
