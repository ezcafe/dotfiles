Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md).

# 01-idea.md

```markdown
# Idea: <short title>

## Problem map (diagnose before framing)

**Mode full:** required. Fill Steps 1–2 + mind map before Outcome.  
**Mode simple:** stub OK — one Core problem line + `N/A — root cause clear` under branches, or 3–5 bullets total.

### Step 1 — Deep exploration (3 WHAT branches)

#### What is happening?
Objective symptoms, metrics, or factual observations (3–5):

-

#### What is missing / wrong?
Gaps in resources, clarity, or alignment (3–5):

-

#### What are the consequences?
Downstream impacts if unsolved (3–5):

-

### Step 2 — Real core problem

- **Surface symptoms:** (short — what people notice first)
- **Root cause:** (short — underlying driver from Step 1 intersections)
- **Core problem (one sentence):**

### Mind map (visual text)

Indented or ASCII outline of Steps 1–2. Mark the top priority action with ★ (feeds Outcome + later Analyze solution branches). Example shape:

    Problem
    ├── Happening: …
    ├── Missing: …
    ├── Consequences: …
    ├── Core: …
    └── ★ Top priority: …

## Problem

One-line restatement of **Core problem** (or “what hurts today” if map is stubbed).

## User / audience

Who is this for?

## Outcome

What does “done” look like? (Align with ★ top priority from Problem map.)

## Metric

How do we know it worked? (one clear signal)

## Sources (primary)

Investigate the question against primary sources (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.

| Claim / topic | Primary source (path, URL, or API) | Notes |
|---------------|--------------------------------------|-------|
| | | |

## Has UI

**yes | no** — set clearly here; parent copies into `00-run.md` during Ideation (before Gate A).

## Lean / skip hints

- **Copy/token-only?** yes | no
- **UI notes for Design:** (short — surfaces to touch; no separate UI concept step)

## 80/20 UI (day-to-day)

If this change has a UI (else `N/A — no UI`):

### Main user goals

What users come here to accomplish (list the real jobs):

-

### Vital few (high-impact ~20%)

Features / problems that matter most for most users (from usage, support, interviews, or clear product judgment):

-

### Primary UI — core actions dominant

- **Important info / action #1 (always visible):**
- **Important info / action #2 (always visible):**
- **Core action placement:** clear placement, strong hierarchy, descriptive labels, fewer steps, helpful defaults, immediate feedback
- **Secondary actions:** menus / overflow / less prominent areas / expand / modal / context menu — list what is deferred:

-

### Top user journey to optimize

Map the most common path (example: Open → Search → Select → …):

-

### Sensible defaults

What should be preselected so most users do less work?

-

### Biggest usability risks to fix first

Unclear nav, hard forms, hidden errors, etc. — fix these before polish:

-

## Non-goals

What we will **not** build in this pass:

-

## Assumptions to attack

| Assumption | Must be true? | Fastest way to kill it | If false, what changes? |
|------------|---------------|------------------------|-------------------------|
| | | | |

## What we should not build

-

## Success criteria

- [ ]
- [ ]

## Open questions

-
```

---
