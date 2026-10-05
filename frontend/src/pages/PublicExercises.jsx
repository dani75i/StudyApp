import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Atom, Calculator, Dumbbell, Zap } from 'lucide-react';
import { api } from '../api';
import { setPageSeo } from '../seo';
import PublicFooter from '../components/PublicFooter';

const icons = { mathematiques: Calculator, 'physique-chimie': Atom };
export default function PublicExercises() {
  const [data, setData] = useState(null);
  useEffect(() => {
    setPageSeo({ title: 'Exercices maths collège corrigés gratuits (6e à 3e) | ExoDéclic', description: 'Exercices corrigés gratuits de maths et physique-chimie pour le collège, de la 6e à la 3e. Entraîne-toi par chapitre avec ExoDéclic.', pathname: '/decouvrir/exercices' });
    api('/public/catalog').then(setData);
  }, []);
  if (!data) return <div className="screen-center"><div className="loader" /></div>;
  return <div className="public-page"><header className="public-nav"><Link className="brand" to="/"><span className="brand-mark"><Zap size={21}/></span><span>ExoDéclic</span></Link><nav><Link to="/decouvrir/cours">Cours</Link><Link className="primary compact" to="/inscription">Créer mon compte</Link></nav></header>
    <main className="public-content"><Link className="back" to="/"><ArrowLeft size={17}/> Accueil</Link><div className="public-course-heading"><span className="eyebrow">EXERCICES CORRIGÉS GRATUITS</span><h1>Exercices de maths et physique-chimie du collège</h1><p>Choisis ton niveau et ton chapitre. Consulte des exercices et leurs corrections gratuitement, de la 6e à la 3e.</p></div>
    <div className="subject-stack">{data.map(subject => { const Icon=icons[subject.slug]||Dumbbell; return <section key={subject.id}><div className="subject-title"><div className={`subject-logo ${subject.slug==='mathematiques'?'math':'physics'}`}><Icon size={25}/></div><div><h2>{subject.name}</h2><p>Exercices corrigés par chapitre</p></div></div><div className="chapter-grid">{subject.chapters.filter(c=>c.exercise_count>0).map(c=><Link key={c.id} className="chapter-card exercise-card" to={`/decouvrir/exercices/${c.id}`}><div className="chapter-top"><Dumbbell size={20}/><span>{c.level}</span></div><h3>{c.title}</h3><p>{c.summary}</p><div className="course-kpis"><span>{c.exercise_count} exercice(s)</span><span>Corrections incluses</span></div><div className="chapter-footer"><small>S'entraîner gratuitement</small><ArrowRight size={17}/></div></Link>)}</div></section>})}</div></main><PublicFooter/></div>;
}
