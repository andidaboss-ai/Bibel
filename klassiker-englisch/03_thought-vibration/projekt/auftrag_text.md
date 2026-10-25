# Task: clean, faithful transcription of William Walker Atkinson, "Thought Vibration, or the Law of Attraction in the Thought World" (1906, public domain)

Folder: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/src/
- b.txt / b.pdf (167 pages) = OCR + scan of the 1906 first edition (New Thought Publishing Co., Chicago). PRIMARY.
- a.txt / a.pdf (161 pages) = OCR + scan of a 1908 printing (The Library Shelf). Use it to correct OCR errors in b.
  If the two printings differ in wording (not just OCR), follow the 1906 edition (b) and note it.
- When unsure, render the page and look: `pdftoppm -r 110 -png -f N -l N b.pdf /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/img/<prefix>-p`
  (find N with `pdftotext -f N -l N b.pdf -`), then Read the PNG.
- Ignore Google/Internet Archive/library stamps, and the publisher's advertising pages after the last chapter.

The book's structure: Preface (by Franklin L. Berry, Editor of New Thought, with the closing acknowledgement and
signature), Foreword (by Atkinson), My Working Creed, then 16 chapters. The CONTENTS pages give, for each part and
chapter, a short italic-style summary ("In which we learn …" / a list of topics separated by dashes).

Output (Markdown), YOUR PART ONLY, into the file named in your assignment:
- `## <Title>` per part/chapter. Titles in normal title case as in the book (e.g. `## The Law of Attraction in the
  Thought World`, `## Preface`, `## Foreword`, `## My Working Creed`). No "Chapter I" text — the layout numbers them.
- Directly after each `##` line, the summary of that part/chapter from the CONTENTS pages as ONE line starting with
  `%% ` (keep the dashes between topics as em dashes —, exactly the 1906 wording, OCR fixed).
- Then the text. Paragraphs separated by one blank line. Sub-headings inside chapters as `### …` exactly as
  printed. Lists or exercises as printed. Keep the Preface signature lines as separate short paragraphs.
- Keep Atkinson's wording, spelling, punctuation, italics (`*…*`), capitalization, emphasis in CAPITALS exactly
  (1906 American English). Do NOT modernize. Fix only OCR damage: rejoin hyphenated line breaks, remove page
  numbers and running heads, fix misread letters; curly quotes “ ” ‘ ’, apostrophe ’, em dash —.
- Check completeness paragraph by paragraph against both OCRs; nothing missing, nothing doubled.

Do not touch other parts. Final report (short): your file, word count, sections, unclear places and decisions.
