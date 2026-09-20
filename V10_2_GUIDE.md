# ExoDéclic V10.2 — Avis utilisateurs

## Nouveautés

Un formulaire privé permet aux visiteurs et élèves de laisser un avis sans compte :
- `⭐ Donner mon avis` : impression générale, avec note facultative de 1 à 5 ;
- `🐛 Signaler un problème` : bouton ou affichage défectueux ;
- `📚 Signaler une erreur` : erreur dans le cours, l'énoncé ou la correction ;
- `💡 Proposer une idée` : suggestion d'évolution.

Le formulaire envoie le type, le commentaire, la note facultative et **le chemin de la page ouverte**. Il ne demande pas de nom ou d'email, n'enregistre aucun identifiant d'utilisateur ni adresse IP avec l'avis, et n'envoie pas les commentaires à Google Analytics. Évitez néanmoins d'y placer des informations personnelles dans le texte libre.

### Où trouver le bouton ?

- Visiteurs non connectés : bouton « Donner mon avis » flottant dans les pages publiques.
- Élèves connectés sur ordinateur : bouton flottant ou lien en bas du menu latéral.
- Élèves connectés sur téléphone : onglet **Plus → Donner mon avis** (afin de ne pas recouvrir la barre de navigation).

### Administration

Connectez-vous avec **votre compte administrateur existant** puis ouvrez `/admin/avis`, ou bien `/admin` puis **Avis utilisateurs**. Vous pouvez filtrer par catégorie et statut, lire le message et sa page d'origine, passer de Nouveau à En cours / Traité / Classé sans suite, et supprimer un avis. Aucun avis n'est publié publiquement.

### Installation / mise à jour

1. Copiez les fichiers de `exodeclic_v10_2/` **dans le dossier du dépôt Git existant**, en conservant `.git`, `.env` et les éventuels fichiers de configuration locaux.
2. Lancez `start.bat` localement et vérifiez l'envoi d'un avis depuis une page publique et depuis un exercice. En local, vous pouvez tester la route `/admin/avis` avec votre compte admin.
3. Après vérification : `git add .`, `git commit -m "V10.2 avis utilisateurs et administration"`, `git push` ; Render effectue le déploiement si l'auto-deploy est activé.
4. À son démarrage, le backend crée **uniquement la nouvelle table `feedback`** grâce à `Base.metadata.create_all`. Les comptes, la progression, les cours et les exercices existants ne sont pas réinitialisés.

### Protection anti-spam et confidentialité

Un champ piège (« honeypot ») et une limite en mémoire de **3 messages/heure par adresse réseau observée par le serveur** sont ajoutés. Ces protections sont élémentaires, locales à un processus, et susceptibles de limiter plusieurs visiteurs partageant le même réseau. Pour un trafic important, prévoyez une protection partagée (WAF, CAPTCHA respectueux de la vie privée ou Redis) et un plan de modération.

L'interface invite à ne pas transmettre de données personnelles. La page Confidentialité décrit le traitement des retours mais **les mentions légales, les coordonnées de l'éditeur, la durée de conservation et la procédure d'exercice des droits doivent être finalisées avant une communication publique**. Les retours peuvent être supprimés dans l'admin. Aucune fonction d'envoi d'email n'a été ajoutée ; le formulaire ne permet pas de répondre directement à l'auteur.

### Vérification rapide après le déploiement

- Testez `https://www.exodeclic.fr/` et le formulaire en navigation privée (visiteur sans compte).
- Sur mobile connecté, ouvrez **Plus → Donner mon avis**.
- Connectez-vous comme administrateur : `https://www.exodeclic.fr/admin/avis` ; vérifiez le message, changez son statut et supprimez un message test.
- Vérifiez que `/api/admin/feedback` répond 401 sans compte et 403 avec un compte élève.
