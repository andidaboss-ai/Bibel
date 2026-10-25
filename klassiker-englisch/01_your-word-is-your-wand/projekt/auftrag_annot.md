# Task: write the original editorial material for "Your Word Is Your Wand (Annotated)"

Book: Florence Scovel Shinn, "Your Word Is Your Wand" (1928, public domain). The clean original text is in
/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/shinn/original.md (chapters as `## Title`). Do NOT change the original text.

We publish an annotated edition on Amazon KDP. KDP only accepts public-domain books that are clearly
differentiated by ORIGINAL added material (introduction, biography, historical context, study guide).
Everything you write must be your own original writing. Never copy or paraphrase other editions,
commentaries, Wikipedia sentences or other books about Shinn. Facts are fine; wording must be yours.

Audience: modern readers (mostly women 25–55, US/UK) interested in affirmations, manifesting, mindset,
spirituality, Christianity-friendly New Thought. Tone: warm, clear, modern, grounded, never preachy,
never hype. Plain American English. Short paragraphs.

Honesty rules (very important):
- No promises of money, healing or guaranteed results. Present Shinn's claims as her teaching and her
  stories ("Shinn tells of…", "In her view…").
- Health chapters (Health, Eyes, Anaemia, Ears, Rheumatism, False Growths, Heart Disease): every editorial
  note there must gently but clearly say that affirmations are a spiritual/emotional practice that can go
  alongside — never instead of — medical care, and to see a doctor.
- Debt/Prosperity: practical grounding (affirmation + wise action), no get-rich claims.
- Explain dated things neutrally: 1928 money amounts (give a rough modern value only as "roughly … today"
  with "about"), "man" meaning all people, King James Bible quotations (give the reference, e.g. Proverbs
  18:21, when Shinn quotes or alludes to the Bible — check carefully, only give references you are sure of).

Write these files into /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/shinn/ (Markdown):

1. `front.md`
   - `## How to Use This Book` (300–450 words): what affirmations are in Shinn's sense, how the book is
     built (original text untouched, then "Reflection" and "Practice" after each chapter, the 30-day
     practice at the end), simple tips (speak aloud, write, repeat, pair with action, be patient).
   - `## About Florence Scovel Shinn` (500–700 words): life facts you are sure of: born 1871 in Camden,
     New Jersey; trained as an artist (Pennsylvania Academy of the Fine Arts); illustrator for magazines and
     books in New York; married the painter Everett Shinn (1898, divorced 1912); later a New Thought teacher
     and lecturer in New York; self-published The Game of Life and How to Play It (1925); Your Word Is Your
     Wand (1928); The Secret Door to Success (1940); died October 17, 1940 in New York; The Power of the
     Spoken Word published after her death (1945). If you are not sure about a detail, leave it out.
   - `## The World of New Thought` (300–450 words): short historical context (Phineas Quimby, Emerson's
     influence, Unity, Divine Science, Religious Science, the 1920s), and her influence on later
     self-help — without naming living authors or modern brands.
   - `## A Note on This Edition` (150–250 words): text follows the 1928 edition, spelling kept, only obvious
     printing errors corrected; dated language; health/money note; editorial material is new.

2. `chapters.md` — for EVERY chapter of original.md, in order, a block:
   ```
   ## <exact chapter title>
   ### Reflection
   <120–220 words: what the chapter says in plain modern words, the key idea, one or two of her stories
   briefly retold, Bible references, how a reader today might use it>
   ### Practice
   <a concrete exercise, 40–100 words, numbered steps allowed>
   ### Key Affirmation
   > <one affirmation quoted EXACTLY, word for word, from this chapter of original.md>
   ```
   For very short chapters (Eyes, Ears, Animals, etc.) Reflection can be 70–120 words.

3. `thirty_days.md` — `## The 30-Day Practice` with a 150–250 word introduction, then
   `### Day 1 – <Theme>` … `### Day 30 – <Theme>`. Each day: one affirmation quoted EXACTLY from
   original.md (as a `>` quote), followed by `Source: <Chapter>` on its own line, then a 2–4 sentence
   prompt or task for the day (your words). Build an arc: week 1 foundations (word, faith, fear), week 2
   relationships & forgiveness, week 3 work, money, guidance, week 4 health of mind, gratitude, divine
   design; days 29–30 review and commitment.

4. `finder.md` — `## Affirmation Finder`: a list of 15–25 everyday situations ("When you feel anxious about
   money", "Before a job interview", "When you can't forgive someone", …) each pointing to the chapter(s)
   and day(s) where the reader finds help. Format: `- **Situation** — Chapter, Chapter · Day N`.

5. `back.md` — `## Afterword: Speaking a New Story` (250–400 words) and `## Further Reading` (only
   Shinn's own other public-domain books and classic public-domain New Thought titles, e.g. by Wallace D.
   Wattles, Thomas Troward, Emma Curtis Hopkins, Ralph Waldo Trine, with year).

When done, run this self-check: every `>` quote in chapters.md and thirty_days.md must appear verbatim in
original.md (write a small Python check, name it /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/shinn/check_quotes.py, and fix until 0 misses).
Final report: word counts per file, the quote check result, anything you were unsure about.
