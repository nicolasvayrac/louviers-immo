# -*- coding: utf-8 -*-
"""Génère les pages HTML statiques de louviers.immo (en-tête et pied communs).

Usage : python3 scripts/gen.py  (Python 3 + Pillow). Modifier les textes ici, puis relancer : toutes les pages sont réécrites."""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))  # racine du site (ce script est dans scripts/)
DOMAIN = 'https://louviers.immo/'
CV_SITE = 'https://www.cvimmobilier.fr/'
CV_EST = 'https://www.cvimmobilier.fr/estimation'
MAIL = 'contact@cvimmobilier.fr'
VER = '20261003b'
# Passerelle cvimmobilier.fr (biens à vendre) : True pour l'afficher sur le site
PASSERELLE = False

NAV = [('adresse.html', 'Mon adresse'), ('commerces.html', 'Commerces'), ('quartiers.html', 'Quartiers'), ('prix.html', 'Prix'),
       ('conciergerie.html', 'S’installer'), ('diagnostics.html', 'Diagnostics'), ('outils.html', 'Outils')]

ORG = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "@id": DOMAIN + "#site", "url": DOMAIN, "name": "louviers.immo",
         "description": "Le guide de Louviers et de l’Agglomération Seine-Eure, par CV Immobilier", "inLanguage": "fr-FR",
         "publisher": {"@id": DOMAIN + "#cv"}},
        {"@type": "RealEstateAgent", "@id": DOMAIN + "#cv", "name": "CV Immobilier", "url": CV_SITE,
         "logo": DOMAIN + "assets/img/logo-navy.png", "foundingDate": "1992",
         "telephone": "+33232402228",
         "address": {"@type": "PostalAddress", "streetAddress": "27 rue du Général de Gaulle", "postalCode": "27400",
                     "addressLocality": "Louviers", "addressCountry": "FR"},
         "areaServed": ["Louviers", "Saint-Pierre-du-Vauvray", "Le Vaudreuil", "Val-de-Reuil", "Agglomération Seine-Eure"],
         "department": [{"@type": "RealEstateAgent", "name": "CV Immobilier Saint-Pierre-du-Vauvray",
                         "telephone": "+33279492171",
                         "address": {"@type": "PostalAddress", "streetAddress": "15 Grande Rue", "postalCode": "27430",
                                     "addressLocality": "Saint-Pierre-du-Vauvray", "addressCountry": "FR"}}],
         "memberOf": [{"@type": "Organization", "name": "FNAIM"}, {"@type": "Organization", "name": "Interkab"}]}
    ]
}

PIN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9C7C33" stroke-width="1.8" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'


def head(title, desc, path, root, noindex=False, jsonld=None, css=''):
    canon = DOMAIN + ('' if path == 'index.html' else path)
    ld = '<script type="application/ld+json">%s</script>\n' % json.dumps(jsonld, ensure_ascii=False) if jsonld else ''
    return f'''<!doctype html>
<html lang="fr" data-root="{root}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className='js';</script>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{'noindex, follow' if noindex else 'index, follow'}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="louviers.immo">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1B2E40">
<meta name="google-site-verification" content="GoHdQ6W1nZJ7YV2Tz9iZWKYWoI4cij_dAX-F8a0LJ_o">
<!-- Plausible Analytics : mesure d'audience sans cookies -->
<script defer data-domain="louviers.immo" src="https://plausible.io/js/script.outbound-links.tagged-events.js"></script>
<script>window.plausible = window.plausible || function () {{ (window.plausible.q = window.plausible.q || []).push(arguments) }}</script>
<link rel="icon" type="image/png" href="{root}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preload" href="{root}assets/fonts/fraunces-latin-300-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/outfit-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
{css}<link rel="stylesheet" href="{root}assets/style.css?v={VER}">
{ld}</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''


def header(active, root, topbar=True):
    cur = ' aria-current="page"'
    items = ''.join(
        f'<a href="{root}{h}"{cur if h == active else ""}>{l}</a>' for h, l in NAV)
    tb = ('<div class="topbar">Le guide de Louviers et de l’Agglomération Seine-Eure<span>·</span>'
          '<b class="tb2" style="font-weight:400">édité par CV Immobilier, agence indépendante depuis 1992</b></div>\n') if topbar else ''
    return f'''{tb}<header class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="{root}index.html" aria-label="louviers.immo — accueil">
      <img src="{root}assets/img/logo-navy.png" alt="CV Immobilier" width="600" height="218">
      <span class="brand-sep" aria-hidden="true"></span>
      <span class="brand-name">louviers<b>.immo</b></span>
    </a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    <nav class="menu" id="menu" aria-label="Navigation principale">
      {items}
      <a class="btn btn-gold" href="{CV_EST}">Estimer mon bien</a>
    </nav>
  </div>
</header>
'''


def footer(root, scripts=()):
    sc = ''.join(f'<script src="{s if s.startswith("http") else root + s}{"" if s.startswith("http") else "?v=" + VER}"></script>\n' for s in scripts)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="f-grid">
      <div class="stack">
        <img src="{root}assets/img/logo-cream.png" alt="CV Immobilier" width="600" height="218" loading="lazy" style="align-self:flex-start">
        <p style="color:#9FB0C0;max-width:28em">louviers.immo est un guide proposé par CV Immobilier, agence immobilière indépendante membre de la FNAIM et du réseau Interkab, à Louviers depuis 1992.</p>
      </div>
      <div>
        <h4>Le guide</h4>
        <ul>
          <li><a href="{root}adresse.html">Mon adresse</a></li>
          <li><a href="{root}commerces.html">Commerces</a></li>
          <li><a href="{root}quartiers.html">Quartiers</a></li>
          <li><a href="{root}prix.html">Prix de l’immobilier</a></li>
          <li><a href="{root}a-vendre.html">Biens à vendre</a></li>
          <li><a href="{root}portraits.html">Portraits</a></li>
          <li><a href="{root}conciergerie.html">S’installer</a></li>
          <li><a href="{root}diagnostics.html">Diagnostics</a></li>
          <li><a href="{root}outils.html">Outils</a></li>
          <li><a href="{root}a-propos.html">À propos</a></li>
        </ul>
      </div>
      <div>
        <h4>Agence de Louviers</h4>
        <ul>
          <li>27 rue du Général de Gaulle<br>27400 Louviers</li>
          <li><a class="tel" href="tel:+33232402228">02 32 40 22 28</a></li>
        </ul>
      </div>
      <div>
        <h4>Saint-Pierre-du-Vauvray</h4>
        <ul>
          <li>15 Grande Rue<br>27430 Saint-Pierre-du-Vauvray</li>
          <li><a class="tel" href="tel:+33279492171">02 79 49 21 71</a></li>
        </ul>
      </div>
    </div>
    <div class="f-bottom">
      <span>© 2026 CV Immobilier · Carte professionnelle CPI 2701 2016 000 005 229</span>
      <nav aria-label="Liens légaux">
        <a href="{root}mentions-legales.html">Mentions légales</a>
        <a href="{root}mentions-legales.html#donnees">Sources des données</a>
        <a href="{CV_SITE}">cvimmobilier.fr</a>
        <a href="https://www.ville-louviers.fr/" target="_blank" rel="noopener">Ville de Louviers</a>
        <a href="https://www.agglo-seine-eure.fr/" target="_blank" rel="noopener">Agglomération Seine-Eure</a>
      </nav>
    </div>
  </div>
</footer>
<script src="{root}assets/site.js?v={VER}"></script>
{sc}</body>
</html>
'''


def search_form(fid, label='Testez une adresse', placeholder='Ex. : rue du Général de Gaulle', btn='Voir mon quartier', chips=True, root=''):
    ch = '''
    <div class="chips" aria-hidden="true"><span class="chip-static">Temps à pied, à vélo, en voiture</span><span class="chip-static">Écoles</span><span class="chip-static">Commerces</span><span class="chip-static">Bus, gare, A13</span></div>''' if chips else ''
    return f'''<form class="search" role="search" action="{root}adresse.html" autocomplete="off">
    <label for="{fid}">{label}</label>
    <div class="search-row">
      <div class="search-field">{PIN}
        <input id="{fid}" name="q" type="text" placeholder="{placeholder}" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="{fid}-list" enterkeyhint="search">
      </div>
      <button class="btn btn-navy" type="submit">{btn}</button>
      <ul class="suggest" id="{fid}-list" role="listbox" aria-label="Suggestions d’adresses"></ul>
    </div>{ch}
  </form>'''


import re
def tag_estimation(content, path):
    pos = path.replace('.html', '').replace('/', '-')
    ev = f'plausible-event-name=Estimation+Click plausible-event-position={pos}'
    def rep(m):
        tag = m.group(0)
        if 'plausible-event-name' in tag:
            return tag
        if 'class="' in tag:
            return tag.replace('class="', f'class="{ev} ', 1)
        return tag.replace('<a ', f'<a class="{ev}" ', 1)
    return re.sub(r'<a [^>]*href="' + re.escape(CV_EST) + r'"[^>]*>', rep, content)


PH_COLOR = {'commerces.html': 'ocre', 'conciergerie.html': 'pomme', 'diagnostics.html': 'brique', 'prix.html': 'ciel',
            'quartiers.html': 'pomme', 'outils.html': 'ocre', 'a-propos.html': 'brique', 'portraits.html': 'brique', 'adresse.html': 'ciel'}


OG_IMG = {'portraits/maison-barbe.html': 'maison-barbe', 'portraits/institut-des-portes-de-l-eau.html': 'institut-des-portes-de-l-eau',
          'portraits/aux-delices-de-louviers.html': 'aux-delices-de-louviers', 'portraits/georget-cycles.html': 'georget-cycles'}
_dims = {}


def img_dims(src_rel):
    from PIL import Image
    if src_rel not in _dims:
        try:
            _dims[src_rel] = Image.open(os.path.join(OUT, src_rel)).size
        except Exception:
            _dims[src_rel] = None
    return _dims[src_rel]


def pictures(content, path):
    """Chaque photo .jpg devient <picture> WebP + JPG de secours, avec largeur et hauteur."""
    depth = path.count('/')
    def rep(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+\.jpg)"', tag).group(1)
        rel = os.path.normpath(os.path.join(os.path.dirname(path), src))
        if not os.path.exists(os.path.join(OUT, rel[:-4] + '.webp')):
            return tag
        if 'width=' not in tag:
            d = img_dims(rel)
            if d:
                tag = tag.replace('<img ', f'<img width="{d[0]}" height="{d[1]}" ', 1)
        return f'<picture><source srcset="{src[:-4]}.webp" type="image/webp">{tag}</picture>'
    return re.sub(r'<img [^>]*src="[^"]+\.jpg"[^>]*>', rep, content)


def sans_passerelle(content):
    """Retire les blocs « biens à vendre » quand PASSERELLE = False."""
    import re
    content = re.sub(r'\n<section class="section"[^>]*data-biens-sec>.*?</section>\n', '\n', content, flags=re.S)
    content = re.sub(r'    <div class="stack-lg biens-pres".*?(?=    <div class="(?:avant|alerte))', '', content, flags=re.S)
    content = re.sub(r'\s*<li><a href="[^"]*a-vendre\.html">Biens à vendre</a></li>', '', content)
    return re.sub(r'<script src="[^"]*assets/biens\.js[^"]*"></script>\n', '', content)


def write(path, content):
    if not PASSERELLE:
        if path == 'a-vendre.html':
            return
        content = sans_passerelle(content)
    content = tag_estimation(content, path)
    if path in OG_IMG:
        content = content.replace(f'{DOMAIN}assets/img/og-image.png', f'{DOMAIN}assets/img/og/{OG_IMG[path]}.jpg')
    content = pictures(content, path)
    content = content.replace('<section class="page-head">', f'<section class="page-head ph-{PH_COLOR.get(path, "ciel")}">')
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print('écrit', path, len(content))


HERO_SVG = '''<svg viewBox="0 0 600 580" role="img" aria-label="Illustration : ce qui se trouve à 5, 10 et 15 minutes à pied d’une adresse">
        <g stroke="#34506A" stroke-width="10" stroke-linecap="round" fill="none"><path d="M-20 120 L620 200"/><path d="M-20 400 L620 330"/><path d="M180 -20 L230 600"/><path d="M420 -20 L380 600"/></g>
        <g stroke="#2D465E" stroke-width="5" stroke-linecap="round" fill="none"><path d="M60 -20 L110 600"/><path d="M520 -20 L500 600"/><path d="M-20 260 L620 270"/><path d="M-20 500 L620 470"/><path d="M300 -20 L310 600"/><path d="M-20 40 L620 90"/></g>
        <path d="M-30 460 C 90 420, 140 330, 250 350 S 420 470, 520 380 S 610 240, 640 250" stroke="#4F7F98" stroke-width="26" fill="none" stroke-linecap="round"/>
        <text x="500" y="345" fill="#8FB3C6" font-family="Fraunces, Georgia, serif" font-style="italic" font-size="17">l’Eure</text>
        <circle cx="300" cy="270" r="92" fill="#C9A961" fill-opacity="0.10" stroke="#C9A961" stroke-opacity="0.8" stroke-width="1.5" stroke-dasharray="4 6"/>
        <circle cx="300" cy="270" r="180" fill="none" stroke="#C9A961" stroke-opacity="0.55" stroke-width="1.5" stroke-dasharray="4 6"/>
        <circle cx="300" cy="270" r="262" fill="none" stroke="#C9A961" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="4 6"/>
        <g font-family="Outfit, sans-serif" font-size="12" font-weight="600" letter-spacing="1.5" fill="#E0C98F"><text x="318" y="188">5 MIN</text><text x="324" y="100">10 MIN</text><text x="330" y="18">15 MIN</text></g>
        <g font-family="Outfit, sans-serif" font-size="13" fill="#F8F6F2">
          <circle cx="238" cy="232" r="7" fill="#F8F6F2"/><text x="162" y="220">Boulangerie</text>
          <circle cx="360" cy="318" r="7" fill="#F8F6F2"/><text x="374" y="322">Pharmacie</text>
          <circle cx="410" cy="170" r="7" fill="#F8F6F2"/><text x="424" y="174">École</text>
          <circle cx="170" cy="370" r="7" fill="#F8F6F2"/><text x="72" y="398">Arrêt de bus</text>
          <circle cx="470" cy="420" r="7" fill="#F8F6F2"/><text x="484" y="424">Marché</text>
          <circle cx="120" cy="120" r="7" fill="#F8F6F2"/><text x="134" y="124">Médecin</text>
        </g>
        <g transform="translate(300 270)"><circle r="26" fill="#C9A961" fill-opacity="0.25"/><circle r="13" fill="#C9A961" stroke="#111F2C" stroke-width="3"/></g>
      </svg>'''

PRIX_SVG = '''<svg viewBox="0 0 640 560" role="img" aria-label="Illustration de la carte des ventes : chaque point est une vente, coloré selon le prix au mètre carré">
        <g stroke="#28415A" stroke-width="7" stroke-linecap="round" fill="none"><path d="M-20 140 L660 210"/><path d="M-20 420 L660 340"/><path d="M200 -20 L240 580"/><path d="M440 -20 L400 580"/><path d="M-20 280 L660 290"/><path d="M90 -20 L130 580"/><path d="M560 -20 L530 580"/></g>
        <path d="M-30 480 C 110 440, 160 340, 280 360 S 450 480, 560 390 S 640 250, 680 260" stroke="#3E6A80" stroke-width="22" fill="none" stroke-linecap="round"/>
        <g><circle cx="250" cy="240" r="7" fill="#E0C98F"/><circle cx="276" cy="262" r="6" fill="#C9A961"/><circle cx="300" cy="228" r="8" fill="#E0C98F"/><circle cx="318" cy="270" r="6" fill="#9C7C33"/><circle cx="232" cy="300" r="6" fill="#C9A961"/><circle cx="340" cy="200" r="7" fill="#E0C98F"/><circle cx="150" cy="170" r="6" fill="#8FB3C6"/><circle cx="120" cy="230" r="7" fill="#8FB3C6"/><circle cx="170" cy="110" r="6" fill="#C9A961"/><circle cx="470" cy="150" r="7" fill="#8FB3C6"/><circle cx="500" cy="210" r="6" fill="#C9A961"/><circle cx="430" cy="250" r="8" fill="#E0C98F"/><circle cx="380" cy="120" r="6" fill="#8FB3C6"/><circle cx="80" cy="330" r="6" fill="#8FB3C6"/><circle cx="360" cy="440" r="7" fill="#C9A961"/><circle cx="420" cy="470" r="6" fill="#8FB3C6"/><circle cx="560" cy="300" r="7" fill="#E0C98F"/><circle cx="200" cy="420" r="6" fill="#9C7C33"/><circle cx="270" cy="160" r="6" fill="#C9A961"/><circle cx="590" cy="120" r="6" fill="#8FB3C6"/></g>
      </svg>'''

QUARTIERS = [
    ('Saint-Germain –', 'Les Acacias'), ('La Londe –', 'Saint-Hildevert'), ('Saint-Jean –', 'Les Hayes Melines'),
    ('Côte de la Justice –', 'Saint-Lubin'), ('Les', 'Amoureux'), ('Pampoule –', 'La Ravine')]
COMMUNES = ['Saint-Pierre-du-Vauvray', 'Le Vaudreuil', 'Incarville', 'Val-de-Reuil', "Pont-de-l'Arche", 'Andé']


def form_proposer(r, where):
    return f'''<form class="lform plausible-event-name=Proposer+Commerce plausible-event-position={where}" name="proposer-commerce" method="POST" action="{r}merci.html" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="proposer-commerce">
      <input type="hidden" name="page" value="{where}">
      <p hidden><label>Ne pas remplir <input name="bot-field"></label></p>
      <div class="lform-grid">
        <div class="field"><label for="pc-nom-{where}">Nom du commerce</label><input id="pc-nom-{where}" name="commerce" required></div>
        <div class="field"><label for="pc-adr-{where}">Adresse</label><input id="pc-adr-{where}" name="adresse" required></div>
        <div class="field"><label for="pc-contact-{where}">Votre nom</label><input id="pc-contact-{where}" name="contact" required></div>
        <div class="field"><label for="pc-mail-{where}">Votre adresse mail</label><input id="pc-mail-{where}" name="email" type="email" required></div>
        <div class="field"><label for="pc-tel-{where}">Téléphone (facultatif)</label><input id="pc-tel-{where}" name="telephone" type="tel"></div>
        <div class="field"><label for="pc-msg-{where}">Votre message (facultatif)</label><textarea id="pc-msg-{where}" name="message" rows="3"></textarea></div>
      </div>
      <label class="check"><input type="checkbox" name="consentement" value="oui" required> <span>J’accepte que CV Immobilier utilise ces informations pour me recontacter au sujet de louviers.immo (<a href="{r}mentions-legales.html#formulaires">en savoir plus</a>).</span></label>
      <button class="btn btn-navy" type="submit" style="align-self:flex-start">Envoyer ma demande</button>
    </form>'''


def adr_link(root, q):
    return f'{root}adresse.html?q=' + q.replace(' ', '+').replace("'", '%27')


def q_grid(root, n0=1):
    cards = [f'''<a class="q-card feature rv" href="{root}quartiers/centre-ville.html">
        <span class="q-tag">Portrait en ligne</span>
        <div>
          <div class="t">Centre-ville</div>
          <p>L’église Notre-Dame, la place de la Halle aux Drapiers, les bords de l’Eure : ici, tout se fait à pied.</p>
          <div class="more">Lire le portrait du quartier</div>
        </div>
      </a>''']
    for a, b in QUARTIERS:
        cards.append(f'''<div class="q-card rv">
        <span class="soon">À venir</span>
        <div><div class="t">{a}<br><span class="it">{b}</span></div><div class="s">Portrait du quartier en préparation</div></div>
      </div>''')
    pills = ''.join(f'<a class="pill" href="{adr_link(root, c)}">{c}</a>' for c in COMMUNES)
    return f'''<div class="q-grid">
      {"".join(cards)}
    </div>
    <div class="communes"><span>Et autour, explorez :</span>{pills}</div>'''


# =========================================================
# ACCUEIL
# =========================================================
STREET_SVG = open(os.path.join(HERE, 'illustrations', 'street.svg')).read()
PIN_X = open(os.path.join(HERE, 'illustrations', 'street_pinx.txt')).read().strip()

def ico(d):
    return f'<svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="#1B2E40" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

ENVIES = [
    ('restaurer', 'Se restaurer', 'Brasseries, tables du midi et du soir', 'pomme',
     '<path d="M12 6v10a3 3 0 0 0 6 0V6M15 6v28M27 34V6c-4 2-5 8-5 13h5"/>'),
    ('cafes', 'Cafés & bars', 'Une terrasse, un verre en fin de journée', 'brique',
     '<path d="M8 15h20v8a9 9 0 0 1-9 9h-2a9 9 0 0 1-9-9z"/><path d="M28 17h2a4 4 0 0 1 0 8h-3M14 5c-1 2 1 3 0 6M20 5c-1 2 1 3 0 6"/>'),
    ('boulangeries', 'Boulangeries', 'Le pain du matin, les douceurs du dimanche', 'ciel',
     '<path d="M7 29c-3-3 9-19 19-22 4-1 7 2 6 6-3 10-19 22-22 19z"/><path d="M15 17l5 5M19 13l5 5M23 10l4 4M12 21l4 4"/>'),
    ('bouche', 'Métiers de bouche', 'Charcutiers, fromagers, primeurs, cavistes', 'ocre',
     '<path d="M5 27l15-17 15 17z"/><path d="M5 27v4h30v-4"/><circle cx="17" cy="22" r="1.6"/><circle cx="24" cy="20" r="1.2"/><circle cx="21" cy="25" r="1"/>'),
    ('habiller', 'S’habiller', 'Mode, chaussures, bijoux', 'brique',
     '<path d="M20 12a3 3 0 1 1 3-3c0 2-3 2-3 4v2"/><path d="M20 15L5 26a2 2 0 0 0 1 4h28a2 2 0 0 0 1-4z"/>'),
    ('artisans', 'Artisans', 'Plombiers, électriciens, menuisiers, couvreurs', 'ciel',
     '<path d="M6 34l14-14"/><path d="M18 14l8-8 8 8-4 4-4-4-4 4z"/><path d="M22 18l4 4"/>'),
    ('sport', 'Clubs sportifs', 'Tennis, volley, pétanque, patinage : une quarantaine de clubs', 'pomme',
     '<circle cx="20" cy="20" r="14"/><path d="M8 13c6 3 10 9 10 21M32 13c-6 3-10 9-10 21M6 22h28"/>'),
    ('notaires', 'Notaires & financement', 'Les offices notariaux, nos courtiers partenaires', 'ocre',
     '<path d="M10 5h14l6 6v24H10z"/><path d="M24 5v6h6M15 18h10M15 23h10M15 28h6"/>'),
]

def page_index():
    r = ''
    tiles = ''.join(
        f'<a class="envie envie-{c}" href="{r}commerces.html#{k}">{ico(d)}<span class="en">{l}</span><span class="ed">{s}</span></a>'
        for k, l, s, c, d in ENVIES)
    faces = ''.join(
        f'<span class="face" tabindex="0"><img src="{r}assets/img/equipe/{img}.jpg" alt="{n}, {role.lower()}" width="400" height="400" loading="lazy">'
        f'<span class="face-tip" aria-hidden="true"><b>{n}</b>{role}</span></span>'
        for n, role, tel, img in TEAM)
    body = head('louviers.immo — Louviers, mode d’emploi · le guide par CV Immobilier',
                'Le guide de Louviers et de l’Agglomération Seine-Eure : testez une adresse pour voir les commerces, écoles et temps de trajet autour, découvrez les quartiers, les prix réels de l’immobilier et les portraits de ceux qui font Louviers.',
                'index.html', r, jsonld=ORG)
    body += header(None, r)
    body += f'''<main id="contenu">
<section class="hero2">
  <div class="wrap hero2-text">
    <h1>Louviers,<br>mode d’emploi.</h1>
    <p class="lede">Le guide de celles et ceux qui vivent à Louviers, et de celles et ceux qui s’apprêtent à y poser leurs cartons.</p>
    {search_form('adresse-hero', label='Entrez une adresse', btn='Voir ce qu’il y a autour')}
  </div>
  <div class="street-wrap" style="--pin:{PIN_X}%">
    <div class="callout" aria-hidden="true">
      <div class="cl-t">Une adresse du centre-ville</div>
      <ul>
        <li><span>Boulangerie</span><b>3 min à pied</b></li>
        <li><span>École primaire</span><b>6 min à pied</b></li>
        <li><span>Marché du samedi</span><b>8 min à pied</b></li>
        <li><span>Gare de Val-de-Reuil</span><b>12 min en voiture</b></li>
      </ul>
      <div class="cl-n">Exemple de résultat</div>
    </div>
    {STREET_SVG}
  </div>
</section>

<div class="ribbon" aria-hidden="true"><div class="ribbon-track"><span>Le marché du mercredi et du samedi</span><span>Les bords de l’Eure</span><span>L’église Notre-Dame</span><span>La place de la Halle aux Drapiers</span><span>La patinoire Glacéo</span><span>Le complexe aquatique Caséo</span><span>Une quarantaine de clubs sportifs</span><span>Rouen et l’A13 tout près</span><span>Le marché du mercredi et du samedi</span><span>Les bords de l’Eure</span><span>L’église Notre-Dame</span><span>La place de la Halle aux Drapiers</span><span>La patinoire Glacéo</span><span>Le complexe aquatique Caséo</span><span>Une quarantaine de clubs sportifs</span><span>Rouen et l’A13 tout près</span></div></div>

<section class="section envies-sec">
  <div class="wrap">
    <div class="head2">
      <h2>Envie de quoi ?</h2>
      <p>Notre sélection de bonnes adresses à Louviers et dans les communes voisines, rangées comme on les cherche.</p>
    </div>
    <div class="envies stagger">{tiles}</div>
    <p class="envies-more"><a class="link-u" href="{r}commerces.html">Voir toute notre sélection de bonnes adresses</a></p>
  </div>
</section>

<section class="section install-sec">
  <div class="wrap">
    <div class="head2">
      <h2>Vendre, louer, emménager : le pas-à-pas</h2>
      <p>Les démarches qui reviennent à chaque projet, expliquées simplement, avec les bons liens.</p>
    </div>
    <div class="install stagger">
      <a class="inst inst-diag" href="{r}diagnostics.html">
        <svg width="56" height="56" viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 26L28 11l18 15v21H10z"/><path d="M20 47V34h16v13"/><path d="M38 6h10v10M48 6l-9 9"/></svg>
        <span class="inst-t">Les diagnostics, mode d’emploi</span>
        <span class="inst-d">Appartement ou maison, année de construction, vente ou location : la liste de ce qu’il faut faire réaliser, en cinq questions.</span>
        <span class="inst-go">Voir mes diagnostics</span>
      </a>
      <a class="inst inst-cg" href="{r}conciergerie.html">
        <svg width="56" height="56" viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="28" r="9"/><path d="M27 28h22M42 28v7M49 28v5"/><circle cx="18" cy="28" r="3"/></svg>
        <span class="inst-t">S’installer, la conciergerie pratique</span>
        <span class="inst-d">Eau, électricité, gaz, box internet, déchets, démarches : qui appeler, dans quel ordre, avec plusieurs prestataires à chaque fois.</span>
        <span class="inst-go">Préparer mon emménagement</span>
      </a>
      <a class="inst inst-eau" href="{r}diagnostics.html#assainissement">
        <svg width="56" height="56" viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M28 7c8 11 14 18 14 26a14 14 0 0 1-28 0c0-8 6-15 14-26z"/><path d="M21 35a7 7 0 0 0 7 7"/></svg>
        <span class="inst-t">Contrôle d’assainissement</span>
        <span class="inst-d">Obligatoire à la vente dans l’Agglomération Seine-Eure, même raccordé au tout-à-l’égout.</span>
        <span class="inst-go">Comment le demander</span>
      </a>
    </div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap feat">
    <div class="feat-car" id="feat-car" aria-roledescription="carrousel" aria-label="Nos portraits">
      <div class="feat-track" id="feat-track">
        <a class="feat-card" href="{r}portraits/maison-barbe.html">
          <div class="feat-art feat-photo"><img src="{r}assets/img/portraits/maison-barbe-facade.jpg" alt="" width="1800" height="1201" loading="lazy"></div>
          <div class="feat-body">
            <span class="kicker">Maison Barbé · Centre-ville</span>
            <h2>La charcuterie du Parvis fait peau neuve</h2>
            <p>Rue du Maréchal Foch, Sylvie et Patrice Barbé perpétuent une charcuterie artisanale, entièrement repensée après de gros travaux.</p>
            <span class="link-u">Lire le portrait</span>
          </div>
        </a>
      </div>
      <div class="feat-nav" id="feat-nav" hidden>
        <button type="button" class="feat-btn" data-dir="-1" aria-label="Portrait précédent"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
        <div class="feat-dots" id="feat-dots"></div>
        <button type="button" class="feat-btn" data-dir="1" aria-label="Portrait suivant"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
    </div>
    <div class="feat-side">
      <h3>Ceux qui font Louviers</h3>
      <p>Commerçants, artisans, restaurateurs : notre équipe pousse une porte et raconte une histoire. Vous tenez une boutique à Louviers et vous aimeriez raconter la vôtre ? C’est gratuit.</p>
      <div class="feat-links">
        <a class="link-u" href="{r}portraits.html">Tous les portraits</a>
        <a class="link-u" href="mailto:{MAIL}?subject=Portrait%20louviers.immo">Proposer un portrait</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="quartiers">
  <div class="wrap">
    <div class="head2">
      <h2>Sept quartiers, sept façons de vivre Louviers</h2>
      <p>Ambiance, écoles, types de maisons, prix : chaque quartier raconté par ceux qui le connaissent depuis 1992.</p>
    </div>
    {q_grid(r)}
  </div>
</section>

<section class="section bg-deep" id="prix">
  <div class="wrap split">
    <div class="a stack-lg">
      <h2>Pas des estimations : des ventes réelles</h2>
      <p class="lede">Chaque point est une vente enregistrée par l’État (base DVF), avec son prix et sa surface. Mis à jour à chaque publication des données.</p>
      <div class="kpis">
        <div class="kpi"><div class="l">Maison</div><div class="v" data-kpi="maison">—</div><div class="u">€/m² médian</div></div>
        <div class="kpi"><div class="l">Appartement</div><div class="v" data-kpi="appart">—</div><div class="u">€/m² médian</div></div>
        <div class="kpi"><div class="l">Ventes</div><div class="v" data-kpi="ventes">—</div><div class="u">sur 12 mois</div></div>
      </div>
      <p class="note" data-kpi-period>Louviers, source DVF</p>
      <a class="btn btn-gold" style="align-self:flex-start" href="{r}prix.html">Explorer la carte des ventes</a>
    </div>
    <figure class="b art">
      {PRIX_SVG}
      <figcaption class="legend"><span><span style="margin-right:14px"><i style="background:#8FB3C6"></i>moins cher</span><span style="margin-right:14px"><i style="background:#C9A961"></i>médian</span><span><i style="background:#E0C98F"></i>plus cher</span></span><span>Illustration</span></figcaption>
    </figure>
  </div>
</section>

<section class="section" id="a-vendre" data-biens-sec>
  <div class="wrap">
    <div class="head2">
      <h2>Les derniers biens à vendre</h2>
      <p>Maisons et appartements proposés par notre agence, CV Immobilier, à Louviers et dans les communes voisines. Un clic ouvre l’annonce complète.</p>
    </div>
    <div class="biens" data-biens data-max="6" data-where="accueil"></div>
    <div class="biens-foot">
      <p class="note" data-biens-maj>Annonces de cvimmobilier.fr, mises à jour chaque nuit.</p>
      <a class="link-u" href="{r}a-vendre.html">Voir tous les biens à vendre</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head2">
      <h2>Faire ses comptes avant de visiter</h2>
    </div>
    <div class="t-grid">
      <a class="t-card t-pomme" href="{r}outils.html#notaire">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#1B2E40" stroke-width="1.5" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h2M12 11h2M8 15h2M12 15h2M8 19h8"/></svg>
        <span class="t">Frais de notaire</span><p>Ancien ou neuf, le montant à prévoir en plus du prix, aux taux en vigueur dans l’Eure.</p><span class="go">Calculer</span>
      </a>
      <a class="t-card t-ciel" href="{r}outils.html#emprunt">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#1B2E40" stroke-width="1.5" aria-hidden="true"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/></svg>
        <span class="t">Capacité d’emprunt</span><p>Le budget accessible selon vos revenus, vos charges et la durée du prêt.</p><span class="go">Simuler</span>
      </a>
      <a class="t-card dark" href="{CV_EST}">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true"><path d="M12 2l2.9 6.3L22 9.2l-5.2 4.7L18.2 21 12 17.3 5.8 21l1.4-7.1L2 9.2l7.1-.9z"/></svg>
        <span class="t">Estimer mon bien</span><p>Un avis de valeur argumenté par l’équipe CV Immobilier, gratuit et sans engagement.</p><span class="go">Demander une estimation</span>
      </a>
    </div>
  </div>
</section>

<section class="section team-sec">
  <div class="wrap team-band">
    <div class="faces">{faces}</div>
    <blockquote>« Depuis 1992, on nous pose les mêmes questions : l’école est-elle loin, où acheter son pain, combien de temps pour la gare ? louviers.immo, c’est notre réponse, ouverte à tous, que vous achetiez avec nous ou non. »</blockquote>
    <p class="team-sign"><b>Nicolas Vayrac</b>, directeur de CV Immobilier, et toute l’équipe des agences de Louviers et de Saint-Pierre-du-Vauvray. <a class="link-u" href="{r}a-propos.html">Rencontrer l’équipe</a></p>
  </div>
</section>
</main>
'''
    body += footer(r, ['data/portraits.js', 'assets/biens.js'])
    write('index.html', body)


# =========================================================
# MON ADRESSE
# =========================================================
def page_adresse():
    r = ''
    ex = [('Place de la Halle aux Drapiers 27400 Louviers', 'Place de la Halle aux Drapiers, Louviers'),
          ('15 Grande Rue 27430 Saint-Pierre-du-Vauvray', 'Grande Rue, Saint-Pierre-du-Vauvray'),
          ('Le Vaudreuil', 'Le Vaudreuil')]
    exl = ''.join(f'<a class="pill" href="{adr_link(r, q)}">{l}</a>' for q, l in ex)
    css = f'<link rel="stylesheet" href="{r}assets/vendor/leaflet/leaflet.css">\n'
    body = head('Mon adresse — vivre à Louviers, rue par rue · louviers.immo',
                'Entrez une adresse à Louviers ou dans l’Agglomération Seine-Eure : commerces les plus proches, écoles, arrêts de bus, gare, temps de trajet à pied, à vélo et en voiture, et prix des ventes autour.',
                'adresse.html', r, css=css)
    body += header('adresse.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  
  </div>
  <div class="wrap res-head">
    <div style="max-width:780px">
      <div class="crumbs"><a href="{r}index.html">Accueil</a> · Mon adresse</div>
      <span class="eyebrow">Vivre ici</span>
      <h1 id="res-title" style="margin-top:12px">Une adresse, <span class="it">tout ce qu’il y a autour.</span></h1>
      <div class="res-sub"><span id="res-city">Louviers et l’Agglomération Seine-Eure</span><span class="dot">·</span><span>Temps estimés · données OpenStreetMap</span></div>
    </div>
    {search_form('adresse-q', label='Tester une adresse', placeholder='Numéro, rue, commune', btn='Rechercher', chips=False)}
  </div>
</section>

<section class="section" id="intro" style="padding-top:56px">
  <div class="wrap stack-lg" style="max-width:860px">
    <p class="lede" id="intro-msg">Tapez une adresse ci-dessus et choisissez-la dans la liste : vous verrez les commerces, écoles, arrêts de bus et services les plus proches, avec les temps de trajet et les prix des ventes autour.</p>
    <div class="communes" style="margin-top:0"><span>Exemples :</span>{exl}</div>
  </div>
</section>

<div id="results" hidden>
<section class="section" style="padding-top:56px;padding-bottom:40px">
  <div class="wrap">
    <p id="far" class="empty-data" hidden style="margin-bottom:28px">Cette adresse est assez loin de Louviers : louviers.immo est conçu pour Louviers et l’Agglomération Seine-Eure, les résultats restent indicatifs.</p>
    <div class="res-grid">
      <div class="stack">
        <span class="eyebrow">Temps de trajet</span>
        <h2 style="font-size:clamp(28px,2.6vw,36px)">Depuis cette adresse, <span class="it" id="mode-label">à pied</span></h2>
        <div class="modes" role="group" aria-label="Mode de déplacement" style="grid-template-columns:repeat(3,minmax(0,1fr))">
          <button type="button" class="mode" data-mode="walk" aria-pressed="true">À pied</button>
          <button type="button" class="mode" data-mode="bike" aria-pressed="false">À vélo</button>
          <button type="button" class="mode" data-mode="car" aria-pressed="false">En voiture</button>
        </div>
        <div id="trips" aria-live="polite"></div>
        <div class="tgroup"><h3>Bus · arrêts les plus proches</h3><div id="bus"></div></div>
        <p class="note">Temps estimés à partir de la distance à vol d’oiseau (corrigée des détours), à 4,8 km/h à pied et 15 km/h à vélo. Données OpenStreetMap : si un lieu manque ou a fermé, <a href="mailto:{MAIL}?subject=louviers.immo%20%E2%80%94%20correction">signalez-le-nous</a>.</p>
      </div>
      <div class="map-box">
        <div class="map" id="map" role="region" aria-label="Carte du quartier"></div>
        <div class="map-badge"><span class="pin-me" style="box-shadow:none;width:14px;height:14px;border-width:2px"></span><span>Votre adresse · cercles ≈ 5, 10, 15 min à pied</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:24px;padding-bottom:56px">
  <div class="wrap stack-lg">
    <div class="head" style="margin-bottom:0">
      <div><span class="eyebrow">À deux pas</span><h2>Les commerces <span class="it">les plus proches</span></h2></div>
      <div class="cats" role="group" aria-label="Filtrer par catégorie">
        <button type="button" class="cat" data-fam="all" aria-pressed="true">Tous</button>
        <button type="button" class="cat" data-fam="alim" aria-pressed="false">Alimentation</button>
        <button type="button" class="cat" data-fam="resto" aria-pressed="false">Restaurants</button>
        <button type="button" class="cat" data-fam="sante" aria-pressed="false">Santé</button>
        <button type="button" class="cat" data-fam="serv" aria-pressed="false">Services</button>
        <button type="button" class="cat" data-fam="shop" aria-pressed="false">Boutiques</button>
      </div>
    </div>
    <div class="shops" id="shops" aria-live="polite"></div>
    <p class="note"><span class="pin-n star" style="display:inline-flex;width:22px;height:22px;font-size:11px;vertical-align:middle;margin-right:6px">1</span>En doré : les commerces dont nous avons fait le portrait.</p>
  </div>
</section>

<section style="padding-bottom:var(--section)">
  <div class="wrap">
    <div class="box-sand split" style="align-items:center">
      <div class="a stack">
        <span class="eyebrow">Les prix autour</span>
        <h2 style="font-size:clamp(28px,2.6vw,38px)">Ce qui s’est vendu <span class="it">à moins de 500 m</span></h2>
        <p class="muted">Ventes réelles enregistrées par l’État (DVF). Médiane calculée dès 3 ventes.</p>
        <a class="link-u" id="prices-link" href="{r}prix.html" style="align-self:flex-start">Voir la carte des ventes</a>
      </div>
      <div class="b stack">
        <div class="kpis" id="prices"></div>
        <div class="two">
          <a class="btn btn-navy" href="{CV_SITE}">Nos biens à vendre</a>
          <a class="btn btn-gold" href="{CV_EST}">Faire estimer un bien</a>
        </div>
      </div>
    </div>

    <div class="stack-lg biens-pres" data-biens-sec hidden>
      <div class="head2" style="margin-bottom:0">
        <h2 style="font-size:clamp(28px,2.6vw,38px)">À vendre près de cette adresse</h2>
        <p>Les biens de notre agence les plus proches, dans la commune ou les communes voisines.</p>
      </div>
      <div class="biens" id="biens-pres"></div>
      <div class="biens-foot"><p class="note" data-biens-maj>Annonces de cvimmobilier.fr, mises à jour chaque nuit.</p><a class="link-u" href="{r}a-vendre.html">Tous les biens à vendre</a></div>
    </div>

    <div class="avant" id="avant">
      <div class="head2" style="margin-bottom:0">
        <h2 style="font-size:clamp(28px,2.6vw,38px)">Votre rue, <span class="it">hier et aujourd’hui</span></h2>
        <p>Faites glisser la poignée pour comparer votre quartier vu du ciel dans les années 1950 et aujourd’hui.</p>
      </div>
      <div class="av-rue" id="av-rue" hidden>
        <div><span class="av-plaque" id="av-plaque"></span></div>
        <div class="stack">
          <p class="av-texte" id="av-texte"></p>
          <p class="note" id="av-src"></p>
          <div id="av-voir-w" class="stack" hidden><b style="color:var(--navy);font-weight:500">À voir en passant</b><ul id="av-voir" style="padding-left:20px"></ul></div>
        </div>
      </div>
      <div class="av-box">
        <div id="av-map" role="region" aria-label="Comparaison des photographies aériennes"></div>
        <span class="av-lab g" id="av-lg">1950–1965</span><span class="av-lab d" id="av-ld">Aujourd’hui</span>
        <div id="av-bar" aria-hidden="true"></div>
      </div>
      <label class="small muted" for="av-range">Position du curseur</label>
      <input id="av-range" type="range" min="0" max="100" value="50">
      <p class="note">Photographies aériennes : IGN, BD ORTHO® historique 1950-1965 et BD ORTHO®, via la Géoplateforme (licence ouverte Etalab).</p>
    </div>

    <div class="alerte no-print" id="alerte">
      <div class="stack">
        <h2 style="font-size:clamp(26px,2.4vw,34px)">Recevoir les biens à vendre dans ce quartier</h2>
        <p class="muted">Laissez votre adresse mail : l’équipe CV Immobilier vous prévient quand un bien se vend ou se met en vente près de cette adresse.</p>
      </div>
      <form class="lform plausible-event-name=Alerte+Quartier" name="alerte-quartier" method="POST" action="{r}merci.html" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="alerte-quartier">
        <input type="hidden" name="adresse" id="alerte-adresse" value="">
        <p hidden><label>Ne pas remplir <input name="bot-field"></label></p>
        <div class="field"><label for="alerte-mail">Votre adresse mail</label><input id="alerte-mail" name="email" type="email" required autocomplete="email"></div>
        <label class="check"><input type="checkbox" name="consentement" value="oui" required> <span>J’accepte de recevoir des informations de CV Immobilier sur ce quartier. Désinscription à tout moment (<a href="{r}mentions-legales.html#formulaires">en savoir plus</a>).</span></label>
        <button class="btn btn-gold" type="submit" style="align-self:flex-start">Me prévenir</button>
      </form>
    </div>
  </div>
</section>
</div>
</main>
'''
    body += footer(r, ['assets/vendor/leaflet/leaflet.js', 'assets/map.js', 'data/portraits.js', 'data/partenaires.js', 'data/exclusions.js', 'data/rues.js', 'assets/biens.js', 'assets/hier.js', 'assets/adresse.js'])
    write('adresse.html', body)


# =========================================================
# PRIX
# =========================================================
def page_prix():
    r = ''
    css = f'<link rel="stylesheet" href="{r}assets/vendor/leaflet/leaflet.css">\n'
    body = head('Prix de l’immobilier à Louviers : les ventes réelles, sur la carte · louviers.immo',
                'Prix au m² à Louviers et dans l’Agglomération Seine-Eure à partir des ventes réelles enregistrées par l’État (DVF) : carte des ventes, médianes maisons et appartements par commune.',
                'prix.html', r, css=css)
    body += header('prix.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap" style="max-width:var(--wrap)">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · Prix</div>
    <span class="eyebrow">Observatoire des prix</span>
    <h1 style="margin-top:12px">Prix de l’immobilier à Louviers.<br><span class="it">Les ventes réelles.</span></h1>
    <p class="lede" style="margin-top:20px">Chaque point de la carte est une vente enregistrée par l’État (base DVF) : prix, surface, date. Pas une estimation d’algorithme.</p>
    <p class="note" style="margin-top:14px">Période couverte : <span id="period">—</span> · Mise à jour : <span id="updated">—</span></p>
  </div>
</section>

<section class="section" style="padding-top:48px">
  <div class="wrap stack-lg">
    <div id="no-data" class="empty-data" hidden>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" style="flex-shrink:0;margin-top:2px"><circle cx="12" cy="12" r="10"/><path d="M12 8v5M12 16h.01"/></svg>
      <div><strong>Les données de ventes sont en cours d’intégration.</strong><br>La carte et les prix au m² s’afficheront ici très bientôt.</div>
    </div>
    <form class="filters" onsubmit="return false" aria-label="Filtres">
      <div class="field"><label for="f-type">Type de bien</label>
        <select id="f-type"><option value="all">Maisons et appartements</option><option value="M">Maisons</option><option value="A">Appartements</option></select></div>
      <div class="field"><label for="f-commune">Commune</label>
        <select id="f-commune"><option value="all">Toutes les communes</option></select></div>
      <div class="field"><label for="f-period">Période</label>
        <select id="f-period"><option value="12">12 derniers mois</option><option value="24" selected>24 derniers mois</option><option value="all">Toute la période</option></select></div>
    </form>
    <div class="kpis" style="max-width:820px">
      <div class="kpi light"><div class="l">Maison</div><div class="v" id="k-maison">—</div><div class="u">€/m² médian</div></div>
      <div class="kpi light"><div class="l">Appartement</div><div class="v" id="k-appart">—</div><div class="u">€/m² médian</div></div>
      <div class="kpi light"><div class="l">Ventes</div><div class="v" id="k-ventes">—</div><div class="u">selon les filtres</div></div>
    </div>
    <div class="map-box" style="height:clamp(420px,68vh,760px)">
      <div class="map" id="map" role="region" aria-label="Carte des ventes"></div>
    </div>
    <div class="legend" aria-label="Légende">
      <span><i style="background:#4F7F98"></i><span id="lg-low">moins cher</span></span>
      <span><i style="background:#C9A961"></i>dans la moyenne</span>
      <span><i style="background:#6B5420"></i><span id="lg-high">plus cher</span></span>
      <span class="muted">· couleurs calculées sur la sélection en cours (tiers)</span>
    </div>

    <div class="stack" style="margin-top:24px">
      <h2 style="font-size:clamp(28px,2.6vw,38px)">Par commune</h2>
      <div class="table-wrap"><table class="data">
        <thead><tr><th scope="col">Commune</th><th scope="col" class="num">Ventes</th><th scope="col" class="num">Maison · €/m²</th><th scope="col" class="num">Appartement · €/m²</th></tr></thead>
        <tbody id="t-body"></tbody>
      </table></div>
      <p class="note">Médianes affichées à partir de 5 ventes.</p>
    </div>
  </div>
</section>

<section class="section" id="estimation" style="padding-top:0">
  <div class="wrap">
    <div class="estim">
      <div class="stack">
        <span class="eyebrow">Estimation rapide</span>
        <h2 style="font-size:clamp(28px,2.6vw,38px)">Une première fourchette pour votre bien</h2>
        <p class="muted">Calculée à partir des ventes réelles de biens du même type autour de l’adresse.</p>
        <form class="lform" id="estim-form" novalidate>
          <div class="field"><label for="e-adr">Adresse du bien</label><input id="e-adr" required placeholder="Numéro, rue, commune" autocomplete="street-address"></div>
          <div class="lform-grid">
            <div class="field"><label for="e-type">Type de bien</label><select id="e-type"><option value="M">Maison</option><option value="A">Appartement</option></select></div>
            <div class="field"><label for="e-surf">Surface habitable (m²)</label><input id="e-surf" type="number" inputmode="numeric" min="10" max="600" required></div>
          </div>
          <button class="btn btn-navy" type="submit" style="align-self:flex-start">Calculer la fourchette</button>
        </form>
      </div>
      <div class="estim-out" id="estim-out" aria-live="polite">
        <p class="muted">Renseignez l’adresse, le type et la surface : la fourchette s’affiche ici.</p>
      </div>
    </div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap split" style="align-items:start">
    <div class="a stack">
      <span class="eyebrow">Méthode</span>
      <h2>D’où viennent <span class="it">ces chiffres ?</span></h2>
    </div>
    <div class="b stack" style="font-size:16px;color:var(--text)">
      <p><strong style="color:var(--navy)">DVF</strong> (Demandes de valeurs foncières) est la base publique des ventes immobilières, publiée par la Direction générale des Finances publiques à partir des actes enregistrés chez les notaires. Elle est mise à jour deux fois par an, avec quelques mois de décalage.</p>
      <p>Nous ne gardons que les ventes simples d’<strong style="color:var(--navy)">une seule maison ou d’un seul appartement</strong> (avec ou sans garage ou cave), écartons les ventes en bloc, les terrains seuls et les valeurs aberrantes, puis calculons des <strong style="color:var(--navy)">médianes</strong> — moins sensibles aux ventes exceptionnelles qu’une moyenne.</p>
      <p>Le prix au m² d’un quartier ne dit pas la valeur d’une maison : état, terrain, exposition, travaux font varier le prix de 30 % ou plus. Pour un chiffre fiable sur votre bien, rien ne remplace une visite.</p>
      <a class="btn btn-navy" style="align-self:flex-start;margin-top:8px" href="{CV_EST}">Demander une estimation</a>
    </div>
  </div>
</section>
</main>
'''
    body += footer(r, ['assets/vendor/leaflet/leaflet.js', 'assets/map.js', 'assets/prix.js', 'assets/estimation.js'])
    write('prix.html', body)


# =========================================================
# QUARTIERS
# =========================================================
def page_quartiers():
    r = ''
    body = head('Les quartiers de Louviers : où vivre à Louviers ? · louviers.immo',
                'Centre-ville, Saint-Germain, La Londe, Saint-Jean, Saint-Lubin, Les Amoureux, Pampoule : les quartiers de Louviers racontés par une agence installée depuis 1992.',
                'quartiers.html', r)
    body += header('quartiers.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · Quartiers</div>
    <span class="eyebrow">Les quartiers</span>
    <h1 style="margin-top:12px">Sept quartiers,<br><span class="it">sept façons de vivre Louviers.</span></h1>
    <p class="lede" style="margin-top:20px">Ambiance, écoles, types de maisons, prix : chaque quartier raconté par ceux qui le connaissent depuis 1992.</p>
  </div>
</section>
<section class="section bg-sand">
  <div class="wrap">
    {q_grid(r)}
    <div class="info-card" style="margin-top:28px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center"><span><strong>Vous hésitez entre deux quartiers ?</strong><span>Prix, écoles, gare et A13, côte à côte.</span></span><a class="btn btn-navy" href="{r}comparer.html">Comparer deux adresses</a></div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="a stack">
      <span class="eyebrow">Une rue en particulier ?</span>
      <h2>Testez <span class="it">une adresse.</span></h2>
      <p class="lede">Commerces, écoles, bus, gare, prix des ventes autour : tout ce qu’il faut savoir avant une visite.</p>
    </div>
    <div class="b">{search_form('adresse-quartiers', chips=False)}</div>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('quartiers.html', body)


def page_centre_ville():
    r = '../'
    body = head('Vivre dans le centre-ville de Louviers : marché, commerces, animations · louviers.immo',
                'Le centre-ville de Louviers : le marché du mercredi et du samedi, plus de 200 commerces de proximité, un agenda culturel toute l’année, et une place pour les aînés comme pour les jeunes.',
                'quartiers/centre-ville.html', r)
    body += header('quartiers.html', r, topbar=False)
    q = adr_link(r, 'Place de la Halle aux Drapiers 27400 Louviers')
    body += f'''<main id="contenu">
<div class="wrap">
  <header class="art-head">
    <div class="small muted"><a href="{r}index.html" class="muted">Accueil</a> · <a href="{r}quartiers.html" class="muted">Quartiers</a> · Centre-ville</div>
    <span class="eyebrow">Quartier 01</span>
    <h1>Le centre-ville,<br><span class="it">tout à pied.</span></h1>
    <div class="byline"><span>Par l’équipe CV Immobilier</span><span class="dot">·</span><span>Agence installée au 27 rue du Général de Gaulle</span></div>
  </header>
  <figure class="hero-art" style="aspect-ratio:21/8;border-radius:28px">
    {HERO_SVG}
    <figcaption><span><strong style="font-weight:600">Le centre de Louviers</strong> · commerces, marché, services à quelques minutes à pied</span><span>Illustration</span></figcaption>
  </figure>
</div>
<section class="section">
  <div class="wrap art-grid">
    <article>
      <p class="chapo">Au cœur de la Normandie, le centre-ville de Louviers séduit par son dynamisme commercial, son patrimoine soigné et sa véritable douceur de vivre.</p>

      <div class="qa"><h2>Le rendez-vous incontournable du marché</h2>
      <p>Deux fois par semaine, le <strong style="color:var(--navy)">mercredi et le samedi matin</strong>, la place de la Halle devient le théâtre d’une effervescence gourmande. Producteurs locaux, étals colorés et senteurs du terroir s’y rassemblent en plein cœur de ville pour offrir aux Lovériens un lieu d’échange authentique et convivial.</p></div>

      <div class="market">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true"><path d="M3 9l1.5-5h15L21 9"/><path d="M3 9h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/><path d="M5 13v7h14v-7"/></svg>
        <div><strong>Marché de Louviers</strong><br>Mercredi et samedi matin · place de la Halle</div>
      </div>

      <div class="qa"><h2>Plus de 200 commerces de proximité</h2>
      <p>Le commerce local est aussi dynamique qu’éclectique : plus de 200 commerces de proximité sont installés en centre-ville pour la grande majorité, mais aussi dans les différents quartiers. Soutenue par la municipalité, Louviers Shopping, l’association des commerçants lovériens, organise de nombreux événements au fil de l’année : salon des commerçants en novembre, animations de Noël, opérations pour la fête des mères et des pères, Pâques…</p>
      <p style="margin-top:14px"><a class="link-u" href="{r}commerces.html">Parcourir l’annuaire des commerçants</a></p></div>

      <div class="qa"><h2>Un agenda culturel et festif tout au long de l’année</h2>
      <p>Le cœur urbain vit au rythme d’animations régulières — braderies commerçantes, rendez-vous artistiques, marchés thématiques et illuminations saisonnières — qui renforcent l’attractivité des boutiques de proximité et la convivialité des terrasses.</p>
      <p style="margin-top:14px"><a class="link-u" href="https://www.ville-louviers.fr/actualite-agenda/" target="_blank" rel="noopener">L’agenda sur le site de la Ville</a></p></div>

      <div class="pull"><span class="q" aria-hidden="true">«</span><p>Le marché le mercredi et le samedi, les terrasses, les boutiques : au centre de Louviers, la voiture reste souvent au garage.</p><cite>— L’équipe CV Immobilier</cite></div>

      <div class="qa"><h2>Une attention particulière portée aux seniors</h2>
      <p>Ville inclusive et solidaire, Louviers déploie un riche programme dédié à ses aînés. Ateliers bien-être, thés dansants, sorties culturelles et rencontres intergénérationnelles favorisent le lien social, l’autonomie et le bien-vieillir au quotidien. Programme et inscriptions auprès de la mairie, au 02 32 09 58 58.</p>
      <p style="margin-top:14px"><a class="link-u" href="https://www.ville-louviers.fr/" target="_blank" rel="noopener">Le site de la Ville de Louviers</a></p></div>

      <div class="qa"><h2>Et une place pour les jeunes</h2>
      <p>Louviers fait aussi une place à sa jeunesse. Le <strong style="color:var(--navy)">Conseil municipal de jeunes</strong> réunit des enfants de 8 à 10 ans, élus pour deux ans dans les écoles de la ville : ils portent leurs propres projets devant le maire et les élus, et découvrent ainsi le fonctionnement de leur commune. Un <strong style="color:var(--navy)">Point Information Jeunesse</strong> accompagne les jeunes dans leurs démarches, et le complexe aquatique <strong style="color:var(--navy)">Caséo</strong>, équipement de l’Agglomération Seine-Eure, est installé à Louviers.</p>
      <p style="margin-top:14px">Écoles, collèges et lycées les plus proches d’une adresse : <a class="link-u" href="{q}">testez-la</a>. Inscriptions scolaires et périscolaire : <a class="link-u" href="https://www.ville-louviers.fr/ma-ville/enfance-education-jeunesse/" target="_blank" rel="noopener">Ville de Louviers</a>. Clubs et associations : <a class="link-u" href="{r}commerces.html#sport">l’annuaire des clubs sportifs</a>.</p></div>

      <div class="box-sand stack" style="border-radius:24px">
        <span class="eyebrow">Les prix du quartier</span>
        <h2 style="font-size:clamp(24px,2.2vw,30px)">Ventes à moins de 500 m <span class="it">de la place de la Halle</span></h2>
        <div class="kpis" id="q-prices" data-ref="Place de la Halle aux Drapiers 27400 Louviers" data-radius="500">
          <div class="kpi light"><div class="l">Maison</div><div class="v" data-k="M">—</div><div class="u">€/m² médian</div></div>
          <div class="kpi light"><div class="l">Appartement</div><div class="v" data-k="A">—</div><div class="u">€/m² médian</div></div>
          <div class="kpi light"><div class="l">Ventes</div><div class="v" data-k="N">—</div><div class="u" data-k="P">ventes DVF</div></div>
        </div>
        <a class="link-u" id="q-prices-link" style="align-self:flex-start" href="{r}prix.html">Voir les ventes sur la carte</a>
      </div>
    </article>
    <aside>
      <div class="side-card dark">
        <span class="eyebrow">Vivre ici</span>
        <p>Commerces, écoles, bus et temps de trajet autour de la place de la Halle.</p>
        <a class="btn btn-gold" href="{q}">Voir ce qu’il y a autour</a>
      </div>
      <div class="side-card">
        <span class="eyebrow">Portrait</span>
        <span class="nm" style="font-size:21px">Maison Barbé, la charcuterie du Parvis fait peau neuve</span>
        <a class="link-u" style="align-self:flex-start" href="{r}portraits/maison-barbe.html">Lire le portrait</a>
      </div>
      <a class="btn btn-navy plausible-event-name=Biens+Quartier plausible-event-position=centre-ville" href="{CV_SITE}">Nos biens à vendre dans ce quartier</a>
      <div class="dashed">Un projet dans le quartier ? Notre agence est au 27 rue du Général de Gaulle. <a href="{CV_EST}" style="font-weight:600">Faire estimer un bien</a></div>
    </aside>
  </div>
</section>
<section class="section" style="padding-top:0" data-biens-sec>
  <div class="wrap">
    <div class="head2"><h2>À vendre à Louviers</h2><p>Les derniers biens de notre agence dans la commune.</p></div>
    <div class="biens" data-biens data-commune="Louviers" data-max="3" data-where="centre-ville"></div>
    <div class="biens-foot"><p class="note" data-biens-maj>Annonces de cvimmobilier.fr, mises à jour chaque nuit.</p><a class="link-u" href="{r}a-vendre.html?commune=Louviers">Tous les biens à Louviers</a></div>
  </div>
</section>
<section class="section bg-sand" style="padding-top:64px;padding-bottom:64px">
  <div class="wrap"><p class="note">Sources : Ville de Louviers (commerce de proximité, Conseil municipal de jeunes) ; Agglomération Seine-Eure (Caséo) ; ventes DVF, DGFiP.</p></div>
</section>
</main>
'''
    body += footer(r, ['assets/quartier.js', 'assets/biens.js'])
    write('quartiers/centre-ville.html', body)


# =========================================================
# PORTRAITS
# =========================================================
def page_portraits():
    r = ''
    body = head('Portraits : ceux qui font Louviers · louviers.immo',
                'Commerçants, artisans, restaurateurs et associations de Louviers : les portraits réalisés par l’équipe CV Immobilier.',
                'portraits.html', r)
    body += header('portraits.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · Portraits</div>
    <span class="eyebrow">Portraits</span>
    <h1 style="margin-top:12px">Ceux qui font <span class="it">Louviers.</span></h1>
    <p class="lede" style="margin-top:20px">Commerçants, artisans, restaurateurs, associations : notre équipe pousse une porte et raconte une histoire.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="p-grid" id="home-portraits" data-all>
      <div class="p-empty" style="grid-column:1/-1">
        <span class="eyebrow">Bientôt</span>
        <h3>Les premiers portraits sont en préparation.</h3>
        <p class="muted">Revenez nous voir très vite — ou proposez le vôtre.</p>
      </div>
    </div>
  </div>
</section>
<section class="section bg-sand">
  <div class="wrap split" style="align-items:start">
    <div class="a stack">
      <span class="eyebrow">Commerçants, artisans</span>
      <h2>Et si le prochain portrait <span class="it">était le vôtre ?</span></h2>
      <p class="lede">C’est gratuit et sans contrepartie. Votre portrait apparaît aussi auprès de tous ceux qui cherchent une maison près de chez vous.</p>
    </div>
    <div class="b">
      <ol class="steps clean">
        <li><span class="n">01</span><span><strong>Une rencontre de 30 minutes</strong><span class="d">Dans votre boutique, à l’heure qui vous arrange.</span></span></li>
        <li><span class="n">02</span><span><strong>Quelques photos</strong><span class="d">Vous, votre lieu, vos produits.</span></span></li>
        <li><span class="n">03</span><span><strong>Vous relisez avant publication</strong><span class="d">Rien n’est publié sans votre accord.</span></span></li>
        <li><span class="n">04</span><span><strong>Votre portrait vit sur louviers.immo</strong><span class="d">Et il apparaît sur la carte de toutes les adresses voisines.</span></span></li>
      </ol>
    </div>
  </div>
  <div class="wrap" id="proposer" style="margin-top:40px">
    <h3 style="margin-bottom:18px">Proposer mon commerce</h3>
    {form_proposer(r, 'portraits')}
  </div>
</section>
</main>
'''
    body += footer(r, ['data/portraits.js'])
    write('portraits.html', body)


def page_portrait_modele():
    r = '../'
    body = head('Modèle de portrait · louviers.immo', 'Modèle de page pour les portraits de commerçants.',
                'portraits/modele.html', r, noindex=True)
    body += header('portraits.html', r, topbar=False)
    qs = ['Comment est née votre affaire ?', 'Pourquoi Louviers ?', 'À quoi ressemble une journée type ?',
          'Le produit ou le service dont vous êtes le plus fier ?', 'Votre adresse préférée à Louviers, en dehors de la vôtre ?',
          'Un conseil à quelqu’un qui s’installe à Louviers ?']
    qa = lambda q: f'<div class="qa"><h2>{q}</h2><p><span class="todo">[Réponse, relue et validée par la personne avant publication.]</span></p></div>'
    body += f'''<main id="contenu">
<div class="wrap">
  <header class="art-head">
    <div class="small muted"><a href="{r}index.html" class="muted">Accueil</a> · <a href="{r}portraits.html" class="muted">Portraits</a> · [Quartier]</div>
    <span class="eyebrow">Portrait n°[00] · [Catégorie]</span>
    <h1>[Nom du commerce],<br><span class="it">[titre du portrait]</span></h1>
    <div class="byline"><span>Par l’équipe CV Immobilier</span><span class="dot">·</span><span>[date]</span><span class="dot">·</span><span>5 min de lecture</span></div>
  </header>
  <figure style="margin:0"><div class="cover">Grande photo du commerçant dans sa boutique · format paysage</div>
  <figcaption class="cover-cap">[Prénom Nom], [fonction], dans sa boutique [rue]. Photo : CV Immobilier.</figcaption></figure>
</div>
<section class="section">
  <div class="wrap art-grid">
    <article>
      <p class="chapo"><span class="todo">[Chapeau : trois ou quatre lignes qui posent la personne, le lieu et ce qui la rend unique.]</span></p>
      {qa(qs[0])}{qa(qs[1])}{qa(qs[2])}
      <div class="pull"><span class="q" aria-hidden="true">«</span><p>[La phrase la plus forte de l’interview, mot pour mot.]</p><cite>— [Prénom Nom]</cite></div>
      {qa(qs[3])}{qa(qs[4])}{qa(qs[5])}
      <div class="two"><div class="ph-block">Photo · produit</div><div class="ph-block">Photo · vitrine</div></div>
    </article>
    <aside>
      <div class="side-card">
        <span class="eyebrow">Infos pratiques</span>
        <span class="nm">[Nom du commerce]</span>
        <div class="small" style="color:var(--text);display:flex;flex-direction:column;gap:8px"><span>[Adresse]<br>27400 Louviers</span><span>[Horaires]</span><span>[Téléphone]</span><span>[Site ou réseaux]</span></div>
      </div>
      <div class="side-card dark">
        <span class="eyebrow">Vivre à côté</span>
        <p>Découvrez ce qu’il y a autour de n’importe quelle adresse.</p>
        <a class="btn btn-gold" href="{r}adresse.html">Tester une adresse</a>
      </div>
      <div class="dashed">Vous êtes commerçant à Louviers ? <a href="mailto:{MAIL}?subject=Portrait%20louviers.immo" style="font-weight:600">Proposez votre portrait</a> — c’est gratuit.</div>
    </aside>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('portraits/modele.html', body)


# =========================================================
# OUTILS
# =========================================================
def page_outils():
    r = ''
    body = head('Frais de notaire et capacité d’emprunt : simulateurs · louviers.immo',
                'Calculez vos frais de notaire dans l’Eure (ancien, neuf, primo-accédant) et votre capacité d’emprunt avant de visiter à Louviers.',
                'outils.html', r)
    body += header('outils.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · Outils</div>
    <span class="eyebrow">Outils pratiques</span>
    <h1 style="margin-top:12px">Faire ses comptes <span class="it">avant de visiter.</span></h1>
  </div>
</section>

<section class="section" style="padding-bottom:0">
  <div class="wrap two">
    <a class="info-card" href="{r}prix.html#estimation"><strong>Estimation rapide</strong><span>Une première fourchette de prix à partir des ventes réelles autour d’une adresse.</span></a>
    <a class="info-card" href="{r}comparer.html"><strong>Comparer deux quartiers</strong><span>Prix, écoles, temps vers la gare et l’A13, côte à côte.</span></a>
  </div>
</section>

<section class="section" id="notaire">
  <div class="wrap stack-lg">
    <div class="head" style="margin-bottom:0"><div><span class="eyebrow">Simulateur</span><h2>Frais de <span class="it">notaire</span></h2></div>
      <p>Ce qui s’ajoute au prix d’achat : taxes reversées à l’État et aux collectivités, rémunération du notaire, frais de formalités.</p></div>
    <div class="calc">
      <form id="form-notaire" novalidate>
        <div class="field"><label for="n-prix">Prix du bien (hors frais d’agence à la charge du vendeur)</label>
          <input id="n-prix" type="number" inputmode="numeric" min="0" step="1000" value="200000"></div>
        <div class="field"><span class="small" style="font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)">Type de bien</span>
          <div class="radio-row" role="radiogroup" aria-label="Type de bien">
            <label><input type="radio" name="n-type" value="ancien" checked> Ancien</label>
            <label><input type="radio" name="n-type" value="neuf"> Neuf (VEFA)</label>
          </div></div>
        <div id="n-primo-row"><label class="check"><input type="checkbox" id="n-primo"> Premier achat de résidence principale</label></div>
        <p class="note">Dans l’Eure, les droits de mutation sont passés à 5 % (part départementale) au 1<sup>er</sup> avril 2026 ; le taux de 4,5 % est maintenu pour les primo-accédants. Estimation indicative : le montant exact est donné par votre notaire.</p>
      </form>
      <div class="out" aria-live="polite">
        <span class="eyebrow">Frais estimés</span>
        <div class="big" id="n-total">—</div>
        <div id="n-pct" style="color:var(--gold-light)"></div>
        <div class="lines">
          <div><span id="n-taxes-l">Droits de mutation</span><span id="n-taxes">—</span></div>
          <div><span>Émoluments du notaire (TTC)</span><span id="n-emo">—</span></div>
          <div><span>Contribution de sécurité immobilière</span><span id="n-csi">—</span></div>
          <div><span>Débours et formalités (forfait)</span><span id="n-deb">—</span></div>
          <div style="border-bottom:0"><span style="color:var(--cream)">Coût total de l’achat</span><span id="n-cout" style="font-weight:600">—</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-sand" id="emprunt">
  <div class="wrap stack-lg">
    <div class="head" style="margin-bottom:0"><div><span class="eyebrow">Simulateur</span><h2>Capacité <span class="it">d’emprunt</span></h2></div>
      <p>Selon la règle des banques : des mensualités (assurance comprise) qui ne dépassent pas 35 % des revenus.</p></div>
    <div class="calc">
      <form id="form-emprunt" novalidate>
        <div class="two">
          <div class="field"><label for="e-rev">Revenus nets du foyer / mois</label><input id="e-rev" type="number" inputmode="numeric" min="0" step="100" value="4000"></div>
          <div class="field"><label for="e-chg">Crédits en cours / mois</label><input id="e-chg" type="number" inputmode="numeric" min="0" step="50" value="0"></div>
        </div>
        <div class="two">
          <div class="field"><label for="e-apport">Apport personnel</label><input id="e-apport" type="number" inputmode="numeric" min="0" step="1000" value="20000"></div>
          <div class="field"><label for="e-duree">Durée du prêt</label>
            <select id="e-duree"><option value="15">15 ans</option><option value="20">20 ans</option><option value="25" selected>25 ans</option></select></div>
        </div>
        <div class="two">
          <div class="field"><label for="e-taux">Taux du crédit (%)</label><input id="e-taux" type="number" inputmode="decimal" min="0" max="15" step="0.05" value="3.5"></div>
          <div class="field"><label for="e-ass">Taux d’assurance (%)</label><input id="e-ass" type="number" inputmode="decimal" min="0" max="2" step="0.01" value="0.30"></div>
        </div>
        <p class="note">Taux pré-remplis à titre d’exemple : modifiez-les selon les conditions du moment. Pour une simulation personnalisée, un courtier ou votre banque vous donnera un chiffre précis : retrouvez <a href="{r}commerces.html#financement" style="font-weight:600">nos courtiers partenaires à Louviers</a>.</p>
      </form>
      <div class="out" aria-live="polite">
        <span class="eyebrow">Budget d’achat estimé</span>
        <div class="big" id="e-budget">—</div>
        <div style="color:var(--gold-light)">frais de notaire inclus (≈ 7,8 % dans l’ancien)</div>
        <div class="lines">
          <div><span>Montant empruntable</span><span id="e-capital">—</span></div>
          <div><span>Mensualité maximale</span><span id="e-mensu">—</span></div>
          <div><span class="small" style="color:var(--on-dark-muted)">dont</span><span class="small" id="e-mensu-d" style="color:var(--on-dark-muted)">—</span></div>
          <div style="border-bottom:0"><span>Coût total du crédit (intérêts + assurance)</span><span id="e-cout">—</span></div>
        </div>
        <a class="btn btn-gold" id="e-link" href="{r}prix.html" style="align-self:flex-start;margin-top:8px">Voir les prix à Louviers</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="t-grid">
      <a class="t-card dark" href="{CV_EST}" style="grid-column:1/-1">
        <span class="eyebrow">Vous vendez ?</span>
        <span class="t" style="font-size:clamp(28px,3vw,40px)">Faites estimer votre bien <span class="it">par une équipe qui connaît chaque rue.</span></span>
        <p>Avis de valeur argumenté, gratuit et sans engagement.</p>
        <span class="go">Demander une estimation</span>
      </a>
    </div>
  </div>
</section>
</main>
'''
    body += footer(r, ['assets/outils.js'])
    write('outils.html', body)


# =========================================================
# À PROPOS
# =========================================================
AG = '02 32 40 22 28'
TEAM = [('Nicolas Vayrac', 'Directeur', '06 76 66 56 20', 'nicolas-vayrac'),
        ('Jessica Mourad', 'Négociation · vente', '06 69 50 44 35', 'jessica-mourad'),
        ('Brigitte Bramille', 'Négociation · vente', '06 62 83 69 95', 'brigitte-bramille-2'),
        ('Maxime Bal', 'Négociation · vente', '06 76 33 88 73', 'maxime-bal'),
        ('Gaétan Hugues', 'Négociation · vente', '06 73 97 32 47', 'gaetan-hugues'),
        ('Arthur Godefroy', 'Négociation · vente', '06 41 07 69 70', 'arthur-godefroy'),
        ('Laëtitia Tierce', 'Location', AG, 'laetitia-tierce'),
        ('Laetitia Duchesne', 'Comptabilité', AG, 'laetitia-duchesne'),
        ('Daniel Vayrac', 'Consultant', AG, 'daniel-vayrac')]


def page_apropos():
    r = ''
    def ini(n):
        p = n.split()
        return (p[0][0] + p[-1][0]).upper()
    team = ''.join(f'''<div class="member">
        <img src="{r}assets/img/equipe/{img}.jpg" alt="{n}" width="400" height="400" loading="lazy">
        <div class="mn">{n}</div><div class="mr">{role}</div>
        <a class="mt" href="tel:+33{tel.replace(' ', '')[1:]}">{tel}</a></div>''' for n, role, tel, img in TEAM)
    body = head('À propos de louviers.immo · CV Immobilier, Louviers depuis 1992',
                'louviers.immo est le guide de Louviers proposé par CV Immobilier, agence immobilière indépendante installée à Louviers depuis 1992 et à Saint-Pierre-du-Vauvray depuis 2024.',
                'a-propos.html', r, jsonld=ORG)
    body += header(None, r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · À propos</div>
    <span class="eyebrow">À propos</span>
    <h1 style="margin-top:12px">Un guide ouvert à tous,<br><span class="it">par une agence d’ici.</span></h1>
  </div>
</section>
<section class="section">
  <div class="wrap word">
    <img class="avatar" src="{r}assets/img/equipe/nicolas-vayrac.jpg" alt="Nicolas Vayrac" width="400" height="400" loading="lazy">
    <div class="stack">
      <blockquote>« Depuis 1992, on nous pose les mêmes questions : l’école est-elle loin, où acheter son pain, combien de temps pour la gare ? louviers.immo, c’est notre réponse, ouverte à tous, que vous achetiez avec nous ou non. »</blockquote>
      <div><span style="font-family:var(--serif);font-size:20px;color:var(--navy)">Nicolas Vayrac</span> <span class="muted" style="margin-left:10px">Directeur de CV Immobilier</span></div>
    </div>
  </div>
</section>
<section class="section bg-sand">
  <div class="wrap">
    <div class="head"><div><span class="eyebrow">L’équipe</span><h2>Neuf personnes, <span class="it">deux agences.</span></h2></div>
      <p>À Louviers depuis 1992, à Saint-Pierre-du-Vauvray depuis 2024. Membre de la FNAIM et du réseau Interkab.</p></div>
    <div class="team">{team}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="head"><div><span class="eyebrow">Nos agences</span><h2>Louviers <span class="it">et Saint-Pierre-du-Vauvray</span></h2></div></div>
    <div class="two" style="gap:28px">
      <div class="stack" style="gap:14px">
        <img src="{r}assets/img/agences/agence-louviers.jpg" alt="Agence CV Immobilier, rue du Général de Gaulle à Louviers" width="1200" height="900" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:22px">
        <div style="font-family:var(--serif);font-size:24px;color:var(--navy)">Louviers <span class="it muted" style="font-size:17px">· depuis 1992</span></div>
        <div class="muted">27 rue du Général de Gaulle, 27400 Louviers · <a href="tel:+33232402228" style="font-weight:600">02 32 40 22 28</a></div>
      </div>
      <div class="stack" style="gap:14px">
        <img src="{r}assets/img/agences/agence-saintpierre.jpg" alt="Agence CV Immobilier, Grande Rue à Saint-Pierre-du-Vauvray" width="1200" height="800" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:22px">
        <div style="font-family:var(--serif);font-size:24px;color:var(--navy)">Saint-Pierre-du-Vauvray <span class="it muted" style="font-size:17px">· depuis 2024</span></div>
        <div class="muted">15 Grande Rue, 27430 Saint-Pierre-du-Vauvray · <a href="tel:+33279492171" style="font-weight:600">02 79 49 21 71</a></div>
      </div>
    </div>
  </div>
</section>
<section class="section bg-sand">
  <div class="wrap split" style="align-items:start">
    <div class="a stack"><span class="eyebrow">Données ouvertes</span><h2>Nos <span class="it">sources</span></h2></div>
    <div class="b stack" style="color:var(--text);font-size:16px">
      <p><strong style="color:var(--navy)">Adresses</strong> — Base Adresse Nationale, via le service de géocodage de la Géoplateforme (IGN).</p>
      <p><strong style="color:var(--navy)">Commerces, écoles, arrêts de bus</strong> — OpenStreetMap, la carte collaborative mondiale. © les contributeurs d’OpenStreetMap, licence ODbL.</p>
      <p><strong style="color:var(--navy)">Ventes immobilières</strong> — Demandes de valeurs foncières (DVF), Direction générale des Finances publiques, Licence Ouverte.</p>
      <p><strong style="color:var(--navy)">Fonds de carte</strong> — Plan IGN, Géoplateforme, Licence Ouverte.</p>
      <p><strong style="color:var(--navy)">Textes et portraits</strong> — rédigés par l’équipe CV Immobilier et relus par les personnes interviewées.</p>
    </div>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('a-propos.html', body)


# =========================================================
# MENTIONS LÉGALES, 404
# =========================================================
def page_mentions():
    r = ''
    body = head('Mentions légales · louviers.immo', 'Mentions légales, sources des données et confidentialité de louviers.immo.',
                'mentions-legales.html', r)
    body += header(None, r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head"><div class="wrap"><div class="crumbs"><a href="{r}index.html">Accueil</a> · Mentions légales</div><h1>Mentions <span class="it">légales</span></h1></div></section>
<section class="section"><div class="wrap" style="max-width:860px">
<article class="stack-lg" style="font-size:16px;color:var(--text)">
  <div class="stack"><h2 style="font-size:28px">Éditeur</h2>
  <p>Le site louviers.immo est édité par CV IMMOBILIER, SARL au capital de 7 622 €, immatriculée au RCS d’Évreux sous le numéro 389 251 117 (SIRET 389 251 117 00039), dont le siège social est situé 27 rue du Général de Gaulle, 27400 Louviers, France. Téléphone : 02 32 40 22 28 · E-mail : {MAIL}.</p>
  <p>Numéro de TVA intracommunautaire : FR45 389 251 117.</p>
  <p>Carte professionnelle « Transaction sur immeubles et fonds de commerce » et « Gestion immobilière » n° CPI 2701 2016 000 005 229, délivrée par la CCI Portes de Normandie.</p>
  <p>Garantie financière : GALIAN, pour un montant de 120 000 €. Membre de la FNAIM.</p>
  <p>Directeur de la publication : Nicolas Vayrac.</p></div>
  <div class="stack"><h2 style="font-size:28px">Médiation de la consommation</h2>
  <p>En cas de litige, et après une démarche écrite préalable auprès de CV Immobilier, le consommateur peut saisir gratuitement le médiateur de la consommation : ANM Conso — <a href="https://www.anm-conso.com" target="_blank" rel="noopener">www.anm-conso.com</a>.</p></div>
  <div class="stack"><h2 style="font-size:28px">Hébergement</h2><p>Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis — <a href="https://www.netlify.com/" target="_blank" rel="noopener">www.netlify.com</a>. Code source hébergé sur GitHub.</p></div>
  <div class="stack" id="donnees"><h2 style="font-size:28px">Sources des données</h2>
  <p>Adresses : Base Adresse Nationale, service de géocodage de la Géoplateforme (IGN), Licence Ouverte Etalab 2.0.</p>
  <p>Commerces, écoles, arrêts de bus et équipements : © les contributeurs d’OpenStreetMap, base de données sous licence ODbL (openstreetmap.org/copyright), interrogée via l’API Overpass.</p>
  <p>Ventes immobilières : Demandes de valeurs foncières (DVF), Direction générale des Finances publiques, publiées sur data.gouv.fr sous Licence Ouverte. Conformément aux conditions de réutilisation, les données ne comportent aucune information nominative et ne sont pas indexées par les moteurs de recherche.</p>
  <p>Fonds de carte : Plan IGN, Géoplateforme, Licence Ouverte. Bibliothèque cartographique : Leaflet.</p>
  <p>Les temps de trajet affichés sont des estimations calculées à partir des distances ; ils n’ont pas de valeur contractuelle.</p></div>
  <div class="stack"><h2 style="font-size:28px">Données personnelles et cookies</h2>
  <p>louviers.immo ne dépose aucun cookie. La fréquentation est mesurée avec Plausible Analytics, un outil européen sans cookie qui ne collecte aucune donnée personnelle et produit uniquement des statistiques anonymes (pages vues, provenance des visites, clics sur les boutons). Lorsque vous recherchez une adresse, celle-ci est transmise au service de géocodage de l’IGN et ses coordonnées au service OpenStreetMap (Overpass) afin d’afficher les résultats ; elle n’est pas conservée par CV Immobilier.</p>
  <p>Pour toute question : {MAIL}.</p></div>
  <div class="stack" id="formulaires"><h2 style="font-size:28px">Formulaires : alerte quartier et proposition de commerce</h2>
  <p>Les informations saisies dans ces formulaires (adresse mail, adresse recherchée, et pour les commerçants : nom, commerce, téléphone, message) sont destinées uniquement à CV Immobilier, responsable du traitement, pour vous recontacter au sujet de votre demande : vous informer des biens et des ventes près de l’adresse indiquée, ou préparer le portrait de votre commerce. Le traitement repose sur votre consentement, donné en cochant la case du formulaire.</p>
  <p>Les données sont reçues par l’intermédiaire de notre hébergeur Netlify et ne sont ni vendues ni cédées. Elles sont conservées trois ans après notre dernier échange, puis supprimées. Vous pouvez à tout moment retirer votre consentement, vous désinscrire, accéder à vos données, les faire rectifier ou supprimer en écrivant à {MAIL}. Vous pouvez aussi adresser une réclamation à la CNIL (cnil.fr).</p></div>
  <div class="stack"><h2 style="font-size:28px">Propriété intellectuelle</h2>
  <p>Les textes, portraits, photographies et éléments graphiques de louviers.immo sont la propriété de CV Immobilier ou des personnes photographiées et ne peuvent être reproduits sans autorisation.</p></div>
</article></div></section>
</main>
'''
    body += footer(r)
    write('mentions-legales.html', body)


def page_404():
    r = '/'
    body = head('Page introuvable · louviers.immo', 'Cette page n’existe pas.', '404.html', r, noindex=True)
    body += header(None, r, topbar=False)
    body += f'''<main id="contenu">
<section class="section"><div class="wrap stack-lg" style="max-width:760px">
  <span class="eyebrow">Erreur 404</span>
  <h1 style="font-size:clamp(40px,5vw,64px)">Cette page s’est <span class="it">perdue dans Louviers.</span></h1>
  <p class="lede">Elle a peut-être été déplacée. Essayez plutôt une adresse :</p>
  {search_form('adresse-404', chips=False, root=r)}
  <a class="link-u" style="align-self:flex-start" href="/">Retour à l’accueil</a>
</div></section>
</main>
'''
    body += footer(r)
    write('404.html', body)


# =========================================================
# ANNUAIRE DES COMMERCES
# =========================================================
def page_commerces():
    r = ''
    css = f'<link rel="stylesheet" href="{r}assets/vendor/leaflet/leaflet.css">\n'
    body = head('Commerces à Louviers : restaurants, snacking, mode, métiers de bouche · louviers.immo',
                'L’annuaire de Louviers et de l’Agglomération Seine-Eure par rubrique : restaurants, snacking, cafés, boulangeries, métiers de bouche, mode, artisans, clubs sportifs, notaires, santé, services.',
                'commerces.html', r, css=css)
    body += header('commerces.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · Commerces</div>
    <span class="eyebrow">L’annuaire</span>
    <h1 style="margin-top:12px">Les bonnes adresses <span class="it">de Louviers.</span></h1>
    <p class="lede" style="margin-top:20px">Où déjeuner, acheter son pain, trouver un artisan ou inscrire les enfants au club de tennis : commerces, artisans et clubs sportifs, rubrique par rubrique.</p>
  </div>
</section>

<section class="section" style="padding-top:44px">
  <div class="wrap stack-lg">
    <div class="market">
      <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true"><path d="M3 9l1.5-5h15L21 9"/><path d="M3 9h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/><path d="M5 13v7h14v-7"/></svg>
      <div><strong>Marché de Louviers</strong> · mercredi et samedi matin, place de la Halle : producteurs locaux et produits du terroir. <a href="https://www.ville-louviers.fr/actualite-agenda/" target="_blank" rel="noopener" style="color:#fff;border-bottom:1px solid var(--gold-light)">Agenda de la Ville</a></div>
    </div>

    <div class="dir-tools">
      <div class="field"><label for="c-q">Rechercher</label>
        <input id="c-q" type="search" placeholder="Nom, activité, sport, rue…" autocomplete="off"></div>
      <div class="field"><label for="c-commune">Commune</label><select id="c-commune"></select></div>
      <div class="note" id="count" aria-live="polite" style="padding-bottom:14px"></div>
    </div>
    <div class="rubs" id="rubs" role="group" aria-label="Rubriques"></div>

    <div class="map-box" style="height:clamp(320px,46vh,520px)">
      <div class="map" id="map" role="region" aria-label="Carte de l’annuaire"></div>
      <div class="map-badge"><span class="pin-n star" style="width:16px;height:16px;font-size:0;border-width:1px"></span><span>En doré : les commerces dont nous avons fait le portrait</span></div>
    </div>

    <div id="dir"></div>

    <div class="box-sand stack" style="margin-top:32px" id="proposer">
      <h2 style="font-size:clamp(26px,2.6vw,36px)">Votre commerce manque, <span class="it">ou mérite un portrait ?</span></h2>
      <p class="muted">Écrivez-nous : nous ajoutons votre adresse et, si vous le souhaitez, nous venons faire votre portrait, gratuitement. Une erreur sur la carte ? Elle se corrige aussi sur <a href="https://www.openstreetmap.org/" target="_blank" rel="noopener">OpenStreetMap</a>, la carte collaborative.</p>
      {form_proposer(r, 'commerces')}
    </div>
  </div>
</section>
</main>
'''
    body += footer(r, ['assets/vendor/leaflet/leaflet.js', 'assets/map.js', 'data/portraits.js', 'data/partenaires.js', 'data/exclusions.js', 'data/clubs.js', 'assets/commerces.js'])
    write('commerces.html', body)


# =========================================================
# PORTRAIT : MAISON BARBÉ — CHARCUTERIE DU PARVIS
# =========================================================
def page_barbe():
    r = '../'
    addr = '43 rue du Maréchal Foch 27400 Louviers'
    near = adr_link(r, addr)
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": "Maison Barbé, la charcuterie du Parvis fait peau neuve",
          "author": {"@type": "Organization", "name": "CV Immobilier"}, "publisher": {"@id": DOMAIN + "#cv"},
          "datePublished": "2026-10-01", "inLanguage": "fr-FR",
          "about": {"@type": "Store", "name": "Maison Barbé — Charcuterie du Parvis", "url": "https://www.maison-barbe.com/",
                    "telephone": "+33232400277",
                    "address": {"@type": "PostalAddress", "streetAddress": "43 rue du Maréchal Foch", "postalCode": "27400",
                                "addressLocality": "Louviers", "addressCountry": "FR"}}}
    body = head('Maison Barbé, la charcuterie du Parvis fait peau neuve · Portrait · louviers.immo',
                'Portrait de la Maison Barbé — Charcuterie du Parvis, 43 rue du Maréchal Foch à Louviers : charcuterie artisanale faite maison, traiteur, formules du midi et une boutique entièrement rénovée.',
                'portraits/maison-barbe.html', r, jsonld=ld)
    body += header('portraits.html', r, topbar=False)
    body += f'''<main id="contenu">
<div class="wrap">
  <header class="art-head">
    <div class="small muted"><a href="{r}index.html" class="muted">Accueil</a> · <a href="{r}portraits.html" class="muted">Portraits</a> · Centre-ville</div>
    <span class="eyebrow">Portrait n°01 · Charcutier-traiteur</span>
    <h1>Maison Barbé,<br><span class="it">la charcuterie du Parvis fait peau neuve</span></h1>
    <div class="byline"><span>Par l’équipe CV Immobilier</span><span class="dot">·</span><span>Octobre 2026</span><span class="dot">·</span><span>4 min de lecture</span></div>
  </header>
  <figure style="margin:0">
    <div class="cover"><img src="{r}assets/img/portraits/maison-barbe-facade.jpg" alt="La devanture rénovée de la Maison Barbé, Charcuterie du Parvis, 43 rue du Maréchal Foch à Louviers" width="1800" height="1201" fetchpriority="high"></div>
    <figcaption class="cover-cap">La nouvelle devanture de la Maison Barbé, 43 rue du Maréchal Foch.</figcaption>
  </figure>
</div>

<section class="section">
  <div class="wrap art-grid">
    <article>
      <p class="chapo">Au 43 rue du Maréchal Foch, en plein centre de Louviers, Sylvie et Patrice Barbé tiennent une charcuterie-traiteur artisanale où tout est fait maison. Après de gros travaux, la boutique a fait peau neuve : nouvelle devanture, nouvelle identité, même exigence du fait maison.</p>

      <div class="qa"><h2>Le métier : tout faire soi-même</h2>
      <p>Chez les Barbé, le métier se résume en deux mots : <em>fait maison</em>. Pâtés, boudins, andouillettes, saucisses, plats à emporter : la charcuterie est préparée par la maison. Derrière le comptoir, c’est une affaire de famille, que Sylvie et Patrice font vivre au cœur de Louviers.</p></div>

      <div class="qa"><h2>Une boutique entièrement modernisée</h2>
      <p>La Maison Barbé s’est offert une vraie transformation. De gros travaux ont permis de moderniser entièrement le magasin, avec une nouvelle devanture et une nouvelle identité aux tons or et taupe, élégante et chaleureuse. Le décor a changé, le savoir-faire est resté.</p></div>

      <figure class="art-photo">
        <img src="{r}assets/img/portraits/maison-barbe-boutique.jpg" alt="L’intérieur de la boutique : étagères en bois, épicerie fine, vins et jus, et l’enseigne Maison Barbé rétroéclairée" width="1200" height="1600" loading="lazy">
        <figcaption>À l’intérieur, l’épicerie fine a trouvé sa place : vins, jus, huiles d’olive, pâtes artisanales et fleur de sel.</figcaption>
      </figure>

      <div class="pull"><span class="q" aria-hidden="true">★</span><p>Quatre produits primés au Grand Prix d’excellence : le boudin blanc truffé au foie gras, le pâté en croûte au ris de veau et foie gras, l’andouillette et la saucisse créative.</p><cite>— Une reconnaissance du savoir-faire de la maison</cite></div>

      <div class="qa"><h2>Du déjeuner sur le pouce au repas de mariage</h2>
      <p>Le midi, salariés et étudiants du centre-ville y trouvent des formules et des plats à emporter. Pour les grandes occasions, la maison prépare des buffets froids ou chauds, à emporter ou livrés : mariages, baptêmes, communions, anniversaires, mais aussi repas d’affaires, séminaires et cocktails pour les entreprises, à Louviers et dans les communes alentour.</p></div>

      <div class="qa"><h2>Les bons plans de la maison</h2>
      <p>Des bons cadeaux pour faire plaisir aux gourmands, et des invendus du jour proposés à prix réduit sur l’application Too Good To Go : une façon intelligente de lutter contre le gaspillage.</p></div>

      <div class="box-sand stack" style="border-radius:24px">
        <span class="eyebrow">Pour y aller</span>
        <h2 style="font-size:clamp(24px,2.2vw,30px)">Maison Barbé — <span class="it">Charcuterie du Parvis</span></h2>
        <p style="font-size:17px;color:var(--text)">43 rue du Maréchal Foch, 27400 Louviers · du mardi au samedi · <a href="tel:+33232400277" style="font-weight:600">02 32 40 02 77</a></p>
        <div class="two">
          <a class="btn btn-navy" href="https://www.maison-barbe.com/" target="_blank" rel="noopener">Visiter maison-barbe.com ↗</a>
          <a class="btn btn-gold" href="{near}">Voir ce qu’il y a autour</a>
        </div>
      </div>
    </article>
    <aside>
      <div class="side-card">
        <span class="eyebrow">Infos pratiques</span>
        <span class="nm">Maison Barbé<br><span style="font-size:17px" class="it">Charcuterie du Parvis</span></span>
        <div class="small" style="color:var(--text);display:flex;flex-direction:column;gap:8px">
          <span>43 rue du Maréchal Foch<br>27400 Louviers</span>
          <span>Du mardi au samedi</span>
          <a href="tel:+33232400277" style="font-weight:600">02 32 40 02 77</a>
          <a href="https://www.maison-barbe.com/" target="_blank" rel="noopener" style="font-weight:600">maison-barbe.com ↗</a>
        </div>
      </div>
      <div class="side-card dark">
        <span class="eyebrow">Vivre à côté</span>
        <p>Commerces, écoles, bus et prix des ventes autour de la rue du Maréchal Foch.</p>
        <a class="btn btn-gold" href="{near}">Explorer le quartier</a>
      </div>
      <div class="dashed">Découvrez tous les <a href="{r}commerces.html#bouche" style="font-weight:600">métiers de bouche de Louviers</a> dans l’annuaire.</div>
    </aside>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('portraits/maison-barbe.html', body)


# =========================================================
# DIAGNOSTICS : MODE D'EMPLOI
# =========================================================
ASSAINI_URL = 'https://www.agglo-seine-eure.fr/protegeons-ressource-eau/controlez-votre-assainissement/'
ASSAINI_FORM = 'https://formulaires.demarches.seine-eure.fr/cycle-de-l-eau/demande-de-diagnostic-assainissement/'
MAIRIE = 'https://www.ville-louviers.fr/'

DIAGS = [
    ('dpe', 'Diagnostic de performance énergétique (DPE)', 'Tous les logements, à la vente comme à la location.',
     'Valable 10 ans. Un DPE réalisé avant le 1<sup>er</sup> juillet 2021 n’est plus valable. Depuis le 1<sup>er</sup> janvier 2026, le calcul est plus favorable aux logements chauffés à l’électricité : leur étiquette peut s’améliorer, jamais se dégrader.'),
    ('audit', 'Audit énergétique', 'Vente d’une maison (ou d’un immeuble entier) classée E, F ou G.',
     'Valable 5 ans, à remettre dès la première visite. Les appartements en copropriété ne sont pas concernés. Les maisons classées D y seront soumises en 2034.'),
    ('amiante', 'Amiante', 'Logements dont le permis de construire date d’avant le 1<sup>er</sup> juillet 1997.',
     'Vente : repérage amiante, valable sans limite de durée si aucune trace n’est trouvée. Location : dossier amiante des parties privatives (DAPP) à tenir à disposition du locataire.'),
    ('plomb', 'Plomb (CREP)', 'Logements construits avant le 1<sup>er</sup> janvier 1949.',
     'Vente : valable 1 an (sans limite si absence de plomb). Location : valable 6 ans.'),
    ('elec', 'Électricité', 'Installation intérieure de plus de 15 ans.',
     'Vente : valable 3 ans. Location : valable 6 ans.'),
    ('gaz', 'Gaz', 'Installation intérieure de gaz de plus de 15 ans.',
     'Vente : valable 3 ans. Location : valable 6 ans.'),
    ('erp', 'État des risques (ERP)', 'Tous les logements, à la vente comme à la location.',
     'Moins de 6 mois. Il signale les risques naturels et technologiques (inondation, cavités, sols argileux…) connus pour la parcelle.'),
    ('carrez', 'Surface « loi Carrez »', 'Vente d’un lot en copropriété.',
     'Pas de durée de validité tant qu’aucun travaux ne modifie la surface. À la location, c’est la surface habitable (« loi Boutin ») qui figure au bail.'),
    ('assaini', 'Assainissement', 'Vente d’un logement, avec un contrôle spécifique dans l’Agglomération Seine-Eure.',
     'Dans l’Agglomération Seine-Eure, le contrôle est obligatoire à la vente même pour une maison raccordée au tout-à-l’égout, depuis 2014. Il est réalisé par un agent de l’Agglo, valable 3 ans, et coûte 100 € pour un logement. Pour une fosse (assainissement non collectif), le contrôle du SPANC doit dater de moins de 3 ans.'),
]


def page_diagnostics():
    r = ''
    cards = ''.join(f'''<article class="dg-card" id="d-{k}">
        <h3>{t}</h3><p class="dg-who">{who}</p><p>{det}</p></article>''' for k, t, who, det in DIAGS)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f"{html.unescape(re.sub('<[^>]+>', '', t))} : quand est-il obligatoire ?",
         "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', who + ' ' + det))}} for k, t, who, det in DIAGS]}
    body = head('Diagnostics immobiliers obligatoires à Louviers : le mode d’emploi · louviers.immo',
                'Vente ou location, appartement ou maison, année de construction : la liste des diagnostics obligatoires, leur durée de validité, et le contrôle d’assainissement exigé dans l’Agglomération Seine-Eure.',
                'diagnostics.html', r, jsonld=ld)
    body += header('diagnostics.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · Diagnostics</div>
    <span class="eyebrow">Vendre ou louer</span>
    <h1 style="margin-top:12px">Les diagnostics, <span class="it">mode d’emploi.</span></h1>
    <p class="lede" style="margin-top:20px">Répondez à cinq questions : vous saurez quels diagnostics faire réaliser pour votre logement, et combien de temps ils restent valables.</p>
  </div>
</section>

<section class="section" style="padding-top:48px">
  <div class="wrap dg-tool">
    <form class="dg-form" id="dg-form" novalidate>
      <fieldset><legend>Votre projet</legend>
        <div class="seg"><label><input type="radio" name="projet" value="vente" checked><span>Je vends</span></label><label><input type="radio" name="projet" value="location"><span>Je loue</span></label></div></fieldset>
      <fieldset><legend>Le logement</legend>
        <div class="seg"><label><input type="radio" name="type" value="appart" checked><span>Appartement en copropriété</span></label><label><input type="radio" name="type" value="maison"><span>Maison</span></label></div></fieldset>
      <fieldset><legend>Année du permis de construire</legend>
        <div class="seg seg3"><label><input type="radio" name="annee" value="1949"><span>Avant 1949</span></label><label><input type="radio" name="annee" value="1997"><span>1949 à mi-1997</span></label><label><input type="radio" name="annee" value="recent" checked><span>Après juillet 1997</span></label></div></fieldset>
      <fieldset><legend>Installations de plus de 15 ans</legend>
        <div class="seg"><label class="chk"><input type="checkbox" name="elec15" checked><span>Électricité</span></label><label class="chk"><input type="checkbox" name="gaz15"><span>Gaz</span></label></div>
        <p class="note">Dans le doute, comptez-les : un diagnostic en trop vaut mieux qu’une vente fragilisée.</p></fieldset>
      <fieldset><legend>Étiquette énergie, si vous la connaissez</legend>
        <div class="seg seg5"><label><input type="radio" name="dpe" value="AD"><span>A à D</span></label><label><input type="radio" name="dpe" value="E"><span>E</span></label><label><input type="radio" name="dpe" value="F"><span>F</span></label><label><input type="radio" name="dpe" value="G"><span>G</span></label><label><input type="radio" name="dpe" value="?" checked><span>Je ne sais pas</span></label></div></fieldset>
      <fieldset><legend>Eaux usées</legend>
        <div class="seg"><label><input type="radio" name="eaux" value="egout" checked><span>Tout-à-l’égout</span></label><label><input type="radio" name="eaux" value="fosse"><span>Fosse, micro-station</span></label></div>
        <label class="check" style="margin-top:12px"><input type="checkbox" name="agglo" checked> Logement situé dans l’Agglomération Seine-Eure (Louviers, Val-de-Reuil, Le Vaudreuil, Pont-de-l’Arche…)</label></fieldset>
    </form>
    <div class="dg-out" aria-live="polite">
      <div class="dg-out-head"><span class="dg-count" id="dg-count">—</span><span id="dg-title">diagnostics à prévoir</span></div>
      <ol class="dg-list" id="dg-list"></ol>
      <div class="dg-alert" id="dg-alert" hidden></div>
      <div class="dg-extra" id="dg-extra"></div>
      <a class="dg-cta plausible-event-name=Diagnostics+Vendeur" id="dg-cta" href="{CV_EST}">Vous vendez ? CV Immobilier organise vos diagnostics</a>
      <p class="note" style="margin-top:14px">Indicatif, selon la réglementation en vigueur en 2026. Termites et mérule ne sont exigés que dans les communes couvertes par un arrêté préfectoral : votre diagnostiqueur le vérifie pour vous.</p>
    </div>
  </div>
</section>

<section class="section ph-band-brique" id="assainissement">
  <div class="wrap split">
    <div class="a stack-lg">
      <span class="eyebrow">Spécificité locale</span>
      <h2>Le contrôle d’assainissement de l’Agglomération Seine-Eure</h2>
      <p class="lede">Ailleurs en France, seule une fosse doit être contrôlée avant une vente. Dans toutes les communes de l’Agglomération Seine-Eure, le contrôle est aussi obligatoire pour les logements raccordés au tout-à-l’égout : il vérifie que les eaux usées et les eaux de pluie partent bien chacune dans le bon réseau.</p>
    </div>
    <div class="b dg-steps">
      <ol class="clean">
        <li><span><b>Faites la demande en ligne</b> sur le formulaire de l’Agglo, dès la mise en vente.</span></li>
        <li><span><b>Un agent de l’Agglo vous appelle</b> pour fixer la visite.</span></li>
        <li><span><b>Le rapport</b> vaut diagnostic, valable 3 ans. Il est à remettre au notaire.</span></li>
        <li><span><b>Facture</b> d’environ 100 € pour un logement, un mois après la visite. En cas de non-conformité, la contre-visite est gratuite si les travaux sont faits dans les 6 mois.</span></li>
      </ol>
      <div class="two" style="margin-top:20px">
        <a class="btn btn-navy" href="{ASSAINI_FORM}" target="_blank" rel="noopener">Demander le contrôle</a>
        <a class="btn btn-line" href="{ASSAINI_URL}" target="_blank" rel="noopener">La page de l’Agglo</a>
      </div>
      <p class="note" style="margin-top:12px">Direction du Cycle de l’eau de l’Agglomération Seine-Eure : <a href="tel:+33276460352">02 76 46 03 52</a>.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head2"><h2>Chaque diagnostic en détail</h2>
      <p>Qui est concerné, et combien de temps le rapport reste valable.</p></div>
    <div class="dg-grid">{cards}</div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap split">
    <div class="a stack">
      <h2 style="font-size:clamp(26px,2.6vw,38px)">Faire réaliser ses diagnostics</h2>
      <p class="muted">Les diagnostics sont réalisés par un diagnostiqueur certifié, en une seule visite le plus souvent. Demandez plusieurs devis : les prix sont libres.</p>
    </div>
    <div class="b stack">
      <a class="info-card" href="https://diagnostiqueurs.din.developpement-durable.gouv.fr/index.action" target="_blank" rel="noopener"><strong>Annuaire officiel des diagnostiqueurs certifiés</strong><span>Ministère du Logement : recherche par commune et par diagnostic.</span></a>
      <a class="info-card" href="https://observatoire-dpe-audit.ademe.fr/" target="_blank" rel="noopener"><strong>Retrouver un DPE existant</strong><span>Observatoire de l’ADEME, avec le numéro à 13 caractères du rapport.</span></a>
      <a class="info-card" href="{CV_EST}"><strong>Vous vendez avec CV Immobilier ?</strong><span>Nous organisons les diagnostics avec des professionnels du secteur que nous connaissons.</span></a>
    </div>
  </div>
</section>
</main>
'''
    body += footer(r, ['assets/diagnostics.js'])
    write('diagnostics.html', body)


# =========================================================
# S'INSTALLER : LA CONCIERGERIE PRATIQUE
# =========================================================
def svc(name, url, note=''):
    n = f'<span>{note}</span>' if note else ''
    return f'<li><a href="{url}" target="_blank" rel="noopener">{name}</a>{n}</li>'


def page_conciergerie():
    r = ''
    blocks = [
        ('eau', 'pomme', 'L’eau', 'Le seul compteur sans choix de fournisseur.',
         '<p>À Louviers, l’eau potable est un service de l’Agglomération Seine-Eure, dont l’exploitation est confiée à Veolia jusqu’en 2028. Le nom de l’exploitant figure sur la dernière facture du logement : relevez l’index du compteur le jour de l’entrée, avec le vendeur ou le propriétaire.</p>',
         [svc('Veolia, ouvrir ou transférer un contrat', 'https://www.eau.veolia.fr/', 'exploitant à Louviers'),
          svc('Le cycle de l’eau à l’Agglomération Seine-Eure', 'https://www.agglo-seine-eure.fr/protegeons-ressource-eau/controlez-votre-assainissement/', 'assainissement, contrôles')]),
        ('elec', 'ocre', 'L’électricité', 'Un réseau unique, plusieurs fournisseurs.',
         '<p>Le compteur appartient au réseau Enedis ; vous choisissez librement votre fournisseur. Gardez sous la main le numéro du point de livraison (PDL, 14 chiffres, sur une ancienne facture ou sur le compteur Linky) et l’index du jour. La mise en service prend en général moins de 5 jours.</p>',
         [svc('EDF', 'https://particulier.edf.fr/', 'tarif réglementé ou offres de marché'),
          svc('Engie', 'https://particuliers.engie.fr/'),
          svc('TotalEnergies', 'https://www.totalenergies.fr/particuliers'),
          svc('Ekwateur', 'https://ekwateur.fr/', 'fournisseur d’énergies renouvelables'),
          svc('Comparateur officiel des offres', 'https://comparateur.energie-info.fr/', 'Médiateur national de l’énergie, gratuit et indépendant'),
          svc('Enedis, en cas de panne ou de compteur coupé', 'https://www.enedis.fr/', 'gestionnaire du réseau')]),
        ('gaz', 'brique', 'Le gaz', 'Si le logement est raccordé au gaz de ville.',
         '<p>Le réseau est géré par GRDF ; le contrat se prend auprès du fournisseur de votre choix, avec le numéro PCE (sur une ancienne facture ou le compteur Gazpar) et l’index du jour. Pour une cuve de propane ou une chaudière fioul, voyez avec le vendeur le contrat en cours.</p>',
         [svc('Engie', 'https://particuliers.engie.fr/'),
          svc('EDF', 'https://particulier.edf.fr/'),
          svc('TotalEnergies', 'https://www.totalenergies.fr/particuliers'),
          svc('Comparateur officiel des offres', 'https://comparateur.energie-info.fr/', 'Médiateur national de l’énergie'),
          svc('GRDF, urgence et sécurité gaz', 'https://www.grdf.fr/', 'gestionnaire du réseau')]),
        ('box', 'ciel', 'Internet et la box', 'À commander avant le déménagement : comptez une à trois semaines.',
         '<p>Commencez par tester l’adresse : vous saurez si la fibre est déjà arrivée dans l’immeuble ou la rue, et quels opérateurs y sont présents. Si une prise fibre existe, notez son numéro (inscrit sur le boîtier) : l’installation sera plus rapide.</p>',
         [svc('Tester l’éligibilité à la fibre', 'https://maconnexioninternet.arcep.fr/', 'carte officielle de l’Arcep'),
          svc('Orange', 'https://boutique.orange.fr/internet/offres-fibre'),
          svc('SFR', 'https://www.sfr.fr/offre-internet/'),
          svc('Bouygues Telecom', 'https://www.bouyguestelecom.fr/offres-internet'),
          svc('Free', 'https://www.free.fr/freebox/')]),
        ('dechets', 'pomme', 'Les déchets', 'La collecte est assurée par l’Agglomération Seine-Eure.',
         '<p>Jours de collecte des ordures ménagères et du tri (bacs et sacs jaunes) selon votre secteur, déchetteries, encombrants : tout est sur les sites de l’Agglo et de la Ville.</p>',
         [svc('Calendriers de collecte', 'https://www.agglo-seine-eure.fr/calendriers-collectes/', 'Agglomération Seine-Eure'),
          svc('Déchets et propreté', 'https://www.agglo-seine-eure.fr/dechets-proprete/', 'déchetteries, encombrants'),
          svc('Collecte des déchets à Louviers', 'https://www.ville-louviers.fr/mes-demarches/collecte-tri-selectif/collecte-des-dechets/', 'Ville de Louviers')]),
        ('demarches', 'ocre', 'Les démarches', 'Changer d’adresse une fois, prévenir tout le monde.',
         '<p>Le service en ligne de l’État transmet votre nouvelle adresse aux impôts, à la CAF, à l’Assurance maladie, à France Travail, au fichier des cartes grises et aux fournisseurs d’énergie participants. Pensez aussi à la réexpédition du courrier et à l’assurance habitation, obligatoire pour un locataire.</p>',
         [svc('Changement d’adresse en ligne', 'https://www.service-public.gouv.fr/particuliers/vosdroits/R11193', 'service-public.gouv.fr'),
          svc('Réexpédition du courrier', 'https://www.laposte.fr/demenagement-absence', 'La Poste'),
          svc('Inscription sur les listes électorales', 'https://www.service-public.gouv.fr/particuliers/vosdroits/R16396', 'service-public.gouv.fr')]),
        ('mairie', 'ciel', 'La mairie', 'L’hôtel de ville, 19 rue Pierre Mendès France.',
         '<p>Écoles et périscolaire, état civil, rendez-vous pour une carte d’identité ou un passeport, agenda des sorties : la Ville de Louviers répond au 02 32 09 58 58.</p>',
         [svc('Site de la Ville de Louviers', MAIRIE),
          svc('Enfance, écoles, jeunesse', 'https://www.ville-louviers.fr/ma-ville/enfance-education-jeunesse/', 'inscriptions scolaires'),
          svc('Rendez-vous carte d’identité et passeport', 'https://www.ville-louviers.fr/prise-de-rendez-vous/'),
          svc('Agenda des sorties', 'https://www.ville-louviers.fr/actualite-agenda/')]),
    ]
    nav = ''.join(f'<a class="cg-chip cg-{c}" href="#{k}">{t}</a>' for k, c, t, *_ in blocks)
    secs = ''.join(f'''<section class="cg-block cg-{c}" id="{k}">
      <div class="cg-head"><h2>{t}</h2><p class="cg-sub">{sub}</p></div>
      <div class="cg-body">{txt}<ul class="cg-links">{''.join(links)}</ul></div>
    </section>''' for k, c, t, sub, txt, links in blocks)
    body = head('Emménager à Louviers : eau, électricité, gaz, box, démarches · louviers.immo',
                'La conciergerie pratique pour s’installer à Louviers : ouvrir les compteurs d’eau, d’électricité et de gaz, choisir sa box internet, collecte des déchets et démarches, avec plusieurs prestataires à chaque fois.',
                'conciergerie.html', r)
    body += header('conciergerie.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · S’installer</div>
    <span class="eyebrow">La conciergerie pratique</span>
    <h1 style="margin-top:12px">Les clés en main, <span class="it">et tout le reste.</span></h1>
    <p class="lede" style="margin-top:20px">Eau, électricité, gaz, internet, déchets, démarches : ce qu’il faut ouvrir, qui appeler, et dans quel ordre, pour être chez soi dès le premier soir.</p>
    <div class="cg-nav">{nav}</div>
  </div>
</section>

<section class="section" style="padding-top:48px">
  <div class="wrap">
    <div class="cg-timeline">
      <div><b>Un mois avant</b><span>Commander la box internet, résilier ou transférer l’ancienne.</span></div>
      <div><b>Deux semaines avant</b><span>Choisir ses fournisseurs d’électricité et de gaz, demander la réexpédition du courrier.</span></div>
      <div><b>Le jour J</b><span>Relever les index d’eau, d’électricité et de gaz, avec photos datées.</span></div>
      <div><b>Le mois suivant</b><span>Déclarer le changement d’adresse en ligne : il met aussi à jour la carte grise.</span></div>
    </div>
    <div class="cg-list">{secs}</div>
    <p class="note" style="margin-top:28px">Les prestataires sont cités par ordre de taille et à titre indicatif : louviers.immo n’est rémunéré par aucun d’entre eux. Comparez les offres avant de choisir.</p>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('conciergerie.html', body)


# =========================================================
# PORTRAIT : INSTITUT DES PORTES DE L'EAU
# =========================================================
def page_portes_eau():
    r = '../'
    addr = '1 place de la Porte de l’Eau 27400 Louviers'
    near = adr_link(r, '1 place de la Porte de l\'Eau 27400 Louviers')
    web = 'https://institutdesportesdeleau.fr/'
    planity = 'https://www.planity.com/institut-des-portes-de-leau-27400-louviers'
    img = r + 'assets/img/portraits/portes-eau-'
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": "Institut des Portes de l’Eau, la beauté au naturel en centre-ville",
          "author": {"@type": "Organization", "name": "CV Immobilier"}, "publisher": {"@id": DOMAIN + "#cv"},
          "datePublished": "2026-10-01", "inLanguage": "fr-FR",
          "image": DOMAIN + "assets/img/portraits/portes-eau-accueil.jpg",
          "about": {"@type": "BeautySalon", "name": "Institut des Portes de l’Eau", "url": web,
                    "telephone": "+33982529216", "openingHours": "Mo-Sa 09:30-19:00",
                    "address": {"@type": "PostalAddress", "streetAddress": "1 place de la Porte de l’Eau", "postalCode": "27400",
                                "addressLocality": "Louviers", "addressCountry": "FR"}}}
    body = head('Institut des Portes de l’Eau, la beauté au naturel à Louviers · Portrait · louviers.immo',
                'Portrait de l’Institut des Portes de l’Eau, 1 place de la Porte de l’Eau à Louviers : soins visage bio Phyt’s, épilations Épiloderm, minceur, massages et manucure, par Élodie, esthéticienne depuis plus de 23 ans.',
                'portraits/institut-des-portes-de-l-eau.html', r, jsonld=ld)
    body += header('portraits.html', r, topbar=False)
    body += f'''<main id="contenu">
<div class="wrap">
  <header class="art-head">
    <div class="small muted"><a href="{r}index.html" class="muted">Accueil</a> · <a href="{r}portraits.html" class="muted">Portraits</a> · Centre-ville</div>
    <span class="eyebrow">Portrait n°02 · Institut de beauté</span>
    <h1>Institut des Portes de l’Eau,<br><span class="it">la beauté au naturel en centre-ville</span></h1>
    <div class="byline"><span>Par l’équipe CV Immobilier</span><span class="dot">·</span><span>Octobre 2026</span><span class="dot">·</span><span>4 min de lecture</span></div>
  </header>
  <figure style="margin:0">
    <div class="cover"><img src="{img}accueil.jpg" alt="L’accueil lumineux de l’Institut des Portes de l’Eau, avec son comptoir clair, ses soins Phyt’s et ses vitres décorées de feuillages" width="1800" height="1350" fetchpriority="high"></div>
    <figcaption class="cover-cap">L’accueil de l’institut, place de la Porte de l’Eau.</figcaption>
  </figure>
</div>

<section class="section">
  <div class="wrap art-grid">
    <article>
      <p class="chapo">Place de la Porte de l’Eau, en plein centre de Louviers, un nouvel institut a ouvert ses portes. Élodie, esthéticienne depuis plus de vingt-trois ans, y propose des soins du visage et du corps, des épilations et de la manucure, avec une ligne claire : des produits bio et des protocoles adaptés à chacun.</p>

      <figure class="art-photo">
        <img src="{img}elodie.jpg" alt="Élodie, esthéticienne, dans son institut, en tunique bleue brodée du logo des Portes de l’Eau" width="1400" height="1050" loading="lazy">
        <figcaption>Élodie, esthéticienne diplômée d’État et coach minceur certifiée.</figcaption>
      </figure>

      <div class="qa"><h2>Élodie, vingt-trois ans de métier</h2>
      <p>Esthéticienne diplômée d’État, Élodie travaille dans la beauté et le bien-être depuis plus de vingt-trois ans. Elle est aussi coach minceur certifiée Cursilhouette Bio et spécialiste des soins Phyt’s et de la technique japonaise Kobido. Avec ce nouvel institut, elle a voulu, selon ses propres mots, créer bien plus qu’un lieu de soins : « un espace de reconnexion à soi, où chaque geste est pensé pour vous ».</p></div>

      <div class="qa"><h2>Le bio comme fil conducteur</h2>
      <p>Les soins du visage sont réalisés avec Phyt’s, marque de cosmétiques certifiés bio. Pour les épilations, l’institut utilise la méthode Épiloderm®, une cire d’origine végétale à base de résine de pin. Et côté ongles, un mur de vernis Manucurist Green aux couleurs vives attend les clientes au comptoir.</p></div>

      <figure class="art-photo">
        <img src="{img}vernis.jpg" alt="Un mur de vernis à ongles de toutes les couleurs, de la marque Manucurist Green" width="1400" height="1050" loading="lazy">
        <figcaption>Le mur des vernis, du rose poudré au vert sauge.</figcaption>
      </figure>

      <div class="pull"><span class="q" aria-hidden="true">«</span><p>Un havre de paix dédié à votre beauté naturelle.</p><cite>— La promesse de l’Institut des Portes de l’Eau</cite></div>

      <div class="qa"><h2>Du visage au corps</h2>
      <p>La carte est large : soins du visage anti-âge, lifting naturel d’inspiration Kobido et photorajeunissement ; beauté du regard ; mains et pieds ; épilations ; massages. Pour la silhouette, Élodie propose neuf programmes Cursilhouette Bio adaptés à chaque morphotype, la madérothérapie et le drainage. L’institut dispose aussi d’une cabine de bronzage.</p></div>

      <div class="two">
        <figure class="art-photo"><img src="{img}cabine.jpg" alt="La cabine de soins, avec sa table chauffante et son papier peint à grandes feuilles noires et dorées" width="1400" height="1050" loading="lazy"><figcaption>La cabine de soins et d’épilation.</figcaption></figure>
        <figure class="art-photo"><img src="{img}brochure.jpg" alt="La brochure des soins de l’institut, ouverte sur la page des épilations" width="1400" height="1050" loading="lazy"><figcaption>La carte des soins, à emporter.</figcaption></figure>
      </div>

      <div class="qa"><h2>Une adresse au nom de la ville</h2>
      <p>L’institut tire son nom de la place où il est installé, la place de la Porte de l’Eau. Son logo, une arche, des vagues et une goutte, rappelle l’Eure qui traverse la ville. Une adresse de centre-ville, à quelques minutes à pied des commerces.</p></div>

      <figure class="art-photo">
        <img src="{img}enseigne.jpg" alt="L’enseigne de l’Institut des Portes de l’Eau, lettres bleues sur fond crème, sur une façade ancienne en brique" width="1600" height="1200" loading="lazy">
        <figcaption>L’enseigne, place de la Porte de l’Eau.</figcaption>
      </figure>

      <div class="box-sand stack" style="border-radius:24px">
        <span class="eyebrow">Pour y aller</span>
        <h2 style="font-size:clamp(24px,2.2vw,30px)">Institut des Portes de l’Eau</h2>
        <p style="font-size:17px;color:var(--text)">1 place de la Porte de l’Eau, 27400 Louviers · du lundi au samedi, de 9 h 30 à 19 h · <a href="tel:+33982529216" style="font-weight:600">09 82 52 92 16</a></p>
        <div class="two">
          <a class="btn btn-navy" href="{planity}" target="_blank" rel="noopener">Réserver en ligne ↗</a>
          <a class="btn btn-gold" href="{near}">Voir ce qu’il y a autour</a>
        </div>
      </div>
    </article>
    <aside>
      <div class="side-card">
        <span class="eyebrow">Infos pratiques</span>
        <span class="nm">Institut des Portes de l’Eau</span>
        <div class="small" style="color:var(--text);display:flex;flex-direction:column;gap:8px">
          <span>1 place de la Porte de l’Eau<br>27400 Louviers</span>
          <span>Du lundi au samedi<br>9 h 30 – 19 h</span>
          <a href="tel:+33982529216" style="font-weight:600">09 82 52 92 16</a>
          <a href="{web}" target="_blank" rel="noopener" style="font-weight:600">institutdesportesdeleau.fr ↗</a>
          <a href="{planity}" target="_blank" rel="noopener" style="font-weight:600">Réservation sur Planity ↗</a>
        </div>
      </div>
      <figure class="art-photo" style="max-width:100%"><img src="{img}porte.jpg" alt="Le logo de l’institut, une arche et des vagues bleues, sur une porte en chêne" width="1000" height="1333" loading="lazy"></figure>
      <div class="side-card dark">
        <span class="eyebrow">Vivre à côté</span>
        <p>Commerces, écoles, bus et prix des ventes autour de la place de la Porte de l’Eau.</p>
        <a class="btn btn-gold" href="{near}">Explorer le quartier</a>
      </div>
      <div class="dashed">Découvrez toutes les adresses <a href="{r}commerces.html#beaute" style="font-weight:600">beauté et bien-être de Louviers</a> dans l’annuaire.</div>
    </aside>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('portraits/institut-des-portes-de-l-eau.html', body)


# =========================================================
# PORTRAIT : AUX DÉLICES DE LOUVIERS — MAISON GUINCÊTRE
# =========================================================
def page_guincetre():
    r = '../'
    near = adr_link(r, '38 rue du Maréchal Foch 27400 Louviers')
    web = 'https://auxdelicesdelouviers.fr/'
    cmd = 'https://commande-auxdelicesdelouviers.fr/'
    img = r + 'assets/img/portraits/guincetre-'
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": "Aux Délices de Louviers, une histoire de famille, de Louviers au Vaudreuil",
          "author": {"@type": "Organization", "name": "CV Immobilier"}, "publisher": {"@id": DOMAIN + "#cv"},
          "datePublished": "2026-10-01", "inLanguage": "fr-FR",
          "image": DOMAIN + "assets/img/portraits/guincetre-equipe.jpg",
          "about": [{"@type": "Bakery", "name": "Aux Délices de Louviers", "url": web, "telephone": "+33232400463",
                     "address": {"@type": "PostalAddress", "streetAddress": "38 rue du Maréchal Foch", "postalCode": "27400",
                                 "addressLocality": "Louviers", "addressCountry": "FR"}},
                    {"@type": "Bakery", "name": "Maison Guincêtre", "url": web + "maison-guincetre/", "telephone": "+33232400463",
                     "address": {"@type": "PostalAddress", "streetAddress": "10 place du Général de Gaulle", "postalCode": "27100",
                                 "addressLocality": "Le Vaudreuil", "addressCountry": "FR"}}]}
    body = head('Aux Délices de Louviers, la boulangerie Guincêtre, de Louviers au Vaudreuil · Portrait · louviers.immo',
                'Portrait de la boulangerie-pâtisserie Aux Délices de Louviers, 38 rue du Maréchal Foch : la famille Guincêtre, finaliste de La Meilleure Boulangerie de France sur M6, et sa nouvelle Maison Guincêtre au Vaudreuil.',
                'portraits/aux-delices-de-louviers.html', r, jsonld=ld)
    body += header('portraits.html', r, topbar=False)
    body += f'''<main id="contenu">
<div class="wrap">
  <header class="art-head">
    <div class="small muted"><a href="{r}index.html" class="muted">Accueil</a> · <a href="{r}portraits.html" class="muted">Portraits</a> · Centre-ville</div>
    <span class="eyebrow">Portrait n°03 · Boulanger-pâtissier</span>
    <h1>Aux Délices de Louviers,<br><span class="it">une histoire de famille, de Louviers au Vaudreuil</span></h1>
    <div class="byline"><span>Par l’équipe CV Immobilier</span><span class="dot">·</span><span>Octobre 2026</span><span class="dot">·</span><span>4 min de lecture</span></div>
  </header>
  <figure style="margin:0">
    <div class="cover"><img src="{img}equipe.jpg" alt="L’équipe de la boulangerie Aux Délices de Louviers réunie devant la boutique, avec l’équipe de tournage de M6" width="1280" height="853" fetchpriority="high" style="object-position:50% 40%"></div>
    <figcaption class="cover-cap">L’équipe devant la boutique de la rue du Maréchal Foch, lors du tournage de La Meilleure Boulangerie de France sur M6.</figcaption>
  </figure>
</div>

<section class="section">
  <div class="wrap art-grid">
    <article>
      <p class="chapo">Rue du Maréchal Foch, la vitrine bleue d’Aux Délices de Louviers est un repère des gourmands. La maison a été fondée en 1996. Derrière, la famille Guincêtre : trois générations de boulangers et de pâtissiers, une finale nationale sur M6, et désormais une seconde boutique au Vaudreuil, la Maison Guincêtre.</p>

      <div class="qa"><h2>Trois générations de passion boulangère</h2>
      <p>Anne et Franck Guincêtre, dont les noms s’affichent au-dessus de la vitrine, en ont fait une affaire de famille, aujourd’hui portée aussi par Maxime, le fils de Franck, pâtissier. La devise de la maison tient en une phrase : « une histoire de famille, de goût et de passion ».</p></div>

      <div class="qa"><h2>Tout est fait sur place, chaque jour</h2>
      <p>Pains, viennoiseries, pâtisseries, traiteur : tout est préparé au laboratoire, avec des farines françaises et des ingrédients de saison, en circuit court dès que c’est possible. La maison résume ses engagements en trois mots : l’artisanat, « vrai et sans compromis » ; la qualité, « du goût à la présentation » ; et les produits locaux.</p>
      <p style="margin-top:14px">En vitrine, les baguettes côtoient le pain muesli et la focaccia ; les croissants, les brioches ; les tartes, les entremets et les éclairs. On y commande aussi les gâteaux d’anniversaire personnalisés, les petits fours et les cakes de voyage.</p></div>

      <figure class="art-photo">
        <img src="{img}trompe-oeil.jpg" alt="Une pâtisserie rouge en forme de fruit, tenue dans la main devant la vitrine des entremets" width="1200" height="1488" loading="lazy">
        <figcaption>Une création de la maison, devant la vitrine des entremets.</figcaption>
      </figure>

      <div class="qa"><h2>Finalistes de La Meilleure Boulangerie de France</h2>
      <p>En 2023, pour la dixième saison de l’émission de M6, Franck et Maxime Guincêtre ont représenté la Haute-Normandie. Le duo père et fils a remporté la sélection régionale et s’est qualifié pour la finale nationale, diffusée en mai 2023. « Le jury a aimé nos produits fétiches », résumait alors Maxime.</p></div>

      <div class="pull"><span class="q" aria-hidden="true">«</span><p>Là, on a un super duo, très original en plus. Il y a le père et le fils.</p><cite>— Le jury de La Meilleure Boulangerie de France, M6, 2023</cite></div>

      <div class="qa"><h2>Le jeudi, c’est éclairs</h2>
      <p>Chaque jeudi, sauf en août et en décembre, la boutique propose quatorze sortes d’éclairs : vanille, mousse au chocolat, caramel-popcorn, chocolat blanc et framboise, spéculoos, citron-yuzu… Pour cinq éclairs achetés, le sixième est offert.</p></div>

      <div class="qa"><h2>La Maison Guincêtre, au Vaudreuil</h2>
      <p>La famille a ouvert une seconde adresse au 10 place du Général de Gaulle, au Vaudreuil : la Maison Guincêtre, « l’atelier gourmand, entre tradition et création ». Boutique et laboratoire à la fois, elle s’est fait une spécialité des wedding cakes, des gâteaux personnalisés et des pièces montées.</p></div>

      <figure class="art-photo">
        <img src="{img}facades.jpg" alt="Les deux boutiques côte à côte : la vitrine bleue Aux Délices de Louviers et la façade claire de la Maison Guincêtre au Vaudreuil" width="547" height="365" loading="lazy">
        <figcaption>À gauche, Aux Délices de Louviers ; à droite, la Maison Guincêtre au Vaudreuil.</figcaption>
      </figure>

      <div class="box-sand stack" style="border-radius:24px">
        <span class="eyebrow">Pour y aller</span>
        <h2 style="font-size:clamp(24px,2.2vw,30px)">Aux Délices de Louviers</h2>
        <p style="font-size:17px;color:var(--text)">38 rue du Maréchal Foch, 27400 Louviers · du lundi au samedi de 6 h 30 à 19 h 45, le dimanche de 7 h 30 à 19 h, fermé le mercredi · <a href="tel:+33232400463" style="font-weight:600">02 32 40 04 63</a></p>
        <p style="font-size:17px;color:var(--text)"><strong style="color:var(--navy)">Maison Guincêtre</strong> : 10 place du Général de Gaulle, 27100 Le Vaudreuil · du mardi au samedi de 6 h 30 à 13 h 15 et de 15 h à 19 h 15, le dimanche de 7 h à 13 h, fermé le lundi.</p>
        <div class="two">
          <a class="btn btn-navy" href="{cmd}" target="_blank" rel="noopener">Commander en ligne ↗</a>
          <a class="btn btn-gold" href="{near}">Voir ce qu’il y a autour</a>
        </div>
      </div>
    </article>
    <aside>
      <div class="side-card">
        <img src="{img}logo.jpg" alt="Logo Maison Guincêtre, Louviers – Le Vaudreuil" width="445" height="449" loading="lazy" style="width:140px;align-self:center">
        <span class="eyebrow">Infos pratiques</span>
        <span class="nm">Aux Délices de Louviers</span>
        <div class="small" style="color:var(--text);display:flex;flex-direction:column;gap:8px">
          <span>38 rue du Maréchal Foch<br>27400 Louviers</span>
          <span>Fermé le mercredi</span>
          <a href="tel:+33232400463" style="font-weight:600">02 32 40 04 63</a>
          <a href="{web}" target="_blank" rel="noopener" style="font-weight:600">auxdelicesdelouviers.fr ↗</a>
          <a href="https://www.instagram.com/maisonguincetre/" target="_blank" rel="noopener" style="font-weight:600">Instagram @maisonguincetre ↗</a>
        </div>
      </div>
      <div class="side-card dark">
        <span class="eyebrow">Vivre à côté</span>
        <p>Commerces, écoles, bus et prix des ventes autour de la rue du Maréchal Foch.</p>
        <a class="btn btn-gold" href="{near}">Explorer le quartier</a>
      </div>
      <div class="dashed">Toutes les <a href="{r}commerces.html#boulangeries" style="font-weight:600">boulangeries et pâtisseries de Louviers</a> dans l’annuaire.</div>
    </aside>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('portraits/aux-delices-de-louviers.html', body)


# =========================================================
# PORTRAIT : GEORGET CYCLES — CULTURE VÉLO
# =========================================================
def page_georget():
    r = '../'
    near = adr_link(r, '1 boulevard du Docteur Postel 27400 Louviers')
    web = 'https://www.georgetcycles.fr/'
    fb = 'https://www.facebook.com/culturevelogeorget/'
    img = r + 'assets/img/portraits/georget-'
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": "Georget Cycles, le vélo à Louviers depuis 1928",
          "author": {"@type": "Organization", "name": "CV Immobilier"}, "publisher": {"@id": DOMAIN + "#cv"},
          "datePublished": "2026-10-01", "inLanguage": "fr-FR",
          "image": DOMAIN + "assets/img/portraits/georget-facade.jpg",
          "about": {"@type": "BikeStore", "name": "Georget Cycles — Culture Vélo", "url": web, "telephone": "+33232400622",
                    "sameAs": [fb],
                    "address": {"@type": "PostalAddress", "streetAddress": "1 boulevard du Docteur Postel", "postalCode": "27400",
                                "addressLocality": "Louviers", "addressCountry": "FR"}}}
    body = head('Georget Cycles, le vélo à Louviers depuis 1928 · Portrait · louviers.immo',
                'Portrait de Georget Cycles — Culture Vélo, 1 boulevard du Docteur Postel à Louviers : un magasin de vélos familial depuis 1928, repris par le Lovérien Cédric Lecerf, plus de 1 000 m², 400 vélos en stock et un atelier.',
                'portraits/georget-cycles.html', r, jsonld=ld)
    body += header('portraits.html', r, topbar=False)
    body += f'''<main id="contenu">
<div class="wrap">
  <header class="art-head">
    <div class="small muted"><a href="{r}index.html" class="muted">Accueil</a> · <a href="{r}portraits.html" class="muted">Portraits</a> · Les Tisserands</div>
    <span class="eyebrow">Portrait n°04 · Magasin de vélos</span>
    <h1>Georget Cycles,<br><span class="it">le vélo à Louviers depuis 1928</span></h1>
    <div class="byline"><span>Par l’équipe CV Immobilier</span><span class="dot">·</span><span>Octobre 2026</span><span class="dot">·</span><span>4 min de lecture</span></div>
  </header>
  <figure style="margin:0">
    <div class="cover"><img src="{img}facade.jpg" alt="Le magasin Culture Vélo Georget, ses grandes verrières en pointe et ses vitrines de vélos, boulevard du Docteur Postel" width="1800" height="1078" fetchpriority="high"></div>
    <figcaption class="cover-cap">Le magasin du boulevard du Docteur Postel, près du centre commercial des Tisserands.</figcaption>
  </figure>
</div>

<section class="section">
  <div class="wrap art-grid">
    <article>
      <p class="chapo">Près d’un siècle de vélo à Louviers. Né d’une histoire de famille commencée en 1928, Georget Cycles est aujourd’hui porté par Cédric Lecerf, un Lovérien pur souche. Sous l’enseigne Culture Vélo, le magasin du boulevard du Docteur Postel réunit plus de 400 vélos en stock et un atelier.</p>

      <div class="qa"><h2>Une histoire de famille commencée en 1928</h2>
      <p>Tout commence à Rouen, en 1920, quand les grands-parents maternels d’Olivier Georget ouvrent un magasin de cycles. En 1928, ils s’installent à Louviers, rue Saint-Jean. Ses parents reprennent le flambeau en 1956, puis la troisième génération prend le relais en 1984. En 1992, Olivier Georget ouvre l’espace du boulevard du Docteur Postel, sur 1 000 m², agrandi en 2012.</p></div>

      <div class="qa"><h2>2018 : un Lovérien reprend le guidon</h2>
      <p>En 2018, après sa rencontre avec Olivier Georget, Cédric Lecerf devient propriétaire du magasin. Lovérien, il perpétue le nom et le savoir-faire de la maison, avec une équipe de vendeurs et de mécaniciens.</p></div>

      <figure class="art-photo">
        <img src="{img}velo.jpg" alt="Un cycliste sur un vélo électrique devant le magasin Culture Vélo Georget Louviers" width="1280" height="853" loading="lazy">
        <figcaption>Devant le magasin, sous l’enseigne Culture Vélo Georget Louviers.</figcaption>
      </figure>

      <div class="pull"><span class="q" aria-hidden="true">«</span><p>Depuis 1928, votre magasin Georget Cycles est le spécialiste du cycle en Normandie.</p><cite>— La devise de la maison</cite></div>

      <div class="qa"><h2>Plus de 400 vélos en stock</h2>
      <p>Vélos de ville, de route, VTT, vélos électriques pour tous les usages, vélos cargos et vélos enfants : le magasin compte plus de 400 vélos en stock et 70 000 références d’accessoires au catalogue. On y trouve notamment Trek, Cannondale, Lapierre, Scott, Look, Orbea, Moustache, Winora ou Babboe, et un espace consacré aux cyclistes femmes, Velleo.</p></div>

      <figure class="art-photo">
        <img src="{img}magasin.jpg" alt="Une rangée de vélos électriques et de vélos de route dans le magasin" width="2000" height="660" loading="lazy">
        <figcaption>Dans le magasin, les vélos électriques et les vélos de route.</figcaption>
      </figure>

      <div class="qa"><h2>Un atelier pour tous les vélos</h2>
      <p>L’atelier assure l’entretien, la réparation et la personnalisation de tous les types de vélos, avec des techniciens formés par les grands constructeurs. Pratique aussi : le retrait en magasin des accessoires commandés en ligne, et un accès rapide depuis l’A13.</p></div>

      <div class="qa"><h2>Le vélo en vidéo</h2>
      <p>Cédric Lecerf fait vivre le magasin en vidéo sur la page Facebook Culture Vélo Georget, suivie par plus de 4 700 personnes.</p>
      <p style="margin-top:14px"><a class="link-u" href="{fb}" target="_blank" rel="noopener">Voir les vidéos sur Facebook ↗</a></p></div>

      <div class="box-sand stack" style="border-radius:24px">
        <span class="eyebrow">Pour y aller</span>
        <h2 style="font-size:clamp(24px,2.2vw,30px)">Georget Cycles — <span class="it">Culture Vélo</span></h2>
        <p style="font-size:17px;color:var(--text)">1 boulevard du Docteur Postel, 27400 Louviers, près du centre commercial des Tisserands · <a href="tel:+33232400622" style="font-weight:600">02 32 40 06 22</a></p>
        <div class="two">
          <a class="btn btn-navy" href="{web}" target="_blank" rel="noopener">Visiter georgetcycles.fr ↗</a>
          <a class="btn btn-gold" href="{near}">Voir ce qu’il y a autour</a>
        </div>
      </div>
    </article>
    <aside>
      <div class="side-card">
        <span class="eyebrow">Infos pratiques</span>
        <span class="nm">Georget Cycles<br><span style="font-size:17px" class="it">Culture Vélo</span></span>
        <div class="small" style="color:var(--text);display:flex;flex-direction:column;gap:8px">
          <span>1 boulevard du Docteur Postel<br>27400 Louviers</span>
          <a href="tel:+33232400622" style="font-weight:600">02 32 40 06 22</a>
          <a href="{web}" target="_blank" rel="noopener" style="font-weight:600">georgetcycles.fr ↗</a>
          <a href="{fb}" target="_blank" rel="noopener" style="font-weight:600">Facebook Culture Vélo Georget ↗</a>
        </div>
      </div>
      <div class="side-card dark">
        <span class="eyebrow">Vivre à côté</span>
        <p>Commerces, écoles, bus et prix des ventes autour du boulevard du Docteur Postel.</p>
        <a class="btn btn-gold" href="{near}">Explorer le quartier</a>
      </div>
      <div class="dashed">Toutes les adresses <a href="{r}commerces.html#loisirs" style="font-weight:600">culture et loisirs de Louviers</a> dans l’annuaire.</div>
    </aside>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('portraits/georget-cycles.html', body)


# =========================================================
# MERCI (après l'envoi d'un formulaire)
# =========================================================
def page_merci():
    r = ''
    body = head('Merci · louviers.immo', 'Votre demande a bien été envoyée à CV Immobilier.', 'merci.html', r, noindex=True)
    body += header(None, r, topbar=False)
    body += f'''<main id="contenu">
<section class="section">
  <div class="wrap stack-lg" style="max-width:760px;text-align:center;align-items:center">
    <h1 style="font-size:clamp(38px,5vw,64px)">Merci, <span class="it">c’est bien reçu.</span></h1>
    <p class="lede">L’équipe CV Immobilier vous recontacte rapidement. Pour toute question : <a href="tel:+33232402228">02 32 40 22 28</a> ou {MAIL}.</p>
    <a class="btn btn-navy" href="{r}index.html">Retour au guide</a>
  </div>
</section>
</main>
'''
    body += footer(r)
    write('merci.html', body)


# =========================================================
# OUTIL INTERNE : CODE QR « VIVRE ICI »
# =========================================================
def page_qr():
    r = ''
    body = head('Code QR « Vivre ici » · outil interne · louviers.immo', 'Outil interne CV Immobilier : code QR vers la page d’une adresse.', 'outil-qr.html', r, noindex=True)
    body += header(None, r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs">Outil interne CV Immobilier · page non référencée</div>
    <span class="eyebrow">Annonces et vitrines</span>
    <h1 style="margin-top:12px">Code QR <span class="it">« Vivre ici »</span></h1>
    <p class="lede" style="margin-top:20px">Tapez l’adresse d’un bien : vous obtenez un code QR qui ouvre sa page « Mon adresse ». À imprimer sur l’annonce, la vitrine ou le panneau.</p>
  </div>
</section>
<section class="section" style="padding-top:48px">
  <div class="wrap qr-tool">
    <form class="lform" id="qr-form" novalidate>
      <div class="field"><label for="qr-adr">Adresse du bien</label><input id="qr-adr" required placeholder="Numéro, rue, commune"></div>
      <button class="btn btn-navy" type="submit" style="align-self:flex-start">Créer le code QR</button>
      <p class="note" id="qr-msg" aria-live="polite"></p>
    </form>
    <div class="qr-out" id="qr-out" hidden>
      <div class="qr-card">
        <div id="qr-svg"></div>
        <p class="qr-cap">Vivre ici : scannez pour découvrir le quartier</p>
        <p class="qr-url" id="qr-url"></p>
      </div>
      <div class="two">
        <a class="btn btn-gold" id="qr-png" download="qr-vivre-ici.png" href="#">Télécharger en PNG</a>
        <a class="btn btn-line" id="qr-svgdl" download="qr-vivre-ici.svg" href="#">Télécharger en SVG</a>
      </div>
    </div>
  </div>
</section>
</main>
'''
    body += footer(r, ['assets/vendor/qrcode/qrcode.js', 'assets/qr.js'])
    write('outil-qr.html', body)


# =========================================================
# COMPARATEUR DE QUARTIERS
# =========================================================
def page_comparer():
    r = ''
    def col(n, ph):
        return f'''<div class="cmp-col" id="cmp-{n}">
        <div class="field"><label for="cmp-q{n}">Adresse ou quartier n°{n}</label><input id="cmp-q{n}" placeholder="{ph}"></div>
        <div class="cmp-res" id="cmp-r{n}"><p class="muted">—</p></div>
      </div>'''
    body = head('Comparer deux quartiers de Louviers · louviers.immo',
                'Deux adresses de Louviers côte à côte : prix médians des ventes réelles, écoles les plus proches, temps de trajet vers la gare et l’A13.',
                'comparer.html', r)
    body += header('quartiers.html', r, topbar=False)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · <a href="{r}quartiers.html">Quartiers</a> · Comparer</div>
    <span class="eyebrow">Hésiter entre deux quartiers</span>
    <h1 style="margin-top:12px">Comparer <span class="it">deux adresses</span></h1>
    <p class="lede" style="margin-top:20px">Prix des ventes autour, écoles les plus proches, temps vers la gare et l’autoroute : côte à côte.</p>
  </div>
</section>
<section class="section" style="padding-top:48px">
  <div class="wrap stack-lg">
    <form id="cmp-form" class="stack-lg" novalidate>
      <div class="cmp-grid">
        {col(1, 'Ex. : place de la Halle aux Drapiers, Louviers')}
        {col(2, 'Ex. : Le Vaudreuil')}
      </div>
      <button class="btn btn-navy plausible-event-name=Comparateur" type="submit" style="align-self:flex-start">Comparer</button>
    </form>
    <p class="note">Prix : médiane des ventes à moins de 500 m (données DVF), affichée dès 3 ventes. Temps estimés à partir des distances, en voiture. Écoles et gares : OpenStreetMap.</p>
  </div>
</section>
</main>
'''
    body += footer(r, ['assets/adresse.js', 'assets/comparer.js'])
    write('comparer.html', body)


def page_a_vendre():
    r = ''
    body = head('Biens à vendre à Louviers et alentour · louviers.immo',
                'Les maisons et appartements à vendre par CV Immobilier à Louviers et dans l’Agglomération Seine-Eure, mis à jour chaque nuit.',
                'a-vendre.html', r)
    body += header(None, r, topbar=False)
    opts = lambda L: ''.join(f'<option value="{v}">{l}</option>' for v, l in L)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · À vendre</div>
    <span class="eyebrow">Les biens de l’agence</span>
    <h1 style="margin-top:12px">À vendre à Louviers <span class="it">et alentour</span></h1>
    <p class="lede" style="margin-top:20px">Les maisons et appartements proposés par CV Immobilier. Chaque fiche ouvre l’annonce complète, avec toutes les photos, sur cvimmobilier.fr.</p>
  </div>
</section>
<section class="section" style="padding-top:48px">
  <div class="wrap">
    <form id="bv-form" class="bv-form" novalidate>
      <div class="field"><label for="bv-commune">Commune</label><select id="bv-commune" name="commune"><option value="">Toutes les communes</option></select></div>
      <div class="field"><label for="bv-type">Type de bien</label><select id="bv-type" name="type">{opts([('', 'Tous'), ('Maison', 'Maison'), ('Appartement', 'Appartement'), ('Autre', 'Autre (terrain, propriété…)')])}</select></div>
      <div class="field"><label for="bv-budget">Budget maximum</label><select id="bv-budget" name="budget">{opts([('', 'Sans limite'), ('150000', '150 000 €'), ('200000', '200 000 €'), ('250000', '250 000 €'), ('300000', '300 000 €'), ('400000', '400 000 €')])}</select></div>
      <div class="field"><label for="bv-tri">Trier par</label><select id="bv-tri" name="tri">{opts([('', 'Les plus récents'), ('prix', 'Prix croissant'), ('prix-', 'Prix décroissant')])}</select></div>
    </form>
    <p class="bv-count" id="bv-count" aria-live="polite">Chargement des annonces…</p>
    <div class="biens biens-all" data-biens data-all></div>
    <div class="biens-foot">
      <p class="note" data-biens-maj>Annonces de cvimmobilier.fr, mises à jour chaque nuit.</p>
      <a class="link-u" href="{CV_SITE}">Le site de l’agence, cvimmobilier.fr</a>
    </div>
  </div>
</section>
</main>
'''
    body += footer(r, ['assets/biens.js'])
    write('a-vendre.html', body)


for fn in [page_a_vendre, page_merci, page_qr, page_comparer, page_georget, page_guincetre, page_portes_eau, page_diagnostics, page_conciergerie, page_index, page_adresse, page_prix, page_quartiers, page_centre_ville, page_portraits,
           page_portrait_modele, page_outils, page_commerces, page_barbe, page_apropos, page_mentions, page_404]:
    fn()
