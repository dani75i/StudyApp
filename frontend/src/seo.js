// Keep metadata in sync on React Router navigation, not only on HTTP reload.
// The backend independently renders SEO metadata for first HTTP responses.
const ORIGIN = 'https://www.exodeclic.fr';
const PUBLIC = /^\/$|^\/decouvrir\/cours(?:\/\d+)?\/?$|^\/confidentialite\/?$/;

function updateMeta(selector, attribute, value, name) {
  let tag = document.querySelector(selector);
  if (!tag && name) {
    tag = document.createElement('meta');
    tag.setAttribute(attribute, name);
    document.head.appendChild(tag);
  }
  if (tag) tag.setAttribute('content', value);
}

export function setPageSeo({ title, description, pathname = window.location.pathname }) {
  const path = pathname === '/' ? '/' : pathname.replace(/\/$/, '');
  const allowed = PUBLIC.test(path);
  document.title = title;
  updateMeta('meta[name="description"]', 'name', description, 'description');
  updateMeta('meta[name="robots"]', 'name', allowed ? 'index,follow' : 'noindex,nofollow', 'robots');
  updateMeta('meta[property="og:title"]', 'property', title, 'og:title');
  updateMeta('meta[property="og:description"]', 'property', description, 'og:description');
  const previousCanonical = document.querySelector('link[rel="canonical"]');
  const previousUrl = document.querySelector('meta[property="og:url"]');
  if (!allowed) {
    previousCanonical?.remove();
    previousUrl?.remove();
    return;
  }
  const url = `${ORIGIN}${path}`;
  const canonical = previousCanonical || document.createElement('link');
  canonical.setAttribute('rel', 'canonical');
  canonical.setAttribute('href', url);
  if (!previousCanonical) document.head.appendChild(canonical);
  updateMeta('meta[property="og:url"]', 'property', url, 'og:url');
}

export function updateRouteSeo(pathname) {
  if (PUBLIC.test(pathname)) return;
  setPageSeo({
    title: 'Espace élève | ExoDéclic',
    description: 'Espace personnel ExoDéclic : exercices, cours et progression.',
    pathname,
  });
}
