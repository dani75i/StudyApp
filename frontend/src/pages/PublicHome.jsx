import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Atom, BookOpenText, Calculator, CheckCircle2, Dumbbell, Sparkles, Target, Zap } from 'lucide-react';
import PublicFooter from '../components/PublicFooter';
import { trackEvent } from '../analytics';

export default function PublicHome() {
  useEffect(() => {
    document.title = 'StudySprint — Maths et physique du collège au lycée';
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute('content', 'Cours de maths et physique, exercices corrigés et suivi de progression pour les collégiens et lycéens. StudySprint est gratuit pendant sa phase de lancement.');
  }, []);

  return (
    <div className="public-page">
      <header className="public-nav">
        <Link className="brand" to="/"><span className="brand-mark"><Zap size={21} /></span><span>StudySprint</span></Link>
        <nav>
          <Link to="/decouvrir/cours">Cours gratuits</Link>
          <Link to="/connexion">Connexion</Link>
          <Link className="primary compact" to="/inscription" onClick={() => trackEvent('cta_click', { cta_name: 'nav_signup', destination: '/inscription' })}>Créer mon compte</Link>
        </nav>
      </header>

      <main>
        <section className="public-hero">
          <div className="public-hero-copy">
            <span className="public-kicker"><Sparkles size={15} /> Gratuit pendant le lancement</span>
            <h1>Progresse en maths et en physique, un exercice à la fois.</h1>
            <p>Des cours clairs, des exercices corrigés et un tableau de bord personnel pour savoir exactement ce que tu maîtrises et ce qu'il faut retravailler.</p>
            <div className="public-actions">
              <Link className="primary public-cta" to="/inscription" onClick={() => trackEvent('cta_click', { cta_name: 'hero_signup', destination: '/inscription' })}>Commencer gratuitement <ArrowRight size={18} /></Link>
              <Link className="secondary public-cta" to="/decouvrir/cours" onClick={() => trackEvent('cta_click', { cta_name: 'hero_courses', destination: '/decouvrir/cours' })}>Voir les cours</Link>
            </div>
            <div className="public-proof"><CheckCircle2 size={17} /> Aucun paiement demandé pour le moment</div>
          </div>

          <div className="public-demo-card">
            <div className="demo-top"><span>Séance du jour</span><b>3e</b></div>
            <h2>15 minutes pour avancer</h2>
            <div className="demo-subject"><span className="demo-icon math"><Calculator size={20} /></span><div><strong>Pythagore</strong><small>3 exercices • priorité à tes lacunes</small></div></div>
            <div className="demo-subject"><span className="demo-icon physics"><Atom size={20} /></span><div><strong>Énergie et puissance</strong><small>2 exercices • niveau progressif</small></div></div>
            <div className="bar demo-bar"><span style={{ width: '62%' }} /></div>
            <div className="demo-footer"><span>Progression du jour</span><b>62 %</b></div>
          </div>
        </section>

        <section className="public-section">
          <div className="public-section-head"><span className="eyebrow">POURQUOI STUDYSPRINT</span><h2>Un outil pensé pour travailler, pas seulement lire.</h2></div>
          <div className="public-feature-grid">
            <article><span className="feature-icon"><BookOpenText /></span><h3>Cours essentiels</h3><p>Des fiches courtes et structurées pour revoir la notion avant de passer à la pratique.</p></article>
            <article><span className="feature-icon"><Dumbbell /></span><h3>Exercices corrigés</h3><p>Travaille par difficulté et retrouve immédiatement les exercices à revoir.</p></article>
            <article><span className="feature-icon"><Target /></span><h3>Progression personnelle</h3><p>Ton compte mémorise tes réussites, tes chapitres maîtrisés et ton objectif de la semaine.</p></article>
          </div>
        </section>

        <section className="public-subjects">
          <div><span className="subject-logo math"><Calculator size={28} /></span><h3>Mathématiques</h3><p>Calcul, géométrie, fonctions, théorèmes et résolution de problèmes.</p></div>
          <div><span className="subject-logo physics"><Atom size={28} /></span><h3>Physique-Chimie</h3><p>Énergie, électricité et compréhension des grands phénomènes physiques.</p></div>
        </section>

        <section className="public-final-cta">
          <h2>Commence avec une vraie progression personnelle.</h2>
          <p>Crée ton compte gratuitement et retrouve ton travail à chaque connexion.</p>
          <Link className="primary public-cta" to="/inscription" onClick={() => trackEvent('cta_click', { cta_name: 'final_signup', destination: '/inscription' })}>Créer mon espace <ArrowRight size={18} /></Link>
        </section>
      </main>

      <PublicFooter />
    </div>
  );
}
