import React from 'react';
import katex from 'katex';
import { Lightbulb } from 'lucide-react';
import { parseLessonBlocks } from '../contentFormat';

function latexify(expression = '') {
  return String(expression)
    .replace(/\b(sin|cos|tan)\b/g, (word) => `\\${word}`)
    .replace(/(opposé|hypoténuse|adjacent|Moyenne|somme|valeurs|effectif|total)/g, (word) => `\\text{${word}}`)
    .replace(/−/g, '-')
    .replace(/×/g, '\\times ')
    .replace(/≈/g, '\\approx ')
    .replace(/≤/g, '\\le ')
    .replace(/≥/g, '\\ge ')
    .replace(/π/g, '\\pi ')
    .replace(/²/g, '^{2}')
    .replace(/³/g, '^{3}')
    .replace(/\^\(([^)]+)\)/g, '^{$1}')
    .replace(/\^([A-Za-z0-9+\-]+)/g, '^{$1}')
    .replace(/√\s*([A-Za-z0-9]+)/g, '\\sqrt{$1}');
}

function renderKatex(expression, displayMode = false) {
  try {
    return katex.renderToString(latexify(expression), {
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
const autoMathRegex = /(√\s*[A-Za-z0-9]+|(?:[A-Za-z][A-Za-z0-9]*\([^)]*\)|[A-Za-zπ]+|[0-9]+(?:[.,][0-9]+)?)(?:\^\([^)]*\)|\^[A-Za-z0-9+\-]+|[²³])?(?:\s*[=≈×+\-/<>]\s*(?:[A-Za-z][A-Za-z0-9]*\([^)]*\)|[A-Za-zπ]+|[0-9]+(?:[.,][0-9]+)?)(?:\^\([^)]*\)|\^[A-Za-z0-9+\-]+|[²³])?)+|[A-Za-z0-9π]+(?:\^\([^)]*\)|\^[A-Za-z0-9+\-]+|[²³])[A-Za-z0-9]*)/g;

function AutoMathText({ text }) {
  const parts = String(text || '').split(autoMathRegex);
  return parts.map((part, index) => {
    if (!part) return null;
    autoMathRegex.lastIndex = 0;
    const isMath = autoMathRegex.test(part) && /[=≈×^²³√/+\-]/.test(part);
    autoMathRegex.lastIndex = 0;
    if (!isMath) return <React.Fragment key={index}>{part}</React.Fragment>;
    return <span key={index} className="inline-math" dangerouslySetInnerHTML={{ __html: renderKatex(part, false) }} />;
  });
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
        return <p key={index}><RichText text={block.content} /></p>;
      })}
    </div>
  );
}
