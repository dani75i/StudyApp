import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, CheckCircle2, Dumbbell, Filter, RotateCcw, Target, XCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../api';
import { getSubjectMeta } from '../subjectMeta';

const statusLabels = {
  all: 'Tous',
  todo: 'À faire',
  retry: 'À revoir',
  mastered: 'Maîtrisés',
};

export default function ExercisesLibrary() {
  const [data, setData] = useState(null);
  const [filters, setFilters] = useState({ subject: 'all', chapter: 'all', difficulty: 'all', status: 'all' });

  useEffect(() => {
    api('/exercise-library').then(setData);
  }, []);

  const subjects = useMemo(() => {
    if (!data) return [];
    const seen = new Map();
    data.forEach((exercise) => seen.set(exercise.subject.slug, exercise.subject));
    return [...seen.values()];
  }, [data]);

  const chapters = useMemo(() => {
    if (!data) return [];
    const seen = new Map();
    data
      .filter((exercise) => filters.subject === 'all' || exercise.subject.slug === filters.subject)
      .forEach((exercise) => seen.set(exercise.chapter.id, exercise.chapter));
    return [...seen.values()];
  }, [data, filters.subject]);

  const filtered = useMemo(() => {
    if (!data) return [];
    return data.filter((exercise) => {
      if (filters.subject !== 'all' && exercise.subject.slug !== filters.subject) return false;
      if (filters.chapter !== 'all' && String(exercise.chapter.id) !== String(filters.chapter)) return false;
      if (filters.difficulty !== 'all' && String(exercise.difficulty) !== String(filters.difficulty)) return false;
      if (filters.status !== 'all' && exercise.status !== filters.status) return false;
      return true;
    });
  }, [data, filters]);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  const reset = () => setFilters({ subject: 'all', chapter: 'all', difficulty: 'all', status: 'all' });

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">ENTRAÎNEMENT</span>
          <h1>Exercices</h1>
          <p>Filtre précisément ce que tu veux travailler en maths ou en physique.</p>
        </div>
        <Link className="primary compact" to="/seance">Séance du jour <ArrowRight size={17} /></Link>
      </header>

      <section className="filter-card">
        <div className="filter-title"><Filter size={18} /><strong>Filtres</strong><span>{filtered.length} exercice{filtered.length > 1 ? 's' : ''}</span></div>
        <div className="filter-grid">
          <label>Matière
            <select value={filters.subject} onChange={(e) => setFilters({ ...filters, subject: e.target.value, chapter: 'all' })}>
              <option value="all">Toutes</option>
              {subjects.map((subject) => <option value={subject.slug} key={subject.slug}>{subject.name}</option>)}
            </select>
          </label>
          <label>Chapitre
            <select value={filters.chapter} onChange={(e) => setFilters({ ...filters, chapter: e.target.value })}>
              <option value="all">Tous</option>
              {chapters.map((chapter) => <option value={chapter.id} key={chapter.id}>{chapter.title}</option>)}
            </select>
          </label>
          <label>Difficulté
            <select value={filters.difficulty} onChange={(e) => setFilters({ ...filters, difficulty: e.target.value })}>
              <option value="all">Toutes</option>
              <option value="1">Facile</option>
              <option value="2">Intermédiaire</option>
              <option value="3">Difficile</option>
            </select>
          </label>
          <label>Progression
            <select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
              {Object.entries(statusLabels).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
            </select>
          </label>
        </div>
        <button className="filter-reset" onClick={reset}><RotateCcw size={15} /> Réinitialiser</button>
      </section>

      <div className="exercise-browser-grid">
        {filtered.map((exercise) => {
          const meta = getSubjectMeta(exercise.subject.slug);
          const Icon = meta.icon;
          const status = exercise.status === 'mastered'
            ? { label: 'Maîtrisé', icon: CheckCircle2, cls: 'mastered' }
            : exercise.status === 'retry'
              ? { label: 'À revoir', icon: XCircle, cls: 'retry' }
              : { label: 'À faire', icon: Target, cls: 'todo' };
          const StatusIcon = status.icon;
          return (
            <Link className="browser-exercise-card" to={`/exercice/${exercise.id}`} key={exercise.id}>
              <div className="browser-card-head">
                <div className={`subject-logo mini ${meta.accent}`}><Icon size={18} /></div>
                <span className={`status-chip ${status.cls}`}><StatusIcon size={13} /> {status.label}</span>
              </div>
              <small>{exercise.subject.name} • {exercise.chapter.title}</small>
              <h3>{exercise.title}</h3>
              <div className="browser-card-foot">
                <span>{'●'.repeat(exercise.difficulty)}{'○'.repeat(3 - exercise.difficulty)}</span>
                <span>{exercise.points} pts</span>
                <ArrowRight size={17} />
              </div>
            </Link>
          );
        })}
      </div>

      {!filtered.length && <div className="empty">Aucun exercice ne correspond à ces filtres.</div>}
    </>
  );
}
