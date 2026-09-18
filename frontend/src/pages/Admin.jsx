import React, { useEffect, useMemo, useState } from 'react';
import {
  BookOpenText,
  CirclePlus,
  Dumbbell,
  Layers3,
  Pencil,
  Save,
  ShieldCheck,
  Trash2,
  X,
} from 'lucide-react';
import { api } from '../api';

const levels = ['6e', '5e', '4e', '3e', '2nde', '1re', 'Terminale'];
const emptyChapter = { subject_id: '', level: '3e', title: '', summary: '', order_index: 0 };
const emptyLesson = { chapter_id: '', title: '', body: '', order_index: 0 };
const emptyExercise = {
  chapter_id: '',
  title: '',
  statement: '',
  exercise_type: 'mcq',
  options: ['', '', '', ''],
  correct_answer: '',
  correction: '',
  difficulty: 1,
  points: 10,
  order_index: 0,
};

function SectionHeader({ icon: Icon, title, description, onAdd, addLabel }) {
  return (
    <div className="admin-section-head">
      <div>
        <h2><Icon size={21} /> {title}</h2>
        <p>{description}</p>
      </div>
      <button className="primary compact" onClick={onAdd}><CirclePlus size={17} /> {addLabel}</button>
    </div>
  );
}

function AdminModal({ title, children, onClose }) {
  return (
    <div className="admin-modal-backdrop" onMouseDown={onClose}>
      <div className="admin-modal" onMouseDown={(e) => e.stopPropagation()}>
        <div className="admin-modal-head">
          <h2>{title}</h2>
          <button className="icon-button" onClick={onClose}><X size={19} /></button>
        </div>
        {children}
      </div>
    </div>
  );
}

export default function Admin() {
  const [data, setData] = useState(null);
  const [tab, setTab] = useState('exercises');
  const [modal, setModal] = useState(null);
  const [form, setForm] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [busy, setBusy] = useState(false);
  const [subjectFilter, setSubjectFilter] = useState('all');
  const [levelFilter, setLevelFilter] = useState('all');

  const load = async () => {
    const next = await api('/admin/content');
    setData(next);
  };

  useEffect(() => { load(); }, []);

  const subjectById = useMemo(() => Object.fromEntries((data?.subjects || []).map((s) => [s.id, s])), [data]);
  const chapterById = useMemo(() => Object.fromEntries((data?.chapters || []).map((c) => [c.id, c])), [data]);

  const filteredChapters = useMemo(() => {
    if (!data) return [];
    return data.chapters.filter((chapter) => {
      const subjectOk = subjectFilter === 'all' || String(chapter.subject_id) === subjectFilter;
      const levelOk = levelFilter === 'all' || chapter.level === levelFilter;
      return subjectOk && levelOk;
    });
  }, [data, subjectFilter, levelFilter]);

  const filteredLessons = useMemo(() => {
    if (!data) return [];
    const allowed = new Set(filteredChapters.map((c) => c.id));
    return data.lessons.filter((lesson) => allowed.has(lesson.chapter_id));
  }, [data, filteredChapters]);

  const filteredExercises = useMemo(() => {
    if (!data) return [];
    const allowed = new Set(filteredChapters.map((c) => c.id));
    return data.exercises.filter((exercise) => allowed.has(exercise.chapter_id));
  }, [data, filteredChapters]);

  const openNew = (kind) => {
    setError('');
    if (kind === 'chapter') {
      setForm({ ...emptyChapter, subject_id: data.subjects[0]?.id || '' });
    } else if (kind === 'lesson') {
      setForm({ ...emptyLesson, chapter_id: filteredChapters[0]?.id || data.chapters[0]?.id || '' });
    } else {
      setForm({ ...emptyExercise, chapter_id: filteredChapters[0]?.id || data.chapters[0]?.id || '', options: [...emptyExercise.options] });
    }
    setModal({ kind, id: null });
  };

  const openEdit = (kind, item) => {
    setError('');
    setForm({ ...item, options: item.options ? [...item.options, '', '', '', ''].slice(0, 6) : undefined });
    setModal({ kind, id: item.id });
  };

  const closeModal = () => {
    if (busy) return;
    setModal(null);
    setForm(null);
    setError('');
  };

  const save = async (event) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    try {
      const endpoint = modal.kind === 'chapter' ? 'chapters' : modal.kind === 'lesson' ? 'lessons' : 'exercises';
      const body = { ...form };
      if (modal.kind === 'chapter') body.subject_id = Number(body.subject_id);
      if (modal.kind !== 'chapter') body.chapter_id = Number(body.chapter_id);
      body.order_index = Number(body.order_index || 0);
      if (modal.kind === 'exercise') {
        body.difficulty = Number(body.difficulty);
        body.points = Number(body.points);
        body.options = body.exercise_type === 'mcq' ? body.options.filter((value) => value.trim()) : [];
      }
      await api(`/admin/${endpoint}${modal.id ? `/${modal.id}` : ''}`, {
        method: modal.id ? 'PATCH' : 'POST',
        body: JSON.stringify(body),
      });
      await load();
      setSuccess(modal.id ? 'Modification enregistrée.' : 'Contenu ajouté à la base.');
      setTimeout(() => setSuccess(''), 2500);
      setModal(null);
      setForm(null);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  const remove = async (kind, item) => {
    const label = kind === 'chapter' ? 'ce chapitre et tout son contenu' : kind === 'lesson' ? 'ce cours' : 'cet exercice';
    if (!window.confirm(`Supprimer ${label} ? Cette action est définitive.`)) return;
    const endpoint = kind === 'chapter' ? 'chapters' : kind === 'lesson' ? 'lessons' : 'exercises';
    try {
      await api(`/admin/${endpoint}/${item.id}`, { method: 'DELETE' });
      await load();
      setSuccess('Suppression effectuée.');
      setTimeout(() => setSuccess(''), 2500);
    } catch (err) {
      setError(err.message);
    }
  };

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">ADMINISTRATION</span>
          <h1>Gestion du contenu</h1>
          <p>Ajoute et modifie les chapitres, cours et exercices enregistrés dans la base de données.</p>
        </div>
        <div className="admin-badge"><ShieldCheck size={18} /> Accès administrateur</div>
      </header>

      {success && <div className="alert success admin-feedback">{success}</div>}
      {error && !modal && <div className="alert error admin-feedback">{error}</div>}

      <div className="admin-summary-grid">
        <div className="admin-summary"><Layers3 /><div><strong>{data.chapters.length}</strong><span>chapitres</span></div></div>
        <div className="admin-summary"><BookOpenText /><div><strong>{data.lessons.length}</strong><span>fiches de cours</span></div></div>
        <div className="admin-summary"><Dumbbell /><div><strong>{data.exercises.length}</strong><span>exercices</span></div></div>
      </div>

      <div className="admin-toolbar">
        <div className="admin-tabs">
          <button className={tab === 'chapters' ? 'active' : ''} onClick={() => setTab('chapters')}>Chapitres</button>
          <button className={tab === 'lessons' ? 'active' : ''} onClick={() => setTab('lessons')}>Cours</button>
          <button className={tab === 'exercises' ? 'active' : ''} onClick={() => setTab('exercises')}>Exercices</button>
        </div>
        <div className="admin-filters">
          <select value={subjectFilter} onChange={(e) => setSubjectFilter(e.target.value)}>
            <option value="all">Toutes les matières</option>
            {data.subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.emoji} {subject.name}</option>)}
          </select>
          <select value={levelFilter} onChange={(e) => setLevelFilter(e.target.value)}>
            <option value="all">Tous les niveaux</option>
            {levels.map((level) => <option key={level}>{level}</option>)}
          </select>
        </div>
      </div>

      {tab === 'chapters' && (
        <section className="admin-panel">
          <SectionHeader icon={Layers3} title="Chapitres" description="Structure les programmes par matière et par niveau." onAdd={() => openNew('chapter')} addLabel="Nouveau chapitre" />
          <div className="admin-list">
            {filteredChapters.map((chapter) => (
              <article className="admin-row" key={chapter.id}>
                <div className="admin-row-main">
                  <span className="subject-pill">{subjectById[chapter.subject_id]?.emoji} {subjectById[chapter.subject_id]?.name} • {chapter.level}</span>
                  <strong>{chapter.title}</strong>
                  <p>{chapter.summary || 'Aucun résumé.'}</p>
                  <small>{chapter.lesson_count} cours • {chapter.exercise_count} exercices • ordre {chapter.order_index}</small>
                </div>
                <div className="admin-actions">
                  <button onClick={() => openEdit('chapter', chapter)}><Pencil size={16} /> Modifier</button>
                  <button className="danger" onClick={() => remove('chapter', chapter)}><Trash2 size={16} /> Supprimer</button>
                </div>
              </article>
            ))}
            {!filteredChapters.length && <div className="empty">Aucun chapitre avec ces filtres.</div>}
          </div>
        </section>
      )}

      {tab === 'lessons' && (
        <section className="admin-panel">
          <SectionHeader icon={BookOpenText} title="Cours" description="Crée les fiches pédagogiques affichées dans chaque chapitre." onAdd={() => openNew('lesson')} addLabel="Nouveau cours" />
          <div className="admin-list">
            {filteredLessons.map((lesson) => {
              const chapter = chapterById[lesson.chapter_id];
              return (
                <article className="admin-row" key={lesson.id}>
                  <div className="admin-row-main">
                    <span className="subject-pill">{chapter?.level} • {chapter?.title}</span>
                    <strong>{lesson.title}</strong>
                    <p className="admin-preview">{lesson.body}</p>
                    <small>ordre {lesson.order_index}</small>
                  </div>
                  <div className="admin-actions">
                    <button onClick={() => openEdit('lesson', lesson)}><Pencil size={16} /> Modifier</button>
                    <button className="danger" onClick={() => remove('lesson', lesson)}><Trash2 size={16} /> Supprimer</button>
                  </div>
                </article>
              );
            })}
            {!filteredLessons.length && <div className="empty">Aucun cours avec ces filtres.</div>}
          </div>
        </section>
      )}

      {tab === 'exercises' && (
        <section className="admin-panel">
          <SectionHeader icon={Dumbbell} title="Exercices" description="Les exercices enregistrés ici deviennent disponibles aux élèves du niveau concerné." onAdd={() => openNew('exercise')} addLabel="Nouvel exercice" />
          <div className="admin-list">
            {filteredExercises.map((exercise) => {
              const chapter = chapterById[exercise.chapter_id];
              return (
                <article className="admin-row" key={exercise.id}>
                  <div className="admin-row-main">
                    <span className="subject-pill">{chapter?.level} • {chapter?.title}</span>
                    <strong>{exercise.title}</strong>
                    <p className="admin-preview">{exercise.statement}</p>
                    <small>{exercise.exercise_type === 'mcq' ? 'QCM' : 'Réponse libre'} • difficulté {exercise.difficulty}/3 • {exercise.points} pts</small>
                  </div>
                  <div className="admin-actions">
                    <button onClick={() => openEdit('exercise', exercise)}><Pencil size={16} /> Modifier</button>
                    <button className="danger" onClick={() => remove('exercise', exercise)}><Trash2 size={16} /> Supprimer</button>
                  </div>
                </article>
              );
            })}
            {!filteredExercises.length && <div className="empty">Aucun exercice avec ces filtres.</div>}
          </div>
        </section>
      )}

      {modal && form && (
        <AdminModal
          title={`${modal.id ? 'Modifier' : 'Ajouter'} ${modal.kind === 'chapter' ? 'un chapitre' : modal.kind === 'lesson' ? 'un cours' : 'un exercice'}`}
          onClose={closeModal}
        >
          <form className="admin-form" onSubmit={save}>
            {modal.kind === 'chapter' && (
              <>
                <div className="admin-form-grid">
                  <label>Matière
                    <select value={form.subject_id} onChange={(e) => setForm({ ...form, subject_id: e.target.value })} required>
                      {data.subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.emoji} {subject.name}</option>)}
                    </select>
                  </label>
                  <label>Niveau
                    <select value={form.level} onChange={(e) => setForm({ ...form, level: e.target.value })}>{levels.map((level) => <option key={level}>{level}</option>)}</select>
                  </label>
                </div>
                <label>Titre<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></label>
                <label>Résumé<textarea rows="4" value={form.summary} onChange={(e) => setForm({ ...form, summary: e.target.value })} /></label>
                <label>Ordre<input type="number" min="0" value={form.order_index} onChange={(e) => setForm({ ...form, order_index: e.target.value })} /></label>
              </>
            )}

            {modal.kind === 'lesson' && (
              <>
                <label>Chapitre
                  <select value={form.chapter_id} onChange={(e) => setForm({ ...form, chapter_id: e.target.value })} required>
                    {data.chapters.map((chapter) => <option key={chapter.id} value={chapter.id}>{chapter.level} • {subjectById[chapter.subject_id]?.name} • {chapter.title}</option>)}
                  </select>
                </label>
                <label>Titre<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></label>
                <label>Contenu du cours<textarea rows="12" value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} required /></label>
                <label>Ordre<input type="number" min="0" value={form.order_index} onChange={(e) => setForm({ ...form, order_index: e.target.value })} /></label>
              </>
            )}

            {modal.kind === 'exercise' && (
              <>
                <label>Chapitre
                  <select value={form.chapter_id} onChange={(e) => setForm({ ...form, chapter_id: e.target.value })} required>
                    {data.chapters.map((chapter) => <option key={chapter.id} value={chapter.id}>{chapter.level} • {subjectById[chapter.subject_id]?.name} • {chapter.title}</option>)}
                  </select>
                </label>
                <label>Titre<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></label>
                <label>Énoncé<textarea rows="5" value={form.statement} onChange={(e) => setForm({ ...form, statement: e.target.value })} required /></label>
                <div className="admin-form-grid three">
                  <label>Type
                    <select value={form.exercise_type} onChange={(e) => setForm({ ...form, exercise_type: e.target.value })}>
                      <option value="mcq">QCM</option>
                      <option value="text">Réponse libre</option>
                    </select>
                  </label>
                  <label>Difficulté
                    <select value={form.difficulty} onChange={(e) => setForm({ ...form, difficulty: e.target.value })}>
                      <option value="1">Facile</option>
                      <option value="2">Moyen</option>
                      <option value="3">Difficile</option>
                    </select>
                  </label>
                  <label>Points<input type="number" min="1" max="1000" value={form.points} onChange={(e) => setForm({ ...form, points: e.target.value })} /></label>
                </div>

                {form.exercise_type === 'mcq' && (
                  <div className="admin-option-box">
                    <strong>Réponses proposées</strong>
                    <p>Ajoute au moins deux choix. La bonne réponse doit correspondre exactement à l'un des choix.</p>
                    {form.options.map((option, index) => (
                      <input
                        key={index}
                        value={option}
                        placeholder={`Choix ${index + 1}`}
                        onChange={(e) => {
                          const options = [...form.options];
                          options[index] = e.target.value;
                          setForm({ ...form, options });
                        }}
                      />
                    ))}
                  </div>
                )}

                <label>Bonne réponse<input value={form.correct_answer} onChange={(e) => setForm({ ...form, correct_answer: e.target.value })} required /></label>
                <label>Correction détaillée<textarea rows="7" value={form.correction} onChange={(e) => setForm({ ...form, correction: e.target.value })} required /></label>
                <label>Ordre<input type="number" min="0" value={form.order_index} onChange={(e) => setForm({ ...form, order_index: e.target.value })} /></label>
              </>
            )}

            {error && <div className="alert error">{error}</div>}
            <div className="admin-form-actions">
              <button type="button" className="secondary" onClick={closeModal}>Annuler</button>
              <button className="primary" disabled={busy}><Save size={17} /> {busy ? 'Enregistrement…' : 'Enregistrer dans la base'}</button>
            </div>
          </form>
        </AdminModal>
      )}
    </>
  );
}
