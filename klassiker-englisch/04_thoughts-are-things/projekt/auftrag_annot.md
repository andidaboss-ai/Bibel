# Task: write the original editorial material for "Thoughts Are Things (Annotated)"

Book: Prentice Mulford, "Thoughts Are Things — Essays Selected from the White Cross Library" (London: G. Bell and
Sons, printing of 1920; public domain; Mulford 1834–1891). Clean original text:
/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/mulford/book/text/original.md (`## Preface` by the anonymous selector "J. W.", then 13
essays as `## Title`). Do NOT change the original text.

We publish an annotated edition on Amazon KDP. KDP accepts public-domain books only when clearly differentiated
by ORIGINAL added material. Everything you write must be your own original writing. Never copy or paraphrase other
editions, commentaries, Wikipedia sentences or books about Mulford. Facts are fine; wording must be yours.

Audience: modern readers (25–60, US/UK) interested in the Law of Attraction, manifesting, mindset, New Thought,
self-discipline; many know "The Secret" era books (do not name living authors, films or brands). Tone: clear,
warm, energetic, grounded, modern, never preachy, never hype. Plain American English. Short paragraphs.

Honesty rules (very important):
- No promises of wealth, health, love or guaranteed results. Present Mulford's claims as his teaching
  ("Mulford argues…", "In his view…").
- 1880s "science": thought as a literal substance or current, "thought-elements" in the air, spirits, physical
  immortality ("Immortality in the Flesh"), cures through mind alone, diet/sleep claims. Say kindly and clearly that
  these are beliefs or speculations of his time, not established science — and then give what still holds up
  (attention and self-talk, rest, nature, kindness, aspiration, cheerful persistence). "Immortality in the Flesh":
  present it as his hope and vision, never as a claim that anyone can stop ageing or avoid death.
- Animal cruelty essay ("Museum and Menagerie Horrors"): treat with respect; connect to today's animal-welfare views.
- Wherever he touches health, fear, worry or the body, add that the practices go alongside — never instead of —
  medical or psychological care. For persistent fear/worry mention talking to a doctor or therapist.
- No victim-blaming: the idea that people "attract" misfortune must be framed with care (illness, poverty, abuse
  are not anyone's fault).
- Explain dated language neutrally ("man" meaning all people, 19th-century terms). Bible references only when sure.

Write these files into /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/mulford/book/text/ (Markdown):

1. `front.md`
   - `## How to Use This Book` (350–450 words): what Mulford means by "thoughts are things", how this edition is
     built (original untouched; after each essay "Reflection", "Practice", "Key Thought"; the 30-day practice; the
     Quick Finder), tips (one essay at a time, slow reading, notes, nature walks, patience).
   - `## About Prentice Mulford` (500–700 words): facts you are sure of: born 1834 in Sag Harbor, Long Island, New
     York; went to California in the Gold Rush years (sailed there in the mid-1850s), worked as a miner, cook,
     teacher and comic writer for San Francisco papers; lectured in England; later journalist in New York (the New
     York Daily Graphic); lived for years in a self-built cabin in the woods of New Jersey (described in *The Swamp
     Angel*, 1888); from 1886 wrote the essays later known as the White Cross Library; died in May 1891 in his small
     boat on Long Island waters (found at Sheepshead Bay). If you are not sure of a detail, leave it out.
   - `## The World of New Thought` (300–450 words): short context (Quimby, Emerson, Chicago as a New Thought
     publishing centre around 1900, the phrase "law of attraction" in New Thought writing), his place in it.
   - `## A Note on This Edition` (150–250 words): follows the London selection published by G. Bell and Sons
     (printing of 1920), which kept Mulford's text but changed a few American expressions; British spelling kept;
     obvious printing errors corrected; the short Preface by the anonymous selector "J. W." is part of that edition;
     dated science and language; editorial material is new.

2. `chapters.md` — for EVERY essay of original.md (NOT the Preface), in the same order:
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

3. `thirty_days.md` — `## The 30-Day Practice`, a 150–250 word introduction, then `### Day 1 – <Theme>` …
   `### Day 30 – <Theme>`. Each day: one sentence quoted EXACTLY from original.md (as a `>` quote), then
   `Source: <Essay title>` on its own line, then a 2–4 sentence task (your words). Arc: walk through the 13 essays
   roughly in order (2–3 days per essay), days 29–30 review and commitment.

4. `finder.md` — `## Quick Finder`: 15–25 everyday situations, each pointing to essay(s) and day(s).
   Format: `- **Situation** — Essay title, Essay title · Day N`.

5. `back.md` — `## Afterword: Thinking in the Open Air` (250–400 words) and `## Further Reading` (only classic
   public-domain titles with year you are sure of: William Walker Atkinson, *Thought Vibration* (1906); Ralph Waldo
   Trine, *In Tune with the Infinite* (1897); James Allen, *As a Man Thinketh* (1903); Wallace D. Wattles,
   *The Science of Getting Rich* (1910); Christian D. Larson, *Your Forces and How to Use Them* (1912); Florence
   Scovel Shinn, *Your Word Is Your Wand* (1928); William James, *The Energies of Men* (1907); Emerson,
   *Essays: First Series* (1841)). Mention that the Atkinson, Larson and Shinn titles are available in this same annotated
   series.

Self-check when done: every `>` quote in chapters.md and thirty_days.md must appear verbatim in original.md
(script: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/mulford/check_<yourpart>.py, normalise only whitespace and `*`;
fix until 0 misses), and the `##` titles of chapters.md must match original.md.
Final report: word counts, quote check result, anything you were unsure about.
