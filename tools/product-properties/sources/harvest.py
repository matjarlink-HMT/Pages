# -*- coding: utf-8 -*-
"""Harvest eXtra classification schemas for the priority families.

Streams each product page, pulls the embedded `classifications` JSON, and
aggregates feature names + observed values per eXtra classification.
Nothing but the aggregate is kept on disk.
"""
import collections
import gzip
import io
import json
import random
import sys
import time
import urllib.request

from extract import schema_from_html

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/125.0 Safari/537.36')

# eXtra category path prefix -> our property family
BUCKETS = {
    'mobiles-tablets/mobiles/smartphone':                  'mobile_phone',
    'mobiles-tablets/tablets/ipad':                        'tablet',
    'mobiles-tablets/tablets/android':                     'tablet',
    'computer/laptops/clamshell':                          'laptop',
    'computer/laptops/gaming-laptops':                     'laptop',
    'computer/laptops/convertible':                        'laptop',
    'computer/laptops/macbook':                            'laptop',
    'electronics/television':                              'television',
    'large-appliances-/refrigerators':                     'fridge',
    'large-appliances-/washing-machines':                  'washer',
    'large-appliances-/air-conditioner':                   'ac',
    'mobiles-tablets/wearable/smart-watches':              'smartwatch',
    'mobiles-tablets/portable-audio/head-phones':          'headphones',
    'mobiles-tablets/portable-audio/earphone':             'headphones',
    'mobiles-tablets/portable-audio/tws':                  'headphones',
    'mobiles-tablets/portable-audio/speaker':              'speaker',
    'small-appliances/home-environment-care/vacuum-cleaner': 'vacuum',
    'computer/printing/printers':                          'printer',
    'mobiles-tablets/mobile-accessories/power-bank':        'powerbank',
}

PER_BUCKET = int(sys.argv[1]) if len(sys.argv) > 1 else 12
PREFIX = 'https://www.extra.com/en-sa/'


def fetch(url, tries=3):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': UA,
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Encoding': 'gzip',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read()
            if r.headers.get('Content-Encoding') == 'gzip':
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            return raw.decode('utf-8', 'ignore')
        except Exception as e:
            if a == tries - 1:
                print(f'    !! {type(e).__name__} {url[:90]}', flush=True)
                return None
            time.sleep(1.5 * (a + 1))


def main():
    urls = [u.strip() for u in open('allurls.txt', encoding='utf-8') if u.strip()]
    by_bucket = collections.defaultdict(list)
    for u in urls:
        tail = u[len(PREFIX):] if u.startswith(PREFIX) else u
        for pref in BUCKETS:
            if tail.startswith(pref + '/'):
                by_bucket[pref].append(u)
                break

    rnd = random.Random(20260810)
    # family -> classification -> feature -> {unit, values, n}
    agg = collections.defaultdict(lambda: collections.defaultdict(dict))
    counts = collections.Counter()

    for pref, fam in BUCKETS.items():
        pool = by_bucket.get(pref, [])
        if not pool:
            print(f'-- {pref}: NO URLS', flush=True)
            continue
        rnd.shuffle(pool)
        sample = pool[:PER_BUCKET]
        print(f'-- {pref} -> {fam}  ({len(pool)} available, sampling {len(sample)})', flush=True)
        for u in sample:
            html = fetch(u)
            if not html:
                continue
            cname, sch = schema_from_html(html)
            if not sch:
                continue
            cname = cname or 'UNKNOWN'
            counts[(fam, cname)] += 1
            slot = agg[fam][cname]
            for name, d in sch.items():
                e = slot.setdefault(name, {'unit': d['unit'], 'values': [], 'n': 0})
                e['n'] += 1
                if d['unit'] and not e['unit']:
                    e['unit'] = d['unit']
                for v in d['values']:
                    if v not in e['values'] and len(e['values']) < 400:
                        e['values'].append(v)
            time.sleep(0.4)

    out = {'per_bucket': PER_BUCKET,
           'sampled': {f'{f}|{c}': n for (f, c), n in counts.items()},
           'schemas': {f: {c: v for c, v in cs.items()} for f, cs in agg.items()}}
    with open('extra_schemas.json', 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print('\nWROTE extra_schemas.json', flush=True)
    for (f, c), n in counts.most_common():
        print(f'  {f:14s} {c[:52]:54s} n={n} feats={len(agg[f][c])}', flush=True)


if __name__ == '__main__':
    main()
