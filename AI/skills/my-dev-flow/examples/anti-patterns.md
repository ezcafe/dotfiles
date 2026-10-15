# Anti-patterns (do not)

Quick “wrong move → right move” for [`my-dev-flow`](../SKILL.md).

| Wrong | Right |
|-------|-------|
| Infer pipeline order from the subflow inventory table | Follow [stages.md](../stages.md) **Full/Simple pipeline order** only |
| Launch separate Adversarial then Quality when Review profile **lite** | One Task `code-review-phase` (Lite combined) |
| Mode **simple** + Review profile **full** | Use profile **lite** / **skip-review**, or reclassify to Mode **full** ([stages.md](../stages.md); lint error) |
| Mode **full**: Skip parallel API ∥ DB when both Has API and Has DB are yes (and not tiny-contract-tweak) | Same-turn parallel isolated Tasks, then general design-review; **Pending parallel:** `api\|db` until both `03a-*` exist ([lenses.md](../lenses.md) · [stages.md](../stages.md) Speed defaults) |
| Mode **simple**: Launch isolated API ∥ DB / set **Pending parallel** `api\|db` when both Has API/DB | Fold into `design-verify-phase`; keep **Pending parallel:** `none` (do not set `api\|db`) ([lenses.md](../lenses.md) · [stages.md](../stages.md) Speed defaults) |
| Advance after Build/Fix on **verify-fail** | Stay; retry within 3 or Decision N ([failure-playbook.md](../failure-playbook.md)) |
| Treat Gate B **auto** / **async-notify** as commit approval | Gate C always blocking; name each git action ([hitl.md](../hitl.md)) |
| Use Gate B **async-notify** as default on Mode **full** | Mode full → **blocking** only; async-notify only Mode **simple** + Has API/DB=no + no auth/PII/schema ([hitl.md](../hitl.md) Option A) |
| Launch Build in the **same parent turn** as async-notify Gate B digest | One turn gap ([hitl.md](../hitl.md)); Build re-reads `Gate B veto`; resume counts as next turn |
| Skip sync-to-cursor after editing `AI/skills/` | Run `./AI/skills/sync-to-cursor.sh` ([skills-path.md](../skills-path.md)) |
| Ignore `main-thread fallbacks ≥ 3` | Decision N soft pause ([invariants.md](../invariants.md)) |
| Keep **skip-review** after Has API/DB flips to yes | Mid-run reclassify Decision N; drop skip-review ([lenses.md](../lenses.md)) |
| Pre-load security/perf/memory lenses “just in case” | Lens plan default **none**; add on clear signals only |
| Force **api**/**db** lenses despite Notes `tiny-contract-tweak` | Fold into design-review / Quality; no isolated API/DB Tasks; never invent empty `03a-api`/`03a-db` |
| Invent Verify commands / stack on `test-lite` | Read `00-run.md` Verify commands only; honor N/A ([verify-and-fix.md](../verify-and-fix.md)) |
| Silently amend `03-design` / `04-tasks` inside Fix | Design-backloop Decision N |
| Re-read full orchestrator `SKILL.md` every step | Card + [parent-next.md](../parent-next.md) / `lint-run.py --next` + **one** companion section |
| Load whole subflow `stages.md` prompt body | Load only `stages/<stage-id>.md` for the Task |
| Launch Build while Notes say veto window open **without** **Build armed** | Next turn / resume sets **Build armed** first ([hitl.md](../hitl.md)); lint `--before-build` |
| Paste full artifact catalog into every Task | Stage-scoped handoff row only ([handoffs.md](../handoffs.md)) |
| Use Status values like `review` / `test` as resume position | Status = `running\|paused\|stopped\|done`; position = stage id on card |
| Mark run `done` before merge or on abort | `done` only after merge success; abort → `stopped` |
| Invent unit/e2e runners when Verify commands say N/A | Honor N/A; do not invent a test stack |
| Copy Gate B HITL tier into Grill | HITL Grill is independent ([grill.md](../grill.md) · [hitl.md](../hitl.md)) |
| Mode **simple** `design-phase` skips Grill HITL when frontier open or Has API/DB | Still honor HITL Grill ([grill.md](../grill.md) · [hitl.md](../hitl.md)); bundle ≠ skip Grill |
