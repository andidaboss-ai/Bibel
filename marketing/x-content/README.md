# X-Content-Strategie: 200 Tage, 2 Kanäle

Dieser Ordner enthält einen Redaktionsplan mit einem fertigen Post pro Tag für 200 Tage (Tag 1–100 plus Vorrat Tag 101–200), für zwei englische X-Kanäle:

| Kanal | Handle | Inhalt | Quelle |
|---|---|---|---|
| **The Bible – Simply Explained** | @BibleSimplyExpl | Bibel in einfachem Englisch, mit Erklärungen | nur `texte/plain-english/` |
| **Ancient Book Wisdom** | (Handle folgt) | Alte englische gemeinfreie Klassiker | nur die 9 Bücher in `klassiker-englisch/` |

## Ziele
1. **Follower gewinnen.** Jeder Post soll beim Scrollen stoppen und einen echten Gedanken fürs Leben mitgeben, nicht nur ein Zitat.
2. **Vertrauen aufbauen.** Täglich verlässlich, warm und ohne Streit oder Belehrung.
3. **Verkauf.** Die Leute sollen merken, wie verständlich die Bücher sind, und über den Link in der Bio kaufen.

## Inhaltliche Säulen
**Bibel:** berühmte Geschichten (David, Josef, Rut, Ester, Daniel, Jona, verlorener Sohn …), Trost bei Angst und Sorgen, Beziehungen und Worte, Identität und Sinn, schwere Zeiten, Vergebung und Gnade, Hoffnung. Keine theologischen Streitfragen und keine politischen oder nationalistischen Inhalte.

**Klassiker:** Stoizismus (Marcus Aurelius, Epiktet), Tao Te Ching, „Mind Power“-Klassiker (Shinn, Larson, Atkinson, Mulford) und stiller Glaube (Bruder Lorenz, Thomas von Kempen). Die 9 Bücher wechseln sich ab, und jede Woche hat ein Thema.

## Wochenrhythmus (7-Tage-Zyklus, beliebig auf Wochentage legbar)
| Tag im Zyklus | Bibel | Klassiker |
|---|---|---|
| 1 | Proverb of the Week (Sprüche) | Stoic Mindset |
| 2 | Story in 60 Seconds (Thread) | Tao for Busy Minds |
| 3 | What It Really Means | Mind Power Classics |
| 4 | Words of Jesus | Quiet Faith |
| 5 | Myth vs. Truth / Thread | Then vs. Now / Thread |
| 6 | Your Turn (Frage für Antworten) | Your Turn (Frage) |
| 7 | Sunday Rest (Psalm) + **sanfter CTA** | Book Spotlight + **sanfter CTA** |

## 100-Tage-Bogen
- **Bibel:** In Woche 1–2 kommen die bekanntesten Verse und Geschichten, um Reichweite aufzubauen. Danach folgen Angst und Mut, Freundschaft und Worte, Identität, schwere Zeiten, Vergebung und Hoffnung. Tag 100 schließt mit Offenbarung 21,4.
- **Klassiker:** Die Wochenthemen sind Morgen und Mindset, Kontrolle, Ruhe, Mut, Worte und Gedanken, Umgang mit anderen, Arbeit, Einfachheit, Glaube, Rückschläge, Zeit, Dankbarkeit, Wachstum und Durchhalten.

## Tag 101–200: Vorrat und zweiter Tages-Slot
- Start: **ein Post pro Tag** (Tag 1–100), dazu täglich 10–20 Minuten aktiv kommentieren.
- Nach etwa **4–6 Wochen** (oder ab ein paar hundert Followern) geht es auf **2 Posts pro Tag**: morgens ein kurzer Post, abends die ausführliche Lektion oder ein Thread mit Bild.
- Die Tage 101–200 sind dafür der Vorrat: Sie füllen den zweiten Slot, sodass Tag 1–100 und 101–200 parallel laufen können. Kurze Posts eignen sich eher morgens, Threads und Bild-Posts eher abends.
- Kein Vers und kein Zitat aus Tag 1–100 wird in Tag 101–200 wiederholt (per Skript geprüft). Gleicher 7-Tage-Rhythmus, gleiche Serien.
- Inhalte: `werkzeug/bible_data2.py` und `werkzeug/classics_data2.py`. Neue Tao-Zitate (Kapitel 24, 33, 64, 67, 81) wurden in `kq.json` ergänzt.

| Kanal | Tage | Bilder | Threads | sanfte CTAs |
|---|---|---|---|---|
| Bibel | 1–100 | 64 | 22 | 14 |
| Bibel | 101–200 | 73 | 20 | 15 |
| Klassiker | 1–100 | 45 | 7 | 14 |
| Klassiker | 101–200 | 56 | 8 | 15 |

## Links und Kaufpfad
- **Keine Links in Posts.** X zeigt Posts mit externen Links deutlich weniger Leuten.
- **Ein Link in der Bio ist erlaubt und sinnvoll.** Er kann auf die spätere Website führen, von dort zu Amazon und Payhip. Alternativ kann ein angehefteter Post mit Link genutzt werden, oder der Link steht in der ersten Antwort unter einem Post (für Reichweite weniger schädlich).
- Etwa jeder 7. Post enthält einen sanften Hinweis wie „link in bio“, insgesamt 14 von 100 pro Kanal (Tag 101–200: 15 von 100).
- Der Kaufpfad: Post → Profil → Bio-Link → Website → Buch. Deshalb muss die Bio den Nutzen klar sagen.

## Wachstumstaktiken
- Mindestens 15 Minuten täglich auf Antworten reagieren, besonders bei den „Your Turn“-Fragen. Antworten zählen bei X stark.
- Bei großen Accounts im Bereich Glaube, Stoizismus und Self-Improvement früh und wertvoll kommentieren.
- Gute Threads anheften und Bestseller-Posts nach 6–8 Wochen mit neuem Bild wiederholen.
- Bilder (Prompts sind in jeder Datei) erhöhen die Verweildauer. Den Stil einheitlich halten: Bibel in Mitternachtsblau mit Goldlinien, Klassiker als Sternenhimmel mit Gold-Icon und Serifenschrift.
- Höchstens 1–2 Hashtags, zum Beispiel #Bible, #Stoicism oder #Wisdom, und nur bei passenden Posts.
- Die Zeiten sind in UTC angegeben, für Publikum in den USA und Großbritannien. Für Berlin gilt im Winter UTC+1.

## Aufbau der Dateien
- `bible-simply-explained/day-001.md` … `day-200.md` und `index.csv`
- `ancient-book-wisdom/day-001.md` … `day-200.md` und `index.csv`
- Jede Tagesdatei enthält Serie, Format, beste Uhrzeit, CTA ja/nein, den **fertigen Post-Text** (bei Threads nummerierte Teile mit Zeichenzahl), den Bild-Prompt, den Alt-Text und die Quelle mit Dateipfad.
- `werkzeug/`: Die Inhalte stehen in `bible_data.py`/`bible_data2.py` und `classics_data.py`/`classics_data2.py`. `python3 werkzeug/gen.py` baut alle Dateien neu und prüft dabei:
  - jeden Teil auf höchstens 280 Zeichen (Emojis zählen doppelt),
  - jedes Zitat **wortgetreu** gegen die Quelldatei. Bibelzitate werden direkt aus den Versen in `texte/plain-english` übernommen, Klassikerzitate aus `projekt/book/text/original.md`.

## Benutzung
1. Den Text aus dem `text`-Block kopieren und posten, bei Threads Teil für Teil als Antwortkette.
2. Wenn „Image: yes“ steht, das Bild mit dem Prompt erzeugen und den Alt-Text eintragen.
3. Die Posts können auch vorab geplant werden, über X-Planung oder ein Tool wie Typefully oder Buffer.
4. Nach 30 Tagen die besten Formate in X Analytics prüfen und den Plan anpassen.

Stand: Oktober 2026. Erstellt von Bibelprojekt-Bot.
