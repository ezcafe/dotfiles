# HITL (Gate B / Gate C / Grill)

Canonical human-in-the-loop rules for [`my-dev-flow`](SKILL.md).  
**This file is SoT for:** Gate B veto, **Gate B approved**, async-notify one-turn gap, **Build armed**, Gate C test bar, **Gate C approved** actions.  
Pipeline order: [stages.md](stages.md). Resume/abort: [resume-abort.md](resume-abort.md). Decision shapes: [handoffs.md](handoffs.md) + [invariants.md](invariants.md). Grill domain: [grill.md](grill.md).

## Tiers

| Tier | Behavior | Allowed for |
|------|----------|-------------|
| **auto** | Approve without waiting. Gate digest + user-first picks. | Gate B (**Mode simple** low-risk only); HITL Grill |
| **async-notify** | Post digest + user-first pick. **Gate B:** end turn; Build on **next** parent turn after **Build armed** (veto window). **Grill:** continue immediately. Silence is **not** a veto. | Gate B (**narrow** — see Default Gate B); HITL Grill |
| **blocking** | Pause for approve / reject. Gate digest ≤4 bullets. | Gate B (**required** Mode **full**); **required** for Gate C; HITL Grill when needed |

## Default Gate B (narrow async)

| Mode / scope | Prefer |
|--------------|--------|
| Mode **full** | Always **blocking**. Never use async-notify or auto as default. |
| Mode **simple** + Has API=no + Has DB=no + no auth/PII/schema in scope + design-review **or** design-verify-phase Result **clean** (by Mode) + (04a ok\|skipped) | **auto** (default) |
| Mode **simple** + any of: Has API=yes, Has DB=yes, auth/PII/schema in scope, open Critical/Major | **blocking** |

**When to choose async:** Mode **simple** low-risk row above **and** the user asks for a veto window / async digest — otherwise prefer **auto**. **async-notify allowed only** for Mode **simple** when Has API=no **and** Has DB=no **and** no auth/PII/schema in scope. Else use **blocking** (or **auto** when the simple low-risk row holds).

**Soft HITL** applies only to **HITL Grill** and Mode **simple** Gate B (when allowed). Mode **full** Gate B and Gate C are never soft.

Mechanics when async-notify is used: section below (veto window · one turn gap · **Build armed**).

## Gate digest

(1) what ships (2) top risks ≤3 (3) what verified (4) ask or auto-pick note / Gate C commit-push-PR-merge ask.

**User-first auto picks:** day-to-day user value first, then system convenience; log `auto-pick — Decision N Option K — user-first: …; system: …`.

## Git / remote (hard)

No `git commit` / `git push` / `gh pr create` / `gh pr merge` without explicit yes naming each action. Reject / silence at Gate C → stop. Gate B auto ≠ commit approval.

## Provenance (required for consent / waivers)

Inventable tokens without a user quote are **rejected**. Before lint accepts **Gate B approved** (blocking), **Gate C approved**, Notes `gate-c-test-override`, Notes `smoke-waive`, Notes/Complexity `docs-only`, Notes `smoke-pass (re-run)`, or Notes `card-override` (unsafe derive unlock), Notes or Run log **must** contain this fixed shape:

```markdown
- provenance — <kind> — user: "<exact user words>"
```

**Quote quality (required):** parent must copy the user’s words **verbatim**. Lint accepts a quote only when length ≥ **12** characters and the normalized quote is **not** a known filler (`yes`, `ok`, `approved`, `merge`, `lgtm`, `ship it`, …). Short or filler-only quotes → treat as missing provenance.

| `<kind>` | When required |
|----------|---------------|
| `gate-b-approved` | HITL Gate B **blocking** and **Gate B approved** is `yes` / named pick (before Build) |
| `gate-c-approved` | **Gate C approved** is a non-empty action subset (before merge) |
| `gate-c-test-override` | Notes include `gate-c-test-override` (waive only with this line) |
| `smoke-waive` | Notes include `smoke-waive` (waive only with this line) |
| `docs-only` | Complexity/Notes `docs-only` escape under skip-review (bare token alone rejected) |
| `smoke-pass-rerun` | Notes `smoke-pass (re-run)` escape under skip-review (bare token alone rejected) |
| `card-override` | Notes `card-override — <reason>` unlocking unsafe card vs derived (merge/build/jump-ahead) |

Bare approved fields, waiver tokens, or card-override **without** matching quality provenance → lint **error** / `--next` → `do-not-launch` (exit **1**). Do **not** invent quotes.

**Honesty:** lint provenance checks shape + quote quality — they are **not** proof the user said those words ([anti-patterns.md](examples/anti-patterns.md)).

**Residual risk:** lint raises the cost of forged quotes (length ≥12, filler ban, kind match). It does **not** prove the quote was uttered in chat.

## async-notify + Gate B veto + Build armed (required)

When Gate B uses **async-notify** (only when Default Gate B allows it):

1. Parent posts digest + auto-pick, then sets on `00-run.md`:
   - **`Gate B veto: none`**
   - Notes: `async-notify posted — veto window open until Build starts`
   - **Run log (required):** `- **HH:MM** · paused · gate-b · async-notify posted — veto window open`
   - Status **`paused`** (card Next step = `build` but do **not** launch yet)
   - Do **not** write **Build armed** yet
2. **One parent turn gap (required):** do **not** launch Build in the **same** parent turn as the async-notify Gate B digest. Run `lint-run.py <run-dir> --next` → expect `handoff: do-not-launch` and a line `async-gap-pending — <digest-HH:MM>` (also writes sidecar `.lint-async-gap`). **Copy that line into Notes.** End the turn after posting.
3. **Arm Build on the next parent turn (or resume):** before launching Build, set durable token **`Build armed`** and append a **second** Run log line whose `HH:MM` is **strictly later** than the digest timestamp, e.g. `- **HH:MM** · paused · gate-b · Build armed`. Lint fail-closed unless **all** of: arm later than digest, Notes `async-gap-pending — <digest-ts>` matching Run log digest, and `.lint-async-gap` from a prior `--next` pause. Inventing Notes `parent turn gap observed` or forging two HH:MM values in one edit **without** the prior `--next` token/sidecar is **not** enough ([anti-patterns.md](examples/anti-patterns.md)).
4. If the user vetoes (reject / change pick) in chat **before or while Build is pending**:
   - Parent sets **`Gate B veto: pending`** + Notes with the veto pick
   - Clear / do not set **Build armed**
   - Status `stopped` **or** re-open Gate B (do not start Build)
5. **Build Task must re-read `00-run.md` first.** If `Gate B veto` is `pending` → stop with Result note `blocked — Gate B veto`; do not write code. If Notes still say veto window open **and** **Build armed** is missing → stop; parent must arm first.
6. After Build **starts** with veto still `none` and **Build armed** present: set Status `running`; **clear** Notes “veto window open”, **Build armed**, and `async-gap-pending` (Build in flight). Lint errors if Status=`running` while Notes still say veto window open, or if `--before-build` / Next=`build` sees veto window without **Build armed** / incomplete gap.

**Lint:** `scripts/lint-run.py <run-dir> --before-build` **and** default lint when card Next=`build` enforce veto `none` + veto-window / **Build armed** / Status consistency + **async turn-boundary gap** (arm later than digest + pending token + sidecar) + **Gate B approved** + provenance when HITL Gate B is **blocking**. `--next` with Next=`build` on the async path runs the **same** gap check and emits `do-not-launch` (exit **1**) until the gap is complete — including when **Build armed** is present but timestamps/token/sidecar fail. Notes `design-backloop` → **error** only on `--before-build` or Next=`build` (blocks Build even when Gate B soft / approved `none`); default lint with Next in recovery (`design-update` / re-review / `gate-b` / …) → **warn** recovery in progress — [design-backloop.md](design-backloop.md). Mode **full** + HITL Gate B ∈ {`auto`,`async-notify`} → lint error. Mode **simple** + Has API/DB = yes + HITL Gate B ∈ {`auto`,`async-notify`} → lint error (default and `--before-build`; hitl.md Default Gate B requires **blocking**). `--next` emits `handoff: do-not-launch` (exit **1**) for Build until blocking **Gate B approved** + provenance is set (or until **Build armed** + turn-boundary gap when async-notify); with Notes `design-backloop` and Next `build` → redirect to `design-update` (Next `gate-b` + token → normal Gate B digest / settle; clear token on settle).

**Residual risk:** wall-clock HH:MM and a Notes token cannot prove a real chat turn boundary without IDE/chat integration. A determined agent can still invent sidecar + pending line + later HH:MM in one edit. The bar raises the cost (must run `--next` once on digest-only state) but does not eliminate forgeability.

**Durable resume:** If Notes say veto window open / Last stage is Gate B async-notify / Status `paused` with Next step `build`, and `Gate B veto` is `none`, a later **resume** counts as the next parent turn — run `--next` if sidecar missing, copy `async-gap-pending`, append **Build armed** Run log line (later timestamp), then launch Build after veto re-read. Do not require same-session memory. See [resume-abort.md](resume-abort.md).

## Gate B approved (durable)

**Required when HITL Gate B is `blocking` before Build:** record the user’s explicit yes (or named pick) on `00-run.md` **and** provenance:

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

Do not silently continue to review. Pause with **Decision N** ([handoffs.md](handoffs.md) shape):

| Option | What |
|--------|------|
| 1 | Discard draft; re-open Gate B with veto pick |
| 2 | Keep draft; re-open Gate B (amend design/tasks only) |
| 3 | Stop (Status `stopped`) |

**On re-open Gate B (Option 1 or 2):** set **`Gate B approved: none`**; clear Notes **Build armed** and veto-window tokens; card Next = `gate-b`; require a **fresh** Gate B digest + yes (or named pick) before Build. Do not reuse the prior approved token. Design-backloop Option 1 uses the same approved/armed reset but Next = `design-update` first ([design-backloop.md](design-backloop.md)).

## HITL Grill (independent of Gate B)

| Mode | Default Grill tier |
|------|--------------------|
| **full** | `async-notify` (prefer human-visible picks; blocking when auth/PII/schema forks) |
| **simple** | `auto` |

Do **not** copy Gate B tier into Grill unless `00-run.md` explicitly sets them equal. Domain rules: [grill.md](grill.md).

## Gate C test bar (before merge subflow)

| Review profile | Required |
|----------------|----------|
| **skip-review** | **Fail-closed:** legal only per [lenses.md](lenses.md) **and** Build **verify-pass** + Smoke smoke-pass **and** one escape **with provenance**: Notes `smoke-pass (re-run)` + `smoke-pass-rerun`, Complexity/Notes `docs-only` + `docs-only`, or `smoke-waive` / `gate-c-test-override` with their kinds. Free-text Notes alone are **rejected**. Relying on Build-writes-Smoke alone → lint `--before-merge` **error** / `--next` → `do-not-launch` (exit **1**). Recovery: [verify-and-fix.md](verify-and-fix.md) |
| **lite** | `06-test-log.md` Result **success** **and** **Test path last run:** `lite` (missing → fail closed; LEGACY alias `Mode last run`) |
| **full** | `06-test-log.md` Result **success** **and** **Test path last run:** `full` (missing → fail closed; LEGACY alias `Mode last run`) |

Explicit user override may waive green tests **only** with Notes `gate-c-test-override` **plus** provenance `gate-c-test-override`. Does **not** waive Notes `review-stale` / `test-stale` (or unpaid clean/success vs `Last verify-pass at` — [verify-and-fix.md](verify-and-fix.md) Stale).

**Lint:** `scripts/lint-run.py <run-dir> --before-merge` (also when `--next` and card Next=`merge`) enforces this bar from `00-run.md` + `06-test-log.md` unless Notes override **with provenance** is present; **errors** on `review-stale` / `test-stale` and on unpaid `05`/`06` vs `Last verify-pass at`; skip-review Build-only smoke → **error** unless the fail-closed escape above; also runs `--check-results` (warn-only).

After Merge Result **success** **and** `merge` ∈ **Gate C approved** → set Status **`done`**. Subset without `merge` (e.g. PR only) → stay `paused`; leave Next for remaining actions. Abort/reject → `stopped`, not `done` ([results.md](results.md) · [stages.md](stages.md) Done criteria).

## Gate C approved actions (durable)

**Required when at Gate C / before merge:** record the user’s explicit yes as a durable field on `00-run.md` **and** provenance:

```markdown
**Gate C approved:** commit,push,pr,merge

### Notes
- provenance — gate-c-approved — user: "commit push PR and merge"
```

| Value | Meaning |
|-------|---------|
| `none` | No Gate C yes yet (default until ask settles) |
| comma-separated subset of `commit` \| `push` \| `pr` \| `merge` | Actions the user named in this chat |

**Rules:**

- Do **not** invent actions. Subset only what the user named (“PR only” → `pr` or `commit,push,pr` as said).
- Provenance quote must match the user’s words (see Provenance section).
- Merge Task / parent must re-read **Gate C approved** before git/remote actions.
- Lint: default `scripts/lint-run.py <run-dir>` errors when card Next=`merge` and **Gate C approved** is missing / `none` / empty **or** provenance missing. `--before-merge` enforces approved-actions + provenance + Gate C test bar and runs `--check-results` warn-only (prefer before launching Merge).
