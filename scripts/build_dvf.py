#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prépare data/dvf.json pour louviers.immo à partir des fichiers DVF géolocalisés.

1. Téléchargez, pour chaque année voulue, le fichier du département de l'Eure :
     https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/27.csv.gz
     https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/27.csv.gz
   (remplacez l'année ; les fichiers .csv.gz peuvent être utilisés tels quels)

2. Lancez :
     python3 scripts/build_dvf.py 27-2024.csv.gz 27-2025.csv.gz

   Options :
     --communes "Louviers,Le Vaudreuil,..."   liste des communes à garder
     --all                                     garder toutes les communes des fichiers
     --out data/dvf.json                       fichier de sortie

Règles de nettoyage (classiques pour DVF) :
  - nature de mutation « Vente » uniquement ;
  - une seule maison OU un seul appartement par vente (dépendances acceptées :
    garage, cave, parking) ; les ventes en bloc et les locaux d'activité sont écartés ;
  - surface habitable >= 9 m², prix au m² entre 300 et 12 000 € ;
  - coordonnées géographiques présentes.
Aucune adresse n'est conservée dans le fichier produit (points GPS arrondis à 5 décimales).
"""
import argparse, csv, gzip, io, json, os, sys, unicodedata
from collections import defaultdict
from datetime import date

DEFAULT_COMMUNES = [
    'Louviers', 'Saint-Pierre-du-Vauvray', 'Le Vaudreuil', 'Val-de-Reuil', 'Incarville',
    "Pont-de-l'Arche", 'Andé', 'Acquigny', 'Pinterville', 'Saint-Étienne-du-Vauvray',
    'La Haye-Malherbe', 'Surville', 'Vironvay', 'Heudebouville', 'Porte-de-Seine',
    'Herqueville', 'Connelles', 'Léry', 'Poses', 'Les Damps', 'Criquebeuf-sur-Seine',
    'Montaure', 'Terres de Bord', 'Saint-Germain-de-Pasquier', 'Quatremare', 'Hondouville',
]


def norm(s):
    s = unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode().lower()
    return ''.join(c if c.isalnum() else ' ' for c in s).split()


def open_any(path):
    if path.endswith('.gz'):
        return io.TextIOWrapper(gzip.open(path, 'rb'), encoding='utf-8', newline='')
    return open(path, encoding='utf-8', newline='')


def fnum(x):
    try:
        return float(str(x).replace(',', '.'))
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+', help='fichiers DVF géolocalisés (.csv ou .csv.gz)')
    ap.add_argument('--communes', help='communes à garder, séparées par des virgules')
    ap.add_argument('--all', action='store_true', help='garder toutes les communes')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'dvf.json'))
    a = ap.parse_args()

    wanted = None
    if not a.all:
        lst = [c.strip() for c in a.communes.split(',')] if a.communes else DEFAULT_COMMUNES
        wanted = {' '.join(norm(c)) for c in lst if c}

    muts = defaultdict(list)
    n_rows = 0
    for path in a.files:
        with open_any(path) as f:
            for row in csv.DictReader(f):
                n_rows += 1
                if wanted is not None and ' '.join(norm(row.get('nom_commune'))) not in wanted:
                    continue
                muts[(path, row.get('id_mutation'))].append(row)

    sales, rejected = [], defaultdict(int)
    for rows in muts.values():
        r0 = rows[0]
        if (r0.get('nature_mutation') or '').strip() != 'Vente':
            rejected['pas une vente'] += 1
            continue
        types = [r.get('type_local') or '' for r in rows]
        # Une ligne par local ET par parcelle : on dédoublonne les locaux par identifiant de local si présent
        locaux = {}
        for r in rows:
            t = r.get('type_local') or ''
            if t in ('Maison', 'Appartement', 'Local industriel. commercial ou assimilé'):
                key = (t, r.get('lot1_numero'), r.get('surface_reelle_bati'), r.get('nombre_pieces_principales'))
                locaux[key] = r
        dw = [r for (t, *_), r in locaux.items() if t in ('Maison', 'Appartement')]
        if any(t.startswith('Local industriel') for t in types):
            rejected['local d’activité'] += 1
            continue
        if len(dw) != 1:
            rejected['vente en bloc ou sans logement'] += 1
            continue
        d = dw[0]
        price = fnum(r0.get('valeur_fonciere'))
        surf = fnum(d.get('surface_reelle_bati'))
        lat, lon = fnum(d.get('latitude')) or fnum(r0.get('latitude')), fnum(d.get('longitude')) or fnum(r0.get('longitude'))
        if not price or not surf or surf < 9:
            rejected['prix ou surface manquant'] += 1
            continue
        if lat is None or lon is None:
            rejected['sans coordonnées'] += 1
            continue
        pm2 = price / surf
        if pm2 < 300 or pm2 > 12000:
            rejected['prix au m² aberrant'] += 1
            continue
        ym = (r0.get('date_mutation') or '')[:7]
        rooms = int(fnum(d.get('nombre_pieces_principales')) or 0)
        sales.append([round(lat, 5), round(lon, 5), ym, int(round(price)), int(round(surf)),
                      'M' if d.get('type_local') == 'Maison' else 'A', rooms, r0.get('nom_commune')])

    sales.sort(key=lambda s: s[2])
    out = {
        'generated': date.today().strftime('%d/%m/%Y'),
        'source': 'DVF — Demandes de valeurs foncières (DGFiP), fichiers géolocalisés data.gouv.fr, Licence Ouverte',
        'period': {'from': sales[0][2], 'to': sales[-1][2]} if sales else None,
        'sales': sales,
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))

    print(f'{n_rows} lignes lues, {len(muts)} mutations retenues pour les communes choisies.')
    print(f'{len(sales)} ventes conservées → {a.out}')
    for k, v in sorted(rejected.items(), key=lambda x: -x[1]):
        print(f'  écartées ({k}) : {v}')
    by = defaultdict(int)
    for s in sales:
        by[s[7]] += 1
    for c, n in sorted(by.items(), key=lambda x: -x[1]):
        print(f'  {c} : {n}')
    if not sales:
        print('Aucune vente : vérifiez les fichiers et les noms de communes.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
