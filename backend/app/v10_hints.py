"""Indices contextuels pour les exercices hérités de V6–V9.
Ne jamais remplacer les guides déjà écrits dans l'admin / présents dans V9.
Une règle s'applique au chapitre et à des opérations concrètes de l'énoncé.
"""
import json
import re
from .models import Chapter, Exercise, ExerciseGuide

# Concept du chapitre, puis action que l’élève doit accomplir sans donner la réponse.
TOPIC_HINTS = {
 'arithmétique': ('Teste les diviseurs possibles des nombres de la question, plutôt que de multiplier au hasard.', 'Pour le PGCD, cherche le plus grand nombre qui divise exactement les deux entiers. Pour un nombre premier, teste les diviseurs premiers jusqu’à sa racine carrée.'),
 'puissance': ('Distingue la base de l’exposant : le nombre en exposant indique combien de fois la base est multipliée par elle-même.', 'Si les bases sont identiques, un produit additionne les exposants et un quotient les soustrait ; ne confonds pas ces deux règles.'),
 'littéral': ('Repère les termes qui contiennent la même lettre, et ceux qui sont constants.', 'Pour développer, multiplie chaque terme de la parenthèse par le facteur extérieur ; pour réduire, regroupe les termes de même nature.'),
 'équation': ('Repère le terme contenant l’inconnue, puis les termes constants de l’équation.', 'Effectue une même opération sur les deux membres pour isoler l’inconnue ; remplace-la ensuite dans l’égalité initiale.'),
 'racine': ('Cherche deux carrés parfaits qui encadrent le nombre sous la racine.', 'Utilise le fait que la racine carrée d’un nombre positif est le nombre positif dont le carré est ce nombre.'),
 'proportionnalité': ('Cherche quelle grandeur correspond à une seule unité : prix unitaire, distance par heure ou part sur cent.', 'Établis le coefficient de proportionnalité à partir des deux valeurs données, puis applique-le à la quantité recherchée.'),
 'pourcentage': ('Distingue la valeur de départ, le pourcentage indiqué et la quantité recherchée.', 'Pour une partie en pourcentage, multiplie la valeur de départ par le pourcentage puis divise par 100 ; pour un prix final, ajoute ou retranche la variation.'),
 'vitesse': ('Repère la distance parcourue et la durée ; relève leurs unités.', 'Vitesse = distance ÷ durée. Pour chercher la distance ou le temps, transforme cette relation et rends les unités cohérentes.'),
 'fonction': ('Repère le nombre donné : est-ce une valeur de x, ou le résultat f(x) ?', 'Pour une image, remplace x dans l’expression ; pour un antécédent, résous l’égalité f(x) = valeur demandée.'),
 'statistique': ('Lis la série ou le tableau : identifie les valeurs et les effectifs.', 'Pour la moyenne, divise la somme pondérée par l’effectif total ; pour la médiane, range les valeurs par ordre croissant avant de choisir le centre.'),
 'probabilité': ('Compte toutes les issues possibles dans cette expérience, puis seulement celles qui conviennent à la question.', 'En cas d’équiprobabilité, probabilité = nombre d’issues favorables ÷ nombre d’issues possibles ; garde un résultat entre 0 et 1.'),
 'pythagore': ('Localise l’angle droit dans le triangle décrit : le côté qui lui est opposé est l’hypoténuse.', 'Dans le triangle rectangle, écris le carré de l’hypoténuse comme la somme des carrés des deux autres côtés ; isole la longueur cherchée.'),
 'thalès': ('Repère les deux droites sécantes et vérifie quels segments se trouvent sur les mêmes droites.', 'Si les droites correspondantes sont parallèles, écris les rapports de côtés homologues ; pour une réciproque, compare d’abord les deux rapports connus.'),
 'trigonométr': ('Dans le triangle rectangle, repère l’angle donné et identifie le côté opposé, le côté adjacent et l’hypoténuse.', 'Choisis sinus, cosinus ou tangente selon les deux côtés concernés ; utilise la fonction inverse lorsque tu cherches un angle.'),
 'transformation': ('Repère la transformation indiquée et le point ou la figure de départ.', 'Une translation conserve longueurs et angles ; une rotation conserve les distances au centre ; une homothétie multiplie les longueurs par la valeur absolue du rapport.'),
 'géométrie': ('Identifie la figure et les dimensions données dans cet énoncé.', 'Écris la formule de l’aire ou du volume de cette figure, puis remplace chaque grandeur en gardant des unités cohérentes.'),
 'triangle': ('Repère si le triangle est isocèle, rectangle ou quelconque.', 'La somme des angles d’un triangle vaut 180° ; utilise aussi les propriétés des côtés égaux et des angles correspondants lorsque c’est indiqué.'),
 'volume': ('Relève les trois dimensions du solide et leurs unités.', 'Pour un pavé, volume = longueur × largeur × hauteur ; pour un cylindre, volume = aire de la base × hauteur.'),
 'algorithm': ('Suis la valeur de chaque variable instruction par instruction.', 'Note séparément le résultat d’une condition ou d’une itération de boucle avant de passer à l’instruction suivante.'),
 'atome': ('Repère les espèces chimiques ou les charges mises en jeu dans l’énoncé.', 'Un atome est neutre ; un ion a gagné ou perdu des électrons. La charge vient de l’écart entre charges positives et négatives.'),
 'molécule': ('Relève le nombre de chaque symbole chimique dans la formule affichée.', 'Un indice en bas à droite d’un symbole compte les atomes de cet élément ; un coefficient devant la formule multiplie l’ensemble.'),
 'chimique': ('Note les réactifs et les produits mentionnés, sans les confondre avec le matériel utilisé.', 'Lors d’une transformation chimique dans un système fermé, le nombre d’atomes de chaque élément et la masse totale se conservent.'),
 'mélange': ('Repère les constituants visibles et ceux qui ont été dissous dans le liquide.', 'Un mélange uniforme à l’œil nu est homogène ; une filtration retient les solides insolubles, une décantation sépare certaines phases distinctes.'),
 'ph': ('Repère la valeur du pH et détermine si la solution est acide, neutre ou basique.', 'Compare la valeur indiquée à 7 : plus petite pour un acide, égale pour une solution neutre, plus grande pour une solution basique.'),
 'mouvement': ('Relève la distance, la durée ou la forme de la trajectoire décrite.', 'Pour une vitesse moyenne, divise la distance par la durée ; si les positions suivent une droite ou un cercle, nomme la trajectoire correspondante.'),
 'force': ('Repère l’objet qui subit l’action et celui qui l’exerce.', 'Pour le poids, P = m × g avec m en kilogrammes ; une force possède une direction, un sens et une intensité.'),
 'gravitation': ('Distingue la masse de l’objet, qui ne change pas selon le lieu, de son poids.', 'La valeur du poids dépend de l’intensité de la pesanteur au lieu considéré ; applique P = m × g uniquement si les unités sont cohérentes.'),
 'énergie': ('Relève l’énergie reçue et les formes d’énergie utiles ou dissipées.', 'Dans le bilan, l’énergie reçue se répartit entre les différentes formes de sortie ; pour une puissance moyenne, utilise P = E / t.'),
 'tension': ('Distingue la tension, mesurée en volts, de l’intensité, mesurée en ampères.', 'En série, l’intensité est la même dans la boucle ; en dérivation, les tensions sont identiques aux bornes des branches.'),
 'circuit': ('Observe si les dipôles appartiennent à une seule boucle ou à plusieurs branches.', 'Un ampèremètre s’insère en série ; un voltmètre se branche en dérivation. Un interrupteur ouvert interrompt la branche concernée.'),
 'ohm': ('Identifie la résistance en ohms, la tension en volts et l’intensité en ampères.', 'Pour un conducteur ohmique, U = R × I ; isole la grandeur demandée, puis vérifie les unités.'),
 'signal': ('Identifie si la situation décrit un son, une lumière ou la transmission d’une information.', 'Un son nécessite un milieu matériel ; la lumière se propage dans le vide. La fréquence correspond au nombre d’oscillations par seconde.'),
 'univers': ('Repère la grandeur demandée et l’unité astronomique donnée.', 'Exprime les distances très grandes avec une écriture scientifique ; utilise le facteur de conversion indiqué, sans mélanger les unités.'),
 'système': ('Repère l’inconnue x et l’inconnue y dans les deux équations.', 'Cherche à éliminer une inconnue par combinaison ou remplace-la à l’aide d’une équation ; contrôle ensuite le couple dans les deux égalités.'),
 'factoris': ('Cherche un facteur commun aux deux termes ou une différence de deux carrés.', 'Pour un facteur commun A, transforme A×B+A×C en A×(B+C) ; pour une différence de carrés, utilise a²−b²=(a−b)(a+b).'),
 'identité': ('Vérifie si l’expression est un carré d’une somme, un carré d’une différence ou un produit de deux conjugués.', 'Applique l’identité correspondante en surveillant le signe du terme du milieu : (a−b)²=a²−2ab+b².'),
 'fraction': ('Repère les numérateurs et dénominateurs des fractions présentes dans l’énoncé.', 'Pour additionner, commence par mettre au même dénominateur ; pour multiplier, multiplie numérateurs entre eux et dénominateurs entre eux.'),
 'relatif': ('Regarde le signe des nombres et le type d’opération demandé.', 'En addition, compare les distances à zéro ; en multiplication ou division, deux signes identiques donnent un résultat positif.'),
 'rotation': ('Identifie le centre de rotation et l’angle indiqué dans la question.', 'Le point image reste à la même distance du centre ; reporte l’angle orienté dans le bon sens.'),
 'son': ('Cherche quel élément vibre ou quelle propriété du signal est mesurée.', 'La fréquence se mesure en hertz ; un son ne se propage pas dans le vide et sa hauteur dépend de la fréquence.'),
 'lumière': ('Identifie la source lumineuse, l’objet et l’éventuel écran.', 'La lumière se propage en ligne droite en milieu transparent homogène ; un objet opaque peut créer une zone d’ombre.'),
}

def contextual_hints(chapter_title, statement, exercise_type=None, options_json=None):
    """Fournit deux conseils de chapitre applicables à un énoncé, sinon aucun.
    Ne fabrique pas de méthode aléatoire ni de correction anticipée.
    """
    title=chapter_title.casefold()
    problem=(statement or '').casefold()
    # Priorité à la compétence explicite de l'énoncé (utile pour les chapitres mixtes).
    keys=('pgcd','factoris','identité','système','probabilité','pourcentage','vitesse','racine','trigonométr','pythagore','thalès','équation','fraction','volume','tension','intensité','énergie')
    for key in keys:
        if key in problem and key in TOPIC_HINTS:
            return list(TOPIC_HINTS[key])
        if key=='pgcd' and key in problem: return list(TOPIC_HINTS['arithmétique'])
        if key=='intensité' and key in problem: return list(TOPIC_HINTS['tension'])
    for key in sorted(TOPIC_HINTS,key=len,reverse=True):
        if key in title:return list(TOPIC_HINTS[key])
    return []


def upgrade_existing_hints(db):
    """Complète seulement les anciens exercices sans guide ; idempotent, jamais de remplacement.
    Les guides du V9 et les modifications /admin ont priorité absolue.
    """
    rows=(db.query(Exercise,Chapter)
          .join(Chapter,Exercise.chapter_id==Chapter.id)
          .filter(Chapter.level.in_(['3e','4e'])).all())
    existing={r[0] for r in db.query(ExerciseGuide.exercise_id).all()}
    created=0
    for exercise,chapter in rows:
        if exercise.id in existing:continue
        hints=contextual_hints(chapter.title,exercise.statement,exercise.exercise_type,exercise.options_json)
        if not hints:continue
        db.add(ExerciseGuide(exercise_id=exercise.id,hints_json=json.dumps(hints,ensure_ascii=False)))
        created+=1
    if created:db.commit()
    return created
