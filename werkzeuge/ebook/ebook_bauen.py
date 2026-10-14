"""Baut aus den Kapiteldateien E-Books (EPUB 3) für Amazon KDP.

Aufruf (im Hauptordner des Projekts):
    python3 werkzeuge/ebook/ebook_bauen.py            # alle Ausgaben bauen
    python3 werkzeuge/ebook/ebook_bauen.py gesamt     # nur die Gesamtausgabe

Erzeugt in ausgabe/ebook/:
    bibel-leichte-sprache-gesamt.epub   alle 66 Bücher
    bibel-leichte-sprache-band-1.epub   1. Mose bis 1. Samuel
    bibel-leichte-sprache-band-2.epub   2. Samuel bis Psalmen
    bibel-leichte-sprache-band-3.epub   Sprüche bis Maleachi
    bibel-leichte-sprache-band-4.epub   Neues Testament
Die Bände sind genauso aufgeteilt wie die Druckausgabe (werkzeuge/druck/baende.json).

Die Cover (JPG für KDP) erzeugt werkzeuge/ebook/cover_bauen.mjs.
Quelle der Wahrheit bleiben die Kapiteldateien in texte/leichte-sprache/.
"""
import datetime, html, json, os, re, sys, uuid, zipfile

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(WURZEL, "ausgabe", "ebook")

# Name, der im Impressum als Herausgeber erscheint. Leer lassen = keine Angabe.
HERAUSGEBER = ""
JAHR = "2026"

AUSGABEN = {
    "gesamt": {
        "datei": "bibel-leichte-sprache-gesamt",
        "titel": "Die Bibel in Leichter Sprache",
        "untertitel": "Gesamtausgabe – Altes und Neues Testament",
        "band": "Gesamtausgabe",
        "oben": "Altes und Neues Testament",
        "buecher": range(1, 67),
    },
    "band-1": {
        "datei": "bibel-leichte-sprache-band-1",
        "titel": "Die Bibel in Leichter Sprache",
        "untertitel": "Band 1 – Altes Testament: 1. Mose bis 1. Samuel",
        "band": "Band 1",
        "oben": "Altes Testament",
        "buecher": range(1, 10),
    },
    "band-2": {
        "datei": "bibel-leichte-sprache-band-2",
        "titel": "Die Bibel in Leichter Sprache",
        "untertitel": "Band 2 – Altes Testament: 2. Samuel bis Psalmen",
        "band": "Band 2",
        "oben": "Altes Testament",
        "buecher": range(10, 20),
    },
    "band-3": {
        "datei": "bibel-leichte-sprache-band-3",
        "titel": "Die Bibel in Leichter Sprache",
        "untertitel": "Band 3 – Altes Testament: Sprüche bis Maleachi",
        "band": "Band 3",
        "oben": "Altes Testament",
        "buecher": range(20, 40),
    },
    "band-4": {
        "datei": "bibel-leichte-sprache-band-4",
        "titel": "Die Bibel in Leichter Sprache",
        "untertitel": "Band 4 – Das Neue Testament",
        "band": "Band 4",
        "oben": "Neues Testament",
        "buecher": range(40, 67),
    },
}

SCHRIFTEN = [
    ("Cinzel-Bold.ttf", "Cinzel", "bold", "normal"),
    ("Cinzel-Regular.ttf", "Cinzel", "normal", "normal"),
    ("Literata-Regular.ttf", "Literata", "normal", "normal"),
    ("Literata-Bold.ttf", "Literata", "bold", "normal"),
    ("Literata-Italic.ttf", "Literata", "normal", "italic"),
    ("Inter-SemiBold.ttf", "Inter", "600", "normal"),
    ("Inter-ExtraBold.ttf", "Inter", "800", "normal"),
]


def esc(t):
    return html.escape(t, quote=False)


def ziffern(t):
    """Ziffern in Cinzel-Überschriften gut lesbar machen (Cinzels 1 sieht aus wie I)."""
    return re.sub(r"(\d+)", r'<span class="z">\1</span>', t)


def inline(t):
    """Escaped Text mit **fett** und *kursiv*."""
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
    return t


# ---------- Kapitel in XHTML umwandeln ----------

def kapitel_html(md, buch, kap):
    zeilen = md.split("\n")
    titel = ""
    for z in zeilen:
        if z.startswith("### "):
            titel = z[4:].strip()
            break

    psalm = buch["code"] == "PSA"
    kopf_nr = f"Psalm {kap}" if psalm else f"Kapitel {kap}"
    out = [
        '<header class="kapkopf">',
        f'<p class="kicker">{esc(buch["name"])}</p>',
        f'<h2 class="kapnr">{ziffern(kopf_nr)}</h2>',
        f'<p class="kaptitel">{inline(titel)}</p>' if titel else "",
        '<div class="zier"><span></span></div>',
        "</header>",
    ]

    vers_offen = False
    intro = False
    box = None  # Liste der Zeilen in einem Kasten

    def vers_zu():
        nonlocal vers_offen
        if vers_offen:
            out.append("</p>")
            vers_offen = False

    def box_zu():
        nonlocal box
        if box is None:
            return
        zeilen_box = [z for z in box]
        box = None
        kopf = ""
        if zeilen_box and re.fullmatch(r"\*\*[^*]+\*\*", zeilen_box[0].strip()):
            kopf = zeilen_box.pop(0).strip()[2:-2]
        art = "erkl"
        if kopf.lower().startswith("wichtiger hinweis") or kopf.lower().startswith("ein wichtiger hinweis"):
            art = "hinweis"
        teile = [f'<aside class="box {art}" epub:type="note">']
        if kopf:
            teile.append(f'<p class="boxkopf">{esc(kopf)}</p>')
        for z in zeilen_box:
            if not z.strip():
                continue
            teile.append(f"<p>{inline(z.strip())}</p>")
        teile.append("</aside>")
        out.append("\n".join(teile))

    for z in zeilen:
        z = z.rstrip()
        if z.startswith("> ") or z == ">":
            vers_zu()
            if box is None:
                box = []
            box.append(z[2:] if z.startswith("> ") else "")
            continue
        box_zu()
        if z.startswith("# ") or z.startswith("### "):
            continue
        if z.strip() == "---":
            vers_zu()
            continue
        if z.startswith("## "):
            vers_zu()
            h = z[3:].strip()
            intro = h.startswith("Bevor es losgeht") or h.startswith("Rückblick")
            m = re.match(r"^(.*?)\s*\((Vers[^)]*)\)\s*$", h)
            klasse = "abschnitt"
            if h.startswith("Bevor es losgeht"):
                klasse = "abschnitt einf"
            elif h.startswith("Rückblick"):
                klasse = "abschnitt rueck"
            if m:
                out.append(f'<h3 class="{klasse}">{inline(m.group(1))} <span class="bereich">{esc(m.group(2))}</span></h3>')
            else:
                out.append(f'<h3 class="{klasse}">{ziffern(inline(h)) if klasse != "abschnitt" else inline(h)}</h3>')
            continue
        if not z.strip():
            vers_zu()
            continue
        m = re.match(r"^\[(\d+)\]\s*(.*)$", z)
        if m:
            vers_zu()
            n = m.group(1)
            out.append(f'<p class="v" id="v{n}"><span class="vn">{n}</span>{inline(m.group(2))}')
            vers_offen = True
            continue
        if vers_offen:
            out.append(f"<br/>{inline(z.strip())}")
        elif intro:
            out.append(f'<p class="t">{inline(z.strip())}</p>')
        else:
            out.append(f'<p class="v fort">{inline(z.strip())}')
            vers_offen = True
    vers_zu()
    box_zu()
    return "\n".join(x for x in out if x)


# ---------- Seitenrahmen ----------

def seite(titel, inhalt, klasse=""):
    k = f' class="{klasse}"' if klasse else ""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de" lang="de">
<head>
<meta charset="utf-8"/>
<title>{esc(titel)}</title>
<link rel="stylesheet" type="text/css" href="../css/bibel.css"/>
</head>
<body{k}>
{inhalt}
</body>
</html>
"""


def titelseite(a):
    return seite(a["titel"], f"""<section epub:type="titlepage" class="titelseite">
<p class="ts-oben">{esc(a["oben"])}</p>
<h1 class="ts-titel">Die Bibel</h1>
<p class="ts-unter">in Leichter Sprache</p>
<div class="zier gross"><span></span></div>
<p class="ts-band">{esc(a["untertitel"])}</p>
<p class="ts-zusatz">Mit Erklärungen zu jedem Abschnitt</p>
</section>""", "mitte")


def impressum(a):
    heute = datetime.date.today().isoformat()
    hg = f"<p>Herausgegeben von {esc(HERAUSGEBER)}.</p>\n" if HERAUSGEBER else ""
    return seite("Impressum", f"""<section epub:type="copyright-page" class="impressum">
<h2 class="klein">Impressum</h2>
<p><strong>{esc(a["titel"])}</strong><br/>{esc(a["untertitel"])}</p>
{hg}<p>Deutsche Übertragung in Leichte Sprache, {JAHR}.</p>
<p><strong>Grundlage:</strong> Diese Übertragung wurde neu aus der englischen World English Bible (WEB) erstellt. Die World English Bible ist gemeinfrei (Public Domain). Es wurde kein Text aus einer urheberrechtlich geschützten deutschen Bibelübersetzung übernommen.</p>
<p>Der Name „World English Bible“ ist eine geschützte Marke von eBible.org. Er wird hier nur genannt, um die Quelle anzugeben. Dieses Buch ist keine Ausgabe der World English Bible und wird nicht von eBible.org herausgegeben.</p>
<p><strong>Leichte Sprache:</strong> Die Übertragung orientiert sich an den Regeln für Leichte Sprache. Sie wurde nicht von einer Prüfgruppe geprüft und trägt kein Prüfsiegel.</p>
<p><strong>Schriften:</strong> Cinzel, Literata und Inter, alle unter der SIL Open Font License 1.1.</p>
<p class="stand">Stand: {heute}</p>
</section>""")


def vorwort(ganz=True):
    """ganz=False: für einen Band der Reihe (nicht die Gesamtausgabe)."""
    inhalt = ("Dieses Buch erzählt die ganze Bibel in Leichter Sprache." if ganz else
              "Diese Reihe erzählt in 4 Bänden die ganze Bibel in Leichter Sprache.")
    ende = "Am Ende des Buches" if ganz else "Am Ende jedes Bandes"
    return seite("So liest du dieses Buch", f"""<section epub:type="preface" class="vorwort">
<h2 class="seitentitel">So liest du dieses Buch</h2>
<div class="zier"><span></span></div>
<p class="t">Die Bibel ist das wichtigste Buch der Welt.</p>
<p class="t">Sie ist alt. Aber ihre Botschaft gilt auch heute.</p>
<p class="t">{inhalt}</p>
<p class="t">Kein Vers ist weggelassen. Kein Name und keine Zahl.</p>
<h3 class="abschnitt">Kurze Sätze</h3>
<p class="t">Jede Zeile ist ein kurzer Gedanke.</p>
<p class="t">So kannst du in Ruhe lesen.</p>
<h3 class="abschnitt">Die Zahlen am Rand</h3>
<p class="v"><span class="vn">1</span>Die kleinen Zahlen sind die Vers-Nummern.<br/>Mit ihnen kannst du jede Stelle finden.<br/>So wie in jeder anderen Bibel.</p>
<h3 class="abschnitt">Die Kästen</h3>
<aside class="box erkl"><p class="boxkopf">Was bedeutet das?</p><p>Nach jedem Abschnitt steht so ein Kasten.</p><p>Er erklärt, was du gelesen hast.</p><p>Und was es für heute bedeuten kann.</p></aside>
<aside class="box hinweis"><p class="boxkopf">Wichtiger Hinweis</p><p>Manche Stellen in der Bibel sind schwer.</p><p>Sie wurden auch missbraucht, zum Beispiel gegen Juden, gegen Frauen oder um Gewalt zu rechtfertigen.</p><p>An solchen Stellen steht so ein Hinweis.</p></aside>
<h3 class="abschnitt">Die Psalmen</h3>
<p class="t">Die Psalmen sind in manchen Bibeln anders gezählt.</p>
<p class="t">Dann steht die andere Zählung in Klammern dabei.</p>
<h3 class="abschnitt">Hilfe</h3>
<p class="t">Die Bibel erzählt auch von Leid und Gewalt.</p>
<p class="t">Wenn dich etwas belastet: {ende} stehen Telefon-Nummern, wo du Hilfe bekommst.</p>
</section>""")


def hilfe():
    nummern = [
        ("Telefonseelsorge", "0800 111 0 111 oder 0800 111 0 222", "kostenlos, rund um die Uhr"),
        ("Nummer gegen Kummer (für Kinder und Jugendliche)", "116 111", "kostenlos"),
        ("Elterntelefon", "0800 111 0 550", "kostenlos"),
        ("Hilfetelefon Gewalt gegen Frauen", "116 016", "kostenlos, rund um die Uhr"),
        ("Hilfetelefon Gewalt an Männern", "0800 123 99 00", "kostenlos"),
        ("Hilfetelefon Sexueller Missbrauch", "0800 22 55 530", "kostenlos"),
        ("Polizei", "110", "im Notfall"),
        ("Rettungsdienst und Feuerwehr", "112", "im Notfall"),
    ]
    zeilen = "\n".join(
        f'<div class="nummer"><p class="n-name">{esc(a)}</p><p class="n-tel">{esc(b)}</p><p class="n-info">{esc(c)}</p></div>'
        for a, b, c in nummern)
    return seite("Hier gibt es Hilfe", f"""<section epub:type="appendix" class="hilfe">
<h2 class="seitentitel">Hier gibt es Hilfe</h2>
<div class="zier"><span></span></div>
<p class="t">Du bist nicht allein.</p>
<p class="t">Wenn es dir schlecht geht, darfst du dir Hilfe holen.</p>
<p class="t">Diese Nummern gelten in Deutschland.</p>
{zeilen}
</section>""")


def teil_seite(testament, untertitel):
    name = "Das Alte Testament" if testament == "altes-testament" else "Das Neue Testament"
    return seite(name, f"""<section epub:type="part" class="teil">
<p class="kicker">Teil</p>
<h1 class="teil-titel">{esc(name)}</h1>
<div class="zier gross"><span></span></div>
<p class="teil-unter">{esc(untertitel)}</p>
</section>""", "mitte")


def buch_seite(buch, nummer_text):
    links = " ".join(
        f'<a class="kn" href="b{buch["nr"]:02d}_k{k:03d}.xhtml">{k}</a>' for k in range(1, buch["kapitel"] + 1))
    einheit = "Psalmen" if buch["code"] == "PSA" else ("Kapitel" if buch["kapitel"] > 1 else "Kapitel")
    anzahl = f'{buch["kapitel"]} {einheit}'
    return seite(buch["name"], f"""<section epub:type="chapter" class="buchseite" id="buch">
<p class="kicker">{esc(nummer_text)}</p>
<h1 class="buch-titel">{ziffern(esc(buch["name"]))}</h1>
<div class="zier gross"><span></span></div>
<p class="buch-anzahl">{esc(anzahl)}</p>
<nav class="kapitelraster" aria-label="Kapitel">
{links}
</nav>
</section>""")


def inhalt_seite(buecher):
    teile = ['<section epub:type="toc" class="inhalt">', '<h2 class="seitentitel">Inhalt</h2>', '<div class="zier"><span></span></div>',
             '<p class="inh-teil"><a href="vorwort.xhtml">So liest du dieses Buch</a></p>']
    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            name = "Das Alte Testament" if letzter == "altes-testament" else "Das Neue Testament"
            teile.append(f'<h3 class="inh-testament">{name}</h3>')
        teile.append(f'<p class="inh-buch"><a href="b{b["nr"]:02d}_buch.xhtml">{ziffern(esc(b["name"]))}</a></p>')
    teile.append('<p class="inh-teil"><a href="hilfe.xhtml">Hier gibt es Hilfe</a></p>')
    teile.append("</section>")
    return seite("Inhalt", "\n".join(teile))


def nav_xhtml(a, buecher):
    z = ['<nav epub:type="toc" id="toc"><h1>Inhalt</h1><ol>',
         '<li><a href="text/titel.xhtml">Titel</a></li>',
         '<li><a href="text/inhalt.xhtml">Inhalt</a></li>',
         '<li><a href="text/vorwort.xhtml">So liest du dieses Buch</a></li>']
    letzter = None
    offen = False
    for b in buecher:
        if b["testament"] != letzter:
            if offen:
                z.append("</ol></li>")
            letzter = b["testament"]
            name = "Das Alte Testament" if letzter == "altes-testament" else "Das Neue Testament"
            kurz = "at" if letzter == "altes-testament" else "nt"
            z.append(f'<li><a href="text/teil_{kurz}.xhtml">{name}</a><ol>')
            offen = True
        kap = "".join(
            f'<li><a href="text/b{b["nr"]:02d}_k{k:03d}.xhtml">{("Psalm " if b["code"] == "PSA" else "Kapitel ")}{k}</a></li>'
            for k in range(1, b["kapitel"] + 1))
        z.append(f'<li><a href="text/b{b["nr"]:02d}_buch.xhtml">{esc(b["name"])}</a><ol>{kap}</ol></li>')
    if offen:
        z.append("</ol></li>")
    z.append('<li><a href="text/hilfe.xhtml">Hier gibt es Hilfe</a></li>')
    z.append('<li><a href="text/impressum.xhtml">Impressum</a></li>')
    z.append("</ol></nav>")
    z.append('<nav epub:type="landmarks" id="landmarks" hidden=""><h1>Orientierung</h1><ol>'
             '<li><a epub:type="toc" href="text/inhalt.xhtml">Inhalt</a></li>'
             f'<li><a epub:type="bodymatter" href="text/b{buecher[0]["nr"]:02d}_k001.xhtml">Beginn</a></li>'
             "</ol></nav>")
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de" lang="de">
<head><meta charset="utf-8"/><title>Inhalt</title></head>
<body>
{"".join(z)}
</body>
</html>
"""


def ncx(a, buecher, uid):
    punkte = []
    n = 0

    def punkt(text, src, kinder=""):
        nonlocal n
        n += 1
        return f'<navPoint id="np{n}" playOrder="{n}"><navLabel><text>{esc(text)}</text></navLabel><content src="{src}"/>{kinder}</navPoint>'

    punkte.append(punkt("Inhalt", "text/inhalt.xhtml"))
    punkte.append(punkt("So liest du dieses Buch", "text/vorwort.xhtml"))
    for b in buecher:
        n0 = n
        kopf = punkt(b["name"], f'text/b{b["nr"]:02d}_buch.xhtml')
        punkte.append(kopf)
    punkte.append(punkt("Hier gibt es Hilfe", "text/hilfe.xhtml"))
    return f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="de">
<head><meta name="dtb:uid" content="urn:uuid:{uid}"/><meta name="dtb:depth" content="1"/><meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>
<docTitle><text>{esc(a["titel"])}</text></docTitle>
<navMap>{"".join(punkte)}</navMap>
</ncx>
"""


# ---------- EPUB zusammensetzen ----------

def baue(schluessel):
    a = AUSGABEN[schluessel]
    alle = json.load(open(os.path.join(WURZEL, "daten", "buecher.json"), encoding="utf-8"))
    buecher = [b for b in alle if b["nr"] in a["buecher"]]
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, "bibel-leichte-sprache/" + schluessel))
    dateien = []  # (pfad_im_epub, inhalt_bytes, media_type, id, properties, in_spine)

    def neu(pfad, inhalt, typ, id_, props="", spine=True):
        if isinstance(inhalt, str):
            inhalt = inhalt.encode("utf-8")
        dateien.append((pfad, inhalt, typ, id_, props, spine))

    css = open(os.path.join(HIER, "bibel.css"), encoding="utf-8").read()
    neu("css/bibel.css", css, "text/css", "css", spine=False)
    for datei, *_ in SCHRIFTEN:
        neu(f"fonts/{datei}", open(os.path.join(HIER, "schriften", datei), "rb").read(),
            "font/ttf", "f-" + datei.replace(".", "-"), spine=False)
    cover = os.path.join(ZIEL, f"{a['datei']}-cover.jpg")
    if os.path.exists(cover):
        neu("bilder/cover.jpg", open(cover, "rb").read(), "image/jpeg", "cover-image", "cover-image", spine=False)

    neu("text/titel.xhtml", titelseite(a), "application/xhtml+xml", "titel")
    neu("text/inhalt.xhtml", inhalt_seite(buecher), "application/xhtml+xml", "inhalt")
    neu("text/vorwort.xhtml", vorwort(schluessel == "gesamt"), "application/xhtml+xml", "vorwort")

    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            kurz = "at" if letzter == "altes-testament" else "nt"
            at_buecher = [x for x in alle if x["testament"] == letzter]
            if len(buecher) > 30 or schluessel in ("gesamt", "band-4"):
                unter = f'{len(at_buecher)} Bücher'
            else:
                unter = f'Die Bücher von {buecher[0]["name"]} bis {buecher[-1]["name"]}'
            neu(f"text/teil_{kurz}.xhtml", teil_seite(letzter, unter), "application/xhtml+xml", f"teil-{kurz}")
        tname = "Altes Testament" if b["testament"] == "altes-testament" else "Neues Testament"
        neu(f'text/b{b["nr"]:02d}_buch.xhtml', buch_seite(b, f'{tname} · Buch {b["nr"]} von 66'),
            "application/xhtml+xml", f'b{b["nr"]:02d}')
        for k in range(1, b["kapitel"] + 1):
            md = open(os.path.join(WURZEL, "texte", "leichte-sprache", b["testament"], b["ordner"], f"kapitel_{k:03d}.md"),
                      encoding="utf-8").read()
            kopf = f'Psalm {k}' if b["code"] == "PSA" else f'{b["name"]} {k}'
            neu(f'text/b{b["nr"]:02d}_k{k:03d}.xhtml',
                seite(kopf, f'<section epub:type="chapter" class="kapitel">\n{kapitel_html(md, b, k)}\n</section>'),
                "application/xhtml+xml", f'b{b["nr"]:02d}k{k:03d}')

    neu("text/hilfe.xhtml", hilfe(), "application/xhtml+xml", "hilfe")
    neu("text/impressum.xhtml", impressum(a), "application/xhtml+xml", "impressum")
    neu("nav.xhtml", nav_xhtml(a, buecher), "application/xhtml+xml", "nav", "nav", spine=False)
    neu("toc.ncx", ncx(a, buecher, uid), "application/x-dtbncx+xml", "ncx", spine=False)

    jetzt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = "\n".join(
        f'<item id="{i}" href="{p}" media-type="{t}"' + (f' properties="{pr}"' if pr else "") + "/>"
        for p, _, t, i, pr, _ in dateien)
    spine = "\n".join(f'<itemref idref="{i}"/>' for p, _, t, i, pr, s in dateien if s)
    creator = f"<dc:creator>{esc(HERAUSGEBER)}</dc:creator>" if HERAUSGEBER else ""
    beschreibung = ("Die ganze Bibel in Leichter Sprache: kurze Sätze, klare Worte. "
                    "Kein Vers ist weggelassen. Nach jedem Abschnitt erklärt ein Kasten: Was bedeutet das?")
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="de">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">urn:uuid:{uid}</dc:identifier>
<dc:title id="t1">{esc(a["titel"])}</dc:title>
<meta refines="#t1" property="title-type">main</meta>
<dc:title id="t2">{esc(a["untertitel"])}</dc:title>
<meta refines="#t2" property="title-type">subtitle</meta>
{creator}
<dc:language>de</dc:language>
<dc:subject>Bibel</dc:subject>
<dc:subject>Leichte Sprache</dc:subject>
<dc:description>{esc(beschreibung)}</dc:description>
<meta property="dcterms:modified">{jetzt}</meta>
<meta name="cover" content="cover-image"/>
</metadata>
<manifest>
{manifest}
</manifest>
<spine toc="ncx">
{spine}
</spine>
</package>
"""
    os.makedirs(ZIEL, exist_ok=True)
    ziel = os.path.join(ZIEL, a["datei"] + ".epub")
    with zipfile.ZipFile(ziel, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>""", compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        for p, inhalt, *_ in dateien:
            z.writestr("OEBPS/" + p, inhalt, compress_type=zipfile.ZIP_DEFLATED)
    kap = sum(b["kapitel"] for b in buecher)
    print(f"{os.path.relpath(ziel, WURZEL)}: {len(buecher)} Bücher, {kap} Kapitel, {os.path.getsize(ziel) / 1e6:.1f} MB")


if __name__ == "__main__":
    wahl = sys.argv[1:] or list(AUSGABEN)
    for s in wahl:
        baue(s)
