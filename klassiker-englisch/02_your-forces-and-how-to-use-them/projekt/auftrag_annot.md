# Task: write the original editorial material for "Your Forces and How to Use Them (Annotated)"

Book: Christian D. Larson, "Your Forces and How to Use Them" (1912, public domain). The clean original text is
/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/book/text/original.md
(`## Foreword`, `## Promise Yourself` (the creed), then 20 chapters as `## Title`). Do NOT change the original text.

We publish an annotated edition on Amazon KDP. KDP accepts public-domain books only when they are clearly
differentiated by ORIGINAL added material. Everything you write must be your own original writing. Never copy
or paraphrase other editions, commentaries, Wikipedia sentences or books about Larson. Facts are fine; the
wording must be yours.

Audience: modern readers (25–60, US/UK) interested in mindset, personal growth, self-discipline, willpower,
character, the power of thought, New Thought; many also read Napoleon Hill, James Allen, Wattles. Tone: clear,
warm, energetic, grounded, modern, never preachy, never hype. Plain American English. Short paragraphs.

Honesty rules (very important):
- No promises of wealth, health or guaranteed success. Present Larson's claims as his teaching ("Larson
  argues…", "In his view…"). Where 1912 "psychology" is outdated or speculative (e.g. claims about the
  subconscious curing disease, heredity, "the race"), say so briefly and kindly, and give what still holds up
  (habits, attention, self-talk, practice, character).
- Wherever Larson touches health or the body, add that the practices go alongside — never instead of — medical
  care.
- Explain dated language neutrally ("man" meaning all people, "the race" meaning humanity, 1912 terms).
- Bible quotations or allusions: give the reference only when you are sure (KJV-era wording).
- The creed "Promise Yourself": mention that it first appeared in this book (1912) and later became widely known
  as "The Optimist Creed", adopted by Optimist International (in the early 1920s). Do not claim more than that.

Write these files into /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/book/text/ (Markdown):

1. `front.md`
   - `## How to Use This Book` (350–450 words): what Larson means by "forces", how this edition is built
     (original untouched; after each chapter "Reflection", "Practice", "Key Thought"; the 30-day practice; the
     Quick Finder), tips (read one chapter at a time, do the practice, keep notes, be patient).
   - `## About Christian D. Larson` (500–700 words): facts you are sure of: born 1874 in Iowa to Norwegian
     immigrant parents; studied (Iowa State / theology – only if sure, otherwise "studied theology"); New
     Thought teacher, lecturer and very prolific author; founded the magazine *Eternal Progress* (Cincinnati,
     early 1900s); influenced later success literature; wrote dozens of books (e.g. *The Ideal Made Real*,
     *Mastery of Self*, *Your Forces and How to Use Them*, *The Pathway of Roses*); the creed; died 1954 in
     California. If you are not sure about a detail, leave it out.
   - `## The World of New Thought` (300–450 words): short context (Quimby, Emerson, the 1900s–1910s boom of
     "mind power" books, the rise of practical psychology), Larson's place in it — without naming living
     authors or modern brands.
   - `## A Note on This Edition` (150–250 words): follows the 1912 text, spelling kept, obvious printing errors
     corrected; the creed taken from the 1912 printing; dated language and claims; editorial material is new.

2. `chapters.md` — for EVERY section of original.md EXCEPT `Foreword`, in the same order, a block:
   ```
   ## <exact section title>
   ### Reflection
   <170–280 words: the chapter's key idea in plain modern words, Larson's main arguments, one or two of his
   examples briefly retold, what still holds up today, how a reader can use it>
   ### Practice
   <a concrete exercise, 50–110 words, numbered steps allowed>
   ### Key Thought
   > <one sentence quoted EXACTLY, word for word, from this section of original.md>
   ```
   For "Promise Yourself": Reflection 120–200 words about the creed and its history, Practice = how to use the
   creed (e.g. read it each morning, pick one line per week), Key Thought = one line of the creed.

3. `thirty_days.md` — `## The 30-Day Practice`, a 150–250 word introduction, then `### Day 1 – <Theme>` …
   `### Day 30 – <Theme>`. Each day: one sentence quoted EXACTLY from original.md (as a `>` quote), then
   `Source: <Section title>` on its own line, then a 2–4 sentence task for the day (your words). Arc: week 1
   awareness and the ruling principle; week 2 subconscious, thought and change; week 3 will, concentration,
   desire, speech; week 4 character, imagination, the higher forces; days 29–30 the creed and commitment.

4. `finder.md` — `## Quick Finder`: 15–25 everyday situations ("When you can't stay focused", "When you doubt
   yourself", "Before an important conversation", …) each pointing to chapter(s) and day(s).
   Format: `- **Situation** — Chapter title, Chapter title · Day N`.

5. `back.md` — `## Afterword: Using All Your Forces` (250–400 words) and `## Further Reading` (only classic
   public-domain titles with year: Larson's own earlier books, James Allen, Wallace D. Wattles, Ralph Waldo
   Trine, Orison Swett Marden, William James's *The Energies of Men* (1907), Emerson).

When done, self-check: every `>` quote in chapters.md and thirty_days.md must appear verbatim in original.md
(write SCRATCH-check: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/check_quotes.py, normalising nothing except
whitespace; fix until 0 misses). Also check that the `##` titles in chapters.md match original.md (minus Foreword).
Final report: word counts per file, quote check result, anything you were unsure about.
