# Google Analytics — StudySprint

Measurement ID: `G-KF2VQGLN8C`

## Comportement technique

- Aucun script Google Analytics n'est présent statiquement dans `index.html`.
- Tant que le visiteur n'a pas choisi **Accepter les statistiques**, `gtag.js` n'est pas chargé.
- Le refus n'empêche aucune fonctionnalité de StudySprint.
- Le choix est mémorisé localement sous `studysprint-analytics-consent-v1`.
- Google Analytics est activé uniquement sur :
  - `/`
  - `/decouvrir/cours`
  - `/decouvrir/cours/:id`
  - `/connexion`
  - `/inscription`
  - `/confidentialite`
- Le runtime Analytics est désactivé dans l'espace élève authentifié et `/admin`.
- Aucun prénom, email, mot de passe, réponse d'exercice ou identifiant interne utilisateur n'est envoyé par le code Analytics.
- Google Signals, la personnalisation publicitaire et les consentements publicitaires sont désactivés/refusés dans l'intégration.

## Événements envoyés après consentement

- `page_view` : pages publiques autorisées uniquement.
- `cta_click` : principaux boutons publics.
- `course_opened` : ouverture d'une fiche de cours publique, avec identifiant de chapitre et matière.
- `sign_up_started` : première interaction avec le formulaire d'inscription.
- `sign_up` : inscription réussie, avec `method=email` uniquement.
- `login` : connexion réussie, avec `method=email` uniquement.

## Réglages GA4 à faire manuellement

1. Administration > Paramètres des données > Conservation des données : choisir **2 mois** pour la phase de lancement.
2. Ne pas activer Google Signals, le remarketing ou la personnalisation publicitaire.
3. Vérifier le flux Web et désactiver le suivi automatique des changements d'historique/pages si celui-ci crée des doublons. StudySprint envoie ses propres événements `page_view` pour les routes publiques autorisées.
4. Marquer éventuellement `sign_up` comme événement clé dans GA4 pour suivre le taux d'inscription.

## Avant une communication publique large

Compléter `/confidentialite` avec :
- l'identité du responsable de traitement / éditeur ;
- une adresse de contact permettant d'exercer les droits RGPD ;
- les mentions légales adaptées à la structure juridique réelle.

Ce fichier décrit le paramétrage technique du projet ; il ne remplace pas un avis juridique.
