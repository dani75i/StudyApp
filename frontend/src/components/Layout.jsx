import React, { useState } from 'react';
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import {
  BookOpenText, ChartNoAxesColumnIncreasing, Clock3, LogOut, MoonStar,
  SunMedium, UserRound, Zap, Dumbbell, Sparkles, ShieldCheck, Award,
  House, Ellipsis, X,
} from 'lucide-react';
import { api } from '../api';
import { useAuth, useTheme } from '../App';
import { openCookiePreferences } from '../analytics';

const navItems = [
  ['/dashboard', ChartNoAxesColumnIncreasing, 'Progression'],
  ['/seance', Sparkles, 'Séance du jour'],
  ['/cours', BookOpenText, 'Cours'],
  ['/exercices', Dumbbell, 'Exercices'],
  ['/historique', Clock3, 'Historique'],
  ['/recompenses', Award, 'Récompenses'],
  ['/profil', UserRound, 'Profil'],
];

const mobileItems = [
  ['/dashboard', House, 'Accueil'],
  ['/cours', BookOpenText, 'Cours'],
  ['/exercices', Dumbbell, 'Exercices'],
  ['/recompenses', Award, 'Badges'],
];

export default function Layout() {
  const { user, setUser } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const nav = useNavigate();
  const location = useLocation();
  const [moreOpen, setMoreOpen] = useState(false);

  const logout = async () => {
    await api('/auth/logout', { method: 'POST' });
    setUser(null);
    setMoreOpen(false);
    nav('/connexion');
  };

  const items = [
    ...navItems,
    ...(user?.role === 'admin' ? [['/admin', ShieldCheck, 'Admin']] : []),
  ];
  const moreActive = ['/seance', '/historique', '/profil', '/admin'].some((route) => location.pathname.startsWith(route));

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-row">
          <div className="brand"><span className="brand-mark"><Zap size={21} /></span><span>ExoDéclic</span></div>
          <button className="theme-toggle" onClick={toggleTheme} title="Changer de thème" aria-label="Changer de thème">
            {theme === 'dark' ? <SunMedium size={18} /> : <MoonStar size={18} />}
          </button>
        </div>
        <div className="sidebar-tag">Maths & physique pour progresser pas à pas</div>
        <nav aria-label="Navigation principale">
          {items.map(([to, Icon, label]) => (
            <NavLink key={to} to={to} end className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              <Icon size={19} /><span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-user">
          <div className="avatar">{user?.first_name?.[0]?.toUpperCase()}</div>
          <div><strong>{user?.first_name}</strong><span>{user?.level}</span></div>
          <button onClick={logout} title="Se déconnecter" aria-label="Se déconnecter"><LogOut size={18} /></button>
        </div>
        <div className="sidebar-legal"><NavLink to="/confidentialite">Confidentialité</NavLink><button type="button" onClick={openCookiePreferences}>Cookies</button></div>
      </aside>

      <header className="mobile-app-header">
        <NavLink className="brand" to="/dashboard"><span className="brand-mark"><Zap size={20} /></span><span>ExoDéclic</span></NavLink>
        <button className="theme-toggle" onClick={toggleTheme} aria-label="Changer de thème" title="Changer de thème">
          {theme === 'dark' ? <SunMedium size={19} /> : <MoonStar size={19} />}
        </button>
      </header>

      <main className="main"><Outlet /></main>

      <nav className="mobile-bottom-nav" aria-label="Navigation mobile">
        {mobileItems.map(([to, Icon, label]) => (
          <NavLink
            key={to}
            to={to}
            end={false}
            className={({ isActive }) => `mobile-bottom-link ${isActive || (to === '/exercices' && location.pathname.startsWith('/exercice/')) || (to === '/cours' && location.pathname.startsWith('/chapitre/')) ? 'active' : ''}`}
            onClick={() => setMoreOpen(false)}
          >
            <Icon size={21} /><span>{label}</span>
          </NavLink>
        ))}
        <button type="button" className={`mobile-bottom-link ${moreOpen || moreActive ? 'active' : ''}`} onClick={() => setMoreOpen((open) => !open)} aria-label="Plus de pages" aria-expanded={moreOpen}>
          <Ellipsis size={22} /><span>Plus</span>
        </button>
      </nav>

      {moreOpen && <>
        <button type="button" className="mobile-more-backdrop" onClick={() => setMoreOpen(false)} aria-label="Fermer le menu" />
        <div className="mobile-more-sheet" role="dialog" aria-label="Autres pages">
          <div className="mobile-more-head"><strong>Mon espace</strong><button type="button" onClick={() => setMoreOpen(false)} aria-label="Fermer"><X size={20} /></button></div>
          <div className="mobile-more-grid">
            {items.filter(([to]) => !mobileItems.some(([mobileTo]) => mobileTo === to)).map(([to, Icon, label]) => (
              <NavLink key={to} to={to} onClick={() => setMoreOpen(false)}><Icon size={19} />{label}</NavLink>
            ))}
            <NavLink to="/confidentialite" onClick={() => setMoreOpen(false)}><ShieldCheck size={19} />Confidentialité</NavLink>
            <button onClick={() => { setMoreOpen(false); openCookiePreferences(); }}>Préférences cookies</button>
            <button onClick={logout}><LogOut size={19} />Déconnexion</button>
          </div>
        </div>
      </>}
    </div>
  );
}
