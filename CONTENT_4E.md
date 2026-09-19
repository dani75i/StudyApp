# Contenu 4e — premier catalogue (rentrée 2026-2027)

Le pack `backend/content/4e_2026_v1.json` ajoute **13 chapitres de mathématiques et 9 chapitres de physique-chimie**, soit **66 fiches structurées et 176 exercices corrigés** (8 exercices par chapitre, difficultés 1 à 3).

L'objectif est un premier parcours de révision pour la 4e ; **ce n'est pas une garantie d'exhaustivité du programme officiel**, ni un substitut aux manuels et progressions pédagogiques de chaque établissement. Relire et tester les énoncés/corrections avant toute communication large.

Références de cadrage (programmes en vigueur, septembre 2026) :
- Mathématiques collège : https://eduscol.education.gouv.fr/5736/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-4 (nouveau programme appliqué en 4e à partir de 2027-2028).
- Physique-chimie cycle 4 : https://eduscol.education.gouv.fr/5739/ressources-d-accompagnement-du-programme-de-physique-chimie-au-cycle-4 (progressions différenciées en 5e, 4e et 3e).

## Installation et conservation des données

Le pack possède l'identifiant `fr-4e-2026-v1`, enregistré dans `content_packs` après import. Au prochain démarrage sur Render, l'import le crée **une seule fois** dans la base Neon actuelle. Les comptes, corrections, tentatives, chapitres de 3e et modifications réalisées dans `/admin` sont conservés. Le redémarrage suivant ne réimporte pas le pack. Aucun changement de schéma SQL n'est nécessaire.

Pour voir les cours de 4e sur un compte de démonstration existant, ouvrir **Plus → Profil** sur mobile ou **Profil** sur ordinateur, changer la classe en **4e** et enregistrer. Les autres comptes ne sont pas modifiés.

## Images

Les illustrations fixes de physique sont livrées en WebP dans `frontend/public/illustrations/physics/` et restent des fichiers du code GitHub, pas des fichiers à écrire sur le disque éphémère de Render. La 4e réutilise les images des phénomènes identiques, sans générer ni stocker d'image en base à chaque visite.
