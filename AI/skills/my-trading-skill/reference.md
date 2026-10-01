# Elliott Wave — reference (classical + engine)

This document is self-contained. **Classical** = standard Elliott theory (guides linked at the end). **Engine** = the concrete detector defaults and behavior described here (configurable inputs with the stated defaults).

---

## Output contract (what to report)

When mapping or explaining wave-detector output, supply these fields whenever data allows:

| Field | Description |
|-------|-------------|
| **Current wave** | Which structure is active: booleans for `wave1`…`wave5`, `waveA`…`waveE`, plus `patternType` (`impulse` \| `leadingDiagonal` \| `endingDiagonal`) and corrective classification when present. Only one **primary** routed wave drives SL/TP merge. |
| **Open position or not** | See [Opening positions (engine vs trading policy)](#opening-positions-engine-vs-trading-policy). Raw engine `canOpenPosition` is **true** only on waves **1, 3, 5, A, C**. **Additionally**, for **wave 2** or **wave 4**, a **new** position is allowed **only** under the **SMA crossing policy** below (≥2 trend-direction crosses from the prior wave 1 or 3 start); then treat entry timing as the **start of the next motive wave (3 or 5)**. |
| **Volume** | Two meanings: (1) **Trading volume** = **order size** in lots/units (e.g. **0.01**, **0.03**), chosen by risk/account — report this when the user asks “how much to trade.” (2) **Bar / candle volume** on the chart: used only for the engine’s **relative volume guideline** (`volumeGuidelineSatisfied`) — baseline **20** bars, multipliers **1×** (waves 1, 5, A, C) and **2×** (wave 3) vs baseline — **not** the same as lot size. |
| **Stop loss** | Single merged `stopLoss` from the first detector in merge order that produced a value. |
| **Take profit** | Single merged `takeProfit`; optional **`takeProfitTargets`** array only from **wave 3, wave 5, or wave C** (same merge precedence for which array wins). |
| **Trend (`trendDirection`)** | `up` \| `down` \| `unknown` — see [Trend direction](#trend-direction). Not equivalent to “close vs last pivot.” |
| **Start price** | Price at the **start** of the current wave leg (pivot-derived). |
| **Start time / index** | **Bar index** in the input series at wave start (for SMA cross counts and logic); if **timestamps** align with bars, the same index maps to **wall-clock time**. |

Also exposed when applicable: `currentWaveRetracement`, `currentWaveTiming`, `currentWaveSmaCrossCount` (default SMA period **6** for crossings from wave start to current bar in trend direction), `validation` checklist, channel lines, `waveDegree` from timeframe mapping, alternation and corrective typing.

---

## Opening positions (engine vs trading policy)

### Raw engine flag

- **`canOpenPosition`** is **`true`** only when the **routed** active wave is **1, 3, 5, A, or C** (not **2, 4, B** in the default merge).

### Trading policy — new positions on **wave 2** and **wave 4** (SMA confirmation)

When the count still places price in **wave 2** (corrective after wave 1) or **wave 4** (corrective after wave 3), **do not** open a **new** position **unless** all of the following hold:

1. **Anchor window** — Measure from the **start of the preceding motive wave**: **wave 1 start** while analyzing wave 2; **wave 3 start** while analyzing wave 4 (same bar index / time as the engine uses for “wave start” for that leg).

2. **Trend direction** — Use `trendDirection` (**up** / **down**). If **`unknown`**, do not use this rule until trend is defined.

3. **SMA crossings (trend-aligned)** — Count closes crossing the configured SMA (**default period 6**, same family as `currentWaveSmaCrossCount`):
   - **Uptrend**: count **upward** crossings (price crosses **up** through the SMA).
   - **Downtrend**: count **downward** crossings (price crosses **down** through the SMA).

4. **Threshold** — Require **at least 2** qualifying crossings **from that anchor** through the current bar.

5. **Interpretation** — When the threshold is met, you may **open a new position** and treat the **operational start** of the next leg as **wave 3** (following wave 2) or **wave 5** (following wave 4): i.e. entry timing aligns with **commencing the next motive wave**, not a discretionary add in the middle of a corrective without confirmation.

**Note:** If the raw detector still flags `wave2`/`wave4` while this policy is satisfied, explain both: **structure** may still show corrective until pivots update; **trading** may allow entry under this rule. The engine flag alone may remain `false` on wave 2/4 — this policy is an **explicit overlay** for execution.

### Volume terminology

| Term | Meaning |
|------|--------|
| **Trading volume** | **Position size** — lots or units per order (e.g. **0.01**, **0.03**). Stated explicitly when sizing risk. |
| **Bar volume** | **Candle volume** — liquidity printed on each bar; feeds `volumeGuidelineSatisfied` vs a baseline SMA, **not** lot size. |

---

## Rules vs guidelines (classical)

| Kind | Meaning |
|------|---------|
| **Rules** | Must hold; count invalid if any rule fails |
| **Guidelines** | Probabilistic; improve confidence when satisfied |

---

## Engine defaults vs classical (authoritative numbers)

Configurable via detector input; defaults below.

| Topic | Classical / textbook | **Engine (defaults)** |
|-------|------------------------|------------------------|
| Wave 2 retracement (1–2 pattern) | Often 38.2–61.8%; max ~70% | **33%–70%**; live wave 2 uses **OHLC extremes** since wave 1 end — wicks beyond max retracement invalidate |
| Wave 4 retracement vs wave 3 | Often 38.2–61.8%; max ~70% | **33%–70%**; extremum over bars after wave 3 pivot through current |
| Wave 2 duration vs wave 1 | — | **33%–75%** of wave 1 bar count; wave 2 duration ≤ **10×** wave 1. Checked in **`timeRatioValid`** when **point count ≥ 6** and wave 2/3/4/5 context applies |
| Wave 4 duration vs wave 3 | — | **33%–75%**; wave 4 ≤ **10×** wave 3; folded into **`timeRatioValid`** when **`isWave4` or `isWave5`** (pivot window uses **L−6…L−1** semantics) |
| Higher-degree wave 2 (ABC after completed 1–5) | Depth often 38.3–61.8%; max ~70% | **Depth** (extremum since wave 5 end vs full 1–5 length) in **33%–70%**. **Also** correction duration / full 1–5 duration **33%–75%**. **Either** failing rejects ABC-as-higher-degree-wave-2 |
| Leading diagonal | Wave 4 overlaps wave 1 | Routed on **wave 4** branch when impulse rule 2 fails (overlap) but **leading diagonal** validation passes → `patternType: 'leadingDiagonal'`; overlap allowed |
| Ending diagonal | Wave 5 path | When overlap on wave 5 path → `patternType: 'endingDiagonal'` |
| Duration hint | — | **`leadingDiagonalDurationHint`**: live wave 2 or wave 4 **timing** strictly **greater** than max time ratio (default **0.75** of prior leg) — soft hint only; does not change pattern type or relax `timeRatioValid` |
| Wave 3 | Not shortest | Price: wave 3 ≥ wave 1 and ≥ wave 5; duration similarity via wave-3-not-shortest logic (~20% / ~25% tolerances) |
| Metrics | — | `currentWaveSmaCrossCount` with default SMA **6**; optional volume guideline |

**Debug / log labels vs narrative pipeline**

| Log label (engine) | Narrative pipeline phase |
|--------------------|--------------------------|
| Step 5 | Corrective pass (after completed impulse) |
| Step 6 | Impulse routing (5, 3, A, 4 [+ leading diagonal fallback], 2) |
| Step 7 | Wave 1 fallback |
| Step 8 | Validation / final assembly |

---

## Foundations (classical)

- **Motive**: 5-wave structures with the trend. **Corrective**: typically 3-wave against the trend.
- **Fractal**: smaller TF 1–5 can be one wave of a larger degree.
- **Higher degree**: completed 1–5 → wave **1** of next degree; following ABC → **wave 2** of that degree (“big wave 2”), subject to depth/time gates above.

---

## Impulse wave rules (inviolable)

| Rule | Statement |
|------|-----------|
| Wave 2 | Never beyond origin of wave 1 (retracement &lt; 100%) |
| Wave 4 | Never enters **price territory** of wave 1 |
| Wave 3 | ≥ wave 1 and ≥ wave 5 in price; time rules when legs similar or when one leg clearly longest / shortest — two shorter legs should match in length and duration |
| Structure | Five subwaves |
| Waves 1,3,5 | Motive sub-structures |

## Impulse guidelines (classical)

- Often one extension; most often **wave 3**.
- Wave 2: zigzag, flat, combination — **not** a full triangle.
- Wave 4: zigzag, flat, combination, or **triangle**.
- Alternation of depth/character between wave 2 and wave 4 is common.

---

## Leading diagonal (classical + engine)

- Motive but not normal impulse; wave 4 may overlap wave 1.
- Structures **3-3-3-3-3** or **5-3-5-3-5**.
- Engine: on **wave 4** branch, if retracement OK but **overlap** → test leading diagonal; if valid → `wave4: true`, `patternType: 'leadingDiagonal'`.
- **`leadingDiagonalDurationHint`** does not by itself select the pattern.

## Ending diagonal (classical)

- Wave **5** or wave **C**; exhaustion; 1–4 overlap; wave 3 ≥ wave 1 and ≥ wave 5.

---

## Corrective waves (summary)

- Zigzag **5-3-5**; Flat **3-3-5**; Triangle **3-3-3-3-3** (only positions **4, B, X, Y** classically — not wave 2 or A as full triangle).
- Double three **W-X-Y**; triple **W-X-Y-X-Z**.
- **Higher-degree wave 2** after 1–5: net ABC depth and duration ratios must pass engine gates (see defaults table).

---

## Fibonacci retracements (classical targets)

| Wave | Typical % of prior leg |
|------|-------------------------|
| 2 | 38.3%, 50%, 61.8%; must not exceed 70% classically in many treatments |
| 4 | Often 38.2–61.8% of 3; max ~70% |
| Big wave 2 | Often 38.3–61.8% of big wave 1; max ~70% |

## Wave 3 take-profit selection (engine) from wave 2 depth

- If wave 2 retracement ≈ **38.2% or 50%** (±2%): TP targets **161.8%** and **261.8%** of wave 1 from wave 2 end.
- If ≈ **61.8%** (±2%): single conservative TP at **100%** of wave 1 from wave 2 end.
- Otherwise in band but outside tight bands: default **100%** of wave 1.

**Fib constants used**: retracements **0.382, 0.5, 0.618**; extensions **1.618, 2.618** for wave 3 TPs. Wave 4 SL uses **0.618 × |wave 3|** from wave 3 end.

---

## Engine SL/TP by detected wave (then merged)

**Merge precedence** for both `stopLoss`/`takeProfit` and for `takeProfitTargets` (targets only from wave **5**, **C**, **3**):

`wave5` → `waveC` → `waveB` → `wave3` → `waveA` → `wave4` → `wave2` → `wave1` → `triangle` → `doubleThree` — **first defined wins**.

| Route | Stop loss anchor | Take profit (primary) | Extra `takeProfitTargets` |
|-------|------------------|------------------------|---------------------------|
| Wave 3 | End of wave 2 (prior pivot) | Per wave-2 depth rules from wave 2 end ± wave 1 × extension | Same as primary: one or two levels |
| Wave 4 | 61.8% retracement of wave **3** from wave **3 end** | From wave **4 extreme** by **\|wave 3\|** in trend direction | — |
| Wave 5 (impulse) | Wave 4 end | From wave 4 end by **baseLength**: if wave 3 extends (≥ extension min × wave 1) use **wave 1** length; else if wave 1 ≈ wave 3 (~20%) use **wave 1 + wave 3**; else **min(wave 1, wave 3)** | **100% w1**, **100% w3**, **61.8% × (w1+w3)** from wave 4 end |
| Wave 5 (ending diagonal) | Wave 4 end | From wave 4 by **min(wave 1, wave 3)** | — |
| Wave 2 | 61.8% retracement of wave 1 from wave 1 end | From wave 2 **extremum** by wave 1 length | — |
| Wave 1 (fallback) | Last significant pivot | Pivot ± **1.618 ×** prior segment | — |
| Wave A | End of prior wave 5 | **38.2%** of total impulse length from wave 5 end, against impulse direction | — |
| Wave B | Wave 5 end (origin of correction) | **100% of wave A** from wave A end | — |
| Wave C | Wave B end | First target **100% of A** from B end | **100% A**, **61.8% A**, **161.8% A** from B end |
| Triangle | Wave E | Wave E ± length of wave A | — |
| Double three | X end | Y end ± length of W | — |

---

## Pipeline (narrative steps) — overview

**Minimum bars**: **50** candles. **MACD** defaults: fast **12**, slow **26**, signal **9**.

1. **Input validation** — OHLC aligned lengths, sanity checks.
2. **MACD** on closes.
3. **Significant points** — MACD/signal crossovers; map to bar high/low; true high/low between crosses.
4. **Pattern flags** — Four overlapping 1–2 triples: **recent** `[L−3,L−2,L−1]`, **o1** `[L−4,L−3,L−2]`, **o2** `[L−5,L−4,L−3]`, **o3** `[L−6,L−5,L−4]`. Uptrend: Low → High → Higher Low in retracement band; downtrend: inverse.
5. **Completed 5-wave impulse search** — Six pivots; rules; reversal after wave 5.
6. **Correctives** (if impulse completed) — Order: triangle if points after ≥5; double three if ≥3; wave C if ≥2; wave B if ≥1. **Logged as engine Step 5.**
7. **Impulse routing** (if no corrective) — First match among 5, 3, A, 4 (+ leading diagonal inside 4), then 2; wave 1 **not** here. **Critical:** wave **2** detector **skipped** when **`recent` OR `o1`** is true. **Logged as engine Step 6.**
8. **Wave 1 fallback** — `prevMove` > 0; `moveRatio` = |current−L−1|/|L−2−L−1| ≥ **0.3**; move opposes prior leg. **Engine Step 7.**
9. **Validation** — Full validation object; channels; optional volume; SMA crossings. **Engine Step 8.**
10. **Trend direction** — See below.
11. **SL/TP merge** — Precedence table above.

### Impulse routing table (when step 6 corrective did not fire)

| Condition | Route |
|-----------|--------|
| `recent && o2 && points ≥ 6` | Wave **5** or **ending diagonal** (if 4–1 overlap on extremes) |
| `recent && !o2 && points ≥ 3` | Wave **3** (needs price resumed past wave 2 end in wave-1 direction) |
| `!recent && o1 && o3 && points ≥ 6` | Wave **A** — requires a **validated completed impulse** in the structural search (not flags alone): wave 2 in band, wave 3 not shortest, **wave 4 no overlap with wave 1**, reversal after wave 5 |
| `!recent && o1 && !o3 && points ≥ 5` | Wave **4** or **leading diagonal** (overlap + diagonal valid) |
| Else if `!recent && !o1 && points ≥ 2` | Wave **2** (extremum vs wave 1 since wave 1 end) |

---

## Trend direction

Computed **after** wave-2 flag known; **first match wins**:

1. If **recent** pattern detected → `trendDirection = recent.trend` (`up`/`down`).
2. Else if **o1** detected → `trendDirection = o1.trend`.
3. Else if **isWave2** and ≥2 points → compare L−1 vs L−2 (up if L−1 > L−2).
4. Else → `unknown`.

Trend **does not** auto-flip to `unknown` merely because price later trades through an older pivot.

---

## Validation checklist (engine)

**Impulse**

- [ ] Wave 2 ≤ 100% of wave 1
- [ ] Wave 4 does not enter wave 1 territory (unless diagonal typing)
- [ ] Wave 3 not shortest vs 1 and 5
- [ ] Overlap rules per pattern type
- [ ] `fibBoundsRespected`, `timeRatioValid` when applicable
- [ ] `leadingDiagonalDurationHint` optional
- [ ] `wave2NotTriangle` helper
- [ ] `zigzagValid` / `flatValid` when correctives typed
- [ ] `volumeGuidelineSatisfied` optional

---

## Foot-guns (read before debugging)

- **Narrative steps 1–11** vs **engine log steps 5–8** — use the mapping table at top.
- **`trendDirection`** is **not** “from last pivot to close.”
- **Wave 2** detector **not run** when `recent || o1` — can fall through to **wave 1** while **recent** still drives trend.
- **Wave 2/4 entries:** engine `canOpenPosition` may be **false**; the **SMA ≥2-cross policy** is a separate **trading** rule for allowing new risk **into** wave 3/5 starts.
- **Wave A** requires **structurally completed impulse**, not only pattern flags.
- **Higher-degree wave 2** ABC: depth **and** time ratio must pass.

---

## Market psychology (classical shorthand)

| Wave | Character |
|------|-------------|
| 1 | Hard to spot; overlap |
| 2 | Deep retrace; doubts |
| 3 | Strong, often largest |
| 4 | Complex; alternation |
| 5 | Exhaustion; divergence possible |
| A | Looks like pullback |
| B | Trap / fake breakout |
| C | Strong, often 100–161.8% of A |

---

## References (external links only)

### Elliott Wave guides (XForceGlobal, TradingView)

- [A Comprehensive Guide to Elliott Wave Rules & Guidelines](https://www.tradingview.com/chart/BTCUSD/xepjxoEQ-A-Comprehensive-Guide-to-Elliott-Wave-Rules-Guidelines/)
- [A Comprehensive Guide to Elliott Wave Degrees (Timeframes)](https://www.tradingview.com/chart/BTCUSD.P/3l5vxtVK-A-Comprehensive-Guide-to-Elliott-Wave-Degrees-Timeframes/)
- [A Comprehensive Guide to Fibonacci Retracements](https://www.tradingview.com/chart/BTCUSD/MHHrzCLA-A-Comprehensive-Guide-to-Fibonacci-Retracements/)
- [A Comprehensive Guide to Fibonacci Retracements (Updated)](https://www.tradingview.com/chart/BTCUSD/tjvjD6Bc-A-Comprehensive-Guide-to-Fibonacci-Retracements-Updated/)

### Elliott Waves Complete Guide (XForceGlobal, TradingView)

- [Chapter 1 – The Overall Cycle](https://www.tradingview.com/chart/BTCUSD/921d0JS9-Elliot-Waves-Complete-Guide-Chapter-1-The-Overall-Cycle/)
- [Chapter 2.1 – Motive Waves (Impulse, Leading Diagonal)](https://www.tradingview.com/chart/BTCUSD/FsD8jcsW-Elliot-Waves-Complete-Guide-Chapter-2-1-Motive-Waves/)
- [Chapter 2.2 – Ending Diagonal](https://www.tradingview.com/chart/BTCUSD/z7j2g1rH-Elliot-Waves-Complete-Guide-Chapter-2-2-Ending-Diagonal/)
- [Chapter 2.3 – Extensions](https://www.tradingview.com/chart/BTCUSD/rDXJz0Lr-Elliot-Waves-Complete-Guide-Chapter-2-3-Extensions/)
- [Chapter 3.1 – Corrective Waves (Zig-zag)](https://www.tradingview.com/chart/BTCUSD/Xb3ciA1G-Elliot-Waves-Complete-Guide-Chapter-3-1-Corrective-Waves/)
- [Chapter 3.2 – Flat & Expanded Flat](https://www.tradingview.com/chart/BTCUSD/ypL8LbFL-Elliot-Waves-Complete-Guide-Chapter-3-2-Flat-Expanded-Flat/)
- [Chapter 3.3 – Running Flat & Contracting Triangle](https://www.tradingview.com/chart/BTCUSD/Gr3w10cL-Elliot-Waves-Complete-Guide-Chapter-3-3-Running-Flat-Contract/)
- [Chapter 3.4 – Barrier & Expanded Triangle](https://www.tradingview.com/chart/BTCUSD/Wci5hObk-Elliot-Waves-Complete-Guide-Chapter-3-4-Barrier-Expanded/)
- [Chapter 3.5 – Double Three](https://www.tradingview.com/chart/BTCUSD/H8tPt7gF-Elliot-Waves-Complete-Guide-Chapter-3-5-Double-Three/)
- [Chapter 3.6 – Triple Three](https://www.tradingview.com/chart/BTCUSD/JH3c1gPH-Elliot-Waves-Complete-Guide-Chapter-3-6-Triple-Three/)
- [Chapter 4.1 – Alternation](https://www.tradingview.com/chart/BTCUSD/VsqijJB-Elliot-Waves-Complete-Guide-Chapter-4-1-Alternation/)
- [Chapter 4.2 – Channeling](https://www.tradingview.com/chart/BTCUSD/NrrJFUm2-Elliot-Waves-Complete-Guide-Chapter-4-2-Channeling/)
- [Chapter 4.3 – Market Psychology](https://www.tradingview.com/chart/BTCUSD/okgudEo0-Elliot-Waves-Complete-Guide-Chapter-4-3-Market-Psychology/)
- [Chapter 4.4 – Fibonacci Ratios](https://www.tradingview.com/chart/BTCUSD/JW9LFJKW-Elliot-Waves-Complete-Guide-Chapter-4-4-Fibonacci-Ratios/)
- [Chapter 4.5 – Fibonacci Lengths](https://www.tradingview.com/chart/BTCUSD/lG1e4x1M-Elliot-Waves-Complete-Guide-Chapter-4-5-Fibonacci-Lengths/)
- [Chapter 4.6 – ABC Fib Lengths](https://www.tradingview.com/chart/BTCUSD/YaMxVSes-Elliot-Waves-Complete-Guide-Chapter-4-6-ABC-Fib-Lengths/)

### Bitcoin cycle analysis

- [Predicting Bitcoin's Cycle Using the Elliott Wave Theory](https://www.tradingview.com/chart/BTCUSD/cEBBT5rV-Predicting-Bitcoin-s-Cycle-Using-the-Elliott-Wave-Theory/)
- [Predicting Bitcoin's Cycle — Part 2](https://www.tradingview.com/chart/BTCUSD/AKQ2n1hH-Predicting-Bitcoin-s-Cycle-Using-the-Elliott-Wave-Theory-Part-2/)
- [Predicting Bitcoin's Cycle — Part 3 (Elliott + Wyckoff)](https://www.tradingview.com/chart/BTCUSD/Ftpdj9OZ-Predicting-Bitcoin-s-Cycle-Using-the-Elliott-Wave-Theory-Part-3/)

### Complementary

- [Bullish Chart Patterns](https://www.tradingview.com/chart/BTCUSD/J9i4sPFN-The-Most-Used-and-Profitable-Chart-Patterns-Bullish-Patterns/)

---

*Classical material aligns with the linked guides. Engine rows document the detector specification bundled with this skill.*
