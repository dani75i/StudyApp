"""Integration tests on a throwaway SQLite DB and validation of V10.7 source data."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

# Lightweight checks that do not need a frontend dependency install.
from pathlib import Path

V107 = json.loads((ROOT / 'backend/content/quality_v107.json').read_text(encoding='utf-8'))
keys = [(p['level'], p['chapter'], p['title']) for p in V107['lessons']]
assert len(keys) == len(set(keys)) == 35
assert set(x[0] for x in keys) == {'3e', '4e', '5e', '6e'}
for patch in V107['lessons']:
    assert patch['expected_bodies'] and all(isinstance(source, str) for source in patch['expected_bodies'])
    assert patch['body'].startswith('@@studysprint-blocks@@')
    blocks = json.loads(patch['body'].split('@@studysprint-blocks@@', 1)[1])
    assert any(b['type'] in ('formula', 'example') for b in blocks), patch['title']
    for block in blocks:
        if block.get('type') in ('formula', 'example', 'note', 'paragraph'):
            content = block.get('content', '')
            assert content and content.count('{') == content.count('}'), patch['title']
            assert content.count('\\(') == content.count('\\)'), patch['title']

code = r'''
import json
from pydantic import ValidationError
from app.schemas import RegisterIn, ProfileIn
for level in ['6e','5e','4e','3e']:
    assert RegisterIn(email='a@b.fr', first_name='Ada', password='password123', level=level).level == level
    assert ProfileIn(first_name='Ada', level=level).level == level
for level in ['2nde','1re','Terminale','lycée','5e ']:
    for Form, payload in [(RegisterIn, {'email':'a@b.fr', 'first_name':'Ada', 'password':'password123', 'level':level}),
                          (ProfileIn, {'first_name':'Ada', 'level':level})]:
        try: Form(**payload)
        except ValidationError: continue
        raise AssertionError((Form, level))

from app.db import Base,engine,SessionLocal
from app.content_pack import install_content_pack
from app.quality_patch import apply_quality_patch
from app.math_patch import apply_math_patch
from app.models import Chapter, Lesson, ContentPack
Base.metadata.create_all(engine)
files=("3e_2026_v1.json", "4e_2026_v1.json", "3e_2026_v9_exercices.json", "6e_2026_v10.json", "5e_2026_v10.json", "3e_2026_v10_3_refresh.json", "4e_2026_v10_3_refresh.json", "5e_2026_v10_3_refresh.json", "6e_2026_v10_3_refresh.json", "3e_2026_v10_3_exercises_refresh.json", "3e_2026_v10_4_refresh.json", "4e_2026_v10_4_refresh.json", "5e_2026_v10_4_refresh.json", "6e_2026_v10_4_refresh.json", "3e_2026_v10_4_exercises_refresh.json", "3e_2026_v10_5_refresh.json", "4e_2026_v10_5_refresh.json", "5e_2026_v10_5_refresh.json", "6e_2026_v10_5_refresh.json", "3e_2026_v10_5_exercises_refresh.json")
db=SessionLocal()
try:
    for file in files: install_content_pack(db, file)
    # A previous custom /admin edit, made before V10.6, should remain untouched.
    custom = db.query(Lesson).join(Chapter).filter(Chapter.level=='3e',Chapter.title=='Statistiques',Lesson.title=='Moyenne').first()
    custom.body = 'Formule personnalisée par le professeur.'
    db.commit()
    v106=apply_quality_patch(db)
    v107=apply_math_patch(db)
    assert v107['lessons_updated'] == 34, v107
    assert v107['lessons_preserved'] == 1, v107
    assert custom.body == 'Formule personnalisée par le professeur.'
    assert apply_math_patch(db)['status'] == 'already_applied'
    # Verify representative chapters and mathematics after actual installation.
    for level, chapter, title, needle in [
        ('3e', 'Racines carrées', 'Définition', r'\sqrt{a}'),
        ('3e', 'Géométrie dans l\'espace', 'Volumes', r'\mathrm{boule}'),
        ('3e', 'Théorème de Thalès', 'Configuration', r'\frac{DE}{BC}'),
        ('4e', 'Statistiques : moyenne et médiane', 'Moyenne', r'\overline{x}'),
        ('5e', 'Aires et volumes composés', 'Volume du pavé', r'V=L'),
        ('6e', 'Volumes et pavés droits', 'Cube', r'V=c^3'),
    ]:
        row=db.query(Lesson).join(Chapter).filter(Chapter.level==level, Chapter.title==chapter, Lesson.title==title).first()
        assert needle in row.body, (level,chapter,title,needle)
    print('PASS: registration/profile restricted to collège (frontend + Pydantic models)')
    print('PASS: narrow V10.7 patch preserves admin edits, applies once:',v107)
    print('PASS: representative 3e–6e lessons installed on an isolated SQLite database')
finally:
    db.close()
'''
# user-written test quotes use exact raw literals, no actual Neon access.
with tempfile.TemporaryDirectory() as d:
    env = dict(os.environ, PYTHONPATH=str(ROOT/'backend'), DATABASE_URL=f'sqlite:///{Path(d)/"test.sqlite"}')
    subprocess.run([sys.executable, '-c', code], cwd=ROOT, env=env, check=True)
print('PASS: 35 targeted content patches, LaTeX delimiters and JSON structure')
