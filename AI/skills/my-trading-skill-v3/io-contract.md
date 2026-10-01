# I/O Contract

## Input Schema

```typescript
interface AnalysisInput {
  symbol: string;                // e.g. "BTCUSD", "AAPL", "EURUSD"
  marketType: "spot" | "futures" | "fx" | "crypto" | "stocks";
  timeframe: string;             // e.g. "15m", "1h", "4h", "1d", "1w"
  ohlcv: Candle[];               // min 100 candles, recommended 300+
}

interface Candle {
  time: string;   // ISO 8601 format, e.g. "2026-04-14T00:00:00Z"
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
```

### Input Validation Rules

| Field | Constraint |
|---|---|
| `symbol` | Required, non-empty string |
| `marketType` | Required, must be one of the enum values |
| `timeframe` | Required, non-empty string |
| `ohlcv` | Required, minimum 100 candles; each candle must have all six fields; `high >= low` for every candle |

## Output Schema

```typescript
interface AnalysisOutput {
  primaryScenario: Scenario;
  alternateScenarios: Scenario[];   // at least one when plausible
  switchTriggers: SwitchTrigger[];
  analysisNotes: string;            // educational disclaimer + any data-quality notes
}

interface Scenario {
  patternFamily: PatternFamily;
  waveLabels: string;               // e.g. "1-2-3-4-5 (active: wave 4)"
  degree: string;                   // e.g. "intermediate", "minor"
  confidence: "high" | "medium" | "low";
  hardRuleChecks: HardRuleChecks;
  entryZone: PriceZone;
  slZone: StopZone;
  tpLadder: TpLevel[];
  invalidation: Invalidation;
  evidence: Evidence;
}

type PatternFamily =
  | "impulse"
  | "leading_diagonal"
  | "ending_diagonal"
  | "zigzag"
  | "double_zigzag"
  | "regular_flat"
  | "expanded_flat"
  | "running_flat"
  | "contracting_triangle"
  | "barrier_triangle"
  | "expanded_triangle"
  | "double_three"
  | "triple_three"
  | "truncation";

interface HardRuleChecks {
  wave2Boundary: RuleCheck;
  wave3Length: RuleCheck;
  wave4Overlap: RuleCheck;
}

interface RuleCheck {
  status: "pass" | "fail" | "not_applicable";
  evidence: string;   // e.g. "Wave 2 low at 42500, Wave 1 start at 42000 -- passes"
}

interface PriceZone {
  low: number;
  high: number;
  trigger: string;    // plain-language confirmation condition
}

interface StopZone {
  low: number;
  high: number;
  basis: string;      // e.g. "structural_invalidation_plus_atr_buffer"
}

interface TpLevel {
  name: "TP1" | "TP2" | "TP3";
  low: number;
  high: number;
  confidence: "high" | "medium" | "low";
  source: string;     // e.g. "wave3_161.8_extension + channel_upper_rail"
}

interface Invalidation {
  type: "rule_break" | "structural_relabel" | "level_loss";
  condition: string;  // e.g. "wave4_enters_wave1_territory"
  priceZone: { low: number; high: number };
}

interface Evidence {
  fibFit: string;                  // e.g. "wave2 at 0.618 retrace of wave1"
  channelFit: string;             // e.g. "wave4 near lower rail of 1-3 channel"
  indicatorConfluence: string[];  // e.g. ["ma_20_50_bullish_alignment", "rsi_divergence_at_wave5"]
  psychologyNote: string;         // e.g. "Wave 3 broad recognition phase; momentum strongest"
}

interface SwitchTrigger {
  condition: string;   // e.g. "close_below_42150"
  fromScenario: string;
  toScenario: string;
}
```

## Scenario States

| State | Meaning | Transition |
|---|---|---|
| `active` | Currently preferred scenario | -> `invalidated` on hard-rule break or key structural level loss |
| `watch` | Plausible but not triggered | -> `active` on breakout/reclaim + confluence confirmation |
| `invalidated` | Rules broken; discard | Terminal state for this scenario |

## Output Validation Rules

| Field | Constraint |
|---|---|
| `primaryScenario` | Required; must have all fields populated |
| `alternateScenarios` | At least one when structural ambiguity exists |
| `hardRuleChecks` | All three checks must be present; corrective patterns use `not_applicable` for impulse-specific rules |
| `tpLadder` | At least TP1; TP2 and TP3 when projectable |
| `invalidation` | Required; must specify a concrete condition and price zone |
| `analysisNotes` | Must include educational disclaimer |

## Human-Readable Output Template

When producing human-facing output, use this 7-point structure:

1. **Working count**: pattern family, wave labels, degree, and confidence
2. **Hard-rule checks**: pass/fail for each of the three impulse rules (or not_applicable for corrective)
3. **Entry zone**: price range + confirmation trigger
4. **SL zone**: price range + structural rationale
5. **TP ladder**: TP1 / TP2 / TP3 with confidence labels and sources
6. **Invalidation**: exact condition and price zone that breaks the count
7. **Scenario switch**: what event activates the alternate scenario

## Example Input

Minimum candle count relaxed to 10 for readability. Production inputs should have 100+ candles.

```json
{
  "symbol": "BTCUSD",
  "marketType": "crypto",
  "timeframe": "4h",
  "ohlcv": [
    {"time": "2026-04-01T00:00:00Z", "open": 82000, "high": 82500, "low": 81200, "close": 82300, "volume": 1200},
    {"time": "2026-04-01T04:00:00Z", "open": 82300, "high": 83800, "low": 82100, "close": 83600, "volume": 1800},
    {"time": "2026-04-01T08:00:00Z", "open": 83600, "high": 84200, "low": 83000, "close": 83200, "volume": 1500},
    {"time": "2026-04-01T12:00:00Z", "open": 83200, "high": 83500, "low": 82400, "close": 82600, "volume": 1100},
    {"time": "2026-04-01T16:00:00Z", "open": 82600, "high": 85500, "low": 82400, "close": 85200, "volume": 2800},
    {"time": "2026-04-01T20:00:00Z", "open": 85200, "high": 87000, "low": 85000, "close": 86800, "volume": 3200},
    {"time": "2026-04-02T00:00:00Z", "open": 86800, "high": 88500, "low": 86500, "close": 88200, "volume": 3500},
    {"time": "2026-04-02T04:00:00Z", "open": 88200, "high": 88600, "low": 86900, "close": 87100, "volume": 2000},
    {"time": "2026-04-02T08:00:00Z", "open": 87100, "high": 87500, "low": 86200, "close": 86500, "volume": 1600},
    {"time": "2026-04-02T12:00:00Z", "open": 86500, "high": 87200, "low": 86000, "close": 86800, "volume": 1400}
  ]
}
```

## Example Output

```json
{
  "primaryScenario": {
    "patternFamily": "impulse",
    "waveLabels": "1-2-3-4-5 (active: wave 4 in progress)",
    "degree": "minor",
    "confidence": "medium",
    "hardRuleChecks": {
      "wave2Boundary": {
        "status": "pass",
        "evidence": "Wave 2 low at 82400, Wave 1 start at 81200 -- Wave 2 did not retrace beyond Wave 1 start"
      },
      "wave3Length": {
        "status": "pass",
        "evidence": "Wave 1 = 2400pts, Wave 3 = 5900pts -- Wave 3 is not the shortest"
      },
      "wave4Overlap": {
        "status": "pass",
        "evidence": "Wave 4 low at 86200, Wave 1 high at 83800 -- no overlap"
      }
    },
    "entryZone": {
      "low": 86000,
      "high": 86500,
      "trigger": "Bullish reclaim above 86500 after Wave 4 retracement holds 38.2% of Wave 3"
    },
    "slZone": {
      "low": 83600,
      "high": 83900,
      "basis": "Below Wave 1 high (83800) which is the Wave 4 overlap invalidation boundary"
    },
    "tpLadder": [
      {
        "name": "TP1",
        "low": 89500,
        "high": 90200,
        "confidence": "high",
        "source": "Wave 5 at 61.8% extension of Wave 4 + channel upper rail"
      },
      {
        "name": "TP2",
        "low": 91000,
        "high": 92000,
        "confidence": "medium",
        "source": "Wave 5 at 100% extension of Wave 1 from Wave 4"
      },
      {
        "name": "TP3",
        "low": 93500,
        "high": 95000,
        "confidence": "low",
        "source": "Wave 5 at 161.8% of Wave 1 (extended scenario)"
      }
    ],
    "invalidation": {
      "type": "rule_break",
      "condition": "wave4_enters_wave1_territory",
      "priceZone": {"low": 83600, "high": 83800}
    },
    "evidence": {
      "fibFit": "Wave 2 at 0.50 retrace of Wave 1; Wave 4 near 0.382 retrace of Wave 3",
      "channelFit": "Wave 4 approaching lower rail of temporary 1-3 channel",
      "indicatorConfluence": ["ma_20_bullish_slope", "rsi_pulling_back_from_overbought"],
      "psychologyNote": "Wave 4 consolidation phase; expect complex/sideways behavior alternating with sharp Wave 2"
    }
  },
  "alternateScenarios": [
    {
      "patternFamily": "zigzag",
      "waveLabels": "A-B-C (active: wave C in progress)",
      "degree": "minor",
      "confidence": "low",
      "hardRuleChecks": {
        "wave2Boundary": {"status": "not_applicable", "evidence": "Corrective pattern -- impulse rules not directly applicable"},
        "wave3Length": {"status": "not_applicable", "evidence": "Corrective pattern"},
        "wave4Overlap": {"status": "not_applicable", "evidence": "Corrective pattern"}
      },
      "entryZone": {
        "low": 84000,
        "high": 84500,
        "trigger": "Bearish break below 86000 confirms corrective C-wave extension"
      },
      "slZone": {
        "low": 88800,
        "high": 89200,
        "basis": "Above Wave B high / Wave 3 peak area"
      },
      "tpLadder": [
        {
          "name": "TP1",
          "low": 83000,
          "high": 83500,
          "confidence": "medium",
          "source": "C equals A (1.0x) target"
        }
      ],
      "invalidation": {
        "type": "structural_relabel",
        "condition": "price_reclaims_88500_invalidates_bearish_C_wave",
        "priceZone": {"low": 88200, "high": 88500}
      },
      "evidence": {
        "fibFit": "If A completed, C at 1.0x A targets ~83200",
        "channelFit": "No clear channel for this corrective read",
        "indicatorConfluence": ["ma_20_flattening"],
        "psychologyNote": "If this is Wave A exhaustion misread as pullback, B trap may be in play"
      }
    }
  ],
  "switchTriggers": [
    {
      "condition": "close_below_83800_on_4h",
      "fromScenario": "impulse_wave4",
      "toScenario": "zigzag_C_wave"
    },
    {
      "condition": "close_above_88500_on_4h",
      "fromScenario": "zigzag_C_wave",
      "toScenario": "impulse_wave5_initiation"
    }
  ],
  "analysisNotes": "Educational analysis only. Wave 4 is tentative -- needs further price confirmation. If Wave 4 holds above 83800 (Wave 1 territory), impulse remains primary. Data sample is limited; production analysis should use 100+ candles for reliable pivot extraction."
}
```
