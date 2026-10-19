# Golden: Has flip drop skip-review

**Start:** Mode simple, profile skip-review, Has UI=no ∧ Has API=no ∧ Has DB=no ∧ Has auth/PII/schema=no (all explicit `no`).  
**Flip:** Design After returns `proposed Has: …` with API and/or DB = yes (not tiny), UI = yes, and/or auth/PII/schema = yes — parent applies card Has via Always §4 ([../lenses.md](../lenses.md) · [../preflight.md](../preflight.md)).

**Parent** ([../lenses.md](../lenses.md)):

1. Drop skip-review → lite (mandatory — [../lenses.md](../lenses.md) Has flip §1; Always §4 applies full §1–5).  
2. Gate B → **blocking** when API/DB/auth flips to yes (or auto predicate fails); UI flip alone fail-closes skip-review but does **not** deny Gate B auto — [../lenses.md](../lenses.md) Has flip §2 · [../gate-b.md](../gate-b.md).  
3. Bump settle gen; clear prior settle — for **any** flip (incl. UI-only) — §3.  
4. Notes `has-flip — <flags> — gen:<N>`.  
5. When API/DB newly yes (not tiny) **or** UI newly yes **or** auth/PII/schema newly yes: parent **must** set overall `03a` → `pending` **same turn** as Always §4 (prior overall `clean` does **not** pay Design clean / Verify clean). Then Prefer re-verify until Design clean / Verify clean:  
   - Mode **simple:** Prefer unpaid **`design-verify-phase` only** — that stage **writes** matching Isolated `03a-api` / `03a-db` + Results when API/DB required (Has ∈ {yes, unknown} not tiny). Do **not** Prefer Isolated Prefer stages.  
   - Mode **full:** Prefer unpaid Isolated when required (API/DB newly yes ¬tiny or Isolated still unpaid) → then `design-review`.  
   UI/auth flips force overall invalidate + Prefer re-verify; they do **not** invent Isolated files alone. Same Isolated duty when Has API/DB stays `unknown` (not a flip) — [../lenses.md](../lenses.md).

**Do not:** Keep skip-review; Build on pre-flip settle; treat overall `03a` soft-re-run without invalidate (incl. UI/auth flip); treat overall `03a` clean alone as Design clean while Isolated unpaid; Prefer Isolated stages under Mode simple.
