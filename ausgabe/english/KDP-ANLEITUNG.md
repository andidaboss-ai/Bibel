# Englische Ausgabe für Amazon KDP – „The Bible in Plain Language“

**Status: fertig zum Hochladen.** Alle Dateien in diesem Ordner sind die finalen KDP-Dateien.
Diese Anleitung ist vollständig: Wer hochlädt, braucht nur sie und die Dateien in `ausgabe/english/`.

Die englische Ausgabe ist genauso gebaut wie die deutsche („Die Bibel in Leichter Sprache“, `ausgabe/ebook/` und `ausgabe/druck/`):
- dieselbe Aufteilung in 4 Bände und eine Gesamtausgabe (E-Book);
- dasselbe Format, 8,25 × 11 Zoll;
- dasselbe Layout: zweispaltig, Kopfzeilen, Kästen „What does this mean?“, jedes Buch beginnt rechts;
- dieselben Schriften und dasselbe Cover-Design mit denselben Farben je Band, nur auf Englisch:
  Volume 1 Violett, Volume 2 Smaragd, Volume 3 Saphir, Volume 4 Rubin, Gesamtausgabe Gold.

Der einzige Unterschied ist der Satz: Er ist minimal dichter, 9 statt 9,2 Punkt, mit Silbentrennung. Englischer Text ist länger als der deutsche. So bleibt jeder Band sicher unter der KDP-Grenze von 550 Seiten.

---

## 1. Die Dateien

### E-Books (`ausgabe/english/ebook/`)

| Ausgabe | Manuskript | Cover |
|---|---|---|
| Gesamtausgabe, 66 Bücher, 1.189 Kapitel | `bible-plain-language-complete.epub` | `bible-plain-language-complete-cover.jpg` |
| Volume 1: Genesis to 1 Samuel, 267 Kapitel | `bible-plain-language-volume-1.epub` | `bible-plain-language-volume-1-cover.jpg` |
| Volume 2: 2 Samuel to Psalms, 361 Kapitel | `bible-plain-language-volume-2.epub` | `bible-plain-language-volume-2-cover.jpg` |
| Volume 3: Proverbs to Malachi, 301 Kapitel | `bible-plain-language-volume-3.epub` | `bible-plain-language-volume-3-cover.jpg` |
| Volume 4: Matthew to Revelation, 260 Kapitel | `bible-plain-language-volume-4.epub` | `bible-plain-language-volume-4-cover.jpg` |

- **E-Books:** EPUB 3. Alle fünf Dateien sind mit EPUBCheck 5.1.0 geprüft: 0 Fehler, 0 Warnungen.
  In den Metadaten stehen Sprache „en“, Titel, Untertitel und Andreas Rupp als Herausgeber („edt“).
- **Cover:** JPG mit 3200 × 5120 Pixeln. Das ist doppelt so groß wie die KDP-Empfehlung, im Verhältnis 1,6 : 1.

### Druck (`ausgabe/english/print/`)

| Band | Inhalt | Seiten | Rücken Taschenbuch | Rücken Hardcover | Umschlag Taschenbuch | Umschlag Hardcover |
|---|---|---|---|---|---|---|
| Volume 1 | Genesis to 1 Samuel | 457 | 1,029 Zoll | 1,218 Zoll | 17,779 × 11,25 Zoll | 19,294 × 12,418 Zoll |
| Volume 2 | 2 Samuel to Psalms | 475 | 1,070 Zoll | 1,259 Zoll | 17,820 × 11,25 Zoll | 19,335 × 12,418 Zoll |
| Volume 3 | Proverbs to Malachi | 457 | 1,029 Zoll | 1,218 Zoll | 17,779 × 11,25 Zoll | 19,294 × 12,418 Zoll |
| Volume 4 | Matthew to Revelation | 519 | 1,169 Zoll | 1,358 Zoll | 17,919 × 11,25 Zoll | 19,434 × 12,418 Zoll |

Je Band gibt es drei Dateien. `N` ist die Nummer des Bandes:
- `bible-plain-language-print-volume-N-innenteil.pdf`: der Innenteil. Er ist **für Hardcover und Taschenbuch gleich**.
- `bible-plain-language-print-volume-N-umschlag-hardcover.pdf`: der Umschlag für das **Hardcover**.
- `bible-plain-language-print-volume-N-umschlag.pdf`: der Umschlag für das **Taschenbuch**.
- Dazu gibt es Vorschaubilder (`…-vorschau.png`). Sie sind nur zum Ansehen und werden nicht hochgeladen.

Technische Daten:
- **Innenteil:** 8,25 × 11 Zoll (594 × 792 pt), ohne Beschnitt. Alle Schriften sind eingebettet.
- **Ränder:** innen 0,8 Zoll, außen 0,45 Zoll. Das erfüllt die KDP-Vorgaben.
- **Umschläge:** 600 dpi. Jeder Umschlag ist ein flaches Bild in einem PDF in exakter Größe und 12–14 MB groß.
- **Rücken:** Die Schrift sitzt genau in der Mitte.
- **Barcode:** Die Fläche unten rechts auf der Rückseite ist frei für den Barcode von KDP.

---

## 2. Hochladen bei KDP (kdp.amazon.com)

Für jeden Band gibt es bis zu drei Ausgaben: Kindle eBook, Paperback und Hardcover.
Bei allen drei müssen **Titel, Untertitel, Autor und Reihe genau gleich** sein. Dann verknüpft Amazon sie auf einer Produktseite.

### Kindle eBook
1. Wähle „+ Create“ → „Kindle eBook“.
2. Fülle die Angaben aus (siehe Abschnitt 3).
3. **Manuscript:** Lade die `.epub`-Datei hoch.
4. **Cover:** Wähle „Upload a cover you already have“ und lade die passende `-cover.jpg` hoch.
5. Blättere das Buch im Kindle Previewer durch. Achte besonders auf das Inhaltsverzeichnis, das Kapitelraster und die Kästen.

### Paperback (Taschenbuch)
- **Print ISBN:** die kostenlose KDP-ISBN, oder eine eigene.
- **Ink and paper:** Black & white interior, **white paper**.
- **Trim size:** **8.25 × 11 in**.
- **Bleed:** **No bleed**.
- **Cover finish:** **Matte**.
- **Manuscript:** `…-innenteil.pdf`.
- **Cover:** Wähle „Upload a cover you already have“ und lade `…-umschlag.pdf` hoch.

### Hardcover
- Wie beim Taschenbuch: schwarzweiß, weißes Papier, **8.25 × 11 in**, **No bleed**, **Matte**.
- **Manuscript:** dieselbe Datei `…-innenteil.pdf`.
- **Cover:** `…-umschlag-hardcover.pdf`.

### Prüfen vor der Freigabe
- **Umschlag:** Vergleiche die Maße mit dem KDP-Cover-Rechner. Gib dort Format, weißes Papier und die Seitenzahl aus der Tabelle oben ein.
  Weicht ein Wert ab, ändere die Werte oben in `werkzeuge/druck/druck_bauen.py` und baue nur die Umschläge neu:
  `UMSCHLAG_DPI=600 BIBEL_SPRACHE=en python3 werkzeuge/druck/druck_bauen.py --nur-umschlag`
- **Print Previewer:** Sieh jeden Band im Print Previewer durch.
- **Probeexemplar:** Bestelle am besten von jedem Band eins. Achte beim Hardcover auf Rücken und Einschlag.

---

## 3. Angaben bei KDP (auf Englisch eintragen)

- **Language:** English.
  **Marketplace:** amazon.com (USA) als Hauptmarkt, dazu .co.uk, .ca und .com.au.
- **Book Title:** The Bible in Plain Language
- **Subtitle:**
  - Gesamtausgabe: `Complete Edition – Old and New Testament, with an explanation after every section`
  - Volume 1: `Volume 1 – Old Testament: Genesis to 1 Samuel`
  - Volume 2: `Volume 2 – Old Testament: 2 Samuel to Psalms`
  - Volume 3: `Volume 3 – Old Testament: Proverbs to Malachi`
  - Volume 4: `Volume 4 – New Testament: Matthew to Revelation`
- **Series:** `The Bible in Plain Language`, Volume 1–4. Die Gesamtausgabe erscheint ohne Reihe.
- **Author / Contributors:** Andreas Rupp, Rolle **Editor**. So steht es auf der Titelseite, im Impressum und in den E-Book-Metadaten.
- **Description:**
  > The whole Bible in plain, easy English – every verse, every name, every number. Short sentences, one thought
  > on every line. After every section, a box called “What does this mean?” explains what you have read and
  > what it can mean for us today. Based on the public-domain World English Bible.
- **Keywords:** plain English Bible; easy to read Bible; Bible for beginners; simple English Bible;
  Bible with explanations; Bible study notes; easy Old and New Testament
- **Categories:** Religion › Bibles › Other English Translations; Religion › Biblical Studies › General
- **AI-generated content:** **Yes.** Der Text und die Erklärungen wurden mit KI (Claude) erstellt.
- **Public domain:** Die Grundlage ist die gemeinfreie World English Bible (WEB). Der englische Text ist eine neue, eigene Übertragung in einfaches Englisch mit eigenen Erklärungen. Es wurde nur aus der WEB gearbeitet, keine anderen Bibelübersetzungen.
  Lies vor dem Veröffentlichen die KDP-Hilfeseite „Public domain content“ und fülle das Formular entsprechend aus.
- **Marke:** „World English Bible“ ist eine Marke. Im Buch steht sie nur als Quellenangabe. Verwende sie nicht in Titel, Untertitel oder Keywords.
- **Plain Language:** Das Buch hat kein offizielles Prüfsiegel. Behaupte bei KDP nichts anderes.

---

## 4. Qualitätsprüfung (abgeschlossen)

- **Vergleich mit der WEB:** Jedes der 1.189 Kapitel wurde Vers für Vers mit der WEB verglichen: ob alles vollständig ist, ob die Bedeutung stimmt, ob Namen und Zahlen stimmen. Formulierungen, die anderen Bibelübersetzungen ähnelten, wurden ersetzt.
- **Einheitliche Begriffe:** Die Begriffsliste in `STYLE-EN.md` gilt für die ganze Ausgabe. Dazu gehören:
  - Zahlen ab 10 als Ziffern;
  - US-Maße;
  - Hilfe-Telefonnummern für die USA und Großbritannien.
- **Rechtschreibung und Grammatik:** Alles wurde mit LanguageTool (en-US) geprüft. Jeder Fund wurde einzeln angesehen.
- **Prüfprogramme:** Alle melden 0:
  - `python3 werkzeuge/pruefung/englisch_pruefen.py` prüft Vollständigkeit und Struktur.
  - `python3 werkzeuge/pruefung/zitate_en.py` prüft, ob die Zitate in den Kästen wörtlich stimmen.
  - `python3 werkzeuge/pruefung/anfuehrung_en.py` prüft die Anführungszeichen.

## 5. Neu bauen (nur wenn sich am Text etwas ändert)

```
BIBEL_SPRACHE=en node werkzeuge/ebook/cover_bauen.mjs                      # E-Book-Cover
BIBEL_SPRACHE=en python3 werkzeuge/ebook/ebook_bauen.py                    # EPUBs
UMSCHLAG_DPI=600 BIBEL_SPRACHE=en python3 werkzeuge/druck/druck_bauen.py   # Innenteile + Umschläge
```

Ändert sich der Text, ändert sich vielleicht die Seitenzahl und damit die Breite des Rückens. Baue deshalb Innenteil und Umschläge immer zusammen neu.

Die Texte liegen in `texte/plain-english/`, die Quelle (WEB) in `texte/englisch-web/`.
