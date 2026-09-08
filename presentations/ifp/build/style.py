#!/usr/bin/env python3
"""Apply one unified design system across the 88 merged slides.

Content is never added or removed -- only geometry offset (4:3 -> 16:9 recentre),
colour, typography, background and table chrome are rewritten.
"""
import os, re, glob
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, 'merged')

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'p': P, 'a': A, 'r': R}
Q = lambda t: '{%s}%s' % (NS[t.split(':')[0]], t.split(':')[1])

EMU = 914400
DX = (12192000 - 9144000) // 2          # recentre the old 4:3 content on 16:9
SW, SH = 12192000, 6858000

# ---------------------------------------------------------------- palette
NAVY = '10263F'      # primary / headings
INK = '1F2C3A'       # body text, diagram strokes
AMBER = 'C8871B'     # accent (fills, rules)
AMBER_TX = '9A6510'  # accent as text: passes contrast on white
RED = 'B3261E'
SURF = 'EDF1F5'      # light panel
TINT = 'C9D6E4'      # instrument-face / diagram panel
AMBER_TINT = 'F4E4C6'
WHITE = 'FFFFFF'
AMBER_LT = 'E8B04B'  # accent on dark
RED_LT = 'F08C82'
NAVY_LT = '1C3A5E'   # panel on dark
RULE = 'C8D3DF'

SYMBOL_FONTS = {'wingdings', 'wingdings 2', 'wingdings 3', 'webdings',
                'monotype sorts', 'symbol', 'zapfdingbats', 'marlett'}
HEAD_FONT = 'Cambria'
BODY_FONT = 'Calibri'
FONT_TAGS = ('a:latin', 'a:ea', 'a:cs')     # schema order

# ------------------------------------------------- slides that go dark (1-based)
#   module openers, pure-title slides and the closing "any questions?" slides
DARK = {1, 16, 35, 36, 41, 62, 63, 75, 88}
# the two source slides that were completely empty become the module openers their
# module never had, titled with the wording that module already uses elsewhere
EMPTY_DIVIDERS = {41: 'HOLDING PROCEDURE', 63: 'TERMINAL APPROACH PLATES (TAPs)'}


# ---------------------------------------------------------------- colour utils
def _rgb(h):
    h = h.lower()
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    r, g, b = (c / 255 for c in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sat(h):
    r, g, b = (c / 255 for c in _rgb(h))
    return max(r, g, b) - min(r, g, b)


def is_red(h):
    r, g, b = _rgb(h)
    return r > 140 and g < r * 0.5 and b < r * 0.5


def is_warm(h):                      # yellow / orange / gold / brown
    r, g, b = _rgb(h)
    return r > 120 and g > 55 and b < min(r, g) * 0.72 and not is_red(h)


def map_color(h, role, dark):
    h = h.lower()
    if dark:
        if role == 'fill':
            return RED if is_red(h) else NAVY_LT
        if is_warm(h):
            return AMBER_LT
        if is_red(h):
            return RED_LT
        return WHITE
    if role == 'fill':
        if lum(h) > 0.93:
            return SURF
        if is_red(h):
            return RED
        if is_warm(h):
            return AMBER_TINT
        if lum(h) > 0.60:
            return TINT
        if sat(h) < 0.12 and lum(h) < 0.22:
            return INK
        return TINT
    if role == 'line':
        if is_red(h):
            return RED
        if is_warm(h):
            return AMBER
        if lum(h) > 0.72:
            return NAVY
        if sat(h) < 0.15:
            return INK
        return NAVY
    if is_warm(h):
        return AMBER_TX
    if is_red(h):
        return RED
    if lum(h) > 0.62:
        return NAVY
    if sat(h) < 0.12 and lum(h) < 0.35:
        return INK
    return NAVY


# ---------------------------------------------------------------- xml helpers
def solid(color):
    f = etree.Element(Q('a:solidFill'))
    etree.SubElement(f, Q('a:srgbClr')).set('val', color)
    return f


def set_font(pr, face):
    for tag in FONT_TAGS:
        node = pr.find(Q(tag))
        cur = (node.get('typeface') or '').lower() if node is not None else ''
        if cur in SYMBOL_FONTS:
            continue
        if node is None:
            node = etree.SubElement(pr, Q(tag))
        node.set('typeface', face)


def set_color(pr, color):
    for e in pr.findall(Q('a:solidFill')):
        pr.remove(e)
    for e in pr.findall(Q('a:ln')):
        pr.remove(e)
    pr.insert(0, solid(color))


def all_rpr(node):
    out = []
    for tag in ('a:rPr', 'a:defRPr', 'a:endParaRPr'):
        out += list(node.iter(Q(tag)))
    return out


def role_of(clr):
    node = clr
    while node is not None:
        tag = etree.QName(node).localname
        if tag in ('rPr', 'defRPr', 'endParaRPr', 'buClr'):
            return 'text'
        if tag in ('ln', 'lnL', 'lnR', 'lnT', 'lnB', 'lnTlToBr', 'lnBlToTr'):
            return 'line'
        if tag in ('spPr', 'grpSpPr', 'tcPr', 'bgPr', 'bg', 'tblPr'):
            return 'fill'
        node = node.getparent()
    return 'text'


def sp_text(sp):
    return ''.join(t.text or '' for t in sp.iter(Q('a:t'))).strip()


def xfrm_of(ch):
    tag = etree.QName(ch).localname
    if tag == 'graphicFrame':
        return ch.find(Q('p:xfrm'))
    if tag == 'grpSp':
        g = ch.find(Q('p:grpSpPr'))
        return g.find(Q('a:xfrm')) if g is not None else None
    sp = ch.find(Q('p:spPr'))
    return sp.find(Q('a:xfrm')) if sp is not None else None


def tree_of(sld):
    return sld.find(Q('p:cSld')).find(Q('p:spTree'))


# ---------------------------------------------------------------- transforms
def shift(sld):
    for ch in tree_of(sld):
        if etree.QName(ch).localname in ('nvGrpSpPr', 'grpSpPr'):
            continue
        xf = xfrm_of(ch)
        if xf is None:
            continue
        off = xf.find(Q('a:off'))
        if off is not None:
            off.set('x', str(int(off.get('x', 0)) + DX))


def recolor(sld, dark):
    for clr in sld.iter(Q('a:srgbClr')):
        v = clr.get('val')
        if v and len(v) == 6:
            clr.set('val', map_color(v, role_of(clr), dark))
    for clr in list(sld.iter(Q('a:schemeClr'))):
        role = role_of(clr)
        new = etree.Element(Q('a:srgbClr'))
        new.set('val', (WHITE if dark else INK) if role == 'text'
                else (NAVY_LT if dark else SURF))
        clr.getparent().replace(clr, new)


def flatten_fills(sld, dark):
    """Legacy 90s gradient and pattern shape fills read as smudges. Collapse each
    to the flat colour its stops already map to."""
    for spPr in list(sld.iter(Q('p:spPr'))) + list(sld.iter(Q('a:tcPr'))):
        for tag in ('a:gradFill', 'a:pattFill'):
            for e in spPr.findall(Q(tag)):
                stops = [s.get('val') for s in e.iter(Q('a:srgbClr')) if s.get('val')]
                col = (NAVY_LT if dark else SURF)
                if stops:
                    col = NAVY_LT if dark else max(stops, key=lum)
                idx = list(spPr).index(e)
                spPr.remove(e)
                spPr.insert(idx, solid(col))


def set_bg(sld, dark):
    csld = sld.find(Q('p:cSld'))
    for old in csld.findall(Q('p:bg')):
        csld.remove(old)
    bg = etree.Element(Q('p:bg'))
    pr = etree.SubElement(bg, Q('p:bgPr'))
    if dark:
        gf = etree.SubElement(pr, Q('a:gradFill'))
        gf.set('rotWithShape', '0')
        lst = etree.SubElement(gf, Q('a:gsLst'))
        for pos, col in (('0', '15355A'), ('100000', '091626')):
            gs = etree.SubElement(lst, Q('a:gs'))
            gs.set('pos', pos)
            etree.SubElement(gs, Q('a:srgbClr')).set('val', col)
        lin = etree.SubElement(gf, Q('a:lin'))
        lin.set('ang', '5400000'); lin.set('scaled', '0')
    else:
        pr.append(solid(WHITE))
    etree.SubElement(pr, Q('a:effectLst'))
    csld.insert(0, bg)


def style_text(sld, dark, title_sp):
    body_col = WHITE if dark else INK
    head_col = WHITE if dark else NAVY

    # legacy WordArt: texture-filled, arched, shadowed text -> plain type
    for sp in sld.iter(Q('p:sp')):
        cnv = sp.find(Q('p:nvSpPr') + '/' + Q('p:cNvPr'))
        name = (cnv.get('name') or '') if cnv is not None else ''
        tx = sp.find(Q('p:txBody'))
        if tx is None:
            continue
        bp = tx.find(Q('a:bodyPr'))
        warped = bp is not None and bp.find(Q('a:prstTxWarp')) is not None
        if not (warped or name.lower().startswith('wordart')):
            continue
        if bp is not None:
            for e in bp.findall(Q('a:prstTxWarp')):
                bp.remove(e)
        spPr = sp.find(Q('p:spPr'))
        ext = None
        if spPr is not None:
            xf = spPr.find(Q('a:xfrm'))
            if xf is not None:
                xf.attrib.pop('rot', None)
                ext = xf.find(Q('a:ext'))
            for e in spPr.findall(Q('a:effectLst')):
                spPr.remove(e)
        txt = sp_text(sp)
        if ext is not None and txt:
            w_pt = int(ext.get('cx', 0)) / EMU * 72.0
            h_pt = int(ext.get('cy', 0)) / EMU * 72.0
            fit = min(w_pt / (0.58 * max(len(txt), 1)), h_pt * 0.62)
            size = int(max(1600, min(4000, fit * 100)) // 100 * 100)
            for pr in all_rpr(sp):
                pr.set('sz', str(size))

    for pr in all_rpr(sld):
        pr.attrib.pop('u', None)
        for bad in ('a:effectLst', 'a:ln', 'a:highlight'):
            for e in pr.findall(Q(bad)):
                pr.remove(e)
        # texture / gradient text fills carry no meaning -- flatten them
        fancy = [e for tag in ('a:blipFill', 'a:gradFill', 'a:pattFill')
                 for e in pr.findall(Q(tag))]
        if fancy:
            for e in fancy:
                pr.remove(e)
            pr.insert(0, solid(head_col))
        owner = pr
        while owner is not None and etree.QName(owner).localname != 'sp':
            owner = owner.getparent()
        set_font(pr, HEAD_FONT if owner is title_sp and owner is not None else BODY_FONT)

    for p in sld.iter(Q('a:p')):
        txt = ''.join(t.text or '' for t in p.iter(Q('a:t')))
        owner_sp = p
        while owner_sp is not None and etree.QName(owner_sp).localname != 'sp':
            owner_sp = owner_sp.getparent()
        shape_len = len(sp_text(owner_sp)) if owner_sp is not None else len(txt)
        narrow = False
        if owner_sp is not None:
            xf = xfrm_of(owner_sp)
            ext = xf.find(Q('a:ext')) if xf is not None else None
            narrow = ext is not None and int(ext.get('cx', 0)) < 2.0 * EMU
        ppr = p.find(Q('a:pPr'))
        if ppr is not None:
            algn = ppr.get('algn')
            if algn == 'just' or (algn == 'r' and not narrow) \
                    or (algn == 'ctr' and shape_len > 80):
                ppr.set('algn', 'l')
        # accents belong to labels and headings; prose always gets the body colour
        in_table = any(etree.QName(a).localname == 'tbl' for a in p.iterancestors())
        if shape_len > 60 and owner_sp is not title_sp and not in_table:
            for r in p.findall(Q('a:r')):
                tnode = r.find(Q('a:t'))
                rt = (tnode.text or '') if tnode is not None else ''
                rpr = r.find(Q('a:rPr'))
                if rpr is None:
                    continue
                cur = rpr.find(Q('a:solidFill') + '/' + Q('a:srgbClr'))
                val = cur.get('val') if cur is not None else None
                accent = val in (RED, AMBER, AMBER_TX, RED_LT, AMBER_LT)
                if accent and len(rt.strip()) <= 25 and len(txt.strip()) > 45:
                    continue          # inline emphasis inside a paragraph stays
                set_color(rpr, body_col)

    # the source was authored in an RTL locale: leftover rtl flags shunt trailing
    # punctuation to the wrong end of these English lines
    for node in list(sld.iter(Q('a:pPr'))) + all_rpr(sld):
        node.attrib.pop('rtl', None)
    for e in list(sld.iter(Q('a:rtl'))):
        e.getparent().remove(e)

    # bullets: one glyph everywhere, and never in a symbol charset
    for bf in sld.iter(Q('a:buFont')):
        bf.set('typeface', 'Arial')
        bf.attrib.pop('charset', None)
        bf.attrib.pop('pitchFamily', None)
    for bc in sld.iter(Q('a:buChar')):
        bc.set('char', '•')
        ppr = bc.getparent()
        if ppr.find(Q('a:buFont')) is None:
            bf = etree.Element(Q('a:buFont'))
            bf.set('typeface', 'Arial')
            ppr.insert(list(ppr).index(bc), bf)

    # a long line set to never wrap is laid out around the shape centre by some
    # renderers, which walks it over its neighbour -- give it a real box instead
    for sp in sld.iter(Q('p:sp')):
        tx = sp.find(Q('p:txBody'))
        spPr = sp.find(Q('p:spPr'))
        if tx is None or spPr is None:
            continue
        bp = tx.find(Q('a:bodyPr'))
        if bp is None or bp.get('wrap') != 'none':
            continue
        if len(''.join(t.text or '' for t in tx.iter(Q('a:t'))).strip()) <= 25:
            continue
        xf = spPr.find(Q('a:xfrm'))
        off = xf.find(Q('a:off')) if xf is not None else None
        ext = xf.find(Q('a:ext')) if xf is not None else None
        if off is None or ext is None:
            continue
        bp.set('wrap', 'square')
        for e in bp.findall(Q('a:spAutoFit')):
            bp.remove(e)
        if bp.find(Q('a:normAutofit')) is None:
            etree.SubElement(bp, Q('a:normAutofit'))
        room = int(12.35 * EMU) - int(off.get('x', 0))
        if room > int(ext.get('cx', 0)):
            ext.set('cx', str(room))

    # narrow diagram labels must not wrap mid-word
    for sp in sld.iter(Q('p:sp')):
        tx = sp.find(Q('p:txBody'))
        spPr = sp.find(Q('p:spPr'))
        if tx is None or spPr is None:
            continue
        xf = spPr.find(Q('a:xfrm'))
        ext = xf.find(Q('a:ext')) if xf is not None else None
        if ext is None or int(ext.get('cx', 0)) > 1.3 * EMU:
            continue
        if len(''.join(t.text or '' for t in tx.iter(Q('a:t'))).strip()) > 16:
            continue
        bp = tx.find(Q('a:bodyPr'))
        if bp is None:
            bp = etree.Element(Q('a:bodyPr'))
            tx.insert(0, bp)
        bp.set('wrap', 'none')
        bp.set('lIns', '0')
        bp.set('rIns', '0')


def pick_title(sld, dark):
    """Return (title_shape, use_big_centred_layout)."""
    tree = tree_of(sld)
    text_sps = [sp for sp in tree.findall(Q('p:sp')) if sp_text(sp)]
    heavy = any(etree.QName(c).localname in ('pic', 'graphicFrame', 'grpSp')
                for c in tree)
    ph_title = None
    for sp in text_sps:
        ph = sp.find(Q('p:nvSpPr') + '/' + Q('p:nvPr') + '/' + Q('p:ph'))
        if ph is not None and ph.get('type') in ('title', 'ctrTitle') \
                and len(sp_text(sp)) <= 90:
            ph_title = sp
            break
    if ph_title is not None:
        alone = len(text_sps) == 1 and not heavy
        return ph_title, alone
    if len(text_sps) == 1 and len(sp_text(text_sps[0])) <= 90 and not heavy:
        return text_sps[0], True
    # no title placeholder: the topmost short line set in display type is the title
    best = None
    for sp in text_sps:
        xf = xfrm_of(sp)
        off = xf.find(Q('a:off')) if xf is not None else None
        if off is None:
            continue
        y = int(off.get('y', 0))
        if y > 2.10 * EMU:
            continue
        txt = sp_text(sp)
        if not txt or len(txt) > 90 or len(txt) < 3:
            continue
        if not any(c.isalpha() for c in txt):
            continue
        sizes = [int(pr.get('sz')) for pr in all_rpr(sp) if pr.get('sz')]
        if not sizes or max(sizes) < 2000:
            continue
        if best is None or y < best[0]:
            best = (y, sp)
    if best is not None:
        others = [s for s in text_sps if s is not best[1]]
        return best[1], (not others and not heavy)
    return None, False


def content_top(sld, title_sp):
    ys = []
    for ch in tree_of(sld):
        if ch is title_sp or etree.QName(ch).localname in ('nvGrpSpPr', 'grpSpPr'):
            continue
        if etree.QName(ch).localname == 'sp' and not sp_text(ch):
            xf = xfrm_of(ch)
            if xf is not None:
                ext = xf.find(Q('a:ext'))
                # ignore hairline rules / tiny ornaments
                if ext is not None and (int(ext.get('cy', 0)) < 0.12 * EMU
                                        or int(ext.get('cx', 0)) < 0.12 * EMU):
                    continue
        xf = xfrm_of(ch)
        if xf is None:
            continue
        off = xf.find(Q('a:off'))
        if off is not None:
            ys.append(int(off.get('y', 0)))
    return min(ys) if ys else SH


def place(sp, x, y, cx, cy):
    spPr = sp.find(Q('p:spPr'))
    xf = spPr.find(Q('a:xfrm'))
    if xf is None:
        xf = etree.Element(Q('a:xfrm'))
        spPr.insert(0, xf)
    off = xf.find(Q('a:off')) if xf.find(Q('a:off')) is not None else etree.SubElement(xf, Q('a:off'))
    ext = xf.find(Q('a:ext')) if xf.find(Q('a:ext')) is not None else etree.SubElement(xf, Q('a:ext'))
    off.set('x', str(int(x))); off.set('y', str(int(y)))
    ext.set('cx', str(int(cx))); ext.set('cy', str(int(cy)))


def style_title(sp, dark, big, top_free):
    """top_free: EMU from the slide top that is clear of other content."""
    if big:
        size = 4000
        place(sp, 1.05 * EMU, 2.35 * EMU, 11.2 * EMU, 2.1 * EMU)
        anchor = 'ctr'
    elif top_free >= 1.62 * EMU:
        size = 2600
        place(sp, 0.95 * EMU, 0.38 * EMU, 11.45 * EMU, 1.16 * EMU)
        anchor = 't'
    elif top_free >= 1.20 * EMU:
        size = 2200
        place(sp, 0.95 * EMU, 0.28 * EMU, 11.4 * EMU, 0.86 * EMU)
        anchor = 't'
    else:
        size = 2000
        anchor = 't'                       # cramped slide: restyle in place
    tx = sp.find(Q('p:txBody'))
    bp = tx.find(Q('a:bodyPr'))
    if bp is None:
        bp = etree.Element(Q('a:bodyPr'))
        tx.insert(0, bp)
    for ch in list(bp):
        bp.remove(ch)
    bp.attrib.clear()
    bp.set('anchor', anchor)
    for k, v in (('lIns', '0'), ('rIns', '0'), ('tIns', '0'), ('bIns', '0'),
                 ('wrap', 'square')):
        bp.set(k, v)
    etree.SubElement(bp, Q('a:normAutofit'))

    spPr = sp.find(Q('p:spPr'))
    for tag in ('a:solidFill', 'a:gradFill', 'a:blipFill', 'a:pattFill', 'a:noFill',
                'a:ln', 'a:effectLst'):
        for e in spPr.findall(Q(tag)):
            spPr.remove(e)
    etree.SubElement(spPr, Q('a:noFill'))
    etree.SubElement(etree.SubElement(spPr, Q('a:ln')), Q('a:noFill'))

    for p in tx.iter(Q('a:p')):
        ppr = p.find(Q('a:pPr'))
        if ppr is None:
            ppr = etree.Element(Q('a:pPr'))
            p.insert(0, ppr)
        ppr.set('algn', 'l')
        ppr.attrib.pop('marL', None)
        ppr.attrib.pop('indent', None)
        for tag in ('a:buChar', 'a:buAutoNum', 'a:buFont', 'a:buClr', 'a:buSzPct',
                    'a:buNone'):
            for e in ppr.findall(Q(tag)):
                ppr.remove(e)
        etree.SubElement(ppr, Q('a:buNone'))
    for pr in all_rpr(tx):
        pr.set('sz', str(size))
        pr.set('b', '1')
        pr.attrib.pop('i', None)
        pr.attrib.pop('u', None)
        set_color(pr, WHITE if dark else NAVY)
        for tag in FONT_TAGS:
            n = pr.find(Q(tag))
            if n is None:
                n = etree.SubElement(pr, Q(tag))
            n.set('typeface', HEAD_FONT)


def style_tables(sld):
    for tbl in sld.iter(Q('a:tbl')):
        rows = tbl.findall(Q('a:tr'))
        dense = len(rows) > 2 or sum(len(r.findall(Q('a:tc'))) for r in rows) > 12
        for ri, tr in enumerate(rows):
            if dense:
                tr.set('h', '0')
            head = (ri == 0)
            for tc in tr.findall(Q('a:tc')):
                tcPr = tc.find(Q('a:tcPr'))
                if tcPr is None:
                    tcPr = etree.SubElement(tc, Q('a:tcPr'))
                for e in list(tcPr):
                    tcPr.remove(e)
                for side in ('a:lnT', 'a:lnB'):           # horizontal rules only
                    ln = etree.SubElement(tcPr, Q(side))
                    ln.set('w', '12700' if head else '6350')
                    ln.append(solid(NAVY if head else RULE))
                tcPr.append(solid(NAVY if head else (WHITE if ri % 2 else SURF)))
                for k, v in (('marL', '68580'), ('marR', '68580'),
                             ('marT', '36576'), ('marB', '36576'), ('anchor', 'ctr')):
                    tcPr.set(k, v)
                for pr in all_rpr(tc):
                    set_color(pr, WHITE if head else INK)
                    if head:
                        pr.set('b', '1')
                    set_font(pr, BODY_FONT)
                    if dense and pr.get('sz'):
                        pr.set('sz', str(max(800, int(int(pr.get('sz')) * 0.8))))


def strip_placeholders(sld):
    """The merged deck sits on one blank layout, so a <p:ph> inherits nothing --
    but renderers still re-lay-out orphan placeholders (centring titles, forcing
    autofit). Every shape already carries explicit geometry and formatting, so
    drop the placeholder tags and let what is written win."""
    for nvPr in sld.iter(Q('p:nvPr')):
        for ph in nvPr.findall(Q('p:ph')):
            nvPr.remove(ph)


def drop_empty_ole(sld):
    """Slides 41 and 63 carry nothing but an embedded, entirely blank sub-slide
    (a pink placeholder outline on a blue gradient -- no text, no data). It is
    the only thing on the slide, so the slide reads as broken. Remove that one
    empty frame so the slide can serve as its module's opener."""
    tree = tree_of(sld)
    for gf in tree.findall(Q('p:graphicFrame')):
        if gf.find('.//' + Q('p:oleObj')) is not None and \
                not ''.join(t.text or '' for t in gf.iter(Q('a:t'))).strip():
            tree.remove(gf)


NUDGE = {
    # slide 3: the definition column starts exactly where the IMC/VMC/IFR/VFR
    # label column ends, so the first letter is clipped -- give it clear air
    3: [('Instrument Meteorological', 0.32, 0.0)],
}


def apply_nudges(sld, n):
    for prefix, dx, dy in NUDGE.get(n, []):
        for sp in tree_of(sld).findall(Q('p:sp')):
            if not sp_text(sp).startswith(prefix):
                continue
            xf = xfrm_of(sp)
            off = xf.find(Q('a:off')) if xf is not None else None
            if off is not None:
                off.set('x', str(int(off.get('x', 0)) + int(dx * EMU)))
                off.set('y', str(int(off.get('y', 0)) + int(dy * EMU)))


# ---------------------------------------------------------------- new furniture
_next_id = [9000]


def textbox(tree, x, y, cx, cy, lines, size, color, bold=False, font=BODY_FONT,
            algn='l', anchor='t'):
    _next_id[0] += 1
    sp = etree.SubElement(tree, Q('p:sp'))
    nv = etree.SubElement(sp, Q('p:nvSpPr'))
    c = etree.SubElement(nv, Q('p:cNvPr'))
    c.set('id', str(_next_id[0])); c.set('name', 'design%d' % _next_id[0])
    etree.SubElement(nv, Q('p:cNvSpPr')).set('txBox', '1')
    etree.SubElement(nv, Q('p:nvPr'))
    spPr = etree.SubElement(sp, Q('p:spPr'))
    xf = etree.SubElement(spPr, Q('a:xfrm'))
    o = etree.SubElement(xf, Q('a:off')); o.set('x', str(int(x))); o.set('y', str(int(y)))
    e2 = etree.SubElement(xf, Q('a:ext')); e2.set('cx', str(int(cx))); e2.set('cy', str(int(cy)))
    g = etree.SubElement(spPr, Q('a:prstGeom')); g.set('prst', 'rect')
    etree.SubElement(g, Q('a:avLst'))
    etree.SubElement(spPr, Q('a:noFill'))
    tx = etree.SubElement(sp, Q('p:txBody'))
    bp = etree.SubElement(tx, Q('a:bodyPr'))
    for k, v in (('anchor', anchor), ('lIns', '0'), ('rIns', '0'),
                 ('tIns', '0'), ('bIns', '0'), ('wrap', 'square')):
        bp.set(k, v)
    etree.SubElement(tx, Q('a:lstStyle'))
    for line in lines:
        p = etree.SubElement(tx, Q('a:p'))
        ppr = etree.SubElement(p, Q('a:pPr')); ppr.set('algn', algn)
        etree.SubElement(ppr, Q('a:buNone'))
        r = etree.SubElement(p, Q('a:r'))
        rpr = etree.SubElement(r, Q('a:rPr'))
        rpr.set('lang', 'en-US'); rpr.set('sz', str(size))
        rpr.set('b', '1' if bold else '0')
        rpr.append(solid(color))
        for tag in FONT_TAGS:
            etree.SubElement(rpr, Q(tag)).set('typeface', font)
        etree.SubElement(r, Q('a:t')).text = line
    return sp


# ---------------------------------------------------------------- main
def main():
    files = sorted(glob.glob(os.path.join(PKG, 'ppt/slides/slide*.xml')),
                   key=lambda f: int(re.search(r'slide(\d+)', f).group(1)))
    for path in files:
        n = int(re.search(r'slide(\d+)', path).group(1))
        dark = n in DARK
        sld = etree.parse(path).getroot()

        if n in EMPTY_DIVIDERS:
            drop_empty_ole(sld)

        shift(sld)
        apply_nudges(sld, n)
        recolor(sld, dark)
        flatten_fills(sld, dark)
        set_bg(sld, dark)

        title, big = pick_title(sld, dark)
        style_text(sld, dark, title)
        if title is not None:
            style_title(title, dark, big, content_top(sld, title))
        style_tables(sld)
        strip_placeholders(sld)

        if n in EMPTY_DIVIDERS:
            textbox(tree_of(sld), 1.05 * EMU, 2.35 * EMU, 11.2 * EMU, 2.1 * EMU,
                    [EMPTY_DIVIDERS[n]], 4000, WHITE, bold=True,
                    font=HEAD_FONT, anchor='ctr')
        if n != 1:
            textbox(tree_of(sld), 11.30 * EMU, 6.90 * EMU, 1.05 * EMU, 0.30 * EMU,
                    [str(n)], 1000, '7E93A8' if dark else '9AACBE', algn='r')

        with open(path, 'wb') as fh:
            fh.write(etree.tostring(sld, xml_declaration=True,
                                    encoding='UTF-8', standalone=True))
    print('styled %d slides' % len(files))


if __name__ == '__main__':
    main()
