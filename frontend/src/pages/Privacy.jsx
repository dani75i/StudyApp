import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, ShieldCheck, Zap } from 'lucide-react';
import PublicFooter from '../components/PublicFooter';
import { openCookiePreferences } from '../analytics';

export default function Privacy() {
  useEffect(() => {
    document.title = 'Confidentialité et cookies — StudySprint';
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute('content', 'Informations sur la confidentialité, les cookies et la mesure d’audience Google Analytics utilisée par StudySprint.');
  }, []);

  return (
    <div className="public-page">
      <header className="public-nav">
        <Link className="brand" to="/"><span className="brand-mark"><Zap size={21} /></span><span>StudySprint</span></Link>
        <nav><Link to="/decouvrir/cours">Cours gratuits</Link><Link to="/connexion">Connexion</Link></nav>
      </header>

      <main className="public-content privacy-page">
        <Link className="back" to="/"><ArrowLeft size={17} /> Accueil</Link>
        <div className="privacy-heading">
          <span className="privacy-icon"><ShieldCheck size={28} /></span>
          <div><span className="eyebrow">CONFIDENTIALITÉ</span><h1>Confidentialité et mesure d'audience</h1></div>
        </div>

        <div className="privacy-notice">
          <strong>À compléter avant une communication publique large</strong>
          <p>Ajoute ici l'identité de l'éditeur de StudySprint et une adresse de contact permettant d'exercer les droits RGPD.</p>
        </div>

        <section className="privacy-section">
          <h2>Pourquoi Google Analytics est utilisé ?</h2>
          <p>StudySprint utilise Google Analytics uniquement après consentement afin de mesurer la fréquentation des pages publiques, comprendre l'origine générale du trafic et améliorer l'ergonomie du site.</p>
        </section>

        <section className="privacy-section">
          <h2>Quelles données sont concernées ?</h2>
          <p>La mesure peut notamment porter sur les pages publiques visitées, le type d'appareil, des informations techniques de navigation, la provenance générale du trafic et quelques événements non nominatifs comme le début ou la fin d'une inscription.</p>
          <p>StudySprint n'envoie pas à Google Analytics le prénom, l'adresse email, le mot de passe, les réponses détaillées aux exercices ni l'identifiant interne du compte.</p>
        </section>

        <section className="privacy-section">
          <h2>Quelles pages sont mesurées ?</h2>
          <p>Google Analytics est limité aux pages publiques, aux pages de connexion et d'inscription et à cette page de confidentialité. Il est désactivé dans l'espace élève authentifié, le tableau de bord, le profil, l'historique, les exercices privés et l'administration.</p>
        </section>

        <section className="privacy-section">
          <h2>Consentement et retrait</h2>
          <p>Google Analytics n'est pas chargé tant que la personne n'a pas choisi « Accepter les statistiques ». Le refus n'empêche pas d'utiliser StudySprint. Le choix peut être modifié à tout moment.</p>
          <button type="button" className="secondary" onClick={openCookiePreferences}>Modifier mes préférences de cookies</button>
        </section>

        <section className="privacy-section">
          <h2>Mineurs</h2>
          <p>StudySprint s'adresse notamment à des collégiens et lycéens. Lorsqu'un utilisateur a moins de 15 ans, l'accord d'un parent doit être recherché pour les traitements optionnels fondés sur le consentement. La mesure d'audience reste donc facultative.</p>
        </section>

        <section className="privacy-section">
          <h2>Durée de conservation</h2>
          <p>Pour le lancement, règle dans Google Analytics la conservation des données d'événements sur 2 mois. Le choix de consentement est mémorisé localement dans le navigateur afin de ne pas redemander la préférence à chaque page.</p>
        </section>

        <section className="privacy-section">
          <h2>Transferts et fournisseur</h2>
          <p>Google Analytics est un service fourni par Google. Son utilisation peut impliquer des traitements ou transferts de données hors de l'Espace économique européen selon la configuration et les services de Google. StudySprint n'active pas Google Signals, le remarketing ni la personnalisation publicitaire dans cette intégration.</p>
        </section>
      </main>

      <PublicFooter />
    </div>
  );
}
