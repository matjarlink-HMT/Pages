# -*- coding: utf-8 -*-
"""Build the expanded Product Properties / Properties + Options workbook."""
import json, re, unicodedata, difflib, collections
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import lib_core
from classify import classify
from relevance import tags_for, keep as relevant
import lib_tech, lib_tech2, lib_home, lib_auto, lib_misc, lib_misc2, lib_ind, lib_last, lib_extra

FAM = {}
for m in (lib_tech, lib_tech2, lib_home, lib_auto, lib_misc, lib_misc2, lib_ind, lib_last, lib_extra):
    FAM.update(m.FAM)

SRC = 'master.xlsx'
OUT = 'MatjarLink_Product_Properties_Expanded.xlsx'

GROUP_ORDER = [
    'Main', 'General', 'Specifications', 'Design', 'Performance', 'Display', 'Camera',
    'Memory', 'Storage', 'Audio', 'Sensors', 'Connectivity', 'Smart Features', 'Battery',
    'Power', 'Electrical', 'Engine', 'Vehicle Fitment', 'Capacity', 'Features',
    'Compatibility', 'Material', 'Dimensions', 'Fit & Size', 'Scent', 'Ingredients',
    'Nutrition', 'Health', 'Dosage', 'Animal Info', 'Course Info', 'Service Info',
    'Usage', 'Care', 'Safety', 'Environment', 'Installation', 'Certification',
    'Warranty', 'Packaging', 'Origin',
]
_GIDX = {g: i for i, g in enumerate(GROUP_ORDER)}


def gsort(group_label):
    en = group_label.split('|')[0].strip()
    # the name is part of the key so groups outside GROUP_ORDER still cluster
    # together instead of interleaving with each other
    return (_GIDX.get(en, len(GROUP_ORDER)), en)


def norm_name(s):
    s = unicodedata.normalize('NFKC', str(s)).replace('’', "'")
    s = s.lower()
    s = re.sub(r'\(.*?\)', ' ', s)          # drop parenthetical units
    s = s.replace('&', ' and ')
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' '.join(s.split())


# ------------------------------------------------------------------ read source
def read_sheet(wb, name, ncols):
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    cats = collections.OrderedDict()
    cur, grp = None, None
    for r in rows[1:]:
        if r[0]:
            cur = str(r[0]).strip()
            cats.setdefault(cur, [])
        elif r[1]:
            grp = str(r[1]).strip()
        elif r[2] and cur is not None:
            cats[cur].append((grp,) + tuple(r[2:ncols]))
    return cats


wb_src = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
PP = read_sheet(wb_src, 'Product Properties', 7)      # grp, en, ar, type, list, required
PO = read_sheet(wb_src, 'Properties + Options', 8)    # grp, en, ar, data, values, required, option

# taxonomy lookup
tax_rows = list(wb_src['Categories'].iter_rows(values_only=True))


def tnorm(s):
    s = unicodedata.normalize('NFKC', str(s)).replace('’', "'").lower().replace('&', ' and ')
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', s).split())


leaf = {}
for r in tax_rows[1:]:
    if r[0] and r[4] and 'Leaf' in str(r[4]):
        leaf.setdefault(tnorm(r[3]), (str(r[1]).strip(), str(r[2]).strip()))
leaf_keys = list(leaf)


def taxonomy_of(cat_label):
    en = cat_label.split('|')[0].strip()
    n = tnorm(en)
    if n in leaf:
        return leaf[n]
    m = difflib.get_close_matches(n, leaf_keys, n=1, cutoff=0.9)
    return leaf[m[0]] if m else (None, None)


# ------------------------------------------------------------------ merge
def po_lookup(cat, en_name):
    """Find matching row in the Properties+Options sheet for an existing property."""
    key = norm_name(en_name)
    for row in PO.get(cat, []):
        if norm_name(row[1]) == key:
            return row
    return None


def existing_props(cat):
    """Existing properties, normalised to the 9-field internal tuple.

    The source sheet contains a handful of same-named properties repeated inside one
    category (two overlapping blocks). Keep the first occurrence and fold in the
    richer option list if the duplicate carries one.
    """
    out = []
    index = {}
    for grp, en, ar, dtype, plist, req in PP.get(cat, []):
        key = norm_name(en)
        if key in index:
            i = index[key]
            prev = out[i]
            if plist and not prev[6]:          # duplicate carries the option list
                pp_list = plist if prev[3] == 'Dropdown' and not prev[4] else prev[4]
                out[i] = prev[:4] + (pp_list, 'List', plist) + prev[7:]
            continue
        index[key] = len(out)
        po = po_lookup(cat, en)
        if po:
            po_data, po_vals, po_req, po_opt = po[3], po[4], po[5], po[6]
        else:
            if dtype == 'Text':
                po_data, po_vals = 'Free', None
            elif dtype == 'Boolean':
                po_data, po_vals = 'List', 'Yes, No'
            elif dtype == 'Dropdown':
                po_data, po_vals = 'List', plist
            else:
                po_data, po_vals = 'Free', None
            po_req, po_opt = req, 'No'
        out.append((grp, en, ar, dtype, plist, po_data, po_vals,
                    req or po_req or 'No', po_opt or 'No'))
    return out


TARGETS = {  # family -> (minimum properties to aim for)
    'mobile_phone': 45, 'laptop': 40, 'television': 35, 'tablet': 32,
    'vehicle': 38, 'camera': 32, 'fridge': 32, 'washer': 30, 'ac': 30,
}

# ------------------------------------------------------------------ identity removal
# Per-product identifiers: they belong on the product record (and the Brands sheet),
# not on a category-level property definition. Matched on the normalised name.
# NOT removed: compatibility/fitment fields (Compatible Make/Model/...), component
# specs that merely contain the word "model" (Processor Model, Console Model),
# year classifications (Model Year), and business terms (Pricing Model).
DROP_NAMES = {norm_name(n) for n in [
    'Brand', 'Brand / Manufacturer', 'Vehicle Brand', 'Controller Brand', 'Engine Brand',
    'Manufacturer',
    'Model Name', 'Model Number', 'Model / Part Number',
    'Manufacturer Part Number (MPN)', 'OEM Part Number',
    'Trim / Variant',
    'Title', 'Author', 'Publisher', 'ISBN', 'Series Name',
    'Course Title', 'Provider / Instructor', 'Provider Name', 'Service Name',
    'Game Title', 'Included Game Titles',
    'Shade Name', 'Colour Code / Name',
    'Registration Number (MOH)', 'License / Registration Number',
]}

# ------------------------------------------------------------------ duplicate collapsing
# Qualifier words that do not change what a property means, so "Material" and
# "Main Material" are the same attribute. Deliberately excludes words that DO
# change the meaning (e.g. "frame", "vehicle", "handle").
QUALIFIERS = {'main', 'product', 'item', 'course', 'compliance', 'overall', 'total', 'net'}
ALIASES = {  # explicit equivalences the qualifier rule must not guess at
    'compatible vehicle make': 'compatible make',
    'compatible vehicle model': 'compatible model',
    'volume size ml': 'volume ml',
    'number of plies': 'number of ply',
    'flavour': 'flavor',
}


def dedupe_key(name):
    """Key for duplicate detection.

    Unlike norm_name this KEEPS the unit in parentheses, so "Net Weight (g)" and
    "Item Weight (kg)" stay distinct -- they are different measurements.
    """
    n = unicodedata.normalize('NFKC', str(name)).replace('’', "'").lower()
    n = n.replace('&', ' and ')
    n = ' '.join(re.sub(r'[^a-z0-9]+', ' ', n).split())
    n = ALIASES.get(n, n)
    return tuple(sorted(set(n.split()) - QUALIFIERS))


dupes = collections.Counter()
irrelevant = collections.Counter()
report = []
merged = collections.OrderedDict()

for cat in PP:
    l1, l2 = taxonomy_of(cat)
    fam = classify(cat.split('|')[0].strip(), l1, l2)
    src_props = existing_props(cat)
    tagged = [(p, True) for p in src_props]           # True = came from the source file
    seen = {norm_name(p[1]) for p in src_props}
    for p in FAM.get(fam, FAM['generic']):
        k = norm_name(p[1])
        if k in seen:
            continue
        seen.add(k)
        tagged.append((p, False))
    # drop properties whose domain this category does not have (nutrition panel on a
    # face cream, warranty on toothpaste, hair type on a nail clipper, ...)
    tags = tags_for(cat.split('|')[0].strip(), fam)
    kept_rel = []
    for p, is_src in tagged:
        if is_src or relevant(norm_name(p[1]), tags, fam):
            kept_rel.append((p, is_src))   # source rows are never gated away
        else:
            irrelevant[(fam, p[1].strip())] += 1
    tagged = kept_rel
    # drop per-product identity properties
    tagged = [(p, s) for p, s in tagged if norm_name(p[1]) not in DROP_NAMES]
    # collapse near-duplicates ("Material" vs "Main Material"), always keeping the
    # property that came from the source workbook so no original data is lost
    kept, index = [], {}
    for p, is_src in tagged:
        k = dedupe_key(p[1])
        if k not in index:
            index[k] = len(kept)
            kept.append((p, is_src))
        else:
            j = index[k]
            dupes[(kept[j][0][1], p[1])] += 1
            if is_src and not kept[j][1]:      # source wins over an added duplicate
                kept[j] = (p, is_src)
    base = [p for p, _ in kept]
    # stable ordering by group, keeping in-group order
    base = sorted(base, key=lambda p: gsort(p[0]))
    merged[cat] = base
    report.append((cat, fam, len(PP[cat]), len(base)))


# ------------------------------------------------------------------ normalisation pass
# The source workbook labels the same property differently across categories
# (Arabic wording, property group, Integer vs Decimal). Pick the value that is
# already the most widely used for that property name and apply it everywhere.
# Nothing is invented: every chosen value already exists in the data.
def _majority(counter):
    return sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0]


# The Arabic label is unified per property name. The property GROUP is deliberately
# NOT unified: the same attribute legitimately sits in different groups in different
# domains (Vegan is an Ingredient for a cream and Nutrition for a snack), so a global
# vote would drag food groupings onto cosmetics.
ar_votes = collections.defaultdict(collections.Counter)
num_votes = collections.defaultdict(collections.Counter)
for props in merged.values():
    for (grp, en, ar, dtype, plist, po_data, po_vals, req, opt) in props:
        k = norm_name(en)
        if ar:
            ar_votes[k][ar] += 1
        if dtype in ('Integer', 'Decimal'):
            num_votes[k][dtype] += 1

grp_label_votes = collections.defaultdict(collections.Counter)
for props in merged.values():
    for p_ in props:
        grp_label_votes[p_[0].split('|')[0].strip()][p_[0]] += 1
grp_label_map = {k: _majority(v) for k, v in grp_label_votes.items()}

ar_map = {k: _majority(v) for k, v in ar_votes.items()}
num_map = {k: _majority(v) for k, v in num_votes.items()}

THOUSANDS = re.compile(r'(?<=\d),(?=\d{3}(?!\d))')


def clean_list(vals):
    """Repair values whose own comma collides with the list delimiter, and trim."""
    if not vals:
        return vals
    s = THOUSANDS.sub('', str(vals))
    return ', '.join(v.strip() for v in s.split(',') if v.strip())


fixes = collections.Counter()
for cat, props in merged.items():
    out = []
    for (grp, en, ar, dtype, plist, po_data, po_vals, req, opt) in props:
        k = norm_name(en)
        canon_grp = grp_label_map.get(grp.split('|')[0].strip())
        if canon_grp and grp != canon_grp:
            grp = canon_grp; fixes['group_label_text'] += 1
        if ar_map.get(k) and ar != ar_map[k]:
            ar = ar_map[k]; fixes['arabic_label'] += 1
        if dtype in ('Integer', 'Decimal') and num_map.get(k) and dtype != num_map[k]:
            dtype = num_map[k]; fixes['numeric_type'] += 1
        np_, nv_ = clean_list(plist), clean_list(po_vals)
        if np_ != plist:
            plist = np_; fixes['value_list_repair'] += 1
        if nv_ != po_vals:
            po_vals = nv_; fixes['value_list_repair'] += 1
        # a free-text field cannot serve as a product variant option
        if po_data == 'Free' and opt == 'Yes':
            opt = 'No'; fixes['option_on_free_text'] += 1
        out.append((grp, en, ar, dtype, plist, po_data, po_vals, req, opt))
    merged[cat] = sorted(out, key=lambda p: gsort(p[0]))

# ------------------------------------------------------------------ write
HDR_FILL = PatternFill('solid', fgColor='1F3864')
CAT_FILL = PatternFill('solid', fgColor='D9E2F3')
GRP_FILL = PatternFill('solid', fgColor='F2F2F2')
HDR_FONT = Font(bold=True, color='FFFFFF', size=11)
CAT_FONT = Font(bold=True, size=11, color='1F3864')
GRP_FONT = Font(bold=True, size=10, color='404040')
THIN = Side(style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

wb = openpyxl.Workbook()

# ---- sheet 1: Product Properties
ws1 = wb.active
ws1.title = 'Product Properties'
h1 = ['Category', 'Property Group', 'Property (EN)', 'Property (AR)',
      'Data_Type', 'Item_List', 'Required']
ws1.append(h1)

# ---- sheet 2: Properties + Options
ws2 = wb.create_sheet('Properties + Options')
h2 = ['Category', 'Property Group', 'Property (EN)', 'Property (AR)',
      'Data', 'Values (Item List)', 'Required', 'Option']
ws2.append(h2)

for cat, props in merged.items():
    ws1.append([cat] + [None] * 6)
    ws2.append([cat] + [None] * 7)
    last_grp = None
    for (grp, en, ar, dtype, plist, po_data, po_vals, req, opt) in props:
        if grp != last_grp:
            ws1.append([None, grp] + [None] * 5)
            ws2.append([None, grp] + [None] * 6)
            last_grp = grp
        ws1.append([None, None, en, ar, dtype, plist, req])
        ws2.append([None, None, en, ar, po_data, po_vals, req, opt])

# ---- sheet 3: summary
ws3 = wb.create_sheet('Summary')
ws3.append(['Category', 'Property Family', 'Properties (Before)', 'Properties (After)', 'Added'])
for cat, fam, before, after in report:
    ws3.append([cat, fam, before, after, after - before])

# ---- styling
for ws, ncol in ((ws1, 7), (ws2, 8), (ws3, 5)):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = BORDER
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:{get_column_letter(ncol)}1'

for ws, ncol in ((ws1, 7), (ws2, 8)):
    for row in ws.iter_rows(min_row=2, max_col=ncol):
        if row[0].value:
            for c in row:
                c.fill = CAT_FILL
                c.font = CAT_FONT
        elif row[1].value:
            for c in row:
                c.fill = GRP_FILL
                c.font = GRP_FONT
        row[3].alignment = Alignment(horizontal='right')
        if ncol >= 6:
            row[5].alignment = Alignment(wrap_text=False, vertical='top')

for ws, widths in ((ws1, [46, 30, 34, 32, 14, 95, 11]),
                   (ws2, [46, 30, 34, 32, 10, 95, 11, 10]),
                   (ws3, [46, 22, 20, 20, 12])):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

wb.save(OUT)

# ------------------------------------------------------------------ report
counts = [r[3] for r in report]
fams = collections.Counter(r[1] for r in report)
print(f'categories        : {len(report)}')
print(f'properties before : {sum(r[2] for r in report)}')
print(f'properties after  : {sum(counts)}')
print(f'min / avg / max   : {min(counts)} / {sum(counts)/len(counts):.1f} / {max(counts)}')
print(f'below 15 props    : {sum(1 for c in counts if c < 15)}')
print('\nreview fixes applied:')
for k, v in fixes.most_common():
    print(f'  {v:6d}  {k}')
print(f'  {sum(dupes.values()):6d}  duplicate_properties_collapsed')
print(f'  {sum(irrelevant.values()):6d}  irrelevant_for_category_removed')
print('\ntop irrelevant removals (family | property):')
for (fam, prop), n in irrelevant.most_common(20):
    print(f'  {n:5d}x  {fam:16s} {prop}')
print('\ntop collapsed duplicates (kept ~ removed):')
for (a, b), n in dupes.most_common(15):
    print(f'  {n:5d}x  {a!r} ~ {b!r}')
print('\nfamily distribution:')
for f, c in fams.most_common():
    print(f'  {c:5d}  {f}')
print('\nrows: PP=%d  PO=%d' % (ws1.max_row, ws2.max_row))
json.dump([{'category': c, 'family': f, 'before': b, 'after': a} for c, f, b, a in report],
          open('report.json', 'w'), ensure_ascii=False, indent=1)
