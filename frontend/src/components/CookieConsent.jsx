import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  acceptAnalytics,
  disableAnalyticsRuntime,
  enableAnalyticsForPublicPages,
  getAnalyticsConsent,
  isAnalyticsAllowedPath,
  rejectAnalytics,
  trackPageView,
} from '../analytics';

export default function CookieConsent() {
  const location = useLocation();
  const [consent, setConsent] = useState(() => getAnalyticsConsent());
  const [visible, setVisible] = useState(() => getAnalyticsConsent() === null);

  useEffect(() => {
    const open = () => setVisible(true);
    const changed = (event) => setConsent(event.detail);
    window.addEventListener('studysprint:open-cookie-preferences', open);
    window.addEventListener('studysprint:analytics-consent-changed', changed);
    return () => {
      window.removeEventListener('studysprint:open-cookie-preferences', open);
      window.removeEventListener('studysprint:analytics-consent-changed', changed);
    };
  }, []);

  useEffect(() => {
    if (consent === 'accepted' && isAnalyticsAllowedPath(location.pathname)) {
      enableAnalyticsForPublicPages();
      const timer = window.setTimeout(() => trackPageView(location.pathname), 0);
      return () => window.clearTimeout(timer);
    }
    disableAnalyticsRuntime();
    return undefined;
  }, [consent, location.pathname, location.search]);

  const accept = () => {
    acceptAnalytics();
    setConsent('accepted');
    setVisible(false);
    if (isAnalyticsAllowedPath(location.pathname)) {
      window.setTimeout(() => trackPageView(location.pathname), 0);
    }
  };

  const reject = () => {
    rejectAnalytics();
    setConsent('rejected');
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div className="cookie-consent" role="dialog" aria-live="polite" aria-label="Préférences de mesure d'audience">
      <div className="cookie-consent-copy">
        <strong>Statistiques de fréquentation</strong>
        <p>
          Avec ton accord, ExoDéclic utilise Google Analytics uniquement sur les pages publiques et d'accès
          pour comprendre le trafic et améliorer le site. Aucun prénom, email ou réponse d'exercice n'est envoyé à Google.
        </p>
        <p className="cookie-minor-note">Si tu as moins de 15 ans, demande l'accord d'un parent avant d'accepter.</p>
        <Link to="/confidentialite">En savoir plus</Link>
      </div>
      <div className="cookie-consent-actions">
        <button type="button" className="cookie-choice" onClick={reject}>Tout refuser</button>
        <button type="button" className="cookie-choice" onClick={accept}>Accepter les statistiques</button>
        {consent !== null && <button type="button" className="cookie-close" onClick={() => setVisible(false)}>Fermer</button>}
      </div>
    </div>
  );
}
