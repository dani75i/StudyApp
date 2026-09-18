import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, CheckCircle2, Circle, Clock3, RotateCcw, Sparkles, Target } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../api';
import { getSubjectMeta } from '../subjectMeta';

export default function DailySession() {
  const [data, setData] = useState(null);

  const load = () => api('/daily-session').then(setData);
  useEffect(() => { load(); }, []);

  const next = useMemo(() => data?.exercises?.find((exercise) => !exercise.completed), [data]);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">ROUTINE DU JOUR</span>
          <h1>Séance du jour</h1>
          <p>Une sélection courte et stable pour avancer sans te demander quoi travailler.</p>
        </div>
        <button className="secondary compact-button" onClick={load}><RotateCcw size={16} /> Actualiser</button>
      </header>

      <section className="daily-hero">
        <div className="daily-hero-main">
          <div className="daily-symbol"><Sparkles size={25} /></div>
          <div>
            <span className="eyebrow">OBJECTIF DU JOUR</span>
            <h2>{data.total ? `${data.total} exercices ciblés` : 'Aucun exercice disponible'}</h2>
            <p><Clock3 size={15} /> Environ {data.estimated_minutes || 0} minutes • {data.correct} réussite{data.correct > 1 ? 's' : ''}</p>
          </div>
        </div>
        <div className="daily-score">
          <strong>{data.percent}%</strong>
          <span>{data.completed}/{data.total} terminés</span>
        </div>
        <div className="bar daily-bar"><span style={{ width: `${data.percent}%` }} /></div>
        {next ? (
          <Link className="primary" to={`/exercice/${next.id}?from=seance`}>Continuer la séance <ArrowRight size={17} /></Link>
        ) : data.total > 0 ? (
          <div className="daily-done"><CheckCircle2 size={20} /> Séance terminée. Beau travail !</div>
        ) : null}
      </section>

      <section>
        <div className="section-head">
          <div>
            <h2><Target size={21} /> Programme</h2>
            <p>Les exercices non maîtrisés sont privilégiés d'un jour à l'autre.</p>
          </div>
        </div>

        <div className="session-list">
          {data.exercises.map((exercise) => {
            const meta = getSubjectMeta(exercise.subject.slug);
            const Icon = meta.icon;
            return (
              <Link className={`session-item ${exercise.completed ? 'done' : ''}`} to={`/exercice/${exercise.id}?from=seance`} key={exercise.id}>
                <div className={`session-status ${exercise.completed ? (exercise.correct ? 'correct' : 'attempted') : ''}`}>
                  {exercise.completed ? <CheckCircle2 size={20} /> : <Circle size={20} />}
                </div>
                <div className={`subject-logo mini ${meta.accent}`}><Icon size={18} /></div>
                <div className="session-copy">
                  <div className="session-topline">
                    <span>Exercice {exercise.order}</span>
                    <small>{'●'.repeat(exercise.difficulty)}{'○'.repeat(3 - exercise.difficulty)}</small>
                  </div>
                  <strong>{exercise.title}</strong>
                  <p>{exercise.subject.name} • {exercise.chapter.title}</p>
                </div>
                <ArrowRight size={18} />
              </Link>
            );
          })}
        </div>
      </section>
    </>
  );
}
