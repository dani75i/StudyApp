const PHYSICS_ILLUSTRATIONS = {
  'Atomes, ions et molécules': '/illustrations/physics/atomes-ions-molecules.png',
  'Transformations chimiques et conservation': '/illustrations/physics/transformations-chimiques.png',
  'Acides, bases et pH': '/illustrations/physics/acides-bases-ph.png',
  'Mouvement et vitesse': '/illustrations/physics/mouvement-vitesse.png',
  'Forces, poids et gravitation': '/illustrations/physics/forces-gravitation.png',
  'Énergie, puissance et conversions': '/illustrations/physics/energie-conversions.png',
  'Circuits électriques : tension et intensité': '/illustrations/physics/circuits-electriques.png',
  'Loi d’Ohm et puissance électrique': '/illustrations/physics/loi-ohm.png',
  'Signaux sonores et lumineux': '/illustrations/physics/signaux-sonores-lumineux.png',
  'Univers, gravitation et ordres de grandeur': '/illustrations/physics/univers-gravitation.png',
};

export function getChapterIllustration({ subjectSlug, title }) {
  if (subjectSlug !== 'physique-chimie') return null;
  return PHYSICS_ILLUSTRATIONS[title] || null;
}
