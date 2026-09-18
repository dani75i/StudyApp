import React, { useEffect, useState } from 'react';
import {
  ArrowRight,
  BookOpenText,
  CheckCircle2,
  Dumbbell,
  Flame,
  Medal,
  Sparkles,
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
};

function Stat({ icon: Icon, label, value, sub }) {
  return <div className="stat-card"><div className="stat-icon"><Icon size={21} /></div><div><span>{label}</span><strong>{value}</strong><small>{sub}</small></div></div>;
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [goalBusy, setGoalBusy] = useState(false);

  const load = () => api('/dashboard').then(setData);
  useEffect(() => { load(); }, []);

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

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">TABLEAU DE BORD</span>
          <h1>Bonjour {data.first_name} 👋</h1>
          <p>Voici où tu en es dans ta progression en {data.level}, uniquement en maths et en physique.</p>
        </div>
        <div className="header-actions">
          <Link className="secondary compact-button" to="/cours">Voir les cours <BookOpenText size={17} /></Link>
          <Link className="primary compact" to="/seance">Séance du jour <Sparkles size={17} /></Link>
        </div>
      </header>

      <div className="stats-grid">
        <Stat icon={CheckCircle2} label="Exercices réussis" value={data.stats.correct} sub={`${data.stats.completed} tentés`} />
        <Stat icon={Target} label="Taux de réussite" value={`${data.stats.success_rate}%`} sub="sur les exercices tentés" />
        <Stat icon={Flame} label="Série actuelle" value={`${data.stats.streak} j`} sub="jours d'entraînement" />
        <Stat icon={Trophy} label="Disponibles" value={data.stats.available} sub={`pour le niveau ${data.level}`} />
      </div>

      <div className="dashboard-two-col">
        <section className="weekly-card">
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
            <span>Choisir mon objectif :</span>
            {[10, 20, 30, 40].map((value) => (
              <button
                key={value}
                disabled={goalBusy}
                className={data.weekly.target === value ? 'active' : ''}
                onClick={() => changeGoal(value)}
              >
                {value}
              </button>
            ))}
          </div>
        </section>

        <section className="daily-cta-card">
          <div className="daily-cta-icon"><Sparkles size={24} /></div>
          <div>
            <span className="eyebrow">ROUTINE</span>
            <h2>Ta séance du jour est prête</h2>
            <p>Une petite sélection d'exercices qui privilégie ce qu'il reste à maîtriser.</p>
          </div>
          <Link className="primary" to="/seance">Commencer <ArrowRight size={17} /></Link>
        </section>
      </div>

      <div className="quick-grid">
        <Link className="quick-card" to="/cours">
          <div className="quick-icon"><BookOpenText size={20} /></div>
          <div><strong>Réviser un cours</strong><p>Consulte une fiche claire avant de t'entraîner.</p></div>
          <ArrowRight size={16} />
        </Link>
        <Link className="quick-card" to="/exercices">
          <div className="quick-icon"><Dumbbell size={20} /></div>
          <div><strong>Choisir mes exercices</strong><p>Filtre par matière, chapitre, difficulté ou progression.</p></div>
          <ArrowRight size={16} />
        </Link>
      </div>

      {data.recommended && (
        <section className="focus-card">
          <div>
            <span className="eyebrow">À TRAVAILLER MAINTENANT</span>
            <h2>{data.recommended.emoji} {data.recommended.title}</h2>
            <p>{data.recommended.percent}% du chapitre maîtrisé. Continue pour renforcer cette compétence.</p>
          </div>
          <Link className="secondary" to={`/chapitre/${data.recommended.chapter_id}#exercices`}>Reprendre <ArrowRight size={17} /></Link>
        </section>
      )}

      <section>
        <div className="section-head">
          <div>
            <h2><Medal size={21} /> Badges</h2>
            <p>Des petits objectifs pour rendre ta progression visible.</p>
          </div>
        </div>
        <div className="badge-cards">
          {data.badges.map((badge) => {
            const Icon = badgeIcons[badge.icon] || Medal;
            const percent = Math.min(100, Math.round((badge.progress / badge.target) * 100));
            return (
              <article className={`badge-card ${badge.unlocked ? 'unlocked' : ''}`} key={badge.id}>
                <div className="badge-icon"><Icon size={22} /></div>
                <div className="badge-copy">
                  <strong>{badge.title}</strong>
                  <p>{badge.description}</p>
                  <div className="badge-progress"><span>{badge.progress}/{badge.target}</span><div className="bar"><span style={{ width: `${percent}%` }} /></div></div>
                </div>
                {badge.unlocked && <span className="unlocked-label">Débloqué</span>}
              </article>
            );
          })}
        </div>
      </section>

      <section>
        <div className="section-head">
          <div>
            <h2>Progression par chapitre</h2>
            <p>La maîtrise correspond aux exercices réussis au moins une fois.</p>
          </div>
          <Link to="/exercices">Voir tous les exercices</Link>
        </div>
        <div className="progress-list">
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
          )) : <div className="empty">Aucun chapitre disponible pour ce niveau dans la démo.</div>}
        </div>
      </section>
    </>
  );
}
