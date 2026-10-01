# Trade Framework

**Educational analysis only.** Output probabilities and scenario ranges, not certainty. Always report invalidation.

## Entry Types

### 1. Structure-Confirmed Entry

Wait for pattern completion before considering entry:

| Completion Signal | Example |
|---|---|
| Wave 2 completes in valid retracement zone | Wave 2 holds 61.8% of Wave 1; reversal candle confirms |
| Triangle E completes and breakout confirms | E terminates near angled support; close beyond triangle boundary |
| ABC completion with C exhaustion | C reaches fib target zone; momentum divergence appears |
| Diagonal completion with reversal | Ending diagonal Wave 5 prints divergence; wedge boundary breached |

### 2. Confluence-Confirmed Entry

Require at least 2-3 factors from:

- Rule-valid wave count
- Fibonacci reaction zone alignment
- Channel boundary reaction
- Momentum confirmation (RSI/MACD turn or divergence)
- Trend filter alignment (MA slope/crossover)

### 3. Breakout Entry

- For triangle and combination exits, prefer close-based breakout confirmation over intra-bar spikes.
- Avoid mid-structure entries inside choppy consolidation (flats, triple threes).
- Post-triangle thrust target: approximately the width of the widest part of the triangle.

## SL Zone Logic

| Component | Method |
|---|---|
| Structural stop | Place beyond the count invalidation point (preferred basis) |
| Volatility buffer | Optional ATR multiplier to avoid noise stop-outs |
| Combined formula | `stop = invalidation_level +/- max(structural_buffer, atr_mult * ATR)` |

### SL Placement by Pattern

| Pattern Context | Invalidation Reference |
|---|---|
| Wave 3 entry (after Wave 2) | Below start of Wave 1 |
| Wave 5 entry (after Wave 4) | Below start of Wave 4 (or Wave 1 territory boundary) |
| Post-triangle breakout | Below Wave E extreme |
| ABC correction completion | Beyond the point where C exceeds expected C-vs-A target materially |

## TP Zone Logic

Build TP zones from the active scenario family.

### Motive Continuation Targets

| Target | Source |
|---|---|
| Wave 3 projection | 161.8% or 261.8% extension of Wave 1 from Wave 2 pivot |
| Wave 5 projection | 61.8%, 100%, or 123.6% extension from Wave 4; also channel upper rail |
| Channel rail | Upper rail of temporary or complete impulse channel |

### Corrective Completion Targets

| Target | Source |
|---|---|
| C vs A multiples | 0.618, 1.0, 1.618 of Wave A (zigzag default: 1.0) |
| Extended flat C | 1.618 x Wave A, measured from start of B to end of C |
| Post-impulse C extension | 138.2% or 161.8% extension from A-leg |
| Prior pivot zones | Previous Wave 4 / Wave A / structural support-resistance |

### TP Ladder

| Level | Definition | Confidence |
|---|---|---|
| TP1 | Conservative confluence: nearest fib zone + channel rail intersection | Higher probability, smaller move |
| TP2 | Base-case confluence: primary fib target with structural alignment | Moderate probability |
| TP3 | Extended case: further extension zone or secondary fib target | Lower probability, larger move |

## Exit Triggers

| Trigger | Action |
|---|---|
| Structural invalidation | Full exit (hard rule broken or count relabeled) |
| Opposite high-confidence scenario activates | Full exit or reduce position |
| Momentum failure near target zone | Partial or full exit |
| TP1 reached | Consider partial exit |
| TP2 reached | Consider further partial exit |
| TP3 reached or exhaustion signals | Full exit |

## Output Template

When reporting trade framework results, use this structure:

1. **Entry zone**: `price_low -> price_high`
2. **Confirmation trigger**: plain-language condition that must be met
3. **SL zone**: `sl_low -> sl_high` + structural rationale
4. **TP ladder**:
   - TP1: price range + confidence label
   - TP2: price range + confidence label
   - TP3: price range + confidence label
5. **Invalidation trigger**: exact structural condition that voids the setup
6. **Scenario switch**: what event flips to the alternate scenario
