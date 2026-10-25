# Task: write the original editorial material for "Thought Vibration (Annotated)"

Book: William Walker Atkinson, "Thought Vibration, or the Law of Attraction in the Thought World" (1906, public
domain). Clean original text: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/book/text/original.md
(`## Preface` by the 1906 editor Franklin L. Berry, `## Foreword`, `## My Working Creed`, then 16 chapters as
`## Title`; each section starts with a `%% ` line = the 1906 chapter summary from the original contents). Do NOT
change the original text.

We publish an annotated edition on Amazon KDP. KDP accepts public-domain books only when clearly differentiated
by ORIGINAL added material. Everything you write must be your own original writing. Never copy or paraphrase other
editions, commentaries, Wikipedia sentences or books about Atkinson. Facts are fine; wording must be yours.

Audience: modern readers (25–60, US/UK) interested in the Law of Attraction, manifesting, mindset, New Thought,
self-discipline; many know "The Secret" era books (do not name living authors, films or brands). Tone: clear,
warm, energetic, grounded, modern, never preachy, never hype. Plain American English. Short paragraphs.

Honesty rules (very important):
- No promises of wealth, health, love or guaranteed results. Present Atkinson's claims as his teaching
  ("Atkinson argues…", "In his view…").
- 1906 "science": thought as literal vibrations/waves, telepathy, Marconi analogies, "thought-waves" travelling
  between people, heredity of habits. Say kindly and clearly that these are metaphors or speculations of his time,
  not established science — and then give what still holds up: attention shapes perception, expectations and
  self-talk influence behaviour, habits, emotions are contagious in groups, practice changes the mind, action
  matters. Do not overclaim modern research either; keep it general.
- Wherever he touches health, fear, worry or the body, add that the practices go alongside — never instead of —
  medical or psychological care. For persistent fear/worry mention talking to a doctor or therapist.
- No victim-blaming: the idea that people "attract" misfortune must be framed with care (illness, poverty, abuse
  are not anyone's fault).
- Explain dated language neutrally ("man" meaning all people, 1906 terms). Bible references only when sure.

Write these files into /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/book/text/ (Markdown):

1. `front.md`
   - `## How to Use This Book` (350–450 words): what Atkinson means by the Law of Attraction in the thought world,
     how this edition is built (original untouched incl. the 1906 chapter summaries; after each chapter
     "Reflection", "Practice", "Key Thought"; the 30-day practice; the Quick Finder), tips.
   - `## About William Walker Atkinson` (500–700 words): facts you are sure of: born December 5, 1862, in
     Baltimore, Maryland; worked in business, then became a lawyer (admitted to the bar in Pennsylvania); breakdown
     from overwork and recovery through New Thought (the Preface mentions this); moved to Chicago; editor of the
     magazine *New Thought* (from 1901, Sydney Flower's New Thought Publishing Co.), later his own magazine
     *Advanced Thought*; extremely prolific, wrote under his own name and many pen names (e.g. Yogi Ramacharaka,
     Theron Q. Dumont) — mention pen names only in general terms if unsure; died November 22, 1932, in California.
     If you are not sure about a detail, leave it out.
   - `## The World of New Thought` (300–450 words): short context (Quimby, Emerson, Chicago as a New Thought
     publishing centre around 1900, the phrase "law of attraction" in New Thought writing), his place in it.
   - `## A Note on This Edition` (150–250 words): follows the 1906 first edition, spelling kept, obvious printing
     errors corrected; the 1906 chapter summaries kept under each title; the Preface by Franklin L. Berry is part of
     the 1906 book; dated science and language; editorial material is new.

2. `chapters.md` — for EVERY section of original.md EXCEPT `Preface` and `Foreword`, in the same order:
   ```
   ## <exact section title>
   ### Reflection
   <170–280 words: key idea in plain modern words, main arguments, one or two of his examples briefly retold,
   what still holds up, what is dated, how a reader can use it>
   ### Practice
   <a concrete exercise, 50–110 words, numbered steps allowed>
   ### Key Thought
   > <one sentence quoted EXACTLY, word for word, from this section of original.md (not from the %% line)>
   ```
   For "My Working Creed": Reflection 120–200 words, Practice = writing one's own "I believe" creed.

3. `thirty_days.md` — `## The 30-Day Practice`, a 150–250 word introduction, then `### Day 1 – <Theme>` …
   `### Day 30 – <Theme>`. Each day: one sentence quoted EXACTLY from original.md (as a `>` quote), then
   `Source: <Section title>` on its own line, then a 2–4 sentence task (your words). Arc: week 1 thought as a force
   and noticing one's mental climate; week 2 mind-building, will, fear; week 3 worry, mental control, focus,
   desire; week 4 the later chapters (find their themes in original.md), days 29–30 the creed and commitment.

4. `finder.md` — `## Quick Finder`: 15–25 everyday situations, each pointing to chapter(s) and day(s).
   Format: `- **Situation** — Chapter title, Chapter title · Day N`.

5. `back.md` — `## Afterword: The Climate of Your Mind` (250–400 words) and `## Further Reading` (only classic
   public-domain titles with year you are sure of: Prentice Mulford, *Thoughts Are Things* (1889); Ralph Waldo
   Trine, *In Tune with the Infinite* (1897); James Allen, *As a Man Thinketh* (1903); Wallace D. Wattles,
   *The Science of Getting Rich* (1910); Christian D. Larson, *Your Forces and How to Use Them* (1912); Florence
   Scovel Shinn, *Your Word Is Your Wand* (1928); William James, *The Energies of Men* (1907); Emerson,
   *Essays: First Series* (1841)). Mention that the Larson and Shinn titles are available in this same annotated
   series.

Self-check when done: every `>` quote in chapters.md and thirty_days.md must appear verbatim in original.md
(script: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/check_<yourpart>.py, normalise only whitespace and `*`;
fix until 0 misses), and the `##` titles of chapters.md must match original.md.
Final report: word counts, quote check result, anything you were unsure about.
