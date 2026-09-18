import json
from sqlalchemy.orm import Session
from .models import Subject, Chapter, Lesson, Exercise, User
from .security import hash_password
from .config import settings


def seed(db: Session):
    if not db.query(User).filter(User.email == settings.admin_email.lower()).first():
        db.add(
            User(
                email=settings.admin_email.lower(),
                first_name='Admin',
                password_hash=hash_password(settings.admin_password),
                level='3e',
                role='admin',
            )
        )

    if db.query(Subject).count() > 0:
        db.commit()
        return

    maths = Subject(
        slug='mathematiques',
        name='Mathématiques',
        emoji='📐',
        description='Calcul, géométrie, théorèmes et fonctions pour le collège et le lycée.',
    )
    physics = Subject(
        slug='physique-chimie',
        name='Physique-Chimie',
        emoji='⚛️',
        description='Comprendre l’énergie, l’électricité et les phénomènes physiques du quotidien.',
    )
    db.add_all([maths, physics])
    db.flush()

    chapters = [
        Chapter(subject_id=maths.id, level='3e', title='Théorème de Pythagore', summary='Reconnaître un triangle rectangle et calculer une longueur.', order_index=1),
        Chapter(subject_id=maths.id, level='3e', title='Théorème de Thalès', summary='Utiliser les rapports de longueurs dans une configuration de Thalès.', order_index=2),
        Chapter(subject_id=maths.id, level='3e', title='Fonctions affines', summary='Lire, calculer et représenter une fonction affine.', order_index=3),
        Chapter(subject_id=physics.id, level='3e', title='Énergie et puissance', summary='Relier énergie, puissance et durée.', order_index=1),
        Chapter(subject_id=physics.id, level='3e', title='Tension et intensité', summary='Comprendre les grandeurs essentielles d’un circuit électrique.', order_index=2),
    ]
    db.add_all(chapters)
    db.flush()

    pyth, thales, funcs, energy, electric = chapters

    db.add_all([
        Lesson(chapter_id=pyth.id, title='Le théorème', order_index=1, body="Dans un triangle rectangle, le carré de la longueur de l'hypoténuse est égal à la somme des carrés des deux autres côtés.\n\nSi ABC est rectangle en A : BC² = AB² + AC².\n\nL'hypoténuse est toujours le côté opposé à l'angle droit."),
        Lesson(chapter_id=pyth.id, title='La réciproque', order_index=2, body="Pour prouver qu'un triangle est rectangle, on compare le carré du plus grand côté avec la somme des carrés des deux autres côtés. Si c² = a² + b², alors le triangle est rectangle."),
        Lesson(chapter_id=thales.id, title='Configuration et égalité des rapports', order_index=1, body="Lorsque deux droites sécantes sont coupées par deux droites parallèles, les longueurs correspondantes sont proportionnelles.\n\nOn écrit par exemple AB/AC = AD/AE = BD/CE selon la configuration."),
        Lesson(chapter_id=thales.id, title='Méthode de résolution', order_index=2, body="Repère d'abord les droites parallèles, puis les sommets communs. Écris les rapports dans le même ordre et termine par un produit en croix."),
        Lesson(chapter_id=funcs.id, title='Définition', order_index=1, body="Une fonction affine est de la forme f(x)=ax+b.\n\nLe nombre a est le coefficient directeur et b l'ordonnée à l'origine.\n\nPour calculer l'image d'un nombre, on remplace x par ce nombre."),
        Lesson(chapter_id=funcs.id, title='Lecture graphique', order_index=2, body="Sur un graphique, l'ordonnée à l'origine est la valeur de la fonction pour x=0.\n\nLe coefficient directeur mesure la variation de y quand x augmente d'une unité."),
        Lesson(chapter_id=energy.id, title='Puissance', order_index=1, body="La puissance exprime la rapidité d'un transfert d'énergie. Relation : E = P × t, avec E en joules, P en watts et t en secondes."),
        Lesson(chapter_id=energy.id, title='Conversions utiles', order_index=2, body="1 kilowatt = 1000 watts.\n\nPour convertir des minutes en secondes, on multiplie par 60.\n\nPense toujours à harmoniser les unités avant le calcul."),
        Lesson(chapter_id=electric.id, title='Définitions', order_index=1, body="La tension s'exprime en volts (V). L'intensité du courant s'exprime en ampères (A).\n\nDans un circuit en série, l'intensité est la même en tout point."),
        Lesson(chapter_id=electric.id, title='Série et dérivation', order_index=2, body="En série, les dipôles sont placés les uns à la suite des autres. En dérivation, le courant se partage entre plusieurs branches.\n\nLa tension est la même aux bornes de branches en dérivation."),
    ])

    exercises = [
        Exercise(chapter_id=pyth.id, title="Repérer l'hypoténuse", statement="Dans le triangle ABC rectangle en A, quel côté est l'hypoténuse ?", exercise_type='mcq', options_json=json.dumps(['AB', 'AC', 'BC']), correct_answer='BC', correction="L'hypoténuse est le côté opposé à l'angle droit. L'angle droit est en A, donc le côté opposé est BC.", difficulty=1, order_index=1),
        Exercise(chapter_id=pyth.id, title='Calcul direct', statement='ABC est rectangle en A. AB = 3 cm et AC = 4 cm. Combien mesure BC ? (répondre par un nombre)', exercise_type='text', options_json='[]', correct_answer='5', correction='BC² = 3² + 4² = 9 + 16 = 25, donc BC = √25 = 5 cm.', difficulty=1, order_index=2),
        Exercise(chapter_id=pyth.id, title='Triangle rectangle ?', statement='Un triangle a pour côtés 6 cm, 8 cm et 10 cm. Est-il rectangle ?', exercise_type='mcq', options_json=json.dumps(['Oui', 'Non']), correct_answer='Oui', correction='10² = 100 et 6² + 8² = 36 + 64 = 100. Par la réciproque de Pythagore, le triangle est rectangle.', difficulty=2, order_index=3),
        Exercise(chapter_id=thales.id, title='Proportion simple', statement='Dans une configuration de Thalès, AB/AC = 2/5 et AD = 6. Si AB correspond à AD et AC à AE, combien vaut AE ?', exercise_type='text', options_json='[]', correct_answer='15', correction='2/5 = 6/AE. Donc 2×AE = 30, d’où AE = 15.', difficulty=2, order_index=1),
        Exercise(chapter_id=thales.id, title='Identifier la bonne égalité', statement='Quelle égalité peut convenir dans une configuration de Thalès ?', exercise_type='mcq', options_json=json.dumps(['AB + AC = AD + AE', 'AB/AC = AD/AE', 'AB × AC = AD × AE']), correct_answer='AB/AC = AD/AE', correction='Dans la configuration de Thalès, on compare des rapports de longueurs correspondantes.', difficulty=1, order_index=2),
        Exercise(chapter_id=funcs.id, title="Image d'un nombre", statement='Soit f(x)=2x+3. Quelle est l’image de 4 ?', exercise_type='text', options_json='[]', correct_answer='11', correction='f(4)=2×4+3=8+3=11.', difficulty=1, order_index=1),
        Exercise(chapter_id=funcs.id, title="Ordonnée à l'origine", statement="Dans f(x)=−3x+7, quelle est l'ordonnée à l'origine ?", exercise_type='mcq', options_json=json.dumps(['−3', '3', '7']), correct_answer='7', correction="Dans f(x)=ax+b, b est l'ordonnée à l'origine. Ici b=7.", difficulty=1, order_index=2),
        Exercise(chapter_id=funcs.id, title='Calculer un coefficient', statement='La fonction affine f vérifie f(0)=5 et f(1)=8. Quel est son coefficient directeur ?', exercise_type='text', options_json='[]', correct_answer='3', correction='Quand x augmente de 1, la valeur passe de 5 à 8, donc elle augmente de 3. Le coefficient directeur vaut 3.', difficulty=2, order_index=3),
        Exercise(chapter_id=energy.id, title="Calcul d'énergie", statement='Un appareil de 100 W fonctionne pendant 10 s. Quelle énergie consomme-t-il en joules ?', exercise_type='text', options_json='[]', correct_answer='1000', correction='E=P×t=100×10=1000 J.', difficulty=1, order_index=1),
        Exercise(chapter_id=energy.id, title='Choisir la bonne formule', statement='Quelle relation relie énergie E, puissance P et durée t ?', exercise_type='mcq', options_json=json.dumps(['E = P × t', 'P = E × t', 'E = P / t']), correct_answer='E = P × t', correction='La relation à connaître est E = P × t.', difficulty=1, order_index=2),
        Exercise(chapter_id=electric.id, title='Unité de la tension', statement="Dans quelle unité s'exprime la tension électrique ?", exercise_type='mcq', options_json=json.dumps(['Ampère', 'Volt', 'Watt']), correct_answer='Volt', correction='La tension se mesure en volts (V).', difficulty=1, order_index=1),
        Exercise(chapter_id=electric.id, title='Intensité en série', statement="Dans un circuit en série, comment est l'intensité du courant ?", exercise_type='mcq', options_json=json.dumps(['Elle est la même partout', 'Elle augmente après chaque lampe', 'Elle vaut toujours 0']), correct_answer='Elle est la même partout', correction="Dans un circuit en série, l'intensité est identique en tout point du circuit.", difficulty=1, order_index=2),
    ]
    db.add_all(exercises)
    db.commit()
