# StudySprint V9 — parcours d'exercice et enrichissement 3e

## Contenu créé

Ce pack apporte **52 exercices originaux** de niveau 3e, rédigés pour StudySprint en s'inspirant du *type de travail* des PDF transmis, **sans recopier leurs énoncés, valeurs, figures ou corrigés**.

| Thème | Exercices ajoutés | Modalités |
| --- | ---: | --- |
| Trigonométrie | 12 | Mesures d'angles/longueurs, réponses numériques et arrondis, schémas non à l'échelle |
| Factorisation | 12 | Facteur commun, différences de carrés, formules composées, QCM |
| Identités remarquables | 12 | Développement, réduction, identification d'erreurs, QCM |
| Réciproque de Thalès | 8 | Justification par comparaison de deux rapports, QCM, schémas non à l'échelle |
| Systèmes d'équations — approfondissement | 8 | Résolution et vérification d'un couple, QCM |

La factorisation, les identités remarquables, la réciproque de Thalès et les systèmes reposent pour l'instant sur des QCM : les réponses algébriques libres ne sont pas validées par un calculateur symbolique. Les nouveaux exercices de trigonométrie acceptent les virgules ou points décimaux ainsi que l'écriture 5 au lieu de 5,0 si la valeur numérique est la même.

Sources d'inspiration fournies par l'utilisateur : `exercice-trigonometrie-3eme-1.pdf` et corrigé, `factorisation-2.pdf` et corrigé, `identite-remarquable-2.pdf` et corrigé, `reciproque-theoreme-thales-1.pdf` (sans corrigé), `systeme-equation-2-corrige.pdf` (sans feuille d'énoncés). Ces fichiers **ne sont pas inclus** dans le site ni dans ce ZIP.

## Parcours V9

1. Ouvrir un exercice → 2 indices progressifs, sélection de réponse et barre de progression.
2. Valider → page `/exercice/:id/correction` (uniquement après une tentative sauvegardée pour cet élève).
3. Voir sa réponse, la réponse attendue, les étapes détaillées et la méthode à retenir, quand elles sont disponibles.
4. Refaire ou aller à l'exercice suivant. Depuis la séance du jour, enchaîner sur les exercices non faits puis afficher `/seance/bilan`.

Les anciens exercices continuent de fonctionner : deux conseils généraux avant validation et leur correction historique après réponse ; les nouvelles fiches bénéficient en plus de solutions découpées en étapes individuelles.

## Admin

Dans `/admin`, la création/modification d'un exercice propose désormais 2 indices, plusieurs étapes de correction (une par ligne) et une méthode à retenir. Les modifications sont écrites dans PostgreSQL/Neon sans redéploiement. Les corrections historiques restent éditables.

## Import sûr

Nouveau pack `backend/content/3e_2026_v9_exercices.json`, identifié `fr-3e-v9-original-exercices-v1`. Au démarrage, FastAPI crée automatiquement la nouvelle table facultative `exercise_guides` avec SQLAlchemy, puis installe le pack si nécessaire. Le pack s'installe **une fois**, n'écrase pas les exercices/cours déjà présents et ne modifie pas le résumé des chapitres existants. Les données élèves, tentatives et sessions restent intactes.

**Avant toute mise à jour de production**, faire une sauvegarde/restauration de test de la base Neon. Tester la V9 en local avec `start.bat`, puis `git add .`, `git commit -m "V9 exercices enrichis et navigation mobile"` et `git push` dans le dépôt Git existant. Ne pas copier de `.env` ou de base SQLite locale dans GitHub.

## Limites / vérifications

- Les problèmes originaux doivent faire l'objet d'une relecture pédagogique avant communication à grande échelle.
- Les diagrammes de trigonométrie/Thalès représentent la configuration des points, pas des mesures à l'échelle ; seules les valeurs de l'énoncé servent au calcul.
- Les PDF de Thalès et de systèmes transmis ne forment pas chacun une paire énoncé/corrigé. Les nouveaux exemples sur ces thèmes ont été résolus et vérifiés indépendamment, pas copiés depuis les documents.
- Pour un `npm install` / `npm run build` complet, le PC doit avoir accès aux dépendances déjà listées dans `frontend/package.json`. Les tests effectués ici incluent l'API et la vérification syntaxique React, mais pas un build npm complet faute de cache npm disponible.
