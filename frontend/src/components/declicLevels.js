/** Progression fondée sur les exercices distincts maîtrisés, fournie par /api/dashboard.
 * Aucun XP artificiel : une nouvelle tentative sur un exercice déjà réussi
 * ne fait pas monter le niveau.
 */
export const DECLIC_LEVELS = Object.freeze([
  { title: 'Explorateur', min: 0 },
  { title: 'Chercheur', min: 8 },
  { title: 'Stratège', min: 25 },
  { title: 'Expert', min: 60 },
  { title: 'Maître Déclic', min: 120 },
]);

export function getDeclicProgress(correctCount = 0) {
  const count = Math.max(0, Math.floor(Number(correctCount) || 0));
  const levelIndex = DECLIC_LEVELS.reduce((result, level, index) => (count >= level.min ? index : result), 0);
  const current = DECLIC_LEVELS[levelIndex];
  const next = DECLIC_LEVELS[levelIndex + 1] ?? null;
  const span = next ? next.min - current.min : 1;
  const percent = next ? Math.min(100, Math.max(0, Math.round((count - current.min) / span * 100))) : 100;
  return {
    count,
    level: levelIndex + 1,
    title: current.title,
    next,
    percent,
    remaining: next ? Math.max(0, next.min - count) : 0,
  };
}
