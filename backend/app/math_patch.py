"""Apply only explicitly reviewed V10.7 lesson changes.

Updates require an exact match against the shipped V10.5 or V10.6 lesson body.
This prevents overwriting any customised lesson edited using /admin.
No other lessons, exercises or accounts are modified.
"""
import json
from pathlib import Path

from sqlalchemy.orm import Session

from .models import Chapter, ContentPack, Lesson


CONTENT = Path(__file__).resolve().parent.parent / 'content'


def apply_math_patch(db: Session) -> dict:
    data = json.loads((CONTENT / 'quality_v107.json').read_text(encoding='utf-8'))
    if db.query(ContentPack).filter(ContentPack.slug == data['slug']).first():
        return {'pack_id': data['slug'], 'status': 'already_applied'}

    counts = {'lessons_updated': 0, 'lessons_preserved': 0}
    for row in data['lessons']:
        lesson = (db.query(Lesson).join(Chapter)
                  .filter(Chapter.level == row['level'],
                          Chapter.title == row['chapter'],
                          Lesson.title == row['title']).first())
        if lesson is None or lesson.body not in row['expected_bodies']:
            counts['lessons_preserved'] += 1
            continue
        lesson.body = row['body']
        counts['lessons_updated'] += 1

    db.add(ContentPack(slug=data['slug'], title=data['title']))
    db.commit()
    return {'pack_id': data['slug'], 'status': 'applied', **counts}
