import React, { useEffect, useMemo, useState } from 'react';
import {
  Crown,
  Flame,
  LockKeyhole,
  Medal,
  Rocket,
  Sparkles,
  Star,
  Target,
  Trophy,
} from 'lucide-react';
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

const badgeTones = ['violet', 'gold', 'cyan', 'rose', 'emerald', 'amber', 'blue', 'orange', 'teal'];

export default function Rewards() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api('/dashboard').then(setData);
  }, []);

  const stats = useMemo(() => {
    if (!data) return { unlocked: 0, total: 0, percent: 0 };
    const unlocked = data.badges.filter((badge) => badge.unlocked).length;
    const total = data.badges.length;
    return { unlocked, total, percent: total ? Math.round((unlocked / total) * 100) : 0 };
  }, [data]);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  return (
    <>
      <header className="rewards-hero">
        <div className="rewards-hero-copy">
          <span className="eyebrow">RÉCOMPENSES</span>
          <h1>Ta collection de badges</h1>
          <p>Chaque badge marque une étape importante de ta progression. Continue à t'entraîner pour compléter la collection.</p>
          <div className="rewards-summary-pills">
            <span><Trophy size={16} /> {stats.unlocked} débloqués</span>
            <span><LockKeyhole size={16} /> {stats.total - stats.unlocked} à conquérir</span>
          </div>
        </div>

        <div className="rewards-progress-orb" style={{ '--reward-progress': `${stats.percent * 3.6}deg` }}>
          <div>
            <strong>{stats.percent}%</strong>
            <span>collection</span>
          </div>
        </div>
      </header>

      <section className="rewards-grid">
        {data.badges.map((badge, index) => {
          const Icon = badgeIcons[badge.icon] || Medal;
          const percent = Math.min(100, Math.round((badge.progress / badge.target) * 100));
          const tone = badgeTones[index % badgeTones.length];
          return (
            <article className={`reward-card ${badge.unlocked ? 'unlocked' : 'locked'} tone-${tone}`} key={badge.id}>
              <div className="reward-card-glow" />
              <div className="reward-medallion"><Icon size={28} /></div>
              <div className="reward-state">
                {badge.unlocked ? <><Sparkles size={14} /> Débloqué</> : <><LockKeyhole size={14} /> En progression</>}
              </div>
              <h2>{badge.title}</h2>
              <p>{badge.description}</p>
              <div className="reward-progress-row">
                <span>{badge.progress}/{badge.target}</span>
                <b>{percent}%</b>
              </div>
              <div className="reward-progress-track"><span style={{ width: `${percent}%` }} /></div>
            </article>
          );
        })}
      </section>
    </>
  );
}
