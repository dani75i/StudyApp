import json
from pathlib import Path

from sqlalchemy.orm import Session

from .models import Chapter, ContentPack, Exercise, ExerciseGuide, Lesson, Subject


CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def _get_or_create_subject(db: Session, slug: str, meta: dict) -> Subject:
    subject = db.query(Subject).filter(Subject.slug == slug).first()
    if subject:
        return subject
    subject = Subject(
        slug=slug,
        name=meta.get("name", slug),
        emoji=meta.get("emoji", "📘"),
        description=meta.get("description", ""),
    )
    db.add(subject)
    db.flush()
    return subject


def install_content_pack(db: Session, filename: str) -> dict:
    path = CONTENT_DIR / filename
    payload = json.loads(path.read_text(encoding="utf-8"))
    pack_id = payload["pack_id"]

    existing_pack = db.query(ContentPack).filter(ContentPack.slug == pack_id).first()
    if existing_pack:
        return {"pack_id": pack_id, "status": "already_applied"}

    subjects = {
        slug: _get_or_create_subject(db, slug, meta)
        for slug, meta in payload.get("subjects", {}).items()
    }

    created = {"chapters": 0, "lessons": 0, "exercises": 0}
    updated = {"chapters": 0}

    for chapter_data in payload.get("chapters", []):
        subject = subjects[chapter_data["subject"]]
        chapter = (
            db.query(Chapter)
            .filter(
                Chapter.subject_id == subject.id,
                Chapter.level == chapter_data["level"],
                Chapter.title == chapter_data["title"],
            )
            .first()
        )

        # Reuse the original demo chapters from older StudySprint versions
        # instead of creating visually duplicated chapters in an existing DB.
        chapter_aliases = {
            "Fonctions linéaires et affines": ["Fonctions affines"],
            "Énergie, puissance et conversions": ["Énergie et puissance"],
            "Circuits électriques : tension et intensité": ["Tension et intensité"],
        }
        if chapter is None:
            aliases = chapter_aliases.get(chapter_data["title"], [])
            if aliases:
                chapter = (
                    db.query(Chapter)
                    .filter(
                        Chapter.subject_id == subject.id,
                        Chapter.level == chapter_data["level"],
                        Chapter.title.in_(aliases),
                    )
                    .first()
                )
                if chapter is not None:
                    chapter.title = chapter_data["title"]

        if chapter is None:
            chapter = Chapter(
                subject_id=subject.id,
                level=chapter_data["level"],
                title=chapter_data["title"],
                summary=chapter_data.get("summary", ""),
                order_index=chapter_data.get("order_index", 0),
            )
            db.add(chapter)
            db.flush()
            created["chapters"] += 1
        else:
            # The pack is applied only once, so updating these fields here cannot
            # overwrite later edits made from /admin on subsequent restarts.
            if filename not in ("3e_2026_v9_exercices.json", "6e_2026_v10.json", "5e_2026_v10.json"):
                chapter.summary = chapter_data.get("summary", chapter.summary)
                chapter.order_index = chapter_data.get("order_index", chapter.order_index)
                updated["chapters"] += 1

        existing_lesson_titles = {
            row[0]
            for row in db.query(Lesson.title).filter(Lesson.chapter_id == chapter.id).all()
        }
        for lesson_data in chapter_data.get("lessons", []):
            if lesson_data["title"] in existing_lesson_titles:
                continue
            db.add(
                Lesson(
                    chapter_id=chapter.id,
                    title=lesson_data["title"],
                    body=lesson_data["body"],
                    order_index=lesson_data.get("order_index", 0),
                )
            )
            created["lessons"] += 1

        existing_exercise_titles = {
            row[0]
            for row in db.query(Exercise.title).filter(Exercise.chapter_id == chapter.id).all()
        }
        for exercise_data in chapter_data.get("exercises", []):
            if exercise_data["title"] in existing_exercise_titles:
                continue
            exercise = Exercise(
                    chapter_id=chapter.id,
                    title=exercise_data["title"],
                    statement=exercise_data["statement"],
                    exercise_type=exercise_data.get("exercise_type", "mcq"),
                    options_json=json.dumps(exercise_data.get("options", []), ensure_ascii=False),
                    correct_answer=str(exercise_data["correct_answer"]),
                    correction=exercise_data["correction"],
                    difficulty=exercise_data.get("difficulty", 1),
                    points=exercise_data.get("points", 10),
                    order_index=exercise_data.get("order_index", 0),
                )
            db.add(exercise)
            db.flush()
            if exercise_data.get("hints") or exercise_data.get("steps") or exercise_data.get("method"):
                db.add(ExerciseGuide(
                    exercise_id=exercise.id,
                    hints_json=json.dumps(exercise_data.get("hints", []), ensure_ascii=False),
                    steps_json=json.dumps(exercise_data.get("steps", []), ensure_ascii=False),
                    method=exercise_data.get("method", ""),
                    diagram_json=json.dumps(exercise_data.get("diagram"), ensure_ascii=False),
                ))
            created["exercises"] += 1

    db.add(ContentPack(slug=pack_id, title=payload.get("title", pack_id)))
    db.commit()
    return {"pack_id": pack_id, "status": "applied", "created": created, "updated": updated}


def install_default_content_packs(db: Session) -> list[dict]:
    return [install_content_pack(db, filename) for filename in ("3e_2026_v1.json", "4e_2026_v1.json", "3e_2026_v9_exercices.json", "6e_2026_v10.json", "5e_2026_v10.json")]
