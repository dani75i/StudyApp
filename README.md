# StudySprint V10 — collège 6e et 5e, indices et récompenses

Nouveauté : ajout de 50 chapitres, 150 courtes fiches et 600 exercices corrigés pour la 6e et la 5e, avec 20 visuels scientifiques SVG, des indices associés aux notions et une distinction visuelle plus forte entre récompenses gagnées et verrouillées. Consulter **`V10_GUIDE.md`** pour l’installation, les limites éditoriales et les vérifications recommandées.

---

# StudySprint V9 — Exercices enrichis et parcours pédagogique

Consulte `V9_GUIDE.md` pour les 52 nouveaux exercices originaux de 3e, les indices, la page de correction, le bilan de séance et la barre mobile flottante. Les fonctionnalités et ressources de la V8 restent incluses.

---

# StudySprint V8 — Mobile et contenu 4e

- Navigation mobile **fixe en bas** : Accueil, Cours, Exercices, Badges, Plus (Profil, Séance, Historique et Admin).
- Sur mobile, les compteurs « Réussis / À revoir / À faire » sont côte à côte.
- Exercices affichés sous « Exercice 1 », « Exercice 2 », etc. avec le sujet en sous-titre et progression conservée.
- Exercices classés par difficulté croissante, puis selon leur ordre initial.
- Mise en forme plus sûre des expressions : le texte courant ne devient plus une formule.
- Anciennes fiches 3e (puissances, poids, Pythagore et trigonométrie) présentées en paragraphes/formules/notes lisibles, sans modifier les fiches sauvegardées dans la base.
- Nouveau pack **4e : 13 chapitres maths, 9 physique-chimie, 66 fiches, 176 exercices corrigés**. Voir `CONTENT_4E.md`.
- Visuels de physique redimensionnés au format WebP pour accélérer l'affichage mobile.

**Mise à jour :** copier le contenu du dossier ZIP dans le dépôt Git **existant** sans toucher à `.git`, tester avec `start.bat`, puis `git add .`, `git commit -m "V8 mobile cours et contenu 4e"`, `git push`. Render réutilise `DATABASE_URL`/Neon ; ne recréez pas de base et ne touchez pas à vos variables d'environnement.

---

# StudySprint V7.3 — Éditeur pédagogique et formules mathématiques

## Nouveautés
- rendu des expressions mathématiques avec KaTeX ;
- les anciennes fiches sont automatiquement aérées en paragraphes/formules ;
- les cours peuvent être structurés depuis `/admin` en blocs Paragraphe / Formule / Liste / À retenir ;
- aperçu élève en direct dans l'éditeur de cours ;
- édition des exercices existants avec aperçu de l'énoncé et de la correction ;
- boutons d'insertion rapide pour fractions, racines, puissances, multiplication et formules centrées ;
- recherche et filtres matière / niveau / chapitre dans `/admin` ;
- duplication rapide d'un exercice ;
- les modifications effectuées dans `/admin` sont enregistrées directement dans la base de production, sans nouveau déploiement.

Les fiches existantes restent compatibles : aucune migration SQL n'est nécessaire. Lorsqu'une ancienne fiche est ouverte dans l'éditeur puis enregistrée, elle passe automatiquement au nouveau format structuré.

---

# StudySprint v7.2 — Illustrations physique

## Ajouts de cette version
- 10 illustrations intégrées pour les chapitres de physique-chimie.
- Affichage des visuels sur les cartes des chapitres de physique.
- Affichage d'une grande illustration en haut de chaque chapitre de physique.
- Les images sont stockées dans `frontend/public/illustrations/physics/`.

---

# StudySprint V5

StudySprint est une application éducative centrée sur les **mathématiques** et la **physique-chimie** pour les collégiens et lycéens.

## Fonctionnalités

- comptes élèves et sessions par cookie HTTP-only ;
- mode clair / sombre ;
- cours et exercices corrigés ;
- séance du jour ;
- filtres `À faire / À revoir / Maîtrisé` ;
- progression, badges et objectif hebdomadaire ;
- back-office `/admin` pour gérer chapitres, cours et exercices ;
- SQLite en local ;
- PostgreSQL/Neon en production ;
- page d'accueil publique et pages de cours publiques ;
- `robots.txt` et `sitemap.xml` dynamique pour le référencement ;
- Dockerfile prêt pour Render.

## Lancer en local sous Windows

```powershell
.\start.bat
```

Le script installe les dépendances nécessaires au premier lancement puis démarre React/Vite et FastAPI.

Le port frontend est choisi automatiquement si le port habituel est déjà pris. Le backend choisit également un port disponible dans la plage prévue par le lanceur.

## Compte admin local par défaut

```text
Email : admin@studysprint.fr
Mot de passe : Admin123!
```

Change impérativement ces identifiants en production via les variables `ADMIN_EMAIL` et `ADMIN_PASSWORD`.

## Production

Le déploiement recommandé pour cette première bêta est :

```text
GitHub
   ↓
Render (Docker : React build + FastAPI)
   ↓
Neon PostgreSQL
```

Consulte **DEPLOYMENT.md** pour la procédure complète étape par étape.

## Données

En local :

```text
backend/studysprint.db
```

Ce fichier est ignoré par Git.

En production, toutes les données persistantes vont dans PostgreSQL :

- utilisateurs ;
- sessions ;
- progression ;
- tentatives ;
- matières ;
- chapitres ;
- cours ;
- exercices ;
- corrections.

Les images/vidéos lourdes devront plus tard être placées dans un stockage objet plutôt qu'en base.

## Google Analytics et consentement

La version inclut l'identifiant GA4 `G-KF2VQGLN8C` avec chargement conditionnel après consentement. Voir `ANALYTICS.md` pour les routes mesurées, les événements et les réglages GA4 recommandés.

## V6 — contenu 3e

Cette version ajoute un pack pédagogique versionné pour la 3e : 15 chapitres de mathématiques, 10 chapitres de physique-chimie, 75 fiches de cours et 300 nouveaux exercices. Voir `CONTENT_3E.md`.

Le pack est compatible avec une base Neon déjà utilisée : il est importé automatiquement une seule fois et ne supprime pas les utilisateurs ni leurs tentatives.

## V7 — Refonte UI/UX et récompenses

Cette version conserve la V6 (contenu 3e, déploiement Render/Neon, Google Analytics avec consentement) et ajoute :

- un dashboard visuellement plus riche avec un grand bloc d'accueil et l'objectif hebdomadaire sous forme d'anneau ;
- une vitrine de récompenses beaucoup plus visible sur le dashboard ;
- une page `/recompenses` dédiée avec progression globale et badges verrouillés/débloqués ;
- 9 badges au total, dont des paliers à 25/50 exercices, 3 chapitres maîtrisés et 7 jours de série ;
- un toast visuel lorsqu'un nouveau badge est détecté comme débloqué ;
- des cartes, états de survol, couleurs et contrastes retravaillés en clair et sombre ;
- une navigation mobile améliorée lorsque davantage d'entrées sont présentes dans le menu.

Aucune migration de base de données n'est nécessaire pour cette version.

## V7.1 — Suivi visuel des exercices dans un chapitre

Cette version améliore la lisibilité de la colonne d'exercices sans modifier la base de données :

- statut visible sur chaque exercice : `À faire`, `À revoir`, `Réussi` ;
- nombre de tentatives affiché ;
- résultat de la dernière tentative pris en compte ;
- résumé du chapitre : réussis / à revoir / à faire ;
- filtres rapides sur ces statuts ;
- bouton de reprise priorisant les exercices à revoir puis ceux jamais faits ;
- difficulté écrite en toutes lettres : Facile / Intermédiaire / Difficile ;
- tag de compétence pédagogique déduit du chapitre et du type d'exercice ;
- cartes colorées et bordures d'état pour identifier la progression au premier coup d'œil.

Aucune migration SQL n'est nécessaire pour cette version.
