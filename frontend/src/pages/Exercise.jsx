import React, { useEffect, useState } from 'react';
import { ArrowLeft, CheckCircle2, RotateCcw, Sparkles, XCircle } from 'lucide-react';
import { Link, useLocation, useParams } from 'react-router-dom';
import { api } from '../api';

export default function Exercise() {
  const { id } = useParams();
  const location = useLocation();
  const fromSession = new URLSearchParams(location.search).get('from') === 'seance';
  const [data, setData] = useState(null);
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api(`/exercises/${id}`).then(setData);
    setAnswer('');
    setResult(null);
  }, [id]);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  const submit = async (e) => {
    e.preventDefault();
    if (!answer.trim()) return;
    setBusy(true);
    try {
      setResult(await api(`/exercises/${id}/answer`, { method: 'POST', body: JSON.stringify({ answer }) }));
    } finally {
      setBusy(false);
    }
  };

  const retry = () => {
    setAnswer('');
    setResult(null);
  };

  return (
    <div className="exercise-page">
      <Link className="back" to={fromSession ? '/seance' : `/chapitre/${data.chapter_id}#exercices`}>
        <ArrowLeft size={17} /> {fromSession ? 'Retour à la séance du jour' : 'Retour au chapitre'}
      </Link>
      <div className="exercise-shell">
        {fromSession && <div className="session-context"><Sparkles size={15} /> Exercice de ta séance du jour</div>}
        <div className="exercise-meta">
          <span>DIFFICULTÉ {'●'.repeat(data.difficulty)}{'○'.repeat(3 - data.difficulty)}</span>
          <span>{data.points} POINTS</span>
        </div>
        <h1>{data.title}</h1>
        <p className="statement">{data.statement}</p>
        <form onSubmit={submit}>
          {data.exercise_type === 'mcq' ? (
            <div className="options">
              {data.options.map((option) => (
                <label className={`option ${answer === option ? 'selected' : ''}`} key={option}>
                  <input type="radio" name="answer" value={option} checked={answer === option} onChange={() => setAnswer(option)} />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          ) : (
            <label className="answer-label">Ta réponse
              <input className="big-input" value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Entre ta réponse…" />
            </label>
          )}
          {!result && <button className="primary answer-button" disabled={busy || !answer.trim()}>{busy ? 'Vérification…' : 'Valider ma réponse'}</button>}
        </form>

        {result && (
          <div className={`correction ${result.is_correct ? 'correct' : 'wrong'}`}>
            <div className="correction-title">
              {result.is_correct ? <><CheckCircle2 /> Bonne réponse !</> : <><XCircle /> Pas encore.</>}
            </div>
            {!result.is_correct && <p><b>Réponse attendue :</b> {result.correct_answer}</p>}
            <p>{result.correction}</p>
            <div className="correction-actions">
              <button className="secondary" onClick={retry}><RotateCcw size={16} /> Refaire l'exercice</button>
              {fromSession && <Link className="primary" to="/seance">Continuer ma séance</Link>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
