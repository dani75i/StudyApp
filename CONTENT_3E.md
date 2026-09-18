# Contenu pédagogique 3e — pack v1

Ce pack ajoute automatiquement du contenu de 3e dans la base de données au premier démarrage de cette version.

## Volume

- 15 chapitres de mathématiques
- 10 chapitres de physique-chimie
- 75 fiches de cours
- 300 nouveaux exercices
- 12 exercices par chapitre

Sur une base déjà utilisée par une version antérieure de StudySprint, les anciens exercices sont conservés pour ne pas casser les tentatives/progressions existantes. Le nombre total peut donc être légèrement supérieur à 300.

## Mathématiques

1. Arithmétique : divisibilité et nombres premiers
2. Puissances et écriture scientifique
3. Calcul littéral et équations
4. Racines carrées
5. Proportionnalité, pourcentages et vitesses
6. Fonctions : images et antécédents
7. Fonctions linéaires et affines
8. Statistiques
9. Probabilités
10. Théorème de Pythagore
11. Théorème de Thalès
12. Trigonométrie dans le triangle rectangle
13. Transformations et homothéties
14. Géométrie dans l'espace
15. Algorithmique et programmation

## Physique-Chimie

1. Atomes, ions et molécules
2. Transformations chimiques et conservation
3. Acides, bases et pH
4. Mouvement et vitesse
5. Forces, poids et gravitation
6. Énergie, puissance et conversions
7. Circuits électriques : tension et intensité
8. Loi d'Ohm et puissance électrique
9. Signaux sonores et lumineux
10. Univers, gravitation et ordres de grandeur

## Installation dans une base existante

Le fichier `backend/content/3e_2026_v1.json` est un pack de déploiement. Les données sont importées dans PostgreSQL/SQLite par `backend/app/content_pack.py`.

Le pack possède un identifiant de version (`fr-3e-2026-v1`). Une fois appliqué, il n'est pas réimporté à chaque redémarrage. Les modifications réalisées ensuite depuis `/admin` restent donc en base.

Les anciens chapitres de démonstration proches d'un chapitre définitif sont réutilisés/renommés au lieu d'être dupliqués. Les comptes, tentatives et progressions ne sont pas supprimés.

## Références programme

Le nouveau programme de mathématiques du cycle 4 publié en mars 2026 entre progressivement en vigueur : 5e en 2026-2027, 4e en 2027-2028, 3e en 2028-2029. Pour l'année 2026-2027, les ressources antérieures restent applicables en 3e.

- Éduscol — ressources mathématiques cycle 4 : https://eduscol.education.gouv.fr/5736/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-4
- Éduscol — repères annuels et attendus jusqu'à la 3e : https://eduscol.education.gouv.fr/6910/reperes-annuels-de-progression-et-attendus-de-fin-d-annee-du-cp-la-troisieme
- Éduscol — enseigner au cycle 4 : https://eduscol.education.gouv.fr/4362/enseigner-au-cycle-4

Ce premier pack est destiné à lancer le catalogue. Avant une exploitation commerciale à grande échelle, une relecture pédagogique par un enseignant reste recommandée, notamment pour harmoniser le niveau de difficulté et la progression avec les pratiques de classe.
