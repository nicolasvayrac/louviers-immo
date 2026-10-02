# louviers.immo — le guide de Louviers, par CV Immobilier

Site statique : du HTML, du CSS et du JavaScript, sans base de données ni WordPress.
Il fonctionne sur n'importe quel hébergement (Netlify, OVH…).

## Ce que contient le site

| Page | Rôle |
|---|---|
| `index.html` | Accueil : recherche d'adresse, quartiers, prix, portraits, outils |
| `adresse.html` | **Mon adresse** : commerces les plus proches, écoles, bus, gare, A13, temps de trajet, prix autour |
| `prix.html` | Carte des ventes réelles (DVF), médianes par commune |
| `quartiers.html` + `quartiers/centre-ville.html` | Les quartiers (le centre-ville sert de modèle) |
| `portraits.html` + `portraits/modele.html` | Portraits de commerçants (modèle de page non référencé) |
| `commerces.html` | Annuaire des commerçants par rubrique (Se restaurer, Snacking, S'habiller…), carte, recherche, 10 communes |
| `diagnostics.html` | Diagnostics obligatoires : questionnaire (vente/location, type, année…) et contrôle d’assainissement de l’Agglomération Seine-Eure |
| `conciergerie.html` | S’installer : eau, électricité, gaz, box, déchets, démarches, mairie, avec plusieurs prestataires |
| `comparer.html` | Comparateur de deux adresses : prix, écoles, gare, A13 |
| `outil-qr.html` | **Outil interne** (non référencé) : code QR « Vivre ici » vers la page d'une adresse, pour les annonces et vitrines |
| `merci.html` | Page affichée après l'envoi d'un formulaire |
| `outils.html` | Frais de notaire (taux de l'Eure 2026) et capacité d'emprunt |
| `a-propos.html`, `mentions-legales.html`, `404.html` | Pages institutionnelles |

Services gratuits utilisés directement par le navigateur du visiteur (aucune clé, aucun abonnement) :

- **Adresses** : Base Adresse Nationale, via le géocodage de l'IGN (Géoplateforme)
- **Commerces, écoles, arrêts de bus** : OpenStreetMap (API Overpass)
- **Fond de carte** : Plan IGN
- **Polices et carte (Leaflet)** : hébergées sur le site, aucun appel à Google, aucun cookie

## Mise en ligne

### Option A — Netlify (recommandée, gratuite, 5 minutes)
1. Créez un compte sur netlify.com.
2. Menu « Add new site » → « Deploy manually » → glissez **tout le dossier** `louviers.immo`.
3. « Domain management » → « Add a domain » → `louviers.immo`, puis suivez les instructions DNS (chez OVH : zone DNS du domaine).
4. Le certificat HTTPS s'active tout seul. Le fichier `netlify.toml` gère déjà les redirections des anciennes pages.

### Option B — Hébergement OVH
1. Supprimez les anciens fichiers de l'opération « taxe foncière » (`index.html`, `reglement.html`, `contact.html`, `style.css`).
2. Déposez tout le contenu du dossier par FTP à la racine (dossier `www`), **y compris le fichier caché `.htaccess`**.
3. Activez le certificat SSL gratuit dans l'espace client OVH.

### Après la mise en ligne
- Ouvrez Google Search Console, ajoutez `louviers.immo` et envoyez `https://louviers.immo/sitemap.xml`.
- Testez « Mon adresse » avec une vraie adresse de Louviers.

## Liste du jour du lancement

1. **Netlify, réglages de test à retirer** : dans `netlify.toml`, supprimez les 3 lignes marquées « AVANT LE LANCEMENT » (consigne `X-Robots-Tag: noindex`). Si vous avez ajouté un mot de passe, supprimez le fichier `_headers` ou désactivez la protection dans Netlify.
2. **Domaine** : Netlify → Domain management → Add a domain → `louviers.immo`, puis suivez les instructions DNS chez OVH. Attendez que le cadenas HTTPS s'active.
3. **Formulaires** : Netlify → Forms → vérifiez que la détection des formulaires est activée et que `alerte-quartier` et `proposer-commerce` apparaissent ; ajoutez une notification par mail vers contact@cvimmobilier.fr (Forms → Form notifications). Faites un envoi d'essai de chaque formulaire.
4. **Google** : Search Console → propriété `louviers.immo` → Sitemaps → envoyez `https://louviers.immo/sitemap.xml`. Demandez l'indexation de l'accueil.
5. **Plausible** : ouvrez le tableau de bord, visitez le site depuis votre téléphone et vérifiez que la visite apparaît. Ajoutez les objectifs (Goals) : Estimation Click, Estimation Rapide, Diagnostics Vendeur, Biens Quartier, Alerte Quartier, Proposer Commerce, Comparateur.
6. **Contrôle final** : testez « Mon adresse » avec une vraie adresse, la carte des prix, un portrait, l'annuaire, et le partage d'un portrait sur Facebook (l'image du commerçant doit apparaître).

## À faire avant d'annoncer le site

- [x] Données de prix DVF 2024-2025 intégrées (1 123 ventes, 25 communes).
- [x] Mentions légales, équipe, photos et téléphones.
- [x] Hébergeur (Netlify), vérification Google Search Console et suivi Plausible conservés.
- [x] Page Centre-ville rédigée (marché, commerces, agenda, aînés, jeunes, prix du quartier).
- [ ] **Portrait Maison Barbé** : le faire relire par Sylvie et Patrice Barbé, et ajouter 2 ou 3 citations de Sylvie et des photos (boutique rénovée, produits).
- [ ] **Liens vers cvimmobilier.fr** : « Estimer mon bien » pointe vers `https://www.cvimmobilier.fr/estimation` et « Nos biens à vendre » vers l'accueil. Vérifiez qu'ils ouvrent les bonnes pages.
- [ ] **Photo de Brigitte** : elle est découpée dans la bannière de l'équipe, donc un peu moins nette. Remplacez `assets/img/equipe/brigitte-bramille.jpg` par sa photo individuelle (format carré) si vous l'avez.

## Ajouter les données de prix (DVF)

1. Téléchargez les fichiers de l'Eure pour 2024 et 2025 (et 2026 quand il paraîtra) :
   - https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/27.csv.gz
   - https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/27.csv.gz
2. Envoyez-les à Claude, ou lancez vous-même (Python 3 requis) :
   ```
   python3 scripts/build_dvf.py 27-2024.csv.gz 27-2025.csv.gz
   ```
3. Le fichier `data/dvf.json` est mis à jour : redéposez-le sur l'hébergement.

DVF est mis à jour deux fois par an (avril et octobre). Le fichier ne contient aucune adresse ni aucun nom, et le dossier `data/` est exclu des moteurs de recherche, conformément aux conditions de réutilisation de DVF.

## Publier un portrait

1. Dupliquez `portraits/modele.html` (par ex. `portraits/boulangerie-dupont.html`), remplacez tous les `[ … ]`, et changez `noindex, follow` en `index, follow`.
2. Ajoutez les photos dans `assets/img/portraits/`.
3. Ajoutez un bloc dans `data/portraits.js` (le mode d'emploi est en haut du fichier) avec les coordonnées GPS de la boutique.
   Le portrait apparaît alors sur l'accueil, sur la page Portraits, **et en doré dans « Mon adresse » pour toutes les adresses voisines**.
4. Ajoutez la page à `sitemap.xml`.

Questionnaire type (6 questions, déjà dans le modèle) : comment est née l'affaire · pourquoi Louviers · une journée type · le produit dont on est le plus fier · son adresse préférée à Louviers · un conseil à un nouvel arrivant.

## Agences et partenaires

Vos deux agences et vos partenaires (courtiers…) sont listés dans `data/partenaires.js`. Ils apparaissent toujours, en doré, dans l'annuaire et dans « Mon adresse ». Pour en ajouter ou en retirer un, modifiez ce fichier (mode d'emploi en haut du fichier) ou demandez à Claude.

## Masquer un commerce

Pour qu'un commerce n'apparaisse plus (ni dans l'annuaire, ni dans « Mon adresse »), ajoutez son nom dans `data/exclusions.js` (mode d'emploi en haut du fichier). Pour le réafficher, supprimez la ligne.

## Clubs sportifs

Les clubs et associations sportives de Louviers sont listés dans `data/clubs.js` (source : annuaire des associations 2024 de la Ville). Ils apparaissent dans la rubrique « Clubs sportifs » de l'annuaire. Pour en ajouter, en retirer ou corriger un lieu, modifiez ce fichier. Par discrétion, ni les noms des présidents ni leurs numéros personnels ne sont publiés : seulement le site du club, son adresse mail de club, ou un lien vers la page de la Ville.

## Mise à jour automatique des commerces

Chaque lundi, GitHub télécharge les commerces, écoles, arrêts de bus et équipements depuis OpenStreetMap (`scripts/build_pois.py`) et les enregistre dans `data/pois.json` : le site les affiche alors instantanément, sans dépendre d'un service extérieur à chaque visite. Pour lancer la mise à jour à la main : onglet **Actions** du dépôt → « Mettre à jour les données » → **Run workflow**.

## Formulaires et données personnelles

Les formulaires « Recevoir les biens à vendre dans ce quartier » (page Mon adresse) et « Proposer mon commerce » (Portraits et Commerces) passent par Netlify Forms. Les demandes s'affichent dans Netlify (onglet Forms) et, une fois la notification réglée, arrivent par mail. La mention RGPD est dans les mentions légales (`#formulaires`) : durée de conservation de 3 ans après le dernier échange, à confirmer par vos soins. Pensez à répondre aux demandes de désinscription.

## Générer les pages

Les pages HTML sont produites par `scripts/gen.py` (Python 3 et Pillow). Les textes se modifient dans ce fichier, puis `python3 scripts/gen.py` réécrit toutes les pages. Les photos sont automatiquement servies en WebP avec le JPG en secours : après avoir ajouté une photo JPG, créez aussi sa version `.webp` (ou demandez à Claude).

## Bon à savoir

- **Temps de trajet** : estimations calculées à partir des distances (détour moyen de 30 %, 4,8 km/h à pied, 15 km/h à vélo, vitesse urbaine puis routière en voiture). Pour le bus, le site affiche les arrêts les plus proches et leurs lignes quand OpenStreetMap les connaît. Des temps de bus exacts nécessiteraient les horaires du réseau Semo (évolution possible).
- **Commerces** : ils viennent d'OpenStreetMap. Si un commerce manque ou a fermé, on peut le corriger soi-même sur openstreetmap.org (gratuit), et la correction apparaît sur le site sous quelques minutes. Les agences immobilières sont volontairement exclues de la liste. Les tabacs ont leur propre rubrique « Tabac & presse », et les artisans du bâtiment (plombiers, électriciens, menuisiers, couvreurs…) sont regroupés dans « Artisans ».
- **Frais de notaire** : les taux sont dans `assets/outils.js` (bloc « Paramètres ») : DMTO de l'Eure à 6,32 % depuis le 1er avril 2026, 5,81 % pour les primo-accédants. À mettre à jour si la loi change.
- **Mesure d'audience** : Plausible, comme sur l'ancien site (voir `GUIDE-TRACKING-PLAUSIBLE.md`). Tous les boutons « Estimer mon bien » envoient l'événement « Estimation Click », avec la page d'origine en position.
