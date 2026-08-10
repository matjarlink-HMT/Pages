# -*- coding: utf-8 -*-
"""Harvest server-rendered facet names + values from Ounass category pages."""
import gzip, io, json, re, sys, time, urllib.request

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/125.0 Safari/537.36')

PAGES = [
    ('apparel_women',  'https://www.ounass.ae/women/clothing'),
    ('apparel_dresses', 'https://www.ounass.ae/women/clothing/dresses'),
    ('apparel_men',    'https://www.ounass.ae/men/clothing'),
    ('footwear_women', 'https://www.ounass.ae/women/shoes'),
    ('footwear_men',   'https://www.ounass.ae/men/shoes'),
    ('bag',            'https://www.ounass.ae/women/bags'),
    ('jewellery',      'https://www.ounass.ae/women/jewellery'),
    ('watch',          'https://www.ounass.ae/women/watches'),
    ('eyewear',        'https://www.ounass.ae/women/sunglasses'),
    ('makeup',         'https://www.ounass.ae/beauty/makeup'),
    ('perfume',        'https://www.ounass.ae/beauty/fragrance'),
    ('personal_care',  'https://www.ounass.ae/beauty/skincare'),
    ('baby',           'https://www.ounass.ae/kids/baby'),
]

TAG = re.compile(r'<[^>]+>')


def fetch(url, tries=3):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': UA, 'Accept-Encoding': 'gzip',
                'Accept': 'text/html', 'Accept-Language': 'en-US,en;q=0.9'})
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read()
                enc = r.headers.get('Content-Encoding')
            if enc == 'gzip':
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            return raw.decode('utf-8', 'ignore')
        except Exception as e:
            if a == tries - 1:
                print(f'  !! {type(e).__name__} {url}', flush=True)
                return None
            time.sleep(1.5 * (a + 1))


def parse_facets(html):
    out = {}
    # each facet section: <section class="Facet..."><header>NAME</header> ... </section>
    for m in re.finditer(r'<section class="Facet[^"]*">(.*?)</section>', html, re.S):
        body = m.group(1)
        h = re.search(r'<header[^>]*>(.*?)</header>', body, re.S)
        if not h:
            continue
        name = TAG.sub('', h.group(1)).strip()
        vals = []
        for v in re.finditer(r'class="FacetLink-name"[^>]*>(.*?)</span>\s*</span>', body, re.S):
            txt = TAG.sub(' ', v.group(1))
            txt = re.sub(r'\(\s*[\d,]+\s*\)', '', txt)          # drop counts
            txt = re.sub(r'\s+', ' ', txt).strip()
            if txt and txt not in vals:
                vals.append(txt)
        if not vals:  # fallback: plain FacetLink anchors
            for v in re.finditer(r'class="[^"]*FacetLink[^"]*"[^>]*>(.*?)</a>', body, re.S):
                txt = re.sub(r'\(\s*[\d,]+\s*\)', '', TAG.sub(' ', v.group(1)))
                txt = re.sub(r'\s+', ' ', txt).strip()
                if txt and txt not in vals:
                    vals.append(txt)
        if name and vals:
            out.setdefault(name, [])
            for v in vals:
                if v not in out[name]:
                    out[name].append(v)
    return out


def main():
    res = {}
    for fam, url in PAGES:
        html = fetch(url)
        if not html:
            continue
        f = parse_facets(html)
        print(f'-- {fam:16s} {len(f):2d} facets  {url}', flush=True)
        for n, v in f.items():
            print(f'     {n}: {", ".join(v[:14])}{" ..." if len(v) > 14 else ""}', flush=True)
        res[fam] = {'url': url, 'facets': f}
        time.sleep(0.8)
    json.dump(res, open('ounass_facets.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('\nWROTE ounass_facets.json', flush=True)


if __name__ == '__main__':
    main()
