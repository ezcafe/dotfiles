## analyze — Analyze + Q&A (Architect) — High

**When:** Mode **full** (or standalone Analyze). Mode **simple** uses **design-phase** instead.

**Skills:** explore; if UI, `dev-decision-routing`.

**subagent_type:** `explore` or `generalPurpose`  
**model:** resolved High

**Done when:** `02-analysis.md` written with mandatory deep dive; builds on skim; honors Gate A / Design UI direction when Has UI.

**Mandatory deep dive** (feature + each major solution piece; ask user when unclear):

1. **What is this?** (align with Core problem)
2. **Why do we need this?**
3. **How to do this?** Other ways? Best practices?
4. **Solution branches** from Core problem: Quick wins / Systemic / Creative — Mode full required; Mode simple stub OK. Mark ★ priority; map to Design.

**Spike (optional):** throwaway exploration only — same What/Why/How; record findings in `02-analysis.md` Spike notes. Do not ship spike code.

**Task prompt:**

```
You are the Architect for my-dev-flow-design Analyze + Q&A. Fresh context only.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py analyze>

Read 01-idea.md (Gate A ok) and 02-skim.md.
When Has UI, explore how to implement within Gate A 80/20 and existing app chrome; do not invent a conflicting IA.
Explore the codebase for related patterns, APIs, schemas, and UI. Expand skim — do not ignore skim hard constraints.

If front-end work, read {dev-decision-routing}/SKILL.md.

Deep dive required — for the overall change and each major solution piece, fill in 02-analysis.md:
1. What is this? (plain words) — align with 01-idea Core problem / Problem map
2. Why do we need this? (outcome; cost of skipping) — use Consequences from Problem map when present
3. How to do this? List other ways. Note best practices (repo patterns first, then industry).
Also fill **Solution branches** (from Core problem):
- Branch 1 Quick wins (low effort, immediate)
- Branch 2 Systemic fixes (process / preventative / structural)
- Branch 3 Creative / lateral options
Mark ★ priority branch for this pass. Map branches to Design (full: Option 1/2 from systemic/creative; simple: one recommended; quick wins → early tasks or Non-goals if deferred).
Mode simple: one recommended branch + ≤2-line note on the other two (or `N/A — single clear path`).
If 2+ real approaches, use Decision N Option shape (What / Example / Pros / Cons / Recommendation).
Ask the user when any of these are unclear — do not guess.

Optional spike: throwaway exploration only to reduce uncertainty. Same What/Why/How before and after. Write Spike notes into 02-analysis.md. Do not leave findings only in chat. Do not treat spike as production Build.

Write 02-analysis.md (template) including Deep dive (+ Solution branches), **Design tree (frontier)** (Settled / Open frontier / Blocked), **Reusable patterns**, **System shape candidates**, and optional Spike notes.
Ask: “Are the instructions and reference files clear enough to design? Any gaps in What / Why / How?”

Also state whether this change touches public APIs / contracts (**Has API** yes/no), schema / migrations / persistence queries (**Has DB** yes/no), and auth / PII / schema trust boundaries (**Has auth/PII/schema** yes/no) so the parent can set 00-run.md.
Confirm or refine **Verify commands** (cwd, build, unit, e2e, or N/A + reason) for 00-run.md — see {my-dev-flow}/verify-and-fix.md.
State whether Grill should run: **yes** if Open frontier or unsettled Decisions remain; **no** if frontier already empty (simple clear asks).

Do not write production code. Do not finalize design yet.
Return: short summary + deep-dive highlights + open questions + Design tree summary + Grill recommended? + Has API/DB + Has auth/PII/schema + Verify commands.
```

**After:** Parent may answer Q&A, sets/refines **Has API**, **Has DB**, **Has auth/PII/schema**, and **Verify commands** in `00-run.md` from Analyze return, then **grill** (or skip per `{my-dev-flow}/grill.md`), then Design (or pause if blocked).

---
