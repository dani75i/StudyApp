"""Generate narrow content updates for V10.7, with compare-before-write safeguards.

Avoid broad auto-rewrites. Edits done by the site administrator are preserved.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'backend' / 'content'
PREFIX = '@@studysprint-blocks@@'
BASE_PACKS = [
    '3e_2026_v10_5_refresh.json',
    '4e_2026_v10_5_refresh.json',
    '5e_2026_v10_5_refresh.json',
    '6e_2026_v10_5_refresh.json',
    '3e_2026_v10_5_exercises_refresh.json',
]


def p(value): return {'type': 'paragraph', 'content': value}
def f(value): return {'type': 'formula', 'content': value}
def e(value): return {'type': 'example', 'content': value}
def n(value): return {'type': 'note', 'content': value}
def li(values): return {'type': 'list', 'items': values}


def encode(blocks):
    return PREFIX + json.dumps(blocks, ensure_ascii=False)


PATCHES = {}


def patch(level, chapter, title, *blocks):
    key = (level, chapter, title)
    if key in PATCHES:
        raise ValueError(f'Duplicate patch: {key}')
    PATCHES[key] = encode(blocks)


# 3e - Racines carrées
patch('3e', 'Racines carrées', 'Définition',
      p(r'Pour \(a\ge 0\), \(\sqrt{a}\) désigne le nombre positif ou nul dont le carré est égal à \(a\).'),
      f(r'\left(\sqrt{a}\right)^2=a\qquad(a\ge 0)'),
      e(r'Comme \(7^2=49\), on obtient \(\sqrt{49}=7\).'),
      n('La racine carrée d’un nombre négatif n’est pas définie dans les nombres réels.'))
patch('3e', 'Racines carrées', 'Carrés parfaits',
      p('Un carré parfait est le carré d’un nombre entier. Connaître les carrés usuels aide à calculer les racines carrées.'),
      f(r'1^2=1,\quad 2^2=4,\quad 3^2=9,\quad 4^2=16,\quad 5^2=25'),
      e(r'Puisque \(12^2=144\), on a \(\sqrt{144}=12\).'))
patch('3e', 'Racines carrées', 'Lien avec la géométrie',
      p('Dans un triangle rectangle, le théorème de Pythagore donne le carré d’une longueur ; la racine carrée permet ensuite de retrouver cette longueur.'),
      f(r'BC=\sqrt{AB^2+AC^2}\quad\text{(triangle rectangle en A)}'),
      e(r'Si \(AB=6\) cm et \(AC=8\) cm, alors \(BC=\sqrt{6^2+8^2}=\sqrt{100}=10\) cm.'))

# 3e - Puissances
patch('3e', 'Puissances et écriture scientifique', 'Règles de calcul',
      p('Avec des puissances de même base, on additionne les exposants pour multiplier et on les soustrait pour diviser (base non nulle).'),
      f(r'a^m\times a^n=a^{m+n}'),
      f(r'\frac{a^m}{a^n}=a^{m-n}\qquad(a\ne 0)'),
      e(r'Pour multiplier des puissances : \(10^3\times10^2=10^5\). Pour les diviser : \(\frac{10^6}{10^2}=10^4\).'))

# 3e - Thalès: replace awkward ratios, keep ordered correspondences and diagrams precise.
patch('3e', 'Théorème de Thalès', 'Configuration',
      p('On considère un triangle ABC. Le point D appartient à [AB], le point E à [AC], et les droites (DE) et (BC) sont parallèles.'),
      p('Le théorème de Thalès donne les rapports de côtés correspondants :'),
      f(r'\frac{AD}{AB}=\frac{AE}{AC}=\frac{DE}{BC}'),
      n('Vérifie toujours l’alignement et le parallélisme avant d’utiliser la formule.'))
patch('3e', 'Théorème de Thalès', 'Méthode',
      p('Pour calculer une longueur, écris les rapports correspondants dans le même ordre, puis isole la longueur cherchée.'),
      f(r'\frac{AD}{AB}=\frac{AE}{AC}'),
      e(r'Si \((DE)\parallel(BC)\), \(AD=2\) cm, \(AB=6\) cm et \(AC=9\) cm, alors \(\frac{2}{6}=\frac{AE}{9}\), d’où \(AE=\frac{2\times9}{6}=3\) cm.'))
patch('3e', 'Théorème de Thalès', 'Agrandissement/réduction',
      p('Dans cette configuration, les deux triangles ADE et ABC ont des côtés correspondants proportionnels.'),
      f(r'k=\frac{AB}{AD}=\frac{AC}{AE}=\frac{BC}{DE}'),
      p('Lorsque les points D et E sont sur les côtés du triangle, le coefficient k du petit triangle vers le grand est supérieur ou égal à 1.'),
      e(r'Si \(AD=2\) cm et \(AB=6\) cm, alors \(k=\frac{6}{2}=3\). Toutes les longueurs du grand triangle sont trois fois celles du petit.'))

# 3e - Statistiques
patch('3e', 'Statistiques', 'Moyenne',
      p('La moyenne est la somme des valeurs divisée par leur nombre. Si les valeurs ont des effectifs, on utilise une moyenne pondérée.'),
      f(r'\overline{x}=\frac{x_1+x_2+\cdots+x_n}{n}'),
      f(r'\overline{x}=\frac{n_1x_1+n_2x_2+\cdots+n_px_p}{n_1+n_2+\cdots+n_p}'),
      e(r'Pour les notes 8, 12 et 16, la moyenne vaut \(\overline{x}=\frac{8+12+16}{3}=12\).'))
patch('3e', 'Statistiques', 'Médiane',
      p('Commence par ranger les valeurs dans l’ordre croissant. Si l’effectif est impair, prends la valeur centrale. S’il est pair, au collège on prend généralement la moyenne des deux valeurs centrales.'),
      e(r'Dans la série 4 ; 7 ; 9 ; 12 ; 18, la médiane est 9. Dans 4 ; 7 ; 9 ; 12, elle vaut \(\frac{7+9}{2}=8\).'),
      n('La médiane n’est pas toujours égale à la moyenne.'))
patch('3e', 'Statistiques', 'Étendue et fréquence',
      p('L’étendue mesure l’écart entre la plus grande et la plus petite valeur. La fréquence indique la proportion d’un effectif.'),
      f(r'\text{Étendue}=x_{\max}-x_{\min}'),
      f(r'\text{Fréquence}=\frac{\text{effectif de la catégorie}}{\text{effectif total}}'),
      e(r'Pour les valeurs 5, 7 et 13, l’étendue vaut \(13-5=8\). Si 6 élèves sur 20 choisissent une réponse, sa fréquence est \(\frac{6}{20}=0{,}30=30\%\).'))

# 3e - Géométrie dans l'espace (rappel des principales formules de volumes)
patch('3e', "Géométrie dans l'espace", 'Volumes',
      p('Le volume d’un solide se calcule avec la formule correspondant à sa forme. Toutes les longueurs doivent être exprimées dans la même unité.'),
      p('Pavé droit et cube :'),
      f(r'V_{\mathrm{pavé}}=L\times\ell\times h'),
      f(r'V_{\mathrm{cube}}=c^3'),
      p('Cylindre et cône de révolution :'),
      f(r'V_{\mathrm{cylindre}}=\pi r^2 h'),
      f(r'V_{\mathrm{cône}}=\frac{\pi r^2h}{3}'),
      p('Pyramide et boule :'),
      f(r'V_{\mathrm{pyramide}}=\frac{\mathcal A_{\mathrm{base}}\times h}{3}'),
      f(r'V_{\mathrm{boule}}=\frac{4}{3}\pi r^3'),
      e(r'Un cylindre de rayon 2 cm et de hauteur 5 cm a un volume \(V=\pi\times2^2\times5=20\pi\approx62{,}8\ \mathrm{cm}^3\).'))
patch('3e', "Géométrie dans l'espace", 'Sections',
      p('Une section est la figure obtenue lorsque l’on coupe un solide par un plan.'),
      li(['Une section d’un cylindre par un plan parallèle aux bases est un disque.',
          'Une section d’une boule par un plan peut être un disque.',
          'Une section d’un pavé droit par un plan parallèle à l’une de ses faces est un rectangle.']),
      e('Si l’on coupe un cylindre droit parallèlement à ses deux bases circulaires, la section est un disque de même rayon que les bases.'))
patch('3e', "Géométrie dans l'espace", 'Unités',
      p('Une mesure de volume s’exprime en unités cubiques ou en litres. Pour convertir, on utilise notamment ces égalités :'),
      f(r'1\ \mathrm{dm}^3=1\ \mathrm{L}'),
      f(r'1\ \mathrm{cm}^3=1\ \mathrm{mL}'),
      f(r'1\ \mathrm{m}^3=1000\ \mathrm{L}'),
      e(r'Un aquarium d’un volume de \(20\ \mathrm{dm}^3\) contient \(20\) litres d’eau s’il est rempli.'))

# 4e - Statistiques
patch('4e', 'Statistiques : moyenne et médiane', 'Moyenne',
      p('La moyenne se calcule en faisant la somme de toutes les valeurs puis en divisant par l’effectif total.'),
      f(r'\overline{x}=\frac{\text{somme des valeurs}}{\text{effectif total}}'),
      e(r'Pour les valeurs 10, 12 et 17, la moyenne vaut \(\frac{10+12+17}{3}=13\).'))
patch('4e', 'Statistiques : moyenne et médiane', 'Médiane',
      p('Ordonne les valeurs dans l’ordre croissant. Si l’effectif est impair, prends la valeur centrale ; s’il est pair, on prend généralement la moyenne des deux valeurs centrales au collège.'),
      e(r'Pour la série 3 ; 5 ; 8 ; 12 ; 15, la médiane est 8. Pour 3 ; 5 ; 8 ; 12, elle vaut \(\frac{5+8}{2}=6{,}5\).'))
patch('4e', 'Statistiques : moyenne et médiane', 'Étendue et interprétation',
      p('L’étendue est la différence entre la valeur maximale et la valeur minimale d’une série.'),
      f(r'\text{Étendue}=x_{\max}-x_{\min}'),
      e(r'Pour les valeurs 6, 9, 11 et 16, l’étendue est \(16-6=10\).'))

# 4e - volumes
patch('4e', 'Volumes de solides', 'Pavé droit',
      p('Le volume d’un pavé droit est le produit de sa longueur, de sa largeur et de sa hauteur.'),
      f(r'V=L\times\ell\times h'),
      e(r'Un pavé de 4 cm sur 3 cm et de hauteur 5 cm a pour volume \(V=4\times3\times5=60\ \mathrm{cm}^3\).'))
patch('4e', 'Volumes de solides', 'Cylindre de révolution',
      p('Le volume d’un cylindre est l’aire de sa base circulaire multipliée par sa hauteur.'),
      f(r'V=\pi r^2\times h'),
      e(r'Pour un rayon de 3 cm et une hauteur de 4 cm, \(V=\pi\times3^2\times4=36\pi\ \mathrm{cm}^3\).'),
      n('Le rayon est la moitié du diamètre.'))
patch('4e', 'Volumes de solides', 'Conversions',
      p('Les volumes se mesurent en unités cubiques. Les équivalences usuelles sont :'),
      f(r'1\ \mathrm{L}=1\ \mathrm{dm}^3'),
      f(r'1\ \mathrm{mL}=1\ \mathrm{cm}^3'),
      f(r'1\ \mathrm{m}^3=1000\ \mathrm{L}'),
      e(r'Un récipient de \(250\ \mathrm{cm}^3\) a une capacité de \(250\) mL.'))

# 5e - Moyenne et statistiques, surfaces et volumes, masse volumique
patch('5e', 'Aires et volumes composés', 'Aire du triangle',
      p('L’aire d’un triangle est la moitié du produit d’une base par la hauteur correspondante.'),
      f(r'\mathcal A=\frac{b\times h}{2}'),
      e(r'Pour une base de 6 cm et une hauteur de 4 cm, \(\mathcal A=\frac{6\times4}{2}=12\ \mathrm{cm}^2\).'))
patch('5e', 'Aires et volumes composés', 'Volume du pavé',
      p('Le volume d’un pavé droit est obtenu en multipliant ses trois dimensions.'),
      f(r'V=L\times\ell\times h'),
      e(r'Pour un pavé de dimensions 5 cm, 3 cm et 2 cm : \(V=5\times3\times2=30\ \mathrm{cm}^3\).'))
patch('5e', 'Probabilités et statistiques', 'Équiprobabilité',
      p('Quand toutes les issues ont la même chance de se produire, la probabilité est le rapport entre les cas favorables et les cas possibles.'),
      f(r'P(A)=\frac{\text{nombre de cas favorables}}{\text{nombre de cas possibles}}'),
      e(r'En lançant un dé équilibré, la probabilité d’obtenir un nombre pair est \(\frac36=\frac12\).'))
patch('5e', 'Probabilités et statistiques', 'Moyenne',
      p('Pour calculer la moyenne d’une série simple, on additionne les valeurs puis on divise par leur nombre.'),
      f(r'\overline{x}=\frac{\text{somme des valeurs}}{\text{effectif total}}'),
      e(r'Pour les valeurs 4, 6 et 8, la moyenne est \(\frac{4+6+8}{3}=6\).'))
patch('5e', 'Masse, volume et masse volumique', 'Comprendre : Masse, volume et masse volumique',
      p('La masse volumique correspond à la masse d’une substance par unité de volume.'),
      f(r'\rho=\frac{m}{V}'),
      e(r'Si un objet a une masse de 20 g et un volume de 10 mL, sa masse volumique vaut \(\rho=\frac{20}{10}=2\ \mathrm{g/mL}\).'))
patch('5e', 'Masse, volume et masse volumique', 'Relation',
      p('Pour déterminer la masse volumique, divise la masse par le volume en utilisant des unités compatibles.'),
      f(r'\rho=\frac{m}{V}'),
      e(r'Pour 50 g répartis dans 25 mL, on obtient \(\rho=\frac{50}{25}=2\ \mathrm{g/mL}\).'))

# 6e - maths statistics, solids
patch('6e', 'Volumes et pavés droits', 'Pavé droit',
      p('Pour un pavé droit, multiplie la longueur, la largeur et la hauteur après les avoir exprimées dans la même unité.'),
      f(r'V=L\times\ell\times h'),
      e(r'Un pavé de 4 cm sur 3 cm et de hauteur 2 cm a un volume \(V=4\times3\times2=24\ \mathrm{cm}^3\).'))
patch('6e', 'Volumes et pavés droits', 'Cube',
      p('Un cube a toutes ses arêtes de même longueur. Son volume est le cube de cette longueur.'),
      f(r'V=c^3'),
      e(r'Si un cube mesure 3 cm de côté, son volume est \(V=3^3=27\ \mathrm{cm}^3\).'))
patch('6e', 'Tableaux et statistiques', 'Moyenne',
      p('La moyenne d’une série simple est la somme des valeurs divisée par leur nombre.'),
      f(r'\overline{x}=\frac{\text{somme des valeurs}}{\text{nombre de valeurs}}'),
      e(r'Pour les valeurs 5, 7 et 9, la moyenne vaut \(\frac{5+7+9}{3}=7\).'))
patch('6e', 'Tableaux et statistiques', 'Étendue',
      p('L’étendue mesure l’écart entre la plus grande et la plus petite valeur d’une série.'),
      f(r'\text{Étendue}=x_{\max}-x_{\min}'),
      e(r'Pour 2, 7, 10 et 14, l’étendue est \(14-2=12\).'))

# Additional reviews: remove fully evaluated calculations from the main rule blocks.
patch('3e', 'Univers, gravitation et ordres de grandeur', 'Système solaire',
      p('Le Soleil est l’étoile au centre du Système solaire. Huit planètes tournent autour de lui, dont la Terre.'),
      e(r'La distance moyenne Terre-Lune est d’environ 384 000 km. En écriture scientifique : \(384\,000=3{,}84\times 10^5\) km.'))
patch('5e', 'Proportionnalité et vitesse', 'Comprendre : Proportionnalité et vitesse',
      p('À vitesse constante, la distance parcourue est proportionnelle au temps. La vitesse moyenne se calcule en divisant la distance par la durée.'),
      f(r'v=\frac{d}{t}'),
      e(r'Une voiture parcourt 150 km en 2 h. Sa vitesse moyenne est \(v=\frac{150}{2}=75\ \mathrm{km/h}\).'))
patch('5e', 'Proportionnalité et vitesse', 'Vitesse',
      p('Utilise des unités compatibles : les kilomètres et les heures donnent des kilomètres par heure.'),
      f(r'v=\frac{d}{t}'),
      e(r'Si un cycliste parcourt 24 km en 2 h, on obtient \(v=\frac{24}{2}=12\ \mathrm{km/h}\).'))
patch('5e', 'Proportionnalité et vitesse', 'Distance',
      p('À vitesse constante, pour calculer la distance, multiplie la vitesse par la durée.'),
      f(r'd=v\times t'),
      e(r'À 15 km/h pendant 3 h, un cycliste parcourt \(d=15\times3=45\ \mathrm{km}\).'))
patch('6e', 'Angles et instruments', 'Comprendre : Angles et instruments',
      p('Un angle est formé par deux demi-droites de même origine. Le rapporteur permet de mesurer un angle en degrés.'),
      e(r'Un angle de \(60^\circ\) est aigu, car il est inférieur à \(90^\circ\).'))
patch('6e', 'Angles et instruments', 'Angles complémentaires',
      p('Deux angles sont complémentaires lorsque la somme de leurs mesures est égale à 90°.'),
      f(r'\alpha+\beta=90^\circ'),
      e(r'Si un angle mesure 35°, alors son angle complémentaire mesure \(90^\circ-35^\circ=55^\circ\).'))

# Safeguards: generate expected sources from all current packs and any V10.6 changes.
existing = {}
for filename in BASE_PACKS:
    data = json.loads((CONTENT / filename).read_text(encoding='utf-8'))
    for chapter in data['chapters']:
        for lesson in chapter['lessons']:
            existing[(chapter['level'], chapter['title'], lesson['title'])] = lesson['body']

v106 = json.loads((CONTENT / 'quality_v106.json').read_text(encoding='utf-8'))
v106_bodies = {(x['level'], x['chapter'], x['title']): x['body'] for x in v106['lessons']}

rows = []
for key, newbody in PATCHES.items():
    if key not in existing:
        raise ValueError(f'Unknown lesson: {key}')
    old = existing[key]
    sources = [old]
    if key in v106_bodies and v106_bodies[key] != old:
        sources.append(v106_bodies[key])
    if newbody in sources:
        continue
    rows.append({
        'level': key[0], 'chapter': key[1], 'title': key[2],
        'expected_bodies': sources, 'body': newbody,
    })

result = {
    'slug': 'quality-v107-math-lessons',
    'title': 'ExoDéclic V10.7 – expressions KaTeX et fiches mathématiques',
    'lessons': rows,
}
(CONTENT / 'quality_v107.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(rows)} lessons patched; {len(PATCHES)} authored')
