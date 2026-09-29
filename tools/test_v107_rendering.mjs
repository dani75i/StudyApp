import assert from 'node:assert/strict';
import { splitExampleText, isWorkedFormula } from '../frontend/src/exampleMath.js';
const math = String.raw;
assert.equal(isWorkedFormula(math`\frac{10^6}{10^2}=10^4`), true);
assert.equal(isWorkedFormula(math`\sqrt{49}=7`), true);
assert.equal(isWorkedFormula('a=x'), false);
assert.deepEqual(splitExampleText(math`Avec \(a=x\), on obtient \((x+3)^2=x^2+6x+9\).`), [
  {type:'text', value:math`Avec \(a=x\), on obtient`},
  {type:'formula', value:'(x+3)^2=x^2+6x+9'},
]);
assert.deepEqual(splitExampleText(math`On calcule \(10^3\times10^2=10^5\) et \(\frac{10^6}{10^2}=10^4\).`), [
  {type:'text', value:'On calcule'},
  {type:'formula', value:math`10^3\times10^2=10^5`},
  {type:'text', value:'et'},
  {type:'formula', value:math`\frac{10^6}{10^2}=10^4`},
]);
assert.deepEqual(splitExampleText(math`Le résultat est \(\sqrt{49}=7\).`), [
  {type:'text', value:'Le résultat est'},
  {type:'formula', value:math`\sqrt{49}=7`},
]);
console.log('PASS: worked formulas in examples use display mode; short symbols stay inline; trailing punctuation removed');
