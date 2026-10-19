# Resume / abort

1. Read `00-run.md` Status, Mode, profile, settle gen, Last stage, Notes.  
2. If `done` / `stopped` — do not Prefer stages (unless user aborts/reopens explicitly).  
3. If **paused-wait** — stay paused until answer / Build arm / remaining Gate C yes.  
   **paused-wait (checkable)** = Status `paused` ∧ (Build armed unpaid on async path ∨ Gate C approved non-empty without `merge` ∨ Notes `waiting — <reason>`).  
   Notes `waiting — <reason>` = **parent-only** set+clear ([hitl.md](hitl.md)); Stages return `candidate waiting — …` / `candidate clear waiting` only — never invent waiting for Status `paused` alone.  
   Else Status `paused` ∧ ¬ paused-wait → Prefer continue (Pre-Build → [derive-next-pre.md](derive-next-pre.md); Post-Build → [derive-next-post.md](derive-next-post.md) — selector [derive-next.md](derive-next.md)).  
4. PR-only Gate C — Prefer `gate-c` for remaining named actions or stay paused (paused-wait via Gate C approved without `merge`).  
5. Else: preflight → derive → continue.  

**Scope change:** Has API/DB/auth → Has flip path ([lenses.md](lenses.md)); Upgrade to full when multi-surface ([step-0.md](step-0.md)).
