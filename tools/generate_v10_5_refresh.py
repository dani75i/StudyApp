import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / 'backend' / 'content'
PREFIX = '@@studysprint-blocks@@'


def serialize(blocks):
    return PREFIX + json.dumps(blocks, ensure_ascii=False)


def parse(body):
    if isinstance(body, str) and body.startswith(PREFIX):
        return json.loads(body[len(PREFIX):])
    return [{'type': 'paragraph', 'content': str(body)}]


def p(text):
    return {'type': 'paragraph', 'content': text}


def f(text):
    return {'type': 'formula', 'content': text}


def ex(text):
    return {'type': 'example', 'content': text}


def note(text):
    return {'type': 'note', 'content': text}


def lst(items):
    return {'type': 'list', 'items': items}


MANUAL = {}


def set_manual(chapter, lesson, blocks):
    MANUAL[(chapter, lesson)] = blocks


# Obvious coherence fixes for repeated but off-topic examples.
set_manual('Symétrie centrale', 'Comprendre : Symétrie centrale', [
    p('Dans une symétrie centrale de centre O, chaque point et son image sont alignés avec O.'),
    note('Le point O est le milieu du segment reliant un point à son image.'),
    ex('Si le point A a pour image A′ par symétrie centrale de centre O, alors O est le milieu du segment [AA′].'),
])
set_manual('Symétrie centrale', 'Coordonnées', [
    p('Avec un repère centré en O, la symétrie centrale change les signes des coordonnées.'),
    f(r'A(x;y)\longrightarrow A\,\!\prime(-x;-y)'),
    ex(r'Si \(A(2;1)\), alors son image par symétrie centrale de centre O est \(A\,\!\prime(-2;-1)\).'),
])
set_manual('Symétrie centrale', 'Conservation', [
    p('La symétrie centrale conserve les longueurs, les angles, l’alignement et le parallélisme.'),
    ex('Un segment de 4 cm garde une longueur de 4 cm après une symétrie centrale.'),
    note('La figure obtenue a la même forme et la même taille que la figure de départ.'),
])

set_manual('Transformations physiques et chimiques', 'Comprendre : Transformations physiques et chimiques', [
    p('Une transformation physique change l’aspect ou l’état d’une substance sans créer de nouvelle espèce chimique. Une transformation chimique forme au moins une nouvelle espèce chimique.'),
    ex('La glace qui fond est une transformation physique, tandis que le fer qui rouille est une transformation chimique.'),
])
set_manual('Transformations physiques et chimiques', 'Exemple physique', [
    p('Lors d’une transformation physique, on retrouve la même substance avant et après la transformation.'),
    ex('L’eau liquide qui s’évapore devient de la vapeur d’eau : la substance reste de l’eau.'),
])
set_manual('Transformations physiques et chimiques', 'Indices', [
    p('Certains indices montrent qu’une transformation chimique a eu lieu.'),
    lst([
        'apparition d’un gaz ;',
        'formation d’un dépôt ;',
        'changement durable de couleur ;',
        'variation de température.',
    ]),
    ex('Quand du vinaigre réagit avec du bicarbonate, un gaz se forme : c’est un indice de transformation chimique.'),
])

set_manual('L’air et les gaz', 'Comprendre : L’air et les gaz', [
    p('L’air est un mélange de gaz invisible qui occupe de l’espace.'),
    ex('Quand on gonfle un ballon, l’air remplit tout le volume disponible.'),
])
set_manual('L’air et les gaz', 'Gaz', [
    p('Un gaz n’a pas de forme propre et n’a pas de volume propre : il prend la forme et le volume du récipient qui le contient.'),
    ex('Dans une seringue non bouchée, l’air s’adapte immédiatement au volume intérieur de la seringue.'),
])
set_manual('L’air et les gaz', 'Pression', [
    p('Quand on comprime un gaz dans un espace plus petit, sa pression augmente.'),
    ex('Si on pousse le piston d’une seringue bouchée, l’air se comprime et il devient plus difficile d’appuyer.'),
])

set_manual('Sons et vibrations', 'Comprendre : Sons et vibrations', [
    p('Un son est produit par la vibration d’un objet.'),
    ex('Quand on pince une corde de guitare, elle vibre et produit un son.'),
])
set_manual('Sons et vibrations', 'Fréquence', [
    p('La fréquence d’un son se mesure en hertz (Hz) et indique le nombre de vibrations par seconde.'),
    ex('Un diapason qui vibre plus vite produit un son plus aigu.'),
    note('Plus la fréquence est grande, plus le son est aigu.'),
])
set_manual('Sons et vibrations', 'Vide', [
    p('Le son a besoin d’un milieu matériel pour se propager.'),
    ex('Dans l’espace, on ne peut pas entendre un son car il n’y a pas d’air pour le transmettre.'),
])

set_manual('Séparer les mélanges', 'Comprendre : Séparer les mélanges', [
    p('On choisit une méthode de séparation selon la nature du mélange.'),
    ex('L’eau et l’huile forment un mélange hétérogène que l’on peut laisser décanter.'),
])
set_manual('Séparer les mélanges', 'Décantation', [
    p('La décantation permet de séparer les constituants d’un mélange hétérogène en les laissant se séparer au repos.'),
    ex('Dans de l’eau boueuse, les particules solides se déposent au fond après un certain temps.'),
])
set_manual('Séparer les mélanges', 'Évaporation', [
    p('L’évaporation permet de récupérer un solide dissous en faisant disparaître le solvant.'),
    ex('Quand l’eau salée s’évapore, il reste du sel solide.'),
])

GENERIC_EXAMPLES_TO_DROP = {
    'applique la méthode du cours à une situation simple, puis vérifie chaque étape du calcul.',
    'observe la situation étudiée, identifie les grandeurs utiles, puis applique la relation vue dans le cours.',
}


def clean_space(text: str) -> str:
    return re.sub(r'\s+', ' ', text or '').strip()


def normalize_prefix(content: str):
    text = clean_space(content)
    lowered = text.lower()
    if lowered.startswith('à retenir :'):
        return 'note', clean_space(text.split(':', 1)[1])
    if lowered.startswith('vérifie que tu as compris :'):
        return 'note', clean_space(text.split(':', 1)[1])
    if lowered.startswith('objectif :'):
        return 'note', clean_space(text.split(':', 1)[1])
    if lowered.startswith('exemple :'):
        return 'example', clean_space(text.split(':', 1)[1])
    return None, text


def normalize_formula(content: str) -> str:
    return clean_space(content)


def normalize_blocks(blocks):
    result = []
    for block in blocks:
        block_type = block.get('type')
        if block_type == 'formula':
            content = normalize_formula(str(block.get('content', '')))
            if content:
                result.append(f(content))
            continue

        if block_type == 'list':
            items = [clean_space(str(item)) for item in block.get('items', []) if clean_space(str(item))]
            if items:
                result.append(lst(items))
            continue

        content = clean_space(str(block.get('content', '')))
        if not content:
            continue

        normalized_type, content = normalize_prefix(content)
        if block_type == 'example' or normalized_type == 'example':
            if content:
                result.append(ex(content))
        elif block_type == 'note' or normalized_type == 'note':
            if content:
                result.append(note(content))
        else:
            result.append(p(content))

    # remove consecutive duplicates
    deduped = []
    for block in result:
        if deduped and deduped[-1] == block:
            continue
        deduped.append(block)
    return deduped


def extract_example_counts(chapter):
    counts = Counter()
    for lesson in chapter.get('lessons', []):
        blocks = normalize_blocks(parse(lesson['body']))
        for block in blocks:
            if block.get('type') == 'example':
                counts[clean_space(block.get('content', '')).lower()] += 1
    return counts


def normalize_lesson(chapter_title, lesson_title, body, chapter_example_counts, chapter_seen_examples):
    key = (chapter_title, lesson_title)
    if key in MANUAL:
        return serialize(MANUAL[key])

    blocks = normalize_blocks(parse(body))
    cleaned = []
    for block in blocks:
        if block.get('type') != 'example':
            cleaned.append(block)
            continue
        content = clean_space(block.get('content', ''))
        lowered = content.lower()
        if lowered in GENERIC_EXAMPLES_TO_DROP:
            continue
        if chapter_example_counts[lowered] > 1:
            if lowered in chapter_seen_examples:
                continue
            chapter_seen_examples.add(lowered)
        cleaned.append(ex(content))

    return serialize(cleaned)


PACKS = [
    ('3e_2026_v10_4_refresh.json', '3e_2026_v10_5_refresh.json', '3e-2026-v10-5-refresh', 'Cours 3e — v10.5 formules, exemples et cohérence'),
    ('4e_2026_v10_4_refresh.json', '4e_2026_v10_5_refresh.json', '4e-2026-v10-5-refresh', 'Cours 4e — v10.5 formules, exemples et cohérence'),
    ('5e_2026_v10_4_refresh.json', '5e_2026_v10_5_refresh.json', '5e-2026-v10-5-refresh', 'Cours 5e — v10.5 formules, exemples et cohérence'),
    ('6e_2026_v10_4_refresh.json', '6e_2026_v10_5_refresh.json', '6e-2026-v10-5-refresh', 'Cours 6e — v10.5 formules, exemples et cohérence'),
    ('3e_2026_v10_4_exercises_refresh.json', '3e_2026_v10_5_exercises_refresh.json', '3e-2026-v10-5-exercises-refresh', 'Compléments 3e — v10.5 formules, exemples et cohérence'),
]


for src_name, out_name, pack_id, title in PACKS:
    data = json.loads((BASE / src_name).read_text(encoding='utf-8'))
    data['pack_id'] = pack_id
    data['title'] = title
    for chapter in data.get('chapters', []):
        chapter_example_counts = extract_example_counts(chapter)
        chapter_seen_examples = set()
        for lesson in chapter.get('lessons', []):
            lesson['body'] = normalize_lesson(chapter['title'], lesson['title'], lesson['body'], chapter_example_counts, chapter_seen_examples)
    (BASE / out_name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('wrote', out_name)
