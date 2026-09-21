import React from 'react';
import katex from 'katex';
import { Lightbulb, BookOpen } from 'lucide-react';
import { parseLessonBlocks } from '../contentFormat';

function latexify(expression = '') {
  const raw = String(expression).trim();
  // Les formules déjà écrites en LaTeX (
  // \frac, \sin, \text, etc.) sont conservées telles quelles.
  if (raw.includes('\\')) return raw;
  return raw
    .replace(/−/g, '-')
    .replace(/×/g, '\\times ')
    .replace(/≈/g, '\\approx ')
    .replace(/≤/g, '\\le ')
    .replace(/≥/g, '\\ge ')
    .replace(/π/g, '\\pi ')
    .replace(/²/g, '^{2}')
    .replace(/³/g, '^{3}')
    .replace(/\^\(([^)]+)\)/g, '^{$1}')
    .replace(/√\s*([A-Za-z0-9]+)/g, '\\sqrt{$1}');
}

function unwrapMathDelimiters(expression = '') {
  const raw = String(expression).trim();
  if (raw.startsWith('\\[') && raw.endsWith('\\]')) return raw.slice(2, -2).trim();
  if (raw.startsWith('\\(') && raw.endsWith('\\)')) return raw.slice(2, -2).trim();
  if (raw.startsWith('$') && raw.endsWith('$')) return raw.slice(1, -1).trim();
  return raw;
}

function renderKatex(expression, displayMode = false) {
  try {
    return katex.renderToString(latexify(unwrapMathDelimiters(expression)), {
      throwOnError: false,
      displayMode,
      strict: 'ignore',
      output: 'html',
    });
  } catch {
    return expression;
  }
}

const explicitMathRegex = /(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))/g;
// Conservative auto-format: match only actual short mathematical expressions.
// Never swallow ordinary French words next to an exponent such as « Pour a non nul ».
const autoMathRegex = /([A-Za-z](?:\([A-Za-z0-9+\-]+\))?|[0-9]+(?:[.,][0-9]+)?)(?:\^\([A-Za-z0-9+\-]+\)|\^[A-Za-z0-9+\-]+|[²³])?(?:\s*[=≈×]\s*(?:[A-Za-z](?:\([A-Za-z0-9+\-]+\))?|[0-9]+(?:[.,][0-9]+)?)(?:\^\([A-Za-z0-9+\-]+\)|\^[A-Za-z0-9+\-]+|[²³])?)+|\b[A-Za-z]\^(?:\([A-Za-z0-9+\-]+\)|[A-Za-z0-9+\-]+)|\b[A-Z]{2}[²³]/g;

function AutoMathText({ text }) {
  const source = String(text || '');
  const parts = [];
  let lastIndex = 0;
  for (const match of source.matchAll(autoMathRegex)) {
    if (match.index > lastIndex) parts.push(source.slice(lastIndex, match.index));
    parts.push(<span key={match.index} className="inline-math" dangerouslySetInnerHTML={{ __html: renderKatex(match[0], false) }} />);
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < source.length) parts.push(source.slice(lastIndex));
  return <>{parts}</>;
}

export function RichText({ text = '' }) {
  const chunks = String(text || '').split(explicitMathRegex);
  return chunks.map((chunk, index) => {
    if (!chunk) return null;
    if (chunk.startsWith('\\[') && chunk.endsWith('\\]')) {
      return <span key={index} className="display-math" dangerouslySetInnerHTML={{ __html: renderKatex(chunk.slice(2, -2), true) }} />;
    }
    if (chunk.startsWith('\\(') && chunk.endsWith('\\)')) {
      return <span key={index} className="inline-math" dangerouslySetInnerHTML={{ __html: renderKatex(chunk.slice(2, -2), false) }} />;
    }
    return <AutoMathText key={index} text={chunk} />;
  });
}

export function Formula({ value = '' }) {
  return <div className="formula-block" dangerouslySetInnerHTML={{ __html: renderKatex(value, true) }} />;
}

export function LessonContent({ body = '' }) {
  const blocks = parseLessonBlocks(body);

  return (
    <div className="lesson-content">
      {blocks.map((block, index) => {
        if (block.type === 'formula') return <Formula key={index} value={block.content} />;
        if (block.type === 'list') {
          return (
            <ul key={index} className="lesson-bullet-list">
              {(block.items || []).map((item, itemIndex) => <li key={itemIndex}><RichText text={item} /></li>)}
            </ul>
          );
        }
        if (block.type === 'note') {
          return (
            <aside key={index} className="lesson-note">
              <Lightbulb size={18} />
              <div><strong>À retenir</strong><p><RichText text={block.content} /></p></div>
            </aside>
          );
        }
        if (block.type === 'example') {
          return (
            <aside key={index} className="lesson-example">
              <BookOpen size={18} />
              <div className="lesson-example-copy">
                <strong>Exemple</strong>
                <div className="lesson-example-body"><RichText text={block.content} /></div>
              </div>
            </aside>
          );
        }
        return <p key={index}><RichText text={block.content} /></p>;
      })}
    </div>
  );
}
