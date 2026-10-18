# Step 0 — Classify + resolve models + create run

**SoT for:** Load budget, Step 0 classify/seed, Mode selection, Review profile, mid-run reclassify.  
Runtime Happy path: [stages.md](stages.md). HITL defaults: [hitl.md](hitl.md).

## Load budget

Per-stage open set is **not** a hard “one companion” / “card + one section” cap. High-risk Next often needs the parent-next Open row **and** a clarity file — that is in budget.

| When | Open | Do not |
|------|------|--------|
| **Step 0** | This file + [artifacts/00-run.md](artifacts/00-run.md) + [models.md](models.md) tier table + lint once | Whole SKILL.md · whole handoffs.md · all artifacts |
| **Each stage** | Orchestrator card + [orchestrator-rules.md](orchestrator-rules.md) launch card + `lint-run.py --next --derive` + `handoff-for.py` + `stages/<id>.md` + [parent-next.md](parent-next.md) **Open** row (1–2) + clarity file when Next ∈ clarity stages ([parent-next.md](parent-next.md)) | Re-read orchestrator SKILL · full handoffs table · unrelated stage prompts |

Soft caps: [size-caps.md](size-caps.md) · [invariants.md](invariants.md) Task-count / main-thread.

## Step 0 — Classify + resolve models + create run

0. **Skills sync (hard stop when `AI/skills/my-dev-flow` exists):** run `./AI/skills/sync-to-cursor.sh --check` (or full sync). Drift → **stop**; do not classify until SoT ↔ `~/.cursor/skills` matches ([skills-path.md](skills-path.md)).
1. **When NOT to run / invent *what*:** ask invents product scope with no framing/spec/`01-idea` → **Decision N**: **myplan** first (`{myplan}` via [skills-path.md](skills-path.md)) vs Mode **full** Ideation. Do not invent scope silently.
2. **Overrides:** resume keeps Mode + profile. User `simple`/`full` → Mode. User `skip-review` → profile skip-review (implies simple unless Decision N).
3. Else **3-question classify** (map to Mode; Decision N only if still ambiguous):
   1. **Outcome clear?** yes → lean simple; no → lean full (or myplan if inventing *what*).
   2. **API/DB?** new/changed public API or persistence → full (unless [tiny tweak](lenses.md)); no → lean simple.
   3. **Invent *what*?** yes → myplan Decision N or Mode full Ideation; no → proceed with Mode from (1)+(2) + [cheap path](stages.md#cheap-path-matrix).
4. Create slug; write `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md): Status `running`, Mode, profile, Complexity (one-line), Has UI/API/DB when known, Lens plan **none**, **Pending parallel: none**, Gate B veto **none**, models ([models.md](models.md)), card, HITL Gate B ([hitl.md](hitl.md) Default Gate B — full → **blocking**; simple low-risk → prefer **auto**; **async-notify** only when user asks for a veto window / async digest), HITL Grill (full → async-notify; simple → auto), HITL Gate C **blocking**.
5. **Lint (required):** `scripts/lint-run.py .my-docs/workflow/<slug>/`. **Before each Task:** `--next --derive` (phase gates auto from card Next — [parent-next.md](parent-next.md) · [scripts/README.md](scripts/README.md)). Optional: `--check-stage-ids` after editing handoffs/parent-next/stages; `--check-results` for Result tokens + size soft warns.
6. Chat one line: Mode + profile + why.

### Mode selection

| Signal | Prefer **simple** | Prefer **full** |
|--------|-------------------|-----------------|
| Scope | Bug fix, tweak, copy/token, one helper/field (tiny only) | New feature, multi-surface, product concept, non-tiny API/DB |
| Clarity | Outcome clear | Needs discovery / 80/20 |
| Framing | Thin idea from ask, or framing done | Needs Ideation → Gate A → skim |
| Risk | Low blast; no new auth; persistence only if tiny | Cross-cutting auth, schema, multi-app |
| UI | None / copy / tiny match | New multi-surface UX (in Design; no UI concept step) |

Rubber-stamp ask → **simple**. Invent *what* → **full** or myplan first. **Complexity** = one-line reason, not a second classifier.

### Review profile

| Profile | When | After Build (review + test) |
|---------|------|------------------------------|
| **full** | Mode **full** only (default for Mode full). **Forbidden** with Mode simple | See [Mode × profile](stages.md#mode--review-profile--post-build-path) |
| **lite** | Mode simple default; also allowed with Mode full | See [Mode × profile](stages.md#mode--review-profile--post-build-path) |
| **skip-review** | Mode simple only; legality ([lenses.md](lenses.md)) | See [Mode × profile](stages.md#mode--review-profile--post-build-path) · [hitl.md](hitl.md) |

Mode **simple** may use **lite** or **skip-review** only. Profile **full** requires Mode **full** (or reclassify).

### Mid-run reclassify

Scope grows (API/DB yes, auth/PII, multi-surface, blast radius): **Decision N** ([invariants.md](invariants.md)); drop **skip-review** when contracts appear ([lenses.md](lenses.md)).
