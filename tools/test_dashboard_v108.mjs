/** Tests sans réseau : node --test tools/test_dashboard_v108.mjs */
import assert from 'node:assert/strict';
import test from 'node:test';
import { DECLIC_LEVELS, getDeclicProgress } from '../frontend/src/components/declicLevels.js';
import { getDashboardMission } from '../frontend/src/dashboardMission.js';

test('Déclic comporte cinq paliers croissants', () => {
  assert.deepEqual(DECLIC_LEVELS.map((item) => item.min), [0, 8, 25, 60, 120]);
  assert.deepEqual(DECLIC_LEVELS.map((item) => item.title), ['Explorateur', 'Chercheur', 'Stratège', 'Expert', 'Maître Déclic']);
});

test('progression et seuils de niveau', () => {
  const cases = [
    [0, 1, 0, 8],
    [3, 1, 38, 5],
    [7, 1, 88, 1],
    [8, 2, 0, 17],
    [24, 2, 94, 1],
    [25, 3, 0, 35],
    [59, 3, 97, 1],
    [60, 4, 0, 60],
    [119, 4, 98, 1],
    [120, 5, 100, 0],
    [200, 5, 100, 0],
  ];
  for (const [count, level, percent, remaining] of cases) {
    const result = getDeclicProgress(count);
    assert.equal(result.level, level, `niveau pour ${count}`);
    assert.equal(result.percent, percent, `pourcentage pour ${count}`);
    assert.equal(result.remaining, remaining, `restant pour ${count}`);
  }
  assert.equal(getDeclicProgress(-6).count, 0);
});

test('mission : ouverture du prochain exercice pas encore terminé', () => {
  const mission = getDashboardMission({
    total: 3, completed: 1,
    exercises: [
      { id: 24, completed: true, order: 1 },
      { id: 25, completed: false, order: 2, title: 'Fractions', subject: { name: 'Mathématiques' }, chapter: { title: 'Fractions et partage' } },
      { id: 26, completed: false, order: 3 },
    ],
  }, null);
  assert.equal(mission.url, '/exercice/25?from=seance');
  assert.equal(mission.status, 'exercise');
  assert.equal(mission.percent, 33);
  assert.equal(mission.title, 'Fractions');
  assert.match(mission.detail, /Mathématiques.*Fractions et partage/);
});

test('mission : séance terminée, proposition de chapitre disponible', () => {
  const mission = getDashboardMission({total: 2, completed: 2, exercises: [
    {id: 1, completed: true}, {id: 2, completed: true},
  ]}, {chapter_id: 9});
  assert.equal(mission.status, 'complete');
  assert.equal(mission.url, '/chapitre/9#exercices');
});

test('mission : zéro exercice, erreur API et chargement', () => {
  assert.equal(getDashboardMission({total: 0, completed: 0, exercises: []}, null).url, '/cours');
  assert.equal(getDashboardMission({error: true}, null).url, '/seance');
  assert.equal(getDashboardMission(null, null).status, 'loading');
});
