# Step 0 — Classify + seed run

**SoT for:** Load budget, classify, Mode, Review profile, mid-run reclassify.

## Load budget

| When | Open | Do not |
|------|------|--------|
| **Step 0** | This file + [artifacts/00-run.md](artifacts/00-run.md) + [models.md](models.md) | Whole SKILL.md · all artifacts |
| **Each stage** | Orchestrator card + [preflight.md](preflight.md) + [derive-next.md](derive-next.md) (Definitions + selector) + matching half ([derive-next-pre.md](derive-next-pre.md) or [derive-next-post.md](derive-next-post.md)) + handoff row + `stages/<id>.md` + [parent-next.md](parent-next.md) Open (1–2) | Re-read orchestrator SKILL · full handoffs · both derive halves |
| **Parent-only Next** (`gate-b` \| `gate-c`) | Orchestrator card + [preflight.md](preflight.md) + [derive-next.md](derive-next.md) (Definitions + selector) + matching half + [parent-next.md](parent-next.md) Open → gate file only ([gate-b.md](gate-b.md) / [gate-c.md](gate-c.md); [hitl.md](hitl.md) when linked) | Handoff compose · `stages/<id>.md` · sibling stage prompts |

Soft caps: [size-caps.md](size-caps.md).  
Golden paths (optional): [examples/INDEX.md](examples/INDEX.md).

## Steps

1. **Skills sync:** `./AI/skills/sync-to-cursor.sh --check` when `AI/skills/my-dev-flow-v2` exists — [skills-path.md](skills-path.md). Drift → stop.
2. **Invent *what*?** No framing/spec/`01-idea` → Decision N: **myplan** first vs Mode full Ideation.
3. **Overrides:** resume keeps Mode+profile. User `simple`/`full` → Mode. User `skip-review`: (1) Mode **full** or Review profile **lite**/**full** → **always** Decision N only ([decisions.md](decisions.md) User override `skip-review`) — Prefer Ask; never auto-downgrade Mode or auto-set skip-review. (2) Fresh seed (no Mode/profile yet) → Mode **simple** + profile **skip-review** only if legality holds ([lenses.md](lenses.md)). (3) Already Mode **simple** and skip-review legality holds → may set profile **skip-review**. (4) Decision N **cannot** legalize Mode **full** + skip-review ([stages.md](stages.md) Forbidden).
4. Else **3-question classify:**
   1. Outcome clear? yes → lean simple; no → lean full
   2. API/DB new/changed? → full (unless [tiny tweak](lenses.md)); no → lean simple
   3. Invent *what*? → myplan or Mode full Ideation
5. Create slug; write `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md): Status `running`, Mode, profile, Complexity (one line), Has UI/API/DB/auth/PII/schema when known, Lens plan `none`, Pending parallel `none`, Gate B veto `none`, **Build armed: none**, models, HITL Gate B (full → blocking; simple → auto only if API=no DB=no auth/PII/schema=no else blocking), HITL Grill (full → async-notify; simple → auto), HITL Gate C **blocking**.
6. Run [preflight.md](preflight.md#seed-checklist) on `00-run.md`.
7. Chat one line: Mode + profile + why.
8. **Mode simple bootstrap `01-idea`:** if no `01-idea.md` yet, parent **either** writes a minimal stub from [artifacts/01-idea.md](artifacts/01-idea.md) (Core problem line + Mode-simple stub OK) **or** launches `ideation` — then Next=`design-phase` ([derive-next.md](derive-next.md) · [handoffs.md](handoffs.md)). Mode full with no idea → `ideation` (not bootstrap).

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

**After Upgrade to full:** set Mode **full**, HITL Gate B **blocking**, profile **full**|**lite** (**never** skip-review — Decision N cannot legalize Mode full + skip-review). Keep `01-idea` unless Decision N requires Ideation redo. **Invalidate Mode-simple design bar:** set Notes `design-stale` — Mode-simple `analyze`/`grill`/`03`/`03a*` are **unpaid** until Mode-full rewrite. **Invalidate prior overall `03a` clean** **and** isolated `03a-api` / `03a-db` **clean** when present (same as Amend — set each Result **pending** or remove **clean** — prior clean is unpaid until a Mode-full design-review + isolated re-clean after the rewrite). Run [derive-next.md](derive-next.md) + [derive-next-pre.md](derive-next-pre.md) Pre-Build (Mode full) **first-match** before Design / API∥DB: unpaid Gate A → `gate-a`, then unpaid skim → `skim`, then Notes `design-stale` Prefer first unpaid among `analyze` → `grill` → `design` only (while `design-stale`, do **not** match Grill open / paid Mode-simple analysis — before Grill open / No `02-analysis`; fail-closed while `01a` ≠ `ok`). **Mirror design-backloop Amend:** **Gate B approved: none**; **Build armed: none**; clear veto-window tokens (`Gate B veto: none`; drop Notes `async-gap-pending` if present); **clear** `gate-b auto — <HH:MM>` (or digest) if present; set **Last Verify: pending**; **Last verify-pass at: none**; keep `review-stale` / `test-stale` when already set (skip-review: clear `review-stale` as N/A). Selector stays **Pre-Build** while Notes `design-stale` (do not open Post-Build on leftover verify-pass). **Parent clears** Notes `design-stale` only after Last stage `design` **and** `03-design.md` rewrite for Mode full — then Prefer re-run API∥DB when Has=yes **and** isolated unpaid/pending (**even if files exist**) until Mode-full isolated Last stage is paid; **Design clean** still unpaid until Mode-full `design-review` (or API∥DB → `design-review`) Result **`clean`** after that rewrite ([derive-next.md](derive-next.md)). Do **not** Build while Notes `design-stale` ([verify.md](verify.md) · [preflight.md](preflight.md)). Example: [reclassify-simple-to-full.md](examples/reclassify-simple-to-full.md).
