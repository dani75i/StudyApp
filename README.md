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
