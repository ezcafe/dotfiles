# Golden: drop skip-review when Has API/DB/auth flips yes

**Start:** Mode simple, profile skip-review, Has API/DB/auth/PII/schema = no (legal).  
**Flip:** Analyze/Design sets Has API=yes, Has DB=yes, **or** Has auth/PII/schema=yes.  
**Parent actions:**

1. Immediately drop Review profile skip-review → lite (or Decision N reclassify to full if not tiny). Mandatory Has-flip drop — **not** Prefer-paid Else / Skip-review else ([anti-patterns.md](anti-patterns.md)).
2. Notes: drop reason; never keep skip-review to “save time.”
3. Gate B: Has API/DB/auth/PII/schema yes → **blocking** ([gate-b.md](../gate-b.md)).
4. **Mirror Amend settle clear:** **Gate B approved: none**; **Build armed: none**; clear veto-window / `async-gap-pending`; **clear** `gate-b auto — <HH:MM>` (or digest) if present; Notes `has-flip — <flags> — <HH:MM>` ([lenses.md](../lenses.md) Has flip · [gate-b.md](../gate-b.md) · [derive-next.md](../derive-next.md) Settle freshness).
5. **When Has API or Has DB newly yes (not tiny):** prior overall `03a` **`clean`** does **not** pay **Design clean** / **Verify clean** while **Isolated API/DB unpaid**. Invalidate overall `03a` to **`pending`**, **or** Prefer re-run `design-verify-phase` (Mode simple) / API∥DB → `design-review` (Mode full) until **Design clean** / **Verify clean** ([lenses.md](../lenses.md) · [derive-next.md](../derive-next.md)). Auth/PII alone does not force isolated 03a.
6. After Build: `code-review-phase` → lenses → `test-lite` → Gate C (skip-review path forbidden).

**Do not:** Mode full + skip-review; keep skip-review after auth/PII/schema flips yes; launch Gate C under skip-review after the flip; treat overall `03a` **`clean`** alone as **Design clean** / **Verify clean** when Has API/DB newly yes and isolated unpaid; Build on a pre-flip Gate B settle (approved / Build armed / auto token).
