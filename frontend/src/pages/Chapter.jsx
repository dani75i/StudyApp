import React, { useEffect, useMemo, useState } from 'react';
import {
  ArrowLeft,
  ArrowRight,
  BookOpenCheck,
  CheckCircle2,
  CircleDashed,
  Dumbbell,
  Gauge,
  RotateCcw,
  ScrollText,
  Sparkles,
} from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../api';
import { getSubjectMeta } from '../subjectMeta';
import { getChapterIllustration } from '../chapterIllustrations';
import { LessonContent } from '../components/RichContent';

const FILTERS = [
  ['all', 'Tous'],
  ['todo', 'À faire'],
  ['review', 'À revoir'],
  ['success', 'Réussis'],
];

const difficultyLabel = {
  1: 'Facile',
  2: 'Intermédiaire',
  3: 'Difficile',
};

function StatusIcon({ status, size = 16 }) {
  if (status === 'success') return <CheckCircle2 size={size} />;
  if (status === 'review') return <RotateCcw size={size} />;
  return <CircleDashed size={size} />;
}

function statusLabel(status) {
  if (status === 'success') return 'Réussi';
  if (status === 'review') return 'À revoir';
  return 'À faire';
}

export default function Chapter() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    api(`/chapters/${id}`).then(setData);
  }, [id]);

  useEffect(() => {
    if (!data) return;
    if (window.location.hash === '#exercices') {
      setTimeout(() => document.getElementById('exercise-zone')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
    }
  }, [data]);

  const summary = useMemo(() => {
    if (!data) return { success: 0, review: 0, todo: 0, total: 0 };
    return data.exercises.reduce((acc, exercise) => {
      acc[exercise.status] += 1;
      acc.total += 1;
      return acc;
    }, { success: 0, review: 0, todo: 0, total: 0 });
  }, [data]);

  const numberedExercises = useMemo(() => {
    if (!data) return [];
    return data.exercises.map((exercise, index) => ({ ...exercise, originalIndex: index + 1 }));
  }, [data]);

  const filteredExercises = useMemo(() => (
    filter === 'all' ? numberedExercises : numberedExercises.filter((exercise) => exercise.status === filter)
  ), [filter, numberedExercises]);

  const continueExercise = useMemo(() => {
    if (!data?.exercises?.length) return null;
    return data.exercises.find((exercise) => exercise.status === 'review')
      || data.exercises.find((exercise) => exercise.status === 'todo')
      || data.exercises[0];
  }, [data]);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  const continueActionLabel = summary.review ? 'Revoir' : summary.todo ? 'Continuer' : 'Recommencer';
  const meta = getSubjectMeta(data.subject.slug);
  const Icon = meta.icon;
  const illustration = getChapterIllustration({ subjectSlug: data.subject.slug, title: data.title });

  return (
    <>
      <Link className="back" to="/cours"><ArrowLeft size={17} /> Tous les cours</Link>

      <header className="chapter-hero">
        <span className="subject-pill">{data.subject.emoji} {data.subject.name} • {data.level}</span>
        <div className={`chapter-hero-split ${illustration ? 'with-visual' : ''}`}>
          <div>
            <div className="chapter-hero-row">
              <div>
                <h1>{data.title}</h1>
                <p>{data.summary}</p>
              </div>
              {!illustration && <div className={`hero-icon ${meta.accent}`}><Icon size={32} /></div>}
            </div>
          </div>

          {illustration && (
            <div className="chapter-hero-visual chapter-hero-visual-large">
              <img src={illustration} alt={`Illustration du chapitre ${data.title}`} />
            </div>
          )}
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
                <LessonContent body={lesson.body} />
              </article>
            ))}
          </div>
        </section>

        <section id="exercise-zone" className="panel practice-panel">
          <div className="exercise-panel-head">
            <div className="section-head chapter-exercise-heading">
              <div>
                <h2><Dumbbell size={21} /> Exercices</h2>
                <p>Vois immédiatement ce qui est fait, réussi ou à retravailler.</p>
              </div>
            </div>

            <div className="chapter-exercise-summary">
              <div className="summary-stat success">
                <CheckCircle2 size={18} />
                <div><strong>{summary.success}</strong><span>réussis</span></div>
              </div>
              <div className="summary-stat review">
                <RotateCcw size={18} />
                <div><strong>{summary.review}</strong><span>à revoir</span></div>
              </div>
              <div className="summary-stat todo">
                <CircleDashed size={18} />
                <div><strong>{summary.todo}</strong><span>à faire</span></div>
              </div>
            </div>

            {continueExercise && (
              <Link className="chapter-continue-card" to={`/exercice/${continueExercise.id}`}>
                <div className="continue-icon"><Sparkles size={19} /></div>
                <div>
                  <small>{summary.review ? 'Priorité : à retravailler' : summary.todo ? 'Prochain exercice' : 'Chapitre terminé'}</small>
                  <strong>{continueExercise.title}</strong>
                </div>
                <span>{continueActionLabel} <ArrowRight size={16} /></span>
              </Link>
            )}

            <div className="exercise-filter-tabs" role="tablist" aria-label="Filtrer les exercices">
              {FILTERS.map(([value, label]) => {
                const count = value === 'all' ? summary.total : summary[value];
                return (
                  <button
                    key={value}
                    type="button"
                    className={filter === value ? 'active' : ''}
                    onClick={() => setFilter(value)}
                  >
                    {label}<span>{count}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="exercise-list chapter-exercise-list">
            {filteredExercises.map((exercise) => (
              <Link
                className={`exercise-item exercise-status-${exercise.status}`}
                to={`/exercice/${exercise.id}`}
                key={exercise.id}
              >
                <span className="exercise-number">{exercise.originalIndex}</span>
                <div className="exercise-item-copy">
                  <div className="exercise-item-title-row">
                    <strong>{exercise.title}</strong>
                    <span className={`exercise-status-badge ${exercise.status}`}>
                      <StatusIcon status={exercise.status} size={14} /> {statusLabel(exercise.status)}
                    </span>
                  </div>
                  <div className="exercise-meta-row">
                    <span className={`difficulty-chip d${exercise.difficulty}`}><Gauge size={13} /> {difficultyLabel[exercise.difficulty]}</span>
                    <span className="skill-chip">{exercise.skill}</span>
                    <span>{exercise.points} pts</span>
                  </div>
                  <small className="attempt-copy">
                    {exercise.attempt_count === 0
                      ? 'Jamais tenté'
                      : `${exercise.attempt_count} tentative${exercise.attempt_count > 1 ? 's' : ''} • ${exercise.last_result ? 'Dernier résultat : réussi' : 'Dernier résultat : à revoir'}`}
                  </small>
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
