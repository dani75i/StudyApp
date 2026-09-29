# ExoDéclic V10.8 — Accueil fusionné, niveaux et prochaine mission

## Ce qui change

- Le personnage Déclic est intégré **dans la carte violette du haut**, entre l'accueil et l'objectif hebdomadaire. Le second encadré dédié au personnage est retiré.
- Déclic dispose de cinq niveaux fondés sur les exercices *distincts* réussis : Explorateur (0), Chercheur (8), Stratège (25), Expert (60), Maître Déclic (120). La jauge indique la progression entre le palier actuel et le suivant. Au niveau 5, elle reste pleine.
- Le bloc « Ta prochaine mission », juste après la carte violette, ouvre le premier exercice **non terminé** de la séance fournie par `/api/daily-session`. Lorsqu'une séance est terminée, il propose de consulter un chapitre non maîtrisé ou les cours ; si la récupération de la séance échoue, il propose la page Séance.
- La carte de présentation du personnage et les invitations redondantes à la séance/au chapitre recommandé ont été retirées du tableau de bord. Le réglage de l'objectif hebdomadaire reste accessible plus bas.
- La présentation est adaptée aux écrans étroits. Les animations de réussite/encouragement existantes restent inchangées : **aucune animation supplémentaire**.

## Installation depuis le ZIP

1. Extraire le ZIP et ouvrir le dossier `exodeclic_v10_8`.
2. Copier **le contenu** de ce dossier dans le dépôt Git ExoDéclic habituel. Ne pas remplacer ni effacer `.git`, `.env` ou une base locale.
3. Depuis VS Code, lancer `start.bat` et contrôler le tableau de bord sur PC et mobile.
4. Vérifier le frontend :

   ```powershell
   cd frontend
   npm install
   npm run build
   cd ..
   ```

5. Vérifier les règles métier indépendamment de React :

   ```powershell
   node --test tools/test_dashboard_v108.mjs
   ```

6. Depuis la racine du dépôt, publier :

   ```powershell
   git status
   git add .
   git commit -m "V10.8 - Fusion du dashboard, niveaux Declic et prochaine mission"
   git push
   ```

## Render

- **Aucune** nouvelle variable d'environnement, migration SQL ou manipulation Neon : mise à jour exclusivement côté frontend.
- Déploiement automatique si configuré. Sinon, Render → **Manual Deploy → Deploy latest commit**.
- Attendre le statut **Live** et vérifier les logs de build Vite.
- Tester avec un compte étudiant : niveau et barre de Déclic, ouverture du bon exercice via « Ta prochaine mission », progression après un exercice, puis adaptation mobile.
- Les alertes Google Search Console (5xx, robots.txt) ne sont **pas** corrigées par cette modification purement visuelle.

## Tests et limites

Les tests Node dans `tools/test_dashboard_v108.mjs` contrôlent les cinq niveaux et le calcul des paliers, ainsi que les différents états de la mission. Une vérification de mise en page à six tailles d'écran (maquette utilisant les classes et CSS de l'application) a vérifié l'absence de débordement horizontal.

Le build Vite complet n'a **pas** pu être lancé dans l'environnement de génération, car les dépendances NPM ne pouvaient pas être téléchargées. Il faut donc le faire localement avant de déployer.
