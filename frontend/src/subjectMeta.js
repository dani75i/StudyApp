import { Atom, Calculator, Sigma, Zap } from 'lucide-react';

export const subjectMeta = {
  mathematiques: { icon: Calculator, accent: 'math', label: 'Mathématiques' },
  'physique-chimie': { icon: Atom, accent: 'physics', label: 'Physique-Chimie' },
};

export function getSubjectMeta(slug) {
  return subjectMeta[slug] || { icon: Sigma, accent: 'generic', label: slug };
}

export const appBadges = [
  { icon: Calculator, title: 'Maths', text: 'Calcul, fonctions, géométrie et résolution.' },
  { icon: Atom, title: 'Physique', text: 'Énergie, électricité et phénomènes du quotidien.' },
  { icon: Zap, title: 'Progression', text: 'Un suivi simple de tes chapitres maîtrisés.' },
];
