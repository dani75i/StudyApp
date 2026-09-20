import React, { useEffect, useMemo, useState } from 'react';
import {
  AlignLeft,
  BookOpen,
  BookOpenText,
  CirclePlus,
  Copy,
  Dumbbell,
  Eye,
  Lightbulb,
  MessageCircleHeart,
  List,
  Layers3,
  Pencil,
  Save,
  Search,
  ShieldCheck,
  Sigma,
  Trash2,
  X,
} from 'lucide-react';
import { api } from '../api';
import { Link } from 'react-router-dom';
import {
  emptyLessonBlocks,
  insertSnippet,
  lessonPreview,
  parseLessonBlocks,
  serializeLessonBlocks,
} from '../contentFormat';
import { LessonContent, RichText } from '../components/RichContent';

const levels = ['6e', '5e', '4e', '3e', '2nde', '1re', 'Terminale'];
const emptyChapter = { subject_id: '', level: '3e', title: '', summary: '', order_index: 0 };
const emptyLesson = { chapter_id: '', title: '', body: '', blocks: emptyLessonBlocks(), order_index: 0 };
const emptyExercise = {
  chapter_id: '',
  title: '',
  statement: '',
  exercise_type: 'mcq',
  options: ['', '', '', ''],
  correct_answer: '',
  correction: '',
  hints: ['', ''],
  steps: [],
  method: '',
  difficulty: 1,
  points: 10,
  order_index: 0,
};

const mathSnippets = [
  ['x²', '\\(x^2\\)'],
  ['Fraction', '\\(\\frac{a}{b}\\)'],
  ['Racine', '\\(\\sqrt{x}\\)'],
  ['×', '\\(a \\times b\\)'],
  ['π', '\\(\\pi\\)'],
  ['Formule centrée', '\\[a = b\\]'],
];

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

function AdminModal({ title, children, onClose, wide = false }) {
  return (
    <div className="admin-modal-backdrop" onMouseDown={onClose}>
      <div className={`admin-modal ${wide ? 'wide' : ''}`} onMouseDown={(e) => e.stopPropagation()}>
        <div className="admin-modal-head">
          <h2>{title}</h2>
          <button className="icon-button" onClick={onClose}><X size={19} /></button>
        </div>
        {children}
      </div>
    </div>
  );
}

function MathToolbar({ value, onChange }) {
  return (
    <div className="math-toolbar">
      <span><Sigma size={14} /> Insérer :</span>
      {mathSnippets.map(([label, snippet]) => (
        <button type="button" key={label} onClick={() => onChange(insertSnippet(value, snippet))}>{label}</button>
      ))}
    </div>
  );
}

function LessonBlockEditor({ blocks, onChange }) {
  const updateBlock = (index, patch) => {
    const next = blocks.map((block, i) => i === index ? { ...block, ...patch } : block);
    onChange(next);
  };

  const removeBlock = (index) => {
    const next = blocks.filter((_, i) => i !== index);
    onChange(next.length ? next : emptyLessonBlocks());
  };

  const addBlock = (type) => {
    const block = type === 'list' ? { type, items: [''] } : { type, content: '' };
    onChange([...blocks, block]);
  };

  return (
    <div className="lesson-editor-layout">
      <div className="lesson-block-editor">
        <div className="block-add-toolbar">
          <strong>Construire la fiche</strong>
          <div>
            <button type="button" onClick={() => addBlock('paragraph')}><AlignLeft size={15} /> Paragraphe</button>
            <button type="button" onClick={() => addBlock('formula')}><Sigma size={15} /> Formule</button>
            <button type="button" onClick={() => addBlock('list')}><List size={15} /> Liste</button>
            <button type="button" onClick={() => addBlock('note')}><Lightbulb size={15} /> À retenir</button>
            <button type="button" onClick={() => addBlock('example')}><BookOpen size={15} /> Exemple</button>
          </div>
        </div>

        <div className="lesson-block-list">
          {blocks.map((block, index) => (
            <div className={`lesson-edit-block type-${block.type}`} key={`${block.type}-${index}`}>
              <div className="lesson-edit-block-head">
                <span>{index + 1}. {block.type === 'paragraph' ? 'Paragraphe' : block.type === 'formula' ? 'Formule' : block.type === 'list' ? 'Liste' : block.type === 'example' ? 'Exemple' : 'À retenir'}</span>
                <button type="button" className="danger-icon" onClick={() => removeBlock(index)}><Trash2 size={15} /></button>
              </div>

              {block.type === 'formula' && (
                <>
                  <textarea
                    rows="3"
                    value={block.content || ''}
                    onChange={(e) => updateBlock(index, { content: e.target.value })}
                    placeholder="Ex. P = m \\times g"
                  />
                  <div className="formula-help">Écris uniquement la formule. Exemple : <code>{'\\\\frac{a}{b}'}</code>, <code>x^2</code>, <code>{'\\\\sqrt{x}'}</code>.</div>
                </>
              )}

              {block.type === 'list' && (
                <textarea
                  rows="5"
                  value={(block.items || []).join('\n')}
                  onChange={(e) => updateBlock(index, { items: e.target.value.split('\n') })}
                  placeholder={'Un élément par ligne\nP : poids en newtons (N)\nm : masse en kilogrammes (kg)'}
                />
              )}

              {(block.type === 'paragraph' || block.type === 'note' || block.type === 'example') && (
                <>
                  <textarea
                    rows={block.type === 'note' || block.type === 'example' ? 4 : 5}
                    value={block.content || ''}
                    onChange={(e) => updateBlock(index, { content: e.target.value })}
                    placeholder={block.type === 'note' ? 'La notion essentielle à mémoriser…' : block.type === 'example' ? 'Exemple concret, calcul commenté ou cas pratique…' : 'Explique la notion avec des phrases courtes et aérées…'}
                  />
                  <MathToolbar value={block.content || ''} onChange={(value) => updateBlock(index, { content: value })} />
                </>
              )}
            </div>
          ))}
        </div>
      </div>

      <aside className="lesson-live-preview">
        <div className="preview-title"><Eye size={17} /> Aperçu élève</div>
        <div className="lesson-card preview-lesson-card">
          <div className="lesson-tag">Fiche cours</div>
          <LessonContent body={serializeLessonBlocks(blocks)} />
        </div>
      </aside>
    </div>
  );
}

function ExercisePreview({ form }) {
  return (
    <div className="exercise-admin-preview">
      <div className="preview-title"><Eye size={17} /> Aperçu</div>
      <div className="exercise-preview-card">
        <h3>{form.title || 'Titre de l’exercice'}</h3>
        <div className="preview-statement"><RichText text={form.statement || 'L’énoncé apparaîtra ici.'} /></div>
        {form.exercise_type === 'mcq' && (
          <div className="preview-options">
            {form.options.filter(Boolean).map((option, index) => <div key={index}><span>{String.fromCharCode(65 + index)}</span><RichText text={option} /></div>)}
          </div>
        )}
        <div className="preview-correction">
          <strong>Correction</strong>
          <div><RichText text={form.correction || 'La correction détaillée apparaîtra ici.'} /></div>
        </div>
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
  const [chapterFilter, setChapterFilter] = useState('all');
  const [query, setQuery] = useState('');

  const load = async () => {
    const next = await api('/admin/content');
    setData(next);
  };

  useEffect(() => { load(); }, []);

  const subjectById = useMemo(() => Object.fromEntries((data?.subjects || []).map((s) => [s.id, s])), [data]);
  const chapterById = useMemo(() => Object.fromEntries((data?.chapters || []).map((c) => [c.id, c])), [data]);

  const baseChapters = useMemo(() => {
    if (!data) return [];
    return data.chapters.filter((chapter) => {
      const subjectOk = subjectFilter === 'all' || String(chapter.subject_id) === subjectFilter;
      const levelOk = levelFilter === 'all' || chapter.level === levelFilter;
      return subjectOk && levelOk;
    });
  }, [data, subjectFilter, levelFilter]);

  useEffect(() => {
    if (chapterFilter !== 'all' && !baseChapters.some((chapter) => String(chapter.id) === chapterFilter)) setChapterFilter('all');
  }, [baseChapters, chapterFilter]);

  const matchesQuery = (value) => String(value || '').toLocaleLowerCase('fr').includes(query.trim().toLocaleLowerCase('fr'));

  const filteredChapters = useMemo(() => baseChapters.filter((chapter) => !query.trim() || matchesQuery(`${chapter.title} ${chapter.summary}`)), [baseChapters, query]);

  const allowedChapterIds = useMemo(() => new Set(
    baseChapters
      .filter((chapter) => chapterFilter === 'all' || String(chapter.id) === chapterFilter)
      .map((chapter) => chapter.id)
  ), [baseChapters, chapterFilter]);

  const filteredLessons = useMemo(() => {
    if (!data) return [];
    return data.lessons.filter((lesson) => allowedChapterIds.has(lesson.chapter_id) && (!query.trim() || matchesQuery(`${lesson.title} ${lessonPreview(lesson.body)}`)));
  }, [data, allowedChapterIds, query]);

  const filteredExercises = useMemo(() => {
    if (!data) return [];
    return data.exercises.filter((exercise) => allowedChapterIds.has(exercise.chapter_id) && (!query.trim() || matchesQuery(`${exercise.title} ${exercise.statement} ${exercise.correction}`)));
  }, [data, allowedChapterIds, query]);

  const openNew = (kind) => {
    setError('');
    if (kind === 'chapter') {
      setForm({ ...emptyChapter, subject_id: data.subjects[0]?.id || '' });
    } else if (kind === 'lesson') {
      setForm({ ...emptyLesson, chapter_id: baseChapters[0]?.id || data.chapters[0]?.id || '', blocks: emptyLessonBlocks() });
    } else {
      setForm({ ...emptyExercise, chapter_id: baseChapters[0]?.id || data.chapters[0]?.id || '', options: [...emptyExercise.options] });
    }
    setModal({ kind, id: null });
  };

  const openEdit = (kind, item) => {
    setError('');
    if (kind === 'lesson') {
      setForm({ ...item, blocks: parseLessonBlocks(item.body) });
    } else if (kind === 'exercise') {
      setForm({ ...item, options: [...(item.options || []), '', '', '', ''].slice(0, 6), hints: [...(item.hints || []), '', ''].slice(0, 2), steps: item.steps || [], method: item.method || '' });
    } else {
      setForm({ ...item });
    }
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
      if (modal.kind === 'lesson') {
        body.body = serializeLessonBlocks(body.blocks);
        delete body.blocks;
      }
      if (modal.kind === 'exercise') {
        body.difficulty = Number(body.difficulty);
        body.points = Number(body.points);
        body.options = body.exercise_type === 'mcq' ? body.options.filter((value) => value.trim()) : [];
        body.hints = (body.hints || []).map(value => value.trim()).filter(Boolean);
        body.steps = (body.steps || []).map(value => value.trim()).filter(Boolean);
      }
      await api(`/admin/${endpoint}${modal.id ? `/${modal.id}` : ''}`, {
        method: modal.id ? 'PATCH' : 'POST',
        body: JSON.stringify(body),
      });
      await load();
      setSuccess(modal.id ? 'Modification enregistrée immédiatement dans la base.' : 'Contenu ajouté à la base.');
      setTimeout(() => setSuccess(''), 3000);
      setModal(null);
      setForm(null);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  const duplicateExercise = async (exercise) => {
    const body = {
      ...exercise,
      chapter_id: Number(exercise.chapter_id),
      title: `${exercise.title} — copie`,
      options: exercise.options || [],
      order_index: Number(exercise.order_index || 0) + 1,
    };
    delete body.id;
    try {
      await api('/admin/exercises', { method: 'POST', body: JSON.stringify(body) });
      await load();
      setSuccess('Exercice dupliqué. Tu peux maintenant modifier la copie.');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.message);
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
          <p>Corrige les cours et exercices directement ici : les changements sont enregistrés dans Neon sans modifier le code.</p>
        </div>
<div className="feedback-admin-header-actions"><Link className="secondary" to="/admin/avis"><MessageCircleHeart size={18} /> Avis utilisateurs</Link><div className="admin-badge"><ShieldCheck size={18} /> Accès administrateur</div></div>
      </header>

      {success && <div className="alert success admin-feedback">{success}</div>}
      {error && !modal && <div className="alert error admin-feedback">{error}</div>}

      <div className="admin-summary-grid">
        <div className="admin-summary"><Layers3 /><div><strong>{data.chapters.length}</strong><span>chapitres</span></div></div>
        <div className="admin-summary"><BookOpenText /><div><strong>{data.lessons.length}</strong><span>fiches de cours</span></div></div>
        <div className="admin-summary"><Dumbbell /><div><strong>{data.exercises.length}</strong><span>exercices</span></div></div>
      </div>

      <div className="admin-toolbar admin-toolbar-v73">
        <div className="admin-tabs">
          <button className={tab === 'chapters' ? 'active' : ''} onClick={() => setTab('chapters')}>Chapitres</button>
          <button className={tab === 'lessons' ? 'active' : ''} onClick={() => setTab('lessons')}>Cours</button>
          <button className={tab === 'exercises' ? 'active' : ''} onClick={() => setTab('exercises')}>Exercices</button>
        </div>
        <div className="admin-search"><Search size={16} /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Rechercher un contenu…" /></div>
        <div className="admin-filters">
          <select value={subjectFilter} onChange={(e) => setSubjectFilter(e.target.value)}>
            <option value="all">Toutes les matières</option>
            {data.subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.emoji} {subject.name}</option>)}
          </select>
          <select value={levelFilter} onChange={(e) => setLevelFilter(e.target.value)}>
            <option value="all">Tous les niveaux</option>
            {levels.map((level) => <option key={level}>{level}</option>)}
          </select>
          {tab !== 'chapters' && (
            <select value={chapterFilter} onChange={(e) => setChapterFilter(e.target.value)}>
              <option value="all">Tous les chapitres</option>
              {baseChapters.map((chapter) => <option key={chapter.id} value={chapter.id}>{chapter.level} • {chapter.title}</option>)}
            </select>
          )}
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
          <SectionHeader icon={BookOpenText} title="Cours" description="Modifie les fiches existantes avec paragraphes, formules, listes et encarts." onAdd={() => openNew('lesson')} addLabel="Nouveau cours" />
          <div className="admin-list">
            {filteredLessons.map((lesson) => {
              const chapter = chapterById[lesson.chapter_id];
              return (
                <article className="admin-row" key={lesson.id}>
                  <div className="admin-row-main">
                    <span className="subject-pill">{chapter?.level} • {chapter?.title}</span>
                    <strong>{lesson.title}</strong>
                    <p className="admin-preview">{lessonPreview(lesson.body)}</p>
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
          <SectionHeader icon={Dumbbell} title="Exercices" description="Corrige l’énoncé, la réponse ou la correction sans toucher directement à la base." onAdd={() => openNew('exercise')} addLabel="Nouvel exercice" />
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
                    <button onClick={() => duplicateExercise(exercise)}><Copy size={16} /> Dupliquer</button>
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
          wide={modal.kind !== 'chapter'}
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
                <div className="admin-form-grid">
                  <label>Chapitre
                    <select value={form.chapter_id} onChange={(e) => setForm({ ...form, chapter_id: e.target.value })} required>
                      {data.chapters.map((chapter) => <option key={chapter.id} value={chapter.id}>{chapter.level} • {subjectById[chapter.subject_id]?.name} • {chapter.title}</option>)}
                    </select>
                  </label>
                  <label>Ordre<input type="number" min="0" value={form.order_index} onChange={(e) => setForm({ ...form, order_index: e.target.value })} /></label>
                </div>
                <label>Titre<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></label>
                <LessonBlockEditor blocks={form.blocks || emptyLessonBlocks()} onChange={(blocks) => setForm({ ...form, blocks })} />
              </>
            )}

            {modal.kind === 'exercise' && (
              <div className="exercise-editor-layout">
                <div>
                  <label>Chapitre
                    <select value={form.chapter_id} onChange={(e) => setForm({ ...form, chapter_id: e.target.value })} required>
                      {data.chapters.map((chapter) => <option key={chapter.id} value={chapter.id}>{chapter.level} • {subjectById[chapter.subject_id]?.name} • {chapter.title}</option>)}
                    </select>
                  </label>
                  <label>Titre<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></label>
                  <label>Énoncé<textarea rows="5" value={form.statement} onChange={(e) => setForm({ ...form, statement: e.target.value })} required /></label>
                  <MathToolbar value={form.statement} onChange={(statement) => setForm({ ...form, statement })} />
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
                      <p>La bonne réponse doit correspondre exactement à l'un des choix.</p>
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
                  <MathToolbar value={form.correction} onChange={(correction) => setForm({ ...form, correction })} />
                  <div className="v9-admin-guides">
                    <strong>Indices et correction pas à pas (V9)</strong>
                    <p>Les indices s’affichent avant validation ; les étapes et la méthode apparaissent uniquement après la réponse.</p>
                    {(form.hints || ['', '']).map((hint, index) => (
                      <label key={index}>Indice {index + 1}
                        <textarea rows="2" value={hint} onChange={(event) => {
                          const hints = [...form.hints]; hints[index] = event.target.value; setForm({ ...form, hints });
                        }} placeholder={index ? 'Deuxième coup de pouce…' : 'Premier coup de pouce…'} />
                      </label>
                    ))}
                    <label>Étapes de la correction (une par ligne)
                      <textarea rows="6" value={(form.steps || []).join('\n')} onChange={(event) => setForm({ ...form, steps: event.target.value.split('\n') })} placeholder="Étape 1 : …\nÉtape 2 : …" />
                    </label>
                    <label>Méthode à retenir
                      <textarea rows="3" value={form.method || ''} onChange={(event) => setForm({ ...form, method: event.target.value })} placeholder="Conseil pédagogique…" />
                    </label>
                  </div>
                  <label>Ordre<input type="number" min="0" value={form.order_index} onChange={(e) => setForm({ ...form, order_index: e.target.value })} /></label>
                </div>
                <ExercisePreview form={form} />
              </div>
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
