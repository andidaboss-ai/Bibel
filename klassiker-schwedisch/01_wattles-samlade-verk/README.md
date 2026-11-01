# Wallace D. Wattles – Samlade verk (svensk utgåva)

Komplette schwedische Ausgabe: zehn Werke + Vorwort (Willkommensgruß von Andreas Rupp), Übungen nach jedem Kapitel, 30-Tage-Programm.

- `kdp/` – fertige Dateien (Innenteil 403 S., EPUB, Cover Taschenbuch/Hardcover, eBook-Cover 10000 px) und `KDP-ANLEITUNG.md`
- `cover-preview.jpg` – Vorschau des Taschenbuch-Umschlags
- `projekt/` – Quellen: `eng/` (Original), `swe/parts/` (Übersetzung), `text/` (front, chapters, thirty_days), `book.json`
- Build: `cd projekt && python3 assemble_sv.py && python3 tools/build.py`; Prüfung: `python3 check_sv.py eng/X.md swe/X.md`

Status: **nicht bei KDP hochgeladen** – erst nach OK.
