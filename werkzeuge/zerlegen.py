"""Lädt die World English Bible (gemeinfrei, ebible.org) und zerlegt sie in Kapiteldateien.

Aufruf (im Hauptordner des Projekts):
    python3 werkzeuge/zerlegen.py

Ergebnis: texte/englisch-web/<testament>/<buch>/kapitel_NNN.txt, ein Vers pro Zeile mit Nummer.
Die Zuordnung der Bücher steht in daten/buecher.json.
"""
import io, json, os, re, urllib.request, zipfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLE = "https://ebible.org/Scriptures/eng-web_readaloud.zip"

buecher = {b["code"]: b for b in json.load(open(os.path.join(WURZEL, "daten", "buecher.json"), encoding="utf-8"))}
anfrage = urllib.request.Request(QUELLE, headers={"User-Agent": "Mozilla/5.0 (bibel-leichte-sprache)"})
zip_daten = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(anfrage).read()))

n = 0
for name in sorted(zip_daten.namelist()):
    m = re.match(r"eng-web_\d+_([A-Z0-9]+)_(\d+)_read\.txt$", os.path.basename(name))
    if not m:
        continue
    code, kap = m.group(1), int(m.group(2))
    b = buecher.get(code)
    teile = (b["testament"], b["ordner"]) if b else ("apokryphen", code)
    ordner = os.path.join(WURZEL, "texte", "englisch-web", *teile)
    os.makedirs(ordner, exist_ok=True)
    zeilen = [z.strip() for z in zip_daten.read(name).decode("utf-8-sig").splitlines() if z.strip()]
    titel, verse = zeilen[0], zeilen[2:]
    with open(os.path.join(ordner, f"kapitel_{kap:03d}.txt"), "w", encoding="utf-8") as out:
        out.write(f"# {titel} Chapter {kap}\n\n")
        for i, v in enumerate(verse, 1):
            out.write(f"{i} {v}\n")
    n += 1
print(n, "Kapiteldateien geschrieben")
