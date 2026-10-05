import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, BookOpenCheck, CheckCircle2, Dumbbell, Zap } from 'lucide-react';
import { api } from '../api';
import { setPageSeo } from '../seo';
import PublicFooter from '../components/PublicFooter';
import { LessonContent } from '../components/RichContent';

export default function PublicExercisesChapter() {
 const { id }=useParams(); const [data,setData]=useState(null);
 useEffect(()=>{api(`/public/exercises/${id}`).then(ch=>{setData(ch);setPageSeo({title:`${ch.title} ${ch.level} : exercices corrigés gratuits | ExoDéclic`,description:`Exercices corrigés gratuits sur ${ch.title} en ${ch.level}. Entraîne-toi en ${ch.subject.name} avec ExoDéclic.`,pathname:`/decouvrir/exercices/${id}`});});},[id]);
 if(!data) return <div className="screen-center"><div className="loader"/></div>;
 return <div className="public-page"><header className="public-nav"><Link className="brand" to="/"><span className="brand-mark"><Zap size={21}/></span><span>ExoDéclic</span></Link><nav><Link to="/decouvrir/cours">Cours</Link><Link className="primary compact" to="/inscription">Créer mon compte</Link></nav></header><main className="public-content public-chapter"><Link className="back" to="/decouvrir/exercices"><ArrowLeft size={17}/> Tous les exercices corrigés</Link><header className="chapter-hero"><span className="subject-pill">{data.subject.emoji} {data.subject.name} • {data.level}</span><h1>Exercices corrigés : {data.title}</h1><p>{data.summary}</p><div className="course-kpis"><span>{data.exercise_count} exercices disponibles</span><span>Du facile au difficile</span></div></header>
 <section className="public-lessons"><div className="section-head"><div><h2><Dumbbell size={21}/> Exercices et corrections</h2><p>Voici une sélection gratuite. Essaie d'abord de résoudre chaque exercice avant d'ouvrir mentalement la correction.</p></div></div><div className="lesson-list">{data.exercises.map((ex,i)=><article className="lesson-card public-seo-exercise" key={ex.id}><div className="lesson-tag">Exercice {i+1} • {'★'.repeat(Math.max(1,Math.min(3,ex.difficulty||1)))}</div><h3>{ex.title}</h3><div className="seo-exercise-block"><strong>Énoncé</strong><LessonContent body={ex.statement}/></div><div className="seo-correction"><strong><CheckCircle2 size={17}/> Correction</strong><LessonContent body={ex.correction}/></div></article>)}</div></section>
 <section className="public-exercise-cta"><BookOpenCheck size={26}/><div><h2>Besoin de revoir le cours ?</h2><p>Retrouve la fiche de cours correspondante, puis crée ton compte gratuit pour faire tous les exercices et suivre ta progression.</p></div><div className="seo-cta-actions"><Link className="secondary" to={`/decouvrir/cours/${data.id}`}>Voir le cours</Link><Link className="primary" to="/inscription">Continuer gratuitement <ArrowRight size={17}/></Link></div></section></main><PublicFooter/></div>;
}
