"""Prüft Zitate in den Erklär-Kästen: Steht der zitierte Wortlaut wirklich in der eigenen Übertragung?

Geprüft werden Zitate „…“ in Kästen (Zeilen mit „>“) und Einleitungen, hinter denen eine Stelle steht,
z. B. „…“ (1. Mose 1,1) oder „…“ (5,24) im selben Buch, oder vor denen „Vers 12:“ steht (selbes Kapitel).
Gemeldet wird jedes Zitat, dessen Wortlaut (ohne Satzzeichen, Groß/klein egal) im Zieltext nicht vorkommt.
Teile, die mit „…“ ausgelassen sind, werden einzeln gesucht."""
import glob, json, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUECHER = json.load(open(os.path.join(WURZEL, "daten", "buecher.json"), encoding="utf-8"))
NAMEN = {b["name"]: b for b in BUECHER}
NAMEN["Psalm"] = NAMEN["Psalmen"]
NAMEN_RX = "|".join(sorted((re.escape(n) for n in NAMEN), key=len, reverse=True))
TEXT = {}


def norm(t):
    t = t.lower().replace("ß", "ss")
    t = re.sub(r"\[\d+\]", " ", t)
    t = re.sub(r"[^\wäöü]+", " ", t)
    return " " + re.sub(r"\s+", " ", t).strip() + " "


def kapiteltext(b, k):
    """Nur der Bibeltext (ohne Kästen und Überschriften) eines Kapitels, normalisiert."""
    key = (b["nr"], k)
    if key not in TEXT:
        f = os.path.join(WURZEL, "texte", "leichte-sprache", b["testament"], b["ordner"], f"kapitel_{k:03d}.md")
        if not os.path.exists(f):
            TEXT[key] = None
        else:
            z = [l for l in open(f, encoding="utf-8").read().split("\n") if l and not l.startswith((">", "#", "---"))]
            TEXT[key] = norm(" ".join(z))
    return TEXT[key]


def verse(b, k, von, bis):
    """Eigener Text der Verse von–bis (ohne Kästen) als Klartext."""
    f = os.path.join(WURZEL, "texte", "leichte-sprache", b["testament"], b["ordner"], f"kapitel_{k:03d}.md")
    if not os.path.exists(f):
        return ""
    zeilen = [l for l in open(f, encoding="utf-8").read().split("\n") if l and not l.startswith((">", "#", "---"))]
    text = " ".join(zeilen)
    teile = re.split(r"\[(\d+)\]", text)
    aus = []
    for i in range(1, len(teile) - 1, 2):
        if von <= int(teile[i]) <= bis:
            aus.append(f"[{teile[i]}] {teile[i + 1].strip()}")
    return " ".join(aus)


def ziel_finden(z, m, b, k):
    """Bestimmt die zitierte Stelle: (Buch, Kapitel, Vers von, Vers bis) oder None."""
    rest = z[m.end():m.end() + 50]
    vorher = z[max(0, m.start() - 120):m.start()]
    stelle = r"(\d+)(?:,(\d+)(?:[–-](\d+))?)?"
    r = re.match(r"\s*[,.]?\s*\((?:vgl\.\s*|vergleiche\s*)?(" + NAMEN_RX + r")\s+" + stelle, rest)
    if r:
        return NAMEN[r.group(1)], int(r.group(2)), r.group(3), r.group(4)
    r = re.match(r"\s*[,.]?\s*\((?:vgl\.\s*|vergleiche\s*)?" + stelle, rest)
    if r and r.group(2):
        return b, int(r.group(1)), r.group(2), r.group(3)
    treffer = list(re.finditer(r"(" + NAMEN_RX + r")\s+" + stelle, vorher))
    if treffer:
        r = treffer[-1]
        return NAMEN[r.group(1)], int(r.group(2)), r.group(3), r.group(4)
    r = re.search(r"Vers(?:e)? (\d+)(?:[–-](\d+))?[^„]*$", vorher)
    if r:
        return b, k, r.group(1), r.group(2)
    return None


def pruefe():
    meldungen = []
    for b in BUECHER:
        for k in range(1, b["kapitel"] + 1):
            f = os.path.join(WURZEL, "texte", "leichte-sprache", b["testament"], b["ordner"], f"kapitel_{k:03d}.md")
            for nr, z in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
                if z.startswith("[") or z.startswith("#"):
                    continue  # Bibeltext selbst / Überschriften
                for m in re.finditer(r"„([^„“]{12,}?)“", z):
                    zitat = m.group(1)
                    if len(zitat.split()) < 4:
                        continue
                    ziel = ziel_finden(z, m, b, k)
                    if not ziel:
                        continue
                    zb, zk, v1, v2 = ziel
                    text = kapiteltext(zb, zk)
                    if text is None:
                        meldungen.append(dict(datei=f, zeile=nr, was=f"Stelle {zb['name']} {zk} gibt es nicht", zitat=zitat, stelle="", eigener_text=""))
                        continue
                    teile = [t for t in re.split(r"…|\.\.\.", zitat) if len(t.split()) >= 2]
                    fehlt = [t for t in teile if norm(t) not in text]
                    if fehlt:
                        v1 = int(v1) if v1 else None
                        v2 = int(v2) if v2 else v1
                        eigen = verse(zb, zk, v1, v2) if v1 else ""
                        meldungen.append(dict(datei=f, zeile=nr, was=f"nicht wörtlich in {zb['name']} {zk}",
                                              zitat=zitat, stelle=f"{zb['name']} {zk}" + (f",{v1}" + (f"–{v2}" if v2 != v1 else "") if v1 else ""),
                                              eigener_text=eigen))
    return meldungen


if __name__ == "__main__":
    m = pruefe()
    nur = sys.argv[1:]  # optional: nur Dateien, deren Pfad einen dieser Teile enthält
    if nur:
        m = [x for x in m if any(n in x["datei"] for n in nur)]
    for x in m:
        print(f"{os.path.relpath(x['datei'], os.path.join(WURZEL, 'texte', 'leichte-sprache'))}:{x['zeile']}: {x['was']}: „{x['zitat']}“")
    print(len(m), "Zitate weichen ab")
