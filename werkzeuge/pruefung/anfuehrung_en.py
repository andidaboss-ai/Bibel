"""Prüft die Anführungszeichen der englischen Ausgabe buchweise (über Kapitelgrenzen hinweg).

Regeln (amerikanische Typografie):
- “ … ” außen, ‘ … ’ innen, eine dritte Ebene wieder “ … ”.
- ’ ist auch der Apostroph: Es schließt nur dann ein ‘, wenn kein Buchstabe folgt.
- Geht eine Rede über mehrere Zeilen oder Verse, darf eine neue Zeile wieder mit “ bzw. ‘ beginnen,
  ohne dass die vorige geschlossen wurde.
Gemeldet wird: Schließen ohne Öffnen, falsche Art des Schließens, am Buchende noch offen.
Kästen und Überschriften werden zeilenweise geprüft.
Aufruf: python3 werkzeuge/pruefung/anfuehrung_en.py [Buchordner …]
"""
import glob, os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAAR = {"”": "“", "’": "‘"}


def zeichen(z):
    """Liefert die Anführungszeichen einer Zeile; ’ zwischen oder vor Buchstaben ist ein Apostroph."""
    for i, ch in enumerate(z):
        if ch == "’":
            danach = z[i + 1:i + 2]
            if danach.isalpha():
                continue
            yield i, "’?"  # schließt ‘ nur, wenn eines offen ist; sonst Apostroph (z. B. „fathers’ “)
        elif ch in "“”‘":
            yield i, ch


def pruefe_zeile(z, stapel, neue_zeile):
    fehler = []
    erstes = True
    for i, ch in zeichen(z):
        if ch in "“‘":
            # Fortsetzung einer offenen Rede am Zeilenanfang
            if erstes and neue_zeile and stapel and stapel[-1] == ch and not z[:i].strip(" [0-9]"):
                erstes = False
                continue
            stapel.append(ch)
        elif ch == "’?":
            if stapel and stapel[-1] == "‘":
                stapel.pop()
        else:  # ”
            if not stapel or stapel[-1] != "“":
                fehler.append(f"{ch} ohne passendes “")
                if stapel and stapel[-1] == "‘":
                    stapel.pop()
                    if stapel and stapel[-1] == "“":
                        stapel.pop()
            else:
                stapel.pop()
        erstes = False
    return fehler


def pruefe_buch(dateien):
    fehler = []
    stapel = []
    for f in dateien:
        for nr, z in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
            if not z.strip() or z.strip() == "---":
                continue
            if z.startswith(">") or z.startswith("#"):
                s = []
                for meldung in pruefe_zeile(z, s, False):
                    fehler.append((f, nr, "Kasten/Überschrift: " + meldung, z))
                if s:
                    fehler.append((f, nr, f"Kasten/Überschrift: {''.join(s)} nicht geschlossen", z))
                continue
            for meldung in pruefe_zeile(z, stapel, True):
                fehler.append((f, nr, meldung, z))
    if stapel:
        fehler.append((dateien[-1], 0, f"am Buchende offen: {''.join(stapel)}", ""))
    return fehler


if __name__ == "__main__":
    nur = sys.argv[1:]
    alle = 0
    for ordner in sorted(glob.glob(os.path.join(WURZEL, "texte", "plain-english", "*", "*"))):
        if nur and os.path.basename(ordner) not in nur:
            continue
        for f, nr, m, z in pruefe_buch(sorted(glob.glob(os.path.join(ordner, "kapitel_*.md")))):
            alle += 1
            print(f"{os.path.relpath(f, WURZEL)}:{nr}: {m}  | {z.strip()[:90]}")
    print(f"{alle} Funde")
