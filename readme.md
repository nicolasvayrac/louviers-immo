# louviers.immo

Site dédié à l'opération commerciale « Votre taxe foncière offerte » de CV IMMOBILIER, du 1er mai au 31 juillet 2026.

## Contenu

- `index.html` — Page d'accueil (hero + mécanisme + manifeste + exemples + CTA)
- `reglement.html` — Règlement complet de l'opération, 10 articles
- `contact.html` — Coordonnées des deux agences
- `style.css` — Feuille de style partagée par les trois pages
- `README.md` — Ce document

## Dépendances externes

Le site utilise uniquement deux polices Google Fonts chargées via CDN :
- **Fraunces** (serif de titrage)
- **Outfit** (sans-serif de corps)

Aucune autre dépendance. Pas de framework JS, pas de build, pas de Node. Pas d'images à gérer — le design repose entièrement sur la typographie et le CSS.

## Déploiement

### Option recommandée — Netlify (gratuit, 2 minutes)

1. Compte sur [netlify.com](https://netlify.com)
2. Drag & drop le dossier `louviers-immo/` sur l'interface
3. Onglet « Domain settings » → ajouter `louviers.immo` comme domaine personnalisé
4. Suivre les instructions DNS pour pointer `louviers.immo` vers Netlify

### Option 2 — OVH hébergement classique

1. Espace client OVH → hébergement web lié à `louviers.immo`
2. FTP → déposer les 4 fichiers à la racine `www/`

### Option 3 — Vercel

Principe identique à Netlify.

## Informations vérifiées (source : ton site cvimmobilier.fr)

- **Louviers** : 27 rue du Général de Gaulle, 27400 Louviers — tél 02 32 40 22 28 — email `cvimmobilier@wanadoo.fr`
- **Saint-Pierre-du-Vauvray** : 15 Grande Rue, 27430 — tél 02 79 49 21 71 — email `contact@cvimmobilier.fr`

⚠️ L'adresse **15 Grande Rue** est celle indiquée sur ton site officiel. Les visuels presse portrait indiquent 20 — à trancher et corriger sur le tirage restant.

⚠️ L'email Louviers est encore `@wanadoo.fr` : à moderniser (ex. `louviers@cvimmobilier.fr`) pour cohérence avec Saint-Pierre.

## À personnaliser avant mise en ligne

Champs marqués `[...]` dans le règlement, à compléter avec ton juriste FNAIM :
- Capital social SARL
- Numéro RCS
- Numéro de carte professionnelle
- Garantie financière
- Coordonnées de l'huissier chargé du dépôt

Vérifier aussi :
- Bouton « Télécharger le PDF » sur la page règlement : remplacer `reglement.pdf` par le PDF officiel signé
- Footer : numéro de carte professionnelle `XXXXX`

## Tracking / analytics

Pour mesurer le ROI des QR codes et de l'affichage, ajoute avant `</head>` dans les 3 pages un snippet Google Analytics 4 ou Plausible. Idéalement, paramètre un événement sur le clic du bouton « Estimation gratuite » pour tracker la conversion vers ton site principal.

Paramètres UTM à ajouter sur les liens sortants selon le support :
- QR codes presse : `?utm_source=presse&utm_medium=qr&utm_campaign=taxe2026`
- QR codes set de table : `?utm_source=settable&utm_medium=qr&utm_campaign=taxe2026`
- QR codes vitrine : `?utm_source=vitrine&utm_medium=qr&utm_campaign=taxe2026`
- QR codes flyers : `?utm_source=flyer&utm_medium=qr&utm_campaign=taxe2026`

Ça permet de savoir exactement d'où viennent les visites et quel support est le plus rentable.

## SEO

Balises title, meta description, canonical et Open Graph déjà en place sur les 3 pages. Mots-clés ciblés : taxe foncière offerte Louviers, mandat exclusif Seine-Eure, vendre maison Le Vaudreuil, agence immobilière Eure.

Une fois en ligne, soumettre à Google Search Console pour indexation.

## Accessibilité et performance

- Contrastes validés WCAG AA sur les textes principaux
- Pas de JavaScript bloquant
- Aucune image raster utilisée, uniquement du CSS/SVG inline
- Le site reste fonctionnel même avec JS désactivé

Temps de chargement attendu : < 1 seconde sur connexion 4G.
