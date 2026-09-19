const PHYSICS_ILLUSTRATIONS = {
  'Atomes, ions et molécules': '/illustrations/physics/atomes-ions-molecules.webp',
  'Transformations chimiques et conservation': '/illustrations/physics/transformations-chimiques.webp',
  'Acides, bases et pH': '/illustrations/physics/acides-bases-ph.webp',
  'Mouvement et vitesse': '/illustrations/physics/mouvement-vitesse.webp',
  'Forces, poids et gravitation': '/illustrations/physics/forces-gravitation.webp',
  'Énergie, puissance et conversions': '/illustrations/physics/energie-conversions.webp',
  'Circuits électriques : tension et intensité': '/illustrations/physics/circuits-electriques.webp',
  'Loi d’Ohm et puissance électrique': '/illustrations/physics/loi-ohm.webp',
  'Signaux sonores et lumineux': '/illustrations/physics/signaux-sonores-lumineux.webp',
  'Univers, gravitation et ordres de grandeur': '/illustrations/physics/univers-gravitation.webp',
  // Pour la 4e, réutilisation de visuels qui représentent bien le même phénomène.
  'Mélanges, dissolution et solubilité': '/illustrations/physics/acides-bases-ph.webp',
  'Atomes, molécules et transformations chimiques': '/illustrations/physics/transformations-chimiques.webp',
  'Circuits électriques et sécurité': '/illustrations/physics/circuits-electriques.webp',
  'Tension et intensité électrique': '/illustrations/physics/circuits-electriques.webp',
  'Mouvement, trajectoire et vitesse': '/illustrations/physics/mouvement-vitesse.webp',
  'Lumière et propagation': '/illustrations/physics/signaux-sonores-lumineux.webp',
  'Son : vibration et fréquence': '/illustrations/physics/signaux-sonores-lumineux.webp',
  'Énergie, transferts et conversions': '/illustrations/physics/energie-conversions.webp',
};

export function getChapterIllustration({ subjectSlug, title }) {
  if (subjectSlug !== 'physique-chimie') return null;
  return PHYSICS_ILLUSTRATIONS[title] || null;
}
