import zipfile,re,sys
from lxml import etree
A='http://schemas.openxmlformats.org/drawingml/2006/main'
def slide_texts(path, slides=None):
    z=zipfile.ZipFile(path)
    names=[n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n)]
    names.sort(key=lambda n:int(re.search(r'(\d+)',n.split('/')[-1]).group(1)))
    out=[]
    for n in names:
        r=etree.fromstring(z.read(n))
        txt=[t.text or '' for t in r.iter('{%s}t'%A)]
        out.append(''.join(txt))
    return out
