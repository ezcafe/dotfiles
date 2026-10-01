---
name: planning-and-task-breakdown
description: >-
  Breaks an approved spec into ordered, verifiable implementation tasks. Use
  when a spec or clear requirements already exist and work needs sizing,
  sequencing, or parallelization. For discovery and spec writing, use myplan
  first.
---

# Planning and Task Breakdown

Cursor-optimized adaptation of [addyosmani/agent-skills planning-and-task-breakdown](https://github.com/addyosmani/agent-skills/tree/main/skills/planning-and-task-breakdown).

## Hand off to myplan when needed

| Situation | Skill |
|-----------|--------|
| Idea vague; need discovery + spec | **[myplan](../myplan/SKILL.md)** first |
| Spec (or clear requirements) already approved | **This skill** — tasks + checkpoints |

Do not re-run full discovery here if `myplan` already produced an approved spec.

## Project first

Follow `AGENTS.md` for feature layout (e.g. workspace apps, API thin routes). Prefer the project’s task tracker if `AGENTS.md` / user names one (GitHub/Linear/etc.); otherwise use markdown under `tasks/`.

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Plan in read-only mode until the task list is approved. Each task has acceptance criteria + verification. Prefer vertical slices. |
| **Ask first** | Overwrite `tasks/plan.md` / `tasks/todo.md` (or tracker items) that still have unchecked work for **different** work. |
| **Never** | Start coding during planning. Write XL tasks (“implement the feature”). Delete another session’s open plan without confirmation. |

## Process

### 1. Read-only intake

- Read the spec and relevant code
- Map dependencies and risks
- Note unknowns — ask the user if they block sequencing

**Output now:** plan doc + task list — not implementation.

### 2. Dependency graph → order

Foundations first (schema → types → API → client → UI), but prefer **vertical slices** that deliver a thin working path over building all DB then all API then all UI.

### 3. Write tasks (S/M sized)

Each task:

```markdown
## Task N: Short title

**Description:** One paragraph.

**Acceptance criteria:**
- [ ] Testable condition
- [ ] Testable condition

**Verification:**
- [ ] Focused tests: <project command>
- [ ] Build/typecheck if relevant
- [ ] Manual: <what to click/see>

**Dependencies:** Task #s or None
**Files likely touched:** `path` …
**Scope:** S (1–2 files) | M (3–5) — split if larger
```

Break further if: > one focused session; acceptance needs >3 bullets; title contains “and”; touches unrelated subsystems.

### 4. Checkpoints

After every 2–3 tasks:

- [ ] Tests pass / build clean
- [ ] Slice works end-to-end where applicable
- [ ] Human review before continuing if risk is high

Put high-risk work early (fail fast).

### 5. Output files

- **Plan:** `tasks/plan.md` — overview, architecture decisions, risks, open questions, ordered task index
- **Tasks:** `tasks/todo.md` checklist **or** one tracker item per task if the project uses an external tracker (note that in the plan)

Create `tasks/` if missing. If existing files have unchecked items for other work → **stop and ask**.

## Parallelization

| Safe | Sequential | Needs contract first |
|------|------------|----------------------|
| Independent slices, docs, tests for done code | Migrations, shared state | Features sharing an API — define contract, then parallelize |

## Checklist before coding

- [ ] Spec approved (or requirements explicit)
- [ ] Every task has acceptance + verification
- [ ] Dependencies ordered
- [ ] No XL tasks left
- [ ] Checkpoints listed
- [ ] No conflicting unfinished plan overwritten
- [ ] User approved the task list

## Related

- Discovery/spec: [myplan](../myplan/SKILL.md)
- Record expensive decisions: [documentation-and-adrs](../documentation-and-adrs/SKILL.md)
- After implementation: [code-review-and-quality](../code-review-and-quality/SKILL.md)
