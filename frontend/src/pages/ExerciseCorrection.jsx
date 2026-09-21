import React, { useEffect, useState } from 'react';
import { ArrowLeft, ArrowRight, BookOpenCheck, CheckCircle2, RotateCcw, Sparkles, XCircle } from 'lucide-react';
import { Link, useLocation, useParams } from 'react-router-dom';
import { api } from '../api';
import { RichText } from '../components/RichContent';
import { correctionToSteps } from '../correctionSteps';
import GeometryDiagram from '../components/GeometryDiagram';

export default function ExerciseCorrection() {
  const { id } = useParams();
  const location = useLocation();
  const fromSession = new URLSearchParams(location.search).get('from') === 'seance';
  const [detail, setDetail] = useState(null);
  const [correction, setCorrection] = useState(null);
  const [session, setSession] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    setDetail(null); setCorrection(null); setSession(null); setError('');
    Promise.all([api(`/exercises/${id}`), api(`/exercises/${id}/latest-correction`)]).then(([d, c]) => {
      if (active) { setDetail(d); setCorrection(c); }
    }).catch((err) => { if (active) setError(err.message); });
    if (fromSession) api('/daily-session').then((s) => { if (active) setSession(s); }).catch(() => {});
    return () => { active = false; };
  }, [id, fromSession]);

  if (error) return <div className="exercise-page"><div className="alert error">{error}</div><Link className="primary" to={`/exercice/${id}${fromSession ? '?from=seance' : ''}`}>Faire l’exercice</Link></div>;
  if (!detail || !correction || (fromSession && !session)) return <div className="loader-page"><div className="loader" /></div>;

  const sessionIndex = session?.exercises.findIndex((exercise) => exercise.id === Number(id)) ?? -1;
  const ordinal = fromSession && sessionIndex >= 0 ? sessionIndex + 1 : detail.sequence_number;
  const total = fromSession ? session.total : detail.sequence_total;
  const upcoming = fromSession
    ? session.exercises.find((exercise) => !exercise.completed && exercise.id !== detail.id)?.id
    : detail.next_exercise_id;
  const onward = upcoming ? `/exercice/${upcoming}${fromSession ? '?from=seance' : ''}` : fromSession ? '/seance/bilan' : `/chapitre/${detail.chapter_id}#exercices`;
  const onwardLabel = upcoming ? 'Exercice suivant' : fromSession ? 'Voir mon bilan' : 'Retour au chapitre';
  const solutionSteps = correctionToSteps(correction.steps, correction.correction);

  return (
    <div className="exercise-page v9-correction-page">
      <Link className="back" to={fromSession ? '/seance' : `/chapitre/${detail.chapter_id}#exercices`}><ArrowLeft size={17} /> {fromSession ? 'Séance du jour' : 'Retour au chapitre'}</Link>
      <div className={`v9-result-hero ${correction.is_correct ? 'correct' : 'review'}`}>
        <span>{correction.is_correct ? <CheckCircle2 size={26} /> : <XCircle size={26} />}</span>
        <div><small>EXERCICE {ordinal} / {total} · TENTATIVE {correction.attempt_number}</small><h1>{correction.is_correct ? 'Bravo, c’est juste !' : 'On reprend ensemble'}</h1><p>{correction.is_correct ? 'Tu as trouvé la bonne réponse. Découvre la méthode pour la retenir.' : 'Ce n’est pas encore la bonne réponse. La résolution détaillée t’aide à comprendre.'}</p></div>
      </div>

      <section className="v9-correction-card"><h2>Rappel de l’énoncé</h2><div className="v9-statement"><RichText text={detail.statement} /><GeometryDiagram diagram={detail.diagram} /></div></section>
      <div className="v9-answers">
        <section className="v9-answer-card"><small>TA RÉPONSE</small><div><RichText text={correction.user_answer} /></div></section>
        <section className="v9-answer-card expected"><small>RÉPONSE ATTENDUE</small><div><RichText text={correction.correct_answer} /></div></section>
      </div>

      <section className="v9-correction-card">
        <h2><BookOpenCheck size={21} /> Correction pas à pas</h2>
        <ol className="v9-solution-steps">
          {solutionSteps.map((step, index) => (
            <li key={index}>
              <span aria-label={`Étape ${index + 1}`}>{index + 1}</span>
              <div className="v106-step-content"><RichText text={step} /></div>
            </li>
          ))}
        </ol>
      </section>
      {correction.method && <aside className="v9-method"><Sparkles size={21} /><div><strong>Méthode à retenir</strong><p><RichText text={correction.method} /></p></div></aside>}
      <div className="v9-correction-actions">
        <Link className="secondary" to={`/exercice/${id}${fromSession ? '?from=seance' : ''}`}><RotateCcw size={17} /> Refaire</Link>
        <Link className="primary" to={onward}>{onwardLabel} <ArrowRight size={17} /></Link>
      </div>
    </div>
  );
}
