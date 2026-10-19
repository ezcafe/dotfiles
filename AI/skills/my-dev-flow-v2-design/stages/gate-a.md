## gate-a — User-role day-to-day review (Medium)

**Role:** end user who would use this in day-to-day work (not PO, not architect).

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `User day-to-day review`

**Done when:** `01a-gate-a.md` written with Result **ok** | **needs update** | **escalate**.

**Task prompt:**

```
You are an end user reviewing the product idea for day-to-day usage. Fresh context only — do not assume prior chat. You are NOT the Product Owner and NOT the Architect.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for gate-a>

Read only:
- .my-docs/workflow/<slug>/00-run.md
- .my-docs/workflow/<slug>/01-idea.md

Ignore technical design. Judge whether this idea would work in real daily use.

Also check **Problem map / Core problem** (product clarity, not engineering):
- Is the **Core problem** one clear sentence a real user would recognize?
- Does Outcome match the ★ top priority (when present)?
- Mode full: if Problem map is missing or Core problem is vague → Result **needs update** (Major).

**80/20 UI rule (required when the idea has UI)** — review and fill every section in the 01a template:

1. **Main user goals**
2. **Vital few**
3. **Core actions visually dominant** — Important info/action **#1** and **#2** always visible; secondary in menus/overflow/expand/modal
4. **Biggest usability problems first**
5. **Simplify**
6. **Top user journeys**
7. **Sensible defaults**
8. **Test, measure, repeat**

Also review for: convenience, easy to use, understanding, mobile usability (or n/a), eye reading flow.

Write .my-docs/workflow/<slug>/01a-gate-a.md using the template from {my-dev-flow-v2}/artifacts/INDEX.md (prefer `01a-gate-a.md`; do not create LEGACY `01a-idea-ui-review.md` on new runs).
Fill all 80/20 sections and set **80/20 overall pass?** yes/no.

Set Result:
- **ok** — no Critical/Major gaps; **80/20 overall pass**; day-to-day checklist acceptable → parent will auto-approve Gate A
- **needs update** — Fix ask lists concrete changes to 01-idea.md
- **escalate** — only if unsafe, unethical, or too unclear without a human

On re-entry after ideation-update: do **not** invent or bump **Round** — parent increments before re-launch (`{my-dev-flow-v2}/parent-next.md` · `{my-dev-flow-v2}/decisions.md`).

Do not write code. Do not rewrite 01-idea.md yourself.
Return FIRST LINE exactly: Result: ok | needs update | escalate
Then short summary + path to 01a-gate-a.md ({my-dev-flow-v2}/results.md).
```

**After (parent)** — mutually exclusive on Result (do **not** treat skim as unconditional):

### Read before you decide (show to user when human must act)

Paste this reading guide when Result is **escalate**, or at **max 3** needs-update (Decision N), or if the user asks to override Gate A. Paths under `.my-docs/workflow/<slug>/`.

**Must read (decision):**

1. `01-idea.md` — Core problem, Outcome, Problem map, Has UI
2. `01a-gate-a.md` — Result, Fix ask / escalate reason, 80/20 sections
3. `00-run.md` — Mode, Complexity, Has UI (spot-check)

**Skim if UI in scope:** Gate A 80/20 Vital few + Core actions (#1 / #2) in `01a-gate-a.md`.

**Decide:** re-run Gate A · override Result **ok** + Notes (explicit yes only) · stop. Never invent Result **ok**.

On Result **ok** (auto path): parent may one-line tell the user Gate A auto-approved and point at `01a-gate-a.md` if they want to spot-check — no pause required.

1. **ok** → check **Gate A** in `00-run.md`; Run log `done · Gate A — ok · auto-approved`; confirm **Has UI** still matches `01-idea.md`; continue to **skim**.
2. **needs update** → loop **ideation-update** ↔ Gate A until Result **ok** or round = 3. **Parent bumps Round** on `01a` before each re-launch ([parent-next.md](../../my-dev-flow-v2/parent-next.md)). Do **not** pause for human after every needs-update round — only at **max 3** (Decision N / raise cap) or on **escalate**.
3. **escalate** → pause for human immediately; set Next=`gate-a`; show **Read before you decide** above; exit for human-resolve. **Decision N** ([decisions.md](../../my-dev-flow-v2/decisions.md)): re-run Gate A · human override Result **ok** + Notes · Stop. **Resume only after Decision N + explicit user yes** — never invent Result **ok**. Then: re-run Gate A (**parent** bumps Round), **or** set Result **ok** + Notes (then skim). See `{my-dev-flow-v2}/results.md` · `{my-dev-flow-v2}/failure.md` · [gate-a-escalate.md](../../my-dev-flow-v2/examples/gate-a-escalate.md).

---
