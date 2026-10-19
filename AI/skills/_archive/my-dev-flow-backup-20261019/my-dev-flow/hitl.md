# HITL (index)

Canonical human-in-the-loop index for [`my-dev-flow`](SKILL.md).

| Concern | SoT file |
|---------|----------|
| Gate B defaults · async-notify · **Build armed** · **Gate B approved** · veto after Build | [hitl-gate-b.md](hitl-gate-b.md) |
| HITL Grill **default tier** (Mode → auto/async/blocking) | [hitl-gate-b.md](hitl-gate-b.md) HITL Grill |
| Grill **domain** (frontier, glossary, ADRs) + what each tier means for Grill | [grill.md](grill.md) |
| Gate C test bar · **Gate C approved** | [hitl-gate-c.md](hitl-gate-c.md) |
| Shared: Tiers · Provenance · Parent-only consent · Git | **this file** |

Pipeline order: [stages.md](stages.md). Resume/abort: [resume-abort.md](resume-abort.md). Decision **option shape:** [handoffs.md](handoffs.md). Max-round Decision **tables:** [invariants.md](invariants.md). Gate B veto-after-Build options: [hitl-gate-b.md](hitl-gate-b.md).

## Tiers

| Tier | Behavior | Allowed for |
|------|----------|-------------|
| **auto** | Approve without waiting. Gate digest + user-first picks. | Gate B (**Mode simple** low-risk only); HITL Grill |
| **async-notify** | Post digest + user-first pick. **Gate B:** end turn; Build on **next** parent turn after **Build armed** (veto window). **Grill:** continue immediately. Silence is **not** a veto. | Gate B (**narrow** — [hitl-gate-b.md](hitl-gate-b.md)); HITL Grill |
| **blocking** | Pause for approve / reject. Gate digest ≤4 bullets. | Gate B (**required** Mode **full**); **required** for Gate C; HITL Grill when needed |

## Parent-only consent (hard)

**Parent** writes these fields on `00-run.md` — **never** from Task returns / Task Write cells:

- **Gate B approved**
- **Gate C approved**
- **Build armed**
- All waiver kinds (`gate-c-test-override`, `smoke-waive`, `docs-only`, `smoke-pass (re-run)`, `card-override`)
- Matching **provenance** lines
- **clarity-check ok — \<Next\>** lines ([parent-next.md](parent-next.md))
- Run log **`parent consent write`** ack lines (when using consent snapshot)

**Same-turn habit (required):** After an **explicit user yes** in **this** parent turn, the **parent** records Gate C approved (and blocking Gate B approved) **in that same turn** — never by copying a Task’s claim that the user approved. Prefer Cursor **AskQuestion** / decision UI when available ([hitl-gate-c.md](hitl-gate-c.md) · [hitl-gate-b.md](hitl-gate-b.md)).

**Optional scratchpad:** Parent may draft consent in run-dir **`.consent.md`** (Tasks must **never** Write it — handoff ban). Durable lint still reads `00-run.md` fields; copy from `.consent.md` into `00-run.md` yourself. Local / do-not-commit unless your team wants it.

Tasks may **read** `00-run.md` to honor gates; they must **not** invent or set consent / waiver / provenance / clarity-check ok. Handoff base block forbids those writes ([handoffs.md](handoffs.md) · `handoff-for.py`).

### Consent write ban (machine check · M1)

**Habit (before / after every Task):**

1. Snapshot before launch — `preflight.py` **always** runs `--snapshot-consent` after `--next --derive`, **or** parent runs `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --snapshot-consent` → writes `.lint-consent-snap` (local / do-not-commit)
2. Launch Task
3. After Task: `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --check-consent-writes` (parent habit — [parent-next.md](parent-next.md))

**Machine path (fail-closed):** When `.lint-consent-snap` exists, `--next` / `--next --derive` **and** `--before-build` / `--before-merge` (also auto when card Next=`build`/`merge`) call the same check with missing-snap as no-op; **error** + `--next` → `do-not-launch` if Gate B/C approved, Build armed, provenance kinds, or waiver tokens changed **without** a new Run log line containing `parent consent write`. Standalone `--check-consent-writes` still **errors** when the snap is missing.

When the **parent** intentionally writes consent, append e.g. `- **HH:MM** · paused · gate-b · parent consent write — gate-b-approved` then re-snapshot (or accept the check after the ack line).

See [scripts/README.md](scripts/README.md) · [scripts/preflight.py](scripts/preflight.py).

## Provenance (required for consent / waivers)

Inventable tokens without a user quote are **rejected**. Before lint accepts **Gate B approved** (blocking), **Gate C approved**, Notes `gate-c-test-override`, Notes `smoke-waive`, Notes/Complexity `docs-only`, or Notes `card-override` (unsafe derive unlock), Notes or Run log **must** contain this fixed shape:

```markdown
- provenance — <kind> — user: "<exact user words>"
```

**Notes `smoke-pass (re-run)`:** bare Notes are **OK** for Mode **full** + Review profile **full** (E1 independent Smoke Result — [verify-and-fix.md](verify-and-fix.md)), **with** Smoke-stage evidence. Provenance `smoke-pass-rerun` is required **only** for the skip-review Gate C escape path (kind table below). Do **not** invent Notes without Smoke-stage evidence (Run log stage `smoke` and/or 06 updated after Last verify-pass at). Writing Notes `smoke-pass (re-run)` flips the consent fingerprint (waiver kind `smoke-pass-rerun`) — append Run log `parent consent write` (e.g. `parent consent write — smoke-pass-rerun`) when a snap exists ([smoke.md](../my-dev-flow-test/stages/smoke.md) After · [parent-next.md](parent-next.md)).

**Quote quality (required):**

1. Parent must copy the user’s words **verbatim**.
2. **Parent habit (not lint-enforced):** the quote should be a **verbatim substring of the latest user message in this parent turn**. Do not reuse quotes from older turns or invent plausible text. Lint cannot see chat history — it does **not** check substring binding.
3. **Lint (shape only):** accepts a quote only when length ≥ **12** characters and the normalized quote is **not** a known filler (`yes`, `ok`, `approved`, `merge`, `lgtm`, `ship it`, …). Short or filler-only quotes → treat as missing provenance.

| `<kind>` | When required |
|----------|---------------|
| `gate-b-approved` | HITL Gate B **blocking** and **Gate B approved** is `yes` / named pick (before Build) |
| `gate-c-approved` | **Gate C approved** is a non-empty action subset (before merge) |
| `gate-c-test-override` | Notes include `gate-c-test-override` (waive only with this line) |
| `smoke-waive` | Notes include `smoke-waive` (waive only with this line) |
| `docs-only` | Complexity/Notes `docs-only` escape under skip-review (bare token alone rejected) |
| `smoke-pass-rerun` | Notes `smoke-pass (re-run)` **escape under skip-review** only (bare token alone rejected there; Mode full + profile full E1 needs Notes + Smoke-stage evidence, **not** this provenance) |
| `card-override` | Notes `card-override — <reason>` unlocking unsafe card vs derived (merge/build/jump-ahead) |

Bare approved fields, waiver tokens, or card-override **without** matching quality provenance → lint **error** / `--next` → `do-not-launch` (exit **1**). Do **not** invent quotes.

**Honesty — provenance + lint are NOT consent proof:**

- Lint provenance checks **shape + quote quality only**. They are **not** proof the user said those words.
- They do **not** enforce latest-message substring binding ([anti-patterns.md](examples/anti-patterns.md)).
- Passing lint with a forged quote is still a process failure — treat provenance as a **cost raiser**, not machine-proof of chat speech.
- This skill system **cannot** implement chat-utterance verification without IDE/chat integration. Do **not** claim otherwise.
- **E1 dual-forge (Mode full + profile full):** Notes `smoke-pass (re-run)` **plus** inventing Run log stage `smoke` and/or touching `06-test-log.md` after **Last verify-pass at** raises cost and unlocks lint — it is **not** proof an independent Smoke Task ran. Same honesty class as Gate C provenance (cost raiser, not chat/process proof).

**Residual risk (overall):**

1. **Forged quotes:** length ≥12 + filler ban raises cost; does not prove utterance.
2. **Task consent writes:** handoff ban + `--check-consent-writes` raise cost; a Task that forges fields **and** a fake `parent consent write` Run-log line can still cheat.
3. **Async gap / AskQuestion:** preferred channels and sidecars raise cost; they are not cryptographic consent.
4. **E1 Smoke dual-forge:** Notes DONE + forged Run-log stage `smoke` / touched `06` Smoke section satisfy the machine gate; they do not prove a real independent Smoke Task (verify-and-fix.md E1).

## Gate digest

(1) what ships (2) top risks ≤3 (3) what verified (4) ask or auto-pick note / Gate C commit-push-PR-merge ask.

**User-first auto picks:** day-to-day user value first, then system convenience; log `auto-pick — Decision N Option K — user-first: …; system: …`.

## Git / remote (hard)

No `git commit` / `git push` / `gh pr create` / `gh pr merge` without explicit yes naming each action. Reject / silence at Gate C → stop. Gate B auto ≠ commit approval.

## Local sidecars (do not commit)

| File | Role |
|------|------|
| `.lint-async-gap` | Written by `--next` during async Gate B gap |
| `.lint-consent-snap` | Written by `--snapshot-consent` before Task |
| `.consent.md` | Optional parent-only consent scratchpad |

**Local only — do not commit** (unless team policy says otherwise for `.consent.md`). See [hitl-gate-b.md](hitl-gate-b.md) · [scripts/README.md](scripts/README.md).
