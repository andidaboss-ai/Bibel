# English Public-Domain Classics (Annotated)

Annotated editions of public-domain classics for Amazon KDP. Each book has the same premium design (see
`09_imitation-of-christ/projekt/book/DESIGN-BLUEPRINT.md`). The original text is in the public domain in the US
(published before 1931) and in the EU (author/translator died more than 70 years ago); the commentary, practices,
30-day practice, finder, glossary, cover and interior design are new.

Each folder:

- `kdp/` — upload-ready files: interior PDF (6 × 9 in, paperback and hardcover), paperback and hardcover cover PDFs
  (600 dpi), EPUB 3, e-book cover (6250 × 10000 px) and `KDP-ANLEITUNG.md` (all KDP fields, in German with English
  texts to paste).
- `cover-preview.jpg` — preview of the paperback cover (where available).
- `projekt/` — sources to rebuild the book: `book/` (book.json, text/*.md, tools/, fonts/), conversion scripts,
  commentary briefs and quote-check scripts. Rebuild: `cd projekt/book && node tools/build_cover.mjs &&
  COVER_SCALE=3.90625 node tools/build_cover.mjs output/ebook/<slug>-cover-10000px.jpg && python3 tools/build.py`.

| No. | Book | Author / translator | Pages | Series |
|---|---|---|---|---|
| 01 | Your Word Is Your Wand (Annotated) | Florence Scovel Shinn (1928) | 157 | Annotated New Thought Classics 1 |
| 02 | Your Forces and How to Use Them (Annotated) | Christian D. Larson (1912) | 302 | Annotated New Thought Classics 2 |
| 03 | Thought Vibration (Annotated) | William Walker Atkinson (1906) | 169 | Annotated New Thought Classics 3 |
| 04 | Thoughts Are Things (Annotated) | Prentice Mulford | 221 | Annotated New Thought Classics 4 |
| 05 | Meditations (Annotated) | Marcus Aurelius, tr. George Long (1862) | 218 | Annotated Ancient Wisdom 1 |
| 06 | Tao Te Ching (Annotated) | Lao Tzu, tr. James Legge (1891) | 228 | Annotated Ancient Wisdom 2 |
| 07 | The Practice of the Presence of God (Annotated) | Brother Lawrence, Revell translation | 127 | Annotated Christian Classics 1 |
| 08 | Epictetus: Discourses and Enchiridion (Annotated) | Epictetus, tr. George Long (1877) | 263 | Annotated Ancient Wisdom 3 |
| 09 | The Imitation of Christ (Annotated) | Thomas à Kempis, tr. William Benham | 295 | Annotated Christian Classics 2 |
| 10 | As a Man Thinketh and Out from the Heart (Annotated) | James Allen (1903, 1904) | 132 | Annotated New Thought Classics 5 |

KDP: add "(Annotated)" to the title, start the description with the list of new material, declare AI-generated
text, and upload no more than about three new titles per day.
