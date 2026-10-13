# E-Book für Amazon KDP

## Die Dateien

| Ausgabe | E-Book (Manuskript) | Cover |
|---|---|---|
| Gesamtausgabe, 66 Bücher, 1.189 Kapitel | `bibel-leichte-sprache-gesamt.epub` (4,8 MB) | `bibel-leichte-sprache-gesamt-cover.jpg` |
| Band 1: 1. Mose bis Ester, 436 Kapitel | `bibel-leichte-sprache-band-1.epub` (2,2 MB) | `bibel-leichte-sprache-band-1-cover.jpg` |
| Band 2: Hiob bis Maleachi, 493 Kapitel | `bibel-leichte-sprache-band-2.epub` (2,0 MB) | `bibel-leichte-sprache-band-2-cover.jpg` |
| Band 3: Neues Testament, 260 Kapitel | `bibel-leichte-sprache-band-3.epub` (1,5 MB) | `bibel-leichte-sprache-band-3-cover.jpg` |

- **E-Books:** EPUB 3. Alle vier Dateien haben die Prüfung mit EPUBCheck 5.1.0 ohne Fehler und ohne Warnungen bestanden.
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
  - Band 1/2/3 – … (wie auf dem Cover)
- **Reihe:** „Die Bibel in Leichter Sprache“, Band 1–3. Die Gesamtausgabe erscheint ohne Reihe.
- **Sprache:** Deutsch
- **Schlüsselwörter:** Bibel Leichte Sprache; Bibel einfach erklärt; Bibel für Jugendliche; einfache Sprache Bibel; Altes Testament leicht; Neues Testament leicht; Bibel mit Erklärungen
- **Kategorien:** Religion > Bibel > Übersetzungen / Christentum > Bibelstudium

## Neu bauen

```
node werkzeuge/ebook/cover_bauen.mjs        # Cover (braucht Playwright + Chromium)
python3 werkzeuge/ebook/ebook_bauen.py      # alle EPUBs, bindet die Cover ein
```

Die Schriften (Cinzel, Literata, Inter) liegen in `werkzeuge/ebook/schriften/`. Sie stehen alle unter der SIL Open Font License 1.1, die Lizenztexte liegen dabei. Sie dürfen in E-Books eingebettet und verkauft werden.
