# Stages — my-guide-flow

Run in order. Resume from `00-run.md` **Last stage**.

## Step index

| Step | Stage | Writes | Done when |
|------|--------|--------|-----------|
| 0 | Bootstrap | `00-run.md` + dirs | Slug chosen; root exists |
| 1 | Mission | `MISSION.md` | Why / Success / Constraints / Out of scope agreed |
| 2 | Resources | `RESOURCES.md` | Enough high-trust sources for the next lesson (Gaps listed if thin) |
| 3 | Lesson | `lessons/NNNN-*.html`, `assets/*` as needed | One short lesson opened for the user |
| 4 | Reference | `reference/*.html`, `GLOSSARY.md` when earned | Compressed units linked from the lesson |
| 5 | Record | `learning-records/NNNN-*.md`, `NOTES.md` | Only if evidence / prior knowledge / mission shift / preference |

After Step 5, loop **2 → 5** (refresh resources if Gaps block the next ZPD topic) or stop if the user ends the session.

---

## Step 0 — Bootstrap

1. Resolve `{topic}` → `{topic-slug}` (ask if ambiguous).
2. Create `.my-docs/guide/{topic-slug}/` if missing.
3. Write/update `00-run.md` (Last stage: Bootstrap → Mission).

**Existing workspace:** read `MISSION.md`, `NOTES.md`, latest learning records; set Last stage to the next incomplete step.

---

## Step 1 — Mission

1. If mission vague → interview (do not invent a fake Why).
2. Write `MISSION.md` per [MISSION-FORMAT.md](MISSION-FORMAT.md).
3. Confirm with the user.
4. Last stage: Mission → Resources.

---

## Step 2 — Resources

1. Search primary / high-trust sources for the mission (and next ZPD topic).
2. Update `RESOURCES.md` per [RESOURCES-FORMAT.md](RESOURCES-FORMAT.md).
3. Surface `## Gaps` when mission-critical areas lack sources.
4. Last stage: Resources → Lesson.

**Rule:** Do not author a lesson whose claims you cannot cite from Resources (or a newly added primary source written into Resources in the same turn).

---

## Step 3 — Lesson

1. Choose next topic (user-named or ZPD from mission + learning records).
2. Read `assets/`; reuse or add shared components.
3. Write next `lessons/NNNN-slug.html` (increment NNNN).
4. Open the file for the user when possible.
5. Last stage: Lesson → Reference.

---

## Step 4 — Reference

1. Extract compressed units into `reference/*.html` when the lesson produced reusable knowledge.
2. Promote glossary terms only after the user can use them correctly ([GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md)).
3. Link lesson ↔ reference via anchors.
4. Last stage: Reference → Record (or Resources if Gaps remain).

---

## Step 5 — Record

Write a learning record only when [LEARNING-RECORD-FORMAT.md](LEARNING-RECORD-FORMAT.md) says it qualifies. Update `NOTES.md` for teaching preferences. Update `00-run.md` Last stage and Notes.

Then ask: continue with next lesson, pause, or revise mission?
