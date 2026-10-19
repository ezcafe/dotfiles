# Gate B — design → Build

**Read before you decide:** Gate B only when **Design clean** / **Verify clean** ([results.md](results.md)): overall `03a` **clean** **and** required isolated API/DB **clean**|**skipped**. Has=yes (not tiny) → isolated file required. Overall token alone does not pay.

## Settle generation (v3 SoT — replaces clock compare)

Card fields on `00-run.md`:

- **Gate B settle gen:** integer (starts `0`)  
- Settle token (one of):  
  - blocking: `Gate B approved` + provenance  
  - auto: Notes / Run-log `gate-b auto — gen:<N>`  
  - async: Build armed after veto window  

**Gate B settled** iff durable settle token exists **and** its `gen` equals current **Gate B settle gen**.

Bump settle gen (+1) and clear approved / armed / auto token on:

- Amend / design-backloop  
- Mid-run Upgrade to full  
- Has flip any flag → **yes** ([lenses.md](lenses.md))

## Prefer gate-b

When Design clean and not settled → Expected Next `gate-b` (parent-only).

- **Blocking:** AskQuestion; on yes write approved + provenance; Prefer `build`.  
- **Auto:** same turn write `gate-b auto — gen:<N>`; Prefer `build` (no user wait).  
- **Async-notify:** post digest; Status `paused` until arm or veto.

## Clear on…

| Event | Clear |
|-------|-------|
| Amend / Upgrade / Has flip | approved, armed, auto token; bump settle gen |
| design-stale / design-backloop | same + Last Verify pending |

## Build fail-closed

Build FIRST: if auto and no matching `gate-b auto — gen:<current>` → `Result: blocked — Gate B auto not settled`.  
If settled gen mismatch → `Result: blocked — Gate B settle stale`.
