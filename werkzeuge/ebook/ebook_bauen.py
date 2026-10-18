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
HERAUSGEBER = "Andreas Rupp"
JAHR = "2026"

# Sprache der Ausgabe: "de" (Die Bibel in Leichter Sprache) oder "en" (The Bible in Plain Language).
# Umschalten mit der Umgebungsvariablen BIBEL_SPRACHE=en.
SPRACHE = os.environ.get("BIBEL_SPRACHE", "de")
EN = SPRACHE == "en"
QUELLE = os.path.join(WURZEL, "texte", "plain-english" if EN else "leichte-sprache")
if EN:
    ZIEL = os.path.join(WURZEL, "ausgabe", "english", "ebook")


def bn(b):
    """Name eines Buches in der Sprache der Ausgabe."""
    return b["name_englisch"] if EN else b["name"]


def tn(testament, art="kurz"):
    """Name des Testaments: kurz = „Altes Testament“, lang = „Das Alte Testament“."""
    at = testament == "altes-testament"
    if EN:
        return ("Old Testament" if at else "New Testament") if art == "kurz" else ("The Old Testament" if at else "The New Testament")
    return ("Altes Testament" if at else "Neues Testament") if art == "kurz" else ("Das Alte Testament" if at else "Das Neue Testament")


T = {
    "de": dict(lang="de", kapitel="Kapitel", psalm="Psalm", psalmen="Psalmen", einf="Bevor es losgeht", rueck="Rückblick",
               vers="Vers", hinweis=("wichtiger hinweis", "ein wichtiger hinweis"), titel_h1="Die Bibel", titel_unter="in Leichter Sprache",
               zusatz="Mit Erklärungen zu jedem Abschnitt", hg="Herausgegeben von", impressum="Impressum", inhalt="Inhalt",
               vorwort="So liest du dieses Buch", hilfe="Hier gibt es Hilfe", teil="Teil", buecher="Bücher",
               buch_von="Buch {n} von 66", von_bis="Die Bücher von {a} bis {b}", titel="Titel", beginn="Beginn",
               orientierung="Orientierung", stand="Stand"),
    "en": dict(lang="en", kapitel="Chapter", psalm="Psalm", psalmen="psalms", einf="Before we begin", rueck="Looking back",
               vers="Verse", hinweis=("important note",), titel_h1="The Bible", titel_unter="in Plain Language",
               zusatz="With an explanation for every section", hg="Edited by", impressum="Copyright", inhalt="Contents",
               vorwort="How to read this book", hilfe="Help is available", teil="Part", buecher="books",
               buch_von="Book {n} of 66", von_bis="The books from {a} to {b}", titel="Title", beginn="Start",
               orientierung="Landmarks", stand="Version"),
}[SPRACHE]

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

if EN:
    _baende = [("band-1", "Volume 1", "Old Testament", "Genesis to 1 Samuel", range(1, 10)),
               ("band-2", "Volume 2", "Old Testament", "2 Samuel to Psalms", range(10, 20)),
               ("band-3", "Volume 3", "Old Testament", "Proverbs to Malachi", range(20, 40)),
               ("band-4", "Volume 4", "New Testament", "Matthew to Revelation", range(40, 67))]
    AUSGABEN = {"gesamt": {"datei": "bible-plain-language-complete", "titel": "The Bible in Plain Language",
                           "untertitel": "Complete Edition – Old and New Testament", "band": "Complete Edition",
                           "oben": "Old and New Testament", "buecher": range(1, 67)}}
    for k, band, oben, zeile, r_ in _baende:
        AUSGABEN[k] = {"datei": f"bible-plain-language-{k.replace('band', 'volume')}", "titel": "The Bible in Plain Language",
                       "untertitel": f"{band} – {'The New Testament' if oben == 'New Testament' else oben + ': ' + zeile}",
                       "band": band, "oben": oben, "buecher": r_}

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
    kopf_nr = f"{T['psalm']} {kap}" if psalm else f"{T['kapitel']} {kap}"
    out = [
        '<header class="kapkopf">',
        f'<p class="kicker">{esc(bn(buch))}</p>',
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
        if kopf.lower().startswith(T["hinweis"]):
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
            intro = h.startswith(T["einf"]) or h.startswith(T["rueck"])
            m = re.match(r"^(.*?)\s*\((" + T["vers"] + r"[^)]*)\)\s*$", h)
            klasse = "abschnitt"
            if h.startswith(T["einf"]):
                klasse = "abschnitt einf"
            elif h.startswith(T["rueck"]):
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
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{T['lang']}" lang="{T['lang']}">
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
<h1 class="ts-titel">{T["titel_h1"]}</h1>
<p class="ts-unter">{T["titel_unter"]}</p>
<div class="zier gross"><span></span></div>
<p class="ts-band">{esc(a["untertitel"])}</p>
<p class="ts-zusatz">{T["zusatz"]}</p>
{f'<p class="ts-hg">{T["hg"]} {esc(HERAUSGEBER)}</p>' if HERAUSGEBER else ""}
</section>""", "mitte")


def impressum_en(a):
    heute = datetime.date.today().isoformat()
    hg = f"<p>Edited by {esc(HERAUSGEBER)}.</p>\n" if HERAUSGEBER else ""
    return seite("Copyright", f"""<section epub:type="copyright-page" class="impressum">
<h2 class="klein">Copyright</h2>
<p><strong>{esc(a["titel"])}</strong><br/>{esc(a["untertitel"])}</p>
{hg}<p>English plain-language edition, {JAHR}.</p>
<p><strong>Source:</strong> This edition was newly written from the World English Bible (WEB). The World English Bible is in the public domain. No text was taken from any copyrighted Bible translation.</p>
<p>“World English Bible” is a trademark of eBible.org. The name is used here only to identify the source. This book is not an edition of the World English Bible and is not published by eBible.org.</p>
<p><strong>Plain language:</strong> This edition follows the principles of plain language. It has not been tested by a reader panel and carries no certification.</p>
<p><strong>Fonts:</strong> Cinzel, Literata and Inter, all under the SIL Open Font License 1.1.</p>
<p class="stand">Version: {heute}</p>
</section>""")


def impressum(a):
    if EN:
        return impressum_en(a)
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


def vorwort_en(ganz=True):
    inhalt = ("This book tells the whole Bible in plain language." if ganz else
              "This series tells the whole Bible in plain language, in 4 volumes.")
    ende = "At the end of this book" if ganz else "At the end of every volume"
    return seite("How to read this book", f"""<section epub:type="preface" class="vorwort">
<h2 class="seitentitel">How to read this book</h2>
<div class="zier"><span></span></div>
<p class="t">The Bible is the most important book in the world.</p>
<p class="t">It is old. But its message is still true today.</p>
<p class="t">{inhalt}</p>
<p class="t">No verse is left out. No name and no number.</p>
<h3 class="abschnitt">Short sentences</h3>
<p class="t">Every line is one short thought.</p>
<p class="t">So you can read in peace.</p>
<h3 class="abschnitt">The numbers</h3>
<p class="v"><span class="vn">1</span>The small numbers are the verse numbers.<br/>With them you can find every passage.<br/>Just like in every other Bible.</p>
<h3 class="abschnitt">The boxes</h3>
<aside class="box erkl"><p class="boxkopf">What does this mean?</p><p>After every section there is a box like this.</p><p>It explains what you have read.</p><p>And what it can mean for us today.</p></aside>
<aside class="box hinweis"><p class="boxkopf">Important note</p><p>Some passages in the Bible are hard.</p><p>They have also been misused, for example against Jews, against women, or to justify violence.</p><p>At such passages you will find a note like this.</p></aside>
<h3 class="abschnitt">The Psalms</h3>
<p class="t">Some Bibles number the Psalms differently.</p>
<p class="t">Then the other number is given in brackets.</p>
<h3 class="abschnitt">Help</h3>
<p class="t">The Bible also tells of suffering and violence.</p>
<p class="t">If something weighs on you: {ende} you will find phone numbers where you can get help.</p>
</section>""")


def vorwort(ganz=True):
    """ganz=False: für einen Band der Reihe (nicht die Gesamtausgabe)."""
    if EN:
        return vorwort_en(ganz)
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
    if EN:
        nummern = [
            ("988 Suicide & Crisis Lifeline (USA)", "Call or text 988", "free, 24 hours a day"),
            ("Childhelp National Child Abuse Hotline (USA)", "1-800-422-4453", "free, 24 hours a day"),
            ("National Domestic Violence Hotline (USA)", "1-800-799-7233", "free, 24 hours a day"),
            ("RAINN Sexual Assault Hotline (USA)", "1-800-656-4673", "free, 24 hours a day"),
            ("Samaritans (UK and Ireland)", "116 123", "free, 24 hours a day"),
            ("Childline (UK, for children and young people)", "0800 1111", "free"),
            ("Other countries", "findahelpline.com", "free help lines worldwide"),
            ("Emergency", "911 (USA) · 999 (UK) · 112 (Europe)", "police, ambulance, fire"),
        ]
        zeilen = "\n".join(
            f'<div class="nummer"><p class="n-name">{esc(a)}</p><p class="n-tel">{esc(b)}</p><p class="n-info">{esc(c)}</p></div>'
            for a, b, c in nummern)
        return seite("Help is available", f"""<section epub:type="appendix" class="hilfe">
<h2 class="seitentitel">Help is available</h2>
<div class="zier"><span></span></div>
<p class="t">You are not alone.</p>
<p class="t">If you are not doing well, it is okay to ask for help.</p>
{zeilen}
</section>""")
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
    name = tn(testament, "lang")
    return seite(name, f"""<section epub:type="part" class="teil">
<p class="kicker">{T["teil"]}</p>
<h1 class="teil-titel">{esc(name)}</h1>
<div class="zier gross"><span></span></div>
<p class="teil-unter">{esc(untertitel)}</p>
</section>""", "mitte")


def buch_seite(buch, nummer_text):
    links = " ".join(
        f'<a class="kn" href="b{buch["nr"]:02d}_k{k:03d}.xhtml">{k}</a>' for k in range(1, buch["kapitel"] + 1))
    if EN:
        einheit = "psalms" if buch["code"] == "PSA" else ("chapters" if buch["kapitel"] > 1 else "chapter")
    else:
        einheit = "Psalmen" if buch["code"] == "PSA" else "Kapitel"
    anzahl = f'{buch["kapitel"]} {einheit}'
    return seite(bn(buch), f"""<section epub:type="chapter" class="buchseite" id="buch">
<p class="kicker">{esc(nummer_text)}</p>
<h1 class="buch-titel">{ziffern(esc(bn(buch)))}</h1>
<div class="zier gross"><span></span></div>
<p class="buch-anzahl">{esc(anzahl)}</p>
<nav class="kapitelraster" aria-label="{T['kapitel']}">
{links}
</nav>
</section>""")


def inhalt_seite(buecher):
    teile = ['<section epub:type="toc" class="inhalt">', f'<h2 class="seitentitel">{T["inhalt"]}</h2>', '<div class="zier"><span></span></div>',
             f'<p class="inh-teil"><a href="vorwort.xhtml">{T["vorwort"]}</a></p>']
    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            teile.append(f'<h3 class="inh-testament">{tn(letzter, "lang")}</h3>')
        teile.append(f'<p class="inh-buch"><a href="b{b["nr"]:02d}_buch.xhtml">{ziffern(esc(bn(b)))}</a></p>')
    teile.append(f'<p class="inh-teil"><a href="hilfe.xhtml">{T["hilfe"]}</a></p>')
    teile.append("</section>")
    return seite(T["inhalt"], "\n".join(teile))


def nav_xhtml(a, buecher):
    z = [f'<nav epub:type="toc" id="toc"><h1>{T["inhalt"]}</h1><ol>',
         f'<li><a href="text/titel.xhtml">{T["titel"]}</a></li>',
         f'<li><a href="text/inhalt.xhtml">{T["inhalt"]}</a></li>',
         f'<li><a href="text/vorwort.xhtml">{T["vorwort"]}</a></li>']
    letzter = None
    offen = False
    for b in buecher:
        if b["testament"] != letzter:
            if offen:
                z.append("</ol></li>")
            letzter = b["testament"]
            name = tn(letzter, "lang")
            kurz = "at" if letzter == "altes-testament" else "nt"
            z.append(f'<li><a href="text/teil_{kurz}.xhtml">{name}</a><ol>')
            offen = True
        kap = "".join(
            f'<li><a href="text/b{b["nr"]:02d}_k{k:03d}.xhtml">{(T["psalm"] if b["code"] == "PSA" else T["kapitel"])} {k}</a></li>'
            for k in range(1, b["kapitel"] + 1))
        z.append(f'<li><a href="text/b{b["nr"]:02d}_buch.xhtml">{esc(bn(b))}</a><ol>{kap}</ol></li>')
    if offen:
        z.append("</ol></li>")
    z.append(f'<li><a href="text/hilfe.xhtml">{T["hilfe"]}</a></li>')
    z.append(f'<li><a href="text/impressum.xhtml">{T["impressum"]}</a></li>')
    z.append("</ol></nav>")
    z.append(f'<nav epub:type="landmarks" id="landmarks" hidden=""><h1>{T["orientierung"]}</h1><ol>'
             f'<li><a epub:type="toc" href="text/inhalt.xhtml">{T["inhalt"]}</a></li>'
             f'<li><a epub:type="bodymatter" href="text/b{buecher[0]["nr"]:02d}_k001.xhtml">{T["beginn"]}</a></li>'
             "</ol></nav>")
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{T['lang']}" lang="{T['lang']}">
<head><meta charset="utf-8"/><title>{T["inhalt"]}</title></head>
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

    punkte.append(punkt(T["inhalt"], "text/inhalt.xhtml"))
    punkte.append(punkt(T["vorwort"], "text/vorwort.xhtml"))
    for b in buecher:
        n0 = n
        kopf = punkt(bn(b), f'text/b{b["nr"]:02d}_buch.xhtml')
        punkte.append(kopf)
    punkte.append(punkt(T["hilfe"], "text/hilfe.xhtml"))
    return f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="{T['lang']}">
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
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, ("bible-plain-language/" if EN else "bibel-leichte-sprache/") + schluessel))
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
                unter = f'{len(at_buecher)} {T["buecher"]}'
            else:
                unter = T["von_bis"].format(a=bn(buecher[0]), b=bn(buecher[-1]))
            neu(f"text/teil_{kurz}.xhtml", teil_seite(letzter, unter), "application/xhtml+xml", f"teil-{kurz}")
        neu(f'text/b{b["nr"]:02d}_buch.xhtml', buch_seite(b, f'{tn(b["testament"])} · {T["buch_von"].format(n=b["nr"])}'),
            "application/xhtml+xml", f'b{b["nr"]:02d}')
        for k in range(1, b["kapitel"] + 1):
            md = open(os.path.join(QUELLE, b["testament"], b["ordner"], f"kapitel_{k:03d}.md"),
                      encoding="utf-8").read()
            kopf = f'Psalm {k}' if b["code"] == "PSA" else f'{bn(b)} {k}'
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
    creator = (f'<dc:creator id="hg">{esc(HERAUSGEBER)}</dc:creator>\n'
               '<meta refines="#hg" property="role" scheme="marc:relators">edt</meta>') if HERAUSGEBER else ""
    beschreibung = ("The whole Bible in plain language: short sentences, clear words. No verse is left out. "
                    "After every section a box explains: What does this mean?") if EN else (
                    "Die ganze Bibel in Leichter Sprache: kurze Sätze, klare Worte. "
                    "Kein Vers ist weggelassen. Nach jedem Abschnitt erklärt ein Kasten: Was bedeutet das?")
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="{T['lang']}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">urn:uuid:{uid}</dc:identifier>
<dc:title id="t1">{esc(a["titel"])}</dc:title>
<meta refines="#t1" property="title-type">main</meta>
<dc:title id="t2">{esc(a["untertitel"])}</dc:title>
<meta refines="#t2" property="title-type">subtitle</meta>
{creator}
<dc:language>{T['lang']}</dc:language>
<dc:subject>{"Bible" if EN else "Bibel"}</dc:subject>
<dc:subject>{"Plain language" if EN else "Leichte Sprache"}</dc:subject>
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
    print(f"{os.path.relpath(ziel, WURZEL)}: {len(buecher)} {T['buecher']}, {kap} {T['kapitel']}, {os.path.getsize(ziel) / 1e6:.1f} MB")


if __name__ == "__main__":
    wahl = sys.argv[1:] or list(AUSGABEN)
    for s in wahl:
        baue(s)
