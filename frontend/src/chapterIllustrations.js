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

// Chaque chapitre scientifique 6e / 5e possède un visuel SVG local, distinct.
const V10_ILLUSTRATIONS = {
  '6e': {
    "Solides, liquides et gaz": '/illustrations/physics/v10/6e-01.svg',
    "La matière à l’échelle des particules": '/illustrations/physics/v10/6e-02.svg',
    "Fusion, solidification et évaporation": '/illustrations/physics/v10/6e-03.svg',
    "Mélanges homogènes et hétérogènes": '/illustrations/physics/v10/6e-04.svg',
    "Dissolution dans l’eau": '/illustrations/physics/v10/6e-05.svg',
    "Masse et volume": '/illustrations/physics/v10/6e-06.svg',
    "Décrire un mouvement": '/illustrations/physics/v10/6e-07.svg',
    "Sources et transformations d’énergie": '/illustrations/physics/v10/6e-08.svg',
    "Premiers circuits électriques": '/illustrations/physics/v10/6e-09.svg',
    "Lumière, ombres et sources": '/illustrations/physics/v10/6e-10.svg',
  },
  '5e': {
    "Séparer les mélanges": '/illustrations/physics/v10/5e-01.svg',
    "Masse, volume et masse volumique": '/illustrations/physics/v10/5e-02.svg',
    "L’air et les gaz": '/illustrations/physics/v10/5e-03.svg',
    "Transformations physiques et chimiques": '/illustrations/physics/v10/5e-04.svg',
    "Trajectoires et vitesses": '/illustrations/physics/v10/5e-05.svg',
    "Circuits en série et dérivation": '/illustrations/physics/v10/5e-06.svg',
    "Mesurer la tension et l’intensité": '/illustrations/physics/v10/5e-07.svg',
    "Conversions et transferts d’énergie": '/illustrations/physics/v10/5e-08.svg',
    "Propagation de la lumière": '/illustrations/physics/v10/5e-09.svg',
    "Sons et vibrations": '/illustrations/physics/v10/5e-10.svg',
  },
 };
export function getChapterIllustration({ subjectSlug, title, level }) {
  if (subjectSlug !== 'physique-chimie') return null;
  return V10_ILLUSTRATIONS[level]?.[title] || PHYSICS_ILLUSTRATIONS[title] || null;
}
