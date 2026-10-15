# Artifact size caps

**This file is SoT for:** soft line/bullet caps on workflow artifacts.  
Handoff base block points here — do not load [handoffs.md](handoffs.md) for caps.  
Lint soft warn: `scripts/lint-run.py <run-dir> --check-results`.

Keep artifacts short so later Tasks stay cheap. Soft caps (body content; headings OK):

| Artifact | Cap | Rule |
|----------|-----|------|
| `02-skim.md` | ≤ ~40 lines | Project shape 1–3 sentences; ≤5 rows per table |
| `01-idea.md` | Problem map ≤ ~25 lines (full); stub OK in simple | 3–5 bullets per WHAT branch; mind map ≤15 lines |
| `02-analysis.md` | Overall What/Why/How short; ≤5 solution pieces | Prefer bullets; Spike ≤5 rows; Design tree ≤15 lines; Solution branches ≤12 lines |
| `02b-grill.md` | ≤ ~60 lines | Frontier rounds + settled; glossary/ADR pointers only |
| `03-design.md` | See Mode | **full:** two Decision options; **simple:** one recommended design + ≤3-line rejected alternative. **System design** Overview ≤ ~12 bullets (or `N/A`); ≤3 Concept N; each Pattern ≤ ~8 lines; ≤3 patterns — point to sequence/contracts instead of restating; cut prose elsewhere if needed |
| `03a` / `04a` Fix ask | ≤10 bullets | Critical/Major first |
| `05-review-log` Fix ask | ≤15 bullets | Critical/Major only; Enhancements → Deferred section ([severity.md](severity.md)) |
| Parent post-step check | First ~40 lines | Read **Result** / Fix ask header only — do not re-read full design docs |

If a cap would hide a Critical risk, keep the risk and cut prose elsewhere.
