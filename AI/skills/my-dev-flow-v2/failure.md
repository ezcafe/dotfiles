# Failure playbook (hard-stop chat)

| Stop | Chat |
|------|------|
| Skills sync drift | Sync SoT then re-check; do not classify |
| Invent *what* without framing | Offer myplan vs Mode full Ideation |
| Gate A escalate | Decision N — never invent Result `ok` |
| design-review not clean before Build | Finish design-review / design-verify |
| Notes `design-stale` before Mode-full rewrite | Run Pre-Build first-match ([derive-next-pre.md](derive-next-pre.md)): unpaid Gate A → `gate-a`; unpaid skim → `skim`; then Prefer first unpaid among `analyze` → `grill` → `design`. Do **not** Build ([step-0.md](step-0.md) · [verify.md](verify.md)) |
| Design / design-review while **Grill open**; `design-phase` while Grill open **and** (design artifacts present **or** `02b` **needs-round**) | Stop; settle Grill (card Next = `grill`) until closed. Prefer `design-phase` on Grill open **only** for true cold start (no `02b` needs-round and no design artifacts) ([grill.md](grill.md) · [derive-next.md](derive-next.md)) |
| Gate B unsettled (incl. settle freshness unpaid / `blocked — Gate B settle stale`) | Prefer `gate-b` / re-settle after Design-clean (+ has-flip Note lower bound when present); do not launch Build ([derive-next.md](derive-next.md) Settle freshness) |
| Mode full + Gate B `auto` / `async-notify` | Force HITL Gate B to `blocking`; do not launch Build ([gate-b.md](gate-b.md) · [preflight.md](preflight.md)) |
| Mode simple Gate B still `auto` after Has API/DB/auth/PII/schema flips to **yes** | Force HITL Gate B to `blocking`; do not launch Build ([gate-b.md](gate-b.md) · [preflight.md](preflight.md)) |
| verify-fail ×3 | Decision N ([decisions.md](decisions.md)) |
| Max-round hit | Decision N |
| Has API/DB yes (not tiny) + Lens plan missing matching api/db before code review | Stop; parent finalize Lens plan ([lenses.md](lenses.md) Finalize deadline · [derive-next-post.md](derive-next-post.md)) |
| skip-review + Has API/DB/auth/PII/schema yes | Drop skip-review; reclassify if needed |
| Gate C without named yes | Ask commit/push/PR/merge; do not invent |
| Prefer stages while Status `done` \| `stopped` | Stop — do not Prefer ([derive-next-post.md](derive-next-post.md)) |
| Prefer `merge` when `merge` ∉ Gate C approved (PR-only / commit-only / **Gate C unpaid**) | Prefer `gate-c` (ask remaining named actions) or stay `paused` — do not Prefer `merge` from non-empty approved alone ([derive-next.md](derive-next.md) · [gate-c.md](gate-c.md)) |
| Prefer `merge` / `gate-c` under profile **lite** \| **full** while **¬Tests success** | Prefer unpaid `test-*` / clear stale per Lite/full clear ([verify.md](verify.md)); Prefer `gate-c` / `merge` only when **Tests success** ([gate-c.md](gate-c.md) · [derive-next.md](derive-next.md)) |
| Prefer stages while Status `paused` and still waiting on user | Stay paused ([resume.md](resume.md)) |
| Task wrote consent fields | Revert; parent re-writes after user yes |
| Secrets in commit path | Refuse; remove from stage |

Do not invent approval, override, or waive tokens to unblock.
