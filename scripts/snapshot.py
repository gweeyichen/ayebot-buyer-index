#!/usr/bin/env python3
"""Fetch the live Ayebot buyer index and write this month's snapshot.

Usage:  python3 scripts/snapshot.py [--url URL] [--dry-run]

Writes data/YYYY-MM.csv, data/YYYY-MM.json and copies them to data/latest.*.
Refuses to write (exit 1) if the source carries any field outside the
allow-list below, so a new or sensitive field can never be published by accident.
Standard library only.
"""
import csv, datetime, json, os, sys, urllib.request

URL = 'https://ayebot.com/data/buyer-index.json'
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# Fields the source is known to carry. Anything else = refuse.
SOURCE_TOP = {'generated', 'source_synced', 'register_unique_buyers', 'sectors', 'markets', 'cells', 'headline'}
SOURCE_HEADLINE = {'unique', 'pe', 'strategic', 'listed',
                   'hq_countries', 'japan_hq', 'overseas_pct', 'hq_identifiable'}
SOURCE_CELL = {'s1', 's1_stated', 's2', 's2_stated', 's3', 's3_stated', 's4', 's4_stated',
               'total', 'market_named', 'region_wide', 'global', 'strategic', 'pe',
               'family_office', 'other', 'japan_hq'}
# Published subset. HQ-derived fields (hq_countries, japan_hq, overseas_pct,
# hq_identifiable) are deliberately NOT published: the HQ field is unreliable.
PUB_HEADLINE = ['unique', 'pe', 'strategic', 'listed']
MARKETS = ['sg', 'my', 'id', 'th', 'vn', 'ph']


def fail(msg):
    sys.exit('REFUSED: ' + msg)


def main():
    url = URL
    if '--url' in sys.argv:
        url = sys.argv[sys.argv.index('--url') + 1]
    req = urllib.request.Request(url, headers={'User-Agent': 'ayebot-buyer-index-snapshot/1'})
    d = json.load(urllib.request.urlopen(req, timeout=30))

    extra = set(d) - SOURCE_TOP
    if extra: fail(f'unexpected top-level fields {sorted(extra)}')
    extra = set(d['headline']) - SOURCE_HEADLINE
    if extra: fail(f'unexpected headline fields {sorted(extra)}')
    for k, v in d['cells'].items():
        extra = set(v) - SOURCE_CELL
        if extra: fail(f'unexpected cell fields in {k}: {sorted(extra)}')
    missing = [f for f in PUB_HEADLINE if f not in d['headline']]
    if missing: fail(f'headline fields missing {missing}')

    sectors, markets = d['sectors'], d['markets']
    if sorted(markets) != sorted(MARKETS): fail(f'markets changed: {sorted(markets)}')
    if len(d['cells']) != len(sectors) * len(markets): fail('cell grid incomplete')
    pub = {f: d['headline'][f] for f in PUB_HEADLINE}
    for name, val in [('register_unique_buyers', d['register_unique_buyers']), *pub.items()]:
        if not isinstance(val, int) or isinstance(val, bool): fail(f'{name} is not an integer')

    snap = d['generated']
    datetime.date.fromisoformat(snap)
    month = snap[:7]

    rows = []
    for s in sectors:
        for m in MARKETS:
            n = d['cells'][f'{s}|{m}']['total']
            if not isinstance(n, int) or isinstance(n, bool): fail(f'cell {s}|{m} not an integer')
            rows.append({'snapshot_date': snap, 'sector': s, 'market': m, 'mapped_acquirers': n})

    headline = {'snapshot_date': snap, 'source': 'https://ayebot.com/data/buyer-index.json',
                'register_unique_buyers': d['register_unique_buyers'], 'headline': pub,
                'sectors': sectors, 'markets': markets}

    if '--dry-run' in sys.argv:
        print(f'OK (dry run): {month}, {len(rows)} rows, headline {pub}')
        return
    os.makedirs(DATA, exist_ok=True)
    for ext in ('csv', 'json'):
        for name in (f'{month}.{ext}', f'latest.{ext}'):
            path = os.path.join(DATA, name)
            with open(path, 'w', newline='') as f:
                if ext == 'csv':
                    w = csv.DictWriter(f, fieldnames=['snapshot_date', 'sector', 'market', 'mapped_acquirers'], lineterminator='\n')
                    w.writeheader(); w.writerows(rows)
                else:
                    json.dump(headline, f, indent=1); f.write('\n')
    print(f'wrote data/{month}.csv, data/{month}.json and data/latest.* ({len(rows)} rows)')


if __name__ == '__main__':
    main()
