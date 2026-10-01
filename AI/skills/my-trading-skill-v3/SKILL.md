---
name: my-trading-skill-v3
description: >-
  Modular Elliott Wave analysis skill for AI agents: condensed rule tables,
  pattern identification, fibonacci targeting, confluence scoring, scenario
  emission with strict input/output contracts.
---

# Elliott Wave Analysis Skill (v3)

## When to Use

Use this skill when the user asks for:

- Elliott Wave counting or relabeling
- Pattern identification (impulse, diagonal, zigzag, flat, triangle, combination)
- Fibonacci target projection (motive or corrective)
- Entry/exit planning with invalidation and target zones
- Scenario branching (primary vs alternate counts)
- Wave degree or timeframe alignment

## First Principles

Apply in this order. Earlier levels override later ones.

1. **Hard rules** -- if violated, invalidate immediately and relabel.
2. **Structural identity** -- classify the wave family before measuring.
3. **Guidelines** -- probability tools (alternation, typical fib zones); failure alone does not invalidate.
4. **Confluence** -- fibonacci fit, channel fit, indicator alignment.
5. **Psychology** -- narrative must be subordinate to verified structure.

## Required Workflow

1. **Validate input** against `io-contract.md` schemas.
2. **Build wave hypothesis** -- identify pivots from OHLCV data and propose candidate segmentations.
3. **Apply hard-rule checks** from `core-rules.md` -- reject any candidate that fails a hard rule.
4. **Classify pattern family** using `pattern-library.md` -- match surviving candidates to known structures.
5. **Score confluence** using `fibonacci-map.md` and `confluence-and-psychology.md` -- rank candidates by multi-factor fit.
6. **Emit output** per `io-contract.md` -- primary scenario, at least one alternate, switch triggers, and analysis notes.

## Module Map

| Module | Purpose |
|---|---|
| `core-rules.md` | Hard rules, corrective gates, diagonal rules, truncation, extensions, degree hierarchy |
| `pattern-library.md` | Pattern identification tables for all families |
| `fibonacci-map.md` | Motive multiples, corrective C-vs-A, post-impulse ABC identification, retracement quick-ref |
| `confluence-and-psychology.md` | Alternation, channeling, psychology by wave position, indicator confluence |
| `trade-framework.md` | Entry/exit types, SL/TP zone logic, output template |
| `io-contract.md` | Input/output schemas, validation rules, inline JSON examples |
| `references.md` | Source links and attribution |

## Constraints

- Do not present outputs as financial advice. All analysis is educational.
- Mark labels as **confirmed** or **tentative** based on subdivision completeness.
- When two scenarios have similar validity, emit both as dual-count rather than forcing one.
- Never hide uncertainty. If data is insufficient, say so and list what confirmation is needed.
- Keep bull and bear framing symmetric -- apply the same structural logic in both directions.
