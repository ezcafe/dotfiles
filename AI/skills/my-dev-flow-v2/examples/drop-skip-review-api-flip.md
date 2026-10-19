# Golden: drop skip-review when Has API/DB/auth flips yes

**Start:** Mode simple, profile skip-review, Has API/DB/auth/PII/schema = no (legal).  
**Flip:** Analyze/Design sets Has API=yes, Has DB=yes, **or** Has auth/PII/schema=yes.  
**Parent actions:**

1. Immediately drop Review profile skip-review → lite (or Decision N reclassify to full if not tiny).
2. Notes: drop reason; never keep skip-review to “save time.”
3. Gate B: Has API/DB/auth/PII/schema yes → **blocking** ([gate-b.md](../gate-b.md)).
4. After Build: `code-review-phase` → lenses → `test-lite` → Gate C (skip-review path forbidden).

**Do not:** Mode full + skip-review; keep skip-review after auth/PII/schema flips yes; launch Gate C under skip-review after the flip.
