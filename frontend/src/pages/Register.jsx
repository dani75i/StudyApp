import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle2, Zap } from 'lucide-react';
import { api } from '../api';
import { useAuth } from '../App';
import { appBadges } from '../subjectMeta';
import { openCookiePreferences, trackEvent } from '../analytics';

const levels = ['6e', '5e', '4e', '3e', '2nde', '1re', 'Terminale'];

export default function Register() {
  const [form, setForm] = useState({ first_name: '', email: '', password: '', level: '3e' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [startedTracked, setStartedTracked] = useState(false);
  const { setUser } = useAuth();

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError('');
    try {
      const user = await api('/auth/register', { method: 'POST', body: JSON.stringify(form) });
      setUser(user);
      trackEvent('sign_up', { method: 'email' });
      window.location.assign('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-visual register-visual">
        <div className="auth-copy">
          <span className="eyebrow">TON PARCOURS, TON RYTHME</span>
          <h1>Crée ton espace pour progresser en maths et en physique.</h1>
          <p>Ton compte conserve tes exercices, tes réussites et les chapitres à retravailler.</p>
          {['Progression par chapitre', 'Corrections détaillées', 'Historique personnel'].map((item) => <div className="benefit" key={item}><CheckCircle2 size={19} />{item}</div>)}
          <div className="badge-grid compact">
            {appBadges.map(({ icon: Icon, title, text }) => (
              <div className="info-badge" key={title}><Icon size={18} /><div><strong>{title}</strong><small>{text}</small></div></div>
            ))}
          </div>
        </div>
      </div>

      <div className="auth-panel">
        <form className="auth-card" onSubmit={submit} onFocus={() => { if (!startedTracked) { trackEvent('sign_up_started'); setStartedTracked(true); } }}>
          <div className="brand auth-brand"><span className="brand-mark"><Zap size={20} /></span><span>StudySprint</span></div>
          <h2>Créer mon compte</h2>
          <p className="muted">Tu pourras tester l'application comme un vrai élève.</p>
          {error && <div className="alert error">{error}</div>}
          <div className="form-grid">
            <label>Prénom<input required value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} placeholder="Daniel" /></label>
            <label>Classe<select value={form.level} onChange={(e) => setForm({ ...form, level: e.target.value })}>{levels.map((level) => <option key={level}>{level}</option>)}</select></label>
          </div>
          <label>Email<input type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="eleve@email.fr" /></label>
          <label>Mot de passe<input type="password" minLength="8" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="8 caractères minimum" /></label>
          <button className="primary" disabled={busy}>{busy ? 'Création…' : 'Créer mon espace'}</button>
          <p className="auth-switch">Déjà inscrit ? <Link to="/connexion">Se connecter</Link></p>
          <p className="auth-legal"><Link to="/confidentialite">Confidentialité</Link><span>•</span><button type="button" onClick={openCookiePreferences}>Gérer les cookies</button></p>
        </form>
      </div>
    </div>
  );
}
