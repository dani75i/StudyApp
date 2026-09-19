import React, { useEffect, useState } from 'react';
import { ArrowLeft, ArrowRight, ChevronDown, Lightbulb, Sparkles } from 'lucide-react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';
import { RichText } from '../components/RichContent';
import GeometryDiagram from '../components/GeometryDiagram';

export default function Exercise() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const fromSession = new URLSearchParams(location.search).get('from') === 'seance';
  const sessionQuery = fromSession ? '?from=seance' : '';
  const [data, setData] = useState(null);
  const [session, setSession] = useState(null);
  const [answer, setAnswer] = useState('');
  const [hintsShown, setHintsShown] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    setData(null); setSession(null); setAnswer(''); setHintsShown(0); setError('');
    api(`/exercises/${id}`).then((response) => { if (active) setData(response); }).catch((err) => { if (active) setError(err.message); });
    if (fromSession) api('/daily-session').then((response) => { if (active) setSession(response); }).catch(() => {});
    return () => { active = false; };
  }, [id, fromSession]);

  if (!data && !error) return <div className="loader-page"><div className="loader" /></div>;
  if (!data) return <div className="alert error">{error}</div>;

  const sessionIndex = session?.exercises.findIndex((exercise) => exercise.id === data.id);
  const ordinal = fromSession && sessionIndex >= 0 ? sessionIndex + 1 : data.sequence_number;
  const total = fromSession && session?.total ? session.total : data.sequence_total;
  const progress = Math.round(((ordinal - 1) / Math.max(1, total)) * 100);
  const submit = async (event) => {
    event.preventDefault();
    if (!answer.trim() || busy) return;
    setBusy(true); setError('');
    try {
      await api(`/exercises/${id}/answer`, { method: 'POST', body: JSON.stringify({ answer }) });
      navigate(`/exercice/${id}/correction${sessionQuery}`);
    } catch (err) { setError(err.message); } finally { setBusy(false); }
  };

  return (
    <div className="exercise-page v9-workspace">
      <Link className="back" to={fromSession ? '/seance' : `/chapitre/${data.chapter_id}#exercices`}>
        <ArrowLeft size={17} /> {fromSession ? 'Retour à la séance' : 'Retour au chapitre'}
      </Link>
      <div className="v9-run-progress" aria-label={`Exercice ${ordinal} sur ${total}`}>
        <div><strong>Exercice {ordinal} / {total}</strong><span>{fromSession ? 'Séance du jour' : 'Progression dans le chapitre'}</span></div>
        <div className="bar"><span style={{ width: `${progress}%` }} /></div>
      </div>
      <div className="exercise-shell">
        {fromSession && <div className="session-context"><Sparkles size={15} /> Ta séance du jour</div>}
        <div className="exercise-meta"><span>{['Facile', 'Intermédiaire', 'Difficile'][data.difficulty - 1]}</span><span>{data.points} POINTS</span></div>
        <h1>Exercice {ordinal}</h1>
        <p className="exercise-detail-topic">{data.title.replace(/^Exercice \d+\s*[—·-]\s*/, '')}</p>
        <div className="v9-statement"><RichText text={data.statement} /><GeometryDiagram diagram={data.diagram} /></div>

        <form onSubmit={submit}>
          {data.exercise_type === 'mcq' ? (
            <fieldset className="v9-fieldset"><legend>Choisis une réponse</legend>
              <div className="options">
                {data.options.map((option, index) => (
                  <label className={`option ${answer === option ? 'selected' : ''}`} key={`${index}-${option}`}>
                    <input type="radio" name="answer" value={option} checked={answer === option} onChange={() => setAnswer(option)} />
                    <span><RichText text={option} /></span>
                  </label>
                ))}
              </div>
            </fieldset>
          ) : (
            <label className="answer-label">Ta réponse
              <input className="big-input" value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Entre la valeur demandée…" autoComplete="off" />
            </label>
          )}

          <div className="v9-hint-panel">
            <div className="v9-hint-header"><Lightbulb size={18} /><strong>Besoin d’un coup de pouce ?</strong><span>{hintsShown}/{data.hints?.length || 0} indices</span></div>
            {(data.hints || []).slice(0, hintsShown).map((hint, index) => (
              <p key={index} className="v9-hint"><b>Indice {index + 1}.</b> <RichText text={hint} /></p>
            ))}
            {hintsShown < (data.hints?.length || 0) && (
              <button type="button" className="v9-hint-reveal" onClick={() => setHintsShown((count) => count + 1)}>
                {hintsShown ? 'Afficher le deuxième indice' : 'Afficher un indice'} <ChevronDown size={15} />
              </button>
            )}
          </div>
          {error && <div className="alert error" role="alert">{error}</div>}
          <button className="primary answer-button v9-submit" disabled={busy || !answer.trim()}>
            {busy ? 'Vérification…' : <>Valider et voir ma correction <ArrowRight size={18} /></>}
          </button>
        </form>
      </div>
    </div>
  );
}
