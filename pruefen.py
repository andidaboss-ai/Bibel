# Prüft: Hat jede deutsche Kapiteldatei alle Verse der englischen Vorlage, in der richtigen Reihenfolge?
# Verse werden im deutschen Text mit [n] am Versanfang markiert.
import glob, os, re, sys
fehler = 0
for f in sorted(glob.glob("deutsch/*/kapitel_*.md")):
    en = f.replace("deutsch/", "englisch/").replace(".md", ".txt")
    soll = sum(1 for z in open(en, encoding="utf-8") if re.match(r"^\d+ ", z))
    ist = [int(n) for n in re.findall(r"\[(\d+)\]", open(f, encoding="utf-8").read())]
    if ist != list(range(1, soll + 1)):
        fehlt = sorted(set(range(1, soll + 1)) - set(ist))
        print(f"FEHLER {f}: {len(ist)} von {soll} Versen. Fehlend: {fehlt or '-'}; Reihenfolge ok: {ist == sorted(ist)}")
        fehler += 1
    else:
        print(f"ok     {f}: alle {soll} Verse")
sys.exit(1 if fehler else 0)
