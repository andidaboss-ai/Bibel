# Die Bibel in leichter Sprache

Die ganze Bibel, Kapitel für Kapitel, in einfachem Deutsch.
Zu jedem Abschnitt gibt es eine kurze Erklärung: **„Was bedeutet das?“**
Grundlage ist die gemeinfreie **World English Bible** (ebible.org).

**Wichtigste Regel:** Kein Vers, kein Name, keine Zahl wird weggelassen.
Ein Prüfprogramm kontrolliert das bei jedem Kapitel automatisch.

Den aktuellen Stand zeigt [FORTSCHRITT.md](FORTSCHRITT.md).

---

## Ordner und Dateien

```
daten/
  buecher.json                  Verzeichnis aller 66 Bücher (Name, Kürzel, Testament, Kapitel, Verse je Kapitel)

texte/
  leichte-sprache/              DIE ÜBERSETZUNG – ein Kapitel pro Datei
    altes-testament/01_1-Mose/kapitel_001.md
    neues-testament/…
  englisch-web/                 Die englische Vorlage – ein Kapitel pro Datei, ein Vers pro Zeile
    altes-testament/…
    neues-testament/…
    apokryphen/…

ausgabe/                        AUTOMATISCH ERZEUGT – nie von Hand bearbeiten
  bibel-leichte-sprache.md      alle fertigen Kapitel als ein einziges Dokument
  bibel.html                    Leseseite zum Öffnen im Browser
  verse.csv                     jeder Vers eine Zeile (öffnet sich in Excel)
  erklaerungen.csv              jede Erklärung eine Zeile (öffnet sich in Excel)
  json/01_1-Mose.json           ein Buch mit Abschnitten, Versen und Erklärungen

werkzeuge/
  bauen.py                      prüft alle Kapitel und erzeugt alles in ausgabe/
  zerlegen.py                   lädt die englische Vorlage neu und zerlegt sie
  vorlage_leseseite.html        Aussehen der Leseseite

archiv/                         ältere Fassungen
STILREGELN.md                   wie übersetzt wird
FORTSCHRITT.md                  Stand der Arbeit (automatisch erzeugt)
```

## Aufbau einer Kapiteldatei

```markdown
# 1. Mose – Kapitel 1
### Gott erschafft die Welt

## Der erste Tag: Gott macht das Licht (Vers 3–5)

[3] Gott sprach: „Es soll Licht werden.“
Und es wurde Licht.
[4] …

> **Was bedeutet das?**
> Gott muss nur sprechen – und es geschieht. …
```

- `# …` Buch und Kapitel
- `### …` Titel des Kapitels
- `## … (Vers 3–5)` ein Abschnitt mit seinen Versen
- `[3]` Beginn von Vers 3
- `> …` die Erklärung zu diesem Abschnitt

## Die Datenbank

Alle Kapiteldateien zusammen sind die Datenbank. Daraus entstehen automatisch:

| Datei | Inhalt | Geeignet für |
|---|---|---|
| `ausgabe/verse.csv` | Buch, Kapitel, Vers, Abschnitt, leichte Sprache, Englisch | Excel, Tabellen |
| `ausgabe/erklaerungen.csv` | alle Erklärungen mit Bibelstelle | Excel, Tabellen |
| `ausgabe/json/<buch>.json` | Bücher → Kapitel → Abschnitte → Verse + Erklärung | Apps, Webseiten |
| `ausgabe/bibel-leichte-sprache.md` | alles als ein Text | Lesen, Drucken, Buch |
| `ausgabe/bibel.html` | Leseseite mit Kapitelauswahl | Browser, Handy |
| `ausgabe/bibel.sqlite` | Tabellen `buecher`, `kapitel`, `abschnitte`, `verse` | Datenbank-Programme |

Die SQLite-Datei wird auf Wunsch erzeugt (`python3 werkzeuge/bauen.py --sqlite`).
Sie liegt nicht im Repository, weil sie bei jeder Änderung komplett neu gespeichert würde.

## Alles neu bauen

```
python3 werkzeuge/bauen.py
```

Das Programm prüft zuerst jedes Kapitel gegen die englische Vorlage.
Fehlt auch nur ein Vers, bricht es ab und nennt die Stelle.
