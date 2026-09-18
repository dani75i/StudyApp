# Déployer StudySprint gratuitement — GitHub + Neon + Render

Cette version est préparée pour le premier déploiement public :

- **GitHub** : stockage/versionnement du code ;
- **Neon** : PostgreSQL persistant ;
- **Render** : un seul Web Service Docker qui sert FastAPI **et** le build React ;
- **même domaine** pour le frontend et l'API, afin de conserver l'authentification par cookie HTTP-only simplement.

## 0. Tester localement avant de publier

Sous Windows, depuis la racine :

```powershell
.\start.bat
```

Vérifie au minimum :

- la page publique `/` ;
- inscription ;
- connexion ;
- `/dashboard` ;
- cours et exercices ;
- compte admin et `/admin`.

## 1. Créer le dépôt GitHub

Sur GitHub, crée un nouveau dépôt **vide**, par exemple `studysprint`.
Ne coche pas l'ajout automatique d'un README ou d'un `.gitignore` puisque le projet les possède déjà.

Puis, dans le terminal VS Code ouvert à la racine du projet :

```bash
git init
git add .
git commit -m "StudySprint V5 - deployment ready"
git branch -M main
git remote add origin https://github.com/TON_USER/studysprint.git
git push -u origin main
```

Le fichier `.gitignore` empêche d'envoyer la base SQLite locale, les `.env`, le venv Python et `node_modules`.

## 2. Créer la base PostgreSQL Neon

1. Crée un compte Neon.
2. Crée un projet, par exemple `studysprint`.
3. Clique sur **Connect**.
4. Pour le premier déploiement, copie la **connection string directe** (non poolée), afin que la création/migration du schéma SQLAlchemy reste simple.
5. Garde cette URL privée. Elle ressemble à :

```text
postgresql://USER:PASSWORD@ep-xxxxx.eu-central-1.aws.neon.tech/neondb?sslmode=require
```

Le projet convertit automatiquement `postgresql://` en `postgresql+psycopg://` pour SQLAlchemy.

## 3. Créer le Web Service Render

1. Crée un compte Render et connecte GitHub.
2. **New > Web Service**.
3. Choisis le dépôt `studysprint`.
4. Runtime : **Docker**. Render détectera le `Dockerfile` à la racine.
5. Choisis le plan **Free**.
6. Donne un nom au service, par exemple `studysprint-fr` si disponible.
7. Dans **Environment**, ajoute :

```text
DATABASE_URL      = <ta connection string Neon>
COOKIE_SECURE     = true
ADMIN_EMAIL       = ton-adresse-admin@example.com
ADMIN_PASSWORD    = un mot de passe admin long et unique
STATIC_DIR        = /app/frontend/dist
SITE_URL          = http://localhost:5173
```

`SITE_URL` sera corrigé juste après le premier déploiement, quand Render aura fourni l'URL publique.

8. Lance **Create Web Service / Deploy**.

Le Dockerfile :

- compile React avec Vite ;
- installe FastAPI et les dépendances Python ;
- copie `frontend/dist` dans l'image ;
- démarre Uvicorn sur le port fourni par Render.

## 4. Corriger SITE_URL après le premier déploiement

Render te donnera une URL ressemblant à :

```text
https://studysprint-fr.onrender.com
```

Dans Render > ton service > Environment, remplace :

```text
SITE_URL=http://localhost:5173
```

par :

```text
SITE_URL=https://studysprint-fr.onrender.com
```

Puis redéploie. Cette variable sert principalement à générer le sitemap SEO.

## 5. Vérifier le site en ligne

Teste :

```text
https://TON-SERVICE.onrender.com/
https://TON-SERVICE.onrender.com/api/health
https://TON-SERVICE.onrender.com/sitemap.xml
https://TON-SERVICE.onrender.com/robots.txt
```

Puis :

1. crée un compte élève ;
2. réponds à un exercice ;
3. déconnecte-toi ;
4. reconnecte-toi ;
5. vérifie que la progression existe toujours ;
6. connecte-toi avec ton compte admin ;
7. ajoute un exercice depuis `/admin` ;
8. vérifie qu'il apparaît pour un élève du bon niveau.

Si tout cela fonctionne, PostgreSQL Neon est bien utilisé et tes données ne dépendent pas du disque éphémère de Render.

## 6. Ajouter le nom de domaine

Une fois l'URL Render validée :

1. achète ton domaine chez le registraire de ton choix ;
2. Render > service > **Settings > Custom Domains > Add Custom Domain** ;
3. saisis ton domaine ;
4. Render t'indique les enregistrements DNS à créer chez ton registraire ;
5. attends la propagation DNS et clique sur **Verify**.

Render génère et renouvelle ensuite automatiquement le certificat HTTPS.

Quand le domaine fonctionne, remplace `SITE_URL` par :

```text
https://ton-domaine.fr
```

et redéploie.

## 7. Google / SEO

La V5 contient :

- une page d'accueil publique ;
- une bibliothèque publique de cours ;
- des pages de cours publiques ;
- balises title/description de base ;
- `robots.txt` ;
- un `sitemap.xml` dynamique contenant les chapitres publics.

Quand le domaine définitif fonctionne :

1. ouvre Google Search Console ;
2. ajoute ton domaine ;
3. suis la procédure de validation DNS proposée par Google ;
4. soumets :

```text
https://ton-domaine.fr/sitemap.xml
```

Les tableaux de bord, pages admin, historique et profil ne sont pas destinés au référencement.

## 8. Les prochaines modifications après GitHub

Après ce premier déploiement, GitHub devient la source officielle. Quand tu modifies des fichiers dans VS Code :

```bash
git status
git add .
git commit -m "Description de la modification"
git push
```

Render redéploie automatiquement la branche connectée. Tu ne recrées pas un nouveau projet à chaque version.

## Important avant d'avoir de vrais utilisateurs

Pour une bêta ouverte, prévoir rapidement :

- vérification de l'adresse email ;
- mot de passe oublié ;
- limitation des tentatives de connexion ;
- politique de confidentialité / mentions légales / RGPD ;
- sauvegarde/export régulier de la base ;
- tests automatisés des parcours inscription, exercices et admin.

## Google Analytics (consentement préalable)

L'identifiant par défaut intégré au frontend est `G-KF2VQGLN8C`.
Google Analytics n'est chargé qu'après acceptation explicite de la mesure d'audience.
L'intégration est volontairement désactivée dans les routes privées de l'espace élève et de l'administration.

Dans Google Analytics :
1. Réglez la conservation des données d'événements sur 2 mois.
2. N'activez pas Google Signals, le remarketing ni la personnalisation publicitaire.
3. Dans le flux Web, désactivez le suivi automatique des changements d'historique/page si vous utilisez la mesure améliorée des pages : StudySprint envoie lui-même les `page_view` des routes publiques autorisées.
4. Ne transmettez jamais email, prénom, réponses d'exercices ou identifiant interne dans les événements Analytics.

Avant une communication publique large, complétez la page `/confidentialite` avec l'identité de l'éditeur et une adresse de contact RGPD.
