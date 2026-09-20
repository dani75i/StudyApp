import json
import re
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


# --- Manual refinements for the most formula-sensitive lessons ---
set_manual('Identités remarquables et développement', 'Carré d’une somme', [
    p("L’identité remarquable du carré d’une somme permet de développer rapidement une expression."),
    f(r'(a+b)^2=a^2+2ab+b^2'),
    ex(r'Avec \(a=x\) et \(b=4\), on obtient \((x+4)^2=x^2+8x+16\).'),
    note('Le terme du milieu est toujours le double produit 2ab.'),
])
set_manual('Identités remarquables et développement', 'Carré d’une différence', [
    p("Le carré d’une différence ressemble au carré d’une somme, mais le terme du milieu change de signe."),
    f(r'(a-b)^2=a^2-2ab+b^2'),
    ex(r'Avec \(a=x\) et \(b=3\), on obtient \((x-3)^2=x^2-6x+9\).'),
    note('Le dernier terme reste positif car \(b^2\) est toujours positif.'),
])
set_manual('Identités remarquables et développement', 'Conjugués', [
    p('Le produit de deux conjugués fait disparaître les termes croisés.'),
    f(r'(a-b)(a+b)=a^2-b^2'),
    ex(r'Avec \(a=x\) et \(b=5\), on obtient \((x-5)(x+5)=x^2-25\).'),
    note('Cette identité est très utile pour factoriser ou développer rapidement.'),
])

set_manual('Fonctions linéaires et affines', 'Fonction linéaire', [
    p('Une fonction linéaire est une fonction de la forme suivante :'),
    f(r'f(x)=ax'),
    p('Sa représentation graphique est une droite qui passe par l’origine.'),
    ex(r'Si \(f(x)=3x\), alors \(f(4)=3\times4=12\). L’image de 4 est donc 12.'),
])
set_manual('Fonctions linéaires et affines', 'Fonction affine', [
    p('Une fonction affine est une fonction de la forme suivante :'),
    f(r'f(x)=ax+b'),
    p('Le nombre a est le coefficient directeur et b l’ordonnée à l’origine.'),
    ex(r'Si \(f(x)=2x+1\), alors \(f(3)=2\times3+1=7\). L’image de 3 est donc 7.'),
])
set_manual('Fonctions linéaires et affines', 'Interprétation', [
    p('Dans une fonction affine, chaque nombre a un rôle précis.'),
    f(r'f(x)=ax+b'),
    lst([
        'a est le coefficient directeur : il indique comment la droite monte ou descend.',
        'b est l’ordonnée à l’origine : c’est la valeur de la fonction pour x = 0.',
    ]),
    ex(r'Pour \(f(x)=2x+5\), on a \(a=2\) et \(b=5\). La droite coupe donc l’axe des ordonnées au point \((0;5)\).'),
])

set_manual('Théorème de Pythagore', 'Théorème', [
    p('Dans un triangle rectangle, le carré de l’hypoténuse est égal à la somme des carrés des deux autres côtés.'),
    f(r'BC^2=AB^2+AC^2'),
    ex(r'Dans un triangle ABC rectangle en A, si \(AB=3\) cm et \(AC=4\) cm, alors \(BC^2=3^2+4^2=25\), donc \(BC=5\) cm.'),
    note('L’hypoténuse est toujours le côté opposé à l’angle droit.'),
])
set_manual('Théorème de Pythagore', "Calcul d'une longueur", [
    p('Pour calculer une longueur dans un triangle rectangle, on applique le théorème de Pythagore puis on isole la longueur cherchée.'),
    f(r'BC=\sqrt{AB^2+AC^2}'),
    f(r'AB=\sqrt{BC^2-AC^2}'),
    ex(r'Si \(BC=13\) cm et \(AC=5\) cm, alors \(AB=\sqrt{13^2-5^2}=\sqrt{169-25}=\sqrt{144}=12\) cm.'),
])
set_manual('Théorème de Pythagore', 'Réciproque', [
    p('La réciproque permet de savoir si un triangle est rectangle.'),
    f(r'\text{Si }BC^2=AB^2+AC^2\text{, alors le triangle ABC est rectangle en A.}'),
    ex(r'Si un triangle a pour côtés 6 cm, 8 cm et 10 cm, alors \(6^2+8^2=36+64=100=10^2\). Le triangle est donc rectangle.'),
])

set_manual('Trigonométrie dans le triangle rectangle', 'Trois rapports', [
    p('Dans un triangle rectangle, les rapports trigonométriques d’un angle aigu α sont :'),
    f(r'\sin(\alpha)=\frac{\text{côté opposé}}{\text{hypoténuse}}'),
    f(r'\cos(\alpha)=\frac{\text{côté adjacent}}{\text{hypoténuse}}'),
    f(r'\tan(\alpha)=\frac{\text{côté opposé}}{\text{côté adjacent}}'),
    ex(r'Si, pour un angle \(\alpha\), le côté opposé vaut 3 cm et l’hypoténuse 5 cm, alors \(\sin(\alpha)=\frac{3}{5}\).'),
])
set_manual('Trigonométrie dans le triangle rectangle', 'Choisir', [
    p('On choisit le rapport trigonométrique en fonction des côtés connus et de la longueur recherchée.'),
    lst([
        'utilise le sinus si tu connais le côté opposé et l’hypoténuse ;',
        'utilise le cosinus si tu connais le côté adjacent et l’hypoténuse ;',
        'utilise la tangente si tu connais le côté opposé et le côté adjacent.',
    ]),
    ex(r'Si on connaît l’hypoténuse et le côté adjacent à l’angle, on choisit le cosinus : \(\cos(\alpha)=\frac{\text{adjacent}}{\text{hypoténuse}}\).'),
])
set_manual('Trigonométrie dans le triangle rectangle', 'Calculer', [
    p('Pour calculer une longueur, on écrit le bon rapport trigonométrique puis on remplace par les valeurs connues.'),
    f(r'\cos(60^\circ)=\frac{\text{adjacent}}{\text{hypoténuse}}'),
    ex(r'Si \(\cos(60^\circ)=\frac{x}{10}\), alors \(\frac{1}{2}=\frac{x}{10}\), donc \(x=5\) cm.'),
])

set_manual('Forces, poids et gravitation', 'Force', [
    p('Une force se caractérise par une direction, un sens et une valeur exprimée en newtons.'),
    lst([
        'direction : horizontale, verticale ou oblique ;',
        'sens : vers la droite, vers la gauche, vers le haut… ;',
        'valeur : intensité de la force, en N.',
    ]),
    ex('Une personne qui tire un chariot exerce une force horizontale vers l’avant. Si l’intensité vaut 5 N, on la représente par une flèche de valeur 5 N.'),
])
set_manual('Forces, poids et gravitation', 'Poids', [
    p('Le poids d’un objet est la force d’attraction exercée par la Terre sur cet objet.'),
    f(r'P=m\times g'),
    lst([
        'P : poids en newtons (N)',
        'm : masse en kilogrammes (kg)',
        'g : intensité de la pesanteur, environ 9,8 N/kg sur Terre',
    ]),
    ex(r'Pour un objet de masse \(2\) kg, on calcule \(P=2\times9{,}8=19{,}6\) N. Son poids est donc d’environ 19,6 N.'),
])
set_manual('Forces, poids et gravitation', 'Équilibre', [
    p('Un objet est en équilibre lorsque les forces qui s’exercent sur lui se compensent.'),
    note('Si deux forces ont la même direction, la même valeur et des sens opposés, leur résultante est nulle.'),
    ex('Un livre posé sur une table est en équilibre : son poids agit vers le bas et la réaction de la table agit vers le haut avec la même intensité.'),
])

set_manual('Loi d’Ohm et puissance électrique', 'Résistance', [
    p('La résistance électrique d’un dipôle se mesure en ohms.'),
    note('Plus la résistance est grande, plus elle s’oppose au passage du courant.'),
    ex('Une résistance marquée 100 Ω freine davantage le courant qu’une résistance de 10 Ω.'),
])
set_manual('Loi d’Ohm et puissance électrique', "Loi d'Ohm", [
    p('Pour un conducteur ohmique, la tension, la résistance et l’intensité sont liées par la loi d’Ohm.'),
    f(r'U=R\times I'),
    ex(r'Si \(R=100\ \Omega\) et \(I=0{,}02\) A, alors \(U=100\times0{,}02=2\) V.'),
])
set_manual('Loi d’Ohm et puissance électrique', 'Puissance', [
    p('La puissance électrique d’un appareil dépend de la tension à ses bornes et de l’intensité du courant.'),
    f(r'P=U\times I'),
    ex(r'Si une lampe fonctionne sous \(6\) V avec une intensité de \(0{,}5\) A, alors \(P=6\times0{,}5=3\) W.'),
])

set_manual('Puissances et écriture scientifique', 'Puissances', [
    p('Pour un entier positif n, la puissance aⁿ représente le produit de n facteurs égaux à a.'),
    f(r'a^n=\underbrace{a\times a\times \cdots \times a}_{n\text{ facteurs}}'),
    ex(r'Par exemple, \(2^4=2\times2\times2\times2=16\). De plus, pour tout nombre non nul, \(a^0=1\).'),
])
set_manual('Puissances et écriture scientifique', 'Règles de calcul', [
    p('Avec des puissances de même base, on applique des règles de calcul simples.'),
    f(r'a^m\times a^n=a^{m+n}'),
    f(r'\frac{a^m}{a^n}=a^{m-n}'),
    ex(r'Par exemple, \(10^3\times10^2=10^5\) et \(\frac{10^6}{10^2}=10^4\).'),
])
set_manual('Puissances et écriture scientifique', 'Écriture scientifique', [
    p('Un nombre en écriture scientifique s’écrit sous la forme suivante :'),
    f(r'a\times10^n\qquad 1\le a<10'),
    ex(r'Le nombre \(45\,000\) s’écrit \(4{,}5\times10^4\). La virgule a été déplacée de 4 rangs vers la gauche.'),
])



set_manual('Proportionnalité, pourcentages et vitesses', 'Proportionnalité', [
    p('Deux grandeurs sont proportionnelles si l’on passe de l’une à l’autre en multipliant toujours par le même nombre.'),
    ex('Si 3 cahiers coûtent 6 €, alors 1 cahier coûte 2 € et 5 cahiers coûtent 10 € : le prix est proportionnel au nombre de cahiers.'),
])
set_manual('Proportionnalité, pourcentages et vitesses', 'Pourcentages', [
    p("Pour calculer p % d’une quantité, on multiplie cette quantité par p/100."),
    f(r'\text{pourcentage}=\text{quantité}\times\frac{p}{100}'),
    ex(r'Pour calculer 15 % de 80, on fait \(80\times\frac{15}{100}=12\).'),
])
set_manual('Proportionnalité, pourcentages et vitesses', 'Vitesse moyenne', [
    p('La vitesse moyenne se calcule en divisant la distance parcourue par la durée du trajet.'),
    f(r'v=\frac{d}{t}'),
    ex(r'Une voiture parcourt 150 km en 2 h. On calcule \(v=\frac{150}{2}=75\) km/h.'),
])

set_manual('Proportionnalité et pourcentages', 'Tableau de proportionnalité', [
    p('Dans un tableau de proportionnalité, on passe toujours d’une ligne à l’autre en multipliant par le même coefficient.'),
    ex('Si 4 stylos coûtent 6 €, alors 8 stylos coûtent 12 € : le prix est proportionnel au nombre de stylos.'),
])
set_manual('Proportionnalité et pourcentages', 'Pourcentages', [
    p("Pour calculer p % d’une quantité, on multiplie cette quantité par p/100."),
    f(r'\text{pourcentage}=\text{quantité}\times\frac{p}{100}'),
    ex(r'Pour calculer 25 % de 60, on fait \(60\times\frac{25}{100}=15\).'),
])
set_manual('Proportionnalité et pourcentages', 'Échelles et vitesse constante', [
    p('Une vitesse constante signifie que l’on parcourt des distances proportionnelles au temps.'),
    f(r'v=\frac{d}{t}'),
    ex(r'Si un cycliste parcourt 30 km en 2 h, sa vitesse moyenne est \(v=\frac{30}{2}=15\) km/h.'),
])

set_manual('Pourcentages simples', 'Comprendre : Pourcentages simples', [
    p('Un pourcentage représente une fraction sur 100.'),
    f(r'p\%=\frac{p}{100}'),
    ex(r'\(25\%\) signifie \(\frac{25}{100}=\frac{1}{4}\).'),
])
set_manual('Pourcentages simples', 'Pourcentages usuels', [
    p('Certains pourcentages courants correspondent à des fractions simples.'),
    lst(['50 % = 1/2', '25 % = 1/4', '10 % = 1/10']),
    ex('25 % d’une tarte, c’est un quart de la tarte.'),
])
set_manual('Pourcentages simples', 'Pourcentage d’une quantité', [
    p('Pour calculer un pourcentage d’une quantité, on multiplie la quantité par le pourcentage écrit sous forme décimale.'),
    f(r'\text{pourcentage}=\text{quantité}\times\frac{p}{100}'),
    ex(r'Pour calculer 15 % de 80, on fait \(80\times\frac{15}{100}=12\).'),
])


def split_example_blocks(blocks):
    main = []
    ex_blocks = []
    in_example = False
    for block in blocks:
        if block.get('type') == 'paragraph':
            content = str(block.get('content', '')).strip()
            if content.lower().startswith('exemple'):
                in_example = True
                rest = content.split(':', 1)[1].strip() if ':' in content else ''
                if rest:
                    ex_blocks.append({'type': 'paragraph', 'content': rest})
                continue
        if in_example:
            ex_blocks.append(block)
        else:
            main.append(block)
    return main, ex_blocks


def build_example_text(example_blocks):
    parts = []
    for block in example_blocks:
        block_type = block.get('type')
        if block_type == 'formula':
            parts.append(rf"\({block.get('content', '')}\)")
        elif block_type == 'paragraph':
            content = str(block.get('content', '')).strip()
            if content and content.lower() != 'exemple :':
                parts.append(content)
        elif block_type == 'note':
            content = str(block.get('content', '')).strip()
            if content:
                parts.append(content)
        elif block_type == 'list':
            items = [str(item).strip() for item in block.get('items', []) if str(item).strip()]
            if items:
                parts.append(' ; '.join(items))
    text = ' '.join(parts)
    return re.sub(r'\s+', ' ', text).strip()


def chapter_has_same_examples(chapter):
    payloads = []
    for lesson in chapter.get('lessons', []):
        _, ex_blocks = split_example_blocks(parse(lesson['body']))
        payloads.append(build_example_text(ex_blocks) or None)
    unique = {payload for payload in payloads if payload}
    return len(unique) == 1 and len(payloads) >= 2, (next(iter(unique)) if unique else None)


def title_prefers_example(lesson_title, example_text):
    title = lesson_title.lower()
    example = example_text.lower()
    if 'poids' in title and 'p=' in example:
        return True
    if 'vitesse' in title and 'v=' in example:
        return True
    if 'puissance' in title and ('p=' in example or 'e=' in example):
        return True
    if "loi d" in title and 'u=' in example:
        return True
    if 'écriture scientifique' in title and '10^' in example:
        return True
    if 'masse volumique' in title and ('rho' in example or '\\rho' in example):
        return True
    if 'avec une formule' in title and 'f(x)' in example:
        return True
    if 'calcul' in title and ('=' in example or '\\sqrt' in example):
        return True
    if 'relation' in title and '=' in example:
        return True
    return False


def generic_transform(chapter_title, lesson_title, body, same_example=False, shared_example=None):
    blocks = parse(body)
    main, example_blocks = split_example_blocks(blocks)
    main = [block for block in main if not (block.get('type') == 'paragraph' and not str(block.get('content', '')).strip())]
    example_text = build_example_text(example_blocks)

    if same_example and shared_example and example_text and not title_prefers_example(lesson_title, shared_example):
        example_text = ''

    if not any(block.get('type') == 'formula' for block in main) and any(block.get('type') == 'formula' for block in example_blocks):
        if title_prefers_example(lesson_title, example_text):
            first_formula = next(block.get('content', '') for block in example_blocks if block.get('type') == 'formula')
            main.append({'type': 'formula', 'content': first_formula})
            example_text = re.sub(r'^\\\([^)]*\\\)\s*', '', example_text).strip()

    result = list(main)
    if example_text:
        result.append(ex(example_text))
    return serialize(result)


PACKS = [
    ('3e_2026_v10_3_refresh.json', '3e_2026_v10_4_refresh.json', '3e-2026-v10-4-refresh', 'Cours 3e — v10.4 formules et exemples'),
    ('4e_2026_v10_3_refresh.json', '4e_2026_v10_4_refresh.json', '4e-2026-v10-4-refresh', 'Cours 4e — v10.4 formules et exemples'),
    ('5e_2026_v10_3_refresh.json', '5e_2026_v10_4_refresh.json', '5e-2026-v10-4-refresh', 'Cours 5e — v10.4 formules et exemples'),
    ('6e_2026_v10_3_refresh.json', '6e_2026_v10_4_refresh.json', '6e-2026-v10-4-refresh', 'Cours 6e — v10.4 formules et exemples'),
    ('3e_2026_v10_3_exercises_refresh.json', '3e_2026_v10_4_exercises_refresh.json', '3e-2026-v10-4-exercises-refresh', 'Compléments 3e — v10.4 formules et exemples'),
]

for src_name, out_name, pack_id, title in PACKS:
    data = json.loads((BASE / src_name).read_text(encoding='utf-8'))
    data['pack_id'] = pack_id
    data['title'] = title
    for chapter in data.get('chapters', []):
        same_example, shared_example = chapter_has_same_examples(chapter)
        for lesson in chapter.get('lessons', []):
            key = (chapter['title'], lesson['title'])
            if key in MANUAL:
                lesson['body'] = serialize(MANUAL[key])
            else:
                lesson['body'] = generic_transform(chapter['title'], lesson['title'], lesson['body'], same_example, shared_example)
    (BASE / out_name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('wrote', out_name)
