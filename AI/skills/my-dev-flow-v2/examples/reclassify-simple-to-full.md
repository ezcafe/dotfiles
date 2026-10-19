# Golden: mid-run reclassify simple → full

**Start:** Mode simple (e.g. tiny copy tweak).  
**Flip:** Design discovers new public route + persistence → Has API=yes, Has DB=yes.  
**Parent actions:**

1. Pause; Decision N ([decisions.md](../decisions.md)): Stay simple · Upgrade to full · New slug/stop. Prefer **Upgrade to full**.
2. Set Mode **full**; Review profile **full** or **lite** (never keep skip-review).
3. Notes: `reclassify simple→full — API+DB appeared`.
4. Resume Full pipeline from incomplete step (usually Design → parallel API∥DB when both yes).
5. Gate B → **blocking** ([gate-b.md](../gate-b.md)).

**Do not:** Keep Mode simple + skip-review after Has API/DB yes; invent Ideation redo unless Decision N requires it.
