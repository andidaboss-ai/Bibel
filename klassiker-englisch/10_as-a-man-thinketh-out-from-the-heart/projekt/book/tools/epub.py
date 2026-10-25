"""EPUB 3 for the annotated classics (same content as the print edition, without journal lines)."""
import datetime, html, os, re, uuid, zipfile

from md import inline, slug
from build import render, split_note, copyright_html, ROMAN, part_plan

CSS = """
body { font-family: serif; line-height: 1.5; margin: 0 5%; text-align: justify; }
p { margin: 0; text-indent: 1.2em; }
p.first, p.lead { text-indent: 0; }
.initial { float: left; font-size: 3.1em; line-height: .9; padding: .06em .08em 0 0; }
.sc { font-variant: small-caps; letter-spacing: .04em; }
h1, h2 { font-weight: normal; text-align: center; line-height: 1.2; }
h1 { font-size: 1.9em; margin: 1em 0 .2em; }
h2 { font-size: 1.6em; margin: .3em 0 .2em; }
.num { text-align: center; font-size: .8em; letter-spacing: .3em; margin-top: 2.5em; }
.label, .afflabel { text-align: center; font-size: .72em; letter-spacing: .3em; text-transform: uppercase; margin: 1.6em 0 .6em; }
p.aff { text-indent: 0; text-align: center; font-style: italic; margin: 0 1em .25em; }
.div { text-align: center; font-size: .6em; margin: .5em 0; }
.orn { text-align: center; margin: .5em 0 1.4em; letter-spacing: .5em; }
blockquote { margin: 1em 1.5em; text-align: center; font-style: italic; }
blockquote p { text-indent: 0; }
.companion { margin-top: 2em; border-top: 1px solid #999; padding-top: .6em; }
.key { border-top: 1px solid #666; border-bottom: 1px solid #666; padding: .4em 1em .8em; margin-top: 1.4em; }
.src { text-align: center; font-size: .72em; letter-spacing: .2em; text-transform: uppercase; margin-bottom: 1em; }
.copy p { text-indent: 0; margin-bottom: .7em; font-size: .85em; text-align: left; }
.title { text-align: center; margin-top: 3em; }
.title p { text-indent: 0; text-align: center; }
.epi { text-align: center; margin-top: 30%; font-style: italic; }
.maxims { border: 1px solid #666; padding: .6em 1em; margin: 1.4em .5em; text-align: center; }
.maxims p { text-indent: 0; font-style: italic; text-align: center; margin: .3em 0; }
.maxims .mt { font-size: .72em; letter-spacing: .3em; text-transform: uppercase; }
p.summary { text-indent: 0; text-align: center; font-style: italic; font-size: .9em; margin: 0 1.5em 1.4em; }
.longitalic p { font-style: italic; }
p.sec { text-indent: 0; margin-top: .5em; }
.sn { font-weight: bold; margin-right: .4em; }
.verse { margin: .6em 0 .6em 1.5em; }
.dn { font-variant: small-caps; }
p.salute { text-indent: 0; font-style: italic; }
p.close { text-indent: 0; text-align: right; font-style: italic; }
p.fnote { text-indent: 0; font-size: .85em; }
.verse p { text-indent: 0; font-style: italic; text-align: left; }
ul.f, .finder ul { list-style: none; padding: 0; }
.finder li { margin-bottom: .5em; }
"""

ORN = '<div class="orn">✦</div>'


def xhtml(title, body):
    body = re.sub(r"<br>", "<br/>", body).replace("&nbsp;", "&#160;")
    body = re.sub(r"<svg.*?</svg>", "✦", body, flags=re.S)
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><meta charset="utf-8"/>'
            f'<title>{html.escape(title)}</title><link rel="stylesheet" href="style.css"/></head><body>{body}</body></html>')


def build(c, B, OUT):
    os.makedirs(os.path.join(OUT, "ebook"), exist_ok=True)
    name = B["slug"]
    path = os.path.join(OUT, "ebook", f"{name}.epub")
    cover = os.path.join(OUT, "ebook", f"{name}-cover.jpg")
    tl = B["title_lines"]
    docs = [("title", "Title", f'<div class="title"><p>{B["author"].upper()}</p><h1>{html.escape(B["title"])}</h1>'
             f'<p><em>{B["edition"]}</em></p><p>{" ".join(B["title_page_sub"])}</p>'
             f'<p style="margin-top:2em">Introduction and notes by {B["editor"]}</p></div>'),
            ("copyright", "Copyright", f'<div class="copy">{copyright_html()}</div>')]
    if B.get("epigraph"):
        docs.append(("epigraph", "Epigraph", f'<div class="epi"><p>{html.escape(B["epigraph"]["text"])}</p>'
                     f'<p class="src">{html.escape(B["epigraph"]["source"])}</p></div>'))
    for t, b in c["front"]:
        docs.append((slug(t), t, f"<h2>{inline(t)}</h2>{ORN}{render(b)}"))
    creed = B.get("creed", "")
    for (t, b, nb), (new, lab, num, part) in zip(c["chapters"], part_plan(c["chapters"])):
        if new and B.get("parts"):
            docs.append((slug(new["title"]), new["title"], f'<div class="title"><h1>{html.escape(new["title"])}</h1><p>{html.escape(new.get("sub", ""))}</p>' + ("".join(f'<p class="motto"><em>{inline(x)}</em></p>' for x in new.get("motto", []))) + '</div>'))
        parts = split_note(nb)
        label = f'<p class="num">{lab.upper()} {ROMAN[num]}</p>' if lab else ""
        s = f'{label}<h2>{inline(t)}</h2>{ORN}{render(b, lead=t != creed, creed=t == creed)}'
        if parts:
            s += '<div class="companion">'
            if "reflection" in parts: s += f'<p class="label">Reflection</p>{render(parts["reflection"])}'
            if "practice" in parts: s += f'<p class="label">Practice</p>{render(parts["practice"])}'
            if "key" in parts: s += f'<div class="key"><p class="label">{B["labels"]["key"]}</p>{render(parts["key"])}</div>'
            s += "</div>"
        docs.append((slug(t), t, s))
    for t, b in c["days"]:
        body = []
        for k, v in b:
            if k == "h3":
                body.append(f'<h2 style="font-size:1.25em;margin-top:2em">{inline(v)}</h2>')
            elif k == "p" and v.startswith("Source:"):
                body.append(f'<p class="src">{inline(v[7:].strip())}</p>')
            else:
                body.append(render([(k, v)]))
        docs.append((slug(t), t, f"<h2>{inline(t)}</h2>{ORN}{''.join(body)}"))
    for t, b in c["finder"]:
        docs.append((slug(t), t, f'<div class="finder"><h2>{inline(t)}</h2>{ORN}{render(b)}</div>'))
    for t, b in c["back"]:
        docs.append((slug(t), t, f"<h2>{inline(t)}</h2>{ORN}{render(b)}"))

    uid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, f"{name}-annotated-{B['editor']}"))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    has_cover = os.path.exists(cover)
    manifest = "".join(f'<item id="d-{d}" href="{d}.xhtml" media-type="application/xhtml+xml"/>' for d, _, _ in docs)
    spine = "".join(f'<itemref idref="d-{d}"/>' for d, _, _ in docs)
    start = next(d for d, _, _ in docs if d not in ("title", "copyright", "epigraph"))
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">{uid}</dc:identifier>
<dc:title id="t1">{html.escape(B["kdp_title"])}</dc:title><meta refines="#t1" property="title-type">main</meta>
<dc:title id="t2">{html.escape(B["subtitle"])}</dc:title><meta refines="#t2" property="title-type">subtitle</meta>
<dc:creator id="au">{B["author"]}</dc:creator><meta refines="#au" property="role" scheme="marc:relators">aut</meta>
<dc:contributor id="ed">{B["editor"]}</dc:contributor><meta refines="#ed" property="role" scheme="marc:relators">edt</meta>
<dc:language>en</dc:language>
<dc:rights>Original text public domain ({B["first_published"]}). Editorial material © {datetime.date.today().year} {B["editor"]}.</dc:rights>
<meta property="dcterms:modified">{now}</meta>
{'<meta name="cover" content="cover-image"/>' if has_cover else ''}
</metadata>
<manifest>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="css" href="style.css" media-type="text/css"/>
{'<item id="cover-image" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>' if has_cover else ''}
{manifest}
</manifest>
<spine>{spine}</spine>
</package>'''
    items = "".join(f'<li><a href="{d}.xhtml">{html.escape(re.sub(r"[*]", "", t))}</a></li>'
                    for d, t, _ in docs if d not in ("title", "copyright", "epigraph"))
    nav = xhtml("Contents", f'<nav epub:type="toc" id="toc"><h2>Contents</h2><ol>{items}</ol></nav>'
                f'<nav epub:type="landmarks" hidden=""><ol><li><a epub:type="bodymatter" href="{start}.xhtml">Start</a></li></ol></nav>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        if has_cover:
            z.write(cover, "OEBPS/cover.jpg", compress_type=zipfile.ZIP_STORED)
        for d, t, b in docs:
            z.writestr(f"OEBPS/{d}.xhtml", xhtml(re.sub(r"[*]", "", t), b), compress_type=zipfile.ZIP_DEFLATED)
    print(path)
