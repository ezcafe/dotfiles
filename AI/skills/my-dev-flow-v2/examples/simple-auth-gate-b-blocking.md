# Golden: Mode simple + auth → Gate B blocking

**Ask:** Login-required settings toggle; no new public API; no DB schema migration.  
**Classify:** Mode simple, profile lite; Has API=no, Has DB=no, **Has auth/PII/schema=yes**.  
**Path:** design-phase (sets auth=yes) → design-verify-phase clean → Gate B **blocking** (not auto) → user yes + provenance `gate-b-approved` → Build → `code-review-phase` → lenses (often **security**) → `test-lite` → Gate C → merge → `done`.

**Do not:** Keep HITL Gate B `auto` / `async-notify` because Has API/DB are no; keep **skip-review** when Has auth/PII/schema=yes (same ban as Has API/DB — [lenses.md](../lenses.md)).
