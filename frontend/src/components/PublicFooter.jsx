import React from 'react';
import { Link } from 'react-router-dom';
import { openCookiePreferences } from '../analytics';

export default function PublicFooter() {
  return (
    <footer className="public-footer">
      <span>© {new Date().getFullYear()} StudySprint</span>
      <Link to="/decouvrir/cours">Cours gratuits</Link>
      <Link to="/confidentialite">Confidentialité</Link>
      <button type="button" className="footer-link-button" onClick={openCookiePreferences}>Gérer les cookies</button>
      <Link to="/connexion">Connexion</Link>
    </footer>
  );
}
