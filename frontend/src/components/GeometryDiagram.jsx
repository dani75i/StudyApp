import React from 'react';

/** Schematic geometry: topology only, never rely on visual scale to calculate. */
export default function GeometryDiagram({ diagram }) {
  if (!diagram?.vertices) return null;
  const letters = diagram.vertices;
  if (diagram.type === 'right_triangle' && letters.length === 3) {
    const [a, b, c] = letters;
    return <figure className="v9-geometry" role="img" aria-label={`Schéma non à l'échelle du triangle ${a}${b}${c} rectangle en ${b}`}>
      <svg viewBox="0 0 310 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
        <path d="M58 25 L58 157 L263 157 Z" fill="none" stroke="currentColor" strokeWidth="2.8" strokeLinejoin="round" />
        <path d="M58 141 H74 V157" fill="none" stroke="var(--purple)" strokeWidth="2.3" />
        <circle cx="58" cy="25" r="3.5" fill="var(--purple)"/><circle cx="58" cy="157" r="3.5" fill="var(--purple)"/><circle cx="263" cy="157" r="3.5" fill="var(--purple)"/>
        <text x="40" y="24">{a}</text><text x="39" y="181">{b}</text><text x="269" y="175">{c}</text>
      </svg>
      <figcaption>Schéma non à l’échelle · Repère l’angle droit et l’hypoténuse.</figcaption>
    </figure>;
  }
  if (diagram.type === 'thales_rays' && letters.length === 5) {
    const [o,a,b,c,d] = letters;
    const bx = diagram.parallel ? 127 : 153;
    const by = diagram.parallel ? 100 : 80;
    return <figure className="v9-geometry" role="img" aria-label={`Schéma non à l'échelle de la configuration de Thalès, deux demi-droites issues de ${o}`}>
      <svg viewBox="0 0 310 206" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
        <path d="M24 180 L274 180 M24 180 L230 20" fill="none" stroke="currentColor" strokeWidth="2.8" strokeLinejoin="round"/>
        <path d={`M149 180 L${bx} ${by} M274 180 L230 20`} fill="none" stroke="var(--purple)" strokeWidth="2" strokeDasharray="6 5"/>
        <text x="9" y="195">{o}</text><text x="148" y="197">{a}</text><text x={bx - 12} y={by - 5}>{b}</text><text x="275" y="197">{c}</text><text x="233" y="17">{d}</text>
      </svg>
      <figcaption>Schéma de position, non à l’échelle · Les longueurs sont celles de l’énoncé.</figcaption>
    </figure>;
  }
  return null;
}
