# Severity exit (canonical)

**This file is SoT for:** clean exit (Critical/Major vs Enhancement).  
All my-dev-flow subflows use this rule unless a stage says otherwise.  
**Result first-line tokens** (verify-pass, clean, blocked, …): [results.md](results.md).  
Lens / skip-review / tiny-tweak: [lenses.md](lenses.md). Pipeline order + Review profiles: [stages.md](stages.md).

## Severities

| Level | Blocks **clean**? |
|-------|-------------------|
| **Critical** | Yes |
| **Major** | Yes |
| **Enhancement** | No — log and defer (see below) |
| **Nit / FYI** | No |

## Clean

**Clean** = zero open **Critical** and **Major** for that stage or round.

Enhancements and nits do **not** block clean. List them in the findings table and copy must-fix items into **Deferred** (in `03a`, `05-review-log`, or `00-run.md` Notes) when not fixing this round.

## Fix ask

Fix ask bullets include **Critical** and **Major** only (≤ cap in [size-caps.md](size-caps.md)). Optional: one line “Deferred Enhancements: …” in Notes.
