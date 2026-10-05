"""Baut aus den Kapiteldateien alle Ausgaben der Bibel in leichter Sprache.

Aufruf (im Hauptordner des Projekts):
    python3 werkzeuge/bauen.py              # prüfen und alles bauen
    python3 werkzeuge/bauen.py --pruefen    # nur prüfen
    python3 werkzeuge/bauen.py --sqlite     # zusätzlich ausgabe/bibel.sqlite erzeugen

Quelle der Wahrheit sind nur:
    daten/buecher.json                         Stammdaten der 66 Bücher
    texte/leichte-sprache/<testament>/<buch>/kapitel_NNN.md
    texte/englisch-web/<testament>/<buch>/kapitel_NNN.txt

Alles in ausgabe/ wird von diesem Programm erzeugt und nie von Hand bearbeitet.
"""
import csv, html, json, os, re, sqlite3, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUSGABE = os.path.join(WURZEL, "ausgabe")


def pfad(*teile):
    return os.path.join(WURZEL, *teile)


# ---------- Einlesen ----------

def lies_englisch(buch, kap):
    f = pfad("texte", "englisch-web", buch["testament"], buch["ordner"], f"kapitel_{kap:03d}.txt")
    verse = {}
    for z in open(f, encoding="utf-8"):
        m = re.match(r"^(\d+) (.*)$", z.rstrip("\n"))
        if m:
            verse[int(m.group(1))] = m.group(2).strip()
    return verse


def lies_kapitel(md):
    """Zerlegt eine Kapiteldatei in Titel, Abschnitte, Verse und Erklärungen."""
    titel = re.search(r"^### (.+)$", md, re.M)
    kapitel = {"titel": titel.group(1).strip() if titel else "", "abschnitte": []}
    abschnitt = None
    for z in md.splitlines():
        if z.startswith("## "):
            kopf = z[3:].strip()
            m = re.search(r"\(Vers (\d+)(?:[–-](\d+))?\)\s*$", kopf)
            abschnitt = {
                "ueberschrift": re.sub(r"\s*\(Vers [^)]*\)\s*$", "", kopf),
                "vers_von": int(m.group(1)) if m else None,
                "vers_bis": int(m.group(2) or m.group(1)) if m else None,
                "text": [], "erklaerung": [],
            }
            kapitel["abschnitte"].append(abschnitt)
        elif abschnitt is None or z.startswith("# ") or z.startswith("### "):
            continue
        elif z.startswith(">"):
            inhalt = z[1:].strip()
            if inhalt and inhalt != "**Was bedeutet das?**":
                abschnitt["erklaerung"].append(inhalt)
        elif z.strip() == "---":
            continue
        else:
            abschnitt["text"].append(z.rstrip())
    for a in kapitel["abschnitte"]:
        text = "\n".join(a["text"]).strip()
        teile = re.split(r"\[(\d+)\]\s*", text)
        a["einleitung"] = teile[0].strip()
        a["verse"] = {int(teile[i]): teile[i + 1].strip() for i in range(1, len(teile), 2)}
        a["text"] = text
        a["erklaerung"] = "\n".join(a["erklaerung"])
    return kapitel


def lade_alles():
    buecher = json.load(open(pfad("daten", "buecher.json"), encoding="utf-8"))
    fehler = []
    for b in buecher:
        b["fertige_kapitel"] = {}
        ordner = pfad("texte", "leichte-sprache", b["testament"], b["ordner"])
        if not os.path.isdir(ordner):
            continue
        for datei in sorted(os.listdir(ordner)):
            m = re.match(r"kapitel_(\d{3})\.md$", datei)
            if not m:
                continue
            kap = int(m.group(1))
            md = open(os.path.join(ordner, datei), encoding="utf-8").read()
            k = lies_kapitel(md)
            k["md"] = md
            k["englisch"] = lies_englisch(b, kap)
            soll = list(range(1, b["verse_je_kapitel"][kap - 1] + 1))
            ist = [int(n) for n in re.findall(r"\[(\d+)\]", md)]
            if ist != soll:
                fehlt = sorted(set(soll) - set(ist))
                fehler.append(f"{b['name']} {kap}: {len(ist)} von {len(soll)} Versen, fehlend: {fehlt or '-'}, Reihenfolge ok: {ist == sorted(ist)}")
            b["fertige_kapitel"][kap] = k
    return buecher, fehler


# ---------- Ausgaben ----------

def schreibe_json(buecher):
    os.makedirs(pfad("ausgabe", "json"), exist_ok=True)
    for b in buecher:
        ziel = pfad("ausgabe", "json", f"{b['ordner']}.json")
        if not b["fertige_kapitel"]:
            if os.path.exists(ziel):
                os.remove(ziel)
            continue
        daten = {k: b[k] for k in ("nr", "code", "kuerzel", "name", "name_englisch", "testament", "kapitel")}
        daten["inhalt"] = []
        for kap, k in sorted(b["fertige_kapitel"].items()):
            daten["inhalt"].append({
                "kapitel": kap, "titel": k["titel"],
                "abschnitte": [{
                    "ueberschrift": a["ueberschrift"], "vers_von": a["vers_von"], "vers_bis": a["vers_bis"],
                    "einleitung": a["einleitung"] or None,
                    "verse": [{"vers": n, "leichte_sprache": t, "englisch_web": k["englisch"].get(n)}
                              for n, t in sorted(a["verse"].items())],
                    "erklaerung": a["erklaerung"],
                } for a in k["abschnitte"]],
            })
        json.dump(daten, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def schreibe_csv(buecher):
    with open(pfad("ausgabe", "verse.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["buch_nr", "buch", "kuerzel", "kapitel", "vers", "stelle", "abschnitt", "leichte_sprache", "englisch_web"])
        for b in buecher:
            for kap, k in sorted(b["fertige_kapitel"].items()):
                for a in k["abschnitte"]:
                    for n, t in sorted(a["verse"].items()):
                        w.writerow([b["nr"], b["name"], b["kuerzel"], kap, n, f"{b['kuerzel']} {kap},{n}",
                                    a["ueberschrift"], t.replace("\n", " "), k["englisch"].get(n, "")])
    with open(pfad("ausgabe", "erklaerungen.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["buch_nr", "buch", "kapitel", "abschnitt", "vers_von", "vers_bis", "erklaerung"])
        for b in buecher:
            for kap, k in sorted(b["fertige_kapitel"].items()):
                for a in k["abschnitte"]:
                    if a["erklaerung"]:
                        w.writerow([b["nr"], b["name"], kap, a["ueberschrift"], a["vers_von"], a["vers_bis"], a["erklaerung"]])


def schreibe_sqlite(buecher):
    ziel = pfad("ausgabe", "bibel.sqlite")
    if os.path.exists(ziel):
        os.remove(ziel)
    db = sqlite3.connect(ziel)
    db.executescript("""
        CREATE TABLE buecher (nr INTEGER PRIMARY KEY, code TEXT, kuerzel TEXT, name TEXT, name_englisch TEXT,
                              testament TEXT, kapitel_anzahl INTEGER);
        CREATE TABLE kapitel (buch_nr INTEGER, kapitel INTEGER, titel TEXT, verse_anzahl INTEGER, fertig INTEGER,
                              PRIMARY KEY (buch_nr, kapitel));
        CREATE TABLE abschnitte (id INTEGER PRIMARY KEY, buch_nr INTEGER, kapitel INTEGER, nr INTEGER,
                                 ueberschrift TEXT, vers_von INTEGER, vers_bis INTEGER, einleitung TEXT, erklaerung TEXT);
        CREATE TABLE verse (buch_nr INTEGER, kapitel INTEGER, vers INTEGER, abschnitt_id INTEGER,
                            leichte_sprache TEXT, englisch_web TEXT, PRIMARY KEY (buch_nr, kapitel, vers));
    """)
    for b in buecher:
        db.execute("INSERT INTO buecher VALUES (?,?,?,?,?,?,?)",
                   (b["nr"], b["code"], b["kuerzel"], b["name"], b["name_englisch"], b["testament"], b["kapitel"]))
        for kap in range(1, b["kapitel"] + 1):
            k = b["fertige_kapitel"].get(kap)
            englisch = k["englisch"] if k else lies_englisch(b, kap)
            db.execute("INSERT INTO kapitel VALUES (?,?,?,?,?)",
                       (b["nr"], kap, k["titel"] if k else None, len(englisch), 1 if k else 0))
            leicht = {}
            if k:
                for i, a in enumerate(k["abschnitte"], 1):
                    cur = db.execute("INSERT INTO abschnitte (buch_nr, kapitel, nr, ueberschrift, vers_von, vers_bis, einleitung, erklaerung) VALUES (?,?,?,?,?,?,?,?)",
                                     (b["nr"], kap, i, a["ueberschrift"], a["vers_von"], a["vers_bis"], a["einleitung"] or None, a["erklaerung"] or None))
                    for n, t in a["verse"].items():
                        leicht[n] = (cur.lastrowid, t)
            for n, en in sorted(englisch.items()):
                aid, t = leicht.get(n, (None, None))
                db.execute("INSERT INTO verse VALUES (?,?,?,?,?,?)", (b["nr"], kap, n, aid, t, en))
    db.commit()
    db.close()


def demote(md):
    """Überschriften eine Ebene tiefer setzen, damit Buchtitel die oberste Ebene sind."""
    return re.sub(r"^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", md, flags=re.M)


def schreibe_gesamt_md(buecher):
    teile = ["# Die Bibel in leichter Sprache\n",
             "Übertragung in leichte Sprache mit Erklärungen. Grundlage: World English Bible (gemeinfrei).\n",
             "Diese Datei wird automatisch aus den einzelnen Kapiteln zusammengesetzt.\n"]
    for b in buecher:
        if not b["fertige_kapitel"]:
            continue
        teile.append(f"\n---\n\n# {b['name']}\n")
        for kap, k in sorted(b["fertige_kapitel"].items()):
            md = re.sub(r"\[(\d+)\] ?", r"<sup>\1</sup>", k["md"])
            teile.append(demote(md).strip() + "\n")
    open(pfad("ausgabe", "bibel-leichte-sprache.md"), "w", encoding="utf-8").write("\n".join(teile))


# ---------- Leseseite (HTML) ----------

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"\[(\d+)\] ?", r'<sup class="v">\1</sup>', t)


def md_zu_html(md):
    out, absatz, box, tabelle = [], [], None, []

    def absatz_ende():
        if absatz:
            ziel = box if box is not None else out
            ziel.append("<p>" + "<br>".join(inline(z) for z in absatz) + "</p>")
            absatz.clear()

    def tabelle_ende():
        if tabelle:
            zeilen = [[inline(c.strip()) for c in z.strip("|").split("|")] for z in tabelle if not re.match(r"^\|[-| ]+\|$", z)]
            kopf, rest = zeilen[0], zeilen[1:]
            t = '<div class="tab"><table><thead><tr>' + "".join(f"<th>{c}</th>" for c in kopf) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rest) + "</tbody></table></div>"
            out.append(t)
            tabelle.clear()

    for z in md.splitlines():
        if z.startswith(">"):
            absatz_ende()
            inhalt = z[1:].strip()
            if box is None:
                box = []
            if inhalt and inhalt != "**Was bedeutet das?**":
                box.append(f"<p>{inline(inhalt)}</p>")
            continue
        if box is not None:
            out.append('<aside class="erkl"><h4>Was bedeutet das?</h4>' + "".join(box) + "</aside>")
            box = None
        if z.startswith("|"):
            absatz_ende()
            tabelle.append(z)
            continue
        tabelle_ende()
        if z.startswith("# "):
            absatz_ende(); out.append(f'<h2 class="kap">{inline(z[2:])}</h2>')
        elif z.startswith("### "):
            absatz_ende(); out.append(f'<p class="unter">{inline(z[4:])}</p>')
        elif z.startswith("## "):
            absatz_ende(); out.append(f"<h3>{inline(z[3:])}</h3>")
        elif z.strip() in ("", "---"):
            absatz_ende()
        else:
            absatz.append(z.strip())
    absatz_ende()
    tabelle_ende()
    if box is not None:
        out.append('<aside class="erkl"><h4>Was bedeutet das?</h4>' + "".join(box) + "</aside>")
    return "\n".join(out)


def schreibe_html(buecher):
    optionen, inhalt, anzahl = [], [], 0
    for b in buecher:
        if not b["fertige_kapitel"]:
            continue
        optionen.append(f'<optgroup label="{html.escape(b["name"])}">')
        for kap, k in sorted(b["fertige_kapitel"].items()):
            kid = f"k-{b['ordner']}-{kap}"
            optionen.append(f'<option value="{kid}">{html.escape(b["name"])} {kap} – {html.escape(k["titel"])}</option>')
            inhalt.append(f'<article id="{kid}" class="kapitel">{md_zu_html(k["md"])}</article>')
            anzahl += 1
        optionen.append("</optgroup>")
    vorlage = open(pfad("werkzeuge", "vorlage_leseseite.html"), encoding="utf-8").read()
    seite = vorlage.replace("{{OPTIONEN}}", "\n".join(optionen)).replace("{{INHALT}}", "\n".join(inhalt)).replace("{{ANZAHL}}", str(anzahl))
    open(pfad("ausgabe", "bibel.html"), "w", encoding="utf-8").write(seite)


def schreibe_fortschritt(buecher):
    gesamt_kap = sum(b["kapitel"] for b in buecher)
    gesamt_verse = sum(sum(b["verse_je_kapitel"]) for b in buecher)
    fertig_kap = sum(len(b["fertige_kapitel"]) for b in buecher)
    fertig_verse = sum(b["verse_je_kapitel"][k - 1] for b in buecher for k in b["fertige_kapitel"])
    z = ["# Fortschritt", "",
         "Diese Datei wird automatisch von `werkzeuge/bauen.py` erzeugt.", "",
         f"**Gesamt: {fertig_kap} von {gesamt_kap} Kapiteln ({fertig_kap * 100 / gesamt_kap:.1f} %), "
         f"{fertig_verse} von {gesamt_verse} Versen.**", "",
         "| Nr | Buch | Testament | Kapitel fertig | Stand |", "|---|---|---|---|---|"]
    for b in buecher:
        n = len(b["fertige_kapitel"])
        stand = "fertig" if n == b["kapitel"] else ("in Arbeit" if n else "–")
        t = "AT" if b["testament"] == "altes-testament" else "NT"
        z.append(f"| {b['nr']} | {b['name']} | {t} | {n} / {b['kapitel']} | {stand} |")
    open(pfad("FORTSCHRITT.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    return fertig_kap, gesamt_kap


def main():
    buecher, fehler = lade_alles()
    if fehler:
        print("PRÜFUNG FEHLGESCHLAGEN:")
        for f in fehler:
            print("  -", f)
        sys.exit(1)
    fertig = sum(len(b["fertige_kapitel"]) for b in buecher)
    print(f"Prüfung ok: {fertig} Kapitel, alle Verse vorhanden.")
    if "--pruefen" in sys.argv:
        return
    os.makedirs(AUSGABE, exist_ok=True)
    schreibe_json(buecher)
    schreibe_csv(buecher)
    schreibe_gesamt_md(buecher)
    schreibe_html(buecher)
    if "--sqlite" in sys.argv:
        schreibe_sqlite(buecher)
    f, g = schreibe_fortschritt(buecher)
    print(f"Ausgaben gebaut: {f} von {g} Kapiteln.")


if __name__ == "__main__":
    main()
