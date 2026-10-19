## design-review (§1) — Design review (Verifier) — Medium

**When:** Mode **full** (after api-contract-review / db-design-review when flagged). Mode **simple** uses **design-verify-phase**.

**Generation ≠ verification:** you did not write this design. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Design review`

**Done when:** `03a-design-review-log.md` has overall Result **clean** or **needs update**. Mode **full** + Has API/DB **yes** (not tiny): matching `03a-*` must be Result **clean** (isolated stage ran) or Notes `tiny-contract-tweak` (fold — treat as skipped). **“No isolated file” alone is not skipped when Has=yes.** Has=no → Notes skip only (never invent empty `03a-*`).

**Task prompt:**

```
You are a Senior Architect verifier for my-dev-flow-v2-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find gaps; do not rewrite 01–04 yourself.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for design-review>

Read 00-run.md, 01-idea.md, 01a-gate-a.md if present (LEGACY fallback `01a-idea-ui-review.md` on resume only), 02-skim.md (if present), 02-analysis.md, 02b-grill.md (if present), 03-design.md, 04-tasks.md.
Also read project AGENTS.md / docs/ARCHITECTURE.md / GLOSSARY.md when present.
Follow useful bits from myplan, planning-and-task-breakdown, documentation-and-adrs, security-and-hardening (OWASP required), and UI skills when UI.

If Has API = yes and `03a-api-contract-review.md` is present (not Notes `tiny-contract-tweak` / skipped): read it. Do NOT deep-re-review API contracts; flag only cross-cutting gaps (e.g. tasks missing API acceptance). If that file is **needs update**, overall Result stays **needs update**. If Notes `tiny-contract-tweak`: fold light API checks here; do not require the isolated file.

If Has DB = yes and `03a-db-design-review.md` is present (not Notes `tiny-contract-tweak` / skipped): read it. Do NOT deep-re-review schema/migrations/queries; flag only cross-cutting gaps. If that file is **needs update**, overall Result stays **needs update**. If Notes `tiny-contract-tweak`: fold light DB checks here; do not require the isolated file.

Review against real-world best practices. Check at least:

Gaps / clarity
- Missing success criteria, non-goals, or open questions that still block build
- **Problem map missing or thin** — Mode **full:** `01-idea.md` must have Steps 1–2 (happening / missing / consequences → surface vs root → Core problem one sentence) + mind map with ★ priority; fail Major if skipped or hand-wavy. Mode **simple:** Core problem line or stub OK
- **Analyze deep dive missing or thin** — `02-analysis.md` must answer What / Why / How (other ways + best practices) for overall change and major solution pieces; Mode **full** also requires **Solution branches** (Quick wins / Systemic / Creative) tied to Core problem; fail Major if skipped or hand-wavy
- **Grill** — Mode full: `02b-grill.md` should be frontier-empty (or explicitly skipped with reason in Notes). Fail **Major** if Build-critical open frontier remains, or Design re-opens Settled grill decisions without new evidence. Mode simple: ok if grill skipped when frontier was empty.
- Spike notes (if any) must not contradict deep dive without explanation; spike must not be treated as shipped design without Design update
- Vague contracts (API/DB) or missing error / auth / ownership — if Has API and API section already reviewed, note “see API contract review”; if Has DB and DB section already reviewed, note “see DB design review”
- Sequence diagram missing actors, main path, or key failure returns
- Tasks too big, no acceptance, or no TDD “what turns red first”
- Missing or thin **System design** — heading required. Overview required when Has API or Has DB (or Mode full + new boundary); else `N/A` with reason OK. Fail **Major** if Overview required but missing/N/A wrongly, hand-wavy, invents a shape that conflicts with `docs/ARCHITECTURE.md` / skim without saying why, or **restates** sequence/contracts field-by-field. Fail **Enhancement** if name-drops without teaching when Overview is present.
- Missing or thin **Design patterns used** — heading required. Teach each pattern (What / How here / Why / Best practices + anti-patterns / Reference), or `N/A` with reason. Fail **Major** if invent-new when a repo pattern exists. Fail **Enhancement** if section only name-drops without teaching (Mode full + patterns claimed). Fail **Major** in Mode full when Analysis listed reusable patterns and Design skipped them without reason.
- Domain / ADR notes — if Design claims a hard-to-reverse surprising trade-off with no ADR and no “ADR skipped” reason → Enhancement (or Major when Has API/DB architecture fork)
- Skim hard constraints ignored
- Same concept dumped in both System design and Design patterns without saying which lens → Enhancement

Correctness / fit
- Conflicts with repo patterns, system architecture, or analysis reference files
- System design / Design patterns **Best practices** ignored by tasks (tasks contradict taught practices) → Major
- Design options ignore analysis Solution branches / alternatives without reason (Mode simple: one option + short rejected alternative is OK)
- Over-building vs idea outcome / Core problem; under-specified failure modes
- Data model / indexes / uniques that will hurt later — if Has DB and DB section reviewed, note “see DB design review” instead of duplicating

UI / UX / mobile (when UI is in scope)
- **Alignment only with Gate A / 01a / Design UI** — do NOT re-argue 80/20 goals if Gate A was ok
- Fail (Critical/Major) if 03-design layout/IA **drifts** from Gate A #1/#2 or Design UI locks when Has UI
- When Has UI: fail Major if Design/tasks lack clear UI locks for Build
- Loading / empty / error / success; skeleton parity; mobile ≥44px; no hover-only; a11y basics

Security / OWASP (design — light pass)
- Trust boundaries + abuse cases; OWASP table in `03-design.md` covers **design-time** risks (not code audit)
- Do not duplicate the full OWASP grid — spot gaps only; code OWASP is the **security lens** after Build
- Primary reference: https://owasp.org/Top10/

Improvements
- Concrete, practical suggestions

Write 03a-design-review-log.md (template: {my-dev-flow-v2}/artifacts/03a-design-review-log.md):
- Overall Result: clean | needs update — **clean only if** zero Critical/Major in this log **and** API/DB are clean|skipped when required: skipped = Has **no** (Notes skip) or Notes `tiny-contract-tweak`; when Has **yes** (not tiny) require isolated `03a-*` Result **clean** (stage ran). **Missing file alone ≠ skipped** when Has=yes ({my-dev-flow-v2}/severity.md)
- Findings table: Severity, Area, Finding, Suggestion
- Fix ask for my-dev-flow-v2-design: Critical/Major only; merge pointers to API/DB Fix ask files when those are open
- **Deferred Enhancements:** optional bullet list (do not block clean)
- Round notes
- **Round:** do **not** invent or bump — parent increments on re-entry (`{my-dev-flow-v2}/parent-next.md` · `{my-dev-flow-v2}/decisions.md`)

Rules:
- Clean only if zero Critical and Major (Enhancements → Deferred).
- Simple plain words.
- Do not edit 01–04. Do not write production code.
- Re-entry: leave **Round** for parent (parent also increments Run metrics `design-review rounds`).

Return FIRST LINE exactly: Result: clean | needs update
Then short summary + path to 03a-design-review-log.md ({my-dev-flow-v2}/results.md).
```

**After:** needs update → `design-update` → re-run from API contract review (when Has API **and** isolated file was required — not Notes `tiny-contract-tweak` / skipped) and/or DB design review (when Has DB **and** isolated file was required) → this stage. Parent bumps artifact **Round** (+ Run metrics) before each re-launch ([parent-next.md](../../my-dev-flow-v2/parent-next.md)). Tiny-tweak: re-run this stage only (folded checks). Max 3 → Decision N (`{my-dev-flow-v2}/decisions.md`). clean → continue (TDD → Gate B → Build verify-pass + Smoke section → then per [stages.md](../../my-dev-flow-v2/stages.md) Mode × Review profile / [verify.md](../../my-dev-flow-v2/verify.md) E1: **skip Smoke Task only when the table allows**; Mode **full** + profile **full** → independent Smoke first → review/test). Lens plan: may set **api**/**db** now when Has API/DB and **not** tiny-tweak; parent **must** finalize Lens plan api/db per `{my-dev-flow-v2}/lenses.md` **before code review** (may set earlier before Gate B).
