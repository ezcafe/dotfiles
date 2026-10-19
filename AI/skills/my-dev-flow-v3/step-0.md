# Step 0 — classify and seed

## Load budget (every later turn) — SoT

Open **only**:

1. **Routing pack:** [preflight.md](preflight.md) + [derive-next.md](derive-next.md) (Definitions + Unsafe jumps) **+** matching half: [derive-next-pre.md](derive-next-pre.md) **or** [derive-next-post.md](derive-next-post.md) per selector  
2. The handoff **row** for Expected Next only (not full [handoffs.md](handoffs.md) unless first compose) — [row-only](#row-only)  
3. [parent-next.md](parent-next.md) — **read only the row** for Expected Next → open its **Open 1–2** files (stage/gate paths in that row; not a separate “one stage file” rule)  
4. When Next ∈ clarity-check set ([clarity-check.md](clarity-check.md)) — open [clarity-check.md](clarity-check.md) (or inline checklist) **before** the stage; log `clarity-check ok — <Next>` ([preflight.md](preflight.md) Always §6 · [parent-next.md](parent-next.md)). **In addition to** Open 1–2 — does **not** compete for the two-file slot.

**Never** re-read orchestrator [SKILL.md](SKILL.md) every step.  
**Parent-only Next** (`gate-b`, `gate-c`, `finalize-lens-plan`): skip handoff compose — Open 1–2 is the gate/lenses file only.

### Row-only

Progressive disclosure: when opening [handoffs.md](handoffs.md) or [parent-next.md](parent-next.md), read **only** the matching Expected Next row — not the whole table.

## Classify

1. Infer Mode + Review profile from ask ([stages.md](stages.md) Cheap path).  
2. Set **Has UI / API / DB / auth/PII/schema** (`yes`/`no`/`unknown`). Template defaults are all **`unknown`** ([artifacts/00-run.md](artifacts/00-run.md)) — do **not** seed all-`no` to unlock auto paths. Prefer resolve to explicit `yes`\|`no` before seed when evidence is clear; **require** explicit `yes`\|`no` before Gate B auto / skip-review.  
3. Create `.my-docs/workflow/<slug>/`.  
4. Seed **only** `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md): Mode, profile, Has flags, **Gate B settle gen: 0**, Status `running`.  
   **`unknown` on the card:** allowed when still unresolved; **`unknown` ≠ `no`** — Gate B auto fail-closes on API/DB/auth `unknown` only ([gate-b.md](gate-b.md)); skip-review fail-closes on UI/API/DB/auth `unknown` ([lenses.md](lenses.md)). Later `unknown`→`yes` runs full Has flip.  
   **Do not** copy other artifact templates at Step 0 — stages create them when they write ([artifacts/INDEX.md](artifacts/INDEX.md)). Seeded `pending` stubs must never count as Design present (`03`+`done`) / Grill closed (`frontier-empty` only; Notes `grill-skip` still closes).

### Overrides

| User says | Rule |
|-----------|------|
| `simple` / `full` | Force Mode |
| `skip-review` while Mode **full** or profile **lite**/**full** | **Always** Decision N (Prefer Ask). Never auto-downgrade. Decision N **cannot** legalize Mode full + skip-review |
| `skip-review` on fresh seed (no Mode yet) | Mode **simple** + skip-review **only if** legality holds ([lenses.md](lenses.md)) |
| Already Mode **simple** + legal | May set profile skip-review |

## Mid-run Upgrade (simple → full)

Same turn (**parent-only** lifecycle Notes — Stages return `candidate design-stale` / stale signals only; [hitl.md](hitl.md)):

1. Write card **Mode = full** (required — Prefer / F11 assume Mode full after Upgrade; Mode simple Prefer rows no longer apply)  
2. **Mode×profile:** drop skip-review if set → profile **lite** or **full** only; clear `review-stale` as N/A when dropping skip-review (Decision N **cannot** keep Mode full + skip-review — [lenses.md](lenses.md) · Overrides above)  
3. Notes `design-stale` (parent set)  
4. Invalidate `03` Result → `pending` (breaks Design present); invalidate overall + isolated `03a*` **clean** → `pending`; optionally invalidate `02-analysis` → `pending` (force re-analyze); optionally invalidate / re-open `02b` (Result → `pending` or delete) so **Grill open** Prefer `grill` under design-stale  
5. Bump **Gate B settle gen** (+1); clear approved / Build armed / auto token  
6. **Last Verify: pending**; clear verify-pass stamp  
7. Keep `review-stale` / `test-stale` (except N/A clear in step 2) — parent set/clear only  
8. Derive Pre-Build: Gate A → skim if unpaid, then Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** (**design-stale unpaid** — checkable Definitions; ban `design` while Grill open; do **not** Prefer Isolated / design-review / design-verify / `design-update` / require design-update Run-log)  
9. Do **not** Build / Post-Build / Isolated / design-review / design-verify / design-update while `design-stale`  
10. Clear `design-stale` only after Mode-full `design` + `03` rewrite (Result `done`) — parent clear when stage returns `candidate clear design-stale`; Design clean only after Mode-full design-review (or API∥DB → design-review)

## Skills path

When `AI/skills/my-dev-flow-v3` exists, run `./AI/skills/sync-to-cursor.sh --check` (or sync) before classify if the project uses that helper — [skills-path.md](skills-path.md).
