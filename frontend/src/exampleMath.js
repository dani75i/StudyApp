/** Pure formatting rules for maths inside lesson examples. No React dependency. */
export const explicitMathRegex = /(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))/g;

export function isWorkedFormula(expression) {
  const raw = String(expression || '').trim();
  return /\\frac|\\dfrac|\\sqrt|\\times|\\div|\\begin/.test(raw)
    || ((raw.includes('=') || raw.includes('\\Rightarrow')) && raw.length >= 13);
}

export function splitExampleText(text = '') {
  const fragments = String(text).split(explicitMathRegex);
  const pieces = [];
  let prose = '';
  const flush = () => {
    const cleaned = prose.trim();
    // Avoid putting a lonely full stop below a display-maths card.
    if (cleaned && !/^[.,;:!?]+$/.test(cleaned)) pieces.push({ type: 'text', value: cleaned });
    prose = '';
  };
  for (const fragment of fragments) {
    const display = fragment.startsWith('\\[') && fragment.endsWith('\\]');
    const inline = fragment.startsWith('\\(') && fragment.endsWith('\\)');
    if ((display || inline) && (display || isWorkedFormula(fragment.slice(2, -2)))) {
      flush();
      pieces.push({ type: 'formula', value: fragment.slice(2, -2) });
    } else {
      prose += fragment;
    }
  }
  flush();
  return pieces;
}
