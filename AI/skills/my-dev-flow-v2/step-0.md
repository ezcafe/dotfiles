# Step 0 — Classify + seed run

**SoT for:** Load budget, classify, Mode, Review profile, mid-run reclassify.

## Load budget

| When | Open | Do not |
|------|------|--------|
| **Step 0** | This file + [artifacts/00-run.md](artifacts/00-run.md) + [models.md](models.md) | Whole SKILL.md · all artifacts |
| **Each stage** | Orchestrator card + [preflight.md](preflight.md) + [derive-next.md](derive-next.md) + handoff row + `stages/<id>.md` + [parent-next.md](parent-next.md) Open (1–2) | Re-read orchestrator SKILL · full handoffs |

Soft caps: [size-caps.md](size-caps.md).  
Golden paths (optional): [examples/INDEX.md](examples/INDEX.md).

## Steps

1. **Skills sync:** `./AI/skills/sync-to-cursor.sh --check` when `AI/skills/my-dev-flow-v2` exists — [skills-path.md](skills-path.md). Drift → stop.
2. **Invent *what*?** No framing/spec/`01-idea` → Decision N: **myplan** first vs Mode full Ideation.
3. **Overrides:** resume keeps Mode+profile. User `simple`/`full` → Mode. User `skip-review` → profile skip-review (implies simple unless Decision N).
4. Else **3-question classify:**
   1. Outcome clear? yes → lean simple; no → lean full
   2. API/DB new/changed? → full (unless [tiny tweak](lenses.md)); no → lean simple
   3. Invent *what*? → myplan or Mode full Ideation
5. Create slug; write `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md): Status `running`, Mode, profile, Complexity (one line), Has UI/API/DB/auth/PII/schema when known, Lens plan `none`, Pending parallel `none`, Gate B veto `none`, **Build armed: none**, models, HITL Gate B (full → blocking; simple → auto only if API=no DB=no auth/PII/schema=no else blocking), HITL Grill (full → async-notify; simple → auto), HITL Gate C **blocking**.
6. Run [preflight.md](preflight.md) seed checklist on `00-run.md`.
7. Chat one line: Mode + profile + why.

## Mode selection

| Signal | Prefer **simple** | Prefer **full** |
|--------|-------------------|-----------------|
| Scope | Bug fix, tweak, one helper | New feature, multi-surface, product concept |
| Clarity | Outcome clear | Needs discovery / 80/20 |
| Risk | Low blast; no new auth | Cross-cutting auth, schema, multi-app |

## Review profile

| Profile | When |
|---------|------|
| **full** | Mode full only (default) |
| **lite** | Mode simple default; also OK with Mode full |
| **skip-review** | Mode simple only; legality [lenses.md](lenses.md) |

## Mid-run reclassify

Scope grows (API/DB, auth/PII, multi-surface) → Decision N ([decisions.md](decisions.md)); drop skip-review when contracts appear.
