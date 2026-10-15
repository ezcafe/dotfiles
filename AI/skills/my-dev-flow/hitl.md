# HITL (Gate B / Gate C / Grill)

Canonical human-in-the-loop rules for [`my-dev-flow`](SKILL.md).  
**This file is SoT for:** Gate B veto, **Gate B approved**, async-notify one-turn gap, **Build armed**, Gate C test bar, **Gate C approved** actions.  
Pipeline order: [stages.md](stages.md). Decision shapes: [handoffs.md](handoffs.md) + [invariants.md](invariants.md). Grill domain: [grill.md](grill.md).

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
| Mode **simple** + Has API=no + Has DB=no + no auth/PII/schema in scope + design-review clean + (04a ok\|skipped) | **auto** or **async-notify** |
| Mode **simple** + any of: Has API=yes, Has DB=yes, auth/PII/schema in scope, open Critical/Major | **blocking** |

**async-notify allowed only** for Mode **simple** when Has API=no **and** Has DB=no **and** no auth/PII/schema in scope. Else use **blocking** (or **auto** when the simple low-risk row above holds).

**Soft HITL** applies only to **HITL Grill** and Mode **simple** Gate B (when allowed). Mode **full** Gate B and Gate C are never soft.

Mechanics when async-notify is used: section below (veto window · one turn gap · **Build armed**).

## Gate digest

(1) what ships (2) top risks ≤3 (3) what verified (4) ask or auto-pick note / Gate C commit-push-PR-merge ask.

**User-first auto picks:** day-to-day user value first, then system convenience; log `auto-pick — Decision N Option K — user-first: …; system: …`.

## Git / remote (hard)

No `git commit` / `git push` / `gh pr create` / `gh pr merge` without explicit yes naming each action. Reject / silence at Gate C → stop. Gate B auto ≠ commit approval.

## async-notify + Gate B veto + Build armed (required)

When Gate B uses **async-notify** (only when Default Gate B allows it):

1. Parent posts digest + auto-pick, then sets on `00-run.md`:
   - **`Gate B veto: none`**
   - Notes: `async-notify posted — veto window open until Build starts`
   - Status **`paused`** (card Next step = `build` but do **not** launch yet)
   - Do **not** write **Build armed** yet
2. **One parent turn gap (required):** do **not** launch Build in the **same** parent turn as the async-notify Gate B digest. End the turn after posting.
3. **Arm Build on the next parent turn (or resume):** before launching Build, set durable token in Notes (or card): **`Build armed`**. Prefer Run log line `parent turn gap observed` + `Build armed`.
4. If the user vetoes (reject / change pick) in chat **before or while Build is pending**:
   - Parent sets **`Gate B veto: pending`** + Notes with the veto pick
   - Clear / do not set **Build armed**
   - Status `stopped` **or** re-open Gate B (do not start Build)
5. **Build Task must re-read `00-run.md` first.** If `Gate B veto` is `pending` → stop with Result note `blocked — Gate B veto`; do not write code. If Notes still say veto window open **and** **Build armed** is missing → stop; parent must arm first.
6. After Build **starts** with veto still `none` and **Build armed** present: set Status `running`; **clear** Notes “veto window open” and **Build armed** (Build in flight). Lint errors if Status=`running` while Notes still say veto window open, or if `--before-build` sees veto window without **Build armed**. A later veto uses **veto after Build** Decision below — do not silently continue to review.

**Lint:** `scripts/lint-run.py <run-dir> --before-build` enforces veto `none` + veto-window / **Build armed** / Status consistency + **Gate B approved** when HITL Gate B is **blocking**. Notes `design-backloop` → error until cleared after fresh Gate B settle (blocks Build even when Gate B soft / approved `none`) — [stages.md](stages.md). Mode **full** + HITL Gate B ∈ {`auto`,`async-notify`} → lint error. Mode **simple** + Has API/DB = yes + HITL Gate B ∈ {`auto`,`async-notify`} → lint error (default and `--before-build`; hitl.md Default Gate B requires **blocking**). `--next` emits `handoff: do-not-launch` for Build until blocking **Gate B approved** is set (or until **Build armed** when async-notify); with Notes `design-backloop` and Next `build` → redirect to `design-update` (Next `gate-b` + token → normal Gate B digest / settle; clear token on settle).

**Durable resume:** If Notes say veto window open / Last stage is Gate B async-notify / Status `paused` with Next step `build`, and `Gate B veto` is `none`, a later **resume** counts as the next parent turn — **set Build armed**, then launch Build after veto re-read. Do not require same-session memory. See [stages.md](stages.md) Resume.

## Gate B approved (durable)

**Required when HITL Gate B is `blocking` before Build:** record the user’s explicit yes (or named pick) on `00-run.md`:

```markdown
**Gate B approved:** yes
```

| Value | Meaning |
|-------|---------|
| `none` | No Gate B yes yet (default until Gate B settles) |
| `yes` | User approved the Gate B digest / default pick |
| named pick (e.g. `Option 2`) | User chose that option; treat as approved |

**Rules by HITL Gate B tier:**

| HITL Gate B | Before Build |
|-------------|--------------|
| **blocking** | **Gate B approved** must be `yes` or a named pick (not `none`). Lint `--before-build` and `--next` → `do-not-launch` until set. |
| **auto** | Allow Build without user yes; **Gate B approved** may stay `none` (optional log of auto-pick). |
| **async-notify** | Do **not** use Gate B approved as the arm token — use **Build armed** + one-turn gap (above). |

Gate B auto/async ≠ Gate C commit approval.

**Example:** Turn N — Gate B posts digest + auto-pick; sets `Gate B veto: none`; veto window Notes; ends turn. Turn N+1 — no veto → Notes/Run log **`Build armed`** → launch Build (re-read veto = none). If user says “stop — use Option 2” → set `Gate B veto: pending`; do not arm; stop or re-open Gate B.

### async-notify veto after Build started

Do not silently continue to review. Pause with **Decision N** ([handoffs.md](handoffs.md) shape):

| Option | What |
|--------|------|
| 1 | Discard draft; re-open Gate B with veto pick |
| 2 | Keep draft; re-open Gate B (amend design/tasks only) |
| 3 | Stop (Status `stopped`) |

**On re-open Gate B (Option 1 or 2):** set **`Gate B approved: none`**; clear Notes **Build armed** and veto-window tokens; card Next = `gate-b`; require a **fresh** Gate B digest + yes (or named pick) before Build. Do not reuse the prior approved token. Design-backloop Option 1 uses the same approved/armed reset but Next = `design-update` first ([stages.md](stages.md)).

## HITL Grill (independent of Gate B)

| Mode | Default Grill tier |
|------|--------------------|
| **full** | `async-notify` (prefer human-visible picks; blocking when auth/PII/schema forks) |
| **simple** | `auto` |

Do **not** copy Gate B tier into Grill unless `00-run.md` explicitly sets them equal. Domain rules: [grill.md](grill.md).

## Gate C test bar (before merge subflow)

| Review profile | Required |
|----------------|----------|
| **skip-review** | **Legal only** in **Mode simple** when Has API = **no** and Has DB = **no** ([lenses.md](lenses.md)). Then: Build **verify-pass** + Smoke section smoke-pass (no Smoke Task / full / lite required). Mode **full**, or Has API/DB = yes → skip-review **forbidden**; use lite/full bar. Smoke Task under skip-review: [verify-and-fix.md](verify-and-fix.md) ordered recovery |
| **lite** | `06-test-log.md` Result **success** after lite run |
| **full** | `06-test-log.md` Result **success** after full run |

Explicit user override may waive green tests; log override in Notes.

After Merge Result **success** **and** `merge` ∈ **Gate C approved** → set Status **`done`**. Subset without `merge` (e.g. PR only) → stay `paused`; leave Next for remaining actions. Abort/reject → `stopped`, not `done` ([results.md](results.md) · [stages.md](stages.md) Done criteria).

## Gate C approved actions (durable)

**Required when at Gate C / before merge:** record the user’s explicit yes as a durable field on `00-run.md`:

```markdown
**Gate C approved:** commit,push,pr,merge
```

| Value | Meaning |
|-------|---------|
| `none` | No Gate C yes yet (default until ask settles) |
| comma-separated subset of `commit` \| `push` \| `pr` \| `merge` | Actions the user named in this chat |

**Notes convention (optional but preferred):** one line referencing the yes, e.g. `Gate C yes — commit+push+pr+merge (chat HH:MM)`.

**Rules:**

- Do **not** invent actions. Subset only what the user named (“PR only” → `pr` or `commit,push,pr` as said).
- Merge Task / parent must re-read **Gate C approved** before git/remote actions.
- Lint: default `scripts/lint-run.py <run-dir>` errors when card Next=`merge` and **Gate C approved** is missing / `none` / empty. `--before-merge` enforces the same check explicitly (prefer before launching Merge).
)
