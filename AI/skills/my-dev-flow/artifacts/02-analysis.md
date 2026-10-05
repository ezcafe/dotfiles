Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md).

# 02-analysis.md

```markdown
# Analysis: <short title>

**Size:** Prefer bullets. ≤5 solution pieces. Spike ≤5 rows. Stay within artifact size caps.

## Deep dive (required)

Answer for the overall change. Repeat the three questions under **Solution pieces** for each major piece (API, schema, UI surface, integration, etc.). Ask the user when unclear — do not guess.

### Overall

#### What is this?
Plain words: the problem, surface, or change.

#### Why do we need this?
User/business outcome. What fails or hurts if we skip it.

#### How to do this?
Proposed approach in plain words. Originate from `01-idea` **Core problem** (and ★ priority).
- **Other ways:** at least one realistic alternative (or “none — constrained by X”).
- **Best practices:** repo patterns first, then industry norms.
- If 2+ real approaches: use Decision N + Option 1/2 (What it is / Example / Pros / Cons / Recommendation).

#### Solution branches (from Core problem)

Required for Mode **full**. Mode **simple:** one recommended branch + ≤2-line note on the other two (or `N/A — single clear path`).

| Branch | Options (bullets) | Effort / risk | Feeds Design? |
|--------|-------------------|---------------|---------------|
| **1. Quick wins** — low effort, immediate | | | yes / later / no |
| **2. Systemic fixes** — process / preventative / structural | | | yes / later / no |
| **3. Creative / lateral** — alternative approaches | | | yes / later / no |

- **★ Priority branch for this pass:** (usually matches idea mind-map ★)
- **Map to Design:** Mode full → Option 1/2 from systemic and/or creative; Mode simple → one recommended design. Quick wins → early tasks and/or Non-goals if deferred.

### Solution pieces

For each major piece:

#### <Piece name>

##### What is this?
-

##### Why do we need this?
-

##### How to do this?
- Approach:
- Other ways:
- Best practices:

## What exists today

1–3 sentences + key paths. (Build on `02-skim.md` when present — do not ignore skim constraints.)

## Dependencies

What else must change or stay compatible?

## Reference files (for Build)

| Path | Why it matters |
|------|----------------|
| | |

## Reusable patterns (prefer in Design)

Discover candidates here; **Design** expands chosen ones into teachable **Design patterns used** in `03-design.md`.

| Pattern / name | Where it lives | Why Design should reuse it |
|----------------|----------------|----------------------------|
| | | |

## System shape candidates (prefer in Design)

Discover architecture candidates here; **Design** expands into teachable **System design** in `03-design.md` (or marks `N/A`).

| Shape / concept | Where it lives (repo or known name) | Why Design should teach it |
|-----------------|-------------------------------------|----------------------------|
| | | |

## Constraints and risks

-

## Settled decisions (do not relitigate)

-

## Design tree (frontier)

Stub for **Grill** (`02b-grill.md`). Keep short.

### Settled
- (prerequisites already locked — Gate A, prior Decisions, repo constraints)

### Open frontier
- (askable now — prerequisites settled)

### Blocked
- (needs settled X first)

**Grill recommended?** yes | no — yes if Open frontier or unsettled Decisions remain; Mode full usually yes.

## Spike notes (optional)

Throwaway exploration only — not production Build. Same What / Why / How before and after.

| Spike | What / Why / How summary | Finding | Keep or discard |
|-------|--------------------------|---------|-----------------|
| | | | |

## Blocking questions

-

## Clear to grill / design?

yes | no — if no, list the gap:
```

---
