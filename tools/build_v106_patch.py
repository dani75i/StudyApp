"""Generate a narrowly scoped V10.6 patch based on shipped V10.5 records.
Changes are guarded at application time; edited admin records are not overwritten.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'backend' / 'content'
PREFIX = '@@studysprint-blocks@@'
PACKS = ['3e_2026_v10_5_refresh.json','4e_2026_v10_5_refresh.json',
         '5e_2026_v10_5_refresh.json','6e_2026_v10_5_refresh.json',
         '3e_2026_v10_5_exercises_refresh.json']
ORIGINALS = ['3e_2026_v1.json','4e_2026_v1.json', '3e_2026_v9_exercices.json']

def P(text): return {'type': 'paragraph', 'content': text}
def F(formula): return {'type': 'formula', 'content': formula}
def E(text): return {'type': 'example', 'content': text}
def N(text): return {'type': 'note', 'content': text}
def L(*items): return {'type':'list','items':list(items)}

def body(blocks): return PREFIX + json.dumps(blocks, ensure_ascii=False)

def old_lesson(level, chapter, title):
    candidates=[]
    for file in PACKS:
        doc=json.loads((CONTENT/file).read_text(encoding='utf-8'))
        for ch in doc['chapters']:
            if (ch['level'],ch['title']) == (level,chapter):
                candidates.extend(l['body'] for l in ch['lessons'] if l['title']==title)
    return list(dict.fromkeys(candidates))

LESSONS = {}
def update(level, chapter, title, blocks):
    originals=old_lesson(level,chapter,title)
    assert originals, (level,chapter,title)
    LESSONS[(level,chapter,title)]={'level':level,'chapter':chapter,'title':title,
         'expected_bodies':originals,'body':body(blocks)}

# Correct the theorem, its ratios, and one distinct example per Thalès skill.
update('3e','Théorème de Thalès','Configuration',[
 P('Dans le triangle ABC, D appartient à [AB], E appartient à [AC] et les droites (DE) et (BC) sont parallèles.'),
 P('Les trois rapports de côtés correspondants sont égaux :'),
 F(r'\frac{AD}{AB}=\frac{AE}{AC}=\frac{DE}{BC}'),
 N('Repère le sommet A commun aux deux triangles et écris les rapports dans le même ordre.'),
])
update('3e','Théorème de Thalès','Méthode',[
 P('Pour chercher une longueur, vérifie d’abord l’alignement des points et le parallélisme, écris les rapports correspondants, puis isole l’inconnue.'),
 F(r'\frac{AD}{AB}=\frac{AE}{AC}'),
 E(r'Si (DE) est parallèle à (BC), avec \(AD=2\) cm, \(AB=6\) cm et \(AC=9\) cm, alors \(\frac{2}{6}=\frac{AE}{9}\). On obtient \(AE=\frac{2\times9}{6}=3\) cm.'),
])
update('3e','Théorème de Thalès','Agrandissement/réduction',[
 P('Lorsque les triangles ADE et ABC sont en configuration de Thalès, on peut passer du petit triangle au grand par un même coefficient k :'),
 F(r'k=\frac{AB}{AD}=\frac{AC}{AE}=\frac{BC}{DE}'),
 P('Si k > 1, les longueurs sont agrandies ; pour passer du grand triangle au petit, on utilise le coefficient inverse 1/k, compris entre 0 et 1.'),
 E(r'Si \(AD=2\) cm et \(AB=6\) cm, alors \(k=\frac{6}{2}=3\). Un segment de 4 cm du petit triangle correspond à un segment de 12 cm du grand triangle.'),
])
update('3e','Transformations et homothéties','Isométries',[
 P('Une isométrie conserve les longueurs et les angles : la figure obtenue a la même forme et la même taille.'),
 E('Une translation qui déplace un segment de 3 cm vers la droite ne change pas sa longueur : le segment mesure toujours 3 cm.'),
])
update('4e','Translations et rotations','Translation',[
 P('Une translation déplace tous les points d’une figure selon le même déplacement, sans modifier sa forme, sa taille ni son orientation.'),
 E('Une figure translatée de 4 cm vers la droite conserve toutes ses longueurs et ses angles.'),
])
update('6e','Durées et horaires','Calculer une durée',[
 P('Pour calculer une durée, on soustrait l’heure de départ à l’heure d’arrivée, en tenant compte du passage éventuel à l’heure suivante.'),
 E('Un cours commence à 14 h 25 et finit à 15 h 10 : de 14 h 25 à 15 h il y a 35 minutes, puis 10 minutes. La durée est donc 45 minutes.'),
])
update('6e','Angles et instruments','Angles complémentaires',[
 P('Deux angles sont complémentaires lorsque la somme de leurs mesures est égale à 90°.'),
 F(r'\alpha+\beta=90^\circ'),
 E('Si un angle mesure 35°, son angle complémentaire mesure 90° − 35° = 55°.'),
])
update('3e','Fonctions : images et antécédents','Avec une formule',[
 P('Pour calculer une image, on remplace x par la valeur demandée. Pour trouver un antécédent, on résout une équation.'),
 F(r'f(x)=2x+1'),
 E(r'L’image de 3 est \(f(3)=2\times3+1=7\). Pour trouver un antécédent de 7, on résout \(2x+1=7\) : \(x=3\).'),
])
update('3e','Circuits électriques : tension et intensité','Mesures',[
 P('On mesure l’intensité I en ampères (A) avec un ampèremètre branché en série ; la tension U se mesure en volts (V) avec un voltmètre branché en dérivation.'),
 E('Pour mesurer la tension aux bornes d’une lampe, relie le voltmètre aux deux bornes de la lampe, sans ouvrir le circuit.'),
])
update('4e','Lumière et propagation','Sources et objets diffusants',[
 P('Une source primaire produit sa propre lumière. Un objet diffusant devient visible parce qu’il renvoie la lumière reçue.'),
 E('Le Soleil est une source primaire. La Lune renvoie la lumière du Soleil : c’est un objet diffusant.'),
])

EXERCISES=[]
STATEMENTS=[]
for file in ORIGINALS:
    doc=json.loads((CONTENT/file).read_text(encoding='utf-8'))
    for ch in doc['chapters']:
        if ch['title']!='Théorème de Pythagore': continue
        for x in ch['exercises']:
            stmt=x['statement']; title=x['title']; answer=x['correct_answer']
            steps=[]
            m=re.search(r'(?:côtés de l[’\']angle droit|côtés de l[’\']angle droit)\s*(\d+)\s*cm\s*et\s*(\d+)\s*cm',stmt)
            if m and 'Hypoténuse' in stmt:
                a,b=map(int,m.groups()); sq=a*a+b*b
                assert int(answer)**2==sq, (stmt,answer)
                steps=['Le triangle est rectangle. L’hypoténuse est le côté opposé à l’angle droit.',
                    r'On applique le théorème de Pythagore : \[c^2=a^2+b^2\]',
                    rf'\[c^2={a}^2+{b}^2={a*a}+{b*b}={sq}\]',
                    rf'\[c=\sqrt{{{sq}}}={answer}\ \text{{cm}}\] L’hypoténuse mesure {answer} cm.']
            elif title.startswith('Hypoténuse '):
                a,b=map(int,re.search(r'(\d+)-(\d+)',title).groups()); sq=a*a+b*b
                assert int(answer)**2==sq
                steps=['Les deux longueurs connues sont les côtés de l’angle droit.',
                    r'On applique Pythagore : \[c^2=a^2+b^2\]',
                    rf'\[c^2={a}^2+{b}^2={sq}\]',
                    rf'\[c=\sqrt{{{sq}}}={answer}\ \text{{cm}}\]']
            elif title.startswith('Côté manquant '):
                a,c=map(int,re.search(r'(\d+)-(\d+)',title).groups()); sq=c*c-a*a
                assert int(answer)**2==sq
                steps=['L’hypoténuse est le plus long côté du triangle rectangle.',
                    r'On applique Pythagore, puis on isole le carré de la longueur cherchée : \[b^2=c^2-a^2\]',
                    rf'\[b^2={c}^2-{a}^2={sq}\]',
                    rf'\[b=\sqrt{{{sq}}}={answer}\ \text{{cm}}\]']
            elif title.startswith('Triangle '):
                nums=list(map(int,re.search(r'(\d+)-(\d+)-(\d+)',title).groups())); a,b,c=sorted(nums)
                assert ((a*a+b*b==c*c) == (answer=='Oui'))
                steps=['On repère le plus long côté du triangle.',
                    rf'On calcule son carré : \[{c}^2={c*c}\]',
                    rf'On calcule la somme des carrés des deux autres côtés : \[{a}^2+{b}^2={a*a}+{b*b}={a*a+b*b}\]',
                    ('Les deux nombres sont égaux : le triangle est rectangle, par la réciproque de Pythagore.' if answer=='Oui' else 'Les deux nombres sont différents : le triangle n’est pas rectangle, par la contraposée du théorème de Pythagore.')]
            elif ch['level']=='4e' and '3,4,5 cm' in title:
                steps=['On repère le plus long côté : 5 cm.',r'\[5^2=25\]',r'\[3^2+4^2=9+16=25\]',
                   'Les deux nombres sont égaux : le triangle est rectangle (réciproque de Pythagore).']
            elif ch['level']=='4e' and '5, 7 et 9' in title:
                steps=['Le plus long côté mesure 9 cm.',r'\[9^2=81\]',r'\[5^2+7^2=25+49=74\]',
                   '81 et 74 sont différents : le triangle n’est pas rectangle.']
            elif ch['level']=='4e' and ('hypoténuse 10' in stmt or 'hypoténuse 15' in stmt):
                c=int(re.search(r'hypoténuse\s*(\d+)',stmt,re.I).group(1))
                a=int(re.search(r'autre côté\s*(\d+)',stmt,re.I).group(1)); sq=c*c-a*a
                assert int(answer)**2==sq
                steps=['On connaît l’hypoténuse et un côté de l’angle droit.',r'\[b^2=c^2-a^2\]',
                    rf'\[b^2={c}^2-{a}^2={sq}\]',rf'\[b=\sqrt{{{sq}}}={answer}\ \text{{cm}}\]']
            elif ch['level']=='4e' and 'rectangle mesure 6' in stmt:
                steps=['La diagonale d’un rectangle est l’hypoténuse du triangle rectangle formé par ses côtés.',
                    r'\[d^2=6^2+8^2=36+64=100\]',r'\[d=\sqrt{100}=10\ \text{cm}\]']
            elif ch['level']=='4e' and ('côtés de l’angle droit 5' in stmt or 'côtés de l’angle droit 3' in stmt):
                mm=re.search(r'(\d+)\s*cm\s*et\s*(\d+)\s*cm',stmt); a,b=map(int,mm.groups()); sq=a*a+b*b
                assert int(answer)**2==sq
                steps=['Le triangle est rectangle. On cherche l’hypoténuse.',r'\[c^2=a^2+b^2\]',
                    rf'\[c^2={a}^2+{b}^2={sq}\]',rf'\[c=\sqrt{{{sq}}}={answer}\ \text{{cm}}\]']
            elif ch['level']=='4e' and 'quelle est l’hypoténuse' in stmt:
                steps=['L’hypoténuse est le côté opposé à l’angle droit.',
                       'Le triangle ABC est rectangle en A : le côté opposé est [BC].']
            if steps:
                EXERCISES.append({'level':ch['level'],'chapter':ch['title'],'title':title,
                    'expected_correction':x['correction'],'steps':steps})

# Original legacy Thalès exercises omitted the essential parallel-lines hypothesis.
original=json.loads((CONTENT/'3e_2026_v1.json').read_text(encoding='utf-8'))
thal = next(ch for ch in original['chapters'] if ch['title']=='Théorème de Thalès')
for x in thal['exercises']:
    match = re.fullmatch(r'AB/AC=(\d+)/(\d+) et AD=(\d+) cm correspond à AB\. Quelle est AE \?',x['statement'])
    if not match: continue
    a,b,ad=map(int,match.groups())
    assert ad*b % a ==0 and str(ad*b//a)==str(x['correct_answer'])
    STATEMENTS.append({'level':'3e','chapter':'Théorème de Thalès','title':x['title'],
      'expected_statement':x['statement'],
      'statement':(f'Dans le triangle ABC, D appartient à [AB], E appartient à [AC] et (DE) est parallèle à (BC). '
                   f'On sait que AB/AC = {a}/{b} et AD = {ad} cm. Quelle est la longueur AE (en cm) ?'),
      'expected_correction':x['correction'],
      'steps':['Les points sont alignés et (DE) est parallèle à (BC) : on peut appliquer le théorème de Thalès.',
         r'\[\frac{AD}{AB}=\frac{AE}{AC}\]',
         rf'Puisque \(\frac{{AB}}{{AC}}=\frac{{{a}}}{{{b}}}\), on a aussi : \[\frac{{AD}}{{AE}}=\frac{{{a}}}{{{b}}}\]',
         rf'\[AE=\frac{{{ad}\times{b}}}{{{a}}}={x["correct_answer"]}\ \text{{cm}}\]']})

OUT={'slug':'quality-v10-6','title':'V10.6 — corrections ciblées et démarches Pythagore',
    'lessons':list(LESSONS.values()),'guides':EXERCISES,'statement_patches':STATEMENTS}
(CONTENT/'quality_v106.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2),encoding='utf-8')
print('LESSON PATCHES',len(OUT['lessons']),'PYTHAGORE GUIDES',len(OUT['guides']),'THALES STATEMENTS',len(OUT['statement_patches']))
