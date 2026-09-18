import React, { useEffect, useState } from 'react';
import { ArrowRight, BookOpenText, Layers3 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api } from '../api';
import { getSubjectMeta } from '../subjectMeta';
import { getChapterIllustration } from '../chapterIllustrations';

export default function Catalog() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api('/catalog').then(setData);
  }, []);

  if (!data) return <div className="loader-page"><div className="loader" /></div>;

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">BIBLIOTHÈQUE</span>
          <h1>Cours</h1>
          <p>Retrouve les notions essentielles de maths et de physique, clairement séparées de la zone d'entraînement.</p>
        </div>
        <Link className="secondary compact-button" to="/exercices">Aller aux exercices <ArrowRight size={17} /></Link>
      </header>

      <div className="subject-stack">
        {data.map((subject) => {
          const meta = getSubjectMeta(subject.slug);
          const Icon = meta.icon;
          return (
            <section className="subject-block" key={subject.id}>
              <div className="subject-title">
                <div className={`subject-logo ${meta.accent}`}><Icon size={25} /></div>
                <div>
                  <h2>{subject.name}</h2>
                  <p>{subject.description}</p>
                </div>
              </div>

              {subject.chapters.length ? (
                <div className="chapter-grid">
                  {subject.chapters.map((chapter) => {
                    const illustration = getChapterIllustration({ subjectSlug: subject.slug, title: chapter.title });

                    return (
                      <Link className="chapter-card course-card" to={`/chapitre/${chapter.id}`} key={chapter.id}>
                        {illustration && (
                          <div className="chapter-visual">
                            <img src={illustration} alt={`Illustration du chapitre ${chapter.title}`} loading="lazy" />
                          </div>
                        )}
                        <div className="chapter-top">
                          <BookOpenText size={20} />
                          <span>{chapter.level}</span>
                        </div>
                        <h3>{chapter.title}</h3>
                        <p>{chapter.summary}</p>
                        <div className="course-kpis">
                          <span><Layers3 size={14} /> {chapter.progress.total} exercices associés</span>
                          <span>{chapter.progress.percent}% maîtrisé</span>
                        </div>
                        <div className="bar"><span style={{ width: `${chapter.progress.percent}%` }} /></div>
                        <div className="chapter-footer">
                          <small>Lire le cours</small>
                          <ArrowRight size={17} />
                        </div>
                      </Link>
                    );
                  })}
                </div>
              ) : (
                <div className="empty">Le contenu de cette matière arrivera dans une prochaine version.</div>
              )}
            </section>
          );
        })}
      </div>
    </>
  );
}
