# Market Psychology and Scenario Engine

## Psychology by Wave Position

## Impulse Psychology

- Wave 1: early reversal phase, low consensus.
- Wave 2: deep retracement, old-trend bias dominates.
- Wave 3: broad recognition, strongest participation.
- Wave 4: fatigue/consolidation, chop and traps increase.
- Wave 5: final push, divergence/exhaustion risk rises.

## ABC Psychology

- A: many traders treat it as a normal pullback.
- B: trap-prone leg (false confidence, fake breaks).
- C: decisive completion leg, often sharp.

## Scenario Engine

Always produce:

- Primary scenario
- At least one alternate scenario
- Explicit trigger to switch scenarios

## Scenario States

- `active`: currently preferred
- `watch`: plausible but not triggered
- `invalidated`: rules broken

## Transition Rules

- From `active` to `invalidated`:
  - hard-rule break or key structural level loss
- From `watch` to `active`:
  - breakout/reclaim + confluence confirmation

## Response Format

1. **Primary**: pattern, confidence, what confirms
2. **Alternate**: closest competing structure
3. **Invalidation**: exact break condition
4. **Switch trigger**: what flips preference
5. **Psychology note**: short narrative aligned to structure

## Anti-Bias Safeguards

- Do not let psychology override hard rules.
- Do not force certainty in prolonged ranges.
- Keep bullish and bearish framing symmetric.
