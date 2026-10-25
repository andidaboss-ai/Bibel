# Task: clean, faithful transcription of Prentice Mulford, "Thoughts Are Things — Essays Selected from the White Cross Library" (London: G. Bell and Sons; public domain)

Folder: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/mulford/src/
- a.txt / a.pdf (192 pages) = OCR + scan of the 1920 printing ("Nineteenth Thousand"). PRIMARY.
- b.txt / b.pdf (200 pages) = OCR + scan of the 1923 printing. Use it to correct OCR errors in a.
  If the printings differ in wording (not just OCR), follow 1920 (a) and note it.
- When unsure, render the page: `pdftoppm -r 110 -png -f N -l N a.pdf /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/mulford/img/<prefix>-p`
  (find N with `pdftotext -f N -l N a.pdf -`), then Read the PNG.
- Ignore the publisher's advertisement pages ("Life and Light Books", "New Thought Books"), library stamps,
  Internet Archive notes, the printer's line at the end.

Structure: Preface (signed "J. W."), then 13 essays:
1 The Material Mind v. the Spiritual Mind · 2 Who Are Our Relations? · 3 Thought Currents · 4 One Way to
Cultivate Courage · 5 Look Forward · 6 God in the Trees · 7 Some Laws of Health and Beauty · 8 Museum and
Menagerie Horrors · 9 The God in Yourself · 10 Healing and Renewing Force of Spring · 11 Immortality in the Flesh ·
12 Attraction of Aspiration · 13 The Accession of New Thought
(Use the heading as printed at the top of each essay in title case; if it differs from this list, say so.)

Output (Markdown), YOUR PART ONLY, into the file named in your assignment:
- `## <Title>` per section (`## Preface` for the preface; keep the signature "J. W." as its own last paragraph).
- Paragraphs separated by one blank line. Sub-headings inside essays (if any) as `### …` exactly as printed.
- Keep the wording, spelling (British spelling of this edition), punctuation, italics (`*…*`) and capitalization
  exactly. Do NOT modernize. Fix only OCR damage: rejoin hyphenated line breaks (keep real compounds), remove page
  numbers and running heads, fix misread letters; curly quotes “ ” ‘ ’, apostrophe ’, em dash —. Drop-cap first
  letters that the OCR split off ("LTHOUGH" → "Although") must be restored.
- Check completeness paragraph by paragraph against both OCRs; nothing missing, nothing doubled; decide
  paragraph breaks at page turns from the page image (indent = new paragraph).

Do not touch other parts. Final report (short): your file, word count, sections, unclear places and decisions.
