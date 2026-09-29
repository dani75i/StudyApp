import React from 'react';
import { getDeclicProgress } from './declicLevels';

/** Le niveau repose sur le nombre d'exercices distincts réussis (statistiques serveur).
 * L'humeur ne change qu'à l'affichage du résultat d'une tentative.
 * Sans nouvel appel réseau ni données sensibles dans le navigateur.
 */
export default function DeclicMascot({ correct = 0, mood = 'idle', compact = false }) {
  const progress = getDeclicProgress(correct);
  const stage = progress.level - 1;
  const state = ['idle', 'success', 'encourage'].includes(mood) ? mood : 'idle';
  const message = state === 'success'
    ? 'Super ! On continue !'
    : state === 'encourage'
      ? 'Ce n’est pas grave, on apprend ensemble !'
      : `Ton compagnon grandit avec tes ${progress.count} exercices maîtrisés !`;
  const aria = `Déclic niveau ${progress.level}, ${progress.title}. ${message}`;

  return (
    <div className={`declic-mascot stage-${stage} mood-${state} ${compact ? 'compact' : ''}`} role="img" aria-label={aria}>
      <svg viewBox="0 0 200 190" aria-hidden="true" focusable="false">
        <defs>
          <linearGradient id="declic-coat" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor={stage >= 4 ? '#ffe8ac' : stage > 1 ? '#a9f6e8' : '#c7c2ff'} />
            <stop offset="100%" stopColor={stage >= 4 ? '#ffca69' : stage > 1 ? '#5cdaca' : '#8478ef'} />
          </linearGradient>
        </defs>
        <ellipse cx="100" cy="172" rx="55" ry="9" fill="#564ba1" opacity=".12" />
        <g className="declic-body">
          <path d="M65 133 L54 153 Q50 162 58 164 L76 156 M135 133 L145 154 Q150 162 141 165 L123 157" fill="none" stroke="#7668da" strokeWidth="13" strokeLinecap="round" />
          <path className="declic-arm-left" d="M52 113 Q28 104 25 85" fill="none" stroke="#8275e9" strokeWidth="13" strokeLinecap="round" />
          <path className="declic-arm-right" d="M147 112 Q169 112 176 91" fill="none" stroke="#8275e9" strokeWidth="13" strokeLinecap="round" />
          <ellipse cx="100" cy="108" rx="58" ry="61" fill="url(#declic-coat)" />
          <path d="M62 103 Q100 123 139 103 L135 137 Q99 157 65 137Z" fill="#fff" opacity=".38" />
          <path d="M64 65 Q101 48 136 67" fill="none" stroke="#fff" strokeWidth="7" strokeLinecap="round" opacity=".65" />
          <rect x="73" y="38" width="54" height="18" rx="8" fill="#8479e3" />
          <path d="M99 42 L99 24" stroke="#6e62d9" strokeWidth="6" strokeLinecap="round" />
          <circle cx="99" cy="19" r="9" fill={stage >= 2 ? '#ffc65f' : '#ff8d9b'} />
          <ellipse cx="71" cy="117" rx="9" ry="6" fill="#ff96b3" opacity=".8" />
          <ellipse cx="129" cy="117" rx="9" ry="6" fill="#ff96b3" opacity=".8" />
          {state === 'encourage' ? (
            <>
              <path d="M71 99 Q79 91 87 99 M113 99 Q121 91 129 99" fill="none" stroke="#342d60" strokeWidth="4" strokeLinecap="round" />
              <path d="M89 130 Q100 121 111 130" fill="none" stroke="#342d60" strokeWidth="4" strokeLinecap="round" />
            </>
          ) : (
            <>
              <ellipse cx="80" cy="98" rx="6" ry={state === 'success' ? 8 : 9} fill="#332a63" />
              <ellipse cx="120" cy="98" rx="6" ry={state === 'success' ? 8 : 9} fill="#332a63" />
              <circle cx="82" cy="95" r="2" fill="white" />
              <circle cx="122" cy="95" r="2" fill="white" />
              <path d={state === 'success' ? 'M87 122 Q100 146 113 122' : 'M89 127 Q100 136 111 127'} fill="none" stroke="#342d60" strokeWidth="4" strokeLinecap="round" />
            </>
          )}
          {stage >= 1 && <path d="M49 66 L58 47 L66 68" fill="#ffd074" stroke="#eaaa42" strokeWidth="3" />}
          {stage >= 2 && <path d="M151 72 l6 -14 7 14 15 2 -12 10 4 15 -14 -8 -13 8 4 -15 -12 -10Z" fill="#fbc557" stroke="#e8a943" strokeWidth="2" />}
          {stage >= 3 && <path d="M75 47 L69 19 89 29 101 8 113 29 136 20 130 47Z" fill="#f8bf5b" stroke="#dd9d36" strokeWidth="3" />}
          {stage >= 4 && <g fill="#fff2a9" stroke="#f4b454" strokeWidth="2"><path d="M35 63 l4 -10 4 10 10 4 -10 4 -4 10 -4 -10 -10 -4Z" /><path d="M163 53 l3 -8 3 8 8 3 -8 3 -3 8 -3 -8 -8 -3Z" /></g>}
          <circle cx="99" cy="143" r="8" fill="#fff" opacity=".65" />
        </g>
        {state === 'success' && <g className="declic-confetti" fill="#e4a847">
          <path d="M23 37 l3 -10 4 10 10 4 -10 4 -4 10 -3 -10 -10 -4Z" />
          <path d="M166 28 l3 -10 4 10 10 4 -10 4 -4 10 -3 -10 -10 -4Z" />
          <circle cx="167" cy="129" r="5" fill="#5acaba" />
          <circle cx="27" cy="132" r="5" fill="#f87a9c" />
        </g>}
      </svg>
      {!compact && <div className="declic-message"><strong>{`Déclic ${progress.title.toLowerCase()}`}</strong><p>{message}</p>{progress.next && <small>Prochaine évolution : {progress.next.min} exercices maîtrisés</small>}</div>}
    </div>
  );
}
