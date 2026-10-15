## gate-a — User-role day-to-day review (Medium)

**Role:** end user who would use this in day-to-day work (not PO, not architect).

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `User day-to-day review`

**Done when:** `01a-idea-ui-review.md` written with Result **ok** | **needs update** | **escalate**.

**Task prompt:**

```
You are an end user reviewing the product idea for day-to-day usage. Fresh context only — do not assume prior chat. You are NOT the Product Owner and NOT the Architect.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py gate-a>

Read only:
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

Write .my-docs/workflow/<slug>/01a-idea-ui-review.md using the template from {my-dev-flow}/artifacts/INDEX.md.
Fill all 80/20 sections and set **80/20 overall pass?** yes/no.

Set Result:
- **ok** — no Critical/Major gaps; **80/20 overall pass**; day-to-day checklist acceptable → parent will auto-approve Gate A
- **needs update** — Fix ask lists concrete changes to 01-idea.md
- **escalate** — only if unsafe, unethical, or too unclear without a human

Do not write code. Do not rewrite 01-idea.md yourself.
Return FIRST LINE exactly: Result: ok | needs update | escalate
Then short summary + path to 01a-idea-ui-review.md ({my-dev-flow}/results.md).
```

**After (parent):**

1. If Result **ok** → check **Gate A** in `00-run.md`; Run log `done · Gate A — ok · auto-approved`.
2. Confirm **Has UI** still matches `01-idea.md`.
3. Continue to **skim**.
4. If **needs update** → **ideation-update** → re-run Gate A (max 3). Then pause for human.
5. If **escalate** → pause for human.

---
