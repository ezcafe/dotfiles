## Build (Senior) — Fast — TDD

**Stage id:** `build`

**When:** After Gate B. Skip until Gate B is checked. **Gate B approved** means the durable `00-run.md` field is settled (`yes` / named pick when HITL Gate B is **blocking**) **plus** provenance `gate-b-approved` with a quality user quote — not “design docs look approved.” Async-notify uses **Build armed** + turn-boundary gap (not Gate B approved). See `{my-dev-flow}/hitl.md`.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Build with TDD`

**Done when:** **Gate B veto** was `none`; if HITL Gate B was **blocking**, **Gate B approved** was `yes`/named pick **+ provenance**; if Notes had veto window open, **Build armed** + async gap (later HH:MM + `async-gap-pending`) were present; Notes had no `design-backloop`; tasks implemented with TDD; `04a` Fix ask addressed; when Has UI, draft UI matches Design UI specs (+ Gate A #1/#2 when `01a` present); **Verify gate pass**; Smoke section written; Result **verify-pass** (or `blocked — …`).

**Rules:** Follow `{my-dev-flow}/verify-and-fix.md` (veto + Gate B approved + provenance + Build armed / async gap + design-backloop check first, Verify commands, max 3 attempts, Smoke on pass). Async window: `{my-dev-flow}/hitl.md`.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-code Build. Fresh context only. First output is a DRAFT. You must pass the Verify gate and write the Smoke section before the parent advances.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py build>
Read {my-dev-flow}/verify-and-fix.md (Gate B veto / Build armed + Verify gate + Smoke after Build). See {my-dev-flow}/hitl.md for async-notify window.

FIRST: Read 00-run.md **Gate B veto**, **Gate B approved** (durable field — not design-doc approval), Notes provenance, and async gap tokens.
- If veto pending → stop; return first line `Result: blocked — Gate B veto`; do not change code.
- If HITL Gate B is blocking and **Gate B approved** is none/missing **or** provenance `gate-b-approved` is missing/weak → stop; return first line `Result: blocked — Gate B approved`; do not change code.
- If Notes say veto window open AND (**Build armed** missing OR async gap incomplete) → stop; return first line `Result: blocked — Build armed missing`; do not change code.
- If Notes match `design-backloop` → stop; return first line `Result: blocked — design-backloop`; do not change code.
Then read Verify commands (required). Read 03-design.md and 04-tasks.md. Read 04a-tdd-test-review.md if present — implement Fix ask tests (Red) with matching tasks.
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

Return FIRST LINE exactly: Result: verify-pass | verify-fail | blocked — Gate B veto | blocked — Gate B approved | blocked — Build armed missing | blocked — design-backloop
Then: what shipped; commands + pass/fail; Smoke section path; remaining risks; if UI, HTML match (yes/no + intentional delta).
```

**After:** Parent advances **only** on **verify-pass**. Update card Last Verify + attempts; set `**Last verify-pass at:**` to now (ISO-8601) on `00-run.md`. **Skip Smoke Task** when Smoke section is smoke-pass (Build-writes-Smoke). If a prior `05-review-log` Result clean (or lens clean) / `06` Result success already existed before this Build: add Notes `- review-stale` / `- test-stale` (or clear those Results) so derive will not skip re-review/re-test ([verify-and-fix.md](../../my-dev-flow/verify-and-fix.md) Stale). On **verify-fail** after 3 attempts → Decision N. skip-review → Gate C only when legal ([lenses.md](../../my-dev-flow/lenses.md)). If Build cannot stay aligned with `03`/`04` → parent **Design-backloop** (never silently rewrite design).
