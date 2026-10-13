"""Baut druckfertige PDFs (Innenteil + Umschlag) für Amazon KDP Print.

Aufruf (im Hauptordner des Projekts):
    python3 werkzeuge/druck/druck_bauen.py            # alle Bände
    python3 werkzeuge/druck/druck_bauen.py band-1     # nur einen Band

Ablauf je Band:
    1. HTML für den Innenteil schreiben (Platzhalter im Inhaltsverzeichnis).
    2. Chromium druckt das HTML als PDF (werkzeuge/druck/pdf_drucken.mjs).
    3. Seitenzahlen der Bücher aus dem PDF lesen, Inhaltsverzeichnis füllen, nochmal drucken.
    4. Umschlag (Vorderseite, Rücken, Rückseite) passend zur Seitenzahl als PDF bauen.

Format: 8,5 x 11 Zoll (21,59 x 27,94 cm), zweispaltig, Schrift 11 pt, ohne Beschnitt im Innenteil.
KDP erlaubt bei Schwarzweißdruck höchstens 828 Seiten pro Buch, darum gibt es mehrere Bände.
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
BREITE, HOEHE = 8.5, 11.0
PAPIER_DICKE = 0.002252  # Zoll pro Seite, KDP weißes Papier, Schwarzweiß
BESCHNITT = 0.125

# Die Bände für den Druck. Grenzen so gewählt, dass jeder Band unter 828 Seiten bleibt.
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


def innenteil_html(band, alle, seiten_der_buecher=None, marken=True):
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
    vw = vw.replace('class="vorwort"', 'class="titelei vorwort"')
    vw = vw.replace("Am Ende des Buches stehen Telefon-Nummern", "Am Ende jedes Bandes stehen Telefon-Nummern")
    teile.append(vw)
    # Inhaltsverzeichnis
    z = ['<section class="titelei inhalt"><h2 class="seitentitel">Inhalt</h2><div class="zier"><span></span></div>']
    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            z.append(f'<p class="inh-testament">{"Das Alte Testament" if letzter == "altes-testament" else "Das Neue Testament"}</p>')
        s = seiten_der_buecher.get(b["nr"], "") if seiten_der_buecher else "000"
        z.append(f'<p class="inh-zeile"><span class="inh-name">{ziffern(esc(b["name"]))}</span><span class="inh-seite">{s}</span></p>')
    s = seiten_der_buecher.get("hilfe", "") if seiten_der_buecher else "000"
    z.append(f'<p class="inh-zeile inh-extra"><span class="inh-name">Hier gibt es Hilfe</span><span class="inh-seite">{s}</span></p>')
    z.append("</section>")
    teile.append("\n".join(z))

    letzter = None
    for b in buecher:
        if b["testament"] != letzter:
            letzter = b["testament"]
            name = "Das Alte Testament" if letzter == "altes-testament" else "Das Neue Testament"
            anzahl = sum(1 for x in alle if x["testament"] == letzter)
            teile.append(f"""<section class="teil"><p class="kicker">Teil</p><h1 class="teil-titel">{name}</h1>
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
    """Liest aus dem PDF, auf welcher Seite jedes Buch beginnt."""
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    seiten = text.split("\f")
    gefunden = {}
    for i, s in enumerate(seiten, start=1):
        s = re.sub(r"\s+", "", s)
        for m in re.finditer(r"@@BUCH(\d\d)@@", s):
            gefunden[int(m.group(1))] = i
        if "@@HILFE@@" in s:
            gefunden["hilfe"] = i
    return gefunden


def baue(band, alle):
    os.makedirs(ZIEL, exist_ok=True)
    name = band["datei"]
    html_datei = os.path.join(ZIEL, f".{name}.html")
    pdf = os.path.join(ZIEL, f"{name}-innenteil.pdf")

    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle))
    drucke(html_datei, pdf, BREITE, HOEHE)
    seiten = finde_marken(pdf)
    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle, seiten))
    drucke(html_datei, pdf, BREITE, HOEHE)
    pruef = finde_marken(pdf)
    if pruef != seiten:
        raise SystemExit(f"Seitenzahlen haben sich verschoben: {seiten} != {pruef}")
    n = seitenzahl(pdf)
    # Endfassung ohne unsichtbare Marken
    open(html_datei, "w", encoding="utf-8").write(innenteil_html(band, alle, seiten, marken=False))
    drucke(html_datei, pdf, BREITE, HOEHE)
    if seitenzahl(pdf) != n or finde_marken(pdf):
        raise SystemExit("Endfassung weicht ab")
    if n > 828:
        raise SystemExit(f"{name}: {n} Seiten – mehr als die 828 Seiten, die KDP erlaubt")
    os.remove(html_datei)

    # Umschlag
    ruecken = n * PAPIER_DICKE
    u_breite = 2 * BREITE + ruecken + 2 * BESCHNITT
    u_hoehe = HOEHE + 2 * BESCHNITT
    umschlag_pdf = os.path.join(ZIEL, f"{name}-umschlag.pdf")
    subprocess.run(["node", os.path.join(HIER, "umschlag.mjs"), json.dumps(band), umschlag_pdf,
                    str(u_breite), str(u_hoehe), str(ruecken), str(BREITE), str(HOEHE), str(BESCHNITT), str(n)],
                   check=True)
    print(f"{os.path.relpath(pdf, WURZEL)}: {n} Seiten · Umschlag {u_breite:.3f} x {u_hoehe:.3f} Zoll, Rücken {ruecken:.3f} Zoll")
    return n


if __name__ == "__main__":
    alle = lade_buecher()
    wahl = sys.argv[1:]
    for band in BAENDE:
        if wahl and band["datei"].split("-")[-1] not in [w.split("-")[-1] for w in wahl]:
            continue
        baue(band, alle)
