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
