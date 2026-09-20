import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { updateRouteSeo } from './seo';
import { api } from './api';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Catalog from './pages/Catalog';
import ExercisesLibrary from './pages/ExercisesLibrary';
import DailySession from './pages/DailySession';
import Chapter from './pages/Chapter';
import Exercise from './pages/Exercise';
import ExerciseCorrection from './pages/ExerciseCorrection';
import SessionRecap from './pages/SessionRecap';
import History from './pages/History';
import Profile from './pages/Profile';
import Rewards from './pages/Rewards';
import Admin from './pages/Admin';
import PublicHome from './pages/PublicHome';
import PublicCourses from './pages/PublicCourses';
import PublicChapter from './pages/PublicChapter';
import Privacy from './pages/Privacy';
import CookieConsent from './components/CookieConsent';
import FeedbackWidget from './components/FeedbackWidget';
import AdminFeedback from './pages/AdminFeedback';

const AuthContext = createContext(null);
const ThemeContext = createContext(null);

export const useAuth = () => useContext(AuthContext);
export const useTheme = () => useContext(ThemeContext);

function Protected({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="screen-center"><div className="loader" /></div>;
  return user ? children : <Navigate to="/connexion" replace />;
}

function AdminOnly({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="screen-center"><div className="loader" /></div>;
  return user?.role === 'admin' ? children : <Navigate to="/dashboard" replace />;
}

function HardRedirect({ to }) {
  useEffect(() => { window.location.replace(to); }, [to]);
  return <div className="screen-center"><div className="loader" /></div>;
}

function GuestOnly({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="screen-center"><div className="loader" /></div>;
  return user ? <HardRedirect to="/dashboard" /> : children;
}

export default function App() {
  const { pathname } = useLocation();
  useEffect(() => { updateRouteSeo(pathname); }, [pathname]);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState(() => localStorage.getItem('studysprint-theme') || 'light');

  const refreshUser = async () => {
    try {
      setUser(await api('/auth/me'));
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { refreshUser(); }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('studysprint-theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme((current) => (current === 'dark' ? 'light' : 'dark'));
  const authValue = useMemo(() => ({ user, setUser, loading, refreshUser }), [user, loading]);
  const themeValue = useMemo(() => ({ theme, toggleTheme }), [theme]);

  return (
    <ThemeContext.Provider value={themeValue}>
      <AuthContext.Provider value={authValue}>
        <Routes>
          <Route path="/" element={<PublicHome />} />
          <Route path="/decouvrir/cours" element={<PublicCourses />} />
          <Route path="/decouvrir/cours/:id" element={<PublicChapter />} />
          <Route path="/confidentialite" element={<Privacy />} />
          <Route path="/connexion" element={<GuestOnly><Login /></GuestOnly>} />
          <Route path="/inscription" element={<GuestOnly><Register /></GuestOnly>} />

          <Route element={<Protected><Layout /></Protected>}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/cours" element={<Catalog />} />
            <Route path="/exercices" element={<ExercisesLibrary />} />
            <Route path="/seance" element={<DailySession />} />
            <Route path="/chapitre/:id" element={<Chapter />} />
            <Route path="/exercice/:id" element={<Exercise />} />
            <Route path="/exercice/:id/correction" element={<ExerciseCorrection />} />
            <Route path="/seance/bilan" element={<SessionRecap />} />
            <Route path="/historique" element={<History />} />
            <Route path="/profil" element={<Profile />} />
            <Route path="/recompenses" element={<Rewards />} />
            <Route path="/admin" element={<AdminOnly><Admin /></AdminOnly>} />
            <Route path="/admin/avis" element={<AdminOnly><AdminFeedback /></AdminOnly>} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <FeedbackWidget />
        <CookieConsent />
      </AuthContext.Provider>
    </ThemeContext.Provider>
  );
}
