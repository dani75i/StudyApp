"""Automated audit for V10.7 shipped content.

Checks source-file structure and known regressions; this is not an exhaustive
mathematical or pedagogical certification of every exercise.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT/'backend'/'content'
FILES = ['3e_2026_v10_5_refresh.json', '4e_2026_v10_5_refresh.json',
         '5e_2026_v10_5_refresh.json', '6e_2026_v10_5_refresh.json',
         '3e_2026_v10_5_exercises_refresh.json']
COUNTS = Counter()
ISSUES = []
BASE = {}
EXERCISES = {}
CHAPTERS = set()


def issue(key, why):
    ISSUES.append({'lesson_or_exercise': key, 'issue': why})


for filename in FILES:
    data = json.loads((CONTENT/filename).read_text(encoding='utf-8'))
    for chap in data['chapters']:
        key = chap['level'], chap['subject'], chap['title']
        CHAPTERS.add(key)
        for les in chap.get('lessons', []):
            lkey = chap['level'], chap['title'], les['title']
            if lkey in BASE: issue(lkey, 'leçon dupliquée')
            BASE[lkey] = les['body']
        for ex in chap.get('exercises', []):
            ekey = chap['level'], chap['title'], ex['title']
            if ekey in EXERCISES: issue(ekey, 'exercice dupliqué')
            EXERCISES[ekey] = ex
            if not ex['statement'].strip() or not ex['correction'].strip() or not str(ex['correct_answer']).strip():
                issue(ekey, 'énoncé/correction/réponse manquant')
            if ex['exercise_type'] == 'mcq' and str(ex['correct_answer']) not in ex.get('options', []):
                issue(ekey, 'réponse QCM absente des choix')

v106 = json.loads((CONTENT/'quality_v106.json').read_text(encoding='utf-8'))
v107 = json.loads((CONTENT/'quality_v107.json').read_text(encoding='utf-8'))
for data in [v106, v107]:
    for row in data['lessons']:
        key = row['level'], row['chapter'], row['title']
        if key not in BASE: issue(key, 'patch sans leçon correspondante')
        BASE[key] = row['body']

for key, body in BASE.items():
    if not body.startswith('@@studysprint-blocks@@'):
        issue(key, 'leçon non structurée')
        continue
    try:
        blocks = json.loads(body.split('@@studysprint-blocks@@', 1)[1])
    except json.JSONDecodeError:
        issue(key, 'blocs JSON invalides')
        continue
    if not isinstance(blocks, list) or not blocks:
        issue(key, 'fiche vide')
        continue
    for block in blocks:
        if block['type'] not in ('paragraph', 'formula', 'note', 'example', 'list'):
            issue(key, 'type de bloc inconnu')
        if block['type'] == 'formula':
            COUNTS['formula_blocks'] += 1
            content = block['content']
            if not content or content.count('{') != content.count('}'):
                issue(key, 'formule vide ou accolades déséquilibrées')
        elif block['type'] == 'example':
            COUNTS['example_blocks'] += 1
            content = block['content']
            if not content.strip() or content.count('\\(') != content.count('\\)'):
                issue(key, 'exemple vide ou délimiteurs LaTeX mal formés')
            if '\\(' in content:
                COUNTS['examples_with_explicit_math'] += 1
    # Regression tests on screenshots from the user.
    if key == ('3e', 'Théorème de Thalès', 'Agrandissement/réduction') and '(x+2)' in body:
        issue(key, 'exemple de distributivité hors sujet')
    if key == ('3e', 'Statistiques', 'Moyenne') and 'Moyenne=somme' in body:
        issue(key, 'formule en texte brut')
    if key == ('3e', 'Racines carrées', 'Définition') and '√a est' in body:
        issue(key, 'racine non rendue en LaTeX')

COUNTS.update({'chapters': len(CHAPTERS), 'lessons': len(BASE), 'exercises': len(EXERCISES),
               'revised_lessons_v107': len(v107['lessons']), 'issues': len(ISSUES)})
report = {
    'scope': 'Catalogue livré avec superposition des modifications V10.6 et V10.7 ; pas les modifications de la base de production.',
    'counts': dict(COUNTS),
    'issues': ISSUES,
    'limits': [
        'Le contrôle des 1128 exercices est surtout structurel : aucune validation mathématique exhaustive n’a été réalisée.',
        'Aucune lecture de la base Neon ni des modifications en production dans /admin.',
        'Le rendu KaTeX n’a pas pu être compilé dans cet environnement faute d’accès au registre npm.',
        'Le test de l’URL publique et le référencement Search Console sont des chantiers distincts.',
    ],
}
(ROOT/'QUALITY_AUDIT_V10_7.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(COUNTS, ensure_ascii=False))
for error in ISSUES[:20]: print('FLAG', error)
if ISSUES: raise SystemExit(1)
