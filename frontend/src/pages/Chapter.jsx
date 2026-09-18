import React, { useEffect, useState } from 'react';
import { ArrowLeft, ArrowRight, BookOpenCheck, Dumbbell, ScrollText } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../api';
import { getSubjectMeta } from '../subjectMeta';

export default function Chapter() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    api(`/chapters/${id}`).then(setData);
  }, [id]);

  useEffect(() => {
    if (!data) return;
    if (window.location.hash === '#exercices') {
      setTimeout(() => document.getElementById('exercise-zone')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
    }
  }, [data]);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  const meta = getSubjectMeta(data.subject.slug);
  const Icon = meta.icon;

  return (
    <>
      <Link className="back" to="/cours"><ArrowLeft size={17} /> Tous les cours</Link>

      <header className="chapter-hero">
        <span className="subject-pill">{data.subject.emoji} {data.subject.name} • {data.level}</span>
        <div className="chapter-hero-row">
          <div>
            <h1>{data.title}</h1>
            <p>{data.summary}</p>
          </div>
          <div className={`hero-icon ${meta.accent}`}><Icon size={32} /></div>
        </div>

        <div className="hero-progress">
          <div><b>{data.progress.percent}%</b><span> maîtrisé</span></div>
          <div className="bar"><span style={{ width: `${data.progress.percent}%` }} /></div>
        </div>

        <div className="mode-switch">
          <a href="#course-zone" className="mode-card course">
            <ScrollText size={18} />
            <div>
              <strong>Partie cours</strong>
              <span>Lire les rappels et les méthodes</span>
            </div>
          </a>
          <a href="#exercise-zone" className="mode-card practice">
            <Dumbbell size={18} />
            <div>
              <strong>Partie exercices</strong>
              <span>S'entraîner avec correction</span>
            </div>
          </a>
        </div>
      </header>

      <div className="chapter-layout">
        <section id="course-zone" className="panel course-panel">
          <div className="section-head">
            <div>
              <h2><BookOpenCheck size={21} /> Le cours</h2>
              <p>Lis l'essentiel avant de t'entraîner.</p>
            </div>
          </div>
          <div className="lesson-list">
            {data.lessons.map((lesson) => (
              <article className="lesson-card" key={lesson.id}>
                <div className="lesson-tag">Fiche cours</div>
                <h3>{lesson.title}</h3>
                {lesson.body.split('\n').map((paragraph, index) => <p key={index}>{paragraph}</p>)}
              </article>
            ))}
          </div>
        </section>

        <section id="exercise-zone" className="panel practice-panel">
          <div className="section-head">
            <div>
              <h2><Dumbbell size={21} /> Exercices</h2>
              <p>Commence simplement puis monte en difficulté.</p>
            </div>
          </div>
          <div className="exercise-list">
            {data.exercises.map((exercise, index) => (
              <Link className="exercise-item" to={`/exercice/${exercise.id}`} key={exercise.id}>
                <span className="exercise-number">{index + 1}</span>
                <div>
                  <strong>{exercise.title}</strong>
                  <small>{'●'.repeat(exercise.difficulty)}{'○'.repeat(3 - exercise.difficulty)} • {exercise.points} pts</small>
                </div>
                <ArrowRight size={18} />
              </Link>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
