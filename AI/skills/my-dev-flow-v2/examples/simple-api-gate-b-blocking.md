# Golden: Mode simple + Has API → Gate B blocking

**Ask:** Tiny change that still adds/changes a public API surface.  
**Classify:** Mode **simple**, profile lite, Has API=**yes** (DB/auth may be no).  
**Path:** design-phase → design-verify-phase clean (finalize Lens plan **api**) → Gate B **blocking** (not auto) → user yes + provenance `gate-b-approved` → Build → `code-review-phase` → `lens-api` (Lens plan unpaid) → test-lite → Gate C → merge → `done`.

**Do not:** Keep HITL Gate B `auto` when Has API/DB/auth/PII/schema = yes; use skip-review with Has API=yes; jump to `test-lite` while Lens plan **api** unpaid.
