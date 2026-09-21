# Installation de la V10.6

1. Faire une sauvegarde de votre projet actuel et conserver `.git`, `.env` et les données locales.
2. Dézipper puis copier **le contenu** du dossier `exodeclic_v10_6` dans la racine habituelle du dépôt Git, pas le dossier parent en tant que sous-dossier.
3. Tester en local via `start.bat` et vérifier les cours Thalès ainsi que les corrections de Pythagore.
4. Dans le terminal VS Code, à la racine du dépôt :

```powershell
git status
git add .
git commit -m "V10.6 - Corrections pas a pas et controle qualite des contenus"
git push
```

**Render** : si `Auto-Deploy` est activé, aucun changement de variables d'environnement n'est requis. Le build et le démarrage appliqueront une seule fois la mise à jour ciblée `quality-v10-6` sur la base liée à l'application. Vérifiez dans Render que le déploiement passe à `Live`, puis testez le site public. Si `Auto-Deploy` est désactivé : `Manual Deploy` > `Deploy latest commit`. Il est prudent de sauvegarder votre base Neon avant une mise à jour de contenus en production.

**Contrôles de qualité** : `python tools/audit_v106.py` et `python tools/test_v106_patch.py` (ce second script ne touche qu'à une base SQLite temporaire). Voir `RAPPORT_QUALITE_V10_6.md`.
