# ExoDéclic : étude concurrentielle et priorités d’amélioration

Étude du 30 septembre 2026. Objectif confirmé : attirer davantage de parents et d’élèves, augmenter les inscriptions et préparer une offre comprenant une partie gratuite et une partie payante.

## 1. Conclusion et positionnement proposé

**La priorité est de rendre la valeur d’ExoDéclic visible avant l’inscription, de renforcer la confiance des parents et de transformer une première visite en une première réussite.** Le catalogue est déjà conséquent. Ajouter beaucoup de chapitres ou de nouvelles matières apporterait probablement moins, à court terme, qu’un meilleur parcours de découverte et quelques contenus exemplaires.

Positionnement recommandé, à tester auprès des familles : **« Des séances courtes de maths et de physique-chimie pour comprendre ses erreurs et savoir quoi retravailler au collège. »** La spécialisation sur deux matières peut rendre l’offre plus facile à comprendre. La gratuité et les badges, déjà proposés ailleurs, ne suffisent pas à différencier durablement le site.

Pour une future offre payante, la piste la plus cohérente est l’organisation du travail et un bilan compréhensible par les parents. La valeur de cet accompagnement doit toutefois être démontrée : un compteur d’exercices réussis ne prouve pas, à lui seul, une maîtrise durable.

Les effets attendus ci-dessous sont des **hypothèses de produit à mesurer**, pas des gains de conversion garantis.

## 2. Méthode et limites

L’étude croise :

- le code React/FastAPI du dépôt local, notamment les parcours publics, l’inscription, les exercices, la sélection quotidienne et les statistiques ;
- les réponses HTTP publiques du site déployé, son catalogue, son sitemap et les textes de son JavaScript public ;
- neuf chapitres publics échantillonnés : un par niveau et matière, plus Pythagore en 3e ;
- les pages officielles de six offres concurrentes et les informations du ministère sur les programmes.

L’accueil déployé répond HTTP 200. L’outil de recherche n’arrivait pas à lire ExoDéclic ; une lecture HTTP directe a permis les vérifications. **Cet échec de l’outil ne démontre ni une panne du site ni un problème d’indexation Google.**

Il ne s’agit pas d’un test visuel complet sur téléphone, d’un audit d’accessibilité, d’une validation pédagogique exhaustive ou d’un essai des abonnements concurrents. Aucun compte n’a été créé, aucune donnée privée consultée et aucune publication modifiée. Les comportements de l’espace connecté sont déduits du code local, sans garantie que chaque ligne soit identique au serveur de production. Les fonctionnalités concurrentes sont celles présentées publiquement ; leur efficacité pédagogique n’a pas été mesurée.

Le budget, le temps disponible, le trafic, les inscriptions et les élèves actifs n’ont pas été communiqués à la rédaction. Les estimations supposent une petite équipe ou une personne maîtrisant le projet. Il faudra les ajuster à ces informations.

## 3. Ce qu’ExoDéclic possède déjà

Comptage des entrées renvoyées par le [catalogue public en production](https://www.exodeclic.fr/api/public/catalog), et non addition des différents packs historiques du dépôt :

| Niveau | Chapitres | Fiches | Exercices annoncés |
|---|---:|---:|---:|
| 6e | 25 | 75 | 300 |
| 5e | 25 | 75 | 300 |
| 4e | 22 | 66 | 176 |
| 3e | 28 | 93 | 364 |
| **Total** | **100** | **309** | **1 140** |

Ces nombres mesurent un volume, pas la couverture exhaustive du programme, la diversité des exercices ou leur exactitude.

Les atouts à conserver et mieux montrer :

- des cours accessibles sans compte ;
- des indices progressifs et une correction après la réponse dans le parcours codé ;
- un historique, des objectifs, une séance quotidienne et des récompenses ;
- une spécialisation claire, de la 6e à la 3e ;
- une base SEO déjà construite : HTML de cours fourni par le serveur, titres, descriptions, URL canoniques et sitemap ;
- une mesure Google Analytics conditionnée au consentement et limitée aux pages publiques dans le code ;
- un formulaire de retour utilisateur.

Le [sitemap](https://www.exodeclic.fr/sitemap.xml) comporte 103 URL lors du contrôle. Il faut donc améliorer la découverte et le contenu des pages existantes plutôt que repartir de zéro sur le référencement.

## 4. Comparaison avec six offres

Les tarifs sont des affichages publics au moment de la consultation, susceptibles d’évoluer. Les promesses et chiffres commerciaux des concurrents ne sont pas traités comme des résultats indépendamment vérifiés.

| Offre | Proposition observable | Ce qu’ExoDéclic peut en apprendre | Possibilité de différenciation |
|---|---|---|---|
| **Afterclasse** | Révisions gratuites, fiches, exercices interactifs et badges. Le site met en avant une communauté de professeurs. | La gratuité, les exercices et la ludification sont déjà des attentes du marché. La provenance des contenus est un argument de confiance. | Faire essayer une séance très simple et expliquer précisément le traitement des erreurs. [Source](https://www.afterclasse.fr/) |
| **Lumni** | Offre gratuite sans publicité, vidéos, quiz et jeux ; espace collège et ressources brevet. | Des entrées par niveau, thème et besoin facilitent la découverte. L’identité de l’éditeur est clairement présentée. | Proposer un entraînement structuré et un prochain exercice pertinent après la consultation d’une notion. [Collège](https://www.lumni.fr/college), [présentation](https://www.lumni.fr/qui-sommes-nous) |
| **Mathenpoche / Sésamath** | Ressources de mathématiques : cours, exercices, aides animées, QCM, entraînement et jeux logiques. | La spécialisation en maths est viable ; la diversité des activités et les aides concrètes comptent. | Articuler maths et physique-chimie dans un parcours lisible pour une famille. [Source](https://mathenpoche.sesamath.net/) |
| **Maths et tiques** | Cours et exercices classés par niveau, nombreux supports et liens vidéo ; page 3e détaillée par notion. | Une page précise sur un problème scolaire constitue une porte d’entrée utile. Les exemples expliqués donnent de la valeur au contenu. | Relier immédiatement une explication à un exercice, une correction et une reprise ultérieure. [Cours](https://www.maths-et-tiques.fr/index.php/cours-maths), [3e](https://www.maths-et-tiques.fr/index.php/cours-maths/niveau-troisieme) |
| **Kartable** | Offre large, cours, quiz, exercices corrigés, PDF, préparation aux examens et suivi parental. Prix mensuel affiché : 14,99 € ; autres engagements annoncés à un équivalent mensuel inférieur. | Le parent voit explicitement ce qu’il achète et ce qu’il peut suivre. L’équipe pédagogique et le support sont mis en avant. | Tester une offre plus ciblée autour des erreurs et du travail hebdomadaire, avec une explication simple de sa valeur. [Source](https://www.kartable.fr/) |
| **SchoolMouv** | Offre collège riche en formats : cours, vidéos, synthèses, quiz, exercices et autres outils ; formules d’abonnement. | Différents supports répondent à différents besoins. La préparation aux contrôles et au brevet rend l’usage concret. | Soigner quelques parcours courts avant d’investir dans une vaste bibliothèque vidéo ou un accompagnement humain coûteux. [Collège](https://www.schoolmouv.fr/college), [offres](https://aide.schoolmouv.fr/knowledge/abonnements-et-offres) |

**Interprétation :** ExoDéclic dispose des composants d’un service utile. Son avantage commercial reste à construire autour de la facilité d’essai, de la qualité vérifiable des explications et du suivi. La présence d’une fonctionnalité chez un concurrent ne signifie pas qu’il faut la copier.

## 5. Les améliorations prioritaires, avec preuves

### A. Permettre une première expérience avant le compte

**Constat.** Le cours public mène à l’inscription pour répondre aux exercices et voir les corrections. Le principal bouton de l’accueil mène également à l’inscription. L’élève doit donc fournir des informations avant d’avoir essayé le cœur du service. Sources : `frontend/src/pages/PublicHome.jsx:35`, `PublicChapter.jsx:53`, `frontend/src/App.jsx:96`.

**Proposition.** Permettre un essai de trois exercices, avec indices et correction, sans compte. Au bilan : « Enregistre ta progression et retrouve les notions à revoir ». Conserver les réponses de l’essai lors de l’inscription, avec un fonctionnement clairement expliqué.

Parcours cible : **choisir sa classe → choisir une notion → répondre → comprendre la correction → créer son espace pour continuer.** Mesurer les inscriptions après essai et l’activité qui suit : une augmentation du nombre de comptes sans utilisation réelle ne serait pas un succès.

### B. Renforcer la confiance des parents

**Constat confirmé dans le JavaScript public déployé.** La page de confidentialité contient encore une instruction demandant d’ajouter l’identité de l’éditeur et une adresse de contact. Le code comporte aussi une consigne de réglage Analytics destinée à l’exploitant. Source : `frontend/src/pages/Privacy.jsx:30` et `:65`.

**Proposition immédiate.** Remplacer ces consignes par les informations réelles. Présenter qui porte le projet, comment joindre le responsable et comment les contenus sont préparés et relus. Faire correspondre les informations publiées aux pratiques effectives. Ce constat éditorial n’est pas un audit juridique.

Créer une page « Pour les parents » contenant une démonstration, un exemple de correction, l’explication du suivi et les réponses aux questions fréquentes. Publier des témoignages seulement lorsqu’ils sont authentiques et autorisés. Mentionner une relecture enseignante uniquement si elle a réellement eu lieu.

### C. Clarifier ce qui restera gratuit

**Constat confirmé en production.** L’accueil présente la gratuité comme liée au lancement et indique qu’aucun paiement n’est demandé pour le moment. Pour un parent, cela peut laisser planer un doute sur la suite. Source : `frontend/src/pages/PublicHome.jsx:31`.

**Proposition.** Définir d’abord le périmètre gratuit durable, puis afficher une formulation précise. Exemple possible après décision : « Les cours et les exercices essentiels sont gratuits. Des options de suivi familial seront proposées séparément. » Ne pas promettre une gratuité permanente si ce choix n’est pas arrêté.

La communication externe et la page d’arrivée doivent décrire la même offre.

### D. Faciliter le choix de la classe et conserver le contexte

**Constat.** Le catalogue public affiche les chapitres regroupés par matière sans filtre de classe dans le composant. L’inscription choisit la 3e par défaut. Après création du compte, elle mène au tableau de bord, même lorsque la visite provient d’un cours précis. Sources : `PublicCourses.jsx`, `Register.jsx:12` et `:26`.

**Proposition.** Afficher les choix 6e / 5e / 4e / 3e dès la découverte ; mémoriser le choix ; reprendre le chapitre ou l’exercice à l’origine de l’inscription. Expliciter l’usage de l’adresse email pour les familles. Prévoir la récupération d’un mot de passe, dont je n’ai trouvé ni page ni endpoint dans le code examiné.

### E. Améliorer d’abord les pages qui serviront à recruter

**Constats sur l’échantillon de production :**

- [Atomes, ions et molécules en 3e](https://www.exodeclic.fr/decouvrir/cours/18) présente trois fiches très brèves, proches de rappels de définitions ;
- [Nombres entiers et décimaux en 6e](https://www.exodeclic.fr/decouvrir/cours/51) répète certains textes entre explication et encadré ;
- [Pythagore en 3e](https://www.exodeclic.fr/decouvrir/cours/1) juxtapose des fiches anciennes et structurées sur les mêmes notions ;
- [Masse volumique en 4e](https://www.exodeclic.fr/decouvrir/cours/39) propose déjà davantage de méthode, d’unités et d’exemple.

**Proposition.** Sélectionner dix pages d’entrée et leur appliquer une structure commune : objectif, prérequis, explication, exemple résolu, erreur fréquente, mini-exercice, correction, étape suivante. Faire relire ces pages par un enseignant avant d’en faire les principales destinations des campagnes. Harmoniser ensuite le catalogue progressivement.

Le rapport local `RAPPORT_QUALITE_V10_7.md` précise lui-même que ses contrôles structurels ne prouvent pas l’exactitude de tous les exercices. Une bonne structure technique est un acquis ; la validation pédagogique reste un travail distinct.

Vérifier également la correspondance chapitre par chapitre avec les programmes effectivement applicables. La 5e est concernée par un nouveau programme de mathématiques à la rentrée 2026 : le nom « 2026 » d’un pack ne suffit pas à établir sa conformité. [Source officielle](https://www.education.gouv.fr/les-programmes-du-college-470408).

### F. Rendre le suivi cohérent avec les promesses

**Constat dans le code local.** La séance quotidienne sélectionne jusqu’à huit exercices, avec cet ordre : jamais tentés, tentés sans réussite, déjà réussis. À priorité égale, le classement varie selon la date et l’utilisateur. L’accueil annonce pourtant une priorité aux lacunes. Sources : `backend/app/main.py:1039`, `frontend/src/pages/PublicHome.jsx:44`.

Par ailleurs, la progression d’un chapitre comptabilise les exercices réussis au moins une fois. Elle ne démontre pas que la notion est retenue dans le temps. Source : `backend/app/main.py:94`. Certaines vues utilisent le dernier résultat, ce qui mérite une harmonisation des intitulés.

**Proposition.** À court terme, aligner le texte et le comportement. Ensuite, tester une sélection par besoin : difficulté récente, prérequis, notion choisie pour un contrôle, révision différée. Distinguer « réussi une fois », « à consolider » et « confirmé sur une nouvelle tentative ». La fréquence de révision doit être expérimentée, pas présentée comme validée scientifiquement par cet audit.

**Autre point à vérifier avant monétisation.** La comparaison de réponse accepte les textes normalisés et certaines écritures numériques équivalentes, mais pas une équivalence mathématique générale. Par exemple, `1/2` et `0,5` ne sont pas équivalents pour cette fonction. Les consignes doivent imposer une forme précise lorsque nécessaire, ou le correcteur doit accepter les formes appropriées à l’exercice. Source : `backend/app/main.py:981`.

## 6. Acquisition : où concentrer les efforts

### Référencement naturel

Créer des pages utiles par classe et matière, puis quelques pages répondant à des besoins précis : fractions en 5e, proportionnalité, Pythagore, conversions et loi d’Ohm. Ce sont des **pistes éditoriales**, pas des mots-clés dont le volume de recherche a été mesuré.

Chaque page devrait donner une vraie réponse et proposer immédiatement un exercice pertinent. Ajouter des liens entre prérequis, cours et exercices. Vérifier l’indexation réelle dans Search Console avant de conclure à un problème de visibilité. Les identifiants numériques actuels n’empêchent pas en eux-mêmes le référencement ; un changement d’URL n’est pas prioritaire.

### Partages et communautés

Faire arriver un parent sur une ressource correspondant à son besoin, par exemple un mini-parcours de fractions, plutôt que toujours sur l’accueil. Préparer une image d’aperçu pour les partages : je n’ai pas trouvé de balise `og:image` dans le HTML d’accueil ou le générateur SEO examiné.

Tester quelques canaux autorisant ce type de ressource : communautés de parents, associations locales et enseignants intéressés. Utiliser des liens de campagne identifiables et comparer les élèves actifs obtenus. Le nombre de publications ou de clics n’est pas une mesure suffisante de recrutement utile.

### Démonstration et preuve

Montrer un exemple réel du parcours « erreur → indice → correction → nouvelle tentative ». Une courte démonstration peut expliquer mieux le produit qu’une liste de fonctionnalités. L’accueil possède aujourd’hui une carte de séance illustrative ; elle ne constitue pas un essai interactif.

Ne lancer un budget publicitaire significatif qu’après avoir mesuré le parcours d’inscription et confirmé la valeur de la première séance auprès de familles.

## 7. Offre gratuite et payante recommandée pour un test

Ce découpage est une proposition à valider, pas une modification de l’offre actuelle.

| Gratuit | Payant à construire et tester |
|---|---|
| Cours publics, essai sans compte | Plan de travail pour un objectif ou un contrôle |
| Exercices essentiels, indices et corrections accessibles | Suivi des notions à consolider dans le temps |
| Compte et suivi personnel de base | Espace parent lié au compte enfant avec accès adapté |
| Possibilité de prendre une habitude de travail | Bilan hebdomadaire lisible, avec recommandations concrètes |
| Découverte des parcours | Parcours brevet structurés et fiches d’entraînement imprimables |

Le compte parent, les liens parent-enfant, les abonnements et la facturation demanderaient un développement spécifique : ils ne figurent pas dans les parcours et modèles examinés. Les corrections essentielles devraient rester accessibles dans le parcours gratuit pour permettre de constater la valeur pédagogique.

Tester d’abord l’intérêt auprès de cinq à dix parents : comprennent-ils le bilan, savent-ils quoi faire ensuite, souhaitent-ils retrouver cet accompagnement ? Puis tester une offre réelle clairement décrite. Le prix doit tenir compte de la disposition à payer et des coûts d’hébergement, de support, de contenu et de paiement. Le tarif d’un concurrent généraliste ne suffit pas à déterminer celui d’ExoDéclic.

Éviter pour l’instant d’engager un abonnement promettant un professeur disponible ou un accompagnement humain sans avoir organisé et chiffré ce service.

## 8. Feuille de route priorisée

Efforts indicatifs en jours de travail, comprenant développement et vérification mais pas les délais d’obtention des informations, la production exhaustive des cours ou une prestation externe. Ils ne constituent pas un devis et peuvent se chevaucher.

| Priorité | Action | Effet recherché | Effort indicatif | Critère de validation |
|---|---|---|---|---|
| P0 | Compléter identité, contact et textes publics | Confiance | 0,5–1 j après réception des informations | Plus de consignes internes sur les pages publiques |
| P0 | Définir et expliquer le périmètre gratuit | Compréhension de l’offre | 0,5–1 j | Les parents interrogés peuvent l’expliquer sans aide |
| P0 | Mesurer le parcours existant | Identifier le principal abandon | 1–3 j | Visite, début d’inscription et inscription suivis avec limites documentées |
| P1 | Filtre de classe et reprise du contexte après inscription | Réduire l’effort de navigation | 1–3 j | Retour à la bonne classe et à la bonne notion |
| P1 | Essai de trois exercices sans compte | Prouver la valeur avant l’inscription | 3–6 j | Essai utilisable, corrections visibles, progression récupérable |
| P1 | Page parents et démonstration réelle | Rassurer et expliquer le bénéfice | 1–3 j | Une famille comprend le fonctionnement en quelques minutes |
| P1 | Dix pages pédagogiques exemplaires et relues | Acquisition et satisfaction | 5–10 j, selon la relecture | Exemple, erreur fréquente, exercice et correction sur chaque page |
| P1 | Récupération de mot de passe | Faciliter le retour | 2–4 j | Parcours complet et sûr, testé de bout en bout |
| P2 | Pages par niveau et matière, liens entre contenus, aperçu social | Découverte et partage | 2–5 j hors rédaction | Pages accessibles et suivi de leur indexation |
| P2 | Sélection quotidienne et indicateurs de maîtrise améliorés | Fidélisation et valeur du suivi | 4–8 j puis expérimentation | Cohérence des états et progression mesurée sur de nouvelles tentatives |
| P3 | Prototype de bilan parent, puis offre payante | Valider la demande | 5–10 j pour un prototype ; commercialisation à chiffrer ensuite | Parents utilisateurs qui souhaitent réellement continuer |

**Ordre pratique sur 90 jours, à adapter aux disponibilités :** premier mois, confiance et premier essai ; deuxième mois, contenus d’entrée et recrutement ciblé ; troisième mois, qualité du suivi et expérimentation d’une offre parent. Les blocs P0/P1 ne sont pas tous obligatoirement terminables en trente jours par une personne à temps partiel.

## 9. Comment juger si les changements fonctionnent

Le code prévoit déjà `cta_click`, `course_opened`, `sign_up_started` et `sign_up`. Il faut vérifier les données effectivement reçues, pas seulement l’existence des appels. Google Analytics dépend du consentement : ses visiteurs et inscriptions mesurés ne représentent pas nécessairement toute l’audience.

| Indicateur | Définition proposée | Décision qu’il aide à prendre |
|---|---|---|
| Passage à l’essai | Visiteurs mesurés démarrant un exercice / visiteurs mesurés de la page | La promesse et le bouton donnent-ils envie d’essayer ? |
| Fin d’essai | Essais terminés / essais commencés | Le parcours est-il compréhensible ? |
| Inscription après essai | Comptes créés après essai / essais terminés, dans une fenêtre définie | L’essai donne-t-il envie de conserver sa progression ? |
| Activation | Nouveaux comptes faisant trois exercices sous 48 h / nouveaux comptes | L’inscription mène-t-elle à un usage réel ? |
| Retour à une semaine | Comptes activés refaisant un exercice entre J7 et J13 / comptes activés ayant assez de recul | L’usage se prolonge-t-il ? |
| Acquisition utile | Dépense du canal / comptes activés attribuables à ce canal | Où investir ? |
| Valeur du payant | Essais payants, usage, résiliations et retours qualitatifs | L’accompagnement justifie-t-il l’abonnement ? |

Pour l’activité connectée, commencer par des agrégats internes à partir des inscriptions et tentatives déjà nécessaires au service, avec accès limité et information adaptée ; ne pas activer automatiquement Google Analytics dans l’espace élève. L’attribution entre campagne et activité n’est pas acquise dans le code actuel et doit être conçue explicitement, avec les choix de confidentialité appropriés.

Fixer une situation de départ avant de donner des objectifs chiffrés. Si le trafic est faible, privilégier cinq séances observées avec des familles et des corrections successives plutôt qu’un test A/B trop petit pour conclure. Mesurer sur des populations comparables et attendre que chaque cohorte ait assez de recul.

## 10. Ce que je différerais

L’ouverture de nombreuses nouvelles matières, une application mobile native, une vaste production vidéo, de nouveaux badges et un assistant IA généraliste peuvent attendre. Dans les éléments examinés, ils répondent moins directement aux freins d’acquisition que la confiance, l’essai immédiat, la qualité des pages d’entrée et la continuité après inscription.

Une étude complémentaire utile porterait sur le rendu mobile réel, les temps de chargement, l’accessibilité au clavier et avec lecteur d’écran, les abandons mesurés et un échantillon plus large d’exercices. Aucun score de performance, taux de conversion ou gain de notes n’est inventé dans ce rapport.
