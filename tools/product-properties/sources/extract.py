# -*- coding: utf-8 -*-
"""Extract eXtra product `classifications` schema (feature names + observed values)."""
import json, re, sys


def find_classifications(html):
    """Locate the "classifications":[...] array and return it, brace-balanced."""
    key = '"classifications":'
    i = html.find(key)
    if i < 0:
        return []
    j = html.find('[', i)
    depth, k, instr, esc = 0, j, False, False
    while k < len(html):
        c = html[k]
        if instr:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c in '[{':
                depth += 1
            elif c in ']}':
                depth -= 1
                if depth == 0:
                    return json.loads(html[j:k + 1])
        k += 1
    return []


def schema_from_html(html):
    """-> (classification_name, {feature_name: [values]})"""
    out = {}
    cname = None
    for cl in find_classifications(html):
        cname = cname or cl.get('name')
        for f in cl.get('features') or []:
            name = (f.get('name') or '').strip()
            if not name:
                continue
            unit = (f.get('featureUnit') or {}).get('symbol') if isinstance(f.get('featureUnit'), dict) else None
            vals = []
            for v in f.get('featureValues') or []:
                val = v.get('value')
                if val is None:
                    continue
                val = str(val).strip()
                if val and val not in vals:
                    vals.append(val)
            out.setdefault(name, {'unit': unit, 'values': []})
            for v in vals:
                if v not in out[name]['values']:
                    out[name]['values'].append(v)
    return cname, out


if __name__ == '__main__':
    html = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
    cname, sch = schema_from_html(html)
    print('CLASSIFICATION:', cname)
    print('FEATURES:', len(sch))
    for n, d in sch.items():
        u = f" [{d['unit']}]" if d['unit'] else ''
        print(f'  - {n}{u}: {", ".join(d["values"][:6])}')
