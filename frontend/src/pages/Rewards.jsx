import React, { useEffect, useMemo, useState } from 'react';
import { Crown, Flame, LockKeyhole, Medal, Rocket, Sparkles, Star, Target, Trophy, CheckCircle2 } from 'lucide-react';
import { api } from '../api';

const badgeIcons = { sparkles: Sparkles, medal: Medal, trophy: Trophy, flame: Flame, target: Target, star: Star, rocket: Rocket, crown: Crown };
const tones = ['violet', 'gold', 'cyan', 'rose', 'emerald', 'amber', 'blue', 'orange', 'teal'];

function BadgeCard({ badge, index }) {
  const Icon = badgeIcons[badge.icon] || Medal;
  const target = Math.max(1, Number(badge.target) || 1);
  const progress = Math.min(target, Math.max(0, Number(badge.progress) || 0));
  const percentage = Math.round(progress / target * 100);
  return (
    <article className={`reward-card v10-reward ${badge.unlocked ? 'unlocked' : 'locked'} tone-${tones[index % tones.length]}`}>
      <div className="reward-card-glow" aria-hidden="true" />
      <div className="v10-reward-top">
        <div className="reward-medallion"><Icon size={badge.unlocked ? 31 : 25} strokeWidth={badge.unlocked ? 2.2 : 1.8} /></div>
        <div className={`v10-reward-state ${badge.unlocked ? 'earned' : 'waiting'}`}>
          {badge.unlocked ? <><CheckCircle2 size={13}/> DÉBLOQUÉ</> : <><LockKeyhole size={13}/> À OBTENIR</>}
        </div>
      </div>
      <h3>{badge.title}</h3>
      <p>{badge.description}</p>
      {!badge.unlocked && (
        <div className="v10-reward-progress">
          <div className="reward-progress-row"><span>Progression</span><strong>{progress} / {target}</strong></div>
          <div className="reward-progress-track" role="progressbar" aria-label={`Progression : ${badge.title}`} aria-valuenow={progress} aria-valuemin="0" aria-valuemax={target}><span style={{ width: `${percentage}%` }} /></div>
        </div>
      )}
      {badge.unlocked && <div className="v10-reward-earned"><Sparkles size={15}/> Trophée dans ta collection</div>}
    </article>
  );
}

export default function Rewards() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  useEffect(() => { api('/dashboard').then(setData).catch((err) => setError(err.message)); }, []);
  const groups = useMemo(() => {
    const badges = data?.badges || [];
    const unlocked = badges.filter((badge) => badge.unlocked);
    const locked = badges.filter((badge) => !badge.unlocked).sort((a,b) => (b.progress / Math.max(1,b.target)) - (a.progress / Math.max(1,a.target)));
    return { unlocked, locked, total: badges.length, percent: badges.length ? Math.round(unlocked.length / badges.length * 100) : 0 };
  }, [data]);
  if (error) return <div className="alert error" role="alert">Impossible de charger les récompenses : {error}</div>;
  if (!data) return <div className="loader-page"><div className="loader" /></div>;
  return (
    <div className="v10-rewards-page">
      <header className="rewards-hero">
        <div className="rewards-hero-copy">
          <span className="eyebrow">TA COLLECTION</span><h1>Mes récompenses <Trophy size={29} aria-hidden="true" /></h1>
          <p>Les trophées remportés brillent en couleur. Les autres indiquent exactement ce qu’il reste à accomplir.</p>
          <div className="rewards-summary-pills"><span><Trophy size={16}/> {groups.unlocked.length} débloquées</span><span><LockKeyhole size={16}/> {groups.locked.length} à obtenir</span></div>
        </div>
        <div className="rewards-progress-orb" style={{ '--reward-progress': `${groups.percent * 3.6}deg` }}><div><strong>{groups.percent}%</strong><span>collection</span></div></div>
      </header>
      <section className="v10-reward-section" aria-labelledby="v10-unlocked-title">
        <div className="v10-reward-section-head"><span className="v10-section-icon earned"><Trophy size={20}/></span><div><h2 id="v10-unlocked-title">Mes trophées débloqués <span>{groups.unlocked.length}</span></h2><p>Bravo pour ces étapes franchies !</p></div></div>
        {groups.unlocked.length ? <div className="rewards-grid">{groups.unlocked.map((badge,index) => <BadgeCard badge={badge} index={index} key={badge.id}/>)}</div> : <div className="v10-no-rewards">Ton premier trophée apparaîtra ici dès que tu auras terminé un exercice. 🚀</div>}
      </section>
      <section className="v10-reward-section" aria-labelledby="v10-locked-title">
        <div className="v10-reward-section-head"><span className="v10-section-icon waiting"><LockKeyhole size={20}/></span><div><h2 id="v10-locked-title">À débloquer <span>{groups.locked.length}</span></h2><p>Les objectifs les plus proches sont affichés en premier.</p></div></div>
        {groups.locked.length ? <div className="rewards-grid">{groups.locked.map((badge,index) => <BadgeCard badge={badge} index={index} key={badge.id}/>)}</div> : <div className="v10-no-rewards">Collection complète ! Tous les trophées sont débloqués. 🏆</div>}
      </section>
    </div>
  );
}
