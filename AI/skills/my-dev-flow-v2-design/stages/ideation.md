## ideation — Ideation (PO) — Medium

**Skills:** `{myplan}/SKILL.md` (discovery + specify only).

**subagent_type:** `generalPurpose`  
**model:** resolved Medium

**Done when:** `01-idea.md` filled; **Has UI** set in `01-idea.md` and parent copies to `00-run.md`; ready for Gate A.

**Task prompt:**

```
You are the Product Owner for my-dev-flow-v2-design Ideation. Fresh context only — do not assume prior chat.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for ideation>

Read and follow: {myplan}/SKILL.md (discovery + specify only — no plan/code).

User idea / request:
<paste user request>

Mode hint from parent (if any): full | simple

Quick-scan the repo first (README, AGENTS.md, related features). Summarize the project shape in 1–3 short sentences.

Investigate the question against primary sources (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.

Then draft .my-docs/workflow/<slug>/01-idea.md using the template from {my-dev-flow-v2}/artifacts/INDEX.md.

Must include:
- **Problem map (diagnose before framing):**
  - Mode **full:** Step 1 three WHAT branches (happening / missing-wrong / consequences, 3–5 each); Step 2 surface vs root + **Core problem** one sentence; visual text mind map with ★ top priority
  - Mode **simple:** stub OK — Core problem one line + `N/A — root cause clear`, or 3–5 bullets total
- Problem (one-line restatement of Core problem), User / audience, Outcome (align with ★), Metric
- **Has UI:** yes | no (required — parent will copy into 00-run.md before Gate A)
- Copy/token-only? UI notes for Design?
- 80/20 UI (if UI): main user goals; vital few; Important info/action #1 and #2 always visible with secondary in menus/expand/modal; top journey; sensible defaults; biggest usability risks first (or `N/A — no UI`)
- Non-goals, Assumptions to attack, Success criteria, Open questions
- **Sources (primary):** paths / URLs / APIs that own each material claim (not blog summaries of those sources)

Diagnose before Outcome — do not jump to solution framing until Core problem is written.
Ask blocking questions only if the idea cannot be reviewed without an answer. Prefer writing Open questions into 01-idea.md and continuing to Gate A.

Do not write code. Do not write the technical design yet.
Do not invent Solution branches here — those belong in Analyze.
Do not treat secondary write-ups (blogs, Stack Overflow, AI summaries of docs) as the authority when a primary source exists.
Return: short summary + path to 01-idea.md + Has UI value + any blocking questions (or none).
```

**After:** Parent sets **Has UI** in `00-run.md` from `01-idea.md`. If true blockers, pause; else continue to **gate-a**.

---
