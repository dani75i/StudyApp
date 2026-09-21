/** Présentation : ne modifie ni le calcul ni la réponse validée par le serveur. */
export function correctionToSteps(steps = [], correction = '') {
  if (Array.isArray(steps) && steps.some((step) => String(step || '').trim())) {
    return steps.map((step) => String(step || '').trim()).filter(Boolean);
  }
  const original = String(correction || '').trim();
  if (!original) return ['Relis l’énoncé et reprends le raisonnement.'];
  // Les délimiteurs LaTeX sont atomiques : on ne coupe jamais une expression entre ses accolades.
  const parts = original.split(/(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))/g);
  const result = [];
  for (const part of parts) {
    if (!part) continue;
    if (/^\\\[|^\\\(/.test(part)) { result.push(part.trim()); continue; }
    result.push(...part.split(/(?:\r?\n+|;\s*|,\s+(?=donc\b)|\.\s+(?=[A-ZÀ-ÖØ-Ý]))/u)
      .map((item) => item.trim()).filter(Boolean));
  }
  return result.length ? result : [original];
}
