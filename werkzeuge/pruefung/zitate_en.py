"""Checks quotations in the English boxes: is the quoted wording really in our own English text?

Checked: quotations “…” in boxes (lines starting with “>”) and introductions that give a passage,
e.g. “…” (Genesis 1:3), “…” (5:24) in the same book, or that follow “verse 12:” (same chapter).
Reports every quotation whose wording (ignoring punctuation and case) is not in our English text there.
Usage: python3 werkzeuge/pruefung/zitate_en.py [folder …]
"""
import json, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUECHER = json.load(open(os.path.join(WURZEL, "daten", "buecher.json"), encoding="utf-8"))
NAMEN = {b["name_englisch"]: b for b in BUECHER}
NAMEN["Psalm"] = NAMEN["Psalms"]
NAMEN["Song of Solomon"] = NAMEN["Song of Songs"]
NAMEN_RX = "|".join(sorted((re.escape(n) for n in NAMEN), key=len, reverse=True))
TEXT = {}
ORDNER = os.path.join(WURZEL, "texte", "plain-english")


def norm(t):
    t = t.lower()
    t = re.sub(r"(?<!\w)[‘’']|[‘’'](?!\w)", " ", t)  # Anführungszeichen am Wortrand
    t = t.replace("’", "'")
    t = re.sub(r"\[\d+\]", " ", t)
    t = re.sub(r"[^\w']+", " ", t)
    return " " + re.sub(r"\s+", " ", t).strip() + " "


def datei(b, k):
    return os.path.join(ORDNER, b["testament"], b["ordner"], f"kapitel_{k:03d}.md")


def kapiteltext(b, k):
    key = (b["nr"], k)
    if key not in TEXT:
        f = datei(b, k)
        if not os.path.exists(f):
            TEXT[key] = None
        else:
            z = [l for l in open(f, encoding="utf-8").read().split("\n") if l and not l.startswith((">", "#", "---"))]
            TEXT[key] = norm(" ".join(z))
    return TEXT[key]


def ziel_finden(z, m, b, k):
    rest = z[m.end():m.end() + 50]
    vorher = z[max(0, m.start() - 120):m.start()]
    stelle = r"(\d+)(?::(\d+)(?:[–-](\d+))?)?"
    r = re.match(r"\s*[,.]?\s*\((?:see\s*|compare\s*|cf\.\s*)?(" + NAMEN_RX + r")\s+" + stelle, rest)
    if r:
        return NAMEN[r.group(1)], int(r.group(2))
    r = re.match(r"\s*[,.]?\s*\((?:see\s*|compare\s*)?(\d+):(\d+)", rest)
    if r:
        return b, int(r.group(1))
    t = list(re.finditer(r"(" + NAMEN_RX + r")\s+" + stelle, vorher))
    if t:
        return NAMEN[t[-1].group(1)], int(t[-1].group(2))
    if re.search(r"[Vv]erses? (\d+)(?:[–-](\d+))?[^“]*$", vorher):
        return b, k
    return None


def pruefe(nur=()):
    meldungen = []
    for b in BUECHER:
        if nur and b["ordner"] not in nur:
            continue
        for k in range(1, b["kapitel"] + 1):
            f = datei(b, k)
            if not os.path.exists(f):
                continue
            for nr, z in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
                if z.startswith("[") or z.startswith("#"):
                    continue
                for m in re.finditer(r"“([^“”]{12,}?)”", z):
                    zitat = m.group(1)
                    if len(zitat.split()) < 4:
                        continue
                    ziel = ziel_finden(z, m, b, k)
                    if not ziel:
                        continue
                    zb, zk = ziel
                    text = kapiteltext(zb, zk)
                    if text is None:
                        continue  # chapter not translated yet
                    teile = [t for t in re.split(r"…", zitat) if len(t.split()) >= 2]
                    if any(norm(t) not in text for t in teile):
                        meldungen.append((f, nr, f"{zb['name_englisch']} {zk}", zitat))
    return meldungen


if __name__ == "__main__":
    m = pruefe(sys.argv[1:])
    for f, nr, stelle, zitat in m:
        print(f"{os.path.relpath(f, ORDNER)}:{nr}: not word for word in {stelle}: “{zitat}”")
    print(len(m), "quotations differ")
