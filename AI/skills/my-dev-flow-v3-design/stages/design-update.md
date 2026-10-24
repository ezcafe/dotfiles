# Design-update

Rewrite design from review findings. Parent Prefer this stage when **Grill closed** **and** **design-update unpaid** (any `03a*` **`needs update`** **or** **backloop rewrite unpaid**) — before Isolated / design-review / design-verify. While **Grill open** → Prefer `grill` first ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/design-backloop.md](../../my-dev-flow-v3/design-backloop.md)).

## FIRST

1. Notes `design-stale` → `Result: blocked — design-stale` (unsafe-jump — Prefer **Grill open** → `grill` first, then Mode-full `design` + `03` rewrite — [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).  
2. **Grill open** → `Result: blocked — Grill open` (Prefer `grill` first — before `design-update` under Notes `design-backloop` / `needs update` — [../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md) · [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).  
3. Else proceed.

## After

**Orchestrated Task:** return `proposed Has: …` / `Has flip detected` / `candidate tiny-contract-tweak` only + Parent-relay — parent writes card Has + Notes via Always §4. **Labeled solo:** stamps Notes+provenance after AskQuestion; applies Has when acting as orchestrator ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md)).

**Hard stop** after Result — do **not** Prefer Next / write card fields. Parent re-derives ([../../my-dev-flow-v3/derive-next-pre.md](../../my-dev-flow-v3/derive-next-pre.md)).

**After (parent / labeled solo as orchestrator):** same-turn Run-log `design-update — settle-gen:<N>` (pays **backloop rewrite**) **and** set **ALL** `03a*` → **`pending`** — then re-derive ([../../my-dev-flow-v3/design-backloop.md](../../my-dev-flow-v3/design-backloop.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §8).
