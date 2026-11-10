#!/usr/bin/env python3
"""Build reference.pptx (for pandoc / R Markdown) from the EU Policy Lab template.

Pandoc selects layouts by *name*, so we rename the corporate layouts to the
names it expects and add a "Section Header" layout (cloned from the chapter
cover) that the corporate template does not have.

Usage: make_reference.py [template.pptx] [reference.pptx]
"""
import re
import sys
import zipfile

SRC = sys.argv[1] if len(sys.argv) > 1 else "eu_policy_lab_corporate_template.pptx"
DST = sys.argv[2] if len(sys.argv) > 2 else "reference.pptx"

RENAME = {  # layout file -> name pandoc looks for
    "slideLayout1.xml": "Title Slide",
    "slideLayout3.xml": "Content with Caption",
    "slideLayout4.xml": "Two Content",
}
NEW = "slideLayout15.xml"

z = zipfile.ZipFile(SRC)
files = {n: z.read(n) for n in z.namelist()}

# drop the example slides: pandoc builds its own
for n in [n for n in files if re.match(r"ppt/(slides|notesSlides)/", n)]:
    del files[n]
files["[Content_Types].xml"] = re.sub(
    rb'<Override PartName="/ppt/(slides|notesSlides)/[^>]*/>', b"", files["[Content_Types].xml"])
pres_rels = files["ppt/_rels/presentation.xml.rels"].decode()
dropped = re.findall(r'<Relationship [^>]*Target="slides/[^>]*/>', pres_rels)
ids = [re.search(r'Id="([^"]+)"', d).group(1) for d in dropped]
for d in dropped:
    pres_rels = pres_rels.replace(d, "")
files["ppt/_rels/presentation.xml.rels"] = pres_rels.encode()
pres = files["ppt/presentation.xml"].decode()
pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", "", pres, flags=re.S)
files["ppt/presentation.xml"] = pres.encode()

# Section Header = chapter cover with a title + body placeholder
cover = files["ppt/slideLayouts/slideLayout1.xml"].decode()
sect = (cover.replace('<p:ph type="ctrTitle"/>', '<p:ph type="title"/>')
             .replace('<p:ph type="subTitle" idx="1"/>', '<p:ph type="body" idx="1"/>'))
files[f"ppt/slideLayouts/{NEW}"] = sect.encode()
files[f"ppt/slideLayouts/_rels/{NEW}.rels"] = files["ppt/slideLayouts/_rels/slideLayout1.xml.rels"]
RENAME[NEW] = "Section Header"

# Content with Caption: pandoc wants the text placeholder typed as body
cap = "ppt/slideLayouts/slideLayout3.xml"
files[cap] = files[cap].replace(b'<p:ph sz="half" idx="2"/>', b'<p:ph type="body" sz="half" idx="2"/>')

for f, name in RENAME.items():
    p = f"ppt/slideLayouts/{f}"
    files[p] = re.sub(rb'(<p:cSld name=")[^"]*(")', rb"\g<1>" + name.encode() + rb"\2", files[p], count=1)

ct = files["[Content_Types].xml"].decode()
ct = ct.replace("</Types>",
    f'<Override PartName="/ppt/slideLayouts/{NEW}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/></Types>')
files["[Content_Types].xml"] = ct.encode()

rels = files["ppt/slideMasters/_rels/slideMaster1.xml.rels"].decode()
rels = rels.replace("</Relationships>",
    f'<Relationship Id="rId99" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{NEW}"/></Relationships>')
files["ppt/slideMasters/_rels/slideMaster1.xml.rels"] = rels.encode()
m = files["ppt/slideMasters/slideMaster1.xml"].decode()
m = m.replace("</p:sldLayoutIdLst>", '<p:sldLayoutId id="2147483699" r:id="rId99"/></p:sldLayoutIdLst>')
files["ppt/slideMasters/slideMaster1.xml"] = m.encode()

with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as out:
    out.writestr("[Content_Types].xml", files.pop("[Content_Types].xml"))
    for n, b in files.items():
        if not n.startswith("[trash]"):
            out.writestr(n, b)
print(f"wrote {DST}")
