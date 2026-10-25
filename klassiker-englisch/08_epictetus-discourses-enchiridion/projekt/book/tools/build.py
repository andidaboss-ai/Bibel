"""Builds an annotated classic from book.json + text/*.md: print interior (PDF), print covers (PDF, 600 dpi), EPUB 3.

Usage (in the book folder):
    python3 tools/build.py            # everything, covers at 600 dpi
    python3 tools/build.py --draft    # covers at 300 dpi (faster)
    python3 tools/build.py --epub     # only the EPUB
Text files: original.md (the public-domain text, ## per chapter), front.md, chapters.md (### Reflection,
### Practice, ### Key … per chapter), thirty_days.md, finder.md, back.md.
"""
import datetime, html, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md import inline, blocks, sections, slug  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
TEXT = os.path.join(ROOT, "text")
OUT = os.path.join(ROOT, "output")
B = json.load(open(os.path.join(ROOT, "book.json"), encoding="utf-8"))
NAME, TRIM, YEAR = B["slug"], tuple(B["trim"]), datetime.date.today().year

def _roman(n):
    r = ""
    for v, l in ((100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            r += l; n -= v
    return r


ROMAN = [_roman(i) for i in range(1, 200)]


def part_plan(chapters):
    """Per chapter: (part starting here or None, label word, number index, part of this chapter).
    Without B["parts"] the whole original text is one part (B["part_title"], labels.chapter)."""
    parts = B.get("parts") or [{"first": chapters[0][0], "title": B["part_title"], "sub": B.get("part_sub", ""),
                                 "label": B["labels"].get("chapter", "Chapter")}]
    starts = {p["first"]: p for p in parts}
    plan, cur, num = [], None, 0
    for t, *_ in chapters:
        new = starts.get(t)
        if new:
            cur, num = new, 0
        if t in B.get("unnumbered", []):
            plan.append((new, "", None, cur))
        else:
            plan.append((new, cur.get("label", ""), num, cur)); num += 1
    return plan

STAR = '<svg viewBox="0 0 10 10"><path d="M5 0C5.4 4.6 5.4 4.6 10 5C5.4 5.4 5.4 5.4 5 10C4.6 5.4 4.6 5.4 0 5C4.6 4.6 4.6 4.6 5 0Z" fill="#555"/></svg>'
ORN = ('<div class="orn"><svg viewBox="0 0 70 9"><line x1="0" y1="4.5" x2="27" y2="4.5" stroke="#444" stroke-width=".5"/>'
       '<path d="M35 0C35.5 3.9 35.5 3.9 39.5 4.5C35.5 5.1 35.5 5.1 35 9C34.5 5.1 34.5 5.1 30.5 4.5C34.5 3.9 34.5 3.9 35 0Z" fill="#222"/>'
       '<circle cx="29.2" cy="4.5" r=".7" fill="#444"/><circle cx="40.8" cy="4.5" r=".7" fill="#444"/>'
       '<line x1="43" y1="4.5" x2="70" y2="4.5" stroke="#444" stroke-width=".5"/></svg></div>')
CAP = ('<div class="cap"><svg viewBox="0 0 300 9" preserveAspectRatio="xMidYMid meet"><line x1="0" y1="4.5" x2="138" y2="4.5" stroke="#555" stroke-width=".5"/>'
       '<path d="M150 0C150.5 3.9 150.5 3.9 154.5 4.5C150.5 5.1 150.5 5.1 150 9C149.5 5.1 149.5 5.1 145.5 4.5C149.5 3.9 149.5 3.9 150 0Z" fill="#222"/>'
       '<line x1="162" y1="4.5" x2="300" y2="4.5" stroke="#555" stroke-width=".5"/></svg></div>')


def read(name):
    p = os.path.join(TEXT, name)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def mk(kind, s):
    """Invisible marker, read back from the PDF to place running heads and page numbers."""
    return f'<span class="mk">@@{kind}:{s}@@</span>'


# ---------- rendering ----------

def lead_html(text):
    """First paragraph of a chapter: drop cap and the first words in small caps."""
    m = re.match(r"^([“‘\"']?)(\w)(.*)$", text, re.S)
    if m and len(text) < 120:  # too short to carry a drop cap: small caps only
        words = text.split(" ")
        return f'<p class="lead"><span class="sc">{inline(" ".join(words[:2]))}</span> {inline(" ".join(words[2:]))}</p>'
    if not m:
        return f'<p class="lead">{inline(text)}</p>'
    q, first, rest = m.groups()
    words = rest.split(" ")
    n = 1 if len(words[0]) > 7 else 2 if len(words) > 2 else 1
    head, tail = " ".join(words[:n]), " ".join(words[n:])
    return (f'<p class="lead"><span class="initial">{html.escape(q)}{html.escape(first)}</span>'
            f'<span class="sc">{inline(head)}</span> {inline(tail)}</p>')


def is_maxim(k, v):
    return k == "p" and re.fullmatch(r"\*[^*].*[^*]\*", v.strip()) is not None


def group_maxims(bl):
    """Author's boxed maxims (whole paragraphs in italics, with an optional ### title before them) → one block."""
    out, i = [], 0
    while i < len(bl):
        k, v = bl[i]
        title = None
        if k in ("h3", "h4") and i + 1 < len(bl) and is_maxim(*bl[i + 1]):
            title, i = v, i + 1
            k, v = bl[i]
        if is_maxim(k, v):
            items = []
            while i < len(bl) and is_maxim(*bl[i]):
                items.append(bl[i][1].strip()[1:-1]); i += 1
            out.append(("maxims", (title, items)))
            continue
        if title is not None:
            out.append(("h3", title))
        out.append((k, v)); i += 1
    return out


def render(bl, lead=False, creed=False):
    bl = group_maxims(bl)
    h, first, aff, pending = [], True, creed, None
    for k, v in bl:
        if k in ("h3", "h4"):
            aff = v.lower().startswith("affirmation")
            h.append(f'<div class="afflabel">{inline(v)}</div>' if aff else f"<{k}>{inline(v)}</{k}>")
            first = True
        elif k == "hr":
            h.append(f'<div class="div">{STAR}</div>'); first = True
        elif k in ("salute", "close", "fnote"):
            h.append(f'<p class="{k}">{inline(v)}</p>'); first = k != "salute" or first
        elif k == "summary":
            h.append(f'<p class="summary">{inline(v)}</p>'); first = True
        elif k == "maxims":
            title, items = v
            t = f'<div class="mt">{inline(title.strip("*"))}</div>' if title else ""
            if sum(len(x) for x in items) > 1100:  # too long for one framed page: flowing italic text
                h.append('<div class="longitalic">' + "".join(f'<p>{inline(x)}</p>' for x in items) + "</div>")
            else:
                h.append(f'<div class="maxims">{t}' + f'<div class="ms">{STAR}</div>'.join(f'<p>{inline(x)}</p>' for x in items) + "</div>")
            first = True
        elif k == "p" and aff:
            h.append(f'<p class="aff">{inline(v)}</p>')
        elif k == "p" and B.get("numbered_sections") and re.fullmatch(r"\d+\.", v.strip()):
            pending = v.strip()[:-1]  # a section number standing alone before verse lines
        elif k == "verse":
            num = f'<span class="sn">{pending}</span>' if pending else ""
            h.append(f'<div class="verse">{num}' + "".join(f"<p>{inline(x)}</p>" for x in v) + "</div>"); pending = None; first = True
        elif k == "p" and B.get("numbered_sections") and re.match(r"^\d+\. ", v):
            n, rest = v.split(". ", 1)
            h.append(f'<p class="sec"><span class="sn">{n}</span>{inline(rest)}</p>'); first = False
        elif k == "p":
            if lead:
                h.append(lead_html(v)); lead = False
            else:
                h.append(('<p class="first">' if first else "<p>") + inline(v) + "</p>")
            first = False
        elif k == "quote":
            h.append(f"<blockquote><p>{inline(v)}</p></blockquote>"); first = True
        elif k in ("ul", "ol"):
            h.append(f"<{k}>" + "".join(f"<li>{inline(x)}</li>" for x in v) + f"</{k}>"); first = True
    return "\n".join(h)


def split_note(nb):
    parts, cur = {}, None
    for k, v in nb:
        if k == "h3":
            cur = v.lower().split()[0]; parts[cur] = []
        elif cur:
            parts[cur].append((k, v))
    return parts


def content():
    notes = dict(sections(read("chapters.md")))
    return {
        "front": sections(read("front.md")),
        "chapters": [(t, b, notes.get(t, [])) for t, b in sections(read("original.md"), numbered=bool(B.get("numbered_sections")))],
        "days": sections(read("thirty_days.md")),
        "finder": sections(read("finder.md")),
        "back": sections(read("back.md")),
    }


def fonts_css():
    f = lambda n: "file://" + os.path.join(ROOT, "fonts", n)
    faces = [("EBG", "normal", 400, "EBG-Regular.ttf"), ("EBG", "italic", 400, "EBG-Italic.ttf"),
             ("EBG", "normal", 600, "EBG-SemiBold.ttf"), ("CG", "normal", 400, "CG-Regular.ttf"),
             ("CG", "normal", 500, "CG-Medium.ttf"), ("CG", "normal", 600, "CG-SemiBold.ttf"),
             ("CG", "italic", 400, "CG-Italic.ttf"), ("CG", "italic", 500, "CG-MediumItalic.ttf"),
             ("Jost", "normal", 300, "Jost-Light.ttf"), ("Jost", "normal", 400, "Jost-Regular.ttf"),
             ("Jost", "normal", 500, "Jost-Medium.ttf")]
    return "".join(f"@font-face{{font-family:{a};font-style:{s};font-weight:{w};src:url('{f(n)}')}}" for a, s, w, n in faces)


def copyright_html():
    crisis = (" If you are thinking about ending your life, please reach out now: in the US call or text 988; "
              "in the UK and Ireland call Samaritans on 116 123." if B.get("crisis_note") else "")
    health = (f"<p><strong>Please note:</strong> This book is about {B.get('practice_kind', 'a spiritual practice')}. It is not medical, psychological, "
              f"financial or legal advice. {B['labels']['practice_word']} can go alongside professional help, never instead of it. If you are "
              f"ill or in crisis, please see a doctor or a qualified professional. In an emergency, call 911 (US) or 999 (UK).{crisis}</p>"
              if B.get("health_note") else "")
    return (f"<p><em>{html.escape(B['kdp_title'])}</em><br>{html.escape(B['subtitle'])}</p>"
            + (f"<p>{B['pd_statement']}</p>" if B.get("pd_statement") else
               f"<p>The text of <em>{html.escape(B['title'])}</em> by {B['author']} ({B['author_years']}) was first published in "
               f"{B['first_published']} and is in the public domain. This edition follows the {B['first_published']} text; "
               f"spelling and wording are kept, obvious printing errors are corrected.</p>") +
            f"<p>{B['labels']['new_material']}, cover and interior design © {YEAR} {B['editor']}. All rights reserved.</p>"
            f"{health}<p>Edited by {B['editor']}</p>")


def toc_entries(c):
    P = B["labels"]["toc_parts"]
    e = [("part", P[0])] + [("i", t) for t, _ in c["front"]]
    for (t, _, _), (new, _, _, part) in zip(c["chapters"], part_plan(c["chapters"])):
        if new:
            e.append(("part", new["title"]))
            if new.get("toc") is False:
                e.append(("i", new["title"]))
        if part.get("toc") is not False:
            e.append(("i", t))
    e += [("part", P[1])] + [("i", t) for t, _ in c["days"]] + [("i", t) for t, _ in c["finder"]]
    e += [("part", P[2])] + [("i", t) for t, _ in c["back"]]
    return e


def front_section(t, b, kick="", cls=""):
    return (f'<section class="recto {cls}">{mk("S", slug(t))}{mk("O", slug(t))}<div class="front-h">'
            f'{f"<div class=kick>{kick}</div>" if kick else ""}<h2>{inline(t)}</h2></div>{ORN}{render(b)}</section>')


def print_html(c, pages):
    h = [f'<!doctype html><html lang="en-US"><head><meta charset="utf-8"><style>{fonts_css()}'
         f'{open(os.path.join(TOOLS, "print.css"), encoding="utf-8").read()}</style></head><body class="{"compact" if B.get("compact_openers") else ""}">']
    tl = B["title_lines"]
    h.append(f'<div class="half">{mk("F", "half")}{html.escape(B["title"])}{ORN}</div>')
    h.append(f'''<div class="title recto">{mk("F", "title")}<div class="au">{B["author"]}</div>
{"".join(f'<div class="{"t2" if st == "small" else "t1"}"{" style=margin-top:0" if i else ""}>{html.escape(l)}</div>' for i, (l, st) in enumerate(zip(tl, B.get("title_styles") or ["small" if j % 2 else "big" for j in range(len(tl))])))}
<div class="ed">{B["edition"]}</div><div class="sub">{"<br>".join(B["title_page_sub"])}</div>
<div class="by">Introduction and notes by {B["editor"]}</div></div>''')
    h.append(f'<div class="copy page">{mk("F", "copy")}{copyright_html()}</div>')
    if B.get("epigraph"):
        ep = B["epigraph"]
        h.append(f'<div class="epigraph recto">{mk("F", "epigraph")}<div class="q">{html.escape(ep["text"])}</div>'
                 f'<div class="s">{html.escape(ep["source"])}</div></div>')
    toc = []
    for kind, t in toc_entries(c):
        if kind == "part":
            toc.append(f'<li class="part">{html.escape(t)}</li>')
        else:
            toc.append(f'<li><span class="t">{inline(t)}</span><span class="d"></span><span class="n">{pages.get(slug(t), "")}</span></li>')
    h.append(f'<section class="recto">{mk("F", "contents")}<div class="toc-h">Contents</div>{ORN}<ul class="toc{" two" if max(len(t) for k, t in toc_entries(c)) <= 30 else ""}">{"".join(toc)}</ul></section>')
    for t, b in c["front"]:
        h.append(front_section(t, b))
    creed = B.get("creed", "")
    for i, ((t, b, nb), (new, lab, num, part)) in enumerate(zip(c["chapters"], part_plan(c["chapters"]))):
        s = slug(t)
        if new:
            h.append(f'<div class="half recto" style="padding-top:2.9in">{mk("F", "part")}{mk("S", slug(new["title"]))}{html.escape(new["title"])}{ORN}'
                     f'<div style="font-family:Jost;font-size:7pt;letter-spacing:.42em;text-transform:uppercase;padding-left:.42em">'
                     f'{html.escape(new.get("sub", ""))}</div></div>')
        label = f'<div class="num"><span>{lab}</span>{ROMAN[num]}</div>' if lab else ""
        body = render(b, lead=t != creed, creed=t == creed)
        out = [f'<section class="{"recto" if new or t == creed else "page"}{" creed" if t == creed else ""}">{mk("S", s)}{mk("O", s)}'
               f'<div class="opener">{label}<h2{" class=long" if len(t) > 48 else ""}>{inline(t)}</h2></div>{ORN}'
               f'<div class="chapter-text">{body}</div>']
        parts = split_note(nb)
        if parts:
            out.append(f'<div class="companion">{CAP}')
            if "reflection" in parts:
                out.append(f'<div class="label">Reflection</div>{render(parts["reflection"])}')
            if "practice" in parts:
                out.append(f'<div class="label sub">Practice</div>{render(parts["practice"])}')
            if "key" in parts:
                out.append(f'<div class="key"><div class="label">{B["labels"]["key"]}</div>{render(parts["key"])}</div>')
            out.append(f'<div class="lines"><div class="label">{B["labels"]["lines"]}</div>' + "<div></div>" * 4 + "</div></div>")
        out.append("</section>")
        h.append("".join(out))
    if c["days"]:
        t, b = c["days"][0]
        intro, days, cur = [], [], None
        for k, v in b:
            if k == "h3":
                cur = (v, []); days.append(cur)
            elif cur:
                cur[1].append((k, v))
            else:
                intro.append((k, v))
        h.append(front_section(t, intro))
        for dt, db in days:
            m = re.match(r"Day (\d+)\s*[–-]\s*(.*)", dt)
            n, theme = (m.group(1), m.group(2)) if m else ("", dt)
            body, first = [], True
            for k, v in db:
                if k == "p" and v.startswith("Source:"):
                    body.append(f'<div class="src">{inline(v[7:].strip())}</div>')
                elif k == "p":
                    body.append(('<p class="first">' if first else "<p>") + inline(v) + "</p>"); first = False
                else:
                    body.append(render([(k, v)]))
            h.append(f'<section class="day">{mk("S", slug(t))}<div class="dnum">Day</div><div class="big">{n}</div>'
                     f'<h2>{inline(theme)}</h2>{ORN}{"".join(body)}'
                     f'<div class="lines fill"><div class="label">{B["labels"]["day_lines"]}</div><div class="ruled">' + "<div></div>" * 24 + '</div></div>'
                     '<div class="check">' + " &nbsp;&nbsp;&nbsp; ".join(f"☐&#8201; {x}" for x in B["labels"]["checks"]) + '</div></section>')
    for t, b in c["finder"]:
        h.append(front_section(t, b, cls="finder"))
    for t, b in c["back"]:
        h.append(front_section(t, b, cls="finder" if any(k == "ul" for k, _ in b) else ""))
    h.append("</body></html>")
    return "\n".join(h)


def place_rectos(doc, pad):
    """Chromium ignores break-before: right. Every .recto element becomes a page break with a marker R:rN;
    the elements in `pad` get an empty page before them, so that they start on a right-hand (odd) page."""
    n = -1

    def rep(m):
        nonlocal n
        n += 1
        cls = re.sub(r"\brecto\b", "page", m.group(2))
        before = '<div class="padpage"></div>' if n in pad else ""
        return f'{before}<{m.group(1)} class="{cls}"{m.group(3)}>{mk("R", f"r{n}")}'
    return re.sub(r'<(div|section) class="([^"]*\brecto\b[^"]*)"([^>]*)>', rep, doc)


def pdf(src_html, out_pdf):
    subprocess.run(["node", os.path.join(TOOLS, "print_pdf.mjs"), src_html, out_pdf, *map(str, TRIM)], check=True)


def page_map(pdf_path):
    """Per page: markers found and whether the page has visible text."""
    txt = subprocess.run(["pdftotext", "-raw", pdf_path, "-"], capture_output=True, text=True).stdout.split("\f")
    if txt and not txt[-1].strip():
        txt = txt[:-1]
    res = []
    for t in txt:
        flat = re.sub(r"\s+", "", t)  # tiny marker text comes out letter-spaced
        marks = re.findall(r"@@(\w):([a-z0-9-]+)@@", flat)
        visible = re.sub(r"@@\w:[a-z0-9-]+@@", "", flat)
        res.append((marks, bool(visible)))
    return res


def running_heads(pm, titles):
    """Per page (recto?, head text, show folio?)."""
    heads, cur, front = [], None, True
    for i, (marks, visible) in enumerate(pm):
        kinds = {k for k, _ in marks}
        if "F" in kinds:
            front = not any(s == "part" for k, s in marks if k == "F") and front
            if any(s == "part" for k, s in marks if k == "F"):
                front = False
        for k, s in marks:
            if k == "S":
                cur = s; front = False
        opener = "O" in kinds or "F" in kinds
        recto = i % 2 == 0
        if front or not visible or "F" in kinds:
            heads.append((recto, "", False))
        elif opener:
            heads.append((recto, "", True))
        else:
            heads.append((recto, B["title"] if not recto else titles.get(cur, ""), True))
    return heads


def overlay_html(heads):
    h = [f'<!doctype html><html lang="en-US"><head><meta charset="utf-8"><style>{fonts_css()}'
         f'@page{{size:6in 9in;margin:0}} body{{margin:0}}'
         f'{open(os.path.join(TOOLS, "print.css"), encoding="utf-8").read().split("/* overlay")[1].split("*/", 1)[1]}'
         f'</style></head><body>']
    for i, (recto, head, folio) in enumerate(heads):
        inner, outer = (0.9, 0.66) if recto else (0.66, 0.9)
        rh = ""
        if head:
            pos = f"right:{outer}in" if recto else f"left:{outer if not recto else inner}in"
            rh = f'<div class="rh" style="{pos}">{html.escape(head)}</div>'
        fo = ""
        if folio:
            fo = f'<div class="fo" style="left:calc({inner if recto else outer}in + (6in - {inner + outer}in)/2 - .3in);text-align:center">{i + 1}</div>'
        h.append(f'<div class="ov">{rh}{fo}</div>')
    h.append("</body></html>")
    return "".join(h)


def build_pdf(c):
    from pypdf import PdfReader, PdfWriter
    os.makedirs(os.path.join(OUT, "print"), exist_ok=True)
    src = os.path.join(OUT, "_interior.html")
    raw = os.path.join(OUT, "_raw.pdf")
    final = os.path.join(OUT, "print", f"{NAME}-interior.pdf")
    titles = {}
    for (t, _, _), (new, _, _, part) in zip(c["chapters"], part_plan(c["chapters"])):
        titles[slug(t)] = part.get("rh") or (t if len(t) <= B.get("rh_max", 60) else part["title"])
        if new:
            titles[slug(new["title"])] = new["title"]
    titles.update({slug(t): t for t, _ in c["front"] + c["days"] + c["finder"] + c["back"]})
    pages, pad = {}, set()
    for _ in range(12):
        open(src, "w", encoding="utf-8").write(place_rectos(print_html(c, pages), pad))
        pdf(src, raw)
        pm = page_map(raw)
        new, wrong = {}, set()
        for i, (marks, _) in enumerate(pm):
            for k, s in marks:
                if k == "S" and s not in new:
                    new[s] = i + 1
                if k == "R" and (i + 1) % 2 == 0:
                    wrong.add(int(s[1:]))
        if new == pages and not wrong:
            break
        pages, pad = new, pad ^ wrong
    heads = running_heads(pm, titles)
    ov_src, ov_pdf = os.path.join(OUT, "_ov.html"), os.path.join(OUT, "_ov.pdf")
    open(ov_src, "w", encoding="utf-8").write(overlay_html(heads))
    pdf(ov_src, ov_pdf)
    base, ov = PdfReader(raw), PdfReader(ov_pdf)
    w = PdfWriter()
    for i, p in enumerate(base.pages):
        p.merge_page(ov.pages[i])
        w.add_page(p)
    w.add_metadata({"/Title": B["kdp_title"], "/Author": B["author"]})
    with open(final, "wb") as f:
        w.write(f)
    for t in (src, raw, ov_src, ov_pdf):
        os.remove(t)
    print(f"{final}: {len(base.pages)} pages")
    return len(base.pages)


# ---------- print covers ----------

PAPER = 0.002252     # inch per page, KDP white paper, black & white interior
BLEED = 0.125
HC_WRAP_X, HC_WRAP_Y, HC_HINGE, HC_BOARD = 0.591, 0.709, 0.197, 0.189   # KDP case laminate hardcover


def build_wraps(n, dpi=600):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    paper = n * PAPER
    kinds = {"paperback": (paper, BLEED, BLEED, 0.0), "hardcover": (paper + HC_BOARD, HC_WRAP_X, HC_WRAP_Y, HC_HINGE)}
    for kind, (spine, ex, ey, hinge) in kinds.items():
        w = 2 * (TRIM[0] + ex + hinge) + spine
        h = TRIM[1] + 2 * ey
        png = os.path.join(OUT, "print", f"{NAME}-cover-{kind}.png")
        subprocess.run(["node", os.path.join(TOOLS, "build_wrap.mjs"), png, str(w), str(h), str(spine),
                        str(ex), str(ey), str(hinge), str(dpi)], check=True, stdout=subprocess.DEVNULL)
        im = Image.open(png).convert("RGB").resize((round(w * dpi), round(h * dpi)), Image.LANCZOS)
        im.save(png[:-4] + ".pdf", "PDF", resolution=dpi, quality=95)
        prev = im.copy(); prev.thumbnail((2400, 2400)); prev.save(png[:-4] + "-preview.jpg", quality=88)
        os.remove(png)
        print(f"{kind}: {n} pages, cover {w:.3f} x {h:.3f} in, spine {spine:.3f} in")


if __name__ == "__main__":
    c = content()
    if "--epub" not in sys.argv:
        n = build_pdf(c)
        build_wraps(n, 300 if "--draft" in sys.argv else 600)
    import epub
    epub.build(c, B, OUT)
