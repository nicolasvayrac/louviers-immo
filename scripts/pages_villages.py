# Les 18 quartiers de Louviers (« Les villages dans la ville », découpage de la Ville)
# Exécuté dans l'espace de noms de gen.py (head, header, footer, write, OUT, CV_EST, CV_SITE, search_form…).
import statistics as _st, math
from urllib.parse import quote
from html import escape as _e

VIL = json.load(open(os.path.join(OUT, 'data/villages.geojson'), encoding='utf-8'))
VFEAT = sorted(VIL['features'], key=lambda f: f['properties']['n'])
VBY = {f['properties']['n']: f for f in VFEAT}
_MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']


def _inpoly(lat, lon, ring):
    c = False; j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]; xj, yj = ring[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi: c = not c
        j = i
    return c


def _dseg(lat, lon, ring):
    kx = math.cos(math.radians(lat)) * 111320; ky = 110574; best = 1e9
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        ax, ay = (x1 - lon) * kx, (y1 - lat) * ky; bx, by = (x2 - lon) * kx, (y2 - lat) * ky
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy or 1e-9
        t = max(0, min(1, -(ax * dx + ay * dy) / L2)); px, py = ax + t * dx, ay + t * dy
        best = min(best, math.hypot(px, py))
    return best


def village_de(lat, lon, maxd=250):
    """Numéro du quartier contenant le point ; à défaut, le plus proche à moins de maxd mètres."""
    for f in VFEAT:
        if _inpoly(lat, lon, f['geometry']['coordinates'][0]): return f['properties']['n']
    d, n = min((_dseg(lat, lon, f['geometry']['coordinates'][0]), f['properties']['n']) for f in VFEAT)
    return n if d <= maxd else None


# ---------- ventes DVF par quartier
_DVF = json.load(open(os.path.join(OUT, 'data/dvf.json'), encoding='utf-8'))
_PER = _DVF['period']
VSALES = {n: [] for n in VBY}
for _s in _DVF['sales']:
    if _s[7] != 'Louviers' or not _s[4] or not 400 <= _s[3] / _s[4] <= 6000: continue  # écarte les ventes aberrantes (lots multiples, terrains)
    _n = village_de(_s[0], _s[1])
    if _n: VSALES[_n].append(_s)


def _stats(sales):
    out = {}
    for t in ('M', 'A'):
        xs = [s for s in sales if s[5] == t]
        m2 = sorted(s[3] / s[4] for s in xs)
        d = {'n': len(xs)}
        if len(xs) >= 3:
            q = _st.quantiles(m2, n=4) if len(m2) >= 4 else [m2[0], 0, m2[-1]]
            d.update(med=_st.median(m2), moy=_st.mean(m2), q1=q[0], q3=q[2], prix_moy=_st.mean(s[3] for s in xs),
                     prix_med=_st.median(s[3] for s in xs), surf=_st.mean(s[4] for s in xs),
                     pieces=_st.median([s[6] for s in xs if s[6]] or [0]))
            for y in ('2024', '2025'):
                ys = [s[3] / s[4] for s in xs if s[2].startswith(y)]
                d['y' + y] = (_st.median(ys), len(ys)) if len(ys) >= 5 else None
        out[t] = d
    out['n'] = len(sales)
    return out


VSTATS = {n: _stats(v) for n, v in VSALES.items()}
LOUV = _stats([s for s in _DVF['sales'] if s[7] == 'Louviers' and s[4] and 400 <= s[3] / s[4] <= 6000])


def _fr(v, r=-1):
    return f'{round(v, r):,.0f}'.replace(',', ' ')


def _pm(s):
    y, m = s.split('-'); return f'{_MOIS[int(m) - 1]} {y}'


VPERIODE = f'{_pm(_PER["from"])} à {_pm(_PER["to"])}'

# ---------- commerces, équipements, portraits (OpenStreetMap + portraits publiés)
_POIS = json.load(open(os.path.join(OUT, 'data/pois.json'), encoding='utf-8'))['pois']
_CJS = open(os.path.join(OUT, 'assets/commerces.js'), encoding='utf-8').read()
_RUB = re.findall(r"\['(\w+)', '([^']+)', '[^']*', \[([^\]]*)\]\]", _CJS)
_K2R = {}
for _rid, _lab, _kinds in _RUB:
    for _k in re.findall(r"'([^']+)'", _kinds): _K2R.setdefault(_k, _rid)
_RLAB = {rid: lab for rid, lab, _ in _RUB}
_EXJS = open(os.path.join(OUT, 'data/exclusions.js'), encoding='utf-8').read()
_EXCL = set(re.findall(r'"([^"]+)"', _EXJS.split('LI_EXCLUS')[1].split(']')[0])) if 'LI_EXCLUS' in _EXJS else set()
VPOI = {n: {'shops': {}, 'ecoles': set(), 'pharma': 0, 'med': 0, 'bus': set(), 'parcs': set()} for n in VBY}
for _p in _POIS:
    _t = _p['t']; _nm = _t.get('name', '')
    if not (49.17 < _p['lat'] < 49.25 and 1.11 < _p['lon'] < 1.23): continue
    _n = village_de(_p['lat'], _p['lon'], 80)
    if not _n: continue
    V = VPOI[_n]
    if _t.get('amenity') in ('school', 'college') and _nm: V['ecoles'].add(_nm); continue
    if _t.get('highway') == 'bus_stop': V['bus'].add(_nm or _p['id']); continue
    if _t.get('leisure') == 'park' and _nm: V['parcs'].add(_nm); continue
    if _t.get('amenity') == 'pharmacy': V['pharma'] += 1
    if _t.get('amenity') in ('doctors', 'clinic'): V['med'] += 1
    _k = next((_t[k] for k in ('amenity', 'shop', 'craft') if _t.get(k) in _K2R), None)
    if _k and _nm and _nm not in _EXCL and not _t.get('office'):
        V['shops'].setdefault(_K2R[_k], set()).add(_nm)

_PJS = open(os.path.join(OUT, 'data/portraits.js'), encoding='utf-8').read().split('window.LI_PORTRAITS')[1]
VPORT = {n: [] for n in VBY}
_QTXT = {'Centre-ville': 1, 'Les Tisserands': 17}
_OSMLL = {p['id']: (p['lat'], p['lon']) for p in _POIS}
for _blk in re.findall(r'\{(.*?)\n  \}', _PJS, re.S):
    if 'listed: false' in _blk: continue
    g = lambda k: (re.search(k + r':\s*"([^"]*)"', _blk) or [None, ''])[1]
    la = re.search(r'lat:\s*([\d.]+),\s*lon:\s*([\d.]+)', _blk)
    n = None
    if la: n = village_de(float(la[1]), float(la[2]))
    elif g('osm') in _OSMLL: n = village_de(*_OSMLL[g('osm')])
    if not n: n = _QTXT.get(g('quartier'))
    if n: VPORT[n].append({'name': g('name'), 'title': g('title'), 'url': g('url'), 'photo': g('photo'), 'cat': g('category')})

# ---------- repères de vie par quartier (pour l'accueil et les cartes)
_ECH = [(49.237849, 1.186267), (49.221612, 1.179477), (49.205573, 1.179995), (49.189169, 1.170085), (49.248772, 1.176256), (49.189576, 1.233928)]  # échangeurs A154 et A13


def _km(a, b, c, d):
    return math.hypot((d - b) * math.cos(math.radians(a)) * 111.32, (c - a) * 110.574)


VVIE = {}
for _f in VFEAT:
    _n = _f['properties']['n']; _V = VPOI[_n]; _S = VSTATS[_n]; _c = _f['properties']['centre']
    VVIE[_n] = {'com': sum(len(v) for v in _V['shops'].values()), 'eco': len(_V['ecoles']), 'bus': len(_V['bus']),
                'pm': round(100 * _S['M']['n'] / _S['n']) if _S['n'] >= 5 else None,
                'ech': round(min(_km(_c[0], _c[1], a, b) for a, b in _ECH), 1)}


# ---------- textes rédigés (seulement quand ils existent : aucun texte générique inventé)
VTEXTES = {
    1: '''<div class="qa"><h2>Le rendez-vous incontournable du marché</h2>
      <p>Deux fois par semaine, le <strong style="color:var(--navy)">mercredi et le samedi matin</strong>, la place de la Halle devient le théâtre d’une effervescence gourmande. Producteurs locaux, étals colorés et senteurs du terroir s’y rassemblent en plein cœur de ville pour offrir aux Lovériens un lieu d’échange authentique et convivial.</p></div>
      <div class="market">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true"><path d="M3 9l1.5-5h15L21 9"/><path d="M3 9h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/><path d="M5 13v7h14v-7"/></svg>
        <div><strong>Marché de Louviers</strong><br>Mercredi et samedi matin · place de la Halle</div>
      </div>
      <div class="qa"><h2>Plus de 200 commerces de proximité</h2>
      <p>Le commerce local est aussi dynamique qu’éclectique : plus de 200 commerces de proximité sont installés en centre-ville pour la grande majorité, mais aussi dans les différents quartiers. Soutenue par la municipalité, Louviers Shopping, l’association des commerçants lovériens, organise de nombreux événements au fil de l’année : salon des commerçants en novembre, animations de Noël, opérations pour la fête des mères et des pères, Pâques…</p></div>
      <div class="qa"><h2>Un agenda culturel et festif tout au long de l’année</h2>
      <p>Le cœur urbain vit au rythme d’animations régulières : braderies commerçantes, rendez-vous artistiques, marchés thématiques et illuminations saisonnières.</p>
      <p style="margin-top:14px"><a class="link-u" href="https://www.ville-louviers.fr/actualite-agenda/" target="_blank" rel="noopener">L’agenda sur le site de la Ville</a></p></div>
      <div class="pull"><span class="q" aria-hidden="true">«</span><p>Le marché le mercredi et le samedi, les terrasses, les boutiques : au centre de Louviers, la voiture reste souvent au garage.</p><cite>— L’équipe CV Immobilier</cite></div>''',
}


def _cmp(v, ref):
    if not v or not ref: return ''
    p = round((v / ref - 1) * 100)
    if abs(p) < 3: return 'comme la moyenne de Louviers'
    return f'{"+" if p > 0 else "−"}{abs(p)} % par rapport à Louviers'


def _bloc_prix(t, d, lv):
    lab = {'M': 'Maisons', 'A': 'Appartements'}[t]
    if d['n'] < 3:
        txt = 'Aucune vente' if d['n'] == 0 else f'{d["n"]} vente{"s" if d["n"] > 1 else ""} seulement'
        return f'''<div class="vq-pcard"><span class="eyebrow">{lab}</span><h3>Pas assez de ventes</h3>
        <p class="muted">{txt} sur la période : trop peu pour afficher un prix fiable. Une estimation sur place reste la seule façon de situer un bien.</p></div>'''
    lo, hi = 800, 3600
    x = lambda v: max(0, min(100, (v - lo) / (hi - lo) * 100))
    evo = ''
    if d.get('y2024') and d.get('y2025'):
        a, b = d['y2024'][0], d['y2025'][0]; p = round((b / a - 1) * 100)
        evo = f'<li><span>Médiane 2024 → 2025</span><b>{_fr(a)} → {_fr(b)} €/m² ({"+" if p >= 0 else "−"}{abs(p)} %)</b></li>'
    pcs = d['pieces']; pcs = (str(int(pcs)) if pcs == int(pcs) else f'{int(pcs)} à {int(pcs) + 1}')
    return f'''<div class="vq-pcard"><span class="eyebrow">{lab} · {d["n"]} ventes</span>
      <div class="vq-big">{_fr(d["med"])} <small>€/m² médian</small></div>
      <p class="vq-cmp">{_cmp(d["med"], lv.get("med"))}</p>
      <div class="vq-bar" aria-hidden="true"><div class="vq-rng" style="left:{x(d["q1"]):.1f}%;width:{x(d["q3"]) - x(d["q1"]):.1f}%"></div><div class="vq-med" style="left:{x(d["med"]):.1f}%"></div><div class="vq-lou" style="left:{x(lv.get("med", 0)):.1f}%" title="Louviers"></div></div>
      <div class="vq-axis"><span>{_fr(lo)} €/m²</span><span>Louviers</span><span>{_fr(hi)} €/m²</span></div>
      <ul class="vq-list">
        <li><span>Moyenne au m²</span><b>{_fr(d["moy"])} €/m²</b></li>
        <li><span>La moitié des ventes entre</span><b>{_fr(d["q1"])} et {_fr(d["q3"])} €/m²</b></li>
        <li><span>Prix moyen</span><b>{_fr(d["prix_moy"], -3)} €</b></li>
        <li><span>Prix médian</span><b>{_fr(d["prix_med"], -3)} €</b></li>
        <li><span>Surface moyenne</span><b>{_fr(d["surf"], 0)} m², {pcs} pièces</b></li>
        {evo}
      </ul></div>'''


def _ventes_table(sales):
    rows = sorted(sales, key=lambda s: s[2], reverse=True)[:30]
    if not rows: return ''
    tr = ''.join(f'''<tr><td>{_pm(s[2])}</td><td>{'Maison' if s[5] == 'M' else 'Appartement'}</td><td class="num">{s[6] or '—'}</td><td class="num">{s[4]} m²</td><td class="num">{_fr(s[3], -2)} €</td><td class="num">{_fr(s[3] / s[4])} €</td></tr>''' for s in rows)
    more = f'<p class="note" style="margin-top:12px">Les 30 ventes les plus récentes sur {len(sales)}.</p>' if len(sales) > 30 else ''
    return f'''<div class="table-wrap" style="overflow-x:auto;border:1px solid var(--line);border-radius:18px;background:var(--white)"><table class="data">
      <thead><tr><th>Date</th><th>Type</th><th class="num">Pièces</th><th class="num">Surface</th><th class="num">Prix</th><th class="num">€/m²</th></tr></thead><tbody>{tr}</tbody></table></div>{more}'''


def _vie(n):
    V = VPOI[n]; shops = sorted(V['shops'].items(), key=lambda kv: -len(kv[1]))
    rubs = ''.join(f'''<div class="vq-rub"><h3>{_RLAB[rid]} <span>{len(v)}</span></h3><p>{_e(", ".join(sorted(v)[:5]))}{"…" if len(v) > 5 else ""}</p></div>''' for rid, v in shops[:6])
    ncom = sum(len(v) for v in V['shops'].values())
    eco = ', '.join(sorted(V['ecoles'])) or 'aucune recensée dans le quartier'
    return ncom, f'''<div class="vq-facts">
        <div><b>{ncom}</b><span>commerces recensés</span></div>
        <div><b>{len(V["ecoles"])}</b><span>écoles et établissements</span></div>
        <div><b>{len(V["bus"])}</b><span>arrêts de bus</span></div>
        <div><b>{V["pharma"] + V["med"]}</b><span>pharmacies et médecins</span></div>
      </div>
      <p style="margin-top:18px"><b style="color:var(--navy)">Écoles :</b> {_e(eco)}.</p>
      {f'<div class="vq-rubs">{rubs}</div>' if rubs else ''}'''


VCSS = '''<style>
.vq-hero{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,3vw,48px);align-items:stretch}
.vq-num{display:inline-grid;place-items:center;width:52px;height:52px;border-radius:50%;font:600 20px var(--sans,inherit);color:var(--navy);border:2px solid rgba(27,46,64,.25)}
.vq-map{min-height:420px;border-radius:24px;overflow:hidden;border:1px solid var(--line)}
.vq-k{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.vq-prix{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.vq-pcard{background:var(--white);border:1px solid var(--line);border-radius:22px;padding:26px 28px;display:flex;flex-direction:column;gap:8px}
.vq-pcard h3{font-size:26px}
.vq-big{font-family:var(--serif);font-size:clamp(40px,4vw,54px);color:var(--navy);line-height:1}
.vq-big small{font-family:inherit;font-size:16px;color:var(--muted)}
.vq-cmp{font-size:14px;color:var(--gold-text);font-weight:600}
.vq-bar{position:relative;height:12px;border-radius:6px;background:var(--sand);margin-top:12px}
.vq-rng{position:absolute;top:0;height:12px;border-radius:6px;background:var(--gold-light)}
.vq-med{position:absolute;top:-5px;width:4px;height:22px;margin-left:-2px;border-radius:2px;background:var(--navy)}
.vq-lou{position:absolute;top:-3px;width:2px;height:18px;margin-left:-1px;background:var(--eure);opacity:.8}
.vq-axis{display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}
.vq-list{list-style:none;margin:10px 0 0;padding:0;font-size:15px}
.vq-list li{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-top:1px solid var(--sand)}
.vq-list b{color:var(--navy);font-weight:600;text-align:right;font-variant-numeric:tabular-nums}
.vq-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.vq-facts div{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:16px 18px;display:flex;flex-direction:column}
.vq-facts b{font-family:var(--serif);font-weight:400;font-size:30px;color:var(--navy)}
.vq-facts span{font-size:13px;color:var(--muted)}
.vq-rubs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:20px}
.vq-rub{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:16px 18px}
.vq-rub h3{font-size:19px;display:flex;justify-content:space-between}
.vq-rub h3 span{font-size:14px;color:var(--gold-text)}
.vq-rub p{font-size:14px;color:var(--text);margin-top:6px;line-height:1.5}
.vq-nb{display:flex;flex-wrap:wrap;gap:10px}
.vq-nb a{display:flex;align-items:center;gap:10px;padding:8px 16px 8px 8px;border-radius:999px;background:var(--white);border:1px solid var(--line);color:var(--navy);font-weight:500}
.vq-nb i{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:13px;font-weight:600}
.vq-cta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.vq-cta a{display:flex;flex-direction:column;gap:8px;border-radius:22px;padding:24px;background:var(--navy);color:var(--on-dark)}
.vq-cta a strong{font-family:var(--serif);font-weight:400;font-size:23px;color:var(--cream)}
.vq-cta a .go{margin-top:auto;color:var(--gold);font-weight:600}
.vq-cta a.alt{background:var(--white);color:var(--text);border:1px solid var(--line)}
.vq-cta a.alt strong{color:var(--navy)}.vq-cta a.alt .go{color:var(--gold-text)}
.vq-pors{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.vq-por{display:flex;flex-direction:column;gap:6px;background:var(--navy);border-radius:20px;overflow:hidden;padding-bottom:16px;color:var(--on-dark)}
.vq-por img{width:100%;aspect-ratio:16/10;object-fit:cover}
.vq-por span,.vq-por strong{padding:0 18px}.vq-por .c{color:var(--gold);font-size:13px;margin-top:8px}
.vq-por strong{color:var(--cream);font-family:var(--serif);font-weight:400;font-size:21px}
.vq-sec{padding:clamp(44px,5vw,72px) 0}
.vq-sec h2{margin-bottom:22px}
.vq-tbl th button{all:unset;cursor:pointer}
.vl-map{height:clamp(420px,62vh,640px);border-radius:24px;overflow:hidden;border:1px solid var(--line)}
.vl-modes{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.vl-modes button{font:500 15px inherit;padding:9px 16px;border-radius:999px;border:1px solid var(--line-strong);background:var(--white);color:var(--navy);cursor:pointer}
.vl-modes button[aria-pressed=true]{background:var(--navy);color:var(--cream);border-color:var(--navy)}
.vl-leg{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--muted);margin-top:10px}
.vl-leg .g{flex:0 0 220px;height:10px;border-radius:5px;background:linear-gradient(90deg,#E8F0E9,#C9A961,#7E3B2B)}
.vl-lbl{font:600 13px/1 var(--sans,sans-serif);color:#1B2E40;background:#fff;border:2px solid #1B2E40;border-radius:50%;width:26px;height:26px;display:grid!important;place-items:center;padding:0!important;box-shadow:0 2px 6px rgba(0,0,0,.2)}
.vl-lbl:before{display:none}
.vl-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.vl-card{display:grid;grid-template-columns:40px 1fr;gap:14px;align-items:center;background:var(--white);border:1px solid var(--line);border-radius:18px;padding:14px 16px;color:var(--text);transition:border-color .2s,transform .2s}
.vl-card:hover{border-color:var(--gold);transform:translateY(-2px)}
.vl-card i{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-weight:600;color:var(--navy)}
.vl-card strong{display:block;font-family:var(--serif);font-weight:400;font-size:20px;color:var(--navy);line-height:1.15}
.vl-card span{font-size:13px;color:var(--muted)}
@media(max-width:900px){.vq-hero,.vq-prix{grid-template-columns:1fr}.vq-k,.vq-facts{grid-template-columns:repeat(2,1fr)}.vq-rubs,.vq-cta,.vq-pors,.vl-grid{grid-template-columns:1fr}.vq-map{min-height:320px}}
</style>
'''
_LEAF = '<link rel="stylesheet" href="{r}assets/vendor/leaflet/leaflet.css">\n'


def _kpi(l, v, u): return f'<div class="kpi light"><div class="l">{l}</div><div class="v">{v}</div><div class="u">{u}</div></div>'


def page_village(f):
    p = f['properties']; n = p['n']; nom = p['nom']; slug = p['slug']; r = '../'
    S = VSTATS[n]; M, A = S['M'], S['A']
    ncom, vie = _vie(n)
    title = f'{nom}, quartier de Louviers : prix, ventes, commerces · louviers.immo'
    desc = (f'Le quartier {nom} à Louviers ({n}e des 18 « villages dans la ville ») : {S["n"]} ventes réelles, prix médian au m² des maisons et des appartements, commerces, écoles et bus.')
    body = head(title, desc, f'quartiers/{slug}.html', r, css=_LEAF.format(r=r) + VCSS)
    body += header('quartiers.html', r, topbar=False)
    mm = f'{_fr(M["med"])} €' if M.get('med') else '—'; ma = f'{_fr(A["med"])} €' if A.get('med') else '—'
    part = round(100 * M['n'] / S['n']) if S['n'] else 0
    nb = ''.join(f'<a href="{VBY[v]["properties"]["slug"]}.html"><i style="background:{VBY[v]["properties"]["c"]}">{v}</i>{_e(VBY[v]["properties"]["nom"])}</a>' for v in p['voisins'])
    pors = ''.join(f'''<a class="vq-por" href="{r}{x['url']}"><img src="{r}{x['photo']}" alt="{_e(x['name'])}" loading="lazy"><span class="c">{_e(x['cat'])}</span><strong>{_e(x['name'])}</strong><span>{_e(x['title'])}</span></a>''' for x in VPORT[n] if x['photo'])
    txt = VTEXTES.get(n, '')
    lead = (f'Le {n}<sup>e</sup> des 18 quartiers de Louviers, les « villages dans la ville » définis par la Ville. '
            f'{_fr(p["surface_ha"], 0)} hectares, {S["n"]} ventes enregistrées de {VPERIODE}, {ncom} commerces recensés.')
    body += f'''<main id="contenu">
<section class="page-head" style="padding-bottom:40px"><div class="wrap vq-hero">
  <div class="stack">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · <a href="{r}quartiers.html">Quartiers</a> · {_e(nom)}</div>
    <span class="vq-num" style="background:{p['c']}">{n}</span>
    <h1 style="margin-top:4px">{_e(nom)}</h1>
    <p class="lede">{lead}</p>
    <div class="vq-k" style="grid-template-columns:repeat(2,minmax(0,1fr));margin-top:8px">
      {_kpi('Maisons', mm, 'm² médian')}{_kpi('Appartements', ma, 'm² médian')}
    </div>
    <a class="btn btn-gold plausible-event-name=Estimation+Click plausible-event-position=quartier-{slug}" style="align-self:flex-start" href="{CV_EST}">Estimer mon bien dans ce quartier</a>
  </div>
  <div class="vq-map" id="vq-map" data-n="{n}" role="img" aria-label="Carte du quartier {_e(nom)} et des ventes"></div>
</div></section>

<section class="vq-sec bg-sand"><div class="wrap">
  <div class="head2"><h2>Les prix du quartier</h2><p>Ventes réelles enregistrées par l’État (DVF), de {VPERIODE}. Le trait bleu situe la médiane de Louviers.</p></div>
  <div class="vq-prix">{_bloc_prix('M', M, LOUV['M'])}{_bloc_prix('A', A, LOUV['A'])}</div>
  <div class="vq-k" style="margin-top:16px">
    {_kpi('Ventes', S['n'], 'sur la période')}{_kpi('Maisons', f'{part} %', 'des ventes')}
    {_kpi('Louviers, maisons', f'{_fr(LOUV["M"]["med"])} €', 'm² médian, toute la ville')}{_kpi('Louviers, appartements', f'{_fr(LOUV["A"]["med"])} €', 'm² médian, toute la ville')}
  </div>
  <div class="box-sand stack" style="margin-top:20px;border-radius:22px;background:var(--white)">
    <h3 style="font-size:23px">Le prix au m² ne suffit pas</h3>
    <p class="muted">Deux maisons de la même rue peuvent avoir des prix très différents : état et travaux, étiquette énergie, terrain, garage, exposition, stationnement, qualité de la rénovation. Les ventes disent ce que le marché a payé, pas ce que vaut votre bien.</p>
    <a class="btn btn-navy plausible-event-name=Estimation+Click plausible-event-position=quartier-prix-{slug}" style="align-self:flex-start" href="{CV_EST}">Obtenir un avis de valeur</a>
  </div>
</div></section>

{f"""<section class="vq-sec"><div class="wrap"><div class="head2"><h2>Les dernières ventes</h2><p>Une ligne par vente, de la plus récente à la plus ancienne. Les ventes atypiques (plusieurs lots, prix au m² hors norme) sont écartées.</p></div>{_ventes_table(VSALES[n])}</div></section>""" if VSALES[n] else ''}

{f'<section class="vq-sec"><div class="wrap" style="max-width:860px"><article class="stack-lg">{txt}</article></div></section>' if txt else ''}
<section class="vq-sec{' bg-sand' if not VSALES[n] or txt else ''}"><div class="wrap">
  <h2>Vivre ici</h2>
  {vie}
  <p style="margin-top:20px"><a class="link-u" href="{r}adresse.html?q={quote(nom + ', Louviers')}&lat={p['centre'][0]}&lon={p['centre'][1]}">Temps à pied, à vélo et en voiture depuis une adresse du quartier</a></p>
</div></section>

{f"""<section class="vq-sec bg-sand"><div class="wrap"><div class="head2"><h2>Ils font le quartier</h2><p>Nos portraits de commerçants installés ici.</p></div><div class="vq-pors">{pors}</div></div></section>""" if pors else ''}

<section class="section" style="padding-top:0" data-biens-sec>
  <div class="wrap">
    <div class="head2"><h2>À vendre à Louviers</h2><p>Les derniers biens de notre agence dans la commune.</p></div>
    <div class="biens" data-biens data-commune="Louviers" data-max="3" data-where="quartier-{slug}"></div>
    <div class="biens-foot"><p class="note" data-biens-maj>Annonces de cvimmobilier.fr, mises à jour chaque nuit.</p><a class="link-u" href="{r}a-vendre.html?commune=Louviers">Tous les biens à Louviers</a></div>
  </div>
</section>

<section class="vq-sec"><div class="wrap stack-lg">
  <div><h2 style="font-size:clamp(24px,2.4vw,32px)">Les quartiers voisins</h2><div class="vq-nb" style="margin-top:16px">{nb}</div></div>
  <div class="vq-cta">
    <a href="{CV_SITE}" class="plausible-event-name=Biens+Quartier plausible-event-position={slug}"><span class="eyebrow">Acheter</span><strong>Vous cherchez&nbsp;ici&nbsp;?</strong><span>Nos biens à vendre à Louviers.</span><span class="go">Voir les biens</span></a>
    <a href="{CV_EST}" class="plausible-event-name=Estimation+Click plausible-event-position=quartier-cta-{slug}"><span class="eyebrow">Vendre</span><strong>Vous possédez un bien ici ?</strong><span>Un avis de valeur fondé sur les ventes du quartier.</span><span class="go">Estimer mon bien</span></a>
    <a class="alt" href="{r}commerces.html#proposer"><span class="eyebrow">Contribuer</span><strong>Une adresse à nous recommander ?</strong><span>Un commerce, un lieu, une information à corriger.</span><span class="go">Proposer une adresse</span></a>
  </div>
  <p class="note">Découpage : « Les villages dans la ville », Ville de Louviers. Limites numérisées par CV Immobilier depuis le plan de la Ville, précision de l’ordre de 20 à 40 mètres. Ventes : DVF, DGFiP, {VPERIODE}. Commerces et équipements : OpenStreetMap.</p>
</div></section>
</main>
'''
    body += footer(r, ['assets/vendor/leaflet/leaflet.js', 'assets/map.js', 'assets/villages.js', 'assets/biens.js'])
    write(f'quartiers/{slug}.html', body)


def _vie_ligne(n):
    v = VVIE[n]; it = []
    if v['com']: it.append(f"{v['com']} commerce{'s' if v['com'] > 1 else ''}")
    if v['eco']: it.append(f"{v['eco']} école{'s' if v['eco'] > 1 else ''}")
    if v['bus']: it.append(f"{v['bus']} arrêt{'s' if v['bus'] > 1 else ''} de bus")
    return ' · '.join(it) or 'Voir le quartier'


VCRIT = [  # (clé, libellé du bouton, explication, test)
    ('pied', 'Tout à pied', 'au moins 10 commerces dans le quartier', lambda v: v['com'] >= 10),
    ('maison', 'Une maison', 'quartiers où au moins 80 % des ventes sont des maisons', lambda v: (v['pm'] or 0) >= 80),
    ('ecoles', 'Près des écoles', 'au moins 2 écoles ou établissements scolaires dans le quartier', lambda v: v['eco'] >= 2),
    ('bus', 'Bien desservi', 'au moins 6 arrêts de bus dans le quartier', lambda v: v['bus'] >= 6),
    ('route', 'Accès rapide à l’A154', 'un échangeur à moins d’1 km du cœur du quartier, à vol d’oiseau', lambda v: v['ech'] <= 1.0),
]


def vl_grid(root):
    cards = ''
    for f in VFEAT:
        p = f['properties']; n = p['n']
        crit = ' '.join(k for k, _, _, t in VCRIT if t(VVIE[n]))
        cards += f'<a class="vl-card" data-n="{n}" data-crit="{crit}" href="{root}quartiers/{p["slug"]}.html"><i style="background:{p["c"]}">{n}</i><span><strong>{_e(p["nom"])}</strong><span>{_vie_ligne(n)}</span></span></a>'
    return f'<div class="vl-grid" id="vl-grid">{cards}</div>'


def vl_home(root):
    return f'''<div class="vh">
      <div class="vl-map vh-map" id="vh-map" role="img" aria-label="Carte des 18 quartiers de Louviers"></div>
      {vl_grid(root)}
    </div>'''


def page_quartiers():
    r = ''
    body = head('Les 18 quartiers de Louviers : prix, ventes, carte · louviers.immo',
                'Les 18 quartiers de Louviers, « les villages dans la ville » : carte, prix médian au m² des maisons et des appartements, nombre de ventes, et une page par quartier.',
                'quartiers.html', r, css=_LEAF.format(r=r) + VCSS)
    body += header('quartiers.html', r, topbar=False)
    rows = ''
    for f in VFEAT:
        p = f['properties']; S = VSTATS[p['n']]
        cell = lambda d: f'<td class="num" data-v="{round(d["med"])}">{_fr(d["med"])} €</td>' if d.get('med') else '<td class="num" data-v="0">—</td>'
        pm = f'<td class="num" data-v="{round(S["M"]["prix_moy"])}">{_fr(S["M"]["prix_moy"], -3)} €</td>' if S['M'].get('med') else '<td class="num" data-v="0">—</td>'
        rows += f'<tr><td data-v="{p["n"]}"><a class="link-u" href="quartiers/{p["slug"]}.html">{p["n"]}. {_e(p["nom"])}</a></td><td class="num" data-v="{S["n"]}">{S["n"]}</td>{cell(S["M"])}{cell(S["A"])}{pm}</tr>'
    pills = ''.join(f'<a class="pill" href="{adr_link(r, c)}">{c}</a>' for c in COMMUNES)
    body += f'''<main id="contenu">
<section class="page-head">
  <div class="wrap">
    <div class="crumbs"><a href="{r}index.html">Accueil</a> · Quartiers</div>
    <span class="eyebrow">Les villages dans la ville</span>
    <h1 style="margin-top:12px">Les 18 quartiers <span class="it">de Louviers.</span></h1>
    <p class="lede" style="margin-top:20px;max-width:46em">La Ville de Louviers découpe la commune en 18 quartiers, qu’elle appelle « les villages dans la ville ». Pour chacun : ses limites, ses prix réels, ses commerces et ses écoles.</p>
  </div>
</section>
<section class="section" style="padding-top:24px">
  <div class="wrap">
    <div class="vl-modes" role="group" aria-label="Couleur de la carte">
      <button type="button" data-mode="q" aria-pressed="true">Quartiers</button>
      <button type="button" data-mode="M" aria-pressed="false">Prix des maisons</button>
      <button type="button" data-mode="A" aria-pressed="false">Prix des appartements</button>
    </div>
    <div class="vl-map" id="vl-map" role="img" aria-label="Carte des 18 quartiers de Louviers"></div>
    <div class="vl-leg" id="vl-leg" hidden><span id="vl-lo"></span><span class="g"></span><span id="vl-hi"></span><span>· médiane au m², quartiers d’au moins 3 ventes</span></div>
  </div>
</section>
<section class="section bg-sand" style="padding-top:56px">
  <div class="wrap">
    <div class="head2"><h2>Une page par quartier</h2><p>Prix détaillés, dernières ventes, commerces, écoles, quartiers voisins.</p></div>
    {vl_grid(r)}
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="head2"><h2>Les 18 quartiers côte à côte</h2><p>Ventes réelles de {VPERIODE}. Cliquez un titre de colonne pour trier.</p></div>
    <div style="overflow-x:auto;border:1px solid var(--line);border-radius:18px;background:var(--white)">
      <table class="data vq-tbl" id="vl-tbl"><thead><tr><th><button type="button" data-c="0">Quartier</button></th><th class="num"><button type="button" data-c="1">Ventes</button></th><th class="num"><button type="button" data-c="2">Maisons €/m²</button></th><th class="num"><button type="button" data-c="3">Appart. €/m²</button></th><th class="num"><button type="button" data-c="4">Prix moyen maison</button></th></tr></thead>
      <tbody>{rows}</tbody>
      <tfoot><tr><td><b>Louviers</b></td><td class="num"><b>{LOUV['n']}</b></td><td class="num"><b>{_fr(LOUV['M']['med'])} €</b></td><td class="num"><b>{_fr(LOUV['A']['med'])} €</b></td><td class="num"><b>{_fr(LOUV['M']['prix_moy'], -3)} €</b></td></tr></tfoot></table>
    </div>
    <p class="note" style="margin-top:12px">Médianes au m², calculées dès 3 ventes. Quand un quartier compte peu de ventes, le chiffre bouge beaucoup d’une année à l’autre : regardez aussi le nombre de ventes. Découpage : Ville de Louviers, numérisé par CV Immobilier (précision de l’ordre de 20 à 40 m).</p>
  </div>
</section>
<section class="section bg-sand">
  <div class="wrap split">
    <div class="a stack">
      <span class="eyebrow">Une rue en particulier ?</span>
      <h2>Testez <span class="it">une adresse.</span></h2>
      <p class="lede">Le quartier, les commerces, les écoles, les temps de trajet et les ventes autour.</p>
      <a class="link-u" href="{r}comparer.html">Ou comparez deux adresses</a>
    </div>
    <div class="b">{search_form('adresse-quartiers', chips=False)}</div>
  </div>
  <div class="wrap"><div class="communes"><span>Et autour de Louviers :</span>{pills}</div></div>
</section>
</main>
'''
    body += footer(r, ['assets/vendor/leaflet/leaflet.js', 'assets/map.js', 'assets/villages.js'])
    write('quartiers.html', body)


def page_villages():
    for f in VFEAT: page_village(f)
    # données pour la carte (limites + chiffres)
    out = {'type': 'FeatureCollection', 'periode': VPERIODE, 'louviers': {'M': round(LOUV['M']['med']), 'A': round(LOUV['A']['med'])}, 'features': []}
    for f in VFEAT:
        p = dict(f['properties']); S = VSTATS[p['n']]
        p['s'] = {'n': S['n'], 'M': [round(S['M']['med']) if S['M'].get('med') else None, S['M']['n']],
                  'A': [round(S['A']['med']) if S['A'].get('med') else None, S['A']['n']],
                  'pm': round(S['M']['prix_moy'], -3) if S['M'].get('med') else None}
        p['v'] = VVIE[p['n']]; p['crit'] = [k for k, _, _, t in VCRIT if t(VVIE[p['n']])]
        out['features'].append({'type': 'Feature', 'properties': p, 'geometry': f['geometry']})
    with open(os.path.join(OUT, 'data/villages.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(',', ':'))
