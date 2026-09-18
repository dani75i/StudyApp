import hashlib
import json
from pathlib import Path
from datetime import date, datetime, time, timedelta

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from .config import settings
from .db import Base, SessionLocal, engine, get_db
from .models import Attempt, Chapter, Exercise, Lesson, Subject, User
from .schemas import (
    AdminChapterIn,
    AdminExerciseIn,
    AdminLessonIn,
    AnswerIn,
    LoginIn,
    ProfileIn,
    RegisterIn,
    WeeklyGoalIn,
)
from .security import create_session, delete_current_session, get_current_user, hash_password, verify_password
from .seed import seed

ALLOWED_SUBJECT_SLUGS = ("mathematiques", "physique-chimie")

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    # Lightweight migration for users upgrading a previous local StudySprint database.
    user_columns = {column["name"] for column in inspect(engine).get_columns("users")}
    if "weekly_goal" not in user_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE users ADD COLUMN weekly_goal INTEGER DEFAULT 20"))
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


def user_dict(user: User):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "level": user.level,
        "role": user.role,
        "weekly_goal": user.weekly_goal,
    }


def allowed_subjects(db: Session):
    return db.query(Subject).filter(Subject.slug.in_(ALLOWED_SUBJECT_SLUGS)).order_by(Subject.id).all()


def level_chapters(db: Session, level: str):
    subject_ids = [s.id for s in allowed_subjects(db)]
    if not subject_ids:
        return []
    return (
        db.query(Chapter)
        .filter(Chapter.level == level, Chapter.subject_id.in_(subject_ids))
        .order_by(Chapter.subject_id, Chapter.order_index)
        .all()
    )


def progress_for_chapter(db: Session, user_id: int, chapter_id: int):
    total = db.query(Exercise).filter(Exercise.chapter_id == chapter_id).count()
    if total == 0:
        return {"total": 0, "completed": 0, "correct": 0, "percent": 0}
    exercise_ids = [x[0] for x in db.query(Exercise.id).filter(Exercise.chapter_id == chapter_id).all()]
    attempted = (
        db.query(Attempt.exercise_id)
        .filter(Attempt.user_id == user_id, Attempt.exercise_id.in_(exercise_ids))
        .distinct()
        .count()
    )
    correct = (
        db.query(Attempt.exercise_id)
        .filter(
            Attempt.user_id == user_id,
            Attempt.exercise_id.in_(exercise_ids),
            Attempt.is_correct.is_(True),
        )
        .distinct()
        .count()
    )
    return {"total": total, "completed": attempted, "correct": correct, "percent": round(correct / total * 100)}


def streak_for_attempts(attempts):
    active_days = sorted({a.created_at.date() for a in attempts}, reverse=True)
    streak = 0
    cursor = date.today()
    if active_days and active_days[0] < cursor:
        cursor = active_days[0]
    active_set = set(active_days)
    while cursor in active_set:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def week_bounds():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    start = datetime.combine(monday, time.min)
    end = start + timedelta(days=7)
    return start, end


def weekly_progress(db: Session, user: User):
    start, end = week_bounds()
    attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user.id, Attempt.created_at >= start, Attempt.created_at < end)
        .all()
    )
    completed = len({a.exercise_id for a in attempts})
    correct = len({a.exercise_id for a in attempts if a.is_correct})
    target = user.weekly_goal or 20
    percent = min(100, round(completed / target * 100)) if target else 0
    return {"completed": completed, "correct": correct, "target": target, "percent": percent}


def badge_data(db: Session, user: User, attempts, chapter_progress, streak, week):
    completed_ids = {a.exercise_id for a in attempts}
    correct_ids = {a.exercise_id for a in attempts if a.is_correct}
    badges = [
        {
            "id": "first-step",
            "title": "Premier pas",
            "description": "Terminer ton premier exercice.",
            "icon": "sparkles",
            "unlocked": len(completed_ids) >= 1,
            "progress": min(1, len(completed_ids)),
            "target": 1,
        },
        {
            "id": "ten-correct",
            "title": "Sérieux à l'entraînement",
            "description": "Maîtriser 10 exercices différents.",
            "icon": "medal",
            "unlocked": len(correct_ids) >= 10,
            "progress": min(10, len(correct_ids)),
            "target": 10,
        },
        {
            "id": "chapter-master",
            "title": "Chapitre maîtrisé",
            "description": "Atteindre 100 % sur un chapitre.",
            "icon": "trophy",
            "unlocked": any(c["percent"] == 100 and c["total"] > 0 for c in chapter_progress),
            "progress": 1 if any(c["percent"] == 100 and c["total"] > 0 for c in chapter_progress) else 0,
            "target": 1,
        },
        {
            "id": "streak-3",
            "title": "3 jours d'affilée",
            "description": "Travailler trois jours consécutifs.",
            "icon": "flame",
            "unlocked": streak >= 3,
            "progress": min(3, streak),
            "target": 3,
        },
        {
            "id": "weekly-goal",
            "title": "Objectif de la semaine",
            "description": "Atteindre ton objectif hebdomadaire.",
            "icon": "target",
            "unlocked": week["completed"] >= week["target"],
            "progress": min(week["target"], week["completed"]),
            "target": week["target"],
        },
    ]
    return badges


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/public/catalog")
def public_catalog(db: Session = Depends(get_db)):
    subjects = allowed_subjects(db)
    result = []
    for subject in subjects:
        chapters = (
            db.query(Chapter)
            .filter(Chapter.subject_id == subject.id)
            .order_by(Chapter.level, Chapter.order_index, Chapter.id)
            .all()
        )
        result.append({
            "id": subject.id,
            "slug": subject.slug,
            "name": subject.name,
            "emoji": subject.emoji,
            "description": subject.description,
            "chapters": [
                {
                    "id": chapter.id,
                    "title": chapter.title,
                    "summary": chapter.summary,
                    "level": chapter.level,
                    "lesson_count": db.query(Lesson).filter(Lesson.chapter_id == chapter.id).count(),
                    "exercise_count": db.query(Exercise).filter(Exercise.chapter_id == chapter.id).count(),
                }
                for chapter in chapters
            ],
        })
    return result


@app.get("/api/public/chapters/{chapter_id}")
def public_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapitre introuvable")
    subject = db.get(Subject, chapter.subject_id)
    if not subject or subject.slug not in ALLOWED_SUBJECT_SLUGS:
        raise HTTPException(404, "Chapitre introuvable")
    lessons = db.query(Lesson).filter(Lesson.chapter_id == chapter_id).order_by(Lesson.order_index).all()
    return {
        "id": chapter.id,
        "title": chapter.title,
        "summary": chapter.summary,
        "level": chapter.level,
        "subject": {"id": subject.id, "name": subject.name, "emoji": subject.emoji, "slug": subject.slug},
        "lessons": [{"id": lesson.id, "title": lesson.title, "body": lesson.body} for lesson in lessons],
        "exercise_count": db.query(Exercise).filter(Exercise.chapter_id == chapter_id).count(),
    }


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt():
    base = settings.site_url.rstrip("/")
    return f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /dashboard\nDisallow: /historique\nDisallow: /profil\nSitemap: {base}/sitemap.xml\n"


@app.get("/sitemap.xml")
def sitemap_xml(db: Session = Depends(get_db)):
    base = settings.site_url.rstrip("/")
    subject_ids = [subject.id for subject in allowed_subjects(db)]
    chapters = (
        db.query(Chapter).filter(Chapter.subject_id.in_(subject_ids)).order_by(Chapter.id).all()
        if subject_ids else []
    )
    urls = [f"{base}/", f"{base}/decouvrir/cours"] + [f"{base}/decouvrir/cours/{chapter.id}" for chapter in chapters]
    rows = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{rows}</urlset>'
    return Response(content=xml, media_type="application/xml")


def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Accès administrateur requis")
    return user


def admin_content_payload(db: Session):
    subjects = allowed_subjects(db)
    subject_ids = [subject.id for subject in subjects]
    chapters = (
        db.query(Chapter)
        .filter(Chapter.subject_id.in_(subject_ids))
        .order_by(Chapter.level, Chapter.subject_id, Chapter.order_index, Chapter.id)
        .all()
        if subject_ids else []
    )
    chapter_ids = [chapter.id for chapter in chapters]
    lessons = (
        db.query(Lesson)
        .filter(Lesson.chapter_id.in_(chapter_ids))
        .order_by(Lesson.chapter_id, Lesson.order_index, Lesson.id)
        .all()
        if chapter_ids else []
    )
    exercises = (
        db.query(Exercise)
        .filter(Exercise.chapter_id.in_(chapter_ids))
        .order_by(Exercise.chapter_id, Exercise.order_index, Exercise.id)
        .all()
        if chapter_ids else []
    )

    return {
        "subjects": [
            {
                "id": subject.id,
                "slug": subject.slug,
                "name": subject.name,
                "emoji": subject.emoji,
                "description": subject.description,
            }
            for subject in subjects
        ],
        "chapters": [
            {
                "id": chapter.id,
                "subject_id": chapter.subject_id,
                "level": chapter.level,
                "title": chapter.title,
                "summary": chapter.summary,
                "order_index": chapter.order_index,
                "lesson_count": sum(1 for lesson in lessons if lesson.chapter_id == chapter.id),
                "exercise_count": sum(1 for exercise in exercises if exercise.chapter_id == chapter.id),
            }
            for chapter in chapters
        ],
        "lessons": [
            {
                "id": lesson.id,
                "chapter_id": lesson.chapter_id,
                "title": lesson.title,
                "body": lesson.body,
                "order_index": lesson.order_index,
            }
            for lesson in lessons
        ],
        "exercises": [
            {
                "id": exercise.id,
                "chapter_id": exercise.chapter_id,
                "title": exercise.title,
                "statement": exercise.statement,
                "exercise_type": exercise.exercise_type,
                "options": json.loads(exercise.options_json or "[]"),
                "correct_answer": exercise.correct_answer,
                "correction": exercise.correction,
                "difficulty": exercise.difficulty,
                "points": exercise.points,
                "order_index": exercise.order_index,
            }
            for exercise in exercises
        ],
    }


@app.get("/api/admin/content")
def admin_content(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return admin_content_payload(db)


@app.post("/api/admin/chapters")
def admin_create_chapter(payload: AdminChapterIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    subject = db.get(Subject, payload.subject_id)
    if not subject or subject.slug not in ALLOWED_SUBJECT_SLUGS:
        raise HTTPException(400, "Matière invalide")
    chapter = Chapter(**payload.model_dump())
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return {"id": chapter.id}


@app.patch("/api/admin/chapters/{chapter_id}")
def admin_update_chapter(chapter_id: int, payload: AdminChapterIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    chapter = db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapitre introuvable")
    subject = db.get(Subject, payload.subject_id)
    if not subject or subject.slug not in ALLOWED_SUBJECT_SLUGS:
        raise HTTPException(400, "Matière invalide")
    for key, value in payload.model_dump().items():
        setattr(chapter, key, value)
    db.commit()
    return {"ok": True}


@app.delete("/api/admin/chapters/{chapter_id}")
def admin_delete_chapter(chapter_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    chapter = db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapitre introuvable")
    db.delete(chapter)
    db.commit()
    return {"ok": True}


@app.post("/api/admin/lessons")
def admin_create_lesson(payload: AdminLessonIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not db.get(Chapter, payload.chapter_id):
        raise HTTPException(400, "Chapitre invalide")
    lesson = Lesson(**payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return {"id": lesson.id}


@app.patch("/api/admin/lessons/{lesson_id}")
def admin_update_lesson(lesson_id: int, payload: AdminLessonIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(404, "Cours introuvable")
    if not db.get(Chapter, payload.chapter_id):
        raise HTTPException(400, "Chapitre invalide")
    for key, value in payload.model_dump().items():
        setattr(lesson, key, value)
    db.commit()
    return {"ok": True}


@app.delete("/api/admin/lessons/{lesson_id}")
def admin_delete_lesson(lesson_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(404, "Cours introuvable")
    db.delete(lesson)
    db.commit()
    return {"ok": True}


@app.post("/api/admin/exercises")
def admin_create_exercise(payload: AdminExerciseIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not db.get(Chapter, payload.chapter_id):
        raise HTTPException(400, "Chapitre invalide")
    data = payload.model_dump(exclude={"options"})
    if payload.exercise_type == "mcq" and len([option for option in payload.options if option.strip()]) < 2:
        raise HTTPException(400, "Un QCM doit contenir au moins deux réponses proposées")
    exercise = Exercise(**data, options_json=json.dumps([option.strip() for option in payload.options if option.strip()], ensure_ascii=False))
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return {"id": exercise.id}


@app.patch("/api/admin/exercises/{exercise_id}")
def admin_update_exercise(exercise_id: int, payload: AdminExerciseIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercice introuvable")
    if not db.get(Chapter, payload.chapter_id):
        raise HTTPException(400, "Chapitre invalide")
    if payload.exercise_type == "mcq" and len([option for option in payload.options if option.strip()]) < 2:
        raise HTTPException(400, "Un QCM doit contenir au moins deux réponses proposées")
    data = payload.model_dump(exclude={"options"})
    for key, value in data.items():
        setattr(exercise, key, value)
    exercise.options_json = json.dumps([option.strip() for option in payload.options if option.strip()], ensure_ascii=False)
    db.commit()
    return {"ok": True}


@app.delete("/api/admin/exercises/{exercise_id}")
def admin_delete_exercise(exercise_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercice introuvable")
    db.delete(exercise)
    db.commit()
    return {"ok": True}


@app.post("/api/auth/register")
def register(payload: RegisterIn, response: Response, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "Un compte existe déjà avec cet email")
    user = User(
        email=email,
        first_name=payload.first_name.strip(),
        password_hash=hash_password(payload.password),
        level=payload.level,
        role="student",
        weekly_goal=20,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    create_session(db, user, response)
    return user_dict(user)


@app.post("/api/auth/login")
def login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower().strip()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Email ou mot de passe incorrect")
    create_session(db, user, response)
    return user_dict(user)


@app.post("/api/auth/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    delete_current_session(db, request.cookies.get(settings.session_cookie_name), response)
    return {"ok": True}


@app.get("/api/auth/me")
def me(user: User = Depends(get_current_user)):
    return user_dict(user)


@app.patch("/api/profile")
def update_profile(payload: ProfileIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.first_name = payload.first_name.strip()
    user.level = payload.level
    db.commit()
    return user_dict(user)


@app.patch("/api/weekly-goal")
def update_weekly_goal(payload: WeeklyGoalIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.weekly_goal = payload.weekly_goal
    db.commit()
    return weekly_progress(db, user)


@app.get("/api/catalog")
def catalog(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    subjects = allowed_subjects(db)
    result = []
    for subject in subjects:
        chapters = (
            db.query(Chapter)
            .filter(Chapter.subject_id == subject.id, Chapter.level == user.level)
            .order_by(Chapter.order_index)
            .all()
        )
        result.append({
            "id": subject.id,
            "slug": subject.slug,
            "name": subject.name,
            "emoji": subject.emoji,
            "description": subject.description,
            "chapters": [
                {
                    "id": c.id,
                    "title": c.title,
                    "summary": c.summary,
                    "level": c.level,
                    "progress": progress_for_chapter(db, user.id, c.id),
                }
                for c in chapters
            ],
        })
    return result


@app.get("/api/exercise-library")
def exercise_library(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chapters = level_chapters(db, user.level)
    chapter_ids = [c.id for c in chapters]
    if not chapter_ids:
        return []

    exercises = (
        db.query(Exercise)
        .filter(Exercise.chapter_id.in_(chapter_ids))
        .order_by(Exercise.chapter_id, Exercise.order_index)
        .all()
    )
    attempts = db.query(Attempt).filter(Attempt.user_id == user.id).all()
    attempted_ids = {a.exercise_id for a in attempts}
    correct_ids = {a.exercise_id for a in attempts if a.is_correct}
    chapter_map = {c.id: c for c in chapters}
    subject_map = {s.id: s for s in allowed_subjects(db)}

    result = []
    for exercise in exercises:
        chapter = chapter_map[exercise.chapter_id]
        subject = subject_map[chapter.subject_id]
        if exercise.id in correct_ids:
            status = "mastered"
        elif exercise.id in attempted_ids:
            status = "retry"
        else:
            status = "todo"
        result.append({
            "id": exercise.id,
            "title": exercise.title,
            "difficulty": exercise.difficulty,
            "points": exercise.points,
            "status": status,
            "chapter": {"id": chapter.id, "title": chapter.title},
            "subject": {"id": subject.id, "name": subject.name, "slug": subject.slug, "emoji": subject.emoji},
        })
    return result


@app.get("/api/chapters/{chapter_id}")
def chapter_detail(chapter_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chapter = db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapitre introuvable")
    subject = db.get(Subject, chapter.subject_id)
    if subject.slug not in ALLOWED_SUBJECT_SLUGS:
        raise HTTPException(404, "Chapitre introuvable")
    lessons = db.query(Lesson).filter(Lesson.chapter_id == chapter_id).order_by(Lesson.order_index).all()
    exercises = db.query(Exercise).filter(Exercise.chapter_id == chapter_id).order_by(Exercise.order_index).all()
    return {
        "id": chapter.id,
        "title": chapter.title,
        "summary": chapter.summary,
        "level": chapter.level,
        "subject": {"id": subject.id, "name": subject.name, "emoji": subject.emoji, "slug": subject.slug},
        "lessons": [{"id": l.id, "title": l.title, "body": l.body} for l in lessons],
        "exercises": [{"id": e.id, "title": e.title, "difficulty": e.difficulty, "points": e.points} for e in exercises],
        "progress": progress_for_chapter(db, user.id, chapter_id),
    }


@app.get("/api/exercises/{exercise_id}")
def exercise_detail(exercise_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercice introuvable")
    chapter = db.get(Chapter, exercise.chapter_id)
    subject = db.get(Subject, chapter.subject_id)
    if subject.slug not in ALLOWED_SUBJECT_SLUGS:
        raise HTTPException(404, "Exercice introuvable")
    previous = (
        db.query(Attempt)
        .filter(Attempt.user_id == user.id, Attempt.exercise_id == exercise.id)
        .order_by(Attempt.created_at.desc())
        .first()
    )
    return {
        "id": exercise.id,
        "chapter_id": exercise.chapter_id,
        "title": exercise.title,
        "statement": exercise.statement,
        "exercise_type": exercise.exercise_type,
        "options": json.loads(exercise.options_json or "[]"),
        "difficulty": exercise.difficulty,
        "points": exercise.points,
        "last_attempt": None if not previous else {"answer": previous.answer, "is_correct": previous.is_correct},
    }


def normalize_answer(value: str) -> str:
    return " ".join(value.strip().lower().replace(",", ".").split())


@app.post("/api/exercises/{exercise_id}/answer")
def answer_exercise(exercise_id: int, payload: AnswerIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercice introuvable")
    count = db.query(Attempt).filter(Attempt.user_id == user.id, Attempt.exercise_id == exercise_id).count()
    is_correct = normalize_answer(payload.answer) == normalize_answer(exercise.correct_answer)
    attempt = Attempt(
        user_id=user.id,
        exercise_id=exercise_id,
        attempt_number=count + 1,
        answer=payload.answer,
        is_correct=is_correct,
    )
    db.add(attempt)
    db.commit()
    return {
        "is_correct": is_correct,
        "correct_answer": exercise.correct_answer,
        "correction": exercise.correction,
        "points": exercise.points if is_correct else 0,
    }


@app.get("/api/daily-session")
def daily_session(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chapters = level_chapters(db, user.level)
    chapter_ids = [c.id for c in chapters]
    if not chapter_ids:
        return {"date": date.today().isoformat(), "total": 0, "completed": 0, "correct": 0, "percent": 0, "exercises": []}

    exercises = db.query(Exercise).filter(Exercise.chapter_id.in_(chapter_ids)).all()
    today_start = datetime.combine(date.today(), time.min)

    # The ranking only considers attempts before today, so today's session remains stable while the student works.
    previous_attempts = db.query(Attempt).filter(Attempt.user_id == user.id, Attempt.created_at < today_start).all()
    previous_attempted = {a.exercise_id for a in previous_attempts}
    previous_correct = {a.exercise_id for a in previous_attempts if a.is_correct}

    def rank(exercise):
        if exercise.id not in previous_attempted:
            priority = 0
        elif exercise.id not in previous_correct:
            priority = 1
        else:
            priority = 2
        digest = hashlib.sha256(f"{date.today().isoformat()}:{user.id}:{exercise.id}".encode()).hexdigest()
        return priority, digest

    selected = sorted(exercises, key=rank)[:8]
    selected_ids = [e.id for e in selected]
    today_attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user.id, Attempt.exercise_id.in_(selected_ids), Attempt.created_at >= today_start)
        .all()
        if selected_ids else []
    )
    today_attempted = {a.exercise_id for a in today_attempts}
    today_correct = {a.exercise_id for a in today_attempts if a.is_correct}

    chapter_map = {c.id: c for c in chapters}
    subjects = {s.id: s for s in allowed_subjects(db)}
    rows = []
    for index, exercise in enumerate(selected, start=1):
        chapter = chapter_map[exercise.chapter_id]
        subject = subjects[chapter.subject_id]
        rows.append({
            "order": index,
            "id": exercise.id,
            "title": exercise.title,
            "difficulty": exercise.difficulty,
            "points": exercise.points,
            "completed": exercise.id in today_attempted,
            "correct": exercise.id in today_correct,
            "chapter": {"id": chapter.id, "title": chapter.title},
            "subject": {"name": subject.name, "slug": subject.slug, "emoji": subject.emoji},
        })

    total = len(selected)
    completed = len(today_attempted)
    correct = len(today_correct)
    return {
        "date": date.today().isoformat(),
        "total": total,
        "completed": completed,
        "correct": correct,
        "percent": round(completed / total * 100) if total else 0,
        "estimated_minutes": total * 2,
        "exercises": rows,
    }


@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    attempts = db.query(Attempt).filter(Attempt.user_id == user.id).order_by(Attempt.created_at.desc()).all()
    attempted_ids = {a.exercise_id for a in attempts}
    correct_ids = {a.exercise_id for a in attempts if a.is_correct}
    chapters = level_chapters(db, user.level)
    chapter_ids = [c.id for c in chapters]
    total_exercises = db.query(Exercise).filter(Exercise.chapter_id.in_(chapter_ids)).count() if chapter_ids else 0
    success = round(len(correct_ids) / len(attempted_ids) * 100) if attempted_ids else 0
    streak = streak_for_attempts(attempts)

    chapter_progress = []
    for chapter in chapters:
        subject = db.get(Subject, chapter.subject_id)
        p = progress_for_chapter(db, user.id, chapter.id)
        chapter_progress.append({
            "chapter_id": chapter.id,
            "title": chapter.title,
            "subject": subject.name,
            "emoji": subject.emoji,
            "slug": subject.slug,
            **p,
        })

    recommended = next((c for c in sorted(chapter_progress, key=lambda x: (x["percent"], x["chapter_id"])) if c["percent"] < 100), None)
    week = weekly_progress(db, user)
    badges = badge_data(db, user, attempts, chapter_progress, streak, week)
    return {
        "first_name": user.first_name,
        "level": user.level,
        "stats": {
            "completed": len(attempted_ids),
            "correct": len(correct_ids),
            "success_rate": success,
            "available": total_exercises,
            "streak": streak,
        },
        "weekly": week,
        "badges": badges,
        "chapters": chapter_progress,
        "recommended": recommended,
    }


@app.get("/api/history")
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.query(Attempt).filter(Attempt.user_id == user.id).order_by(Attempt.created_at.desc()).limit(50).all()
    out = []
    for attempt in rows:
        exercise = db.get(Exercise, attempt.exercise_id)
        chapter = db.get(Chapter, exercise.chapter_id)
        subject = db.get(Subject, chapter.subject_id)
        if subject.slug not in ALLOWED_SUBJECT_SLUGS:
            continue
        out.append({
            "id": attempt.id,
            "exercise": exercise.title,
            "chapter": chapter.title,
            "subject": subject.name,
            "answer": attempt.answer,
            "is_correct": attempt.is_correct,
            "created_at": attempt.created_at.isoformat(),
        })
    return out

# In production the Docker image contains the Vite build. FastAPI serves the
# generated assets and returns index.html for React Router routes. API routes
# above keep priority because this catch-all is registered last.
_static_dir = Path(settings.static_dir).resolve() if settings.static_dir else None
if _static_dir and _static_dir.exists():
    assets_dir = _static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_fallback(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(404, "Route API introuvable")
        requested = (_static_dir / full_path).resolve()
        try:
            requested.relative_to(_static_dir)
        except ValueError:
            requested = _static_dir / "index.html"
        if requested.is_file():
            return FileResponse(requested)
        return FileResponse(_static_dir / "index.html")

