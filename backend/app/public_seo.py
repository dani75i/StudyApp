"""Server-side HTML for public ExoDéclic pages.

React still owns the interface. The initial HTTP response also contains the
public educational content so that crawlers and users without JS can read it.
Do not use this module on private/student routes.
"""
from __future__ import annotations

import html
import json
import re

from sqlalchemy.orm import Session

from .models import Chapter, Lesson, Subject

PREFIX = "@@studysprint-blocks@@"  # Existing storage marker: do not rename it.
PUBLIC_PREFIX = "/decouvrir/cours/"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def lesson_fragment(raw: str) -> str:
    """Render old plain text and current structured lessons without accepting HTML."""
    raw = raw or ""
    if raw.startswith(PREFIX):
        try:
            blocks = json.loads(raw[len(PREFIX):])
        except (ValueError, TypeError):
            blocks = []
        fragments = []
        for block in blocks if isinstance(blocks, list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "list":
                items = "".join(f"<li>{esc(item)}</li>" for item in (block.get("items") or []))
                if items:
                    fragments.append(f"<ul>{items}</ul>")
            else:
                text = str(block.get("content") or "").strip()
                if text:
                    tag = "blockquote" if block.get("type") == "note" else "p"
                    fragments.append(f"<{tag}>{esc(text)}</{tag}>")
        return "".join(fragments)
    return "".join(f"<p>{esc(part.strip())}</p>" for part in re.split(r"\n+", raw) if part.strip())


def document_context(path: str, db: Session) -> dict | None:
    """Returns search metadata and a readable initial snapshot for public pages."""
    if path == "/":
        return {
            "title": "ExoDéclic — Cours et exercices corrigés du collège",
            "description": "Cours gratuits et exercices corrigés de maths et de physique-chimie pour la 6e, 5e, 4e et 3e. Révise à ton rythme avec ExoDéclic.",
            "content": (
                "<h1>ExoDéclic : cours et exercices corrigés du collège</h1>"
                "<p>Progresse en mathématiques et en physique-chimie, de la 6e à la 3e. "
                "Retrouve des fiches de cours gratuites et entraîne-toi avec des exercices corrigés.</p>"
                '<p><a href="/decouvrir/cours">Découvrir les cours gratuits</a></p>'
            ),
        }
    if path == "/decouvrir/cours":
        subjects = db.query(Subject).filter(Subject.slug.in_(("mathematiques", "physique-chimie"))).order_by(Subject.id).all()
        parts = ["<h1>Cours gratuits de maths et de physique-chimie du collège</h1>",
                 "<p>Choisis une matière puis un chapitre de la 6e à la 3e.</p>"]
        for subject in subjects:
            parts.append(f"<section><h2>{esc(subject.name)}</h2><ul>")
            chapters = db.query(Chapter).filter(Chapter.subject_id == subject.id).order_by(Chapter.level, Chapter.order_index).all()
            for chapter in chapters:
                parts.append(f'<li><a href="/decouvrir/cours/{chapter.id}">{esc(chapter.title)} — {esc(chapter.level)}</a> : {esc(chapter.summary)}</li>')
            parts.append("</ul></section>")
        return {
            "title": "Cours gratuits de maths et physique-chimie (6e à 3e) | ExoDéclic",
            "description": "Découvre les cours gratuits de maths et physique-chimie du collège : 6e, 5e, 4e et 3e. Fiches de révision et exercices corrigés sur ExoDéclic.",
            "content": "".join(parts),
        }
    if path.startswith(PUBLIC_PREFIX) and path[len(PUBLIC_PREFIX):].isdigit():
        chapter = db.get(Chapter, int(path[len(PUBLIC_PREFIX):]))
        if chapter is None:
            return None
        subject = db.get(Subject, chapter.subject_id)
        if subject is None or subject.slug not in ("mathematiques", "physique-chimie"):
            return None
        lesson_rows = db.query(Lesson).filter(Lesson.chapter_id == chapter.id).order_by(Lesson.order_index, Lesson.id).all()
        parts = [f'<p><a href="/decouvrir/cours">Cours gratuits</a> / {esc(subject.name)} / {esc(chapter.level)}</p>',
                 f'<h1>{esc(chapter.title)} — {esc(chapter.level)}</h1>',
                 f'<p>{esc(chapter.summary)}</p>']
        for lesson in lesson_rows:
            parts.append(f'<section><h2>{esc(lesson.title)}</h2>{lesson_fragment(lesson.body)}</section>')
        parts.append(f'<p><a href="/inscription">Créer un compte pour faire des exercices corrigés</a></p>')
        description = f"{chapter.title} en {chapter.level} : {chapter.summary} Cours gratuit de {subject.name} sur ExoDéclic."
        return {"title": f"{chapter.title} — {subject.name} {chapter.level} | ExoDéclic",
                "description": description[:225], "content": "".join(parts)}
    if path == "/confidentialite":
        return {"title": "Confidentialité et cookies | ExoDéclic",
                "description": "Information sur la confidentialité, les cookies et la mesure d’audience de la plateforme ExoDéclic.",
                "content": "<h1>Confidentialité et cookies</h1><p>Informations concernant l'utilisation de la plateforme ExoDéclic et le suivi d'audience facultatif.</p>"}
    return None


def render_index(index_html: str, context: dict | None, url: str, path: str) -> str:
    """Add canonical/OG metadata and a visible, escaped public HTML snapshot."""
    if context is None:
        title = "Espace élève | ExoDéclic"
        description = "ExoDéclic, cours et exercices de mathématiques et physique-chimie pour le collège."
        robots = "noindex,nofollow"
    else:
        title = context["title"]
        description = context["description"]
        robots = "index,follow"

    for selector, attr, value in [
        (r'<title>.*?</title>', None, f"<title>{esc(title)}</title>"),
        (r'<meta name="description"[^>]*>', "content", description),
        (r'<meta name="robots"[^>]*>', "content", robots),
        (r'<meta property="og:title"[^>]*>', "content", title),
        (r'<meta property="og:description"[^>]*>', "content", description),
    ]:
        replacement = value if attr is None else re.sub(r'content="[^"]*"', lambda _: f'content="{esc(value)}"',
                                                         re.search(selector, index_html).group(0), count=1)
        index_html = re.sub(selector, lambda _: replacement, index_html, count=1, flags=re.DOTALL)

    if context is not None:
        head = (f'<link rel="canonical" href="{esc(url)}" />'
                f'<meta property="og:url" content="{esc(url)}" />')
        index_html = index_html.replace("</head>", f"    {head}\n  </head>", 1)
        # React replaces this snapshot immediately. Search engines can read it
        # even if their JS renderer is delayed or unavailable.
        snapshot = ('<main class="seo-snapshot" style="max-width:980px;margin:36px auto;padding:20px;'
                    'font-family:system-ui,sans-serif;line-height:1.7;color:#26334a">'
                    f'{context["content"]}</main>')
        index_html = index_html.replace('<div id="root"></div>', f'<div id="root">{snapshot}</div>', 1)
    return index_html
