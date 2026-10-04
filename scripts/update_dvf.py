#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mise à jour automatique des prix (DVF) pour louviers.immo.

Télécharge les fichiers DVF géolocalisés de l'Eure pour l'année en cours et les
cinq précédentes (DVF garde 5 ans d'historique ; les années absentes sont ignorées), puis reconstruit data/dvf.json avec scripts/build_dvf.py.
Le fichier n'est remplacé que si la nouvelle publication apporte des ventes plus
récentes (DVF est mis à jour en avril et en octobre).

Lancé chaque mois par GitHub Actions (.github/workflows/dvf.yml).
À la main :  python3 scripts/update_dvf.py
"""
import json, os, subprocess, sys, tempfile, urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'dvf.json')
URL = os.environ.get('DVF_URL', 'https://files.data.gouv.fr/geo-dvf/latest/csv/{y}/departements/27.csv.gz')


def fetch(year, folder):
    path = os.path.join(folder, f'27-{year}.csv.gz')
    req = urllib.request.Request(URL.format(y=year), headers={'User-Agent': 'louviers.immo/1.0 (contact@cvimmobilier.fr)'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r, open(path, 'wb') as f:
            f.write(r.read())
    except Exception as e:  # noqa: BLE001
        print(f'  {year} : non disponible ({e})', flush=True)
        return None
    print(f'  {year} : {os.path.getsize(path) // 1024} Ko', flush=True)
    return path


def period_to(path):
    try:
        with open(path, encoding='utf-8') as f:
            return (json.load(f).get('period') or {}).get('to') or ''
    except Exception:  # noqa: BLE001
        return ''


def main():
    today = date.today()
    years = list(range(today.year - 5, today.year + 1))
    with tempfile.TemporaryDirectory() as tmp:
        print('Téléchargement des fichiers DVF de l’Eure…', flush=True)
        files = [p for p in (fetch(y, tmp) for y in years) if p]
        if len(files) < 2:
            sys.exit('Moins de deux années disponibles : fichier inchangé.')
        new = os.path.join(tmp, 'dvf.json')
        subprocess.run([sys.executable, os.path.join(HERE, 'build_dvf.py'), *files, '--out', new], check=True)
        old_to, new_to = period_to(OUT), period_to(new)
        print(f'Période actuelle jusqu’à {old_to or "?"}, nouvelle jusqu’à {new_to or "?"}', flush=True)
        def count(p):
            try:
                with open(p, encoding='utf-8') as f:
                    return len(json.load(f).get('sales') or [])
            except Exception:  # noqa: BLE001
                return 0
        n_old, n_new = count(OUT), count(new)
        if n_old and n_new < n_old * 0.5:
            sys.exit(f'Seulement {n_new} ventes contre {n_old} aujourd’hui : fichier inchangé par sécurité.')
        n_old_y = len({s[2][:4] for s in (json.load(open(OUT, encoding='utf-8')).get('sales') or [])}) if os.path.exists(OUT) else 0
        n_new_y = len({s[2][:4] for s in (json.load(open(new, encoding='utf-8')).get('sales') or [])})
        if new_to and (new_to > old_to or n_new_y > n_old_y):
            os.replace(new, OUT)
            print('data/dvf.json mis à jour.', flush=True)
        else:
            print('Pas de ventes plus récentes : fichier inchangé.', flush=True)


if __name__ == '__main__':
    main()
