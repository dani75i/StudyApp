"""Scoped, once-only quality corrections. Never reset all lessons in production.

Existing /admin edits are preserved unless their body exactly equals a known V10.5
shipped version. Exercise guides are added only when no steps already exist.
"""
import json
from pathlib import Path

from sqlalchemy.orm import Session

from .models import Chapter, ContentPack, Exercise, ExerciseGuide, Lesson

CONTENT = Path(__file__).resolve().parent.parent / 'content'


def apply_quality_patch(db: Session) -> dict:
    payload = json.loads((CONTENT / 'quality_v106.json').read_text(encoding='utf-8'))
    if db.query(ContentPack).filter_by(slug=payload['slug']).first():
        return {'pack_id': payload['slug'], 'status': 'already_applied'}

    counters = {'lessons_updated': 0, 'lessons_skipped': 0,
                'guides_added': 0, 'guides_skipped': 0,
                'statements_updated': 0, 'statements_skipped': 0}
    for patch in payload['lessons']:
        lesson = (db.query(Lesson).join(Chapter)
                  .filter(Chapter.level == patch['level'],
                          Chapter.title == patch['chapter'],
                          Lesson.title == patch['title']).first())
        if lesson is None or lesson.body not in patch['expected_bodies']:
            counters['lessons_skipped'] += 1
            continue
        lesson.body = patch['body']
        counters['lessons_updated'] += 1

    for patch in payload['guides']:
        exercise = (db.query(Exercise).join(Chapter)
                    .filter(Chapter.level == patch['level'],
                            Chapter.title == patch['chapter'],
                            Exercise.title == patch['title']).first())
        if exercise is None or exercise.correction != patch['expected_correction']:
            counters['guides_skipped'] += 1
            continue
        guide = db.query(ExerciseGuide).filter_by(exercise_id=exercise.id).first()
        if guide and json.loads(guide.steps_json or '[]'):
            counters['guides_skipped'] += 1
            continue
        if guide is None:
            guide = ExerciseGuide(exercise_id=exercise.id)
            db.add(guide)
        guide.steps_json = json.dumps(patch['steps'], ensure_ascii=False)
        counters['guides_added'] += 1

    for patch in payload.get('statement_patches', []):
        exercise = (db.query(Exercise).join(Chapter)
                    .filter(Chapter.level == patch['level'],
                            Chapter.title == patch['chapter'],
                            Exercise.title == patch['title']).first())
        if exercise is None or (exercise.statement != patch['expected_statement']
                                or exercise.correction != patch['expected_correction']):
            counters['statements_skipped'] += 1
            continue
        exercise.statement = patch['statement']
        counters['statements_updated'] += 1
        guide = db.query(ExerciseGuide).filter_by(exercise_id=exercise.id).first()
        if guide is None:
            guide = ExerciseGuide(exercise_id=exercise.id)
            db.add(guide)
        if not json.loads(guide.steps_json or '[]'):
            guide.steps_json = json.dumps(patch['steps'], ensure_ascii=False)
            counters['guides_added'] += 1

    db.add(ContentPack(slug=payload['slug'], title=payload['title']))
    db.commit()
    return {'pack_id': payload['slug'], 'status': 'applied', **counters}
