# Has flags / Lens plan / skip-review

## Has flags

`Has UI` · `Has API` · `Has DB` · `Has auth/PII/schema` — each `yes` \| `no`.

**Tiny:** isolated review may `skipped` when change is docs-only / comment-only against that surface.

## Has flip (no → yes)

Same turn:

1. If profile skip-review → drop to **lite** (mandatory; not Decision N Prefer-paid Else).  
2. Gate B → **blocking**.  
3. Bump **Gate B settle gen**; clear approved / armed / auto.  
4. Notes `has-flip — <flags> — gen:<N>`.  
5. If API/DB newly yes: invalidate overall `03a` clean **or** Prefer re-run until Design clean (Isolated unpaid even if files exist).  

Checked on: design / design-phase / design-update After, preflight Always, Before Build.

## Lens plan

Default `none`. When Has API/DB yes (not tiny), finalize `api` / `db` / `api|db` **before** Adv / code-review-phase.

**Lenses paid / clean:** see [derive-next.md](derive-next.md) Lens plan unpaid. Prefer `merge-findings` only when every planned lens is Result-bearing **and** Merged unpaid.

## skip-review legality

Only Mode **simple** + Has API=no + Has DB=no + Has auth/PII/schema=no.  
Mode full + skip-review = Forbidden (Decision N cannot legalize).

## UI craft

When Has UI = yes, design and review stages should apply interface craft: hierarchy, a11y, copy, typography, color, polish — point agents at project UI skills / impeccable / better-interface when installed ([references.md](references.md)). Do not invent a second design system.
