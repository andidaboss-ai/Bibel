"""Sucht Schreibvarianten von Namen: großgeschriebene Wörter, die sich nur in einem Buchstaben unterscheiden
(ein Buchstabe mehr/weniger/anders), z. B. „Hetiter“/„Hethiter“. Gibt Paare mit Häufigkeit und Fundstellen aus.
Normale Beugungsformen (David/Davids, Sohn/Sohnes …) werden ausgelassen."""
import collections, glob, os, re

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
zaehler, orte = collections.Counter(), collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(WURZEL, "texte", "leichte-sprache", "*", "*", "kapitel_*.md"))):
    kurz = os.path.relpath(f, os.path.join(WURZEL, "texte", "leichte-sprache")).replace("altes-testament/", "").replace("neues-testament/", "")
    for nr, z in enumerate(open(f, encoding="utf-8"), 1):
        for w in re.findall(r"\b[A-ZÄÖÜ][a-zäöüßA-ZÄÖÜ]+(?:-[A-ZÄÖÜ][a-zäöüß]+)*\b", z):
            zaehler[w] += 1
            if len(orte[w]) < 3:
                orte[w].append(f"{kurz}:{nr}")
ENDUNGEN = ("s", "es", "n", "en", "e", "er", "ern", "em", "ns", "'s", "’s")
def beugung(a, b):
    a, b = sorted((a, b), key=len)
    return b.startswith(a) and b[len(a):] in ENDUNGEN or (a.endswith("e") and b == a[:-1] + "en")
index = collections.defaultdict(set)
for w in zaehler:
    if len(w) < 4:
        continue
    index[w].add(w)
    for i in range(len(w)):
        index[w[:i] + w[i + 1:]].add(w)
paare = set()
for gruppe in index.values():
    g = sorted(gruppe)
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            a, b = g[i], g[j]
            if a.lower() == b.lower() or beugung(a, b):
                continue
            paare.add((a, b))
liste = sorted(paare, key=lambda p: min(zaehler[p[0]], zaehler[p[1]]))
for a, b in liste:
    if min(zaehler[a], zaehler[b]) <= 5:
        print(f"{a} ({zaehler[a]}) ~ {b} ({zaehler[b]}) | {orte[a][0] if zaehler[a] <= zaehler[b] else orte[b][0]}")
print(len(liste), "Paare insgesamt")
