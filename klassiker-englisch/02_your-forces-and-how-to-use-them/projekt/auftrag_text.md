# Task: clean, faithful transcription of Christian D. Larson, "Your Forces and How to Use Them" (1912, public domain)

Folder: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/src/
- a.txt = OCR of the Digital Library of India scan (a.pdf, 342 pages). PRIMARY for the chapters.
- b.txt = OCR of a second 1912 scan (b.pdf, 361 pages; Google scan). Use it to correct OCR errors in a.txt,
  and as the ONLY source of the "PROMISE YOURSELF" creed (b.txt around line 408), which is not in a.txt.
  Ignore all Google / Internet Archive / library boilerplate.
- When the two OCRs disagree and you can't tell, render the page image and look:
  `pdftoppm -r 110 -png -f N -l N a.pdf /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/img/<yourpart>-p` (find N by searching the text layer with
  `pdftotext -f N -l N a.pdf -`), then Read the PNG.

Chapter titles (from the contents page, OCR-corrected — use exactly these):
I The Ruling Principle in Man · II How We Govern the Forces We Possess · III The Use of Mind in Practical Action ·
IV The Forces of the Subconscious · V Training the Subconscious for Special Results · VI The Power of Subjective
Thought · VII How Man Becomes What He Thinks · VIII The Art of Changing for the Better · IX He Can Who Thinks He Can ·
X How We Secure What We Persistently Desire · XI Concentration and the Power Back of Suggestion · XII The
Development of the Will · XIII The Building of a Great Mind · XIV How Character Determines Constructive Action ·
XV The Art of Building Character · XVI The Creative Forces in Man · XVII The Building Power of Constructive Speech ·
XVIII Imagination and the Master Mind · XIX The Higher Forces in Man · XX The Greatest Power in Man
(If the chapter heading inside the book differs slightly from the contents, follow the heading in the book and say so.)

Output format (Markdown), YOUR PART ONLY, into the file named in your assignment:
- `## <Chapter title>` per chapter (no "Chapter I" text; the numbering is added by the layout).
- For the Foreword: `## Foreword`. For the creed: `## Promise Yourself` followed by each "To …" line as its own paragraph.
- Paragraphs separated by one blank line. If the book has sub-headings or numbered points inside a chapter, keep
  them (`### …` for sub-headings, numbered points as paragraphs starting with the number as printed).
- Keep Larson's wording, spelling, punctuation, italics (`*…*`) and capitalization exactly (1912 American English).
  Do NOT modernize. Fix only OCR damage: rejoin hyphenated line breaks, remove page numbers and running heads
  ("Your Forces and How to Use Them", "Foreword", chapter running titles), fix misread letters, use curly quotes
  “ ” ‘ ’, apostrophe ’, em dash —.
- Check completeness paragraph by paragraph against both OCRs; nothing missing, nothing doubled, no page-break
  splits left in the middle of a paragraph.

Do not touch other parts. Final report (short): your file, word count, chapters, unclear places and decisions.
