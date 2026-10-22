# Englische Ausgabe für Amazon KDP – „The Bible in Plain Language“

Die englische Ausgabe ist genauso aufgebaut wie die deutsche: dieselben Abschnitte, dieselben Kästen
„What does this mean?“, dieselbe Bandaufteilung, dasselbe Layout und dieselben Cover (auf Englisch).

## Die Dateien

### E-Books (`ausgabe/english/ebook/`)

| Ausgabe | E-Book (Manuskript) | Cover |
|---|---|---|
| Gesamtausgabe, 66 Bücher, 1.189 Kapitel | `bible-plain-language-complete.epub` | `bible-plain-language-complete-cover.jpg` |
| Volume 1: Genesis bis 1 Samuel | `bible-plain-language-volume-1.epub` | `bible-plain-language-volume-1-cover.jpg` |
| Volume 2: 2 Samuel bis Psalms | `bible-plain-language-volume-2.epub` | `bible-plain-language-volume-2-cover.jpg` |
| Volume 3: Proverbs bis Malachi | `bible-plain-language-volume-3.epub` | `bible-plain-language-volume-3-cover.jpg` |
| Volume 4: Matthew bis Revelation | `bible-plain-language-volume-4.epub` | `bible-plain-language-volume-4-cover.jpg` |

- EPUB 3, geprüft mit EPUBCheck 5.1.0 (0 Fehler, 0 Warnungen).
- Cover: JPG, 3200 × 5120 Pixel (doppelte KDP-Empfehlung, Seitenverhältnis 1,6 : 1).

### Druck (`ausgabe/english/print/`)

| Band | Inhalt | Seiten | Rücken Taschenbuch | Rücken Hardcover |
|---|---|---|---|---|
| Volume 1 | Genesis bis 1 Samuel | 457 | 1,029 Zoll | 1,218 Zoll |
| Volume 2 | 2 Samuel bis Psalms | 475 | 1,070 Zoll | 1,259 Zoll |
| Volume 3 | Proverbs bis Malachi | 457 | 1,029 Zoll | 1,218 Zoll |
| Volume 4 | Matthew bis Revelation | 519 | 1,169 Zoll | 1,358 Zoll |

Alle Bände liegen unter der KDP-Grenze von 550 Seiten. Dateinamen: `bible-plain-language-print-volume-N-…`.

Je Band gibt es drei Dateien:
- **`…-innenteil.pdf`**: Innenteil, gleich für Hardcover und Taschenbuch.
- **`…-umschlag-hardcover.pdf`**: Umschlag für das Hardcover. Vorschau: `…-umschlag-hardcover-vorschau.png`.
- **`…-umschlag.pdf`**: Umschlag für das Taschenbuch. Vorschau: `…-umschlag-vorschau.png`.

## Hochladen bei KDP

Wie bei der deutschen Ausgabe – siehe `ausgabe/ebook/KDP-ANLEITUNG.md`. Die Einstellungen sind gleich:
- **E-Book:** `.epub` als Manuskript, `-cover.jpg` als Cover.
- **Hardcover und Taschenbuch:** Schwarzweiß, weißes Papier, Format **8,25 × 11 Zoll**, Innenteil **ohne Beschnitt**,
  Umschlag matt. Hardcover-Umschlag `…-umschlag-hardcover.pdf`, Taschenbuch-Umschlag `…-umschlag.pdf`.
- Vor dem Hochladen die Umschlagmaße mit dem KDP-Cover-Rechner vergleichen (Seitenzahl eintragen).
- Umschläge mit 600 dpi, Schrift auf dem Rücken nachgemessen mittig.

## Angaben bei KDP (auf Englisch eintragen)

- **Marketplace / Sprache:** English. Hauptmarkt amazon.com (USA); zusätzlich .co.uk, .ca, .com.au.
- **Title:** The Bible in Plain Language
- **Subtitle:**
  - Gesamtausgabe: *Complete Edition – Old and New Testament, with an explanation after every section*
  - Bände: *Volume 1 – Old Testament: Genesis to 1 Samuel* (entsprechend für 2–4)
- **Series:** „The Bible in Plain Language“, Volume 1–4 (Gesamtausgabe ohne Reihe).
- **Author / Contributors:** Andreas Rupp als **Editor** (so steht es auf der Titelseite, im Impressum und in den E-Book-Metadaten).
- **Description (Vorschlag):**
  > The whole Bible in plain, easy English – every verse, every name, every number. Short sentences, one thought
  > on every line. After every section, a box called “What does this mean?” explains what you have read and
  > what it can mean for us today. Based on the public-domain World English Bible.
- **Keywords:** plain English Bible; easy to read Bible; Bible for beginners; simple English Bible; Bible with
  explanations; Bible study notes; Old Testament easy; New Testament easy
- **Categories:** Religion › Bibles › Other English Translations / Religion › Biblical Studies › General
- **AI-generated content:** Ja – Text und Erklärungen wurden mit KI (Claude) erstellt. Im KDP-Formular entsprechend angeben.
- **Public domain:** Grundlage ist die gemeinfreie World English Bible (WEB). Der Text ist eine neue, eigene
  Übertragung in einfaches Englisch mit eigenen Erklärungen. Vor dem Veröffentlichen die KDP-Hilfeseite
  „Public domain content“ lesen und das Formular entsprechend ausfüllen.
- **Marke:** „World English Bible“ ist eine Marke. Sie steht im Buch nur als Quellenangabe. Nicht im Titel oder Untertitel bei KDP verwenden.
- **Plain Language:** Das Buch trägt kein offizielles Prüfsiegel. Bei KDP nichts anderes behaupten.

## Qualitätsprüfung der englischen Ausgabe

- Jedes der 1.189 Kapitel wurde Vers für Vers mit der WEB verglichen (Vollständigkeit, Bedeutung, Namen, Zahlen),
  sprachlich in einfaches amerikanisches Englisch überarbeitet und auf Formulierungen anderer Bibelübersetzungen geprüft.
- Einheitliche Begriffe für die ganze Ausgabe (Begriffsliste in `STYLE-EN.md`), Zahlen ab 10 als Ziffern,
  Maße in US-Einheiten, Hilfe-Telefonnummern für USA und Großbritannien.
- Prüfprogramme (alle melden 0):
  `python3 werkzeuge/pruefung/englisch_pruefen.py` (alle Verse, Struktur),
  `python3 werkzeuge/pruefung/zitate_en.py` (Zitate in den Kästen wörtlich),
  `python3 werkzeuge/pruefung/anfuehrung_en.py` (Anführungszeichen),
  dazu LanguageTool (en-US): `BIBEL_SPRACHE=en python3 werkzeuge/pruefung/sprachpruefung.py`.

## Neu bauen

```
BIBEL_SPRACHE=en node werkzeuge/ebook/cover_bauen.mjs      # Cover
BIBEL_SPRACHE=en python3 werkzeuge/ebook/ebook_bauen.py    # EPUBs
BIBEL_SPRACHE=en python3 werkzeuge/druck/druck_bauen.py    # Druck: Innenteile und Umschläge
```

Der englische Druck-Satz ist minimal dichter als der deutsche (9 statt 9,2 Punkt, mit Silbentrennung),
weil englischer Text länger ist. So bleibt jeder Band unter der KDP-Grenze von 550 Seiten für Hardcover.
