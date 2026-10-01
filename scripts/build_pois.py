#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Télécharge depuis OpenStreetMap (API Overpass) les commerces, écoles, arrêts de bus,
gares, équipements… de Louviers et des communes voisines, et les enregistre dans
data/pois.json. Le site lit ce fichier en priorité : plus rapide et plus fiable
qu'une interrogation en direct à chaque visite.

Lancé automatiquement chaque semaine par GitHub Actions (.github/workflows/donnees.yml).
Peut aussi être lancé à la main :  python3 scripts/build_pois.py
"""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'data', 'pois.json')

COMMUNES = {
    '27375': 'Louviers', '27598': 'Saint-Pierre-du-Vauvray', '27528': 'Le Vaudreuil', '27701': 'Val-de-Reuil',
    '27351': 'Incarville', '27469': "Pont-de-l'Arche", '27003': 'Acquigny', '27015': 'Andé',
    '27537': 'Saint-Étienne-du-Vauvray', '27456': 'Pinterville',
}
# Zone couverte (sud, ouest, nord, est) : Louviers et l'agglomération, avec une marge
BBOX = (49.10, 1.02, 49.37, 1.36)

ENDPOINTS = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
]
KEEP = ['name', 'shop', 'amenity', 'craft', 'leisure', 'highway', 'railway', 'station', 'ref', 'route_ref',
        'isced:level', 'addr:housenumber', 'addr:street', 'website', 'contact:website', 'phone', 'contact:phone', 'office']


class OverpassError(Exception):
    pass


def overpass(q, tries=2):
    data = urllib.parse.urlencode({'data': q}).encode()
    last = None
    for url in ENDPOINTS:
        for attempt in range(tries):
            try:
                req = urllib.request.Request(url, data=data, headers={'User-Agent': 'louviers.immo/1.0 (contact@cvimmobilier.fr)'})
                with urllib.request.urlopen(req, timeout=180) as r:
                    return json.loads(r.read().decode('utf-8'))
            except Exception as e:  # noqa: BLE001
                last = e
                print(f'  {url} : {e} — nouvel essai', flush=True)
                time.sleep(15)
    raise OverpassError(str(last))


def main():
    s, w, n, e = BBOX
    bb = f'{s},{w},{n},{e}'
    q = f'''[out:json][timeout:170];(
      nwr({bb})[shop][name][shop!~"^(vacant|estate_agent)$"];
      nwr({bb})[amenity~"^(pharmacy|restaurant|cafe|bar|pub|fast_food|food_court|ice_cream|bank|post_office|doctors|dentist|clinic|library|marketplace|townhall|school|kindergarten|college)$"];
      nwr({bb})[craft][name];
      nwr({bb})[leisure~"^(park|playground|sports_centre|swimming_pool|pitch)$"][name];
      node({bb})[highway=bus_stop];
      node({bb})[railway~"^(station|halt)$"][station!~"subway|light_rail"];
      node({bb})[highway=motorway_junction];
    );out center tags;'''
    print('Téléchargement des lieux…', flush=True)
    try:
        j = overpass(q, tries=3)
    except OverpassError as e:
        raise SystemExit(f'Overpass indisponible, fichier inchangé : {e}')
    pois, index = [], {}
    for el in j.get('elements', []):
        la = el.get('lat', (el.get('center') or {}).get('lat'))
        lo = el.get('lon', (el.get('center') or {}).get('lon'))
        if la is None:
            continue
        t = {k: v for k, v in (el.get('tags') or {}).items() if k in KEEP}
        pid = f"{el['type']}/{el['id']}"
        index[pid] = len(pois)
        pois.append({'id': pid, 'lat': round(la, 6), 'lon': round(lo, 6), 't': t})
    print(f'{len(pois)} lieux.', flush=True)

    # Commune de chaque lieu (pour l'annuaire). Une commune qui ne répond pas est sautée :
    # le site interrogera alors OpenStreetMap en direct pour elle.
    ok = []
    for insee, name in COMMUNES.items():
        time.sleep(8)
        qa = (f'[out:json][timeout:90];area["ref:INSEE"="{insee}"]["boundary"="administrative"]->.a;('
              'nwr(area.a)[shop][name];'
              'nwr(area.a)[amenity~"^(restaurant|fast_food|food_court|cafe|bar|pub|ice_cream|pharmacy|bank|post_office)$"][name];'
              'nwr(area.a)[craft][name];);out ids;')
        try:
            ja = overpass(qa)
        except OverpassError as e:
            print(f'  {name} : sautée ({e})', flush=True)
            continue
        c = 0
        for el in ja.get('elements', []):
            i = index.get(f"{el['type']}/{el['id']}")
            if i is not None:
                pois[i]['c'] = insee
                c += 1
        ok.append(name)
        print(f'  {name} : {c} commerces', flush=True)
    print(f'Communes traitées : {len(ok)}/{len(COMMUNES)}', flush=True)

    out = {'generated': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'bbox': BBOX, 'communes': COMMUNES,
           'licence': 'Données © contributeurs OpenStreetMap, ODbL', 'pois': pois}
    if len(pois) < 200:
        raise SystemExit('Trop peu de lieux : fichier non remplacé par sécurité.')
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print('Écrit', OUT, flush=True)


if __name__ == '__main__':
    main()
