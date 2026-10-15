# E-Book für Amazon KDP

## Die Dateien

| Ausgabe | E-Book (Manuskript) | Cover |
|---|---|---|
| Gesamtausgabe, 66 Bücher, 1.189 Kapitel | `bibel-leichte-sprache-gesamt.epub` (7,3 MB) | `bibel-leichte-sprache-gesamt-cover.jpg` |
| Band 1: 1. Mose bis 1. Samuel, 267 Kapitel | `bibel-leichte-sprache-band-1.epub` (3,9 MB) | `bibel-leichte-sprache-band-1-cover.jpg` |
| Band 2: 2. Samuel bis Psalmen, 361 Kapitel | `bibel-leichte-sprache-band-2.epub` (4,1 MB) | `bibel-leichte-sprache-band-2-cover.jpg` |
| Band 3: Sprüche bis Maleachi, 301 Kapitel | `bibel-leichte-sprache-band-3.epub` (4,0 MB) | `bibel-leichte-sprache-band-3-cover.jpg` |
| Band 4: Neues Testament, 260 Kapitel | `bibel-leichte-sprache-band-4.epub` (4,0 MB) | `bibel-leichte-sprache-band-4-cover.jpg` |

Die vier Bände sind genauso aufgeteilt wie die Druckausgabe. So passen E-Book, Taschenbuch und Hardcover als eine Reihe zusammen.

- **E-Books:** EPUB 3. Alle fünf Dateien haben die Prüfung mit EPUBCheck 5.1.0 ohne Fehler und ohne Warnungen bestanden.
- **Cover:** JPG mit 3200 × 5120 Pixeln. Das ist doppelt so groß wie die KDP-Empfehlung (1600 × 2560) im selben Seitenverhältnis 1,6 : 1. KDP erlaubt bis 10.000 Pixel.

## Hochladen bei KDP

1. Bei kdp.amazon.com „Kindle eBook“ anlegen.
2. **Manuskript:** die `.epub`-Datei hochladen.
3. **Cover:** „Cover hochladen“ wählen und die passende `-cover.jpg` hochladen. Das Cover steht nur in den Metadaten des E-Books, nicht als eigene Seite. So erscheint es nicht doppelt.
4. Mit dem **Kindle Previewer** (in KDP eingebaut) das Buch durchblättern, besonders Inhaltsverzeichnis, Kapitelraster und Kästen.

## Angaben, die du selbst machen musst

- **Autor oder Mitwirkende:** Andreas Rupp als **Herausgeber**. So steht es auch auf der Titelseite und im Impressum jedes Bandes und E-Books. Der Name steht in `werkzeuge/ebook/ebook_bauen.py` bei `HERAUSGEBER`.
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

**Cover-Design:** Das Titelbild (Kreuz aus Kristall, Splitter, Kirchenfenster) ist die Vorlage `werkzeuge/ebook/cover_vorlage/vorlage.jpg`. `werkzeuge/ebook/cover_bild.py` vergrößert sie einmal mit KI-Hochskalierung (EDSR) auf das Vierfache (`kunst-4x.jpg`) und färbt sie für jede Ausgabe um: Band 1 Violett (Original), Band 2 Smaragd, Band 3 Saphir, Band 4 Rubin, Gesamtausgabe Gold. Gold, Weiß und Schwarz bleiben dabei gleich. Titel und Texte werden scharf neu darübergesetzt. E-Book-Cover und Druck-Umschläge benutzen dasselbe Bild.

Die Vorlage hat nur 1152 × 1728 Pixel. Für den Druck wird sie stark vergrößert. Auf dem Probeexemplar prüfen, ob die Bildschärfe reicht. Wenn du die Vorlage in höherer Auflösung hast: als `vorlage.jpg` ablegen, `kunst-4x.jpg` löschen und neu bauen.

Die Schriften (Anton, Cinzel, Literata, Inter) liegen in `werkzeuge/ebook/schriften/`. Sie stehen alle unter der SIL Open Font License 1.1, die Lizenztexte liegen dabei. Sie dürfen in E-Books eingebettet und verkauft werden.

---

# Druckausgabe für Amazon KDP Print: Hardcover und Taschenbuch

Die Druckausgabe besteht aus **4 Bänden**. Jeder Band hat höchstens 550 Seiten. Das ist die Grenze von KDP für gebundene Bücher (Hardcover). So kann **jeder Band als Hardcover und als Taschenbuch** erscheinen, mit demselben Innenteil. Die Dateien liegen in `ausgabe/druck/`.

| Band | Inhalt | Seiten | Rücken Hardcover | Rücken Taschenbuch |
|---|---|---|---|---|
| 1 | Altes Testament: 1. Mose bis 1. Samuel | 511 | 1,340 Zoll | 1,151 Zoll |
| 2 | Altes Testament: 2. Samuel bis Psalmen | 519 | 1,358 Zoll | 1,169 Zoll |
| 3 | Altes Testament: Sprüche bis Maleachi | 495 | 1,304 Zoll | 1,115 Zoll |
| 4 | Neues Testament: Matthäus bis Offenbarung | 515 | 1,349 Zoll | 1,160 Zoll |

Die Bände sind fast gleich dick. Im Regal sehen sie aus wie eine Reihe. Jeder Band hat eine eigene Farbe: Band 1 Violett, Band 2 Smaragd, Band 3 Saphir, Band 4 Rubin. Die Gesamtausgabe ist Gold.

Je Band gibt es drei Dateien:
- **`…-innenteil.pdf`:** der Innenteil, gleich für Hardcover und Taschenbuch.
- **`…-umschlag-hardcover.pdf`:** der Umschlag für das Hardcover (mit Einschlag und Falz). Vorschau: `…-umschlag-hardcover-vorschau.png`.
- **`…-umschlag.pdf`:** der Umschlag für das Taschenbuch. Vorschau: `…-umschlag-vorschau.png`.

## Gestaltung des Innenteils

- Format **8,25 × 11 Zoll** (20,96 × 27,94 cm). Das ist das größte Format, das KDP für Hardcover und Taschenbuch gleich anbietet.
- Zweispaltig, Schrift Literata 9,2 Punkt. Keine Schrift ist kleiner als 7 Punkt.
- **Für Schwarzweißdruck gemacht:** Aller Text ist reines Schwarz. So wird er im Druck nicht gerastert und bleibt gestochen scharf. Grau gibt es nur bei breiten Zierlinien.
- **Kopfzeilen wie in hochwertigen Bibeln:** außen auf jeder Seite Buch und Kapitel, z. B. „MATTHÄUS 2–3“.
- Titel, Vorwort, Inhalt, die Teile und **jedes biblische Buch beginnen auf einer rechten Seite**. Davor steht, wenn nötig, eine leere Seite.
- Titelseite und Impressum: „Herausgegeben von Andreas Rupp“.
- Alle Schriften sind eingebettet. Jeder Innenteil ist ein PDF mit 4,6 bis 5,5 MB.

## Korrekturlesung

Vor dem Druck wurde der ganze Text (rund 1,3 Millionen Wörter) geprüft:
- **Rechtschreibung und Grammatik** mit LanguageTool, jeder Fund einzeln angesehen und, wo nötig, korrigiert.
- **Anführungszeichen:** In allen 66 Büchern ist jede wörtliche Rede richtig geöffnet, verschachtelt und geschlossen.
- **Namen:** überall einheitlich geschrieben (z. B. Joschija, Elija, Hiskija, Betlehem, Tarschisch).
- **Zitate in den Erklärungen** stehen wörtlich so da, wie sie in dieser Übertragung lauten. Es gibt keine Zitate aus anderen Bibelübersetzungen.
- Die Prüfprogramme liegen in `werkzeuge/pruefung/` und können nach jeder Textänderung wieder laufen:
  `python3 werkzeuge/pruefung/zitate.py` und `python3 werkzeuge/pruefung/anfuehrung.py` (beide sollen 0 melden).

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
- **Auflösung:** Alle Umschläge sind mit **600 dpi** gerendert, doppelt so hoch wie die 300 dpi, die KDP mindestens verlangt. Sie liegen als ein flaches Bild (ohne Ebenen und Transparenz) in einem PDF in exakter Größe, als JPEG in höchster Qualität. Jedes PDF ist 12–14 MB groß, unter den von KDP empfohlenen 40 MB.
- **Rücken:** Die Schrift auf dem Rücken ist nachgemessen genau in der Mitte (Abweichung unter 0,005 Zoll) und hat mindestens 0,26 Zoll Abstand zu den Kanten. KDP verlangt mindestens 0,0625 Zoll.

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
