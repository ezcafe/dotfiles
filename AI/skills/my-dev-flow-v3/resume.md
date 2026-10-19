# Resume / abort

1. Read `00-run.md` Status, Mode, profile, settle gen, Last stage, Notes.  
2. If `done` / `stopped` — do not Prefer stages (unless user aborts/reopens explicitly).  
3. If `paused` waiting on user — stay paused until answer / Build arm.  
4. PR-only Gate C — Prefer `gate-c` for remaining named actions or stay paused.  
5. Else: preflight → derive → continue.  

**Scope change:** Has API/DB/auth → Has flip path ([lenses.md](lenses.md)); Upgrade to full when multi-surface ([step-0.md](step-0.md)).
