# Preflight (agent checklist — replaces Python lint)

Run **before every Task**. Soft enforcement: stop and fix `00-run.md` / ask user when a check fails. Do **not** invent approvals to pass.

## Always

1. Card **Mode** / **Review profile** / **Status** match `00-run.md` body.
2. **Status** ∈ `running|paused|stopped|done` (not a stage id). Status **`done`** \| **`stopped`** → do **not** Prefer / launch stages ([derive-next-post.md](derive-next-post.md)). Status **`paused`** and still waiting on user (Gate B/C AskQuestion open, async veto without arm, Grill blocking open) → stay paused ([resume.md](resume.md)).
3. Mode × profile legal ([stages.md](stages.md) Forbidden).
4. **skip-review legality:** if Review profile = **skip-review**, Has API **and** Has DB **and** Has auth/PII/schema must all be **no** ([lenses.md](lenses.md)). If any Has = **yes** → drop skip-review → **lite** (or Decision N reclassify to full); set HITL Gate B **blocking**; **Mirror Amend settle clear:** **Gate B approved: none**; **Build armed: none**; clear veto-window / `async-gap-pending`; **clear** design-scoped `gate-b auto — <HH:MM>` (or digest) if present; Notes `has-flip — <flags> — <HH:MM>` ([lenses.md](lenses.md) Has flip · [gate-b.md](gate-b.md) · [derive-next.md](derive-next.md) Settle freshness); do-not-launch until card matches.
5. **Has = yes settle freshness:** when any Has = **yes** (API / DB / auth/PII/schema) — not only under skip-review — enforce [derive-next.md](derive-next.md) Settle freshness: clear unpaid pre-flip / pre-Design-clean settle; **separate duty** — require Notes `has-flip — <flags> — <HH:MM>` on every no→yes flip; Gate B unsettled until settle post-dates **Design-clean time** (+ current Has set) — has-flip HH:MM is a lower bound **only** when a `has-flip — …` Note exists (otherwise Design-clean alone); unresolved Design-clean Run-log → settle unpaid / stale (do not invent) ([lenses.md](lenses.md) Has flip · [gate-b.md](gate-b.md)).
6. Card **Next** matches [derive-next.md](derive-next.md) expected next — else fix card or Notes `card-override — <reason>` + provenance `card-override` (**mismatch carve only** — never waives unpaid lite/full test bar / illegal Mode×profile / illegal skip-review).
7. Compose handoff from [handoffs.md](handoffs.md) for `<stage-id>`; load only `stages/<id>.md`. **Parent-only carve:** when Next is `gate-b` or `gate-c`, skip handoff compose and `stages/<id>.md` — open [parent-next.md](parent-next.md) → gate file only ([gate-b.md](gate-b.md) / [gate-c.md](gate-c.md); [step-0.md](step-0.md) Load budget).
8. Soft-cap Open paths ≤2 ([parent-next.md](parent-next.md)).
9. After Task: read Result first line ([results.md](results.md)); **skip** when artifact-presence stage — check Done when / paths instead ([results.md](results.md) Artifact-presence stages · Parent habit); update card; on paying `design-review` / `design-verify-phase` / required isolated **clean** (or isolated **skipped** when that pays), same-turn Run-log `- **HH:MM** · … · <stage-id> · …` (Design-clean time SoT — [derive-next.md](derive-next.md) Settle freshness · [artifacts/00-run.md](artifacts/00-run.md)); on **verify-pass**, same turn set **Last Verify:** `verify-pass` **and** **Last verify-pass at:** `<ISO-8601 Run-log local wall time>` ([results.md](results.md) · [artifacts/00-run.md](artifacts/00-run.md) · [derive-next.md](derive-next.md) Freshness); **fail-closed** — do not advance while **Last Verify** = `verify-pass` **and** **Last verify-pass at** = `none`; bump Round / Run metrics ([decisions.md](decisions.md)). Parent-only consent fields unchanged by Task.

## Clarity boundaries

When Next ∈ `design-phase|analyze|grill|design|tdd-review|build|fix-review|fix-tests|merge`:

1. Open the matching clarity-check file (design or code subflow).
2. On pass, parent Notes: `clarity-check ok — <exact Next>`.
3. Fail → ask user; do not launch.

## Before design-review / design-verify / api|db-review

- Has API / Has DB / Has auth/PII/schema each `yes|no`.
- skip-review forbidden if Has API or Has DB or Has auth/PII/schema = yes ([lenses.md](lenses.md)).
- Mode full + both API+DB yes (not tiny): Pending parallel `api|db` while both Isolated API/DB unpaid (missing or Result unpaid/pending — Prefer re-run even if files exist); Next may be `api|db` or first Prefer — Pending authorizes both; Prefer only unpaid/pending sibling on resume; clear to `none` when both paid (`clean`\|`skipped`) ([lenses.md](lenses.md) · [derive-next.md](derive-next.md)).
- **Grill closed:** not **Grill open** ([grill.md](grill.md) · [derive-next.md](derive-next.md)) — Mode simple included. While Grill open and (design artifacts present **or** `02b` Result **`needs-round`**), card Next must be **`grill`** (Task or parent apply into `02b`; token stays `grill` until Grill closed); do-not-launch design-review / design-verify / api\|db-review.

## Before Build

- **Design clean** (Mode full) / **Verify clean** (Mode simple) — overall `03a` **`clean`** **and** isolated API/DB paid when required; overall token alone is **not** enough when **Isolated API/DB unpaid** ([derive-next.md](derive-next.md)).
- **04a bar:** `04a` Result **`clean`** **or** Notes `04a skipped` — reject `needs more tests` (re-`tdd-review` until clean/skip — [derive-next.md](derive-next.md) · [results.md](results.md)).
- **Grill closed:** not **Grill open** ([grill.md](grill.md) · [derive-next.md](derive-next.md)) — Mode simple included. While Grill open and (design artifacts present **or** `02b` Result **`needs-round`**), card Next must be **`grill`** (Task or parent apply into `02b`; token stays `grill` until Grill closed).
- **skip-review legality (fail-closed):** profile **skip-review** only when Has API=no **and** Has DB=no **and** Has auth/PII/schema=no. Any Has = **yes** → drop skip-review → lite\|reclassify **and** HITL Gate B **blocking** before Build ([lenses.md](lenses.md) · [stages.md](stages.md) Forbidden).
- `Gate B veto: none`.
- **Fail-closed Mode full:** if Mode = **full**, HITL Gate B **MUST** be `blocking` (reject `auto` / `async-notify`); else do-not-launch ([gate-b.md](gate-b.md)).
- **Fail-closed tier (Mode simple):** if Has API or Has DB or Has auth/PII/schema = **yes**, HITL Gate B **MUST** be `blocking` (not `auto` / `async-notify`); else do-not-launch ([gate-b.md](gate-b.md)).
- Blocking Gate B → **Gate B approved** set + provenance `gate-b-approved` ([gate-b.md](gate-b.md)).
- Auto Gate B (Mode **simple** low-risk only) → durable design-scoped Notes or Run log `gate-b auto — <HH:MM>` (or digest) **after** current **Design clean** / **Verify clean** (Design-clean time — [derive-next.md](derive-next.md) Settle freshness; absence → do-not-launch / Prefer `gate-b` — [gate-b.md](gate-b.md) · [derive-next.md](derive-next.md) Gate B settled).
- Async-notify (Mode **simple** low-risk only) → durable **`Build armed: yes`** + Run log arm HH:MM later than digest + Notes `async-gap-pending — <digest-HH:MM>` (veto window open and **Build armed** ≠ `yes` → do-not-launch).
- **Settle freshness (all Has = yes + Amend):** Gate B settle (approved / Build armed / `gate-b auto`) **MUST** post-date **Design-clean time** (+ current Has set); when a Notes `has-flip — <flags> — <HH:MM>` exists, also post-date that expanded has-flip minute — has-flip is a lower bound **only** when such a Note exists (Always #5 separate duty still requires the Note on every no→yes). A pre-flip or pre-Amend settle is unpaid → Gate B unsettled ([derive-next.md](derive-next.md) Gate B settled · Settle freshness · Always #5 · [lenses.md](lenses.md) Has flip · [gate-b.md](gate-b.md) Clear on…).
- No Notes `design-backloop`.
- No Notes `design-stale`.
- Verify commands set ([verify.md](verify.md)).

## Seed checklist

Run once when seeding or re-seeding `00-run.md` ([step-0.md](step-0.md)). Soft stop if any check fails.

1. Mode × Review profile legal ([stages.md](stages.md) Forbidden) — including skip-review only when all Has flags are **no**.
2. Mode **full** → HITL Gate B = **blocking** (never seed `auto` / `async-notify`).
3. Mode **simple** → HITL Gate B = **auto** only when Has API=no AND Has DB=no AND Has auth/PII/schema=no; else **blocking**.
4. HITL Gate C = **blocking**.
5. **Build armed** = `none`.
6. Required fields present: Status `running`, Mode, Review profile, Lens plan, Pending parallel, Gate B veto `none`, **HITL Gate B / Grill / C**, models, Verify commands (or placeholder until known).

## Before Smoke / Adv / Quality / code-review-phase / gate-c (Post-Build)

- **Last verify-pass at:** if **Last Verify** = `verify-pass` **and** **Last verify-pass at** = `none` → stop / fix card; do **not** Prefer or launch Smoke / Adv / Quality / code-review-phase / gate-c ([results.md](results.md) · [derive-next-post.md](derive-next-post.md)).

## Before Adv / Quality / code-review-phase

- Lens plan includes api/db when Has API/DB yes (unless tiny-tweak).
- Mode full + profile full → independent Smoke done **before Adv and before Quality** per [verify.md](verify.md) Independent Smoke (SoT). E1 FIRST also on Quality if Adv was skipped ([quality.md](../my-dev-flow-v2-review/stages/quality.md)).

## Before test-* / gate-c

- Lens plan **2+**: Merged lenses Result must be **`clean`**. Planned `05-lens-*` unpaid (missing or Result missing/**`pending`**) → do-not-launch; Prefer unpaid `lens-*` (**Lens plan unpaid**). Every planned Result-bearing (`clean` \| `needs fix`) **and** Merged unpaid/pending → do-not-launch; Expected Next `merge-findings`. Merged **`needs fix`** → do-not-launch; Expected Next `fix-review` (or Prefer re-lens after Fix verify-pass — [derive-next.md](derive-next.md)).
- Lens plan **1**: that planned `05-lens-*` (or Merged if parent copied) Result must be **`clean`**. Missing or Result missing/**`pending`** → do-not-launch; Prefer that `lens-*`. **`needs fix`** → do-not-launch; Expected Next `fix-review` (or Prefer re-lens after Fix verify-pass).
- Plan `none`: no lens gate.
- Profile **skip-review** → **Tests success** (Gate C test bar — [gate-c.md](gate-c.md); Independent Smoke SoT: [verify.md](verify.md)).
- Profile **lite** / **full** → Prefer / launch `gate-c` only when **Tests success** (`06` Result **success** + matching **Test path last run** + stale Notes cleared — [gate-c.md](gate-c.md) · [derive-next.md](derive-next.md) Definitions).

## Before Merge

- Confirm **Tests success** ≡ Gate C test bar only ([gate-c.md](gate-c.md) · [derive-next.md](derive-next.md) Definitions).
- Confirm `merge` ∈ **Gate C approved** (+ provenance `gate-c-approved`). Non-empty approved alone is **not** enough (PR-only / commit-only / **Gate C unpaid** → Prefer `gate-c` or stay `paused` — [derive-next-post.md](derive-next-post.md)).
- Do **not** treat success/path (or skip-review escape) as paid while unpaid `review-stale` / `test-stale` remain.

## Consent habit (parent-only)

Before Task: note current Gate B/C approved, **Build armed** (`none`\|`yes`), and waiver Notes.

After Task: confirm Task did **not** change those fields. Only parent writes them after explicit user yes — [hitl.md](hitl.md). After Build **verify-pass**, parent clears **Build armed** to `none` ([gate-b.md](gate-b.md) step 5); Task must not.
