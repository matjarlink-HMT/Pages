# -*- coding: utf-8 -*-
"""Diff harvested eXtra classification schemas against the current lib_*.py blocks."""
import json, re, sys, os

sys.path.insert(0, '/home/user/Pages/tools/product-properties')
import lib_tech, lib_tech2, lib_home, lib_auto, lib_misc, lib_misc2, lib_ind, lib_last, lib_extra

FAM = {}
for m in (lib_tech, lib_tech2, lib_home, lib_auto, lib_misc, lib_misc2, lib_ind, lib_last, lib_extra):
    FAM.update(m.FAM)

NOISE = {'product name', 'product model', 'brand name', 'comp agreement', 'model',
         'made in', 'product type', 'style'}


def norm(s):
    s = re.sub(r'\(.*?\)', ' ', str(s)).lower().replace('&', ' and ')
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return ' '.join(s.split())


def cur_names(fam):
    return {norm(p[1]): p[1] for p in FAM.get(fam, [])}


def main():
    data = json.load(open('extra_schemas.json', encoding='utf-8'))
    only = sys.argv[1:] or None
    for fam, classes in data['schemas'].items():
        if only and fam not in only:
            continue
        have = cur_names(fam)
        # merge all classifications of this family
        merged = {}
        for cname, feats in classes.items():
            for n, d in feats.items():
                e = merged.setdefault(n, {'values': [], 'n': 0, 'cls': set()})
                e['n'] += d['n']
                e['cls'].add(cname)
                for v in d['values']:
                    if v not in e['values']:
                        e['values'].append(v)
        print(f'\n{"="*78}\n{fam.upper()}   current block: {len(FAM.get(fam, []))} props   '
              f'harvested: {len(merged)} attrs   classifications: {list(classes)}')
        missing = []
        for n, e in sorted(merged.items(), key=lambda kv: -kv[1]['n']):
            if norm(n) in NOISE:
                continue
            vals = [v for v in e['values'] if v.lower() not in
                    ('not applicable', 'n/a', 'na', '-', 'none')]
            if norm(n) in have:
                continue
            missing.append((n, e['n'], vals))
        print(f'--- MISSING from block ({len(missing)}):')
        for n, cnt, vals in missing:
            print(f'  [{cnt:3d}] {n}: {" | ".join(vals[:18])}')
    print()


if __name__ == '__main__':
    main()
