---
name: myplan
description: Asks about ideas and requirements, follows spec-driven development (Addy Osmani's good-spec framework), and creates an implementation plan before coding. Use when the user wants to plan a feature, build something new, or says "let's plan", "help me implement", or "create a plan for".
---

# MyPlan — Spec-Driven Planning for Implementation

This skill guides a discovery → spec → plan → implement workflow. **Plan first, code second.** Reference: Work/Skills/AI/Prompt technique.md (Addy Osmani, Jan 2026). Read it when in the qan workspace.

---

## Phase 1: Discovery (Scan + Ask First)

Before asking questions, do a **quick scan of the current project** to ground yourself:

- Skim any obvious entry points (e.g. `main.*`, `index.*`, `app.*`) and the nearest `README` / `SPEC` / `PLAN` files.
- Look for existing docs, configs, or patterns that relate to the user's request (e.g. similar features, existing APIs, UI components).
- Summarize what you learned in **1–3 short sentences** so the user sees you understand the current shape of the project.

After the quick scan, before drafting any spec or plan, ask the user to clarify:

| Area | Questions to Ask |
|------|------------------|
| **Idea / Goal** | What are you trying to build or improve? Who is it for? |
| **Success** | What does "done" look like? What are the must-have outcomes? |
| **Constraints** | Tech stack? Deadlines? Performance or security requirements? |
| **Existing** | Any current code, docs, or design we should align with? |
| **Scope** | In scope vs. out of scope for this iteration? |
| **Concerns** | Any worries, risks, or unknowns? What could go wrong? What needs clarification before we proceed? |

Do **not** skip to planning if answers are vague. Ask follow-up questions until you have a clear high-level picture. **Always ask for concerns** — surface risks, assumptions, and ambiguities so they can be resolved early.

---

## Phase 2: Specify

Draft a high-level spec. Focus on **what and why**, not how.

Include:

- **Objective** — One clear goal statement
- **Users / Audience** — Who benefits
- **Success criteria** — Measurable outcomes (e.g. "User can add, edit, complete tasks; data persists")
- **Test plan** — What must be testable? Unit vs integration vs E2E? Critical paths? Non-functional checks (performance, security, a11y)?
- **Out of scope** — Explicitly excluded for now

Present the spec to the user for approval. **Before proceeding, ask: "Any concerns or risks we should address?"** Do not proceed until they confirm or correct it.

---

## Phase 3: Plan

Turn the approved spec into a technical plan.

Add:

- **Tech stack** — Exact versions (e.g. "React 18+, TypeScript, Vite")
- **Project structure** — Where source, tests, docs live
- **Commands** — Build, test, lint (full commands with flags)
- **Test strategy** — Tools (e.g. Jest, RTL, Playwright), test types per area, coverage goals. Include concrete test cases or specs where feasible.
- **Boundaries (three-tier)** — Always do / Ask first / Never do

Example boundaries:

- ✅ **Always:** Run tests before commits, follow naming conventions
- ⚠️ **Ask first:** DB schema changes, new dependencies, CI changes
- 🚫 **Never:** Commit secrets, edit `node_modules/`, remove failing tests

Have the user approve the plan before breaking into tasks. **Ask: "Any concerns about this plan? Anything we should revisit before we break into tasks?"**

---

## Phase 4: Tasks

Break the plan into small, reviewable chunks. Each task should be implementable and testable in isolation. **Include explicit test tasks** — e.g. "Write unit tests for X", "Add integration test for Y", or "TDD: spec → tests → impl" per task.

| Task | Description | Acceptance | Tests |
|------|-------------|------------|-------|
| 1 | ... | ... | Unit tests for ... |
| 2 | ... | ... | Integration / E2E for ... |

Ask the user if they want to implement all tasks or only some. **Ask: "Any concerns about the task breakdown or testing approach?"** Do not start implementation without explicit go-ahead.

---

## Phase 5: Implement

Implement tasks one by one (or in parallel if non-overlapping). Prefer **TDD** where practical: write tests first, then implement. After each task:

- Run tests / lint
- Confirm acceptance criteria
- Ensure test plan coverage for that task (unit, integration, or E2E as specified)
- Update spec if discoveries warrant it

If the user hasn't approved the spec or plan yet, **do not implement** — stay in planning mode and iterate. If implementation surfaces new concerns or risks, **pause and ask the user** before proceeding.

---

## Output Format

Save the approved spec and plan as:

- `SPEC.md` — Spec + Plan (objective, success criteria, test plan, tech stack, structure, commands, boundaries)
- Optional: `PLAN.md` — Task breakdown with acceptance criteria and test tasks

Both should be version-controlled and treated as living docs.

---

## Rules

- **No code until spec + plan approved** — Planning is read-only; implementation starts only after user confirmation
- **Test plan is mandatory** — Every spec and plan must include a test strategy and concrete test tasks; write tests before or alongside implementation
- **Always clarify concerns** — At each phase, ask the user for worries, risks, or ambiguities; do not assume silence means no concerns
- **One focus per prompt** — Don't mix discovery, spec, plan, and code in one long dump
- **Modular context** — If the spec is large, feed only the relevant section for the current task
- **Spec as source of truth** — If requirements change, update the spec first, then re-sync the plan
