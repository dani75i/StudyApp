# ExoDéclic — V10.1 : domaine et référencement

Cette version reprend **tous les fichiers de StudySprint V10**. Elle change la marque visible et améliore les pages publiques pour le référencement, sans migrer la base de données.

## Avant de copier

1. Conserve ton dépôt Git existant, le dossier `.git`, tes fichiers `.env` et ta base locale `backend/studysprint.db` si tu l'utilises.
2. Copie le **contenu** du dossier `exodeclic_v10_1` dans ton dépôt Git en remplaçant les fichiers du code existant. Ne supprime pas ton dépôt pour créer un nouveau dépôt sous un autre nom.
3. En local, lance `start.bat` et vérifie la connexion, les cours, les exercices, les illustrations, `/admin`, les badges et les pages publiques.
4. Si le test local est satisfaisant : `git add .`, puis `git commit -m "V10.1 ExoDeclic marque et SEO"`, puis `git push`.
5. Dans Render, **conserve le même Web Service et la même DATABASE_URL Neon**. Vérifie que la variable `SITE_URL` vaut `https://www.exodeclic.fr` (avec `www`, car la redirection Render est configurée en ce sens).

## Ce qui change

- Nom public « ExoDéclic » dans l'interface, les titres et les pages de confidentialité ; nouveau favicon vectoriel.
- Un titre et une description par page publique ; URL canonique `https://www.exodeclic.fr/...`, Open Graph ; `noindex` pour les pages de connexion et de l'espace élève.
- Sur Render, les réponses HTML initiales des pages publiques contiennent **le texte des cours** directement depuis la base. React continue de rendre l'interface normale lorsque la page se charge. Les chapitres ajoutés ou modifiés dans `/admin` sont donc reflétés dans le HTML reçu à l'URL publique, sans rebuild.
- Les visites de l'ancienne adresse `*.onrender.com` vers les pages Web sont redirigées vers `www.exodeclic.fr` lorsque `SITE_URL` est configurée comme ci-dessus. Les endpoints `/api` et `/api/health` ne sont pas redirigés.
- `robots.txt` et `sitemap.xml` existent toujours et utilisent `SITE_URL`.

## Ce qui ne change PAS

- **Aucun changement de schéma de base, de contenu scolaire, d'identifiants de chapitres ou d'exercices.** Les comptes et les tentatives stockées dans la même base Neon restent en place.
- **Ne renomme pas** les anciens noms techniques `studysprint_session`, `studysprint-analytics-consent-v1`, `@@studysprint-blocks@@`, la base SQLite locale ni ton compte admin existant : ces éléments ont volontairement été conservés pour préserver la compatibilité.
- L'identifiant de mesure Google Analytics `G-KF2VQGLN8C` est conservé ; pas besoin de nouvelle propriété GA4.
- Une connexion réalisée sous l'ancien domaine Render ne peut pas automatiquement être transférée au nouveau domaine : reconnecte-toi sur `www.exodeclic.fr` avec **ton compte existant** si nécessaire.

## Vérifications de référencement après déploiement

- Ouvre `https://www.exodeclic.fr/` et un chapitre public `https://www.exodeclic.fr/decouvrir/cours/1`.
- Dans « Afficher le code source de la page » (pas seulement « Inspecter »), tu dois voir « ExoDéclic », la balise `canonical` du chapitre, ainsi que **le texte des fiches de cours dans le HTML initial**. Le compte et la progression n'apparaissent jamais dans cet HTML public.
- Vérifie `https://www.exodeclic.fr/robots.txt` et `https://www.exodeclic.fr/sitemap.xml`.
- Google Search Console : ton sitemap est déjà enregistré. Attends la prochaine exploration puis surveille « Pages ». Une URL soumise n'est pas garantie d'être indexée ni de bien se classer.
- Si tu modifies un cours dans `/admin`, recharge la page publique correspondante : son HTML initial doit refléter les changements.

## Important avant une communication grand public

La page `/confidentialite` contient encore un encart **« À compléter »** : complète l'identité de l'éditeur, les coordonnées et les informations légales adaptées à ton activité. Renommer StudySprint ne suffit pas pour rendre cette page légalement complète. Vérifie également les modalités de consentement adaptées à un site destiné à des mineurs.

**Validation technique effectuée :** routes HTML publiques et privées, balises SEO, sitemap, page de cours inconnue (404), redirection depuis l'ancien domaine et compilation Python. Le build Vite/React complet n'est pas disponible dans cet environnement : teste `start.bat` puis Render avant d'en faire la promotion.
