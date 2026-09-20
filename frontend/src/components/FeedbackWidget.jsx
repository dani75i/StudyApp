import React, { useEffect, useId, useState } from 'react';
import { CheckCircle2, MessageCircleHeart, Send, Star, X } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import { api } from '../api';

export const OPEN_FEEDBACK_EVENT = 'exodeclic:open-feedback';

const types = [
  ['opinion', '⭐', 'Donner mon avis'],
  ['bug', '🐛', 'Signaler un problème'],
  ['content_error', '📚', 'Erreur dans un cours ou un exercice'],
  ['suggestion', '💡', 'Proposer une idée'],
];
const initial = { category: '', rating: 0, message: '', website: '' };

export default function FeedbackWidget() {
  const { pathname } = useLocation();
  const headingId = useId();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState(initial);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState('');
  const [sending, setSending] = useState(false);
  const isPrivateMobile = !['/', '/decouvrir/cours', '/connexion', '/inscription', '/confidentialite'].includes(pathname) && !pathname.startsWith('/decouvrir/cours/');

  useEffect(() => {
    const handler = () => { setOpen(true); setStatus('idle'); setError(''); setForm(initial); };
    window.addEventListener(OPEN_FEEDBACK_EVENT, handler);
    return () => window.removeEventListener(OPEN_FEEDBACK_EVENT, handler);
  }, []);

  useEffect(() => {
    if (!open) return undefined;
    const onKeyDown = (event) => { if (event.key === 'Escape' && !sending) setOpen(false); };
    window.addEventListener('keydown', onKeyDown);
    const old = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = old; window.removeEventListener('keydown', onKeyDown); };
  }, [open, sending]);

  async function submit(event) {
    event.preventDefault();
    setError('');
    setSending(true);
    try {
      await api('/feedback', { method: 'POST', body: JSON.stringify({
        category: form.category,
        rating: form.rating || null,
        message: form.message.trim(),
        page_path: pathname.slice(0, 240),
        website: form.website,
      }) });
      setStatus('sent');
    } catch (err) {
      setError(err.message || 'Envoi impossible, réessaie plus tard.');
    } finally {
      setSending(false);
    }
  }

  return <>
    <button type="button" className={`feedback-fab ${isPrivateMobile ? 'private-page' : ''}`} onClick={() => { setOpen(true); setForm(initial); setError(''); setStatus('idle'); }}>
      <MessageCircleHeart size={19} aria-hidden="true"/><span>Donner mon avis</span>
    </button>

    {open && <div className="feedback-overlay" onMouseDown={() => { if (!sending) setOpen(false); }}>
      <section className="feedback-dialog" role="dialog" aria-modal="true" aria-labelledby={headingId} onMouseDown={(event) => event.stopPropagation()}>
        <div className="feedback-dialog-top">
          <div className="feedback-dialog-icon"><MessageCircleHeart size={23} /></div>
          <button type="button" className="feedback-close" onClick={() => setOpen(false)} aria-label="Fermer le formulaire"><X size={20} /></button>
        </div>
        {status === 'sent' ? <div className="feedback-done" role="status">
          <CheckCircle2 size={46} />
          <h2 id={headingId}>Merci pour ton retour !</h2>
          <p>Ton message a bien été reçu. Il sera lu pour améliorer ExoDéclic.</p>
          <button type="button" className="primary" onClick={() => setOpen(false)}>Fermer</button>
        </div> : <>
          <h2 id={headingId}>Aide-nous à améliorer ExoDéclic</h2>
          <p className="feedback-intro">Une remarque, une idée ou une erreur repérée ? Dis-nous ce que tu en penses.</p>
          <form onSubmit={submit} className="feedback-form">
            <label htmlFor="feedback-type">Quel type de retour ? <span aria-hidden="true">*</span></label>
            <select id="feedback-type" value={form.category} required onChange={event => setForm(current => ({ ...current, category: event.target.value }))}>
              <option value="">Choisir une catégorie…</option>
              {types.map(([value, emoji, label]) => <option key={value} value={value}>{emoji} {label}</option>)}
            </select>
            <fieldset className="feedback-rating">
              <legend>Quelle note donnerais-tu au site ? <small>(facultatif)</small></legend>
              <div className="feedback-stars" aria-label="Note sur 5 étoiles">
                {[1, 2, 3, 4, 5].map(value => <button type="button" key={value} className={value <= form.rating ? 'selected' : ''}
                  aria-label={`${value} étoile${value > 1 ? 's' : ''}`} aria-pressed={form.rating === value}
                  onClick={() => setForm(current => ({ ...current, rating: current.rating === value ? 0 : value }))}>
                  <Star size={27} fill={value <= form.rating ? 'currentColor' : 'none'} />
                </button>)}
              </div>
            </fieldset>
            <label htmlFor="feedback-message">Ton message <span aria-hidden="true">*</span></label>
            <textarea id="feedback-message" required minLength={12} maxLength={1500} rows={5} value={form.message}
              onChange={event => setForm(current => ({ ...current, message: event.target.value }))}
              placeholder="Exemple : dans l'exercice sur Pythagore, je ne comprends pas la deuxième étape de la correction…" />
            <span className="feedback-counter">{form.message.length}/1 500 caractères</span>
            <div className="feedback-honeypot" aria-hidden="true"><label>Ne pas renseigner ce champ<input tabIndex={-1} autoComplete="off" value={form.website} onChange={event => setForm(current => ({ ...current, website: event.target.value }))} /></label></div>
            <p className="feedback-privacy">Pas besoin de compte ni d'adresse email. N'indique pas ton nom, ton numéro de téléphone ou d'autres informations personnelles. Ton message sera visible uniquement par l'administrateur.</p>
            {error && <p role="alert" className="feedback-error">{error}</p>}
            <button type="submit" className="primary feedback-submit" disabled={sending || form.message.trim().length < 12 || !form.category}>
              <Send size={17} /> {sending ? 'Envoi en cours…' : 'Envoyer mon avis'}
            </button>
          </form>
        </>}
      </section>
    </div>}
  </>;
}
