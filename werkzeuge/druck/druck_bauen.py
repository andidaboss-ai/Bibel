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

ZIEL = os.path.join(WURZEL, "ausgabe", "druck")
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
BAENDE = json.load(open(os.path.join(HIER, "baende.json"), encoding="utf-8"))

esc = eb.esc
ziffern = eb.ziffern


def lade_buecher():
    return json.load(open(os.path.join(WURZEL, "daten", "buecher.json"), encoding="utf-8"))


def kapitel_md(b, k):
    return open(os.path.join(WURZEL, "texte", "leichte-sprache", b["testament"], b["ordner"], f"kapitel_{k:03d}.md"),
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
    # Kopfzeilen: je Buch eine benannte Seite
    kopf = []
    for b in buecher:
        name = esc(b["name"]).replace('"', '\\"')
        kopf.append(f'@page b{b["nr"]:02d}:left {{ @top-left {{ content: "{name}"; }} }}')
        kopf.append(f'@page b{b["nr"]:02d}:right {{ @top-right {{ content: "{name}"; }} }}')
        kopf.append(f'.buch-{b["nr"]:02d} {{ page: b{b["nr"]:02d}; }}')

    teile = []
    # Titelei
    teile.append(f"""<section class="titelei schmutztitel"><p class="st-titel">Die Bibel</p><p class="st-unter">in Leichter Sprache</p></section>
<section class="titelei leerseite"></section>
<section class="titelei titelseite">
<p class="ts-oben">{esc(band["oben"])}</p>
<h1 class="ts-titel">Die Bibel</h1>
<p class="ts-unter">in Leichter Sprache</p>
<div class="zier gross"><span></span></div>
<p class="ts-band">{esc(band["titel"])}</p>
<p class="ts-zusatz">{esc(band["zeile"])}</p>
<p class="ts-zusatz2">Mit Erklärungen zu jedem Abschnitt</p>
</section>""")
    hg = f"<p>Herausgegeben von {esc(eb.HERAUSGEBER)}.</p>" if eb.HERAUSGEBER else ""
    teile.append(f"""<section class="titelei impressum">
<p><strong>Die Bibel in Leichter Sprache</strong><br/>{esc(band["titel"])}: {esc(band["zeile"])}</p>
{hg}<p>Deutsche Übertragung in Leichte Sprache, {JAHR}.</p>
<p><strong>Grundlage:</strong> Diese Übertragung wurde neu aus der englischen World English Bible (WEB) erstellt. Die World English Bible ist gemeinfrei (Public Domain). Es wurde kein Text aus einer urheberrechtlich geschützten deutschen Bibelübersetzung übernommen.</p>
<p>Der Name „World English Bible“ ist eine geschützte Marke von eBible.org. Er wird hier nur genannt, um die Quelle anzugeben. Dieses Buch ist keine Ausgabe der World English Bible und wird nicht von eBible.org herausgegeben.</p>
<p><strong>Leichte Sprache:</strong> Die Übertragung orientiert sich an den Regeln für Leichte Sprache. Sie wurde nicht von einer Prüfgruppe geprüft und trägt kein Prüfsiegel.</p>
<p><strong>Schriften:</strong> Cinzel, Literata und Inter, alle unter der SIL Open Font License 1.1.</p>
<p><strong>Die Bände dieser Ausgabe:</strong><br/>{"<br/>".join(esc(x["titel"] + ": " + x["zeile"]) for x in BAENDE)}</p>
</section>""")
    # Vorwort aus dem E-Book übernehmen (ohne Seitenrahmen)
    vw = re.search(r"<section.*?</section>", eb.vorwort(), re.S).group(0)
    vw = vw.replace('class="vorwort"', 'class="titelei vorwort"').replace("<h2", '<p class="marke">@@VORWORT@@</p><h2', 1)
    vw = vw.replace("Am Ende des Buches stehen Telefon-Nummern", "Am Ende jedes Bandes stehen Telefon-Nummern")
    teile.append(vw)
    # Inhaltsverzeichnis
    z = ['<section class="titelei inhalt"><p class="marke">@@INHALT@@</p><h2 class="seitentitel">Inhalt</h2><div class="zier"><span></span></div>']
    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            z.append(f'<p class="inh-testament">{"Das Alte Testament" if letzter == "altes-testament" else "Das Neue Testament"}</p>')
        s = seiten_der_buecher.get(f'BUCH{b["nr"]:02d}', "") if seiten_der_buecher else "000"
        z.append(f'<p class="inh-zeile"><span class="inh-name">{ziffern(esc(b["name"]))}</span><span class="inh-seite">{s}</span></p>')
    s = seiten_der_buecher.get("HILFE", "") if seiten_der_buecher else "000"
    z.append(f'<p class="inh-zeile inh-extra"><span class="inh-name">Hier gibt es Hilfe</span><span class="inh-seite">{s}</span></p>')
    z.append("</section>")
    teile.append("\n".join(z))

    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            name = "Das Alte Testament" if letzter == "altes-testament" else "Das Neue Testament"
            anzahl = sum(1 for x in alle if x["testament"] == letzter)
            kurz = "TEILAT" if letzter == "altes-testament" else "TEILNT"
            teile.append(f"""<section class="teil"><p class="marke">@@{kurz}@@</p><p class="kicker">Teil</p><h1 class="teil-titel">{name}</h1>
<div class="zier gross"><span></span></div><p class="teil-unter">{anzahl} Bücher</p></section>""")
        einheit = "Psalmen" if b["code"] == "PSA" else "Kapitel"
        tname = "Altes Testament" if b["testament"] == "altes-testament" else "Neues Testament"
        teile.append(f"""<section class="buchseite"><p class="marke">@@BUCH{b["nr"]:02d}@@</p>
<p class="kicker">{tname} · Buch {b["nr"]} von 66</p>
<h1 class="buch-titel">{ziffern(esc(b["name"]))}</h1>
<div class="zier gross"><span></span></div>
<p class="buch-anzahl">{b["kapitel"]} {einheit}</p></section>""")
        kap = []
        for k in range(1, b["kapitel"] + 1):
            kap.append(f'<article class="kapitel">{eb.kapitel_html(kapitel_md(b, k), b, k)}</article>')
        teile.append(f'<section class="buchtext buch-{b["nr"]:02d}">' + "\n".join(kap) + "</section>")

    hilfe = re.search(r"<section.*?</section>", eb.hilfe(), re.S).group(0)
    hilfe = hilfe.replace('class="hilfe"', 'class="titelei hilfe"').replace("<h2", '<p class="marke">@@HILFE@@</p><h2', 1)
    teile.append(hilfe)

    doc = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"/><title>Die Bibel in Leichter Sprache – {esc(band["titel"])}</title>
<style>
{font_css()}
{css}
{chr(10).join(kopf)}
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


def finde_marken(pdf):
    """Liest aus dem PDF, auf welcher Seite jede Marke steht (Buchanfänge, Teile, Vorwort, Inhalt, Hilfe)."""
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    gefunden = {}
    for i, s in enumerate(text.split("\f"), start=1):
        for m in re.finditer(r"@@([A-Z0-9]+)@@", re.sub(r"\s+", "", s)):
            gefunden[m.group(1)] = i
    return gefunden


def leerseiten(marken):
    """Bestimmt, vor welchen Marken eine leere Seite nötig ist, damit sie auf einer rechten (ungeraden) Seite stehen.
    Jede Marke beginnt eine neue Seite, eine eingefügte Leerseite verschiebt also nur alles danach um 1."""
    leer, neu, schub = [], {}, 0
    for m, s in sorted(marken.items(), key=lambda x: x[1]):
        if (s + schub) % 2 == 0:
            leer.append(m)
            schub += 1
        neu[m] = s + schub
    return leer, neu


def baue(band, alle):
    os.makedirs(ZIEL, exist_ok=True)
    name = band["datei"]
    html_datei = os.path.join(ZIEL, f".{name}.html")
    pdf = os.path.join(ZIEL, f"{name}-innenteil.pdf")

    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle))
    drucke(html_datei, pdf, BREITE, HOEHE)
    leer, seiten = leerseiten(finde_marken(pdf))
    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle, seiten, leer=leer))
    drucke(html_datei, pdf, BREITE, HOEHE)
    pruef = finde_marken(pdf)
    if pruef != seiten or any(x % 2 == 0 for x in pruef.values()):
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
