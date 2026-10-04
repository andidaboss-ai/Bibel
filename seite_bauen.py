# Baut aus deutsch/**/kapitel_NNN.md eine einzelne Leseseite (bibel.html).
import glob, html, os, re

BUCHNAMEN = {"01_1-Mose": "1. Mose"}

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
            t = "<div class=\"tab\"><table><thead><tr>" + "".join(f"<th>{c}</th>" for c in kopf) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rest) + "</tbody></table></div>"
            out.append(t); tabelle.clear()
    for z in md.splitlines():
        if z.startswith(">"):
            absatz_ende()
            inhalt = z[1:].strip()
            if box is None:
                box = []
            if inhalt == "**Was bedeutet das?**":
                continue
            if inhalt:
                box.append(f"<p>{inline(inhalt)}</p>")
            continue
        if box is not None:
            out.append('<aside class="erkl"><h4>Was bedeutet das?</h4>' + "".join(box) + "</aside>")
            box = None
        if z.startswith("|"):
            absatz_ende(); tabelle.append(z); continue
        tabelle_ende()
        if z.startswith("# "):
            absatz_ende(); out.append(f"<h2 class=\"kap\">{inline(z[2:])}</h2>")
        elif z.startswith("### "):
            absatz_ende(); out.append(f"<p class=\"unter\">{inline(z[4:])}</p>")
        elif z.startswith("## "):
            absatz_ende(); out.append(f"<h3>{inline(z[3:])}</h3>")
        elif z.strip() in ("", "---"):
            absatz_ende()
        else:
            absatz.append(z.strip())
    absatz_ende(); tabelle_ende()
    if box is not None:
        out.append('<aside class="erkl"><h4>Was bedeutet das?</h4>' + "".join(box) + "</aside>")
    return "\n".join(out)

kapitel = []
for f in sorted(glob.glob("deutsch/*/kapitel_*.md")):
    ordner = os.path.basename(os.path.dirname(f))
    nr = int(re.search(r"(\d+)\.md$", f).group(1))
    buch = BUCHNAMEN.get(ordner, ordner.split("_", 1)[1].replace("-", ". ", 1))
    md = open(f, encoding="utf-8").read()
    titel = re.search(r"^### (.+)$", md, re.M)
    kapitel.append((f"k-{ordner}-{nr}", buch, nr, titel.group(1) if titel else "", md_zu_html(md)))

optionen = "\n".join(f'<option value="{i}">{b} {n} – {html.escape(t)}</option>' for i, b, n, t, _ in kapitel)
inhalt = "\n".join(f'<article id="{i}" class="kapitel">{h}</article>' for i, _, _, _, h in kapitel)

vorlage = open("seite_vorlage.html", encoding="utf-8").read()
seite = vorlage.replace("{{OPTIONEN}}", optionen).replace("{{INHALT}}", inhalt).replace("{{ANZAHL}}", str(len(kapitel)))
open("bibel.html", "w", encoding="utf-8").write(seite)
print(len(kapitel), "Kapitel in bibel.html")
