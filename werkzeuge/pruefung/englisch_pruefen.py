"""Checks the English edition (texte/plain-english) against the WEB and the German edition.

For every English chapter file:
- all verses [1] … [n] of the WEB chapter are there, in order;
- same number of sections (##) and boxes (> **…**) as the German chapter;
- no German left (umlauts/ß or typical German words), straight quotes, wrong markers.
Usage: python3 werkzeuge/pruefung/englisch_pruefen.py [folder …]   (prints problems and progress)
"""
import glob, json, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUECHER = json.load(open(os.path.join(WURZEL, "daten", "buecher.json"), encoding="utf-8"))
DEUTSCH = re.compile(r"[äöüÄÖÜß]|\b(und|der|das|nicht|ist|Vers|Kapitel|bedeutet|Wichtiger|Hinweis)\b")
ERLAUBT_UMLAUT = re.compile(r"\b(Mose|Sch\w+|naïve|Zoë|Noël)\b")


def pruefe_kapitel(b, k):
    en = os.path.join(WURZEL, "texte", "plain-english", b["testament"], b["ordner"], f"kapitel_{k:03d}.md")
    de = os.path.join(WURZEL, "texte", "leichte-sprache", b["testament"], b["ordner"], f"kapitel_{k:03d}.md")
    if not os.path.exists(en):
        return None
    md = open(en, encoding="utf-8").read()
    dm = open(de, encoding="utf-8").read()
    fehler = []
    soll = list(range(1, b["verse_je_kapitel"][k - 1] + 1))
    ist = [int(n) for n in re.findall(r"^\s*>?\s*\[(\d+)\]", md, re.M)]
    if ist != soll:
        fehlt = sorted(set(soll) - set(ist))
        fehler.append(f"verses: {len(ist)} of {len(soll)}, missing {fehlt[:10]}, order ok: {ist == sorted(ist)}")
    titel = f"# Psalm {k}" if b["code"] == "PSA" else f"# {b['name_englisch']} – Chapter {k}"
    if not md.startswith(titel + "\n"):
        fehler.append(f"first line must be '{titel}'")
    for name, rx in (("sections", r"^## "), ("boxes", r"^> \*\*")):
        a, c = len(re.findall(rx, md, re.M)), len(re.findall(rx, dm, re.M))
        if a != c:
            fehler.append(f"{name}: {a} (German: {c})")
    if "(Vers " in md or "Was bedeutet" in md:
        fehler.append("German marker left")
    for nr, z in enumerate(md.split("\n"), 1):
        if '"' in z:
            fehler.append(f"line {nr}: straight quote"); break
    for nr, z in enumerate(md.split("\n"), 1):
        t = re.sub(r"„[^“]*“", "", z)  # German quotations (e.g. quoted terms) are rare but allowed? no: flag
        if DEUTSCH.search(z) and not ERLAUBT_UMLAUT.search(z):
            fehler.append(f"line {nr}: German? {z.strip()[:80]}")
            break
    return fehler


if __name__ == "__main__":
    nur = sys.argv[1:]
    fertig = gesamt = probleme = 0
    for b in BUECHER:
        if nur and b["ordner"] not in nur:
            continue
        for k in range(1, b["kapitel"] + 1):
            gesamt += 1
            f = pruefe_kapitel(b, k)
            if f is None:
                continue
            fertig += 1
            if f:
                probleme += 1
                print(f"{b['name_englisch']} {k}: " + " | ".join(f))
    print(f"{fertig} of {gesamt} chapters translated, {probleme} with problems")
