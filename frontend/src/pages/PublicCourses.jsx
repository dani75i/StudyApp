import { setPageSeo } from '../seo';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Atom, BookOpenText, Calculator, Zap } from 'lucide-react';
import { api } from '../api';
import PublicFooter from '../components/PublicFooter';
import { trackEvent } from '../analytics';
import { getChapterIllustration } from '../chapterIllustrations';

const icons = { mathematiques: Calculator, 'physique-chimie': Atom };

export default function PublicCourses() {
  const [data, setData] = useState(null);

  useEffect(() => {
    setPageSeo({
      title: 'Cours gratuits de maths et physique-chimie (6e à 3e) | ExoDéclic',
      description: 'Découvre les cours gratuits de maths et physique-chimie du collège : 6e, 5e, 4e et 3e. Fiches de révision et exercices corrigés sur ExoDéclic.',
      pathname: '/decouvrir/cours',
    });
    api('/public/catalog').then(setData);
  }, []);

  if (!data) return <div className="screen-center"><div className="loader" /></div>;

  return (
    <div className="public-page">
      <header className="public-nav">
        <Link className="brand" to="/"><span className="brand-mark"><Zap size={21} /></span><span>ExoDéclic</span></Link>
        <nav><Link to="/connexion">Connexion</Link><Link className="primary compact" to="/inscription" onClick={() => trackEvent('cta_click', { cta_name: 'courses_nav_signup', destination: '/inscription' })}>Créer mon compte</Link></nav>
      </header>

      <main className="public-content">
        <Link className="back" to="/"><ArrowLeft size={17} /> Accueil</Link>
        <div className="public-course-heading"><span className="eyebrow">COURS GRATUITS</span><h1>Maths et physique-chimie de la 6e à la 3e</h1><p>Découvre les fiches disponibles publiquement. Crée ensuite un compte pour accéder aux exercices corrigés et suivre ta progression.</p></div>

        <div className="subject-stack">
          {data.map((subject) => {
            const Icon = icons[subject.slug] || BookOpenText;
            return (
              <section key={subject.id}>
                <div className="subject-title"><div className={`subject-logo ${subject.slug === 'mathematiques' ? 'math' : 'physics'}`}><Icon size={25} /></div><div><h2>{subject.name}</h2><p>{subject.description}</p></div></div>
                <div className="chapter-grid">
                  {subject.chapters.map((chapter) => {
                    const illustration = getChapterIllustration({ subjectSlug: subject.slug, title: chapter.title, level: chapter.level });

                    return (
                      <Link key={chapter.id} className="chapter-card course-card" to={`/decouvrir/cours/${chapter.id}`} onClick={() => trackEvent('course_opened', { chapter_id: chapter.id, subject: subject.slug })}>
                        {illustration && (
                          <div className="chapter-visual">
                            <img src={illustration} alt={`Illustration du chapitre ${chapter.title}`} loading="lazy" />
                          </div>
                        )}
                        <div className="chapter-top"><BookOpenText size={20} /><span>{chapter.level}</span></div>
                        <h3>{chapter.title}</h3><p>{chapter.summary}</p>
                        <div className="course-kpis"><span>{chapter.lesson_count} fiche(s)</span><span>{chapter.exercise_count} exercice(s)</span></div>
                        <div className="chapter-footer"><small>Lire gratuitement</small><ArrowRight size={17} /></div>
                      </Link>
                    );
                  })}
                </div>
              </section>
            );
          })}
        </div>
      </main>
      <PublicFooter />
    </div>
  );
}
