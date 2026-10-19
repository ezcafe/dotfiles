# Derive next (agent checklist)

Given Mode, Review profile, and artifacts under `.my-docs/workflow/<slug>/`, compute **expected Next**. If card Next disagrees → fix card or `card-override` + provenance ([preflight.md](preflight.md)). **`card-override` carve:** only for Next↔derive mismatch — **never** to skip unpaid `test-*` / Gate C test bar when Review profile is **lite** or **full** ([gate-c.md](gate-c.md)).

**Load path:** this file (Definitions + selector) + **one** half — [derive-next-pre.md](derive-next-pre.md) or [derive-next-post.md](derive-next-post.md). Do not open both halves in the same derive pass.

## Definitions (derive load path)

| Term | Literal meaning |
|------|-----------------|
| **`01a` file** | Prefer `01a-gate-a.md`. **Resume only:** if that file is absent, accept LEGACY `01a-idea-ui-review.md` as the Gate A Result ([artifacts/INDEX.md](artifacts/INDEX.md) · [CUTOVER.md](CUTOVER.md)). New runs write `01a-gate-a.md` only. |
| **`01a` ok** | The accepted `01a` file exists and Result = **`ok`**. |
| **Grill open** | `02b-grill.md` Result **`needs-round`**, **or** unpaid Grill (no `02b` **and** no Notes grill-skip) — [grill.md](grill.md). |
| **design artifacts** (Mode simple) | All present: `02-analysis.md` **and** `03-design.md` **and** `04-tasks.md` — **ignore** grill (`02b` / Notes grill-skip). |
| **Smoke unpaid** | Profile **skip-review** or E1 (Mode **full** × profile **full**): unpaid until independent Smoke per [verify.md](verify.md) Independent Smoke (SoT). Profile **lite** (Mode **simple** or Mode **full** + lite): Build-writes-Smoke matching smoke-pass may pay ([verify.md](verify.md) · [gate-c.md](gate-c.md)). |
| **Design present** | `03-design.md` exists. |
| **Isolated API/DB unpaid** | Has API=yes (not tiny) → `03a-api-contract-review.md` missing **or** Result ≠ **`clean`** (incl. **pending** / invalidated pre-amend or pre-upgrade **`clean`**). Has DB=yes (not tiny) → same for `03a-db-design-review.md`. Has=no or Notes `tiny-contract-tweak` → N/A (**skipped**). File presence alone does **not** pay when Result is unpaid/pending. |
| **Design clean** / **Verify clean** | Overall `03a-design-review-log.md` Result **`clean`** **and** isolated API/DB paid when required (not **Isolated API/DB unpaid**). Overall token alone is **not** enough when **Isolated API/DB unpaid**. **While Notes `design-backloop`:** only a **fresh** overall **`clean`** **and** fresh isolated **`clean`**\|**`skipped`** after this amend counts (Last stage `design-review` / `design-verify-phase` with Result **`clean`** after `design-update` + re-run API∥DB when unpaid — pre-amend **`clean`** is unpaid). **After Upgrade / while Notes `design-stale`:** Mode-simple or pre-upgrade overall **or** isolated **`clean`** does **not** count. After Notes `design-stale` clear (Mode-full `03` rewrite): Prefer re-run API∥DB while **Isolated API/DB unpaid** (**even if files exist**); only a **fresh** Mode-full overall **`clean`** counts — Last stage `design-review` (after API∥DB when required) with Result **`clean`** after that rewrite. |
| **design-review not clean** (Pre-Build) | **¬Design clean** — overall `03a-design-review-log.md` missing **or** Result ≠ **`clean`**, **or** **Isolated API/DB unpaid** (explicit; do **not** treat overall token alone as clean when isolated unpaid — [results.md](results.md) · [severity.md](severity.md)). **While Notes `design-backloop`:** also true when overall **or** required isolated Result is still a **pre-amend** **`clean`** (unpaid until fresh re-clean after this amend — parent invalidates overall + isolated on Amend; [design-backloop.md](design-backloop.md)). **While Notes `design-stale` (or after Upgrade until Mode-full re-clean):** also true when overall **or** required isolated Result is still a **pre-upgrade** / Mode-simple **`clean`** (unpaid — parent invalidates overall + isolated on Upgrade same as Amend; [step-0.md](step-0.md)). |
| **verify not clean** (Mode simple) | **¬Verify clean** — same predicate as **design-review not clean** (overall missing or ≠ **`clean`**, **or** **Isolated API/DB unpaid**; including unpaid pre-amend **`clean`** while Notes `design-backloop`, and unpaid pre-upgrade / Mode-simple overall **`clean`** while Notes `design-stale` or until Mode-full re-clean after Upgrade). |
| **overall Result** (Post-Build `05`) | **Derived on the derive load path** (do **not** require file-top to match before resume). Worst-of required section Results with order `needs fix` > `pending` > `clean`. **Not the same as Review clean** — may include Merged. **Profile full:** Adv + Quality section Results; when Lens plan **2+** and Merged is in scope for the current unpaid-check / advance, also Merged lenses section Result. **Profile lite:** Adv + Quality section Results (same inputs as full for those sections; file-top should match after `code-review-phase` but is never a substitute). **File-top may stay `pending`** after Adv/Quality (and until `merge-findings` when plan **2+**) — **do not** stall resume on file-top alone when required sections are already **`clean`**. Lite `code-review-phase` may set file-top; Adv/Quality/`merge-findings` need not. Same severity bar as [severity.md](severity.md). |
| **Review clean** | Profile ≠ skip-review **and** Adv + Quality section Results both **`clean`** (full and lite — section Results only; same bar as [results.md](results.md) · [artifacts/05-review-log.md](artifacts/05-review-log.md)). Does **not** require lenses **`clean`**, Merged **`clean`**, or file-top **`clean`**. Distinct from **overall Result** (which may include Merged when plan **2+**). |
| **Review needs fix** | Profile ≠ skip-review **and** Adv and/or Quality section Result = **`needs fix`** (not missing/pending). Prefer `fix-review` — not the unpaid Adv/Quality rows. |
| **code-review unpaid** | Profile ≠ skip-review **and** (planned Adv/Quality missing **or** Adv/Quality section Result missing/**`pending`** — not Result-bearing) — **exclude** **`needs fix`** (that is **Review needs fix**). Mirror **Lens plan unpaid** / Result-bearing: missing Result or **`pending`** is unpaid. |
| **code-review not clean** (Post-Build) | Profile ≠ skip-review **and** Adv+Quality ≠ **Review clean** — union of **Review needs fix** **or** **code-review unpaid**. Lenses are separate — not this predicate: **Lens plan unpaid** → Prefer unpaid `lens-*`; every planned Result-bearing **and** Merged unpaid/pending (plan **2+**) → Prefer `merge-findings`; plan **1** unpaid → Prefer that `lens-*`; dirty **`needs fix`** → Prefer `fix-review` Mode `merged-lenses` (plan **2+**) or Mode `plan-1-lens` (plan **1**) (**Lenses clean** still required before `test-*` / `gate-c`). |
| **Result-bearing** (planned `05-lens-*`) | Result is **`clean`** or **`needs fix`** only — **not** missing file, missing Result, or **`pending`**. |
| **Lens plan unpaid** | Lens plan ≠ **`none`** **and** some planned `05-lens-*` is **missing** **or** Result is missing/**`pending`** (not Result-bearing). **Excludes Merged** — Prefer `merge-findings` only when every planned `05-lens-*` is Result-bearing **and** Merged is unpaid/pending ([derive-next-post.md](derive-next-post.md) · [lenses.md](lenses.md)). |
| **verify-pass fresh for current Gate B settlement** | Last Verify = **`verify-pass`** **and** **Last verify-pass at** ≠ **`none`** **and** that ISO timestamp (Run-log local wall time — SoT clock below) is **same calendar minute or later** than the **expanded current Gate B settle token time** (below) — after a successful Build for that settle. Leftover verify-pass from a prior settle (or after Amend / Upgrade cleared settle) is **not** fresh → treat as unpaid (Pre-Build). Gate B unsettled (no settle token) → not fresh. |
| **Gate C unpaid** | **Gate C approved** is `none` / empty, **or** remaining named actions unpaid (approved non-empty but some of `commit` / `push` / `pr` / `merge` still not in the set — e.g. PR-only). Prefer `gate-c` until paid, or stop while Status `paused` / `done` / `stopped` ([derive-next-post.md](derive-next-post.md) · [gate-c.md](gate-c.md)). Do **not** treat non-empty approved alone as Prefer `merge` — require `merge` ∈ approved (+ provenance `gate-c-approved`). |
| **Tests success** | ≡ Gate C test bar met ([gate-c.md](gate-c.md) Test bar) — one definition; includes unpaid stale Notes cleared (`review-stale` / `test-stale`; skip-review: `review-stale` N/A cleared; `test-stale` cleared). |
| **Tests unpaid** | Profile ≠ skip-review **and** ¬(`06` Result **success** **and** **Test path last run** matches profile). Stale Notes (`review-stale` / `test-stale`) stay on earlier Post-Build rows ([derive-next-post.md](derive-next-post.md)) — do **not** fold into this term. |

## Gate B settled

| HITL Gate B | Settled when |
|-------------|--------------|
| **blocking** | **Gate B approved** set + provenance `gate-b-approved` |
| **async-notify** | durable **Build armed: yes** + Run log arm HH:MM later than digest + Notes `async-gap-pending — <digest-HH:MM>` ([gate-b.md](gate-b.md)) |
| **auto** | durable design-scoped Notes or Run log token `gate-b auto — <HH:MM>` (or digest) **after** current **Design clean** / **Verify clean** (Design-clean time below) + `Gate B veto: none` — **Gate B approved** may stay `none`. **Absence → Prefer `gate-b`** (fail-closed — not digest N/A alone). Parent at Prefer `gate-b` (auto): write the token same turn, then Prefer `build` (no user wait) — [gate-b.md](gate-b.md) |

**Settle freshness (all tiers — fail-closed):** a settle that does **not** post-date the current **Design clean** / **Verify clean** **and** the current Has set is **unpaid** → treat as **Gate B unsettled** (Prefer `gate-b`). Pre-flip or pre-Amend settle (approved / Build armed / `gate-b auto`) is unpaid even when the token fields look set — mirror [preflight.md](preflight.md) Always / Before Build · [gate-b.md](gate-b.md) Clear on Amend / Has flip · [lenses.md](lenses.md) Has flip.

**Design-clean time:** max expanded Run-log time among the stages that establish the current **Design clean** / **Verify clean**. Parent **MUST** same-turn append Run-log `- **HH:MM** · … · <stage-id> · …` on each paying `design-review` / `design-verify-phase` / required isolated `api-contract-review` / `db-design-review` that returns **clean** (or isolated **skipped** when that pays). Expand with the same SoT clock as settle / verify-pass (below). **Unresolved** (missing Run-log line for a required paying stage) → treat settle as unpaid / `blocked — Gate B settle stale` — do **not** invent a time.

**Has-flip Notes (required on every no→yes):** parent writes Notes `has-flip — <flags> — <HH:MM>` on every Has no→yes flip (`<flags>` = which Has flipped, e.g. `api` / `db` / `auth` / `api+db`). Expand with the same SoT clock. Missing Notes after a known no→yes flip → fail-closed unpaid until Notes written **or** settle cleared. This duty is **separate** from settle freshness lower-bound math below.

**Settle unpaid when** expanded settle token time is **earlier** than expanded **Design-clean time** (and the current Has set), **or** — **only when** a `has-flip — …` Note exists — earlier than the later of that Design-clean time and expanded latest **Has-flip** HH:MM. Has-flip is a lower bound **only** when such a Note exists; otherwise Design-clean (+ current Has set) alone. Same calendar minute or later = fresh (mirror verify-pass). Auto token must also clear this bar (not overall `03a` token alone when isolated unpaid).

**Current Gate B settle token time** (for freshness compare — use the token of the *current* settlement only):

| HITL Gate B | Settle token time |
|-------------|-------------------|
| **blocking** | Run log HH:MM (or ISO if recorded) of the turn that set **Gate B approved** + provenance `gate-b-approved` |
| **auto** | HH:MM in the current design-scoped `gate-b auto — <HH:MM>` (or digest) token |
| **async-notify** | Run log arm HH:MM when **Build armed: yes** was set for this settle |

**SoT clock (settle + Design-clean + has-flip + verify-pass):** Run-log **local wall time** — one zone for all sides. Do **not** mix UTC `Z` verify-pass with local settle / Design-clean / has-flip expansion.

**Settle expansion:** Expand HH:MM settle / Design-clean / has-flip tokens to `<Run-log calendar day of that turn>T<HH:MM>:00` (Run-log local wall time). Keep full ISO settle times as recorded **in the same local wall clock** (no UTC `Z` conversion).

**Freshness compare (verify-pass vs settle):** **Last verify-pass at** must be ISO-8601 **Run-log local wall time** (same zone as settle expansion — e.g. `2026-10-19T14:32:05`, **not** `…Z` unless Run-log/settle are also UTC, which they are not). Fresh when that timestamp is in the **same calendar minute** as the expanded settle instant, **or later**. Earlier minutes are not fresh. Same-minute counts as fresh so same-turn auto Gate B → Build → verify-pass is not stuck on HH:MM vs ISO seconds.

## Pre / Post selector

Pick **one** table; do not mix rows across Pre-Build and Post-Build in the same derive pass.

| Use | When | Open half |
|-----|------|-----------|
| **Pre-Build** (Mode full or simple) | No **verify-pass fresh for current Gate B settlement**, **or** Notes `design-backloop` (always Pre-Build while backloop — entry Prefer unpaid `design-update`; prior overall + isolated `03a*` **clean** unpaid until fresh re-clean), **or** Notes `design-stale` (always Pre-Build while stale — mirror backloop; Mode-simple `03` unpaid until Mode-full rewrite; prior overall + isolated `03a*` **clean** invalidated unpaid). | [derive-next-pre.md](derive-next-pre.md) |
| **Post-Build** | **verify-pass fresh for current Gate B settlement** **and** no Notes `design-backloop` **and** no Notes `design-stale`. | [derive-next-post.md](derive-next-post.md) |

**Backloop / stale carve:** Notes `design-backloop` **or** Notes `design-stale` → always **Pre-Build** (selector). Backloop entry Expected Next = Prefer unpaid `design-update` ([derive-next-pre.md](derive-next-pre.md)). **While Notes `design-stale`:** stay Pre-Build; run Mode-full **first-match** (Gate A / skim if unpaid, then Prefer unpaid `analyze` → `grill` → `design` — [derive-next-pre.md](derive-next-pre.md)). Do **not** Prefer API∥DB / `design-review` / `gate-b` / `build` while stale (prior overall + isolated `03a*` **clean** unpaid — parent invalidates on Upgrade). After Notes clear: Prefer re-run API∥DB while **Isolated API/DB unpaid** (**even if files exist**); **Design clean** only after Mode-full `design-review` (or API∥DB → `design-review`) **clean**. Do **not** open Post-Build on a leftover verify-pass earlier than the current expanded settle minute.

## Unsafe jumps (do-not-launch)

Always unsafe (no `card-override` waiver):

- Prefer / launch any stage while Status **`done`** \| **`stopped`** — Stop; do not Prefer ([derive-next-post.md](derive-next-post.md) · [resume.md](resume.md))
- Prefer / launch stages while Status **`paused`** and still waiting on user (Gate B/C AskQuestion open, async veto without arm, Grill blocking open) — stay paused ([resume.md](resume.md))
- `merge` unless **Tests success** **and** `merge` ∈ **Gate C approved** (+ provenance `gate-c-approved`) — PR-only / commit-only / **Gate C unpaid** → Prefer `gate-c` (ask remaining named actions) or stop while Status `paused` ([derive-next-post.md](derive-next-post.md) · [gate-c.md](gate-c.md)). Do **not** Prefer `merge` from non-empty approved alone.
- `merge` / `gate-c` while **¬Tests success** under profile **lite** or **full** — require **Tests success** (Gate C test bar — [gate-c.md](gate-c.md)): `06` Result **success** + Test path last run `lite`|`full` **and** unpaid stale Notes cleared (`review-stale` / `test-stale`). **`card-override` never** waives this bar.
- Legal **skip-review** Gate C / Prefer paid only when **Tests success** (Gate C test bar — [gate-c.md](gate-c.md)): **verify-pass** + independent **smoke-pass** per [verify.md](verify.md) Independent Smoke (SoT) **and** one escape Notes↔provenance (`smoke-pass-rerun` / `docs-only` / `smoke-waive` / `gate-c-test-override`) **and** unpaid stale Notes cleared (`review-stale` N/A cleared; `test-stale` cleared). Escape alone is **not** enough. Still no `card-override` for unpaid lite/full tests. Prefer-paid destination: [verify.md](verify.md) Prefer paid (`merge` \| `gate-c`).
- `test-full` / `test-lite` / `gate-c` while Lens plan **2+** or **1** and lenses not **clean** — **Lens plan unpaid** → Prefer unpaid `lens-*`; every planned Result-bearing **and** Merged unpaid/pending (2+) → Prefer `merge-findings`; unpaid (1) → Prefer that `lens-*`; **`needs fix`** → `fix-review` (or Prefer re-lens after Fix verify-pass) ([lenses.md](lenses.md) · [preflight.md](preflight.md))
- Review / test / `gate-c` / `merge` / `build` while Notes `design-backloop`
- `gate-b` while Notes `design-backloop` **and** design not re-clean (prior overall + isolated `03a*` **clean** unpaid — mirror Notes `design-stale`; allow `gate-b` only after fresh overall `03a` **clean** + isolated paid when required)
- Post-Build / review / test / `gate-c` / `merge` while Notes `design-stale` **or** while Last Verify looks like **verify-pass** but is **not** **verify-pass fresh for current Gate B settlement** (earlier than current expanded settle minute, or settle cleared on Amend / Upgrade — force Pre-Build)
- `gate-c` / `merge` while Notes `review-stale` or `test-stale` — under **skip-review**: `review-stale` is N/A (clear on Amend; do not Prefer review); `test-stale` → Prefer unpaid independent Smoke until cleared; Prefer paid only when stale Notes cleared ([verify.md](verify.md) Stale · [derive-next-post.md](derive-next-post.md))
- `build` while design-review not clean or Gate B unsettled (incl. settle freshness unpaid — pre-flip / pre-Amend settle does not pay)
- `api-contract-review` / `db-design-review` / `design-review` / `design-verify-phase` / `gate-b` / `build` while Notes `design-stale` (Mode-simple `03` unpaid; first-match stays Gate A / skim / analyze → grill → design)
- `design` / `design-review` / `design-verify-phase` / `gate-b` / `build` while **Grill open** (both Modes — never launch Design or review while Grill unsettled)
- `design-phase` while **Grill open** **and** (design artifacts present **or** `02b-grill.md` exists with Result **`needs-round`**) (Mode simple — Prefer `grill`; allow Prefer `design-phase` on Grill open **only** for true cold start: no `02b` **needs-round** **and** no design artifacts — [derive-next-pre.md](derive-next-pre.md))
- `gate-b` / `build` while 04a Result is **`needs more tests`** (re-`tdd-review` until **clean** or Notes `04a skipped`)
- Review/test stages while still pre-Build
- Profile-full-only stages (`adversarial`, `quality`, `test-full`) while profile lite (and inverse) — reclassify; do **not** unlock with `card-override`
- `test-full` / `test-lite` / `code-review-phase` / `adversarial` / `quality` while Review profile is still **skip-review**
- Any stage while Review profile is **skip-review** and Has API or Has DB or Has auth/PII/schema = **yes** — drop skip-review first ([preflight.md](preflight.md) · [lenses.md](lenses.md))

`card-override` + provenance applies **only** when card Next ≠ derive expected Next (mismatch carve) — not the bullets above.

## Max rounds

If Round / Verify attempts hit caps in [decisions.md](decisions.md) → Decision N; do not launch. Round ownership: [decisions.md](decisions.md) only.
