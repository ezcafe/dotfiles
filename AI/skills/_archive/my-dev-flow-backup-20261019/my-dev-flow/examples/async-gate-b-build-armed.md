# Golden path — Mode simple async-notify Gate B → Build armed

Short walkthrough of the one-turn gap. SoT: [hitl-gate-b.md](../hitl-gate-b.md) async-notify + Build armed · [stages.md](../stages.md) Simple pipeline.

## When

Mode **simple**, Has API=no, Has DB=no, **Has auth/PII/schema=no**, design-verify clean — Default Gate B prefers **auto** (seeded in template); this example switches to **async-notify** only after the user asks for a veto window ([hitl-gate-b.md](../hitl-gate-b.md) · E4).

## Ask

> Fix a one-line copy typo in a settings label — no schema, no API. Please give me a veto window before Build.

## Step 0 (abbrev)

- Mode **simple**, Review profile **lite** (or legal **skip-review**), Pending parallel **none**
- HITL Gate B starts **auto**; parent sets **async-notify** only with Notes `- async-notify requested — user: "Please give me a veto window before Build"`
- Gate B veto **none**; Gate B approved **none**; Gate C **blocking**
- Lint: `scripts/lint-run.py .my-docs/workflow/<slug>/`

## Parent before each Task (fixed)

1. Clarity boundary when Next ∈ clarity stages; log `clarity-check ok — <Next>`.
2. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py` launch pack)
3. `--snapshot-consent` before launch; `--check-consent-writes` after ([hitl.md](../hitl.md))
4. After any parent consent/waiver write (incl. **Build armed**): Run log `parent consent write — <kind>` → re-snapshot
5. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`

## Pipeline (Gate B → Build focus)

| # | Turn / stage | Action |
|---|--------------|--------|
| 1–3 | `design-phase` → `design-verify-phase` → (04a skip) | Clean design path (same as [simple-bugfix.md](simple-bugfix.md)) |
| 4a | **Turn N — Gate B async-notify** | Post digest + auto-pick. Set Notes `async-notify posted — veto window open until Build starts`. **Run log:** `- **14:00** · paused · gate-b · async-notify posted — veto window open`. Status **`paused`**. Card Next = `build`. Run `--next` → `do-not-launch` + `async-gap-pending — 14:00` (writes `.lint-async-gap`). **Copy** that pending line into Notes. Do **not** set **Build armed**. Do **not** launch Build this turn. End turn. |
| 4b | **Turn N+1 (or resume)** | No veto → append Run log **`Build armed`** with a **strictly later** timestamp (e.g. `- **14:05** · paused · gate-b · Build armed`) **and** `parent consent write — build-armed` → re-snapshot. Keep Notes `async-gap-pending — 14:00`. Re-read `Gate B veto` = `none`. Do **not** invent `parent turn gap observed` as a substitute. |
| 5 | `build` | Lint `--before-build` / `--next --derive` OK (turn-boundary gap). Launch Build. On start: Status `running`; clear veto-window + **Build armed** + pending token. verify-pass + Smoke section. |
| 6+ | review / test / Gate C / merge | Continue Happy path (simple) |

## Do not

- Launch Build in the **same** parent turn as the async-notify digest
- Invent `parent turn gap observed` (or same-turn dual HH:MM without prior `--next` pending token/sidecar) to fake the gap
- Treat silence as a veto
- Use **Gate B approved** as the arm token (async uses **Build armed**)
- Use async-notify on Mode **full** (always **blocking**)

## Parent habits

- Resume with Notes veto window open + Next `build` + veto `none` **is** the next parent turn — run `--next` if sidecar missing, copy `async-gap-pending`, append **Build armed** with a **later** HH:MM, then Build ([hitl-gate-b.md](../hitl-gate-b.md) Durable resume)
- Anti-patterns: [anti-patterns.md](anti-patterns.md) (same-turn Build · inventable gap · missing Build armed)
