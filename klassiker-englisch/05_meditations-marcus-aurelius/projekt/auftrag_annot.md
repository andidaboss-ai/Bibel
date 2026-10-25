# Task: write the original editorial material for "Meditations (Annotated)"

Book: Marcus Aurelius, *Meditations*, in the English translation by George Long (1862, public domain).
Clean text: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/marcus/book/text/original.md — 12 sections `## The First Book` …
`## The Twelfth Book`; inside, numbered paragraphs ("2. …"). Long's square brackets [ ] are his own insertions and
part of the text. Do NOT change the original text.

We publish an annotated edition on Amazon KDP. KDP accepts public-domain books only when clearly differentiated by
ORIGINAL added material. Everything you write must be your own original writing. Never copy or paraphrase other
editions, commentaries, translations (no Hays, Hammond, Waterfield, Robertson, Holiday …), Wikipedia sentences or
books about Stoicism. Facts are fine; wording must be yours. Quote ONLY Long's translation.

Audience: modern readers (20–60, US/UK) who are curious about Stoicism, resilience, discipline, calm, leadership,
dealing with anger, anxiety and loss. Tone: clear, warm, steady, practical, modern, never preachy, never hype.
Plain American English. Short paragraphs. Long's English is old-fashioned (thee/thou, "ruling faculty",
"the universal nature"): always explain in plain words what a passage means.

Honesty and care rules:
- Present Marcus's ideas as his and the Stoics' views ("Marcus reminds himself…", "the Stoics held…").
- Death, grief, suffering: treat with care; Stoic acceptance is not "don't feel". Where the text touches despair or
  "departing from life", add gently that anyone struggling should talk to someone and seek help (in an emergency
  988 in the US, Samaritans 116 123 in the UK). Do NOT present Stoicism as therapy or as a replacement for medical or
  psychological care, but you may mention that modern cognitive approaches were influenced by Stoic ideas, kept
  general.
- Ancient views (slavery, gods, providence vs atoms, cosmic cycles) explained neutrally and historically.
- References: when you mention a section, use the form "Book IV, 3". Name people only when sure (Rusticus, Epictetus,
  Antoninus Pius, Faustina, Lucius Verus, Commodus, the Marcomannic wars, Carnuntum, the Quadi, the Granua river).

Files (Markdown) in /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/marcus/book/text/:

1. `front.md`
   - `## How to Use This Book` (350–450 words): what the Meditations are (private notes, never meant for publication),
     how this edition is built (Long's complete text; after each Book "Reflection", "Practice", "Key Thought";
     the 30-day practice; the Quick Finder; the glossary of Long's old words), how to read it (a few sections a
     day, slowly, read aloud, keep notes).
   - `## About Marcus Aurelius` (550–750 words): born 121 in Rome; adopted by Antoninus Pius at Hadrian's wish;
     emperor 161–180, first together with Lucius Verus; the Antonine plague; long wars on the Danube against the
     Marcomanni and Quadi; wrote these notes in Greek, partly on campaign; married Faustina; son Commodus succeeded
     him; died 180. Only details you are sure of.
   - `## Stoicism in Brief` (450–600 words): the core ideas in plain words — what is in our power and what is not,
     judgments vs events, virtue (wisdom, justice, courage, self-control), living according to nature and reason,
     the common good / we are made for one another, the view from above, memento mori, the present moment.
     Zeno, Cleanthes, Chrysippus, Seneca, Epictetus as names only.
   - `## A Note on This Translation` (200–300 words): George Long (1801–1879), first published 1862; why his version
     is still loved (faithful, dignified), its old-fashioned style, square brackets = Long's insertions, his
     footnotes and his marks for doubtful passages are left out here, the numbering of sections.
2. `chapters.md` — for EACH of the 12 Books, in order, using the exact `##` titles:
   ```
   ## The First Book
   ### Reflection
   <250–380 words: what this Book is about, its main themes, 2–4 key sections explained in plain words with
   references ("Book II, 1"), what it means for life today>
   ### Practice
   <a concrete Stoic exercise, 60–120 words, numbered steps allowed>
   ### Key Thought
   > <one sentence quoted EXACTLY, word for word, from this Book of original.md>
   ```
3. `thirty_days.md` — `## The 30-Day Practice`, intro 150–250 words, then `### Day 1 – <Theme>` … `### Day 30 –
   <Theme>`. Each day: one sentence quoted EXACTLY from original.md (`>` quote; prefer short, strong sentences), then
   `Source: <Book title>` (e.g. `Source: The Fourth Book`), then a 2–4 sentence task. Arc: week 1 morning
   preparation & what is in our power; week 2 judgments, anger, other people; week 3 duty, work, the present moment;
   week 4 nature, change, death and gratitude; days 29–30 review and an evening review practice.
4. `finder.md` — `## Quick Finder`: 18–25 everyday situations ("When someone insults you", "When you can't get out of
   bed", "When you fear what others think", "After a loss", …) → Book(s) with section numbers and day(s).
   Format: `- **Situation** — Book IV, 3; Book VIII, 47 · Day N`.
5. `back.md` — `## A Glossary of Long’s Words` (25–40 entries, alphabetical, `- **term** — plain meaning`: e.g. ruling
   faculty, universal nature, daemon, the Whole, providence, atoms, thee/thou/thy, art/hast/doth, perturbation …),
   then `## Afterword: The Emperor’s Notebook` (250–400 words), then `## Further Reading` (only public-domain
   classics with translator and year you are sure of: Epictetus, *Enchiridion* / *Discourses* (George Long, 1877 /
   1890); Seneca, *Letters* (Richard M. Gummere, 1917–1925); Cicero, *On Duties* (Walter Miller, 1913); Boethius,
   *The Consolation of Philosophy* (H. R. James, 1897)).

Self-check: every `>` quote in chapters.md and thirty_days.md must appear verbatim in original.md, inside the Book
named (normalise only whitespace). Script: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/marcus/check_<yourpart>.py. Fix until 0 misses.
Final report: word counts, quote check result, anything unsure. Also suggest one short verbatim sentence (≤ 15 words)
for the back cover and one for the epigraph.
