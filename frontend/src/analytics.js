export const GA_MEASUREMENT_ID = import.meta.env.VITE_GA_MEASUREMENT_ID || 'G-KF2VQGLN8C';
export const ANALYTICS_CONSENT_KEY = 'studysprint-analytics-consent-v1';

export function getAnalyticsConsent() {
  try {
    const value = localStorage.getItem(ANALYTICS_CONSENT_KEY);
    return value === 'accepted' || value === 'rejected' ? value : null;
  } catch {
    return null;
  }
}

export function isAnalyticsAllowedPath(pathname) {
  return pathname === '/'
    || pathname === '/connexion'
    || pathname === '/inscription'
    || pathname === '/confidentialite'
    || pathname === '/decouvrir/cours'
    || pathname.startsWith('/decouvrir/cours/');
}

function ensureGtag() {
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
}

export function loadGoogleAnalytics() {
  if (typeof window === 'undefined' || getAnalyticsConsent() !== 'accepted') return;
  if (window[`ga-disable-${GA_MEASUREMENT_ID}`]) return;

  ensureGtag();

  if (!window.__studysprintGaConfigured) {
    window.gtag('consent', 'default', {
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
    });
    window.gtag('js', new Date());
    window.gtag('config', GA_MEASUREMENT_ID, {
      send_page_view: false,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });
    window.__studysprintGaConfigured = true;
  }

  if (!document.querySelector(`script[data-studysprint-ga="${GA_MEASUREMENT_ID}"]`)) {
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_MEASUREMENT_ID)}`;
    script.dataset.studysprintGa = GA_MEASUREMENT_ID;
    document.head.appendChild(script);
  }
}

export function enableAnalyticsForPublicPages() {
  if (typeof window === 'undefined') return;
  window[`ga-disable-${GA_MEASUREMENT_ID}`] = false;
  if (getAnalyticsConsent() === 'accepted') loadGoogleAnalytics();
}

export function disableAnalyticsRuntime() {
  if (typeof window === 'undefined') return;
  window[`ga-disable-${GA_MEASUREMENT_ID}`] = true;
}

function deleteGoogleAnalyticsCookies() {
  if (typeof document === 'undefined') return;
  const hostname = window.location.hostname;
  const domains = [hostname, `.${hostname}`];

  document.cookie.split(';').forEach((rawCookie) => {
    const name = rawCookie.split('=')[0].trim();
    if (!name.startsWith('_ga')) return;

    document.cookie = `${name}=; Max-Age=0; path=/; SameSite=Lax`;
    domains.forEach((domain) => {
      document.cookie = `${name}=; Max-Age=0; path=/; domain=${domain}; SameSite=Lax`;
    });
  });
}

export function acceptAnalytics() {
  localStorage.setItem(ANALYTICS_CONSENT_KEY, 'accepted');
  window[`ga-disable-${GA_MEASUREMENT_ID}`] = false;
  loadGoogleAnalytics();
  window.dispatchEvent(new CustomEvent('studysprint:analytics-consent-changed', { detail: 'accepted' }));
}

export function rejectAnalytics() {
  localStorage.setItem(ANALYTICS_CONSENT_KEY, 'rejected');
  ensureGtag();
  window.gtag('consent', 'update', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
  });
  disableAnalyticsRuntime();
  deleteGoogleAnalyticsCookies();
  window.dispatchEvent(new CustomEvent('studysprint:analytics-consent-changed', { detail: 'rejected' }));
}

export function openCookiePreferences() {
  window.dispatchEvent(new CustomEvent('studysprint:open-cookie-preferences'));
}

export function trackPageView(pathname) {
  if (getAnalyticsConsent() !== 'accepted' || !isAnalyticsAllowedPath(pathname)) return;
  enableAnalyticsForPublicPages();
  ensureGtag();
  window.gtag('event', 'page_view', {
    page_path: `${window.location.pathname}${window.location.search}`,
    page_location: window.location.href,
    page_title: document.title,
  });
}

export function trackEvent(name, params = {}) {
  if (getAnalyticsConsent() !== 'accepted') return;
  if (!isAnalyticsAllowedPath(window.location.pathname)) return;
  enableAnalyticsForPublicPages();
  ensureGtag();
  window.gtag('event', name, params);
}
