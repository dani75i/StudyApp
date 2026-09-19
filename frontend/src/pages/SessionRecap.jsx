import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, CheckCircle2, RotateCcw, Sparkles, Target } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../api';

export default function SessionRecap() {
  const [session, setSession] = useState(null);
  useEffect(() => { api('/daily-session').then(setSession); }, []);
  const stats = useMemo(() => {
    if (!session) return null;
    const review = session.exercises.filter((exercise) => exercise.completed && !exercise.correct);
    const remaining = session.exercises.filter((exercise) => !exercise.completed);
    return { review, remaining, correct: session.exercises.filter((exercise) => exercise.correct).length };
  }, [session]);
  if (!session) return <div className="loader-page"><div className="loader" /></div>;
  return <div className="exercise-page v9-recap">
    <div className="v9-recap-hero"><Sparkles size={32} /><span>BILAN DE TA SÉANCE</span><h1>{session.completed === session.total ? 'Séance terminée 🎉' : 'Ta séance en cours'}</h1><p>{session.completed} exercice{session.completed > 1 ? 's' : ''} effectué{session.completed > 1 ? 's' : ''} sur {session.total}</p></div>
    <div className="v9-recap-kpis"><div><CheckCircle2 /><b>{stats.correct}</b><span>réussis</span></div><div><RotateCcw /><b>{stats.review.length}</b><span>à revoir</span></div><div><Target /><b>{stats.remaining.length}</b><span>restants</span></div></div>
    <div className="v9-recap-progress"><strong>{session.percent}% de la séance effectuée</strong><div className="bar"><span style={{width:`${session.percent}%`}}/></div></div>
    {stats.review.length > 0 && <section className="v9-correction-card"><h2>À retravailler</h2><p>Tu peux refaire ces exercices pour consolider tes acquis.</p><div className="v9-recap-list">{stats.review.map(exercise => <Link key={exercise.id} to={`/exercice/${exercise.id}?from=seance`}><RotateCcw size={17}/>{exercise.title}<ArrowRight size={16}/></Link>)}</div></section>}
    <div className="v9-correction-actions"><Link className="secondary" to="/dashboard">Mon tableau de bord</Link><Link className="primary" to="/seance">{stats.remaining.length ? 'Continuer la séance' : 'Revoir ma séance'} <ArrowRight size={17}/></Link></div>
  </div>;
}
