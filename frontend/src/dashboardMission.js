/** Le prochain exercice de la séance du jour est établi par l'API.
 * Ne jamais fabriquer un numéro d'exercice en fonction d'une progression globale.
 */
export function getDashboardMission(session, recommended) {
  if (!session) {
    return {
      status: 'loading',
      title: 'Ta séance se prépare…',
      detail: 'Retrouve ta sélection d’exercices du jour.',
      meta: 'OBJECTIF DU JOUR',
      action: 'Voir ma séance',
      url: '/seance',
      percent: 0,
    };
  }

  if (session.error) {
    return {
      status: 'fallback',
      title: 'Prêt pour une nouvelle séance ?',
      detail: 'Retrouve tes exercices sélectionnés pour avancer à ton rythme.',
      meta: 'TON PROGRAMME',
      action: 'Voir ma séance',
      url: '/seance',
      percent: 0,
    };
  }

  const total = Math.max(0, Number(session.total) || 0);
  const completed = Math.max(0, Math.min(total, Number(session.completed) || 0));
  const percent = total ? Math.round(completed / total * 100) : 0;
  const next = session.exercises?.find((exercise) => !exercise.completed);

  if (next && Number.isInteger(next.id) && next.id > 0) {
    return {
      status: 'exercise',
      title: next.title,
      detail: `${next.subject?.name || 'Exercice'} • ${next.chapter?.title || 'Ta séance'}`,
      meta: `EXERCICE ${next.order} SUR ${total} · ${completed} TERMINÉ${completed > 1 ? 'S' : ''}`,
      action: 'Faire cet exercice',
      url: `/exercice/${next.id}?from=seance`,
      percent,
    };
  }

  if (total && completed >= total) {
    return {
      status: 'complete',
      title: 'Séance du jour terminée !',
      detail: `Tu as terminé ${total} exercice${total > 1 ? 's' : ''}. Déclic est fier de toi !`,
      meta: 'MISSION ACCOMPLIE',
      action: recommended ? 'Explorer un autre chapitre' : 'Revoir mes cours',
      url: recommended ? `/chapitre/${recommended.chapter_id}#exercices` : '/cours',
      percent: 100,
    };
  }

  return {
    status: 'empty',
    title: 'Découvre une nouvelle notion',
    detail: 'Tes exercices seront proposés dès qu’une séance sera disponible.',
    meta: 'À TON RYTHME',
    action: 'Parcourir les cours',
    url: '/cours',
    percent: 0,
  };
}
