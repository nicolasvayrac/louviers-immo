# -*- coding: utf-8 -*-
# Exécuté dans l'espace de noms de gen.py (head, header, footer, write, TEAM, CV_EST…).
# Pages « Le Louviers de… » : une page par membre de l'équipe, à partir de ce qu'ils racontent.
# Récits de ventes : jamais de nom ni d'adresse précise de client.

def _q(slug, n, nom, c):
    return {'slug': slug, 'n': n, 'nom': nom, 'c': c}

_QU = {
    'coeur-de-ville': _q('coeur-de-ville', 1, 'Cœur de Ville', '#bad735'),
    'les-monts': _q('les-monts', 4, 'Les Monts', '#e974ad'),
    'les-amoureux': _q('les-amoureux', 10, 'Les Amoureux', '#64b6ac'),
    'maison-rouge': _q('maison-rouge', 11, 'Maison Rouge', '#fdcc87'),
    'pichou': _q('pichou', 12, 'Pichou', '#bfa4c9'),
    'le-clos-saint-lubin': _q('le-clos-saint-lubin', 13, 'Le Clos Saint-Lubin', '#fcef08'),
}

AGENTS = {
    'arthur-godefroy': {
        'prenom': 'Arthur', 'nom': 'Arthur Godefroy', 'de': 'd’Arthur',
        'facts': [('Né à', 'Louviers'), ('Son quartier', '<a class="link-u" href="../quartiers/les-amoureux.html">Les Amoureux</a>'), ('Son coup de cœur', '<a class="link-u" href="https://www.facebook.com/GrainDeCafe.Louviers" target="_blank" rel="noopener">Grain de café 27</a>')],
        'lede': 'Né à Louviers, Arthur y a grandi, y a fait toute sa scolarité et y vit toujours, dans le quartier des Amoureux. À Louviers, il est comme un poisson dans l’eau.',
        'quote': None,
        'quartiers': ['les-amoureux', 'coeur-de-ville'],
        'quartiers_txt': 'Son quartier depuis l’enfance, et l’hyper-centre, où se font ses ventes préférées.',
        'sections': [
            ('Louviers, depuis toujours',
             '<p>Arthur a grandi aux Amoureux, son quartier préféré, où il vit encore aujourd’hui. Il a fait toute sa scolarité à Louviers : l’école Jules-Ferry, le collège Les Fougères puis le lycée Les Fontenelles. En 5<sup>e</sup>, il a même siégé au conseil municipal des jeunes.</p>'),
            ('Ses adresses',
             '<p>Ce qu’il aime le plus à Louviers, ce sont ses commerçants. Pour un café ou un thé, comme à la maison, c’est au <a class="link-u" href="https://www.facebook.com/GrainDeCafe.Louviers" target="_blank" rel="noopener">Grain de café 27</a>, rue du Matrey. Il a aussi ses habitudes chez Bonobo et au Ragnar. Le samedi matin, c’est le marché.</p>'
             '<p>Très sportif, Arthur joue au <a class="link-u" href="https://www.louviersvolleyball.com/" target="_blank" rel="noopener">Louviers Volley-Ball</a> et au <a class="link-u" href="https://louviers-tennis-club.com/" target="_blank" rel="noopener">Louviers Tennis Club</a>, et ne rate pas une occasion de sortir son vélo.</p>'),
            ('Les ventes qui l’ont marqué',
             '<p>Ses ventes préférées se font en hyper-centre : c’est le Louviers de toute sa vie, et il sait mieux que personne en parler.</p>'
             '<p>Il y a cette maison bourgeoise face à l’école de musique, entièrement à rénover. Une maman, locataire à Louviers, attendait patiemment le bien qui lui ressemblerait. Elle l’a trouvé, et elle la rénove de fond en comble avec les conseils d’Arthur et des artisans partenaires de l’agence.</p>'
             '<p>Et cette maison de ville place de la République, dont la propriétaire n’y croyait plus : le bien avait été mal estimé au départ. Arthur l’a vendue à des investisseurs lovériens, qui vont la rénover et la louer.</p>'),
            ('Son conseil',
             '<p>Faire la descente en kayak de la vallée de l’Eure. Louviers se découvre aussi depuis la rivière.</p>'),
        ],
        'photo': None,
        'ventes': [('agents/arthur-maison-bourgeoise.jpg', 'La maison bourgeoise face à l’école de musique.'), ('agents/arthur-maison-de-ville.jpg', 'La maison de ville, place de la République.')],
    },
    'jessica-mourad': {
        'prenom': 'Jessica', 'nom': 'Jessica Mourad', 'de': 'de Jessica',
        'facts': [('Née à', 'Louviers'), ('Elle vit à', 'Léry, dans l’agglomération'), ('Ses adresses', 'Les Joliettes, Les Floralies')],
        'lede': 'Née à Louviers, Jessica vit aujourd’hui à Léry, tout près, et sa famille à Pinterville. Elle est partout à Louviers, et elle y connaît beaucoup de monde.',
        'quote': None,
        'quartiers': ['coeur-de-ville'],
        'quartiers_txt': 'Le centre-ville et ses commerces, qu’elle fréquente chaque semaine.',
        'sections': [
            ('Louviers, ses racines',
             '<p>Jessica est née à Louviers. Elle y a été à l’école Notre-Dame puis au collège Saint-Louis. Elle vit aujourd’hui à Léry, dans l’Agglomération Seine-Eure, mais Louviers reste sa ville : elle y est très présente, et il est rare qu’elle traverse le centre sans croiser quelqu’un qu’elle connaît.</p>'),
            ('Ses adresses',
             '<p>Jessica adore les commerces de Louviers : <a class="link-u" href="https://lesjoliettes.fr/" target="_blank" rel="noopener">Les Joliettes</a>, Kenzy, Leonidas, rue du Général-de-Gaulle, et <a class="link-u" href="https://www.lesfloralies.fr/" target="_blank" rel="noopener">Les Floralies</a>.</p>'
             '<p>Ce qu’elle préfère à Louviers ? La qualité de ses commerces, et le stationnement gratuit, qui permet d’en profiter sans y penser.</p>'),
            ('La vente qui l’a marquée',
             '<p>Un appartement place de la Porte-de-l’Eau, qui appartenait à un jeune propriétaire. L’acquéreuse, une retraitée, cherchait une maison. Elle a eu un coup de cœur pour l’appartement, et elle ne l’a jamais regretté. Depuis, Jessica et ses clients sont devenus des proches.</p>'),
        ],
        'photo': None,
        'ventes': [('agents/jessica-immeuble.jpg', 'La résidence, place de la Porte-de-l’Eau.'), ('agents/jessica-sejour.jpg', 'Le séjour qui a fait craquer l’acquéreuse.')],
    },
    'nicolas-vayrac': {
        'prenom': 'Nicolas', 'nom': 'Nicolas Vayrac', 'de': 'de Nicolas',
        'facts': [('Né à', 'Louviers'), ('Son quartier', '<a class="link-u" href="../quartiers/pichou.html">Pichou</a>'), ('Dans l’immobilier depuis', '2016')],
        'lede': 'Né à Louviers, Nicolas est revenu en 2016, après ses études à Rouen et à Paris, pour rejoindre l’agence familiale. Dix ans plus tard, il la dirige.',
        'quote': '« À Louviers, tout est simple d’accès. Ce que j’aime, c’est tout faire à pied. »',
        'quartiers': ['les-monts', 'maison-rouge', 'pichou', 'le-clos-saint-lubin'],
        'quartiers_txt': 'Ceux où il a grandi et vécu, et le Clos Saint-Lubin, qu’il aime pour son calme.',
        'sections': [
            ('Louviers, de quartier en quartier',
             '<p>« J’ai grandi aux Monts. Petit, je m’y ennuyais parfois ; aujourd’hui, je suis convaincu par ce quartier résidentiel et familial. J’ai été à l’école Notre-Dame, au collège Saint-Louis puis au lycée Les Fontenelles. J’ai habité à Maison Rouge, le quartier du lycée, puis rue Massacre, et je vis aujourd’hui à Pichou. J’aime tous les coins de Louviers. »</p>'),
            ('Mes habitudes',
             '<p>« J’ai toutes mes habitudes à Louviers. Je me fais coiffer chez Patrick Armand, je m’habille chez Bonobo, je prends un café chez Couleur Kfé. Le midi, je déjeune à la <a class="link-u" href="../portraits/maison-barbe.html">Maison Barbé</a>, ou en terrasse à la Brasserie de la Halle ou au Parvis. Le samedi, je vais au marché, et je joue au tennis au Louviers Tennis Club. »</p>'
             '<p>« Les commerçants sont adorables, l’équipe de Louviers Shopping aussi, comme l’équipe municipale. J’ai présidé l’association des commerçants Louviers Shopping en 2019 : une expérience très formatrice. »</p>'),
            ('Les ventes qui m’ont marqué',
             '<p>« Ma toute première vente : un appartement de charme rue Pierre-Mendès-France, juste en face de la mairie, avec ses poutres et ses beaux parquets. L’acquéreuse, très sympathique, est une figure de Louviers. »</p>'
             '<p>« Et deux ventes coup sur coup au Clos Saint-Lubin, un quartier que j’apprécie pour son calme, son charme et son côté familial. L’une d’elles concernait une famille de la région parisienne. Je les ai pris par la main pour leur faire découvrir Louviers, ses accès, ses alentours : je voulais qu’ils connaissent tout avant de faire une offre. Ils y sont toujours très heureux. »</p>'),
            ('Ce que j’aime à Louviers',
             '<p>« Les changements, les grands projets, la modernisation. J’aime les grandes villes, et je vois de façon flagrante tout ce qui est fait à Louviers pour se développer comme une grande ville, en gardant tout à portée de pas. »</p>'),
        ],
        'photo': ('portraits/maison-barbe-facade.jpg', 'Le midi, à la Maison Barbé, sur le parvis.'),
    },
}
AGENT_PAGES = set(AGENTS)

AG_CSS = '''<style>
.ag-hero{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:center}
.ag-role{font-size:18px;color:var(--text);margin:0}
.ag-facts{list-style:none;padding:0;margin:14px 0 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.ag-facts li{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:14px 16px;display:grid;gap:4px}
.ag-facts b{font-size:13px;font-weight:500;color:var(--muted)}.ag-facts span{font-family:var(--serif);font-size:20px;color:var(--navy);line-height:1.25}
.ag-photo img{width:100%;max-width:380px;aspect-ratio:1;object-fit:cover;border-radius:50%;border:4px solid var(--gold);display:block;margin-left:auto}
.ag-body{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:28px clamp(28px,4vw,56px);align-items:start}
.ag-main{display:grid;gap:30px;min-width:0}
.ag-side{display:grid;gap:16px;position:sticky;top:110px}
.ag-quote{margin:0;font-family:var(--serif);font-style:italic;font-weight:300;font-size:clamp(24px,2.6vw,34px);line-height:1.35;color:var(--navy);border-left:3px solid var(--gold);padding-left:24px}
.ag-qa{display:grid;gap:10px;max-width:40em}.ag-qa h2{font-size:clamp(22px,2vw,28px)}.ag-qa p{font-size:17px;line-height:1.7;margin:0;color:var(--text)}
.ag-fig{margin:0}.ag-fig img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:20px;display:block}.ag-fig figcaption{font-size:14px;color:var(--muted);margin-top:10px}
.ag-ventes{display:grid;grid-template-columns:1fr 1fr;gap:16px}.ag-ventes .ag-fig img{aspect-ratio:3/2}
@media(max-width:560px){.ag-ventes{grid-template-columns:1fr}}
.ag-chips{display:flex;flex-wrap:wrap;gap:8px}.ag-chips a{display:flex;gap:8px;align-items:center;border:1px solid var(--line);border-radius:999px;padding:6px 12px 6px 6px;font-size:14px;color:var(--navy);background:var(--white)}
.ag-chips i{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:12px;font-weight:600;color:var(--navy)}
.ag-team{display:flex;flex-wrap:wrap;gap:24px}.ag-team a{display:grid;justify-items:center;gap:8px;color:var(--navy);font-family:var(--serif);font-size:18px}
.ag-team img{width:96px;height:96px;border-radius:50%;object-fit:cover;border:3px solid var(--gold)}
.ag-team a[aria-current] img{border-color:var(--navy)}
@media(max-width:900px){.ag-hero,.ag-body{grid-template-columns:1fr}.ag-side{position:static}.ag-photo img{margin:0;max-width:240px}.ag-facts{grid-template-columns:1fr}}
</style>
'''


def page_agent(slug):
    A = AGENTS[slug]; r = '../'
    n, role, tel, img = next(t for t in TEAM if t[3] == slug)
    title = f'Le Louviers {A["de"]} · {A["nom"]}, CV Immobilier · louviers.immo'
    desc = f'{A["nom"]}, {role.lower()} chez CV Immobilier : son Louviers, ses quartiers, ses commerces préférés et les ventes qui l’ont marqué.'
    ld = {'@context': 'https://schema.org', '@type': 'Person', 'name': A['nom'], 'jobTitle': role,
          'image': f'{DOMAIN}assets/img/equipe/{img}.jpg', 'homeLocation': {'@type': 'Place', 'name': 'Louviers'},
          'worksFor': {'@type': 'RealEstateAgent', 'name': 'CV Immobilier', 'url': CV_SITE}}
    body = head(title, desc, f'agents/{slug}.html', r, jsonld=ld, css=AG_CSS)
    body += header(None, r, topbar=False)
    facts = ''.join(f'<li><b>{k}</b><span>{v}</span></li>' for k, v in A['facts'])
    secs = ''.join(f'<div class="ag-qa"><h2>{h}</h2>{t}</div>' for h, t in A['sections'])
    if A['photo']:
        f, cap = A['photo']
        fig = f'<figure class="ag-fig"><img src="{r}assets/img/{f}" alt="" loading="lazy"><figcaption>{cap}</figcaption></figure>'
        secs = secs.replace('</div><div class="ag-qa"><h2>Les ventes', f'</div>{fig}<div class="ag-qa"><h2>Les ventes', 1)
    if A.get('ventes'):
        g = ''.join(f'<figure class="ag-fig"><img src="{r}assets/img/{f}" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>' for f, cap in A['ventes'])
        grid = f'<div class="ag-ventes">{g}</div>'
        k = secs.index('<h2>Les ventes') if '<h2>Les ventes' in secs else secs.index('<h2>La vente')
        end = secs.index('</div>', k) + len('</div>')
        secs = secs[:end] + grid + secs[end:]
    chips = ''.join(f'<a href="{r}quartiers/{q}.html"><i style="background:{_QU[q]["c"]}">{_QU[q]["n"]}</i>{_QU[q]["nom"]}</a>' for q in A['quartiers'])
    cur = ' aria-current="page"'
    others = ''.join(
        f'<a href="{s}.html"{cur if s == slug else ""}><img src="{r}assets/img/equipe/{s}.jpg" alt="" loading="lazy"><span>{nn.split()[0]}</span></a>'
        for nn, rr, tt, s in TEAM if s in AGENT_PAGES)
    quote = f'<blockquote class="ag-quote">{A["quote"]}</blockquote>' if A['quote'] else ''
    body += f'''<main id="contenu">
<section class="page-head" style="padding-bottom:48px">
  <div class="wrap ag-hero">
    <div class="stack">
      <div class="crumbs"><a href="{r}index.html">Accueil</a> · <a href="{r}a-propos.html">L’équipe</a> · {A["nom"]}</div>
      <span class="eyebrow">Le Louviers {A["de"]}</span>
      <h1 style="margin-top:6px">{A["nom"]}</h1>
      <p class="ag-role">{role} chez CV Immobilier</p>
      <ul class="ag-facts">{facts}</ul>
    </div>
    <div class="ag-photo"><img src="{r}assets/img/equipe/{img}.jpg" alt="{A["nom"]}" width="400" height="400"></div>
  </div>
</section>
<section class="section" style="padding-top:56px"><div class="wrap ag-body">
  <div class="ag-main">
    <p class="lede" style="max-width:none">{A["lede"]}</p>
    {quote}
    {secs}
  </div>
  <aside class="ag-side">
    <div class="side-card">
      <span class="eyebrow">Ses quartiers</span>
      <p>{A["quartiers_txt"]}</p>
      <div class="ag-chips">{chips}</div>
    </div>
    <div class="side-card dark">
      <span class="eyebrow">Un projet ?</span>
      <p>Pour vendre, acheter ou faire estimer un bien à Louviers, {A["prenom"]} vous répond directement.</p>
      <a class="btn btn-gold" href="tel:+33{tel.replace(" ", "")[1:]}">{tel}</a>
      <a class="link-u" style="color:var(--cream)" href="{CV_EST}">Faire estimer un bien</a>
    </div>
  </aside>
</div></section>
<section class="section bg-sand"><div class="wrap">
  <div class="head2"><h2>Le Louviers de l’équipe</h2><p>Chacun a son quartier, ses commerces et ses habitudes.</p></div>
  <div class="ag-team">{others}</div>
  <p style="margin-top:24px"><a class="link-u" href="{r}a-propos.html">Toute l’équipe de CV Immobilier</a></p>
</div></section>
</main>
'''
    body += footer(r)
    write(f'agents/{slug}.html', body)


def page_agents():
    for s in AGENTS:
        page_agent(s)
