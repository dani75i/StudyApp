# ExoDéclic V10.6 — rapport de qualité pédagogique et technique

## Périmètre contrôlé

L'audit porte sur le contenu **livré dans les fichiers du projet**, en simulant les 10 corrections de fiches et 4 corrections d'énoncés de la V10.6. Il ne peut pas lire les modifications qui ont été effectuées directement dans votre base Neon depuis `/admin`.

| Contrôle | Résultat |
|---|---:|
| Chapitres (6e, 5e, 4e, 3e) | 100 |
| Fiches de cours uniques | 300 |
| Exercices uniques | 1 128 |
| Blocs de formule structurés, après patch | 86 |
| Blocs d'exemple structurés, après patch | 90 |
| Anomalies relevées par les **contrôles automatiques définis** | 0 |

**Attention :** zéro anomalie détectée ne signifie pas que les 1 128 réponses et corrections sont toutes mathématiquement ou pédagogiquement exactes. Les contrôles automatiques vérifient surtout la structure, les choix QCM, la présence des réponses/corrections, la difficulté, l'équilibre des accolades LaTeX et plusieurs régressions hors sujet déjà identifiées. Une revue de fond par un enseignant reste souhaitable avant de commercialiser l'intégralité du catalogue.

## Corrections de fond effectuées dans V10.6

- **Thalès (3e)** : configuration avec hypothèses explicites, rapports de côtés correspondants présentés dans le même bloc de formule que les autres cours, méthode distincte, exemple de calcul géométrique, agrandissement/réduction sans exemple de distributivité.
- **Quatre exercices de Thalès** : ajout de l'hypothèse de parallélisme absente des énoncés et d'une démarche détaillée sous réserve que l'énoncé/correction initial n'ait pas été modifié dans `/admin`.
- **Pythagore (3e et 4e)** : 20 exercices dotés de démarches séparant identification du triangle, formule, calcul, puis conclusion ; calculs vérifiés dans le script de construction. Les autres exercices bénéficient d'une présentation générale plus aérée, mais n'ont pas tous reçu une correction de fond.
- **Autres exemples hors sujet corrigés** : homothétie dans les isométries (3e) et la translation (4e), aire de rectangle dans une fiche de calcul de durée (6e) et d'angles complémentaires (6e), exemple de circuit électrique inadapté à la leçon sur les mesures (3e), exemple de propagation de la lumière inadapté à la distinction des sources lumineuses (4e).
- **Fonctions (3e)** : séparation de la formule générale et du calcul d'image/antécédent, précédemment mélangés.

Au total, **10 leçons** ont reçu des modifications pédagogiques ciblées. Ces chiffres ne doivent pas être interprétés comme une relecture humaine exhaustive de toutes les fiches et de tous les exercices.

## Correction de la présentation

Les exercices qui ont des étapes enregistrées affichent chacune dans un cadre distinct, avec leurs mathématiques à la ligne. Pour les corrections historiques sans étapes, l'interface sépare prudemment les segments au niveau des points-virgules, des retours à la ligne, des phrases et de « donc » ; elle **ne prétend pas fabriquer une démonstration nouvelle** à partir d'une phrase courte. Le texte de la correction d'origine et les réponses sauvegardées restent inchangés.

## Sécurité de la mise à jour sur une base existante

Le patch `quality-v10-6` est **appliqué une seule fois** au démarrage du backend, uniquement aux fiches dont le contenu est identique au contenu V10.5 fourni. Les fiches éditées dans `/admin` sont conservées. Les démarches des exercices ne sont complétées que si aucune démarche n'existe déjà ; les corrections personnalisées ne sont pas remplacées. Les comptes, les tentatives et les progressions ne sont pas touchés.

## Tests exécutés

- Compilation Python des modules du backend et du script d'audit : OK.
- Import de tous les packs dans une base SQLite temporaire : 100 chapitres, 300 leçons et 1 128 exercices ; patch V10.6 et seconde exécution idempotente : OK.
- Test d'intégration séparé préservant une fiche et un guide modifiés dans `/admin` : OK.
- Vérification arithmétique des exemples de Pythagore réécrits et des quatre calculs de Thalès : OK (assertions lors de la construction du patch).
- Présentation des corrections : test JavaScript de séparation de texte court et d'une expression LaTeX : OK.
- Build React complet : **non exécuté** dans cet environnement. L'installation hors ligne échoue car `katex` n'est pas disponible dans le cache npm ; vérifier avec `npm install` puis `npm run build` ou `start.bat` sur votre PC, et contrôler ensuite les logs du build sur Render.

## À vérifier manuellement avant une diffusion plus large

1. Sur téléphone et ordinateur : les formules de Thalès et les corrections de Pythagore (dont le triangle 5–6–8 et l'hypoténuse 7–24).
2. Sur un compte élève : quatre étapes de correction apparaissent correctement pour les exercices de Pythagore réécrits.
3. Dans `/admin` : une ancienne correction personnalisée doit rester intacte.
4. Relire pédagogiquement les fiches et exercices non ciblés : notamment les démonstrations, les figures, les unités, les réponses ambiguës et les erreurs de niveau/programme.

Pour reproduire l'audit hors ligne : `python tools/audit_v106.py`. Le détail machine est dans `QUALITY_AUDIT_V10_6.json`.
