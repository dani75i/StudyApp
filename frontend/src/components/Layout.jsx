import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  BookOpenText,
  ChartNoAxesColumnIncreasing,
  Clock3,
  LogOut,
  MoonStar,
  SunMedium,
  UserRound,
  Zap,
  Dumbbell,
  Sparkles,
  ShieldCheck,
} from 'lucide-react';
import { api } from '../api';
import { useAuth, useTheme } from '../App';
import { openCookiePreferences } from '../analytics';

export default function Layout() {
  const { user, setUser } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const nav = useNavigate();

  const logout = async () => {
    await api('/auth/logout', { method: 'POST' });
    setUser(null);
    nav('/connexion');
  };

  const items = [
    ['/dashboard', ChartNoAxesColumnIncreasing, 'Progression'],
    ['/seance', Sparkles, 'Séance du jour'],
    ['/cours', BookOpenText, 'Cours'],
    ['/exercices', Dumbbell, 'Exercices'],
    ['/historique', Clock3, 'Historique'],
    ['/profil', UserRound, 'Profil'],
    ...(user?.role === 'admin' ? [['/admin', ShieldCheck, 'Admin']] : []),
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-row">
          <div className="brand"><span className="brand-mark"><Zap size={21} /></span><span>StudySprint</span></div>
          <button className="theme-toggle" onClick={toggleTheme} title="Changer de thème">
            {theme === 'dark' ? <SunMedium size={18} /> : <MoonStar size={18} />}
          </button>
        </div>

        <div className="sidebar-tag">Maths & physique pour progresser pas à pas</div>

        <nav>
          {items.map(([to, Icon, label]) => (
            <NavLink key={to} to={to} end={to === '/dashboard'} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              <Icon size={19} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-user">
          <div className="avatar">{user?.first_name?.[0]?.toUpperCase()}</div>
          <div>
            <strong>{user?.first_name}</strong>
            <span>{user?.level}</span>
          </div>
          <button onClick={logout} title="Se déconnecter"><LogOut size={18} /></button>
        </div>
        <div className="sidebar-legal"><NavLink to="/confidentialite">Confidentialité</NavLink><button type="button" onClick={openCookiePreferences}>Cookies</button></div>
      </aside>
      <main className="main"><Outlet /></main>
    </div>
  );
}
