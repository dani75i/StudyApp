import React, { useCallback, useEffect, useState } from 'react';
import { ArrowLeft, CheckCircle2, Inbox, MessageCircleHeart, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../api';

const categoryNames = {
  opinion: '⭐ Avis général', bug: '🐛 Problème technique',
  content_error: '📚 Erreur de cours / exercice', suggestion: '💡 Suggestion',
};
const statusNames = {
  new: 'Nouveau', in_progress: 'En cours', resolved: 'Traité', dismissed: 'Classé sans suite',
};
const safePage = (value) => typeof value === 'string' && /^\/(?:decouvrir\/cours\/?\d*|(?:chapitre|exercice)\/\d+(?:\/correction)?|cours|exercices|dashboard|seance|recompenses|historique|profil|confidentialite|connexion|inscription|)$/.test(value);

export default function AdminFeedback() {
  const [data, setData] = useState(null);
  const [filter, setFilter] = useState('all');
  const [category, setCategory] = useState('all');
  const [page, setPage] = useState(1);
  const [busyId, setBusyId] = useState(null);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    try {
      setError('');
      setData(await api(`/admin/feedback?status=${filter}&category=${category}&page=${page}`));
    } catch (err) { setError(err.message); }
  }, [filter, category, page]);
  useEffect(() => { load(); }, [load]);

  async function changeStatus(id, status) {
    setBusyId(id);
    try {
      await api(`/admin/feedback/${id}`, { method: 'PATCH', body: JSON.stringify({ status }) });
      await load();
    } catch (err) { setError(err.message); }
    finally { setBusyId(null); }
  }
  async function remove(id) {
    if (!window.confirm('Supprimer définitivement cet avis ?')) return;
    setBusyId(id);
    try {
      await api(`/admin/feedback/${id}`, { method: 'DELETE' });
      await load();
    } catch (err) { setError(err.message); }
    finally { setBusyId(null); }
  }

  return <div className="feedback-admin-page">
    <header className="page-header">
      <div><Link className="back" to="/admin"><ArrowLeft size={17} /> Retour à l'administration</Link>
        <span className="eyebrow">ADMINISTRATION · RETOURS</span>
        <h1><MessageCircleHeart size={28} /> Avis utilisateurs</h1>
        <p>Messages privés des visiteurs et des élèves. Aucun avis n'est publié automatiquement sur le site.</p>
      </div>
      <span className="feedback-new-counter"><Inbox size={19}/>{data ? data.new_count : '…'} nouveaux</span>
    </header>
    <div className="feedback-admin-filters">
      <label>Statut<select value={filter} onChange={event => { setFilter(event.target.value); setPage(1); }}>
        <option value="all">Tous les statuts</option>{Object.entries(statusNames).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
      </select></label>
      <label>Catégorie<select value={category} onChange={event => { setCategory(event.target.value); setPage(1); }}>
        <option value="all">Toutes les catégories</option>{Object.entries(categoryNames).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
      </select></label>
      <button type="button" className="secondary" onClick={load}>Actualiser</button>
    </div>
    {error && <p role="alert" className="alert error">{error}</p>}
    {!data && !error && <div className="loader-page"><div className="loader"/></div>}
    {data && !data.items.length && <div className="feedback-empty"><CheckCircle2 size={29} /><strong>Aucun retour pour ces filtres</strong><p>Les prochains messages s'afficheront ici.</p></div>}
    {data?.items.map(item => <article className="feedback-admin-card" key={item.id}>
      <div className="feedback-admin-meta">
        <span className={`feedback-status status-${item.status}`}>{statusNames[item.status]}</span>
        <span>{categoryNames[item.category]}</span>
        <time dateTime={item.created_at}>{new Date(item.created_at + (item.created_at.endsWith('Z') ? '' : 'Z')).toLocaleString('fr-FR', { dateStyle: 'medium', timeStyle: 'short' })}</time>
      </div>
      <div className="feedback-admin-rating">{item.rating ? `${'★'.repeat(item.rating)}${'☆'.repeat(5 - item.rating)} · ${item.rating}/5` : 'Aucune note'}</div>
      <p className="feedback-admin-message">{item.message}</p>
      {item.page_path && <div className="feedback-admin-source">Page concernée : {safePage(item.page_path) ? <Link to={item.page_path}>{item.page_path}</Link> : <span>{item.page_path}</span>}</div>}
      <div className="feedback-admin-actions">
        <label>Traitement <select disabled={busyId === item.id} value={item.status} onChange={event => changeStatus(item.id, event.target.value)}>
          {Object.entries(statusNames).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select></label>
        <button disabled={busyId === item.id} type="button" className="feedback-delete" onClick={() => remove(item.id)}><Trash2 size={16}/> Supprimer</button>
      </div>
    </article>)}
    {data && data.total > data.per_page && <div className="feedback-pagination">
      <button className="secondary" type="button" disabled={page === 1} onClick={() => setPage(current => current - 1)}>Précédent</button>
      <span>Page {page} / {Math.ceil(data.total / data.per_page)} · {data.total} avis</span>
      <button className="secondary" type="button" disabled={page * data.per_page >= data.total} onClick={() => setPage(current => current + 1)}>Suivant</button>
    </div>}
  </div>;
}
