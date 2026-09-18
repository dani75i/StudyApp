import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { GraduationCap, Zap } from 'lucide-react';
import { api } from '../api';
import { useAuth } from '../App';
import { appBadges } from '../subjectMeta';
import { openCookiePreferences, trackEvent } from '../analytics';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const { setUser } = useAuth();

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError('');
    try {
      const user = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });
      setUser(user);
      trackEvent('login', { method: 'email' });
      window.location.assign('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-visual">
        <div className="auth-copy">
          <span className="eyebrow">APPRENDRE • S'ENTRAÎNER • PROGRESSER</span>
          <h1>Maths et physique, dans un espace simple et motivant.</h1>
          <p>Des cours clairs, des exercices corrigés et un suivi simple de ta progression.</p>
          <div className="mini-stat"><GraduationCap /><span><b>Ton espace personnel</b><small>Retrouve ton niveau, tes résultats et ta progression à chaque connexion.</small></span></div>
          <div className="badge-grid">
            {appBadges.map(({ icon: Icon, title, text }) => (
              <div className="info-badge" key={title}><Icon size={18} /><div><strong>{title}</strong><small>{text}</small></div></div>
            ))}
          </div>
        </div>
      </div>

      <div className="auth-panel">
        <form className="auth-card" onSubmit={submit}>
          <div className="brand auth-brand"><span className="brand-mark"><Zap size={20} /></span><span>StudySprint</span></div>
          <h2>Bon retour 👋</h2>
          <p className="muted">Connecte-toi pour reprendre là où tu t'es arrêté.</p>
          {error && <div className="alert error">{error}</div>}
          <label>Email<input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="eleve@email.fr" /></label>
          <label>Mot de passe<input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" /></label>
          <button className="primary" disabled={busy}>{busy ? 'Connexion…' : 'Se connecter'}</button>
          <p className="auth-switch">Pas encore de compte ? <Link to="/inscription">Créer mon compte</Link></p>
          <p className="auth-legal"><Link to="/confidentialite">Confidentialité</Link><span>•</span><button type="button" onClick={openCookiePreferences}>Gérer les cookies</button></p>
        </form>
      </div>
    </div>
  );
}
