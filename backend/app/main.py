import hashlib
import os
import threading
import time as time_module
from collections import defaultdict, deque
import json
from pathlib import Path
from datetime import date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import settings
from .content_pack import install_default_content_packs
from .v10_hints import upgrade_existing_hints, contextual_hints
from .db import Base, SessionLocal, engine, get_db
from .models import Attempt, Chapter, Exercise, ExerciseGuide, Feedback, Lesson, Subject, User
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
from .public_seo import document_context, render_index

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
        install_default_content_packs(db)
        upgrade_existing_hints(db)
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
    mastered_chapters = sum(1 for c in chapter_progress if c["percent"] == 100 and c["total"] > 0)
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
            "id": "twenty-five-correct",
            "title": "Élan confirmé",
            "description": "Maîtriser 25 exercices différents.",
            "icon": "star",
            "unlocked": len(correct_ids) >= 25,
            "progress": min(25, len(correct_ids)),
            "target": 25,
        },
        {
            "id": "fifty-correct",
            "title": "Machine à réviser",
            "description": "Maîtriser 50 exercices différents.",
            "icon": "rocket",
            "unlocked": len(correct_ids) >= 50,
            "progress": min(50, len(correct_ids)),
            "target": 50,
        },
        {
            "id": "chapter-master",
            "title": "Chapitre maîtrisé",
            "description": "Atteindre 100 % sur un chapitre.",
            "icon": "trophy",
            "unlocked": mastered_chapters >= 1,
            "progress": min(1, mastered_chapters),
            "target": 1,
        },
        {
            "id": "three-chapters",
            "title": "Triple maîtrise",
            "description": "Maîtriser entièrement 3 chapitres.",
            "icon": "crown",
            "unlocked": mastered_chapters >= 3,
            "progress": min(3, mastered_chapters),
            "target": 3,
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
            "id": "streak-7",
            "title": "Semaine en feu",
            "description": "Travailler sept jours consécutifs.",
            "icon": "flame",
            "unlocked": streak >= 7,
            "progress": min(7, streak),
            "target": 7,
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
    return f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /dashboard\nDisallow: /historique\nDisallow: /profil\nDisallow: /recompenses\nDisallow: /seance\nDisallow: /exercices\nDisallow: /chapitre/\nDisallow: /exercice/\nSitemap: {base}/sitemap.xml\n"


@app.get("/sitemap.xml")
def sitemap_xml(db: Session = Depends(get_db)):
    base = settings.site_url.rstrip("/")
    subject_ids = [subject.id for subject in allowed_subjects(db)]
    chapters = (
        db.query(Chapter).filter(Chapter.subject_id.in_(subject_ids)).order_by(Chapter.id).all()
        if subject_ids else []
    )
    urls = [f"{base}/", f"{base}/decouvrir/cours", f"{base}/confidentialite"] + [f"{base}/decouvrir/cours/{chapter.id}" for chapter in chapters]
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

    guides = {guide.exercise_id: guide for guide in db.query(ExerciseGuide).filter(ExerciseGuide.exercise_id.in_([ex.id for ex in exercises])).all()} if exercises else {}

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
                "hints": json.loads(guides[exercise.id].hints_json) if exercise.id in guides else [],
                "steps": json.loads(guides[exercise.id].steps_json) if exercise.id in guides else [],
                "method": guides[exercise.id].method if exercise.id in guides else "",
            }
            for exercise in exercises
        ],
    }



# V10.2 — anonymous feedback. No visitor name/email/user ID or IP is persisted.
FEEDBACK_CATEGORIES = {"opinion", "bug", "content_error", "suggestion"}
FEEDBACK_STATUSES = {"new", "in_progress", "resolved", "dismissed"}
_FEEDBACK_SALT = os.urandom(32)
_feedback_window = defaultdict(deque)
_feedback_lock = threading.Lock()


class FeedbackIn(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    category: str
    message: str = Field(min_length=12, max_length=1500)
    rating: int | None = Field(default=None, ge=1, le=5)
    page_path: str = Field(default="", max_length=240)
    website: str = Field(default="", max_length=250)  # honeypot, hidden from visitors

    @field_validator("message")
    @classmethod
    def message_must_be_meaningful(cls, value):
        if len(value.strip()) < 12 or len(set(value.casefold())) < 4:
            raise ValueError("Précise ton retour en quelques mots (12 caractères minimum).")
        return value

    @field_validator("page_path")
    @classmethod
    def clean_page_path(cls, value):
        if not value or value == "/":
            return value
        if not value.startswith("/") or value.startswith("//") or "?" in value or "#" in value or "\\" in value or any(ord(c) < 32 for c in value):
            raise ValueError("Page invalide")
        return value


class FeedbackStatusIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: str


def _feedback_throttle(request: Request):
    """Small in-memory burst limit, no IP written to logs/DB by this feature.

    Uses the ASGI client address; upstream proxy configuration determines whether
    it is the visitor IP. Multi-worker/multi-instance deployments need a shared
    persistent limiter (Redis or edge WAF) before increasing public traffic.
    """
    remote = request.client.host if request.client else "unknown"
    identity = hashlib.sha256(_FEEDBACK_SALT + remote.encode("utf-8", errors="replace")).digest()
    now = time_module.monotonic()
    with _feedback_lock:
        # No unbounded growth of abandoned identities.
        if len(_feedback_window) > 2000:
            for key in list(_feedback_window):
                if not _feedback_window[key] or _feedback_window[key][-1] < now - 3600:
                    del _feedback_window[key]
        recent = _feedback_window[identity]
        while recent and recent[0] < now - 3600:
            recent.popleft()
        if len(recent) >= 3:
            raise HTTPException(429, "Trop de messages envoyés. Réessaie dans une heure.")
        recent.append(now)


def _feedback_dict(entry: Feedback):
    return {"id": entry.id, "category": entry.category, "rating": entry.rating,
            "message": entry.message, "page_path": entry.page_path,
            "status": entry.status, "created_at": entry.created_at.isoformat()}


@app.post("/api/feedback", status_code=201)
def submit_feedback(payload: FeedbackIn, request: Request, db: Session = Depends(get_db)):
    if payload.website:
        # Bot trap: appear to accept without storing the submission.
        return {"ok": True}
    if payload.category not in FEEDBACK_CATEGORIES:
        raise HTTPException(422, "Catégorie de retour invalide")
    _feedback_throttle(request)
    entry = Feedback(category=payload.category, rating=payload.rating,
                     message=payload.message, page_path=payload.page_path, status="new")
    db.add(entry)
    db.commit()
    return {"ok": True}


@app.get("/api/admin/feedback")
def list_feedback(status: str = "all", category: str = "all", page: int = 1,
                  db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if status not in FEEDBACK_STATUSES | {"all"} or category not in FEEDBACK_CATEGORIES | {"all"}:
        raise HTTPException(422, "Filtre invalide")
    if page < 1 or page > 10000:
        raise HTTPException(422, "Page invalide")
    query = db.query(Feedback)
    if status != "all":
        query = query.filter(Feedback.status == status)
    if category != "all":
        query = query.filter(Feedback.category == category)
    total = query.count()
    rows = query.order_by(Feedback.created_at.desc(), Feedback.id.desc()).offset((page-1)*30).limit(30).all()
    return {"items": [_feedback_dict(row) for row in rows], "total": total, "page": page, "per_page": 30,
            "new_count": db.query(Feedback).filter(Feedback.status == "new").count()}


@app.patch("/api/admin/feedback/{feedback_id}")
def update_feedback_status(feedback_id: int, payload: FeedbackStatusIn,
                           db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if payload.status not in FEEDBACK_STATUSES:
        raise HTTPException(422, "Statut invalide")
    entry = db.get(Feedback, feedback_id)
    if entry is None:
        raise HTTPException(404, "Avis introuvable")
    entry.status = payload.status
    db.commit()
    return _feedback_dict(entry)


@app.delete("/api/admin/feedback/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    entry = db.get(Feedback, feedback_id)
    if entry is None:
        raise HTTPException(404, "Avis introuvable")
    db.delete(entry)
    db.commit()
    return {"ok": True}


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


def save_exercise_guide(db: Session, exercise_id: int, payload: AdminExerciseIn):
    guide = db.query(ExerciseGuide).filter_by(exercise_id=exercise_id).first()
    if not guide:
        guide = ExerciseGuide(exercise_id=exercise_id)
        db.add(guide)
    guide.hints_json = json.dumps([h.strip() for h in payload.hints if h.strip()], ensure_ascii=False)
    guide.steps_json = json.dumps([s.strip() for s in payload.steps if s.strip()], ensure_ascii=False)
    guide.method = payload.method.strip()


@app.post("/api/admin/exercises")
def admin_create_exercise(payload: AdminExerciseIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not db.get(Chapter, payload.chapter_id):
        raise HTTPException(400, "Chapitre invalide")
    data = payload.model_dump(exclude={"options", "hints", "steps", "method"})
    if payload.exercise_type == "mcq" and len([option for option in payload.options if option.strip()]) < 2:
        raise HTTPException(400, "Un QCM doit contenir au moins deux réponses proposées")
    exercise = Exercise(**data, options_json=json.dumps([option.strip() for option in payload.options if option.strip()], ensure_ascii=False))
    db.add(exercise)
    db.flush()
    save_exercise_guide(db, exercise.id, payload)
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
    data = payload.model_dump(exclude={"options", "hints", "steps", "method"})
    for key, value in data.items():
        setattr(exercise, key, value)
    exercise.options_json = json.dumps([option.strip() for option in payload.options if option.strip()], ensure_ascii=False)
    save_exercise_guide(db, exercise.id, payload)
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
            "order_index": exercise.order_index,
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

    exercise_ids = [exercise.id for exercise in exercises]
    attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user.id, Attempt.exercise_id.in_(exercise_ids))
        .order_by(Attempt.created_at.asc())
        .all()
        if exercise_ids else []
    )
    attempts_by_exercise = {}
    for attempt in attempts:
        attempts_by_exercise.setdefault(attempt.exercise_id, []).append(attempt)

    def infer_skill(exercise):
        chapter_name = chapter.title.lower()
        title = exercise.title.lower()

        if "arithmétique" in chapter_name:
            if "pgcd" in title:
                return "Calculer un PGCD"
            if "premier" in title:
                return "Reconnaître un nombre premier"
            return "Utiliser la divisibilité"
        if "puissances" in chapter_name:
            return "Calculer avec des puissances"
        if "calcul littéral" in chapter_name:
            return "Résoudre une équation" if "résoudre" in title else "Substituer une valeur"
        if "racines carrées" in chapter_name:
            return "Calculer une racine carrée"
        if "proportionnalité" in chapter_name:
            if "%" in title or "hausse" in title or "baisse" in title:
                return "Calculer un pourcentage"
            return "Utiliser la proportionnalité"
        if "images et antécédents" in chapter_name:
            return "Trouver un antécédent" if "antécédent" in title else "Calculer une image"
        if "linéaires et affines" in chapter_name:
            if "coefficient" in title:
                return "Identifier le coefficient directeur"
            if "origine" in title:
                return "Identifier l’ordonnée à l’origine"
            return "Calculer une image"
        if "statistiques" in chapter_name:
            if "médiane" in title:
                return "Calculer une médiane"
            if "moyenne" in title:
                return "Calculer une moyenne"
            return "Interpréter une série statistique"
        if "probabilités" in chapter_name:
            return "Calculer une probabilité"
        if "pythagore" in chapter_name:
            return "Appliquer Pythagore"
        if "thalès" in chapter_name or "thales" in chapter_name:
            return "Appliquer Thalès"
        if "trigonométrie" in chapter_name:
            if "définition" in title:
                return "Choisir le bon rapport"
            return "Calculer avec la trigonométrie"
        if "transformations" in chapter_name:
            return "Utiliser une transformation"
        if "géométrie dans l'espace" in chapter_name:
            return "Calculer un volume"
        if "algorithmique" in chapter_name:
            if "boucle" in title:
                return "Comprendre une boucle"
            if "condition" in title:
                return "Comprendre une condition"
            return "Lire un programme"
        if "atomes" in chapter_name:
            return "Identifier les constituants de la matière"
        if "transformations chimiques" in chapter_name:
            return "Interpréter une transformation chimique"
        if "ph" in chapter_name:
            return "Interpréter une valeur de pH"
        if "mouvement" in chapter_name:
            return "Calculer une vitesse"
        if "forces" in chapter_name:
            return "Caractériser une force"
        if "énergie" in chapter_name:
            return "Calculer énergie et puissance"
        if "circuits électriques" in chapter_name:
            return "Identifier tension et intensité"
        if "ohm" in chapter_name:
            return "Appliquer la loi d’Ohm"
        if "signaux" in chapter_name:
            return "Caractériser un signal"
        if "univers" in chapter_name:
            return "Connaître les ordres de grandeur"

        if any(token in title for token in ("graph", "lecture", "lire", "interpr")):
            return "Lire et interpréter"
        if any(token in title for token in ("identifier", "repérer", "reconnaître", "unité", "symbole")):
            return "Identifier"
        if any(token in title for token in ("calcul", "valeur", "image", "résoudre", "coefficient")):
            return "Calculer"
        return "S'entraîner"


    exercise_rows = []
    for exercise in exercises:
        exercise_attempts = attempts_by_exercise.get(exercise.id, [])
        last_attempt = exercise_attempts[-1] if exercise_attempts else None
        ever_correct = any(attempt.is_correct for attempt in exercise_attempts)
        if last_attempt is None:
            status = "todo"
        elif last_attempt.is_correct:
            status = "success"
        else:
            status = "review"
        exercise_rows.append({
            "id": exercise.id,
            "title": exercise.title,
            "difficulty": exercise.difficulty,
            "points": exercise.points,
            "order_index": exercise.order_index,
            "skill": infer_skill(exercise),
            "status": status,
            "attempt_count": len(exercise_attempts),
            "ever_correct": ever_correct,
            "last_is_correct": None if last_attempt is None else last_attempt.is_correct,
        })

    return {
        "id": chapter.id,
        "title": chapter.title,
        "summary": chapter.summary,
        "level": chapter.level,
        "subject": {"id": subject.id, "name": subject.name, "emoji": subject.emoji, "slug": subject.slug},
        "lessons": [{"id": l.id, "title": l.title, "body": l.body} for l in lessons],
        "exercises": exercise_rows,
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
    chapter_exercises = (
        db.query(Exercise.id)
        .filter(Exercise.chapter_id == exercise.chapter_id)
        .order_by(Exercise.difficulty, Exercise.order_index, Exercise.id)
        .all()
    )
    sequence_number = next((index for index, (row_id,) in enumerate(chapter_exercises, 1) if row_id == exercise.id), 1)
    previous = (
        db.query(Attempt)
        .filter(Attempt.user_id == user.id, Attempt.exercise_id == exercise.id)
        .order_by(Attempt.created_at.desc())
        .first()
    )
    guide = db.query(ExerciseGuide).filter_by(exercise_id=exercise.id).first()
    return {
        "id": exercise.id,
        "chapter_id": exercise.chapter_id,
        "sequence_number": sequence_number,
        "title": exercise.title,
        "statement": exercise.statement,
        "exercise_type": exercise.exercise_type,
        "options": json.loads(exercise.options_json or "[]"),
        "difficulty": exercise.difficulty,
        "points": exercise.points,
        "last_attempt": None if not previous else {"answer": previous.answer, "is_correct": previous.is_correct},
        "hints": (json.loads(guide.hints_json or "[]") if guide and json.loads(guide.hints_json or "[]") else contextual_hints(chapter.title, exercise.statement, exercise.exercise_type, exercise.options_json)),
        "diagram": json.loads(guide.diagram_json or "null") if guide else None,
        "sequence_total": len(chapter_exercises),
        "previous_exercise_id": chapter_exercises[sequence_number - 2][0] if sequence_number > 1 else None,
        "next_exercise_id": chapter_exercises[sequence_number][0] if sequence_number < len(chapter_exercises) else None,
    }


def normalize_answer(value: str) -> str:
    return " ".join(value.strip().lower().replace("−", "-").replace(",", ".").split())


def answers_match(candidate: str, expected: str, exercise_type: str) -> bool:
    if normalize_answer(candidate) == normalize_answer(expected):
        return True
    if exercise_type != "text":
        return False
    try:
        # A number written as 5,0 or 5.00 represents the same numerical answer as 5.
        return Decimal(normalize_answer(candidate)) == Decimal(normalize_answer(expected))
    except (InvalidOperation, ValueError):
        return False


@app.post("/api/exercises/{exercise_id}/answer")
def answer_exercise(exercise_id: int, payload: AnswerIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercice introuvable")
    count = db.query(Attempt).filter(Attempt.user_id == user.id, Attempt.exercise_id == exercise_id).count()
    is_correct = answers_match(payload.answer, exercise.correct_answer, exercise.exercise_type)
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
        "user_answer": payload.answer,
        "correct_answer": exercise.correct_answer,
        "correction": exercise.correction,
        "points": exercise.points if is_correct else 0,
    }


@app.get("/api/exercises/{exercise_id}/latest-correction")
def latest_correction(exercise_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(404, "Exercice introuvable")
    last = (db.query(Attempt).filter(Attempt.user_id == user.id, Attempt.exercise_id == exercise_id)
            .order_by(Attempt.id.desc()).first())
    if last is None:
        raise HTTPException(404, "Réponds d'abord à l'exercice pour voir la correction")
    guide = db.query(ExerciseGuide).filter_by(exercise_id=exercise.id).first()
    return {
        "is_correct": last.is_correct,
        "user_answer": last.answer,
        "correct_answer": exercise.correct_answer,
        "correction": exercise.correction,
        "steps": json.loads(guide.steps_json or "[]") if guide else [],
        "method": guide.method if guide else "",
        "attempt_number": last.attempt_number,
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
    def spa_fallback(full_path: str, request: Request):
        if full_path.startswith("api/"):
            raise HTTPException(404, "Route API introuvable")
        # Avoid two public copies of the same site under Render's temporary URL.
        # Existing Render-domain cookies cannot be transferred: sign in again
        # on the new domain if needed. Never redirect /api or health checks.
        host = (request.url.hostname or "").lower()
        official_base = settings.site_url.rstrip("/")
        if host.endswith(".onrender.com") and official_base.startswith("https://www.exodeclic.fr"):
            path = "/" + full_path.lstrip("/")
            query = f"?{request.url.query}" if request.url.query else ""
            return RedirectResponse(official_base + path + query, status_code=308)
        requested = (_static_dir / full_path).resolve()
        try:
            requested.relative_to(_static_dir)
        except ValueError:
            requested = _static_dir / "index.html"
        if requested.is_file() and requested.name != "index.html":
            return FileResponse(requested)
        # Render public pages as readable HTML + dynamic SEO metadata on first
        # request. React takes over in the browser; private routes are noindex.
        normalized_path = "/" + full_path.strip("/") if full_path.strip("/") else "/"
        with SessionLocal() as db:
            context = document_context(normalized_path, db)
        if normalized_path.startswith("/decouvrir/cours/") and context is None:
            raise HTTPException(404, "Cours introuvable")
        base = settings.site_url.rstrip("/")
        html_page = render_index((_static_dir / "index.html").read_text(encoding="utf-8"), context,
                                 base + normalized_path if normalized_path != "/" else base + "/", normalized_path)
        return HTMLResponse(content=html_page)

