# E-Book für Amazon KDP

## Die Dateien

| Ausgabe | E-Book (Manuskript) | Cover |
|---|---|---|
| Gesamtausgabe, 66 Bücher, 1.189 Kapitel | `bibel-leichte-sprache-gesamt.epub` (5,5 MB) | `bibel-leichte-sprache-gesamt-cover.jpg` |
| Band 1: 1. Mose bis 1. Samuel, 267 Kapitel | `bibel-leichte-sprache-band-1.epub` (2,2 MB) | `bibel-leichte-sprache-band-1-cover.jpg` |
| Band 2: 2. Samuel bis Psalmen, 361 Kapitel | `bibel-leichte-sprache-band-2.epub` (2,3 MB) | `bibel-leichte-sprache-band-2-cover.jpg` |
| Band 3: Sprüche bis Maleachi, 301 Kapitel | `bibel-leichte-sprache-band-3.epub` (2,2 MB) | `bibel-leichte-sprache-band-3-cover.jpg` |
| Band 4: Neues Testament, 260 Kapitel | `bibel-leichte-sprache-band-4.epub` (2,2 MB) | `bibel-leichte-sprache-band-4-cover.jpg` |

Die vier Bände sind genauso aufgeteilt wie die Druckausgabe. So passen E-Book, Taschenbuch und Hardcover als eine Reihe zusammen.

- **E-Books:** EPUB 3. Alle fünf Dateien haben die Prüfung mit EPUBCheck 5.1.0 ohne Fehler und ohne Warnungen bestanden.
- **Cover:** JPG mit 1600 × 2560 Pixeln. Das ist das Seitenverhältnis 1,6 : 1, das KDP empfiehlt.

## Hochladen bei KDP

1. Bei kdp.amazon.com „Kindle eBook“ anlegen.
2. **Manuskript:** die `.epub`-Datei hochladen.
3. **Cover:** „Cover hochladen“ wählen und die passende `-cover.jpg` hochladen. Das Cover steht nur in den Metadaten des E-Books, nicht als eigene Seite. So erscheint es nicht doppelt.
4. Mit dem **Kindle Previewer** (in KDP eingebaut) das Buch durchblättern, besonders Inhaltsverzeichnis, Kapitelraster und Kästen.

## Angaben, die du selbst machen musst

- **Autor oder Mitwirkende:** zum Beispiel als „Übersetzer“ bzw. „Herausgeber“. Wenn dein Name auch im Impressum stehen soll: in `werkzeuge/ebook/ebook_bauen.py` bei `HERAUSGEBER = ""` eintragen und neu bauen.
- **KI-Inhalte:** KDP fragt, ob Texte mit KI erstellt wurden. Die Übertragung und die Erklärungen wurden mit KI (Claude) erstellt. Das muss im KDP-Formular angegeben werden. Dort ist „KI-generiert“ die passende Auswahl.
- **Gemeinfreie Inhalte:** KDP hat eigene Regeln für Bücher, die auf gemeinfreien Texten beruhen. Die Vorlage (World English Bible) ist gemeinfrei. Der deutsche Text ist eine neue Übertragung mit eigenen Erklärungen. Bitte vor dem Veröffentlichen die aktuelle KDP-Hilfeseite zu „Public domain content“ lesen und das Formular entsprechend ausfüllen.
- **Marke:** „World English Bible“ ist eine Marke. Sie wird im Buch nur als Quelle genannt. Im Titel oder Untertitel bei KDP sollte sie nicht stehen.
- **Leichte Sprache:** Das Buch trägt kein Prüfsiegel für Leichte Sprache. Das steht auch im Impressum. Bitte bei KDP nichts anderes behaupten.

## Vorschläge für die Angaben bei KDP

- **Titel:** Die Bibel in Leichter Sprache
- **Untertitel:**
  - Gesamtausgabe – Altes und Neues Testament. Mit Erklärungen zu jedem Abschnitt
  - Band 1/2/3/4 – … (wie auf dem Cover)
- **Reihe:** „Die Bibel in Leichter Sprache“, Band 1–4. E-Book, Taschenbuch und Hardcover eines Bandes verknüpft KDP automatisch, wenn Titel, Autor und Reihe gleich sind. Die Gesamtausgabe erscheint ohne Reihe.
- **Sprache:** Deutsch
- **Schlüsselwörter:** Bibel Leichte Sprache; Bibel einfach erklärt; Bibel für Jugendliche; einfache Sprache Bibel; Altes Testament leicht; Neues Testament leicht; Bibel mit Erklärungen
- **Kategorien:** Religion > Bibel > Übersetzungen / Christentum > Bibelstudium

## Neu bauen

```
node werkzeuge/ebook/cover_bauen.mjs        # Cover (braucht Playwright + Chromium)
python3 werkzeuge/ebook/ebook_bauen.py      # alle EPUBs, bindet die Cover ein
```

**Cover-Design:** großer Titel „DIE BIBEL“, darunter ein leuchtendes Kreuz aus Kristall mit Splittern, Funken und Kirchenfenstern. Alle Bände haben dasselbe Bild, nur in ihrer eigenen Farbe. Das Bild wird mit Code gezeichnet (`werkzeuge/ebook/cover_kunst.mjs`). Darum ist es in jeder Größe scharf, auch mit 300 dpi für den Druck. E-Book-Cover und Druck-Umschläge benutzen dasselbe Design.

Die Schriften (Anton, Cinzel, Literata, Inter) liegen in `werkzeuge/ebook/schriften/`. Sie stehen alle unter der SIL Open Font License 1.1, die Lizenztexte liegen dabei. Sie dürfen in E-Books eingebettet und verkauft werden.

---

# Druckausgabe für Amazon KDP Print: Hardcover und Taschenbuch

Die Druckausgabe besteht aus **4 Bänden**. Jeder Band hat höchstens 550 Seiten. Das ist die Grenze von KDP für gebundene Bücher (Hardcover). So kann **jeder Band als Hardcover und als Taschenbuch** erscheinen, mit demselben Innenteil. Die Dateien liegen in `ausgabe/druck/`.

| Band | Inhalt | Seiten | Rücken Hardcover | Rücken Taschenbuch |
|---|---|---|---|---|
| 1 | Altes Testament: 1. Mose bis 1. Samuel | 511 | 1,340 Zoll | 1,151 Zoll |
| 2 | Altes Testament: 2. Samuel bis Psalmen | 519 | 1,358 Zoll | 1,169 Zoll |
| 3 | Altes Testament: Sprüche bis Maleachi | 493 | 1,299 Zoll | 1,110 Zoll |
| 4 | Neues Testament: Matthäus bis Offenbarung | 515 | 1,349 Zoll | 1,160 Zoll |

Die Bände sind fast gleich dick. Im Regal sehen sie aus wie eine Reihe. Jeder Band hat eine eigene Farbe: Band 1 Violett, Band 2 Smaragd, Band 3 Saphir, Band 4 Rubin. Die Gesamtausgabe ist Gold.

Je Band gibt es drei Dateien:
- **`…-innenteil.pdf`:** der Innenteil, gleich für Hardcover und Taschenbuch.
- **`…-umschlag-hardcover.pdf`:** der Umschlag für das Hardcover (mit Einschlag und Falz). Vorschau: `…-umschlag-hardcover-vorschau.png`.
- **`…-umschlag.pdf`:** der Umschlag für das Taschenbuch. Vorschau: `…-umschlag-vorschau.png`.

## Gestaltung des Innenteils

- Format **8,25 × 11 Zoll** (20,96 × 27,94 cm). Das ist das größte Format, das KDP für Hardcover und Taschenbuch gleich anbietet.
- Zweispaltig, Schrift Literata 9,2 Punkt.
- Wie bei hochwertigen Büchern beginnen Titel, Vorwort, Inhalt, die Teile und **jedes biblische Buch auf einer rechten Seite**. Davor steht, wenn nötig, eine leere Seite.
- Kopfzeile mit dem Namen des Buches, Seitenzahl unten in der Mitte.

## Einstellungen bei KDP: Hardcover

- **Druckoptionen:** Schwarzweiß, **weißes Papier**.
- **Format (Trim Size):** **8,25 × 11 Zoll**.
- **Beschnitt (Bleed):** Innenteil **ohne Beschnitt** („No Bleed“).
- **Umschlag-Oberfläche:** **matt** wirkt bei dem dunklen Design am edelsten.
- **Manuskript:** `…-innenteil.pdf` hochladen.
- **Cover:** „Ein Cover hochladen, das Sie bereits haben“ und `…-umschlag-hardcover.pdf` hochladen.
- **Maße des Hardcover-Umschlags:** 19,4 × 12,418 Zoll. Er hat 0,591 Zoll Einschlag links und rechts, 0,709 Zoll oben und unten und 0,197 Zoll Falz neben dem Rücken. Der Rücken ist Papier plus 0,189 Zoll für die Pappe. **Bitte vor dem Hochladen mit dem Cover-Rechner von KDP vergleichen** (KDP-Hilfe „Cover Calculator“: Hardcover, 8,25 × 11, weißes Papier, Seitenzahl eintragen). Weicht die Vorlage ab, die Werte oben in `werkzeuge/druck/druck_bauen.py` (`HC_…`) anpassen und nur die Umschläge neu bauen:
  `python3 werkzeuge/druck/druck_bauen.py --nur-umschlag`
- **Barcode:** KDP setzt den Barcode unten rechts auf die Rückseite. Diese Fläche ist frei.

## Einstellungen bei KDP: Taschenbuch

- Schwarzweiß, weißes Papier, **8,25 × 11 Zoll**, Innenteil ohne Beschnitt.
- Cover: `…-umschlag.pdf` (0,125 Zoll Beschnitt rundum).

## Wichtig

- **Seitenzahl ändert sich:** Wenn sich der Text ändert, ändert sich vielleicht die Seitenzahl und damit die Breite des Rückens. Darum immer Innenteil und Umschläge zusammen neu bauen:
  `python3 werkzeuge/druck/druck_bauen.py`
- **Reserve:** Jeder Band hat noch mindestens 31 Seiten Platz bis zur Grenze von 550 Seiten. Bei mehr als 550 Seiten bricht das Bau-Programm mit einer Meldung ab.
- **Probeexemplar:** Vor dem Freigeben den „Print Previewer“ durchsehen und am besten von jedem Band ein Probeexemplar bestellen. Beim Hardcover besonders auf den Rücken und den Einschlag achten.
- **Schriften:** Alle Schriften sind in den PDFs eingebettet.
- **Ränder:** Innenrand (Bundsteg) 0,8 Zoll, Außenrand 0,45 Zoll. Das erfüllt die KDP-Vorgaben für 501–700 Seiten (innen mindestens 0,75 Zoll).
