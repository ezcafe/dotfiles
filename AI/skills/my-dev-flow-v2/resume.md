# Resume / abort / scope-change

## Resume

1. Read `00-run.md` Status, Last stage, card **Next**, Gate B/C / **Build armed** fields, **Last Verify** / **Last verify-pass at**, Notes (`design-backloop` / `design-stale` / stale).
2. Status **`done`** \| **`stopped`** → Stop; do **not** Prefer stages ([derive-next-post.md](derive-next-post.md)). PR-only / commit-only (**Gate C approved** non-empty but `merge` ∉ approved) → stay **`paused`** until user names remaining actions (`gate-c`) or aborts — do **not** Prefer `merge` ([gate-c.md](gate-c.md) · [derive-next.md](derive-next.md) **Gate C unpaid**).
3. Run [derive-next.md](derive-next.md); align card or ask. Selector: **Post-Build** only when **verify-pass fresh for current Gate B settlement** **and** no Notes `design-backloop` / `design-stale` — leftover verify-pass earlier than the current expanded settle minute (or after Amend / Upgrade reset) forces **Pre-Build**.
4. Set Status **`running`** when continuing work — on resume, Build arm, post-Decision continue, or Grill answers settled — unless still waiting on the user (async veto window open without arm, Gate A escalate unsettled, Gate B/C AskQuestion open, **Grill blocking** with open frontier / Decision N unsettled). Stay `paused` while waiting ([grill.md](grill.md)).
5. Async Gate B paused with veto window → treat resume as next turn: Status **`running`**; set **`Build armed: yes`** + Run log later HH:MM then Build if veto `none`.
6. Do not invent Gate B/C approved from memory.

## Abort

User reject/cancel → Status `stopped` (not `done`). Set **Build armed: none**; clear open veto window Notes as needed. Do **not** Prefer stages after `stopped`.

## Scope-change

API/DB/auth appears mid-run → Decision N reclassify ([decisions.md](decisions.md)); drop skip-review ([lenses.md](lenses.md)). Large pivot → new slug.
