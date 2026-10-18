"""Baut druckfertige PDFs (Innenteil + Umschlag) für Amazon KDP Print.

Aufruf (im Hauptordner des Projekts):
    python3 werkzeuge/druck/druck_bauen.py            # alle Bände
    python3 werkzeuge/druck/druck_bauen.py band-1     # nur einen Band

Ablauf je Band:
    1. HTML für den Innenteil schreiben (Platzhalter im Inhaltsverzeichnis).
    2. Chromium druckt das HTML als PDF (werkzeuge/druck/pdf_drucken.mjs).
    3. Seitenzahlen der Bücher aus dem PDF lesen, Inhaltsverzeichnis füllen, nochmal drucken.
    4. Umschläge (Vorderseite, Rücken, Rückseite) passend zur Seitenzahl als PDF bauen:
       einen für das Taschenbuch und einen für die gebundene Ausgabe (Hardcover).

Format: 8,25 x 11 Zoll (20,96 x 27,94 cm), zweispaltig, Schrift 9,2 pt, ohne Beschnitt im Innenteil.
KDP erlaubt bei gebundenen Büchern höchstens 550 Seiten, darum gibt es 4 Bände.
"""
import html, json, os, re, subprocess, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(WURZEL, "werkzeuge", "ebook"))
import ebook_bauen as eb  # noqa: E402

EN = eb.EN
T = eb.T
bn, tn = eb.bn, eb.tn
ZIEL = os.path.join(WURZEL, "ausgabe", "english", "print") if EN else os.path.join(WURZEL, "ausgabe", "druck")
SCHRIFTEN = os.path.join(WURZEL, "werkzeuge", "ebook", "schriften")
JAHR = eb.JAHR

# Seitenbreite/-höhe in Zoll
BREITE, HOEHE = 8.25, 11.0
PAPIER_DICKE = 0.002252  # Zoll pro Seite, KDP weißes Papier, Schwarzweiß
BESCHNITT = 0.125
MAX_SEITEN = 550  # KDP Hardcover

# Hardcover-Umschlag nach KDP-Vorlage (Zoll): Einschlag rundum, Falz neben dem Rücken,
# Rücken = Papier + Pappe. Vor dem Hochladen mit dem KDP-Cover-Rechner vergleichen.
HC_EINSCHLAG_SEITE = 0.591
HC_EINSCHLAG_OBEN = 0.709
HC_FALZ = 0.197
HC_PAPPE = 0.189

# Die Bände für den Druck. Grenzen so gewählt, dass jeder Band unter 550 Seiten bleibt.
BAENDE = json.load(open(os.path.join(HIER, "baende_en.json" if EN else "baende.json"), encoding="utf-8"))

esc = eb.esc
ziffern = eb.ziffern


def lade_buecher():
    return json.load(open(os.path.join(WURZEL, "daten", "buecher.json"), encoding="utf-8"))


def kapitel_md(b, k):
    return open(os.path.join(eb.QUELLE, b["testament"], b["ordner"], f"kapitel_{k:03d}.md"),
                encoding="utf-8").read()


def font_css():
    regeln = []
    for datei, fam, gew, stil in eb.SCHRIFTEN:
        regeln.append(f'@font-face {{ font-family: "{fam}"; font-weight: {gew}; font-style: {stil}; '
                      f'src: url("file://{os.path.join(SCHRIFTEN, datei)}"); }}')
    return "\n".join(regeln)


def innenteil_html(band, alle, seiten_der_buecher=None, marken=True, leer=()):
    buecher = [b for b in alle if band["von"] <= b["nr"] <= band["bis"]]
    css = open(os.path.join(HIER, "druck.css"), encoding="utf-8").read()

    teile = []
    # Titelei
    teile.append(f"""<section class="titelei schmutztitel"><p class="st-titel">{T["titel_h1"]}</p><p class="st-unter">{T["titel_unter"]}</p></section>
<section class="titelei leerseite"></section>
<section class="titelei titelseite">
<p class="ts-oben">{esc(band["oben"])}</p>
<h1 class="ts-titel">{T["titel_h1"]}</h1>
<p class="ts-unter">{T["titel_unter"]}</p>
<div class="zier gross"><span></span></div>
<p class="ts-band">{esc(band["titel"])}</p>
<p class="ts-zusatz">{esc(band["zeile"])}</p>
<p class="ts-zusatz2">{T["zusatz"]}</p>
{f'<p class="ts-hg">{T["hg"]} {esc(eb.HERAUSGEBER)}</p>' if eb.HERAUSGEBER else ""}
</section>""")
    hg = f"<p>{T['hg']} {esc(eb.HERAUSGEBER)}.</p>" if eb.HERAUSGEBER else ""
    if EN:
        teile.append(f"""<section class="titelei impressum">
<p><strong>The Bible in Plain Language</strong><br/>{esc(band["titel"])}: {esc(band["zeile"])}</p>
{hg}<p>English plain-language edition, {JAHR}.</p>
<p><strong>Source:</strong> This edition was newly written from the World English Bible (WEB). The World English Bible is in the public domain. No text was taken from any copyrighted Bible translation.</p>
<p>“World English Bible” is a trademark of eBible.org. The name is used here only to identify the source. This book is not an edition of the World English Bible and is not published by eBible.org.</p>
<p><strong>Plain language:</strong> This edition follows the principles of plain language. It has not been tested by a reader panel and carries no certification.</p>
<p><strong>Fonts:</strong> Cinzel, Literata and Inter inside, Anton on the cover, all under the SIL Open Font License 1.1.</p>
<p><strong>The volumes of this edition:</strong><br/>{"<br/>".join(esc(x["titel"] + ": " + x["zeile"]) for x in BAENDE)}</p>
</section>""")
    else:
        teile.append(f"""<section class="titelei impressum">
<p><strong>Die Bibel in Leichter Sprache</strong><br/>{esc(band["titel"])}: {esc(band["zeile"])}</p>
{hg}<p>Deutsche Übertragung in Leichte Sprache, {JAHR}.</p>
<p><strong>Grundlage:</strong> Diese Übertragung wurde neu aus der englischen World English Bible (WEB) erstellt. Die World English Bible ist gemeinfrei (Public Domain). Es wurde kein Text aus einer urheberrechtlich geschützten deutschen Bibelübersetzung übernommen.</p>
<p>Der Name „World English Bible“ ist eine geschützte Marke von eBible.org. Er wird hier nur genannt, um die Quelle anzugeben. Dieses Buch ist keine Ausgabe der World English Bible und wird nicht von eBible.org herausgegeben.</p>
<p><strong>Leichte Sprache:</strong> Die Übertragung orientiert sich an den Regeln für Leichte Sprache. Sie wurde nicht von einer Prüfgruppe geprüft und trägt kein Prüfsiegel.</p>
<p><strong>Schriften:</strong> Cinzel, Literata und Inter im Innenteil, Anton auf dem Umschlag, alle unter der SIL Open Font License 1.1.</p>
<p><strong>Die Bände dieser Ausgabe:</strong><br/>{"<br/>".join(esc(x["titel"] + ": " + x["zeile"]) for x in BAENDE)}</p>
</section>""")
    # Vorwort aus dem E-Book übernehmen (ohne Seitenrahmen)
    vw = re.search(r"<section.*?</section>", eb.vorwort(False), re.S).group(0)
    vw = vw.replace('class="vorwort"', 'class="titelei vorwort"').replace("<h2", '<p class="marke">@@VORWORT@@</p><h2', 1)
    teile.append(vw)
    # Inhaltsverzeichnis
    z = [f'<section class="titelei inhalt"><p class="marke">@@INHALT@@</p><h2 class="seitentitel">{T["inhalt"]}</h2><div class="zier"><span></span></div>']
    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            z.append(f'<p class="inh-testament">{tn(letzter, "lang")}</p>')
        s = seiten_der_buecher.get(f'BUCH{b["nr"]:02d}', "") if seiten_der_buecher else "000"
        z.append(f'<p class="inh-zeile"><span class="inh-name">{ziffern(esc(bn(b)))}</span><span class="inh-seite">{s}</span></p>')
    s = seiten_der_buecher.get("HILFE", "") if seiten_der_buecher else "000"
    z.append(f'<p class="inh-zeile inh-extra"><span class="inh-name">{T["hilfe"]}</span><span class="inh-seite">{s}</span></p>')
    z.append("</section>")
    teile.append("\n".join(z))

    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            name = tn(letzter, "lang")
            anzahl = sum(1 for x in alle if x["testament"] == letzter)
            kurz = "TEILAT" if letzter == "altes-testament" else "TEILNT"
            teile.append(f"""<section class="teil"><p class="marke">@@{kurz}@@</p><p class="kicker">{T["teil"]}</p><h1 class="teil-titel">{name}</h1>
<div class="zier gross"><span></span></div><p class="teil-unter">{anzahl} {T["buecher"]}</p></section>""")
        if EN:
            einheit = "psalms" if b["code"] == "PSA" else ("chapters" if b["kapitel"] > 1 else "chapter")
        else:
            einheit = "Psalmen" if b["code"] == "PSA" else "Kapitel"
        teile.append(f"""<section class="buchseite"><p class="marke">@@BUCH{b["nr"]:02d}@@</p>
<p class="kicker">{tn(b["testament"])} · {T["buch_von"].format(n=b["nr"])}</p>
<h1 class="buch-titel">{ziffern(esc(bn(b)))}</h1>
<div class="zier gross"><span></span></div>
<p class="buch-anzahl">{b["kapitel"]} {einheit}</p></section>""")
        kap = []
        for k in range(1, b["kapitel"] + 1):
            inhalt = eb.kapitel_html(kapitel_md(b, k), b, k).replace(
                '<header class="kapkopf">', f'<header class="kapkopf"><p class="marke">@@K{b["nr"]:02d}{k:03d}@@</p>', 1)
            kap.append(f'<article class="kapitel">{inhalt}</article>')
        teile.append(f'<section class="buchtext buch-{b["nr"]:02d}">' + "\n".join(kap) + "</section>")

    hilfe = re.search(r"<section.*?</section>", eb.hilfe(), re.S).group(0)
    hilfe = hilfe.replace('class="hilfe"', 'class="titelei hilfe"').replace("<h2", '<p class="marke">@@HILFE@@</p><h2', 1)
    teile.append(hilfe)

    doc = f"""<!doctype html>
<html lang="{T['lang']}"><head><meta charset="utf-8"/><title>{T["titel_h1"]} {T["titel_unter"]} – {esc(band["titel"])}</title>
<style>
{font_css()}
{css}
</style></head>
<body>
{chr(10).join(teile)}
</body></html>
"""
    # Leere linke Seiten, damit Vorwort, Inhalt, Teile, Bücher und Hilfe rechts beginnen.
    # (Chromium beachtet break-before: right nicht.)
    for m in leer:
        i = doc.index(f'<p class="marke">@@{m}@@</p>')
        i = doc.rindex("<section", 0, i)
        doc = doc[:i] + '<section class="titelei leerseite"></section>\n' + doc[i:]
    if not marken:
        # Marken sind absolut positioniert: Entfernen ändert den Umbruch nicht.
        doc = re.sub(r'<p class="marke">@@[A-Z0-9]+@@</p>', "", doc)
    return doc


def drucke(html_datei, pdf_datei, breite, hoehe):
    subprocess.run(["node", os.path.join(HIER, "pdf_drucken.mjs"), html_datei, pdf_datei, str(breite), str(hoehe)],
                   check=True)


def seitenzahl(pdf):
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", info).group(1))


def finde_marken(pdf, mit_hoehe=False):
    """Liest aus dem PDF, auf welcher Seite jede Marke steht (Buchanfänge, Kapitel, Teile, Vorwort, Inhalt, Hilfe).
    Mit mit_hoehe=True zusätzlich die Höhe (in pt von oben), auf der die Marke steht."""
    xml = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    gefunden = {}
    for i, seite in enumerate(re.findall(r"<page .*?</page>", xml, re.S), start=1):
        woerter = re.findall(r'<word xMin="[\d.]+" yMin="([\d.]+)"[^>]*>([^<]*)</word>', seite)
        text, hoehe = "", []
        for y, w in woerter:
            w = html.unescape(w)
            text += w
            hoehe += [float(y)] * len(w)
        for m in re.finditer(r"@@([A-Z0-9]+)@@", text):
            gefunden[m.group(1)] = (i, hoehe[m.start()]) if mit_hoehe else i
    return gefunden


def leerseiten(marken):
    """Bestimmt, vor welchen Marken eine leere Seite nötig ist, damit Vorwort, Inhalt, Teile, Bücher und Hilfe
    auf einer rechten (ungeraden) Seite beginnen. Diese Marken beginnen immer eine neue Seite, eine eingefügte
    Leerseite verschiebt also nur alles danach um 1. Kapitel-Marken werden nur mitverschoben."""
    leer, neu, schub = [], {}, 0
    for m, s in sorted(marken.items(), key=lambda x: (x[1], not x[0].startswith("K"))):
        if not m.startswith("K") and (s + schub) % 2 == 0:
            leer.append(m)
            schub += 1
        neu[m] = s + schub
    return leer, neu


def kopfzeilen(pdf, marken, leer, buecher, n):
    """Setzt auf jede Textseite eine Kopfzeile mit Buch und Kapiteln, z. B. „2. SAMUEL 1–2“.
    Linke Seiten: außen links, rechte Seiten: außen rechts. marken: {name: (seite, höhe)}."""
    seite_von = {m: s for m, (s, _) in marken.items()}
    sonder = sorted({s for m, s in seite_von.items() if not m.startswith("K")} |
                    {seite_von[m] - 1 for m in leer})
    oben = 0.72 * 72 + 16  # Marke so weit oben = Kapitel beginnt ganz oben auf der Seite
    zeilen = {}
    for b in buecher:
        kap = {k: marken[f'K{b["nr"]:02d}{k:03d}'] for k in range(1, b["kapitel"] + 1)}
        start = kap[1][0]
        ende = min([s for s in sonder if s > start] + [n + 1]) - 1
        for p in range(start, ende + 1):
            hier = [k for k, (s, y) in kap.items() if s == p]
            vorher = [k for k, (s, y) in kap.items() if s < p]
            erste = hier[0] if hier and kap[hier[0]][1] < oben or not vorher else max(vorher)
            letzte = max(hier) if hier else erste
            if b["code"] == "PSA":
                name = "Psalm" if erste == letzte else ("Psalms" if EN else "Psalmen")
            else:
                name = bn(b)
            zeilen[p] = (name, f"{erste}" if erste == letzte else f"{erste}–{letzte}")
    seiten = []
    for p in range(1, n + 1):
        inhalt = ""
        if p in zeilen:
            name, kap = zeilen[p]
            inhalt = f'<div class="kopf {"links" if p % 2 == 0 else "rechts"}"><span>{esc(name)}</span><span class="k">{kap}</span></div>'
        seiten.append(f'<section class="seite">{inhalt}</section>')
    doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"/><style>
{font_css()}
@page {{ size: {BREITE}in {HOEHE}in; margin: 0; }}
html, body {{ margin: 0; }}
.seite {{ position: relative; width: {BREITE}in; height: {HOEHE}in; break-after: page; overflow: hidden; }}
.kopf {{ position: absolute; top: 0; height: 0.72in; display: flex; align-items: center; gap: 0.9em;
  font-family: "Inter", sans-serif; font-weight: 800; font-size: 7.5pt; letter-spacing: 0.22em; text-transform: uppercase; color: #000; }}
.kopf.links {{ left: 0.45in; }}
.kopf.rechts {{ right: 0.45in; flex-direction: row-reverse; }}
.kopf .k {{ letter-spacing: 0.08em; }}
</style></head><body>{"".join(seiten)}</body></html>"""
    html_datei = pdf + ".kopf.html"
    kopf_pdf = pdf + ".kopf.pdf"
    open(html_datei, "w", encoding="utf-8").write(doc)
    drucke(html_datei, kopf_pdf, BREITE, HOEHE)
    import pikepdf
    with pikepdf.open(pdf, allow_overwriting_input=True) as innen, pikepdf.open(kopf_pdf) as oben:
        if len(oben.pages) != n:
            raise SystemExit(f"Kopfzeilen: {len(oben.pages)} Seiten statt {n}")
        for p in zeilen:
            innen.pages[p - 1].add_overlay(oben.pages[p - 1])
        innen.save(pdf, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
    os.remove(html_datei)
    os.remove(kopf_pdf)
    return zeilen


def baue(band, alle):
    os.makedirs(ZIEL, exist_ok=True)
    name = band["datei"]
    html_datei = os.path.join(ZIEL, f".{name}.html")
    pdf = os.path.join(ZIEL, f"{name}-innenteil.pdf")

    buecher = [b for b in alle if band["von"] <= b["nr"] <= band["bis"]]
    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle))
    drucke(html_datei, pdf, BREITE, HOEHE)
    leer, seiten = leerseiten(finde_marken(pdf))
    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle, seiten, leer=leer))
    drucke(html_datei, pdf, BREITE, HOEHE)
    marken = finde_marken(pdf, mit_hoehe=True)
    pruef = {m: s for m, (s, _) in marken.items()}
    if pruef != seiten or any(x % 2 == 0 for m, x in pruef.items() if not m.startswith("K")):
        raise SystemExit(f"Seitenzahlen haben sich verschoben: {seiten} != {pruef}")
    n = seitenzahl(pdf)
    # Endfassung ohne unsichtbare Marken
    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle, seiten, marken=False, leer=leer))
    drucke(html_datei, pdf, BREITE, HOEHE)
    if seitenzahl(pdf) != n or finde_marken(pdf):
        raise SystemExit("Endfassung weicht ab")
    if n > MAX_SEITEN:
        raise SystemExit(f"{name}: {n} Seiten – mehr als die {MAX_SEITEN} Seiten, die KDP beim Hardcover erlaubt")
    os.remove(html_datei)
    kopfzeilen(pdf, marken, leer, buecher, n)
    umschlaege(band, n)
    return n


def umschlaege(band, n):
    name = band["datei"]
    papier = n * PAPIER_DICKE
    arten = {
        # art: (Rücken, Rand links/rechts, Rand oben/unten, Falz)
        "taschenbuch": (papier, BESCHNITT, BESCHNITT, 0.0),
        "hardcover": (papier + HC_PAPPE, HC_EINSCHLAG_SEITE, HC_EINSCHLAG_OBEN, HC_FALZ),
    }
    for art, (ruecken, rand_x, rand_y, falz) in arten.items():
        u_breite = 2 * (BREITE + rand_x + falz) + ruecken
        u_hoehe = HOEHE + 2 * rand_y
        endung = "umschlag" if art == "taschenbuch" else "umschlag-hardcover"
        pdf = os.path.join(ZIEL, f"{name}-{endung}.pdf")
        subprocess.run(["node", os.path.join(HIER, "umschlag.mjs"), json.dumps(band), pdf,
                        str(u_breite), str(u_hoehe), str(ruecken), str(rand_x), str(rand_y), str(falz), str(n)],
                       check=True)
        print(f"{name} {art}: {n} Seiten · Umschlag {u_breite:.3f} x {u_hoehe:.3f} Zoll, Rücken {ruecken:.3f} Zoll")


if __name__ == "__main__":
    alle = lade_buecher()
    wahl = sys.argv[1:]
    baende = [w for w in wahl if not w.startswith("--")]
    for band in BAENDE:
        if baende and band["datei"].split("-")[-1] not in [w.split("-")[-1] for w in baende]:
            continue
        if "--nur-umschlag" in wahl:
            umschlaege(band, seitenzahl(os.path.join(ZIEL, f'{band["datei"]}-innenteil.pdf')))
        else:
            baue(band, alle)
