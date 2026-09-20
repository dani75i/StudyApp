# StudySprint V10 — 6e, 5e, illustrations et trophées

Cette version complète le **premier catalogue** de mathématiques et sciences pour les quatre classes du collège. Elle part du code de la V9 et conserve son parcours d'exercices et sa navigation flottante sur téléphone.

## Contenu ajouté

| Niveau | Mathématiques | Sciences | Fiches de cours | Exercices |
|---|---:|---:|---:|---:|
| 6e | 15 chapitres | 10 chapitres | 75 | 300 |
| 5e | 15 chapitres | 10 chapitres | 75 | 300 |
| **Total ajouté** | **30** | **20** | **150** | **600** |

En 6e, ces chapitres scientifiques constituent une sélection de notions de **sciences et technologie** ; en 5e, de **physique-chimie**. Il s'agit d'un **premier catalogue**, et non de l'intégralité des programmes officiels, ni de contenus dont tous les exercices auraient été relus par un enseignant. Vérifiez la progression, les énoncés et les corrections avant diffusion à un large public.

Les 20 visuels scientifiques vectoriels (`frontend/public/illustrations/physics/v10/`) sont spécifiques aux chapitres de 6e et de 5e. Ils illustrent les cartes de cours et les en-têtes de chapitres. **Ce sont des pictogrammes/schémas d'illustration, et non des montages électriques à reproduire en classe.**

## Indices

- Les **600 nouveaux exercices** reçoivent deux indices progressifs associés à la question et, lorsque c'est pertinent, aux nombres de l'énoncé. La correction reste sur sa page séparée.
- Pour les exercices de **3e et de 4e sans guide enregistré**, une aide liée à la notion (Thalès, équations, circuits, etc.) remplace le message passe-partout. Les anciens guides déjà présents, notamment ceux rédigés dans `/admin`, ne sont **jamais remplacés**.
- Les anciens indices ne sont pas tous rédigés individuellement : utilisez `/admin` pour affiner les exercices qui nécessitent un accompagnement spécifique.

## Récompenses

Les badges obtenus s'affichent en premier, en couleur avec une bordure et un cartouche « Débloqué ». Les objectifs verrouillés sont désaturés, affichent « À obtenir » et une barre de progression. Affichage adapté aux écrans de téléphone. Les seuils de déblocage et les données de progression restent inchangés.

## Installation dans votre dépôt existant

1. **Sauvegarder** ou committer vos changements locaux. Ne supprimez **jamais** `.git`, `backend/.env`, `frontend/.env` ou votre base SQLite locale si vous voulez conserver les comptes locaux.
2. Dézipper et **copier le contenu de `studysprint_v10`** dans le dossier du dépôt Git déjà utilisé pour V9, en remplaçant les fichiers du projet. Ne remplacez pas le dossier de travail par un nouveau dépôt vide.
3. Double-cliquer sur `start.bat`, ou lancer `./start.bat` dans le terminal Windows. Choisir **6e** puis **5e** dans le profil d'un compte élève. Vérifier Cours, Exercices, Indices, Récompenses et `/admin`.
4. Vérifier la génération des pages et des visuels sur un téléphone ou avec l'inspecteur responsive. Tester aussi les cours 3e et 4e ainsi qu'un compte déjà existant.
5. Après les tests locaux :

```powershell
git status
git add .
git commit -m "V10 contenus 6e 5e et nouvelles recompenses"
git push
```

Render utilise toujours `DATABASE_URL`/Neon : **aucune nouvelle base** et aucune réinitialisation ne sont nécessaires. Les deux nouveaux packs (`fr-6e-2026-v10` et `fr-5e-2026-v10`) sont ajoutés **une seule fois** au démarrage. Les cours et exercices déjà modifiés depuis `/admin` ne sont pas écrasés ; les comptes et tentatives existants restent en place. Évitez d'importer manuellement les JSON dans la base.

### Vérifications réalisées

- Python : compilation des fichiers Python, import complet sur SQLite vierge, décompte des contenus, redémarrage et conservation de modifications enregistrées en base.
- Fichiers SVG : parsing XML des 20 illustrations.
- JSX React modifié : contrôle syntaxique avec TypeScript.
- **Non vérifié ici :** build complet `npm run build` et rendu visuel dans un navigateur. Testez `start.bat` et le rendu mobile **avant** de déployer sur Render.
