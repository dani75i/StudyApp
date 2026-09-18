import React, { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  Award,
  BookOpenText,
  CheckCircle2,
  Crown,
  Dumbbell,
  Flame,
  Medal,
  Rocket,
  Sparkles,
  Star,
  Target,
  Trophy,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../api';

const badgeIcons = {
  sparkles: Sparkles,
  medal: Medal,
  trophy: Trophy,
  flame: Flame,
  target: Target,
  star: Star,
  rocket: Rocket,
  crown: Crown,
};

function Stat({ icon: Icon, label, value, sub, tone = 'violet' }) {
  return (
    <div className={`stat-card stat-${tone}`}>
      <div className="stat-icon"><Icon size={21} /></div>
      <div><span>{label}</span><strong>{value}</strong><small>{sub}</small></div>
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [goalBusy, setGoalBusy] = useState(false);
  const [toastBadge, setToastBadge] = useState(null);

  const load = () => api('/dashboard').then(setData);
  useEffect(() => { load(); }, []);

  useEffect(() => {
    if (!data?.badges) return;
    const unlockedIds = data.badges.filter((badge) => badge.unlocked).map((badge) => badge.id);
    const storageKey = 'studysprint-unlocked-badges';
    const previous = JSON.parse(localStorage.getItem(storageKey) || '[]');
    const newlyUnlocked = data.badges.find((badge) => badge.unlocked && !previous.includes(badge.id));
    if (previous.length && newlyUnlocked) {
      setToastBadge(newlyUnlocked);
      setTimeout(() => setToastBadge(null), 4500);
    }
    localStorage.setItem(storageKey, JSON.stringify(unlockedIds));
  }, [data]);

  const badgeStats = useMemo(() => {
    if (!data?.badges) return { unlocked: 0, total: 0, percent: 0 };
    const unlocked = data.badges.filter((badge) => badge.unlocked).length;
    const total = data.badges.length;
    return { unlocked, total, percent: total ? Math.round((unlocked / total) * 100) : 0 };
  }, [data]);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  const changeGoal = async (value) => {
    setGoalBusy(true);
    try {
      await api('/weekly-goal', { method: 'PATCH', body: JSON.stringify({ weekly_goal: value }) });
      await load();
    } finally {
      setGoalBusy(false);
    }
  };

  const featuredBadges = [...data.badges]
    .sort((a, b) => Number(b.unlocked) - Number(a.unlocked) || (b.progress / b.target) - (a.progress / a.target))
    .slice(0, 4);

  return (
    <>
      {toastBadge && (
        <div className="achievement-toast">
          <div className="achievement-toast-icon"><Sparkles size={20} /></div>
          <div><span>Nouveau badge débloqué</span><strong>{toastBadge.title}</strong></div>
        </div>
      )}

      <section className="dashboard-hero-card">
        <div className="dashboard-hero-copy">
          <div className="dashboard-kicker"><Sparkles size={15} /> TON ESPACE DE PROGRESSION</div>
          <h1>Bonjour {data.first_name} 👋</h1>
          <p>Une nouvelle séance, quelques exercices bien choisis, et tu avances encore en {data.level}.</p>
          <div className="dashboard-hero-actions">
            <Link className="primary hero-primary" to="/seance">Commencer ma séance <ArrowRight size={18} /></Link>
            <Link className="hero-link" to="/cours"><BookOpenText size={17} /> Réviser un cours</Link>
          </div>
        </div>

        <div className="hero-goal-panel">
          <div className="hero-goal-top">
            <span>Objectif de la semaine</span>
            <strong>{data.weekly.completed}/{data.weekly.target}</strong>
          </div>
          <div className="hero-goal-orb" style={{ '--goal-progress': `${data.weekly.percent * 3.6}deg` }}>
            <div><strong>{data.weekly.percent}%</strong><span>atteint</span></div>
          </div>
          <div className="hero-goal-foot">
            <span><CheckCircle2 size={15} /> {data.weekly.correct} réussis</span>
            <span><Flame size={15} /> {data.stats.streak} j de série</span>
          </div>
        </div>
      </section>

      <div className="stats-grid dashboard-stats">
        <Stat icon={CheckCircle2} label="Exercices maîtrisés" value={data.stats.correct} sub={`${data.stats.completed} tentés`} tone="green" />
        <Stat icon={Target} label="Taux de réussite" value={`${data.stats.success_rate}%`} sub="sur les exercices tentés" tone="violet" />
        <Stat icon={Flame} label="Série actuelle" value={`${data.stats.streak} j`} sub="jours d'entraînement" tone="orange" />
        <Stat icon={Trophy} label="Exercices disponibles" value={data.stats.available} sub={`pour le niveau ${data.level}`} tone="gold" />
      </div>

      <section className="achievement-showcase">
        <div className="achievement-showcase-head">
          <div>
            <span className="eyebrow reward-eyebrow">RÉCOMPENSES</span>
            <h2><Award size={23} /> Ta collection prend forme</h2>
            <p>{badgeStats.unlocked} badge{badgeStats.unlocked > 1 ? 's' : ''} débloqué{badgeStats.unlocked > 1 ? 's' : ''} sur {badgeStats.total}. Continue pour remplir la vitrine.</p>
          </div>
          <Link className="reward-link" to="/recompenses">Voir toutes les récompenses <ArrowRight size={16} /></Link>
        </div>

        <div className="achievement-overview">
          <div className="collection-meter" style={{ '--collection-progress': `${badgeStats.percent * 3.6}deg` }}>
            <div><strong>{badgeStats.percent}%</strong><span>collection</span></div>
          </div>

          <div className="featured-badges">
            {featuredBadges.map((badge, index) => {
              const Icon = badgeIcons[badge.icon] || Medal;
              const percent = Math.min(100, Math.round((badge.progress / badge.target) * 100));
              return (
                <Link to="/recompenses" className={`featured-badge ${badge.unlocked ? 'unlocked' : ''} badge-tone-${index + 1}`} key={badge.id}>
                  <div className="featured-badge-icon"><Icon size={23} /></div>
                  <div className="featured-badge-copy">
                    <span>{badge.unlocked ? 'Débloqué' : `${percent}%`}</span>
                    <strong>{badge.title}</strong>
                    <div className="mini-progress"><i style={{ width: `${percent}%` }} /></div>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      <div className="dashboard-two-col polished-grid">
        <section className="weekly-card polished-card">
          <div className="weekly-card-head">
            <div>
              <span className="eyebrow">OBJECTIF HEBDOMADAIRE</span>
              <h2>{data.weekly.completed}/{data.weekly.target} exercices</h2>
              <p>{data.weekly.correct} réussis cette semaine</p>
            </div>
            <div className="weekly-percent">{data.weekly.percent}%</div>
          </div>
          <div className="bar weekly-bar"><span style={{ width: `${data.weekly.percent}%` }} /></div>
          <div className="goal-actions">
            <span>Mon objectif :</span>
            {[10, 20, 30, 40].map((value) => (
              <button key={value} disabled={goalBusy} className={data.weekly.target === value ? 'active' : ''} onClick={() => changeGoal(value)}>{value}</button>
            ))}
          </div>
        </section>

        <section className="daily-cta-card polished-card">
          <div className="daily-cta-icon"><Sparkles size={24} /></div>
          <div>
            <span className="eyebrow">SÉANCE DU JOUR</span>
            <h2>Prêt pour quelques minutes utiles ?</h2>
            <p>La sélection privilégie ce qu'il te reste à maîtriser.</p>
          </div>
          <Link className="primary" to="/seance">Démarrer <ArrowRight size={17} /></Link>
        </section>
      </div>

      <div className="quick-grid polished-quick-grid">
        <Link className="quick-card quick-course" to="/cours">
          <div className="quick-icon"><BookOpenText size={20} /></div>
          <div><strong>Réviser un cours</strong><p>Une fiche claire pour revoir une notion en quelques minutes.</p></div>
          <ArrowRight size={16} />
        </Link>
        <Link className="quick-card quick-practice" to="/exercices">
          <div className="quick-icon"><Dumbbell size={20} /></div>
          <div><strong>Choisir mes exercices</strong><p>Filtre par chapitre, difficulté ou progression.</p></div>
          <ArrowRight size={16} />
        </Link>
      </div>

      {data.recommended && (
        <section className="focus-card focus-card-v7">
          <div>
            <span className="eyebrow">À TRAVAILLER MAINTENANT</span>
            <h2>{data.recommended.emoji} {data.recommended.title}</h2>
            <p>{data.recommended.percent}% du chapitre maîtrisé. Encore quelques exercices pour faire monter la jauge.</p>
          </div>
          <Link className="secondary" to={`/chapitre/${data.recommended.chapter_id}#exercices`}>Reprendre <ArrowRight size={17} /></Link>
        </section>
      )}

      <section>
        <div className="section-head">
          <div>
            <span className="eyebrow">PAR CHAPITRE</span>
            <h2>Ta progression</h2>
            <p>La maîtrise correspond aux exercices réussis au moins une fois.</p>
          </div>
          <Link to="/exercices">Voir tous les exercices</Link>
        </div>
        <div className="progress-list progress-list-v7">
          {data.chapters.length ? data.chapters.map((chapter) => (
            <Link to={`/chapitre/${chapter.chapter_id}`} className="progress-row" key={chapter.chapter_id}>
              <div className="progress-main">
                <span className="subject-pill">{chapter.emoji} {chapter.subject}</span>
                <strong>{chapter.title}</strong>
                <small>{chapter.correct}/{chapter.total} exercices maîtrisés</small>
              </div>
              <div className="progress-side">
                <b>{chapter.percent}%</b>
                <div className="bar"><span style={{ width: `${chapter.percent}%` }} /></div>
              </div>
            </Link>
          )) : <div className="empty">Aucun chapitre disponible pour ce niveau.</div>}
        </div>
      </section>
    </>
  );
}
