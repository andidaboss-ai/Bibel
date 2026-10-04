# Die Bibel in leichter Sprache

Die Bibel Kapitel für Kapitel in einfachem Deutsch, dazu bei jedem Abschnitt eine kurze Erklärung: **„Was bedeutet das?“**

Grundlage ist die gemeinfreie **World English Bible** (ebible.org).

## Stand

Siehe [FORTSCHRITT.md](FORTSCHRITT.md).

## Aufbau

| Ordner / Datei | Inhalt |
|---|---|
| `deutsch/` | Die deutsche Fassung, ein Kapitel pro Datei, mit Versnummern `[1]`, `[2]`, … |
| `englisch/` | Die englische Vorlage, ein Kapitel pro Datei, ein Vers pro Zeile |
| `STILREGELN.md` | Wie übersetzt wird – damit alles einheitlich bleibt |
| `pruefen.py` | Prüft, dass in jedem deutschen Kapitel **alle** Verse vorhanden sind |
| `seite_bauen.py` | Baut daraus die Leseseite `bibel.html` |
| `zerlegen.py` | Zerlegt die englische Vorlage in Kapiteldateien |
| `archiv/` | Ältere Fassungen |

## Wichtigste Regel

Kein Vers, kein Name, keine Zahl wird weggelassen.
