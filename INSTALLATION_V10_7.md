# Installation d'ExoDéclic V10.7

1. Extraire l'archive et ouvrir le dossier `exodeclic_v10_7`.
2. Copier **le contenu** de ce dossier dans le dépôt Git utilisé pour ExoDéclic, sans supprimer `.git`, `.env` ni une base de données locale.
3. Ouvrir VS Code à la racine du dépôt, exécuter `start.bat` et vérifier les fiches de maths/physique, l'inscription et le compagnon sur le tableau de bord.
4. Vérifier le build frontend : `cd frontend`, `npm install`, `npm run build`, `cd ..`.
5. Lancer l'audit : `python tools/audit_v107.py` et les tests si souhaité (voir `RAPPORT_QUALITE_V10_7.md`).
6. Faire une sauvegarde de la base Neon avant la production, puis pousser vers GitHub :

```powershell
git status
git add .
git commit -m "V10.7 - Formules harmonisees et compagnon de progression"
git push
```

### Render

Aucune nouvelle variable d'environnement ni migration SQL manuelle n'est requise. Si le déploiement automatique est activé, le `git push` relance le service Docker. Sinon : **Manual Deploy → Deploy latest commit**. Attendre le statut **Live**, regarder les logs du build frontend et vérifier les pages publiques et privées.

Le patch des **35 leçons sélectionnées** s'exécute une seule fois au démarrage, uniquement si la fiche n'a pas été modifiée par l'administrateur. Les contenus personnalisés restent en place, même s'ils conservent donc éventuellement l'ancien format pédagogique.

Les erreurs 5xx et les règles `robots.txt` remontées dans Search Console doivent être examinées à part. Cette livraison n'affirme pas les avoir corrigées.
