# Anti-patterns (do not)

Quick “wrong move → right move” for [`my-dev-flow`](../SKILL.md).

| Wrong | Right |
|-------|-------|
| Infer pipeline order from the subflow inventory table | Follow [stages.md](../stages.md) **Full/Simple pipeline order** only |
| Launch separate Adversarial then Quality when Review profile **lite** | One Task `code-review-phase` (Lite combined) |
| Mode **simple** + Review profile **full** | Use profile **lite** / **skip-review**, or reclassify to Mode **full** ([stages.md](../stages.md); lint error) |
| Mode **full**: Skip parallel API ∥ DB when both Has API and Has DB are yes (and not tiny-contract-tweak) | Same-turn parallel isolated Tasks when both `03a-*` missing, then general design-review; **Pending parallel:** `api\|db` until both `03a-*` exist ([lenses.md](../lenses.md) · [stages.md](../stages.md) Speed defaults) |
| Mode **full**: Re-launch API ∥ DB parallel when one `03a-*` already exists (resume) | Launch **missing only** (resume serialize); do not re-parallel ([lenses.md](../lenses.md) · derive H3) |
| Mode **simple**: Launch isolated API ∥ DB / set **Pending parallel** `api\|db` when both Has API/DB | Fold into `design-verify-phase`; keep **Pending parallel:** `none` (do not set `api\|db`) ([lenses.md](../lenses.md) · [stages.md](../stages.md) Speed defaults) |
| Advance after Build/Fix on **verify-fail** | Stay; retry within 3 or Decision N ([failure-playbook.md](../failure-playbook.md)) |
| Treat Gate B **auto** / **async-notify** as commit approval | Gate C always blocking; name each git action ([hitl.md](../hitl.md)) |
| Launch Merge when **Gate C approved** is missing / `none` | Ask Gate C; set durable field; `--next` / lint block until non-empty ([hitl.md](../hitl.md)) |
| Use Gate B **async-notify** as default on Mode **full** | Mode full → **blocking** only; async-notify only Mode **simple** + Has API/DB=no + no auth/PII/schema ([hitl.md](../hitl.md) Default Gate B narrow async) |
| Mode **simple** low-risk: default Gate B to **async-notify** without user asking for a veto window / async digest | Prefer **auto**; use **async-notify** only when the user asks for that veto window ([hitl.md](../hitl.md) Default Gate B) |
| Launch Build in the **same parent turn** as async-notify Gate B digest | One turn gap: `--next` → copy `async-gap-pending — <digest-ts>`; arm with **later** HH:MM + **Build armed** ([hitl.md](../hitl.md)); Build re-reads `Gate B veto`; resume counts as next turn |
| Invent Notes `parent turn gap observed` (or same-turn dual HH:MM / missing pending token) to fake the async gap | Run `--next` on digest-only state; copy `async-gap-pending`; arm later than digest; keep `.lint-async-gap` ([hitl.md](../hitl.md)) |
| Set **Gate B approved** / **Gate C approved** / waive kinds / `docs-only` / `smoke-pass (re-run)` / `card-override` without quality provenance | Add `provenance — <kind> — user: "<verbatim ≥12 chars, non-filler>"` ([hitl.md](../hitl.md) Provenance) |
| Launch with card Next ahead of derive (e.g. `merge` / `build` / `code-review-phase` while derived is pre-Build) without card-override + provenance | Fix card, or Notes `card-override — <reason>` + `provenance — card-override — user: "…"` (+ Decision N); unsafe → `do-not-launch` exit 1 ([parent-next.md](../parent-next.md)) |
| Skip sync-to-cursor after editing `AI/skills/` | Run `./AI/skills/sync-to-cursor.sh` (optional `--check` for my-dev-flow* drift — [skills-path.md](../skills-path.md)) |
| Load whole [handoffs.md](../handoffs.md) for every Task launch | **Required** `scripts/handoff-for.py <stage-id>` ([handoffs.md](../handoffs.md) = edit SoT / debug only) |
| Ignore `main-thread fallbacks ≥ 3` | Decision N soft pause ([invariants.md](../invariants.md)) |
| Keep **skip-review** after Has API/DB flips to yes | Mid-run reclassify Decision N; drop skip-review ([lenses.md](../lenses.md)) |
| Pre-load security/perf/memory lenses “just in case” | Lens plan default **none**; add on clear signals only |
| Force **api**/**db** lenses despite Notes `tiny-contract-tweak` | Notes fold into Quality / code-review-phase; no isolated API/DB Tasks; never invent empty `03a-api`/`03a-db` |
| Invent Verify commands / stack on `test-lite` | Read `00-run.md` Verify commands only; honor N/A ([verify-and-fix.md](../verify-and-fix.md)) |
| Silently amend `03-design` / `04-tasks` inside Fix | Design-backloop Decision N |
| Re-read full orchestrator `SKILL.md` every step | Card + [parent-next.md](../parent-next.md) / `lint-run.py --next` + **one** companion section |
| Load whole subflow `stages.md` prompt body | Load only `stages/<stage-id>.md` for the Task |
| Launch Build while Notes say veto window open **without** **Build armed** | Next turn / resume sets **Build armed** first ([hitl.md](../hitl.md)); lint `--before-build` |
| Launch Build without **Gate B approved** when HITL Gate B is **blocking** | Set **Gate B approved** `yes` (or named pick) **+ provenance**; keep veto `none` ([hitl.md](../hitl.md)); lint `--before-build` / `--next` |
| Launch Merge when **Gate C approved** lacks provenance | Add `provenance — gate-c-approved — user: "…"` ([hitl.md](../hitl.md)) |
| Paste full artifact catalog into every Task | Stage-scoped handoff via `handoff-for.py` only |
| Use Status values like `review` / `test` as resume position | Status = `running\|paused\|stopped\|done`; position = stage id on card |
| Mark run `done` on PR-only / commit-only or before Merge Result **success** | `done` only when Merge Result **success** **and** `merge` ∈ Gate C approved; subset without `merge` → stay `paused`; abort → `stopped` ([results.md](../results.md)) |
| Invent unit/e2e runners when Verify commands say N/A | Honor N/A; do not invent a test stack |
| Copy Gate B HITL tier into Grill | HITL Grill is independent ([grill.md](../grill.md) · [hitl.md](../hitl.md)) |
| Mode **simple** `design-phase` skips Grill HITL when frontier open or Has API/DB | Still honor HITL Grill ([grill.md](../grill.md) · [hitl.md](../hitl.md)); bundle ≠ skip Grill |
| Rush Gate C under **skip-review** with only Build-writes-Smoke and no independent check | Before Gate C: Notes `smoke-waive` / `smoke-pass (re-run)` / `gate-c-test-override` / `docs-only` **each with provenance**; else lint `--before-merge` **errors** (fail-closed). Recovery order: [verify-and-fix.md](../verify-and-fix.md) · [hitl.md](../hitl.md) |
| Invent Gate A Result `ok` on resume (no Decision N + explicit user yes) | Hold; Decision N → re-run Gate A, or set `ok` + Notes **only after explicit user yes** — never invent ([results.md](../results.md) · [failure-playbook.md](../failure-playbook.md)) |
| Omit Notes `review-stale` / `test-stale` after rebuild or design-backloop when prior `05`/`06` Results exist | Add both tokens (or clear Results); lint fail-closed when `Last verify-pass at` shows unpaid clean/success ([verify-and-fix.md](../verify-and-fix.md) Stale) |
| Skip required clarity-check at design/code boundaries | Open the boundary file; if it fails → ask the user; do not launch. Soft Next: presence-any token; high-risk (`tdd-review` / `build` / `fix-*` / `merge`): boundary-matched `clarity-check ok — <Next>` ([parent-next.md](../parent-next.md) · [invariants.md](../invariants.md)) |
| Use a soft-boundary clarity token (e.g. `design-phase`) to unlock Next `tdd-review` / `build` / `merge` | Log a matching high-risk token (`clarity-check ok — tdd-review` / `build` / `merge` / …) |
