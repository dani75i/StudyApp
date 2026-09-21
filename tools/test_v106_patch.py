"""Integration test using an isolated SQLite database, never the user's Neon DB."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
code=r'''
import json
from app.db import Base,engine,SessionLocal
from app.content_pack import install_content_pack
from app.quality_patch import apply_quality_patch
from app.models import Chapter, Lesson, Exercise, ExerciseGuide, ContentPack, Attempt
Base.metadata.create_all(engine)
db=SessionLocal()
try:
    files=("3e_2026_v1.json","4e_2026_v1.json","3e_2026_v9_exercices.json","6e_2026_v10.json","5e_2026_v10.json","3e_2026_v10_3_refresh.json","4e_2026_v10_3_refresh.json","5e_2026_v10_3_refresh.json","6e_2026_v10_3_refresh.json","3e_2026_v10_3_exercises_refresh.json","3e_2026_v10_4_refresh.json","4e_2026_v10_4_refresh.json","5e_2026_v10_4_refresh.json","6e_2026_v10_4_refresh.json","3e_2026_v10_4_exercises_refresh.json","3e_2026_v10_5_refresh.json","4e_2026_v10_5_refresh.json","5e_2026_v10_5_refresh.json","6e_2026_v10_5_refresh.json","3e_2026_v10_5_exercises_refresh.json")
    for file in files: install_content_pack(db,file)
    # A previous admin edit must remain untouched.
    custom=db.query(Lesson).join(Chapter).filter(Chapter.level=='3e',Chapter.title=='Théorème de Thalès',Lesson.title=='Méthode').first()
    custom.body='Contenu personnalisé rédigé dans /admin.'
    x=db.query(Exercise).filter(Exercise.title=='Hypoténuse 7-24').first()
    customguide=db.query(ExerciseGuide).filter_by(exercise_id=x.id).first()
    if customguide is None:
        customguide=ExerciseGuide(exercise_id=x.id)
        db.add(customguide)
    customguide.steps_json=json.dumps(['Guide personnel conservé.'])
    db.commit()
    result=apply_quality_patch(db)
    assert result['lessons_skipped']>=1,result
    assert result['guides_skipped']>=1,result
    assert db.get(Lesson,custom.id).body=='Contenu personnalisé rédigé dans /admin.'
    assert json.loads(db.get(ExerciseGuide,customguide.id).steps_json)==['Guide personnel conservé.']
    pyth=db.query(Exercise).filter(Exercise.title=='Hypoténuse 5-12').first()
    assert len(json.loads(db.query(ExerciseGuide).filter_by(exercise_id=pyth.id).first().steps_json))==4
    thales=db.query(Exercise).filter(Exercise.title=='Longueur Thalès 1').first()
    assert '(DE) est parallèle à (BC)' in thales.statement
    assert apply_quality_patch(db)['status']=='already_applied'
    print('PASS isolated patch preservation / idempotency / targeted content:',result)
finally:
    db.close()
'''
with tempfile.TemporaryDirectory() as directory:
    env=dict(os.environ,PYTHONPATH=str(ROOT/'backend'),DATABASE_URL=f'sqlite:///{Path(directory)/"quality.sqlite"}')
    subprocess.run([sys.executable,'-c',code],cwd=ROOT,env=env,check=True)
