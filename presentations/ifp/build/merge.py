#!/usr/bin/env python3
"""Merge the six IFP decks into one package built on a single clean master/theme."""
import os, re, shutil, zipfile
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
OUT = os.path.join(HERE, 'merged')

DECKS = ['1_IFP_Intro', '2_Arcs__Radials', '3_FIX_TO_FIX', '4_holding',
         '5_taps', '6_Instrument_Approach_Procedures']

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
PR = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS = {'p': P, 'a': A, 'r': R}

RT = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'

SLIDE_W = 12192000   # 13.333in
SLIDE_H = 6858000    # 7.5in

# ---------------------------------------------------------------- theme/master

def theme_xml():
    def sc(name, val):
        return f'<a:{name}><a:srgbClr val="{val}"/></a:{name}>'
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="{A}" name="IFP">
<a:themeElements>
<a:clrScheme name="IFP">
<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
{sc('dk2','10263F')}{sc('lt2','EDF1F5')}{sc('accent1','10263F')}{sc('accent2','C8871B')}
{sc('accent3','4A5D72')}{sc('accent4','B3261E')}{sc('accent5','7A93AC')}{sc('accent6','2E5D62')}
{sc('hlink','10263F')}{sc('folHlink','4A5D72')}
</a:clrScheme>
<a:fontScheme name="IFP">
<a:majorFont><a:latin typeface="Cambria"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
</a:fontScheme>
<a:fmtScheme name="IFP">
<a:fillStyleLst>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
</a:fillStyleLst>
<a:lnStyleLst>
<a:ln w="9525" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
<a:ln w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
<a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
</a:lnStyleLst>
<a:effectStyleLst>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
</a:effectStyleLst>
<a:bgFillStyleLst>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
</a:bgFillStyleLst>
</a:fmtScheme>
</a:themeElements>
</a:theme>'''


def master_xml():
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}">
<p:cSld>
<p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
<p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>'''


def layout_xml():
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}" type="blank" preserve="1">
<p:cSld name="Blank">
<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld>
<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>'''


def rels(items):
    """items: list of (id, type, target[, mode])"""
    out = [f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{PR}">']
    for it in items:
        rid, typ, tgt = it[0], it[1], it[2]
        mode = f' TargetMode="{it[3]}"' if len(it) > 3 else ''
        out.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{tgt}"{mode}/>')
    out.append('</Relationships>')
    return ''.join(out)


# ---------------------------------------------------------------- merge

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for d in ('ppt/slides/_rels', 'ppt/slideLayouts/_rels', 'ppt/slideMasters/_rels',
              'ppt/theme', 'ppt/media', 'ppt/notesSlides/_rels', 'ppt/notesMasters/_rels',
              'ppt/_rels', '_rels'):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)

    write = lambda p, s: open(os.path.join(OUT, p), 'w', encoding='utf8').write(s)

    write('ppt/theme/theme1.xml', theme_xml())
    write('ppt/theme/theme2.xml', theme_xml().replace('name="IFP"', 'name="IFP Notes"', 1))
    write('ppt/notesMasters/notesMaster1.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notesMaster xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}">
<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld>
<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
<p:notesStyle/></p:notesMaster>''')
    write('ppt/notesMasters/_rels/notesMaster1.xml.rels', rels([
        ('rId1', RT + 'theme', '../theme/theme2.xml')]))
    write('ppt/slideMasters/slideMaster1.xml', master_xml())
    write('ppt/slideMasters/_rels/slideMaster1.xml.rels', rels([
        ('rId1', RT + 'slideLayout', '../slideLayouts/slideLayout1.xml'),
        ('rId2', RT + 'theme', '../theme/theme1.xml')]))
    write('ppt/slideLayouts/slideLayout1.xml', layout_xml())
    write('ppt/slideLayouts/_rels/slideLayout1.xml.rels', rels([
        ('rId1', RT + 'slideMaster', '../slideMasters/slideMaster1.xml')]))

    media_names = {}          # (deck, orig name) -> new name
    slide_no = 0
    notes_no = 0
    manifest = []             # (out_slide_index, deck, src_index)
    exts = set()

    for deck in DECKS:
        z = zipfile.ZipFile(os.path.join(SRC, deck + '.pptx'))
        pres = etree.fromstring(z.read('ppt/presentation.xml'))
        prels = etree.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
        rid2tgt = {e.get('Id'): e.get('Target') for e in prels}
        order = []
        for sid in pres.find('p:sldIdLst', NS):
            tgt = rid2tgt[sid.get('{%s}id' % R)]
            order.append('ppt/' + tgt.replace('../', '').lstrip('/'))

        for src_name in order:
            slide_no += 1
            src_idx = int(re.search(r'slide(\d+)\.xml', src_name).group(1))
            manifest.append((slide_no, deck, src_idx))

            xml = z.read(src_name)
            srels_name = src_name.replace('slides/', 'slides/_rels/') + '.rels'
            new_rels = [('rId1', RT + 'slideLayout', '../slideLayouts/slideLayout1.xml')]
            rid_map = {}
            nrid = 2
            if srels_name in z.namelist():
                sr = etree.fromstring(z.read(srels_name))
                for e in sr:
                    typ, tgt, rid = e.get('Type'), e.get('Target'), e.get('Id')
                    if typ.endswith('/slideLayout'):
                        rid_map[rid] = 'rId1'
                        continue
                    if typ.endswith('/image') or typ.endswith('/audio') or typ.endswith('/video'):
                        base = os.path.basename(tgt)
                        key = (deck, base)
                        if key not in media_names:
                            ext = os.path.splitext(base)[1].lower().lstrip('.')
                            exts.add(ext)
                            newn = f'm{len(media_names)+1:03d}.{ext}'
                            media_names[key] = newn
                            srcpath = 'ppt/' + tgt.replace('../', '')
                            with open(os.path.join(OUT, 'ppt/media', newn), 'wb') as fh:
                                fh.write(z.read(srcpath))
                        newid = f'rId{nrid}'; nrid += 1
                        rid_map[rid] = newid
                        new_rels.append((newid, typ, '../media/' + media_names[key]))
                        continue
                    if typ.endswith('/notesSlide'):
                        notes_no += 1
                        nsrc = 'ppt/' + tgt.replace('../', '')
                        nroot = etree.fromstring(z.read(nsrc))
                        # this notes part gets fresh rels; drop every inherited r: ref
                        for el in nroot.iter():
                            for att in list(el.attrib):
                                if att.startswith('{%s}' % R):
                                    del el.attrib[att]
                        nname = f'notesSlide{notes_no}.xml'
                        with open(os.path.join(OUT, 'ppt/notesSlides', nname), 'wb') as fh:
                            fh.write(etree.tostring(nroot, xml_declaration=True,
                                                    encoding='UTF-8', standalone=True))
                        write(f'ppt/notesSlides/_rels/{nname}.rels', rels([
                            ('rId1', RT + 'notesMaster', '../notesMasters/notesMaster1.xml'),
                            ('rId2', RT + 'slide', f'../slides/slide{slide_no}.xml')]))
                        newid = f'rId{nrid}'; nrid += 1
                        rid_map[rid] = newid
                        new_rels.append((newid, typ, f'../notesSlides/{nname}'))
                        continue
                    if typ.endswith('/hyperlink'):
                        newid = f'rId{nrid}'; nrid += 1
                        rid_map[rid] = newid
                        new_rels.append((newid, typ, tgt, e.get('TargetMode') or 'External'))
                        continue
                    # anything else (oleObject etc.) -> drop reference
                    rid_map[rid] = None

            # rewrite r:embed / r:link / r:id refs in the slide xml
            root = etree.fromstring(xml)
            for el in root.iter():
                for att in ('{%s}embed' % R, '{%s}link' % R, '{%s}id' % R):
                    v = el.get(att)
                    if v is None:
                        continue
                    nv = rid_map.get(v, None)
                    if nv is None:
                        del el.attrib[att]
                    else:
                        el.set(att, nv)

            with open(os.path.join(OUT, f'ppt/slides/slide{slide_no}.xml'), 'wb') as fh:
                fh.write(etree.tostring(root, xml_declaration=True,
                                        encoding='UTF-8', standalone=True))
            write(f'ppt/slides/_rels/slide{slide_no}.xml.rels', rels(new_rels))

    # ---------------- presentation.xml
    sldids = ''.join(f'<p:sldId id="{255+i}" r:id="rId{100+i}"/>' for i in range(1, slide_no + 1))
    write('ppt/presentation.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}" saveSubsetFonts="1">
<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
<p:notesMasterIdLst><p:notesMasterId r:id="rId4"/></p:notesMasterIdLst>
<p:sldIdLst>{sldids}</p:sldIdLst>
<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}"/>
<p:notesSz cx="{SLIDE_H}" cy="{SLIDE_W}"/>
</p:presentation>''')

    pr = [('rId1', RT + 'slideMaster', 'slideMasters/slideMaster1.xml'),
          ('rId2', RT + 'theme', 'theme/theme1.xml'),
          ('rId3', RT + 'presProps', 'presProps.xml'),
          ('rId4', RT + 'notesMaster', 'notesMasters/notesMaster1.xml')]
    pr += [(f'rId{100+i}', RT + 'slide', f'slides/slide{i}.xml') for i in range(1, slide_no + 1)]
    write('ppt/_rels/presentation.xml.rels', rels(pr))
    write('ppt/presProps.xml',
          f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"/>')

    write('_rels/.rels', rels([
        ('rId1', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument',
         'ppt/presentation.xml')]))

    defaults = {'rels': 'application/vnd.openxmlformats-package.relationships+xml',
                'xml': 'application/xml'}
    img_ct = {'png': 'image/png', 'jpeg': 'image/jpeg', 'jpg': 'image/jpeg',
              'gif': 'image/gif', 'emf': 'image/x-emf', 'wmf': 'image/x-wmf',
              'tiff': 'image/tiff', 'bmp': 'image/bmp', 'svg': 'image/svg+xml'}
    for e in exts:
        defaults[e] = img_ct.get(e, 'application/octet-stream')
    ct = [f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="{CT}">']
    for e, c in defaults.items():
        ct.append(f'<Default Extension="{e}" ContentType="{c}"/>')
    base = 'application/vnd.openxmlformats-officedocument.presentationml.'
    ct.append(f'<Override PartName="/ppt/presentation.xml" ContentType="{base}presentation.main+xml"/>')
    ct.append(f'<Override PartName="/ppt/presProps.xml" ContentType="{base}presProps+xml"/>')
    ct.append(f'<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="{base}slideMaster+xml"/>')
    ct.append(f'<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="{base}slideLayout+xml"/>')
    ct.append('<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>')
    if notes_no:
        ct.append('<Override PartName="/ppt/theme/theme2.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>')
        ct.append(f'<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="{base}notesMaster+xml"/>')
    for i in range(1, slide_no + 1):
        ct.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="{base}slide+xml"/>')
    for i in range(1, notes_no + 1):
        ct.append(f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="{base}notesSlide+xml"/>')
    ct.append('</Types>')
    write('[Content_Types].xml', ''.join(ct))

    with open(os.path.join(HERE, 'manifest.txt'), 'w') as fh:
        for i, d, s in manifest:
            fh.write(f'{i}\t{d}\t{s}\n')
    print(f'merged {slide_no} slides, {len(media_names)} media, {notes_no} notes')


if __name__ == '__main__':
    main()
