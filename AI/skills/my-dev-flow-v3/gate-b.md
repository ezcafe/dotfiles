# Gate B — design → Build

**Read before you decide:** Gate B only when **Design clean** / **Verify clean** ([results.md](results.md)): overall `03a` **clean** **and** required isolated API/DB **clean**|**skipped**. Has ∈ {yes, unknown} (not tiny) → isolated file required. Overall token alone does not pay.

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
- Has flip any flag → **yes** (from `no` **or** `unknown` — [lenses.md](lenses.md))

## Default tier

| Mode / scope | Prefer |
|--------------|--------|
| Mode **full** | Always **blocking** ([hitl.md](hitl.md)) |
| Mode **simple** + API=no ∧ DB=no ∧ auth/PII/schema=no | **auto** |
| Mode **simple** else (any API **or** DB **or** auth/PII/schema = **yes** **or** `unknown` — not all explicit `no`) | **blocking** ([hitl.md](hitl.md)) |

**SoT phrase (everywhere):** Mode simple auto **iff** Has API=no ∧ Has DB=no ∧ Has auth/PII/schema=no (explicit `no` only — `unknown` ≠ `no`); else **blocking** (yes **or** unknown on any of those flags). **Has UI** is not in this predicate — UI-only Has flip bumps settle + clears token but does **not** force blocking when API/DB/auth stay explicit `no` ([lenses.md](lenses.md) Has flip §2–3).

**async-notify:** only Mode simple auto path **and** user asks for a veto window.

## Prefer gate-b

When Design clean ∧ **04a ok** (¬ **04a unpaid / dirty**, incl. ¬ planned tests present) and not settled → Expected Next `gate-b` (parent-inline **or** labeled solo as orchestrator — not a Task stage — [derive-next.md](derive-next.md) · [solo-entry.md](solo-entry.md) · [hitl.md](hitl.md)).

**Run-log settle line (required on every settle):** after writing the durable settle token, append a Run-log settle line for that settle (`Gate B approved — gen:<N>` / `gate-b auto — gen:<N>` / Build-armed arm). When Notes `design-backloop` is set, that Run-log line **must** appear **after** the Notes `design-backloop` line (or ISO stamp on Notes vs Run-log proves after) so **Gate B settled post-Notes** can hold — [design-backloop.md](design-backloop.md) · [derive-next.md](derive-next.md).

**Prefer after settle (Notes `design-backloop`):**

| Notes `design-backloop` | After settle → Prefer |
|------------------------|------------------------|
| **Set** ∧ ¬ **Gate B settled post-Notes** | Stay / Prefer `gate-b` — do **not** Prefer `build` (even Mode simple **auto** same turn; gen-match alone ≠ post-Notes) |
| **Set** ∧ **Gate B settled post-Notes** | Clear Notes same turn → Prefer `build` ([derive-next-pre.md](derive-next-pre.md) clear→build row) |
| **Cleared** / absent ∧ Gate B settled | Prefer `build` |

- **Blocking:** AskQuestion; on yes write `Gate B approved` + provenance `gate-b-approved` (`user: "…"` ≥12 chars — [hitl.md](hitl.md)) **and** Run-log settle line (above); then Prefer per table (not unconditional `build`).  
- **Auto:** Mode simple only when API=no ∧ DB=no ∧ auth/PII/schema=no; same turn write Notes/Run-log `gate-b auto — gen:<N>` (gen = current settle gen) **and** Run-log settle line ordered for post-Notes when Notes set; Prefer per table — **never** Prefer `build` while Notes `design-backloop` still set without **Gate B settled post-Notes**.  
- **Async-notify:** post digest; Status `paused` until **Build armed: yes** + Run-log arm (same settle gen; arm line after Notes when backloop set) or veto — **paused-wait** while Build armed unpaid (do **not** Prefer `gate-b` again — [derive-next-pre.md](derive-next-pre.md) · [resume.md](resume.md)).

## Clear on…

| Event | Clear |
|-------|-------|
| Amend / Upgrade / Has flip | approved, armed, auto token; bump settle gen |
| design-stale / design-backloop | same + Last Verify pending |

## Build fail-closed

Build FIRST is the **full ordered list** in [../my-dev-flow-v3-code/stages/build.md](../my-dev-flow-v3-code/stages/build.md) and [verify.md](verify.md) Build Gate B check (Design clean → Grill closed → **04a ok** → no stale/backloop Notes → Gate B settled) — **not** the Gate B predicate alone.

Gate B item on that list:

if ¬ **Gate B settled** → `Result: blocked — Gate B not settled`

Covers all of: missing blocking `Gate B approved` + provenance, missing matching `gate-b auto — gen:<current>`, missing **Build armed** on async-notify, settle gen mismatch. Optional subtype in body: `blocking` / `auto` / `async` / `stale`.
