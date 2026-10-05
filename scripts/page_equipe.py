# -*- coding: utf-8 -*-
# Exécuté dans l'espace de noms de gen.py.
# Questionnaire interne de l'équipe : leur page « Le Louviers de… » + l'avis de quartier.
# Page non indexée et non listée. Réponses : Netlify > Forms > « equipe ».

EQ_PAGE = [
    ('p1', 'Depuis quand êtes-vous à Louviers, ou dans le coin ? Qu’est-ce qui vous y a amené ?'),
    ('p2', 'Ce que vous adorez à Louviers.'),
    ('p3', 'Votre commerce coup de cœur, et pourquoi.'),
    ('p4', 'Votre balade ou votre coin préféré.'),
    ('p5', 'Une vente ou une rencontre qui vous a marqué. Sans nom ni adresse du client : racontez l’émotion, pas le dossier.'),
    ('p6', 'Le conseil que vous donneriez à quelqu’un qui arrive à Louviers.'),
    ('p7', 'Le quartier que vous connaissez par cœur, et ce qu’on y trouve.'),
    ('p8', 'Un souvenir de Louviers d’il y a quelques années.'),
    ('p9', 'Ce que vous aimez faire quand vous ne travaillez pas, si vous voulez le partager.'),
    ('p10', 'La question que les acquéreurs vous posent tout le temps, et votre réponse.'),
]
EQ_QUART = [
    ('q1', 'En une ou deux phrases, comment présenteriez-vous ce quartier à quelqu’un qui ne le connaît pas ?'),
    ('q2', 'Qu’est-ce que vous aimez dans ce quartier ? Une ambiance, un moment, une habitude.'),
    ('q3', 'Le lieu à connaître dans le quartier (commerce, parc, chemin, vue), et pourquoi.'),
    ('q4', 'Qu’est-ce qui rend la vie pratique ici au quotidien ? (à pied, école, bus, gare, courses, stationnement)'),
    ('q5', 'Une histoire, un souvenir ou un fait d’histoire sur le quartier. Si c’est un fait historique, d’où le tenez-vous ?'),
    ('q6', 'Ce qu’il est utile de savoir avant de s’y installer (circulation, projets, rues calmes ou animées).'),
]

EQ_CSS = '''<style>
.eq-rules{margin:20px 0 0;padding-left:20px;display:grid;gap:6px;color:var(--text)}
.eq-form{gap:28px;min-width:0}
.eq-part>*{min-width:0;max-width:100%}
.eq-form input[type=file]{max-width:100%}
@media(max-width:560px){.eq-part{padding:16px}}
.eq-part{border:1px solid var(--line);border-radius:20px;padding:24px;margin:0;display:grid;gap:20px;background:var(--white);min-width:0}
.eq-part legend{font-family:var(--serif);font-size:24px;color:var(--navy);padding:0 8px;display:flex;gap:10px;align-items:center}
.eq-n{width:32px;height:32px;border-radius:50%;background:var(--gold);color:var(--navy);display:inline-grid;place-items:center;font:600 15px var(--sans)}
.eq-form textarea{width:100%;border-radius:12px;border:1px solid var(--line-strong);padding:10px 14px;font:inherit;background:var(--white)}
.eq-ph input[type=text]{margin-top:6px}
.eq-ck{display:flex;gap:10px;align-items:flex-start;font-size:15px}
.eq-ck input{margin-top:5px;accent-color:var(--navy)}
.eq-actions{display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.eq-done{display:grid;gap:12px;padding:40px 0}
</style>
'''


def _eq_ta(k, q):
    return f'<div class="field"><label for="{k}">{q}</label><textarea id="{k}" name="{k}" rows="3" maxlength="1500"></textarea></div>'


def _eq_ph(k, lab, hint):
    h = f'<p class="note">{hint}</p>' if hint else ''
    return (f'<div class="field eq-ph"><label for="{k}">{lab}</label>{h}'
            f'<input type="file" id="{k}" name="{k}" accept="image/*">'
            f'<input type="text" name="{k}_legende" aria-label="Légende de la photo" placeholder="Légende : lieu, rue" maxlength="140"></div>')


def page_equipe():
    r = '../'
    body = head('Questionnaire de l’équipe · louviers.immo', 'Questionnaire interne CV Immobilier.', 'equipe/questionnaire.html', r, noindex=True, css=EQ_CSS)
    body += header('', r, topbar=False)
    pers = ''.join(f'<option>{html.escape(t[0])}</option>' for t in TEAM)
    feats = sorted(json.load(open(os.path.join(OUT, 'data/villages.geojson'), encoding='utf-8'))['features'], key=lambda f: f['properties']['n'])
    quart = ''.join(f'<option value="{f["properties"]["slug"]}">{f["properties"]["n"]}. {html.escape(f["properties"]["nom"])}</option>' for f in feats)
    page_q = ''.join(_eq_ta(k, q) for k, q in EQ_PAGE)
    quart_q = ''.join(_eq_ta(k, q) for k, q in EQ_QUART)
    body += f'''<main id="contenu">
<section class="page-head" style="padding-bottom:32px"><div class="wrap" style="max-width:820px">
  <span class="eyebrow">Réservé à l’équipe CV Immobilier</span>
  <h1 style="margin-top:12px">Votre Louviers, <span class="it">en quelques réponses.</span></h1>
  <p class="lede" style="margin-top:16px">Ce questionnaire sert à deux choses : votre page sur louviers.immo (« Le Louviers de… ») et l’avis de l’équipe sur les quartiers. Répondez à ce qui vous parle, rien n’est obligatoire. Comptez 15 minutes.</p>
  <ul class="eq-rules">
    <li>Seulement ce que vous connaissez vous-même. Une réponse courte vaut mieux qu’une réponse inventée.</li>
    <li>Jamais de nom, d’adresse ou de détail qui permettrait de reconnaître un client.</li>
    <li>Pas de prix ni de jugement sur les habitants d’un quartier.</li>
    <li>Rien n’est publié sans votre relecture.</li>
  </ul>
</div></section>
<section class="section" style="padding-top:24px"><div class="wrap" style="max-width:820px">
<form class="lform eq-form" id="eq-form" name="equipe" method="POST" action="{r}merci.html" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="equipe">
  <p hidden><label>Ne pas remplir : <input name="bot-field"></label></p>
  <div class="field"><label for="personne">Qui êtes-vous ?</label><select id="personne" name="personne" required><option value="">Choisir</option>{pers}</select></div>

  <fieldset class="eq-part"><legend><span class="eq-n">1</span> Votre page « Le Louviers de… »</legend>
    <p class="muted">Choisissez quatre ou cinq questions parmi les dix, celles qui vous inspirent. Laissez les autres vides.</p>
    {page_q}
    {_eq_ph('photo_portrait', 'Une photo de vous', 'En extérieur à Louviers si possible. Ou laissez vide : on en fera une à l’agence.')}
    {_eq_ph('photo_lieu', 'Une photo de votre lieu préféré à Louviers', 'Prise par vous, sans visage reconnaissable.')}
  </fieldset>

  <fieldset class="eq-part"><legend><span class="eq-n">2</span> Un quartier que vous connaissez bien</legend>
    <p class="muted">Facultatif. Pour parler d’un autre quartier, renvoyez le questionnaire en remplissant seulement cette partie.</p>
    <div class="field"><label for="quartier">Le quartier</label><select id="quartier" name="quartier"><option value="">Choisir un quartier</option>{quart}</select></div>
    {quart_q}
    {_eq_ph('photo_q1', 'Photo du quartier 1', 'Une rue, une façade, un commerce, un parc, une vue.')}
    {_eq_ph('photo_q2', 'Photo du quartier 2', '')}
    {_eq_ph('photo_q3', 'Photo du quartier 3', '')}
  </fieldset>

  <fieldset class="eq-part"><legend><span class="eq-n">3</span> Votre accord</legend>
    <div class="field"><span class="lbl">Sur le site, on vous présente avec</span>
      <label class="eq-ck"><input type="radio" name="signature" value="Prénom et nom" checked> Votre prénom et votre nom</label>
      <label class="eq-ck"><input type="radio" name="signature" value="Prénom seulement"> Votre prénom seulement</label></div>
    <label class="eq-ck"><input type="checkbox" name="accord_photos" value="oui"> J’ai pris ces photos moi-même (ou j’en ai les droits) et CV Immobilier peut les publier sur louviers.immo</label>
    <label class="eq-ck"><input type="checkbox" name="accord_publication" value="oui" required> J’accepte que mes réponses soient publiées sur louviers.immo après ma relecture</label>
  </fieldset>
  <div class="eq-actions"><button class="btn btn-navy" type="submit" id="eq-send">Envoyer mes réponses</button><p class="note" id="eq-st" aria-live="polite"></p></div>
</form>
<div class="eq-done" id="eq-done" hidden>
  <h2>Merci, c’est envoyé.</h2>
  <p class="lede">Nicolas relira vos réponses et vous enverra le texte avant toute publication.</p>
  <p><a class="link-u" href="questionnaire.html">Répondre pour un autre quartier</a></p>
</div>
</div></section>
</main>
'''
    body += footer(r, ['assets/equipe.js'])
    write('equipe/questionnaire.html', body)
