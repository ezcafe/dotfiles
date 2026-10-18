# Resume + Abort

**SoT for:** mid-run resume, abort / scope-change.  
Happy path: [stages.md](stages.md). Design invalid after Build: [design-backloop.md](design-backloop.md). Async arm: [hitl.md](hitl.md).

## Resume (mid-run)

1. Read `00-run.md`: Status, Last stage, card, Gates, profile, Mode, Gate B veto, Pending parallel.
2. Do not re-classify unless asked or scope changed.
3. Do not redo completed gates unless artifacts changed.
4. Next = first incomplete Full/Simple step, or card Next step / Stage id ([LEGACY.md](LEGACY.md) for Status-as-stage). **Required:** `lint-run.py <run-dir> --next --derive`. Unsafe card vs derived → error + `do-not-launch` unless Notes `card-override — <reason>` **and** `provenance — card-override — user: "…"` (+ optional Decision N) ([parent-next.md](parent-next.md); optional `tdd-review` until 04a / Notes skip — [lenses.md](lenses.md)).
5. When `--next` emits Task handoff (exit 0): one subflow `SKILL.md`; prompt = **required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` (includes Description) + **`stages/<stage-id>.md`** ([parent-next.md](parent-next.md) · [skills-path.md](skills-path.md); handoffs.md = edit SoT / debug only). If `do-not-launch`, stop and follow printed next action.
6. `stopped` → new Decision; `done` → new slug or explicit re-open.
7. Gate B veto `pending` → do not Build. Blocking without **Gate B approved** + provenance → do not Build ([hitl.md](hitl.md)).
8. async-notify gap: Notes veto window / paused + Next `build` + veto `none` → this resume **is** next parent turn — run `--next` if `.lint-async-gap` sidecar missing, copy `async-gap-pending`, append **Build armed** Run log line (**later** HH:MM), then launch after veto re-read ([hitl.md](hitl.md) Durable resume). Do **not** short-circuit to append **Build armed** then launch alone.

## Abort / scope-change

- Reject gate / stop / abort / cancel → Status `stopped` + Notes frozen stage + reason.
- Scope change → Decision N (reclassify / new slug / continue). Not Gate C approval.
- Silence at blocking gate → `paused` (do not invent approval).
- Design invalid after Build → [design-backloop.md](design-backloop.md).
- Merge Result success + `merge` ∈ Gate C approved → `done` + strongly recommended calibration Notes + `_calibration.md` append (lint warn — [stages.md](stages.md)). Soft Task-count / main-thread fallbacks: [invariants.md](invariants.md). Scripts: [failure-playbook.md](failure-playbook.md).
