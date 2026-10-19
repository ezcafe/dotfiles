# HITL Gate B

**SoT for:** Default Gate B tiers, async-notify veto window, **Build armed**, **Gate B approved**, veto after Build, HITL Grill.  
Index + shared Provenance / Tiers / Git: [hitl.md](hitl.md). Gate C: [hitl-gate-c.md](hitl-gate-c.md). Pipeline: [stages.md](stages.md).

**Parent-only write (hard):** Parent writes **Gate B approved**, **Build armed**, and matching provenance — never from Task returns. See [hitl.md](hitl.md) Parent-only consent.

**Preferred collection (blocking Gate B):** When the IDE exposes **AskQuestion** / decision UI, prefer it to collect the user’s yes or named pick, then **parent** records **Gate B approved** + provenance in the **same turn**. Do not trust Task output as the yes. Residual: AskQuestion is preferred process, not machine-proof of speech ([hitl.md](hitl.md) Honesty).

## Default Gate B (narrow async)

| Mode / scope | Prefer |
|--------------|--------|
| Mode **full** | Always **blocking**. Never use async-notify or auto as default. |
| Mode **simple** + Has API=no + Has DB=no + no auth/PII/schema in scope + design-review **or** design-verify-phase Result **clean** (by Mode) + (04a ok\|skipped) | **auto** (default) |
| Mode **simple** + any of: Has API=yes, Has DB=yes, auth/PII/schema in scope, open Critical/Major | **blocking** |

**When to choose async:** Mode **simple** low-risk row above **and** the user asks for a veto window / async digest — otherwise prefer **auto**. **async-notify allowed only** for Mode **simple** when Has API=no **and** Has DB=no **and** no auth/PII/schema in scope. Else use **blocking** (or **auto** when the simple low-risk row holds).

**Seed + machine check (E4):** [artifacts/00-run.md](artifacts/00-run.md) seeds **HITL Gate B: auto**. Before lint allows tier **async-notify**, Notes (or Run log) **must** include a quality request line:

```markdown
- async-notify requested — user: "<verbatim ≥12 chars, non-filler>"
```

Bare `HITL Gate B: async-notify` without that line → lint **error**. Quote quality matches provenance (shape only — not chat-proof).

**Soft HITL** applies only to **HITL Grill** and Mode **simple** Gate B (when allowed). Mode **full** Gate B and Gate C are never soft.

## async-notify + Gate B veto + Build armed (required)

When Gate B uses **async-notify** (only when Default Gate B allows it):

1. Parent posts digest + auto-pick, then sets on `00-run.md`:
   - **`Gate B veto: none`**
   - Notes: `async-notify posted — veto window open until Build starts`
   - **Run log (required):** `- **HH:MM** · paused · gate-b · async-notify posted — veto window open`
   - Status **`paused`** (card Next step = `build` but do **not** launch yet)
   - Do **not** write **Build armed** yet
2. **One parent turn gap (required):** do **not** launch Build in the **same** parent turn as the async-notify Gate B digest. Run `lint-run.py <run-dir> --next` → expect `handoff: do-not-launch` and a line `async-gap-pending — <digest-HH:MM>` (also writes sidecar `.lint-async-gap` — local / do-not-commit; [hitl.md](hitl.md) · [scripts/README.md](scripts/README.md)). **Copy that line into Notes.** End the turn after posting.
3. **Arm Build on the next parent turn (or resume):** before launching Build, set durable token **`Build armed`** and append a **second** Run log line whose `HH:MM` is **strictly later** than the digest timestamp, e.g. `- **HH:MM** · paused · gate-b · Build armed`. Lint fail-closed unless **all** of: arm later than digest, Notes `async-gap-pending — <digest-ts>` matching Run log digest, and `.lint-async-gap` from a prior `--next` pause. Inventing Notes `parent turn gap observed` or forging two HH:MM values in one edit **without** the prior `--next` token/sidecar is **not** enough ([anti-patterns.md](examples/anti-patterns.md)).
4. If the user vetoes (reject / change pick) in chat **before or while Build is pending**:
   - Parent sets **`Gate B veto: pending`** + Notes with the veto pick
   - Clear / do not set **Build armed**
   - Status `stopped` **or** re-open Gate B (do not start Build)
5. **Build Task must re-read `00-run.md` first.** If `Gate B veto` is `pending` → stop with Result note `blocked — Gate B veto`; do not write code. If Notes still say veto window open **and** **Build armed** is missing → stop; parent must arm first.
6. After Build **starts** with veto still `none` and **Build armed** present: set Status `running`; **clear** Notes “veto window open”, **Build armed**, and `async-gap-pending` (Build in flight). Lint errors if Status=`running` while Notes still say veto window open, or if `--before-build` / Next=`build` sees veto window without **Build armed** / incomplete gap.

**Lint:** `scripts/lint-run.py <run-dir> --before-build` **and** default lint when card Next=`build` enforce veto `none` + veto-window / **Build armed** / Status consistency + **async turn-boundary gap** (arm later than digest + pending token + sidecar) + **Gate B approved** + provenance when HITL Gate B is **blocking**. `--next` with Next=`build` on the async path runs the **same** gap check and emits `do-not-launch` (exit **1**) until the gap is complete — including when **Build armed** is present but timestamps/token/sidecar fail. Notes `design-backloop` → **error** only on `--before-build` or Next=`build` (blocks Build even when Gate B soft / approved `none`); default lint with Next in recovery (`design-update` / re-review / `gate-b` / …) → **warn** recovery in progress — [design-backloop.md](design-backloop.md). Mode **full** + HITL Gate B ∈ {`auto`,`async-notify`} → lint error. Mode **simple** + (Has API/DB = yes **or** **Has auth/PII/schema** = yes) + HITL Gate B ∈ {`auto`,`async-notify`} → lint error (default and `--before-build`; Default Gate B requires **blocking**). `--before-design-review` requires **Has auth/PII/schema** `yes|no` (same as Has API/DB). `--next` emits `handoff: do-not-launch` (exit **1**) for Build until blocking **Gate B approved** + provenance is set (or until **Build armed** + turn-boundary gap when async-notify); with Notes `design-backloop` and Next `build` → redirect to `design-update` (Next `gate-b` + token → normal Gate B digest / settle; clear token on settle).

**Residual risk:** wall-clock HH:MM and a Notes token cannot prove a real chat turn boundary without IDE/chat integration. A determined agent can still invent sidecar + pending line + later HH:MM in one edit. The bar raises the cost (must run `--next` once on digest-only state) but does not eliminate forgeability.

**Durable resume:** If Notes say veto window open / Last stage is Gate B async-notify / Status `paused` with Next step `build`, and `Gate B veto` is `none`, a later **resume** counts as the next parent turn — run `--next` if sidecar missing, copy `async-gap-pending`, append **Build armed** Run log line (later timestamp), then launch Build after veto re-read. Do not require same-session memory. See [resume-abort.md](resume-abort.md).

## Gate B approved (durable)

**Required when HITL Gate B is `blocking` before Build:** parent records the user’s explicit yes (or named pick) on `00-run.md` **and** provenance ([hitl.md](hitl.md) Provenance):

```markdown
**Gate B approved:** yes

### Notes
- provenance — gate-b-approved — user: "yes go build"
```

| Value | Meaning |
|-------|---------|
| `none` | No Gate B yes yet (default until Gate B settles) |
| `yes` | User approved the Gate B digest / default pick |
| named pick (e.g. `Option 2`) | User chose that option; treat as approved |

**Rules by HITL Gate B tier:**

| HITL Gate B | Before Build |
|-------------|--------------|
| **blocking** | **Gate B approved** must be `yes` or a named pick (not `none`) **plus** provenance `gate-b-approved`. Lint `--before-build` and `--next` → `do-not-launch` until both set. |
| **auto** | Allow Build without user yes; **Gate B approved** may stay `none`. Log a Run log `gate-b` digest/auto-pick line (lint **warns** when Next=`build` / `--before-build` lacks it). |
| **async-notify** | Do **not** use Gate B approved as the arm token — use **Build armed** + turn-boundary gap (arm later than digest + `async-gap-pending` + sidecar; above). |

Gate B auto/async ≠ Gate C commit approval.

**Example:** Turn N — Gate B posts digest + auto-pick; sets `Gate B veto: none`; veto window Notes + Run log digest line; ends turn. Turn N+1 — no veto → Run log **`Build armed`** (new `HH:MM`) → launch Build (re-read veto = none). If user says “stop — use Option 2” → set `Gate B veto: pending`; do not arm; stop or re-open Gate B.

### async-notify veto after Build started

Do not silently continue to review. Pause with **Decision N** ([handoffs.md](handoffs.md) option shape; table SoT [invariants.md](invariants.md)):

| Option | What |
|--------|------|
| 1 | Discard draft; re-open Gate B with veto pick |
| 2 | Keep draft; re-open Gate B (amend design/tasks only) |
| 3 | Stop (Status `stopped`) |

**On re-open Gate B (Option 1 or 2):** set **`Gate B approved: none`**; clear Notes **Build armed** and veto-window tokens; card Next = `gate-b`; require a **fresh** Gate B digest + yes (or named pick) before Build. Do not reuse the prior approved token. Design-backloop Option 1 uses the same approved/armed reset but Next = `design-update` first ([design-backloop.md](design-backloop.md)).

## HITL Grill — default tier only (SoT)

**This section is SoT for Grill default tier by Mode.** Domain behavior (frontier / glossary / what each tier means in Grill): [grill.md](grill.md). Shared tier table: [hitl.md](hitl.md).

| Mode | Default Grill tier |
|------|--------------------|
| **full** | `async-notify` (prefer human-visible picks; blocking when auth/PII/schema forks) |
| **simple** | `auto` |

Do **not** copy Gate B tier into Grill unless `00-run.md` explicitly sets them equal.
