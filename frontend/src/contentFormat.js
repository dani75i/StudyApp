export const LESSON_BLOCKS_PREFIX = '@@studysprint-blocks@@';

export const emptyLessonBlocks = () => ([
  { type: 'paragraph', content: '' },
]);

const sentenceSplit = /(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Ý0-9])|;\s+/u;

function formulaCandidate(value) {
  const trimmed = String(value || '').replace(/[.!?]+$/, '').trim();
  // Ne JAMAIS faire passer une phrase contenant une équation pour une formule.
  // C'était la cause des mots collés : « Pour a non nul, a^0=1 ».
  if (!trimmed || trimmed.length > 110 || !/[=≈×]/.test(trimmed)) return null;
  if (/[,;:]\s+|\b(pour|avec|sur|on|est|sont|soit|si|alors|donc|dans|une|un|la|le|les)\b/i.test(trimmed)) return null;
  if ((trimmed.match(/[A-Za-zÀ-ÿ]{4,}/g) || []).some((word) => !['sin', 'cos', 'tan', 'frac', 'sqrt', 'times', 'text'].includes(word.toLowerCase()))) return null;
  return trimmed;
}

function legacyPartToBlocks(content) {
  const clean = String(content || '').trim();
  if (!clean) return [];

  const colonMatch = clean.match(/^([^:]{2,70}):\s*(.+)$/u);
  if (colonMatch) {
    const formula = formulaCandidate(colonMatch[2]);
    if (formula) {
      return [
        { type: 'paragraph', content: `${colonMatch[1].trim()} :` },
        { type: 'formula', content: formula.replace(/\s+et\s+/g, ' \\qquad ') },
      ];
    }
  }

  const formula = formulaCandidate(clean);
  if (formula && !/\s[A-Za-zÀ-ÿ]{4,}\s/u.test(formula)) {
    return [{ type: 'formula', content: formula.replace(/\s+et\s+/g, ' \\qquad ') }];
  }

  return [{ type: 'paragraph', content: clean }];
}

export function legacyLessonToBlocks(body = '') {
  const clean = String(body || '').trim();
  if (!clean) return emptyLessonBlocks();

  // Fiches historiques 3e corrigées à l'affichage : aucune écriture en base,
  // les modifications faites ensuite dans /admin restent prioritaires.
  if (clean.startsWith('Pour n entier positif, a^n est le produit')) {
    return [
      { type: 'paragraph', content: 'Pour un entier positif n, la puissance aⁿ est le produit de n facteurs égaux à a.' },
      { type: 'formula', content: String.raw`a^n=\underbrace{a\times a\times\cdots\times a}_{n\text{ facteurs}}` },
      { type: 'note', content: 'Pour tout nombre a non nul, a⁰ = 1. Exemple : 7⁰ = 1.' },
    ];
  }
  if (clean.startsWith('Pour une même base : a^m×a^n=')) {
    return [
      { type: 'paragraph', content: 'Pour multiplier deux puissances de même base, on additionne les exposants.' },
      { type: 'formula', content: String.raw`a^m\times a^n=a^{m+n}` },
      { type: 'paragraph', content: 'Pour diviser deux puissances de même base non nulle, on soustrait les exposants.' },
      { type: 'formula', content: String.raw`\frac{a^m}{a^n}=a^{m-n}` },
    ];
  }
  if (clean.startsWith('Un nombre en écriture scientifique s')) {
    return [
      { type: 'paragraph', content: 'L’écriture scientifique d’un nombre s’obtient en écrivant un facteur décimal compris entre 1 (inclus) et 10 (exclu), multiplié par une puissance de dix.' },
      { type: 'formula', content: String.raw`a\times10^n\qquad 1\leqslant a<10` },
      { type: 'note', content: 'Exemple : 45 000 = 4,5 × 10⁴.' },
    ];
  }
  if (clean.startsWith("Dans un triangle rectangle, le carré de l'hypoténuse")) {
    return [
      { type: 'paragraph', content: 'Dans un triangle ABC rectangle en A, le côté BC est l’hypoténuse : il se trouve en face de l’angle droit.' },
      { type: 'formula', content: String.raw`BC^2=AB^2+AC^2` },
      { type: 'note', content: 'Repère toujours le sommet de l’angle droit avant d’appliquer le théorème.' },
    ];
  }
  if (clean.startsWith('Hypoténuse : addition des carrés puis racine.')) {
    return [
      { type: 'paragraph', content: 'Dans ABC rectangle en A, BC est l’hypoténuse, car BC est opposé à l’angle droit.' },
      { type: 'paragraph', content: 'Pour calculer l’hypoténuse, additionne les carrés des deux côtés de l’angle droit.' },
      { type: 'formula', content: String.raw`BC=\sqrt{AB^2+AC^2}` },
      { type: 'paragraph', content: 'Pour retrouver un côté de l’angle droit, soustrais son autre carré de celui de l’hypoténuse.' },
      { type: 'formula', content: String.raw`AB=\sqrt{BC^2-AC^2}` },
    ];
  }
  if (clean.startsWith('P=m×g. Sur Terre')) {
    return [
      { type: 'paragraph', content: 'Le poids est la force de gravitation exercée sur un objet de masse m.' },
      { type: 'formula', content: String.raw`P=m\times g` },
      { type: 'list', items: ['P : poids, exprimé en newtons (N).', 'm : masse, exprimée en kilogrammes (kg).', 'g : intensité de la pesanteur, exprimée en N/kg.'] },
      { type: 'note', content: 'Sur Terre, g ≈ 9,8 N/kg, souvent arrondi à 10 N/kg au collège.' },
    ];
  }

  // Ancienne fiche : éviter de rendre des mots comme « opposé/hypoténuse »
  // sous forme d'une fraction illisible sans angle de référence.
  if (/\bsin\s*=\s*oppos[ée]/i.test(clean) && /\bcos\s*=/i.test(clean)) {
    return [
      { type: 'paragraph', content: 'Dans un triangle rectangle, choisis un angle aigu α. Les trois rapports trigonométriques sont :' },
      { type: 'formula', content: String.raw`\sin(\alpha)=\frac{\text{côté opposé}}{\text{hypoténuse}}` },
      { type: 'formula', content: String.raw`\cos(\alpha)=\frac{\text{côté adjacent}}{\text{hypoténuse}}` },
      { type: 'formula', content: String.raw`\tan(\alpha)=\frac{\text{côté opposé}}{\text{côté adjacent}}` },
      { type: 'note', content: 'L’hypoténuse est le côté le plus long, situé en face de l’angle droit. Le côté opposé et le côté adjacent dépendent de l’angle α choisi.' },
    ];
  }

  return clean
    .split(/\n{2,}|\n/)
    .flatMap((part) => part.split(sentenceSplit))
    .flatMap(legacyPartToBlocks)
    .filter(Boolean);
}

export function parseLessonBlocks(body = '') {
  const raw = String(body || '');
  if (!raw.startsWith(LESSON_BLOCKS_PREFIX)) return legacyLessonToBlocks(raw);
  try {
    const blocks = JSON.parse(raw.slice(LESSON_BLOCKS_PREFIX.length));
    return Array.isArray(blocks) && blocks.length ? blocks : emptyLessonBlocks();
  } catch {
    return legacyLessonToBlocks(raw);
  }
}

export function serializeLessonBlocks(blocks = []) {
  const normalized = blocks
    .map((block) => {
      if (block.type === 'list') {
        return {
          type: 'list',
          items: (block.items || []).map((item) => String(item).trim()).filter(Boolean),
        };
      }
      return {
        type: block.type || 'paragraph',
        content: String(block.content || '').trim(),
      };
    })
    .filter((block) => block.type === 'list' ? block.items.length : block.content);

  return `${LESSON_BLOCKS_PREFIX}${JSON.stringify(normalized.length ? normalized : emptyLessonBlocks())}`;
}

export function lessonPreview(body = '') {
  return parseLessonBlocks(body)
    .map((block) => block.type === 'list' ? (block.items || []).join(' • ') : block.content)
    .filter(Boolean)
    .join(' ');
}

export function insertSnippet(value = '', snippet = '') {
  const base = String(value || '');
  const separator = base && !/[\s\n]$/.test(base) ? ' ' : '';
  return `${base}${separator}${snippet}`;
}
