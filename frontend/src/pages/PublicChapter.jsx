import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, BookOpenCheck, Dumbbell, Zap } from 'lucide-react';
import { api } from '../api';

export default function PublicChapter() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    api(`/public/chapters/${id}`).then((chapter) => {
      setData(chapter);
      document.title = `${chapter.title} — ${chapter.level} — StudySprint`;
      const meta = document.querySelector('meta[name="description"]');
      if (meta) meta.setAttribute('content', `${chapter.summary} Cours gratuit de ${chapter.subject.name} niveau ${chapter.level} sur StudySprint.`);
    });
  }, [id]);

  if (!data) return <div className="screen-center"><div className="loader" /></div>;

  return (
    <div className="public-page">
      <header className="public-nav"><Link className="brand" to="/"><span className="brand-mark"><Zap size={21} /></span><span>StudySprint</span></Link><nav><Link to="/connexion">Connexion</Link><Link className="primary compact" to="/inscription">Créer mon compte</Link></nav></header>
      <main className="public-content public-chapter">
        <Link className="back" to="/decouvrir/cours"><ArrowLeft size={17} /> Tous les cours gratuits</Link>
        <header className="chapter-hero"><span className="subject-pill">{data.subject.emoji} {data.subject.name} • {data.level}</span><h1>{data.title}</h1><p>{data.summary}</p></header>
        <section className="public-lessons">
          <div className="section-head"><div><h2><BookOpenCheck size={21} /> Le cours</h2><p>Les notions essentielles à connaître.</p></div></div>
          <div className="lesson-list">{data.lessons.map((lesson) => <article className="lesson-card" key={lesson.id}><div className="lesson-tag">Fiche cours</div><h3>{lesson.title}</h3>{lesson.body.split('\n').map((p, i) => <p key={i}>{p}</p>)}</article>)}</div>
        </section>
        <section className="public-exercise-cta"><Dumbbell size={26} /><div><h2>{data.exercise_count} exercice(s) pour t'entraîner</h2><p>Crée un compte gratuit pour répondre aux exercices, voir les corrections et enregistrer ta progression.</p></div><Link className="primary" to="/inscription">M'entraîner gratuitement <ArrowRight size={17} /></Link></section>
      </main>
    </div>
  );
}
