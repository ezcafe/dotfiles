---
name: code-simplification
description: >-
  Simplifies code for clarity without changing behavior. Use when refactoring
  for readability, reducing nesting or duplication, or cleaning code that works
  but is hard to maintain. Do not use for rewrites or unscoped drive-by edits.
---

# Code Simplification

Cursor-optimized adaptation of [addyosmani/agent-skills code-simplification](https://github.com/addyosmani/agent-skills/tree/main/skills/code-simplification). Goal: easier to read and change — not fewer lines.

## Project first

If the repo has `AGENTS.md` / `CLAUDE.md`, match its conventions (imports, naming, errors, types) before applying generic style.

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Preserve inputs, outputs, errors, side effects, and ordering. Run existing tests without modifying them to “pass.” |
| **Ask first** | Delete symbols you believe are dead; rename public APIs; touch code outside the current change scope. |
| **Never** | Change behavior to make code “cleaner.” Batch unscoped refactors into feature work. Optimize line count over clarity. |

## When not to use

- Code is already clear
- You do not yet understand why the code exists (Chesterton’s fence)
- Hot path where a “simpler” version is measurably slower
- Module is about to be rewritten anyway

## Process

### 1. Understand before touching

Answer before editing:

- What is this responsible for?
- Who calls it / what does it call?
- Edge cases and error paths?
- Tests that define expected behavior?
- Why might it look this way (perf, platform, history)?

If you cannot answer, read more context first. Use `git blame` / history only when the reason is unclear.

### 2. Spot signals (then fix one at a time)

| Signal | Move |
|--------|------|
| Nesting 3+ levels | Guard clauses or named helpers |
| Function 50+ lines / mixed jobs | Split with clear names |
| Nested ternaries | `if` chain, `switch`, or lookup map |
| Boolean flag params | Options object or separate functions |
| Same `if` in many places | Named predicate |
| Names like `data` / `tmp` / `usr` | Rename to content (`validationErrors`) |
| Comment that restates the next line | Delete the comment |
| Comment that explains *why* | Keep it |
| Duplicated 5+ lines | Shared helper |
| Unreachable / unused / commented-out | Remove only after confirm (ask if unsure) |
| Wrapper that adds nothing | Inline |

### 3. Apply incrementally

For each simplification:

1. Make one focused change
2. Re-run the relevant tests / typecheck
3. If green → continue; if red → revert that change and rethink

Prefer clarity over cleverness. Explicit beats dense one-liners that need a mental pause.

### 4. Balance (failure modes)

- **Do not** inline a helper that named a real concept
- **Do not** merge unrelated functions into one mega-function
- **Do not** strip abstractions that exist for testability or extension *and are in use*
- **Do not** chase line-count wins

### 5. Scope

Default to **recently modified** code. Unscoped simplification creates noisy diffs and regressions. If a refactor would touch 500+ lines, stop and propose automation (codemod) or split PRs — do not hand-edit that scale in one go.

### 6. Verify

- [ ] Same behavior for same inputs (tests unchanged and green)
- [ ] Build / lint clean for touched files
- [ ] Diff is reviewable; no unrelated churn
- [ ] Matches project conventions
- [ ] A new teammate would understand this *faster* than before

If the “simplified” version is harder to follow, revert.

## Related

- Before merge: [code-review-and-quality](../code-review-and-quality/SKILL.md)
- Spec/plan first: [myplan](../myplan/SKILL.md)
