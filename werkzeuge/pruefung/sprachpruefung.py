"""Prüft alle Kapitel mit einem lokalen LanguageTool-Server auf Rechtschreibung und Grammatik.

Vorher LanguageTool starten (https://languagetool.org/download/):
    java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081
Aufruf (im Hauptordner):
    python3 werkzeuge/pruefung/sprachpruefung.py [ausgabe.json]
Ergebnis: eine JSON-Liste aller Funde mit Datei, Zeile, Regel, Fundstelle und Vorschlägen.
"""
import concurrent.futures as cf, glob, json, os, re, sys, urllib.parse, urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER = "http://localhost:8081/v2/check"
EN = os.environ.get("BIBEL_SPRACHE") == "en"  # BIBEL_SPRACHE=en prüft die englische Ausgabe (en-US)


def reiner_text(md):
    """Markdown → Text. Gibt je Textzeile den Text, die Zeilennummer in der Datei und
    ob danach ein neuer Absatz beginnt (Leerzeile, Überschrift, Vers, Kasten-Ende)."""
    zeilen = []
    for i, z in enumerate(md.split("\n"), start=1):
        t = z.strip()
        if not t or t == "---":
            if zeilen:
                zeilen[-1][2] = True
            continue
        kopf = t.startswith("#")
        if zeilen and (kopf or re.match(r"^>?\s*\[\d+\]", t) or t.startswith("> **")):
            zeilen[-1][2] = True
        t = re.sub(r"^#+\s*", "", t)
        t = re.sub(r"^>\s?", "", t)
        t = re.sub(r"\[\d+\]\s*", "", t)
        t = t.replace("**", "").replace("*", "")
        zeilen.append([t, i, kopf])
    return zeilen


def pruefe(datei):
    md = open(datei, encoding="utf-8").read()
    zeilen = reiner_text(md)
    teile, anfang, pos = [], [], 0
    for t, nr, ende in zeilen:
        anfang.append(pos)
        trenner = "\n\n" if ende else " "
        teile.append(t + trenner)
        pos += len(t) + len(trenner)
    text = "".join(teile)
    daten = urllib.parse.urlencode({"text": text, "language": "en-US" if EN else "de-DE", "level": "picky"}).encode()
    antwort = json.load(urllib.request.urlopen(SERVER, daten, timeout=900))
    funde = []
    for m in antwort["matches"]:
        o = m["offset"]
        k = max(i for i, a in enumerate(anfang) if a <= o)
        funde.append({
            "datei": os.path.relpath(datei, WURZEL), "zeile": zeilen[k][1],
            "regel": m["rule"]["id"], "kategorie": m["rule"]["category"]["id"],
            "fund": text[o:o + m["length"]], "meldung": m["message"],
            "vorschlaege": [r["value"] for r in m["replacements"][:4]],
            "kontext": m["context"]["text"],
        })
    return funde


if __name__ == "__main__":
    aus = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WURZEL, "sprachpruefung.json")
    dateien = sorted(glob.glob(os.path.join(WURZEL, "texte", "plain-english" if EN else "leichte-sprache", "*", "*", "kapitel_*.md")))
    alle = []
    with cf.ThreadPoolExecutor(6) as pool:
        for i, f in enumerate(pool.map(pruefe, dateien), start=1):
            alle.extend(f)
            if i % 50 == 0:
                print(f"{i}/{len(dateien)} Kapitel, {len(alle)} Funde", flush=True)
    json.dump(alle, open(aus, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Fertig: {len(dateien)} Kapitel, {len(alle)} Funde → {aus}")
