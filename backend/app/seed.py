from sqlalchemy.orm import Session

from .config import settings
from .models import Subject, User
from .security import hash_password


def seed(db: Session):
    """Create only the technical baseline.

    Pedagogical content is installed through versioned content packs so that an
    existing Neon database can receive new material without being reset.
    """
    if not db.query(User).filter(User.email == settings.admin_email.lower()).first():
        db.add(
            User(
                email=settings.admin_email.lower(),
                first_name="Admin",
                password_hash=hash_password(settings.admin_password),
                level="3e",
                role="admin",
            )
        )

    subjects = [
        {
            "slug": "mathematiques",
            "name": "Mathématiques",
            "emoji": "📐",
            "description": "Mathématiques du collège et du lycée.",
        },
        {
            "slug": "physique-chimie",
            "name": "Physique-Chimie",
            "emoji": "⚛️",
            "description": "Physique-Chimie du collège et du lycée.",
        },
    ]
    for data in subjects:
        if not db.query(Subject).filter(Subject.slug == data["slug"]).first():
            db.add(Subject(**data))

    db.commit()
