import base64
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta
from fastapi import Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from .config import settings
from .db import get_db
from .models import Session as UserSession, User


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        _, salt_b64, digest_b64 = encoded.split("$", 2)
        salt = base64.urlsafe_b64decode(salt_b64)
        expected = base64.urlsafe_b64decode(digest_b64)
        actual = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_session(db: Session, user: User, response: Response) -> None:
    token = secrets.token_urlsafe(48)
    expires = datetime.utcnow() + timedelta(days=settings.session_days)
    db.add(UserSession(user_id=user.id, token_hash=_token_hash(token), expires_at=expires))
    db.commit()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.session_days * 86400,
        path="/",
    )


def delete_current_session(db: Session, token: str | None, response: Response) -> None:
    if token:
        db.query(UserSession).filter(UserSession.token_hash == _token_hash(token)).delete()
        db.commit()
    response.delete_cookie(settings.session_cookie_name, path="/")


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non connecté")
    session = db.query(UserSession).filter(UserSession.token_hash == _token_hash(token)).first()
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expirée")
    user = db.get(User, session.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur introuvable")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès administrateur requis")
    return user
