export const LESSON_BLOCKS_PREFIX = '@@studysprint-blocks@@';

export const emptyLessonBlocks = () => ([
  { type: 'paragraph', content: '' },
]);

const sentenceSplit = /(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Ý0-9])|;\s+/u;

function formulaCandidate(value) {
  const trimmed = String(value || '').replace(/[.!?]+$/, '').trim();
  const words = trimmed.match(/\p{L}+/gu) || [];
  const hasMath = /[=≈×/^²³√]/.test(trimmed);
  const mostlySymbols = words.length > 0 && words.filter((word) => word.length > 3).length <= 1;
  return hasMath && mostlySymbols && trimmed.length <= 110 ? trimmed : null;
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
