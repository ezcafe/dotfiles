---
name: my-dev-flow
description: >-
  Orchestrates the AI-assisted delivery pipeline (design → review → build →
  test → merge). Classifies simple vs full. Gate C always blocking; Mode full
  Gate B blocking; Mode simple Gate B soft (prefer auto; async-notify
  when user asks for a veto window); Grill soft by default. Use when the
  user says run my-dev-flow, start my-dev-flow, run my-plan-flow /
  my-workflow (legacy), simple mode, ideate → build → merge, grill /
  stress-test this plan, or wants the end-to-end delivery pipeline.
---

# my-dev-flow

**TL;DR:** (1) Classify Mode simple vs full. (2) Seed `.my-docs/workflow/<slug>/` from artifacts. (3) Run **Full/Simple pipeline order** in [stages.md](stages.md). (4) Gate C always **blocking**. Mode **full** Gate B **blocking**. Mode **simple** Gate B soft (prefer **auto**; **async-notify** when user asks for a veto window). Grill soft by default. Soft HITL → Grill + Mode simple Gate B only — [hitl.md](hitl.md).

End-to-end **orchestrator only**. Stage prompts live in subflows.  
**Runtime order (SoT):** [stages.md](stages.md) Happy path.  
**Companions:** [hitl.md](hitl.md) · [models.md](models.md) · [lenses.md](lenses.md) · [invariants.md](invariants.md) · [failure-playbook.md](failure-playbook.md) · [grill.md](grill.md) · [verify-and-fix.md](verify-and-fix.md) · [parent-next.md](parent-next.md) · [size-caps.md](size-caps.md) · [results.md](results.md).

Practices: [AI-assisted engineering](https://newsletter.eng-leadership.com/p/how-to-do-ai-assisted-engineering) —
design-heavy, never ship first draft, generation ≠ verification.

## Start (Step 0)

Follow **[stages.md](stages.md) Step 0** (classify, seed `00-run.md`, models, lint, chat one line). Do not restate Step 0 bullets here.

**Skills sync:** Step 0 hard stop when `AI/skills/my-dev-flow` exists — `./AI/skills/sync-to-cursor.sh --check` (or sync) before classify; after SoT edits, sync then re-check ([skills-path.md](skills-path.md)).

## When to run

- **Default:** `run my-dev-flow` / `start my-dev-flow` / `ideate → build → merge` → classify Mode ([stages.md](stages.md)), then pipeline.
- **Solo subflow** (not full pipeline): [solo-entry.md](solo-entry.md).
- **Legacy alias:** `run my-plan-flow` / `my-workflow` → same as `my-dev-flow` (not Build).
- **Override:** `simple` / `full` → that **Mode**; `skip-review` → Review profile **skip-review** (implies Mode **simple** unless Decision N). Do not re-classify (still drop skip-review if Has API/DB becomes yes — [lenses.md](lenses.md)).
- **Grill-only:** `grill` / `grill-with-docs` / `stress-test this plan` → [grill.md](grill.md) (needs Analyze / idea).

## Non-negotiables (hard stops)

1. **Gate C always blocking.** Never commit, push, open a PR, or merge without an explicit user yes that names each action. ([hitl.md](hitl.md))
2. **No secrets** in commits; never force-push.
3. **Design before code.** Design-review **or** design-verify-phase Result **clean** (by Mode) before Build (and before optional 04a).
4. **Build / Fix Verify gate** — do not advance on verify-fail. ([verify-and-fix.md](verify-and-fix.md))
5. **Do not invent approval** — stop / veto / async Gate B gap / **Build armed** / Status / skip-review ban: [stages.md](stages.md) · [hitl.md](hitl.md) · [lenses.md](lenses.md).

**Companion links (not duplicated here):** Smoke after Build (Build-writes-Smoke) · legal skip-review → [lenses.md](lenses.md) · [verify-and-fix.md](verify-and-fix.md) · [hitl.md](hitl.md). Fresh Task → **required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` ([handoffs.md](handoffs.md) = edit SoT / debug only · [skills-path.md](skills-path.md)). Usage limit → [models.md](models.md). Design-backloop / max-round → [failure-playbook.md](failure-playbook.md) · [invariants.md](invariants.md). No UI concept step → [LEGACY.md](LEGACY.md). Parent checklist → [invariants.md](invariants.md). Skills SoT + sync → [skills-path.md](skills-path.md).

## Routing (package + parent load)

| Need | Read |
|------|------|
| Runtime order / Mode / resume / abort | [stages.md](stages.md) |
| Card Stage id / Next → which 1–2 files | [parent-next.md](parent-next.md) · `lint-run.py --next` |
| Gate B/C · veto · **Gate B approved** · async gap · **Build armed** · Gate C bar | [hitl.md](hitl.md) |
| Models + usage-limit | [models.md](models.md) |
| Has API/DB · tiny-tweak · Lens plan · skip-review ban | [lenses.md](lenses.md) |
| Parent checklist · Task-count budget · max-round Decisions | [invariants.md](invariants.md) |
| Hard stop chat scripts | [failure-playbook.md](failure-playbook.md) |
| Next step (live run) | `00-run.md` Orchestrator card + **one** companion section |
| Task prompt | **Required:** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` + **subflow `stages/<id>.md`**. [handoffs.md](handoffs.md) = edit SoT / debug only (do not load whole file for launch) |
| Build / Fix | card + handoff `build`/`fix-*` + [verify-and-fix.md](verify-and-fix.md) |
| New artifact body | one file under [artifacts/](artifacts/INDEX.md) |
| Grill | [grill.md](grill.md) (once when entering Grill) |
| Lint `00-run.md` | [scripts/lint-run.py](scripts/lint-run.py) · [scripts/README.md](scripts/README.md) (`--next`, `--before-build`, `--before-code-review`, `--before-merge`, `--dry-run-seed`) |
| Phase entry | that subflow `SKILL.md` once |
| Golden paths | [examples/INDEX.md](examples/INDEX.md) |
| Anti-patterns | [examples/anti-patterns.md](examples/anti-patterns.md) |
| Solo subflow | [solo-entry.md](solo-entry.md) |
| Resolve `{skill}` + sync | [skills-path.md](skills-path.md) |
| Severity exit | [severity.md](severity.md) |
| Result first-line tokens | [results.md](results.md) |
| Artifact size / context budget | [size-caps.md](size-caps.md) |
| Legacy resume aliases | [LEGACY.md](LEGACY.md) |

Do **not** duplicate Happy path / Mode / veto / skip-review / Verify rules here — edit the SoT file in the table.  
Do **not** re-read this whole SKILL every step.  
`disable-model-invocation` is omitted so the orchestrator stays discoverable.

## Sub-workflows (inventory — not runtime order)

**Runtime order** lives only in [stages.md](stages.md). Solo prerequisites: [solo-entry.md](solo-entry.md).

| Skill | Role |
|-------|------|
| [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md) | Full chain or simple **design-phase**; Update from design review; design-backloop updates |
| [`my-dev-flow-design-review`](../my-dev-flow-design-review/SKILL.md) | Full: API∥DB parallel + general; simple: **design-verify-phase** |
| [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) | Optional TDD review → Build (draft + Verify gate + Smoke section); Fix from tests/review |
| [`my-dev-flow-review`](../my-dev-flow-review/SKILL.md) | Profile full: Adv→Quality→lenses; profile lite: **must** code-review-phase (any Mode) |
| [`my-dev-flow-test`](../my-dev-flow-test/SKILL.md) | Smoke re-run (usually skipped); **test-full** (profile full) or **test-lite** (profile lite) |
| [`my-dev-flow-merge`](../my-dev-flow-merge/SKILL.md) | Gate C (**blocking**) → commit/push/PR/merge only after explicit yes |

Each subflow can run **alone** when its prerequisites are met.
