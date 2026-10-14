"""Prüft die Anführungszeichen im Bibeltext buchweise (über Kapitelgrenzen hinweg).

Regeln (deutsche Typografie):
- „ … “ außen, ‚ … ‘ innen, eine dritte Ebene wieder „ … “.
- Geht eine Rede über mehrere Absätze (Verse), darf jeder neue Absatz wieder mit „ bzw. ‚ beginnen,
  ohne dass der vorige geschlossen wurde.
Gemeldet wird: Schließen ohne Öffnen, falsche Art des Schließens, am Buchende noch offen.
Kästen („Was bedeutet das?“) und Überschriften werden zeilenweise geprüft.
"""
import collections, glob, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pruefe_buch(dateien):
    fehler = []
    stapel = []  # Einträge: "„" oder "‚"
    for f in dateien:
        for nr, z in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
            if z.startswith(">") or z.startswith("#"):
                s = []
                for ch in z:
                    if ch in "„‚":
                        s.append(ch)
                    elif ch in "“‘":
                        if not s or s[-1] != ("„" if ch == "“" else "‚"):
                            fehler.append((f, nr, f"Kasten/Überschrift: {ch} passt nicht", z))
                            break
                        s.pop()
                else:
                    if s:
                        fehler.append((f, nr, "Kasten/Überschrift: nicht geschlossen", z))
                continue
            text = re.sub(r"^\[\d+\]\s*", "", z.strip())
            anfang = True
            for ch in text:
                if ch in "„‚":
                    if anfang and stapel and stapel[-1] == ch:
                        pass  # neuer Absatz einer laufenden Rede
                    else:
                        stapel.append(ch)
                elif ch in "“‘":
                    soll = "„" if ch == "“" else "‚"
                    if not stapel:
                        fehler.append((f, nr, f"{ch} schließt, aber nichts ist offen", z))
                    elif stapel[-1] != soll:
                        fehler.append((f, nr, f"{ch} schließt, aber offen ist {stapel[-1]}", z))
                        stapel.pop()
                    else:
                        stapel.pop()
                if not ch.isspace() and ch not in "„‚":
                    anfang = False
    if stapel:
        fehler.append((dateien[-1], 0, f"am Buchende noch offen: {''.join(stapel)}", ""))
    return fehler


if __name__ == "__main__":
    buecher = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(WURZEL, "texte", "leichte-sprache", "*", "*", "kapitel_*.md"))):
        buecher[os.path.dirname(f)].append(f)
    alle = []
    for buch in sorted(buecher, key=os.path.basename):
        alle += pruefe_buch(buecher[buch])
    for f, nr, was, z in alle:
        print(f"{os.path.relpath(f, WURZEL)}:{nr}: {was} | {z.strip()[:120]}")
    print(f"{len(alle)} Auffälligkeiten")
