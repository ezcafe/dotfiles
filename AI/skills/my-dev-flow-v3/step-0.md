# Step 0 — classify and seed

## Load budget (every later turn)

Open **only**:

1. [preflight.md](preflight.md)  
2. [derive-next.md](derive-next.md) (Definitions + matching Pre **or** Post half if split — v3 keeps one file)  
3. The handoff **row** for Next (not full [handoffs.md](handoffs.md) unless first compose)  
4. [parent-next.md](parent-next.md) Open 1–2  
5. Subflow `stages/<id>.md` **or** parent-only gate file for `gate-b` / `gate-c`

**Never** re-read orchestrator [SKILL.md](SKILL.md) every step.  
**Parent-only Next** (`gate-b`, `gate-c`): skip handoff compose and `stages/<id>.md` — open the gate file only.

## Classify

1. Infer Mode + Review profile from ask ([stages.md](stages.md) Cheap path).  
2. Set **Has UI / API / DB / auth-PII-schema** tentatively (`yes`/`no`/`unknown`).  
3. Seed `.my-docs/workflow/<slug>/` from [artifacts/INDEX.md](artifacts/INDEX.md).  
4. Write `00-run.md`: Mode, profile, Has flags, **Gate B settle gen: 0**, Status `running`.

### Overrides

| User says | Rule |
|-----------|------|
| `simple` / `full` | Force Mode |
| `skip-review` while Mode **full** or profile **lite**/**full** | **Always** Decision N (Prefer Ask). Never auto-downgrade. Decision N **cannot** legalize Mode full + skip-review |
| `skip-review` on fresh seed (no Mode yet) | Mode **simple** + skip-review **only if** legality holds ([lenses.md](lenses.md)) |
| Already Mode **simple** + legal | May set profile skip-review |

## Mid-run Upgrade (simple → full)

Same turn:

1. Notes `design-stale`  
2. Invalidate overall + isolated `03a*` **clean** → `pending`  
3. Bump **Gate B settle gen** (+1); clear approved / Build armed / auto token  
4. **Last Verify: pending**; clear verify-pass stamp  
5. Keep `review-stale` / `test-stale` (skip-review: clear `review-stale` as N/A)  
6. Drop skip-review if set  
7. Derive Pre-Build: Gate A → skim if unpaid, then Prefer unpaid `analyze` → `grill` → `design`  
8. Do **not** Build / Post-Build while `design-stale`  
9. Clear `design-stale` only after Mode-full `design` + `03` rewrite; Design clean only after Mode-full design-review (or API∥DB → design-review)

## Skills path

When `AI/skills/my-dev-flow-v3` exists, run `./AI/skills/sync-to-cursor.sh --check` (or sync) before classify if the project uses that helper — [skills-path.md](skills-path.md).
