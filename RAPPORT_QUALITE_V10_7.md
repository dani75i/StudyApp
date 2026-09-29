# ExoDéclic V10.7 — Rapport de vérification

## Fonctionnalités livrées

- **Rendu mathématique** : une formule explicite d'exemple avec division `\frac`, racine `\sqrt`, multiplication `\times` ou égalité développée est affichée avec le même `Formula` en mode `display` que le cours. Les simples variables courtes restent dans la phrase. Une formule longue peut défiler horizontalement sur mobile, sans casser la mise en page.
- **Fiches corrigées** : 35 mises à jour ciblées sur les classes 6e, 5e, 4e et 3e : racines carrées, puissances, Thalès, statistiques, volumes, certaines notions de proportions, de sciences et d'angles. Six formules de volumes sont distinguées en 3e (pavé, cube, cylindre, cône, pyramide, boule).
- **Inscription collège** : choix limité à 6e, 5e, 4e ou 3e dans le formulaire et le profil **et dans les schémas Pydantic côté API**. Un appel direct à l'API ne peut plus ouvrir de nouveau compte avec un niveau lycée. Aucun compte existant n'est supprimé.
- **Compagnon Déclic** : personnage SVG léger, quatre stades visuels (0, 8, 25 et 60 exercices distincts maîtrisés), affiché sur le tableau de bord. Sur les corrections, il bondit à la bonne réponse et fait un geste d'encouragement en cas d'erreur. Le choix `prefers-reduced-motion` désactive ces mouvements.
- **Préservation des personnalisations** : patch `quality-v107-math-lessons` appliqué une seule fois, uniquement si le corps de la fiche est rigoureusement identique à celui de la V10.5 ou V10.6 livrée. Les modifications faites dans `/admin` sont conservées et comptées comme ignorées. Aucun exercice ou compte n'est écrasé par ce patch.

## Vérifications réellement exécutées

| Contrôle | Résultat |
|---|---|
| Audit structurel du catalogue fourni | 100 chapitres, 300 fiches, 1 128 exercices : aucun problème selon les règles **définies** |
| Fiches V10.7 réécrites explicitement | 35, toutes présentes dans les packs sources |
| Formules / blocs d'exemple après superposition des patchs | 112 / 116 |
| Tests Pydantic d'inscription/profil | 6e–3e acceptés ; 2nde, 1re, terminale rejetés |
| Intégration base SQLite isolée | Patch V10.6 suivi du patch V10.7 : OK |
| Protection d'une fiche modifiée dans `/admin` | OK : 34 fiches mises à jour et 1 fiche personnalisée préservée dans le test |
| Rejouer le patch une seconde fois | OK : application unique |
| Routage de calculs LaTeX vers des blocs display (tests Node natifs) | OK : `\frac`, `\sqrt`, `\times` et formule développée |
| Analyse syntaxique JS/JSX | 36 fichiers analysés sans erreur de syntaxe |
| Build React via `npm run build` | **Non exécuté** : le registre npm est inaccessible depuis l'environnement de création |

L'audit vérifie les formats JSON, la présence des réponses, la cohérence des QCM, les blocs LaTeX et plusieurs défauts précédemment relevés. **Il ne prouve pas que toutes les réponses, les calculs et les formulations pédagogiques des 1 128 exercices sont exacts.** Les cours personnalisés de la base Neon ne sont pas inclus dans l'audit hors ligne. Une relecture humaine demeure nécessaire.

### Tests reproductibles

Depuis la racine du projet :

```powershell
python tools/audit_v106.py
python tools/audit_v107.py
python tools/test_v106_patch.py
python tools/test_v107_release.py
node tools/test_v107_rendering.mjs
```

Sur un ordinateur avec les dépendances npm disponibles :

```powershell
cd frontend
npm install
npm run build
cd ..
```

## Vérification manuelle conseillée avant publication

1. Une fiche 3e « Racines carrées » et une fiche « Statistiques » : affichage correct des racines et fractions dans les blocs bleus.
2. Une fiche « Géométrie dans l'espace » : six formules distinctes, accessibles sur mobile.
3. Les exemples du chapitre Thalès : aucune distributivité.
4. Une fiche « Puissances » : division de puissances en grand dans l'exemple.
5. Inscription avec 6e / 3e : OK ; l'option lycée ne doit pas apparaître et l'API la refuse.
6. Sur le tableau de bord : le compagnon évolue après avoir maîtrisé des exercices distincts.
7. Sur une correction : animation de joie pour une bonne réponse, encouragement pour une erreur ; aucune animation si l'OS a désactivé les animations.
8. Dans `/admin` : les cours que vous aviez personnalisés doivent conserver leur texte initial.
9. Dans Search Console : vérifier séparément les 4 URL 5xx et la règle `robots.txt` ; cette version **ne résout pas** ces problèmes sans en connaître la cause actuelle.

## Avant de déployer

Faire une sauvegarde de la base Neon. Le patch est ciblé et ne doit pas toucher les comptes ni les tentatives, mais une sauvegarde reste utile avant toute mise à jour de production.
