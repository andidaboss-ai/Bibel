# Task: prepare a clean, print-ready English text (Wallace D. Wattles, complete works)

Working folder: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/wattles/
We publish the public-domain originals on Amazon KDP. The text must be EXACTLY Wattles' wording, complete, with
OCR errors removed — nothing added, nothing omitted, nothing modernised (keep his spelling, punctuation, capitals and
italics; only fix obvious OCR/printing errors). Sources are raw OCR or reprints; where page images exist, CHECK them
with the Read tool whenever the OCR is doubtful (missing drop-cap letters, garbled words, decorated pages, chapter
headings, line-end hyphens, page breaks that split paragraphs).

Output format (Markdown), one file per work in eng/:
- `## <Chapter title>` per chapter, title in title case WITHOUT the chapter number (e.g. `## The Source of Power`).
  An author's preface: `## Preface`; a closing summary: `## A Summary of …` as in the source.
- Paragraphs separated by one blank line; restore paragraphs split at page breaks; remove running heads, page numbers,
  printer's marks, illustration captions, publisher advertisements, modern copyright lines.
- Italics as `*…*`; words in SMALL CAPS/ALL CAPS used for emphasis stay as in the source (e.g. `POSITIVE`);
  block quotations / chapter mottoes as `> ` lines (source line as `> — Author`); verse lines with `| ` prefix;
  in-chapter sub-headings as `### `; author footnotes: superscript marker in the text (¹ ²) and the note as a line
  `~~ ¹ text` at the end of the chapter.
- Use typographic quotes “ ” ‘ ’, apostrophe ’, dashes — as in the source.
Self-check: compare your word count per chapter against the source (should be within a few percent, minus junk);
read each chapter once more against the source/page images. Report briefly: chapters, word counts, every place where
you had to reconstruct text and how, anything uncertain.
