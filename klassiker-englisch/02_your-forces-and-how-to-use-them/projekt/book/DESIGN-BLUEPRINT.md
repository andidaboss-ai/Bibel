# Design-Blueprint für kommentierte Klassiker

Diese Vorlage gilt für alle kommenden Bücher der Reihe, also gemeinfreie Klassiker mit eigenem Kommentar.
Für ein neues Buch: Ordner kopieren, `book.json` und `text/*.md` ersetzen, `python3 tools/build.py` ausführen.

## Format
- **Druck:** 6 × 9 Zoll als Taschenbuch und Hardcover, Innenteil schwarzweiß, weißes Papier, ohne Beschnitt.
- **E-Book:** EPUB 3. Das Cover ist ein JPG mit 3200 × 5120 Pixeln.
- **Umschläge:** 600 dpi. Die Maße werden aus der Seitenzahl berechnet (KDP weißes Papier: 0,002252 Zoll pro Seite).

## Schriften
Alle Schriften stehen unter der SIL Open Font License und liegen in `fonts/`.

| Rolle | Schrift | Satz |
|---|---|---|
| Grundtext | EB Garamond | 11,4/16 pt, Blocksatz mit Silbentrennung, `text-wrap: pretty`, Mediävalziffern |
| Titel, Kapitel, Affirmationen | Cormorant Garamond | Medium/SemiBold, kursiv für Zitate und Affirmationen |
| Labels, Kolumnentitel | Jost | Versalien, stark gesperrt (0,3–0,5 em) |

## Satzspiegel
- **Ränder:** oben 0,86 Zoll, unten 0,92 Zoll, Bundsteg (innen) 0,9 Zoll, außen 0,66 Zoll. Das ergibt etwa 62–66 Zeichen pro Zeile.
- **Absätze:** Einzug 1,15 em, kein Abstand. Nach Überschriften, Zitaten und Trennern beginnt der Absatz ohne Einzug.
- **Seitenumbruch:** keine Witwen und Waisen (je 2 Zeilen). Überschriften und Labels bleiben beim folgenden Text.

## Seitengestaltung
- **Kolumnentitel:** Sie werden als Overlay gesetzt.
  - Linke Seite: Buchtitel, oben außen.
  - Rechte Seite: Kapiteltitel, oben außen.
  - Kapitelanfänge, Titelei und Leerseiten bekommen keinen Kolumnentitel.
- **Pagina:** unten auf die Mitte des Satzspiegels, EB Garamond 9,6 pt. Auf Kapitelanfängen steht nur die Pagina, in der Titelei gar keine.
- **Titelei, in dieser Reihenfolge:**
  1. Schmutztitel
  2. Titelseite (rechts)
  3. Impressum mit Hinweis zu Gemeinfreiheit und KI/Gesundheit
  4. Motto (rechts)
  5. Inhalt (rechts), Seitenzahlen automatisch, mit Teil-Labels
- **Teile und Kapitel:**
  - Einleitungsteile beginnen rechts.
  - Vor dem Originaltext steht ein Zwischentitel (rechts).
  - Jedes Kapitel beginnt auf einer neuen Seite.

## Kapitelanfang
- **Aufbau:** 1,05 Zoll Vorschlag (Leerraum über dem Titel), darüber das Label „CHAPTER“ in Jost, darunter die römische Zahl in Cormorant und der Titel in Cormorant SemiBold 27 pt.
- **Ornament:** Linie, Punkt, Stern, Punkt, Linie.
- **Erster Absatz:**
  - Initiale über 2 Zeilen in Cormorant SemiBold.
  - Die ersten Wörter in echten Kapitälchen.
  - Ist der Absatz kürzer als 120 Zeichen, gibt es nur Kapitälchen und keine Initiale.

## Elemente
- **Affirmationen des Autors:**
  - Zentriert, Cormorant kursiv 13,2 pt, mit ausgeglichenen Zeilen.
  - Kleiner Stern als Trenner zwischen den Gruppen.
  - Label „— AFFIRMATIONS —“ mit Haarlinien.
- **Begleittext nach jedem Kapitel:**
  - Haarlinie mit Stern.
  - Darunter die Labels REFLECTION und PRACTICE, Text in 10,6/14,8 pt.
  - KEY AFFIRMATION zwischen zwei Linien.
  - Danach 4 Schreiblinien („My own words“).
- **Übungsseiten:** Jeder Tag hat eine eigene Seite.
  - Oben „DAY“, darunter eine große Ziffer (Cormorant 54 pt), Thema, Ornament.
  - Dann die Affirmation in 16 pt, die Quelle und die Aufgabe.
  - Darunter 6 Schreiblinien und eine Checkliste.
- **Anführungszeichen:** Gerade Anführungszeichen werden automatisch zu typografischen (“ ” ‘ ’ …).

## Cover
- **Hintergrund:** Nachthimmel als radialer Verlauf von Indigo zu Schwarzblau, Sternenfeld, goldene Doppellinie als Rahmen.
- **Mitte:** ein Emblem in Gold-Linienkunst, für jedes Buch neu als Motiv zum Titel gezeichnet (hier ein Zauberstab mit Sternexplosion).
- **Titel:** Cormorant SemiBold mit Goldverlauf. Autor in Jost gesperrt oben, Ausgabe in Jost unten mit kursivem Untertitel.
- **Rückseite:**
  - Kicker
  - dreizeilige Headline in Gold
  - zwei Absätze Klappentext
  - fünf Punkte mit Stern
  - Zitat aus dem Buch
  - Barcodefläche unten rechts frei
- **Rücken:** Titel in Cormorant, Stern, Autor in Jost. Bei weniger als 0,3 Zoll Rückenbreite bleibt der Rücken ohne Schrift.
- Der Name des Herausgebers steht nicht auf dem Cover, nur im Buch (Titelseite, Impressum).

## KDP-Regeln für gemeinfreie Texte
- **Titel:** mit „(Annotated)“. Die Beschreibung beginnt mit einer Liste, was an dieser Ausgabe neu ist.
- **Eigene Zusätze:** Einleitung, Biografie, historischer Kontext, Kommentar zu jedem Kapitel, Übungsteil.
- **Rechte:** Text des Originals in den USA und in der EU gemeinfrei, also Autor seit mindestens 70 Jahren tot und Erstausgabe vor 1931.
