"""Deterministic audit of SHIPPED content, not a claim of teacher validation.
Run at the repository root: python tools/audit_v106.py
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT/'backend'/'content'
PREFIX = '@@studysprint-blocks@@'
FILES = [
    '3e_2026_v10_5_refresh.json', '4e_2026_v10_5_refresh.json',
    '5e_2026_v10_5_refresh.json', '6e_2026_v10_5_refresh.json',
    '3e_2026_v10_5_exercises_refresh.json',
]
PATCH = json.loads((CONTENT/'quality_v106.json').read_text(encoding='utf-8'))
lesson_patch = {(x['level'],x['chapter'],x['title']):x for x in PATCH['lessons']}
statement_patch = {(x['level'],x['chapter'],x['title']):x for x in PATCH['statement_patches']}
counts = Counter()
issues = []
seen_exercises = set()
seen_lessons = set()
chapters = set()


def flag(code, level, chapter, title, message):
    issues.append({'code':code, 'level':level, 'chapter':chapter, 'title':title, 'detail':message})


for filename in FILES:
    data=json.loads((CONTENT/filename).read_text(encoding='utf-8'))
    for chapter in data['chapters']:
        level, name=chapter['level'],chapter['title']
        chapters.add((level,chapter['subject'],name))
        for lesson in chapter['lessons']:
            key=(level,name,lesson['title'])
            if key in seen_lessons:
                flag('duplicate_lesson',*key,'Leçon répétée dans plusieurs packs')
                continue
            seen_lessons.add(key)
            counts['lessons']+=1
            body=lesson_patch.get(key,{}).get('body',lesson['body'])
            if not body.startswith(PREFIX):
                flag('lesson_plain_text',*key,'Contenu non structuré')
                continue
            try:
                blocks=json.loads(body[len(PREFIX):])
            except (ValueError, TypeError):
                flag('invalid_lesson_json',*key,'Structure JSON invalide')
                continue
            if not isinstance(blocks,list) or not blocks:
                flag('empty_lesson',*key,'Leçon sans blocs')
                continue
            formula_count=sum(b.get('type')=='formula' for b in blocks)
            counts['formula_blocks']+=formula_count
            counts['example_blocks']+=sum(b.get('type')=='example' for b in blocks)
            for b in blocks:
                if b.get('type') not in ('paragraph','formula','example','note','list'):
                    flag('unknown_block_type',*key,str(b.get('type')))
                if b.get('type')=='formula':
                    formula=str(b.get('content','')).strip()
                    if not formula or formula.startswith(('\\[','\\(')):
                        flag('bad_formula',*key,formula)
                    if formula.count('{')!=formula.count('}'):
                        flag('unbalanced_formula',*key,formula)
                if b.get('type')=='example' and not str(b.get('content','')).strip():
                    flag('empty_example',*key,'Exemple vide')
            # High-confidence topic-mismatch regression checks for previously spotted defects.
            all_examples=' '.join(b.get('content','') for b in blocks if b.get('type')=='example').lower()
            if name=='Théorème de Thalès' and ('distribue' in all_examples or '(x+2)' in all_examples):
                flag('off_topic_example',*key,'Distributivité dans Thalès')
            if name=='Durées et horaires' and 'rectangle de longueur' in all_examples:
                flag('off_topic_example',*key,'Aire du rectangle dans le calcul de durée')
            if name=='Translations et rotations' and lesson['title']=='Translation' and 'homothétie' in all_examples:
                flag('off_topic_example',*key,'Homothétie dans la translation')
            if name=='Angles et instruments' and lesson['title']=='Angles complémentaires' and 'rectangle de longueur' in all_examples:
                flag('off_topic_example',*key,'Aire du rectangle dans les angles')
        for exercise in chapter['exercises']:
            key=(level,name,exercise['title'])
            if key in seen_exercises:
                flag('duplicate_exercise',*key,'Exercice répété dans plusieurs packs')
                continue
            seen_exercises.add(key)
            counts['exercises']+=1
            statement=statement_patch.get(key,{}).get('statement',exercise['statement'])
            answer=str(exercise.get('correct_answer','')).strip()
            if not statement.strip() or not answer or not exercise['correction'].strip():
                flag('missing_exercise_field',*key,'Énoncé, réponse ou correction manquants')
            if exercise['exercise_type']=='mcq':
                options=exercise.get('options',[])
                if answer not in options:
                    flag('mcq_answer_not_in_options',*key,'Réponse attendue absente des choix')
                if len(options)!=len(set(options)):
                    flag('duplicate_mcq_option',*key,'Choix identiques')
            if exercise.get('difficulty') not in (1,2,3):
                flag('bad_difficulty',*key,'Difficulté en dehors de 1–3')
            if name=='Théorème de Thalès' and exercise['title'].startswith('Longueur Thalès'):
                if '(DE) est parallèle à (BC)' not in statement:
                    flag('missing_thales_hypothesis',*key,'Hypothèse de parallélisme absente')

counts['chapters']=len(chapters)
counts['patched_lessons']=len(lesson_patch)
counts['patched_statements']=len(statement_patch)
counts['new_pythagoras_guides']=len(PATCH['guides'])
counts['issues']=len(issues)
report={'scope':'Contenus fournis dans la V10.6, avec corrections V10.6 appliquées en mémoire.',
        'counters':dict(counts),'issues':issues,
        'limits':['Contrôles de structure, cohérence ciblée et calculs des exercices de Pythagore réécrits ; pas de certification humaine de toutes les solutions.',
                  'Les fiches modifiées sur le site via /admin ne sont pas inspectées par cet audit hors ligne.',
                  'Un bloc KaTeX équilibré peut malgré tout contenir une erreur mathématique.']}
(ROOT/'QUALITY_AUDIT_V10_6.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(counts,ensure_ascii=False))
for issue in issues[:20]: print('FLAG', issue)
if issues: raise SystemExit(1)
