# Auftrag: Revision der deutschen Übersetzung – Wallace D. Wattles, Gesammelte Werke

Arbeitsordner: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/wattles/
- Maßgebliche englische Vorlage (bereinigt, an den Scans geprüft): `eng/<werk>.md`
- Bisherige deutsche Übersetzung (aus teils fehlerhaften Rohvorlagen übersetzt): `de/<werk>*.md`
- Ausgabe: `deu/<werk>.md` (EIN Datei pro Werk)

Ziel: eine druckreife, vollständige, treue deutsche Fassung in makellosem Deutsch (Duden, neue Rechtschreibung).

Arbeitsschritte
1. Gehe Kapitel für Kapitel und ABSATZ FÜR ABSATZ die englische Vorlage `eng/` durch und vergleiche mit der deutschen
   Fassung. Ergänze Fehlendes, streiche Überzähliges (z. B. Text, der nur in der Rohvorlage stand), korrigiere
   Übersetzungsfehler, übernimm die Korrekturen der bereinigten Vorlage (z. B. wiederhergestellte Wörter, richtige
   Kursivierungen, Fußnoten, Zitatblöcke, Verse, Zwischenüberschriften). Die Absatzfolge soll der englischen entsprechen.
2. Einheitliche Regeln für das GANZE Buch:
   - Anrede „Sie“ (Ausnahme: Dialoge im Roman, Bibelzitate, bewusst im Du gehaltene Passagen).
   - Pronomen für Gott und Jesus KLEIN (er, ihm, sein) – im ganzen Buch einheitlich.
   - Begriffe: „auf die bestimmte Weise“ (Certain Way); „formlose Substanz“; „denkende Substanz“ (Thinking
     Substance); „denkender Stoff“ (thinking stuff); „Wachstum“ (increase); „Gebrauchswert“/„Geldwert“;
     „schöpferische Ebene“/„Ebene des Wettbewerbs“; „der aufstrebende Mensch“ (the Advancing Man);
     „Gesundheitsprinzip“, „Lebensprinzip“, „Kraftprinzip“ (Principle of Power); „Neues Denken“ für New Thought nur
     erklärend, sonst „New Thought“; „Geist“ für mind, „spirituell/Geist“ für spirit je nach Zusammenhang.
   - Bibelzitate an Luther 1912 angelehnt, aber Wattles' Wortlaut folgend.
   - Typografie: „…“ und ‚…‘, Gedankenstrich – mit Leerzeichen, Auslassung …, echte Umlaute und ß.
   - Hervorhebungen der Vorlage: *kursiv*; Wörter in VERSALIEN als Hervorhebung dürfen kursiv gesetzt werden.
3. Format: `## <deutscher Kapiteltitel>` (ohne Nummer; Vorwort des Autors: `## Vorwort`), Absätze durch Leerzeile,
   `> ` Zitatblöcke (Quellenzeile `> – Autor`), `| ` Verszeilen, `### ` Zwischenüberschriften, `%% ` für die
   Inhaltszeilen unter Kapiteltiteln (wie in eng/), Fußnoten wie in eng/ (hochgestellte ¹ im Text und Zeile
   `~~ ¹ …` am Kapitelende). Kein Kapitel „About This Work“, keine Anmerkungen des Übersetzers.
4. Prüfung: `python3 check_de.py eng/<werk>.md deu/<werk>.md` (Verhältnis Wörter DE/EN 0,85–1,35 je Kapitel,
   gleiche Kapitelzahl). Danach die ganze Datei einmal zusammenhängend Korrektur lesen (Rechtschreibung,
   Grammatik, Zeichensetzung, Stil).
5. Bericht (kurz): Kapitel, Wortzahlen, was du geändert/ergänzt hast, unsichere Stellen.
