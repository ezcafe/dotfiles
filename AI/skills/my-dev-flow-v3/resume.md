# Resume / abort

1. Read `00-run.md` Status, Mode, profile, settle gen, Last stage, Notes.  
2. If `done` / `stopped` — do not Prefer stages (unless user aborts/reopens explicitly).  
3. If **paused-wait** — stay paused until answer / Build arm / remaining Gate C yes.  
   **paused-wait (checkable)** = Status `paused` ∧ (Build armed unpaid on async path ∨ Gate C approved non-empty without `merge` ∨ Notes `waiting — <reason>`).  
   Notes `waiting — <reason>` = parent **or** labeled solo set+clear ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)); Stages return `candidate waiting — …` / `candidate clear waiting` only — never invent waiting for Status `paused` alone.  
   Else Status `paused` ∧ ¬ paused-wait → fall-through Prefer (evaluate next unpaid row — Pre-Build → [derive-next-pre.md](derive-next-pre.md); Post-Build → [derive-next-post.md](derive-next-post.md) — selector [derive-next.md](derive-next.md)).  
4. PR-only Gate C — Prefer `gate-c` for remaining named actions or stay paused (paused-wait via Gate C approved without `merge`).  
5. Else: preflight → derive → continue.  

## Task crash / partial artifacts

| Situation | Resume |
|-----------|--------|
| Task died / tool error mid-skill | Parent keeps card + on-disk artifacts. Re-run routing pack → Prefer unpaid stage that owns incomplete files. Do **not** invent Result tokens or consent Notes. Re-spawn fresh Task ([spawn-contract.md](spawn-contract.md)). |
| Partial `design-phase` (`03` `pending`, Grill still open, Qs in artifact) | Prefer `grill` or re-enter `design-phase` per Prefer; Parent-relay present `Blocked / questions` if any; never treat partial as Design present / Grill closed. |
| HITL hard-stop mid-ideation / mid-grill | Parent presents Qs → stamps Notes → re-spawn same skill ([spawn-contract.md](spawn-contract.md) HITL re-entry). |
| After signals applied but Next unclear | Prefer first-match; unmatched → Decision N ([failure.md](failure.md)) — do not invent Next. |

**Scope change:** Has API/DB/auth → Has flip path ([lenses.md](lenses.md)); Upgrade to full when multi-surface ([step-0.md](step-0.md)).
