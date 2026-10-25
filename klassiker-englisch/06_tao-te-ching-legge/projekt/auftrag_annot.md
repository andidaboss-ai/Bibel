# Task: write the original editorial material for "Tao Te Ching (Annotated)"

Book: the *Tao Te Ching*, traditionally attributed to Lao Tzu, in the English translation by James Legge (1891,
public domain). Clean text: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/tao/book/text/original.md — 81 sections `## Chapter 1` …
`## Chapter 81`; inside, Legge's numbered verses ("2. …"), and rhymed verse passages as lines starting with "| ".
Legge's words in round brackets ( ) are his own insertions and part of the text. Do NOT change the original text.

We publish an annotated edition on Amazon KDP. KDP accepts public-domain books only when clearly differentiated by
ORIGINAL added material. Everything you write must be your own original writing. Never copy or paraphrase other
translations or commentaries (no Mitchell, Le Guin, Feng/English, Lau, Henricks, Wilhelm, Wikipedia …). Facts are
fine; wording must be yours. Quote ONLY Legge's text.

Audience: modern readers (20–65, US/UK) interested in calm, mindfulness, simplicity, leadership, letting go,
Eastern wisdom. Tone: clear, quiet, warm, practical, modern, never preachy, never mystical hype. Plain American
English. Legge's English is old-fashioned and heavy: always say in plain words what a chapter means.

Honesty and care rules:
- Authorship and dating: say plainly that tradition names Lao Tzu, that scholars debate whether he was one
  historical person, and that the text probably took shape over time (roughly 4th–3rd century BC). Don't invent
  dates or legends as fact; the gatekeeper Yin Xi story can be told as legend.
- Political chapters (rulers keeping people "without knowledge", weapons, war): explain historically and fairly;
  note where a modern reader would read them differently.
- No promises of health or longevity; where the text speaks of long life or the body, keep it as image/teaching.
- Use the spelling "Tao" and "Te" in your notes; mention once that Legge wrote "Tâo" and "Teh".

Files (Markdown) in /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/tao/book/text/:

1. `front.md`
   - `## How to Use This Book` (300–420 words): one chapter a day, read twice, once aloud; how this edition is built
     (Legge's complete text; after each chapter a short "Reflection", "Practice" and "Key Line"; the 30-day practice;
     the Quick Finder; the glossary).
   - `## About Lao Tzu and the Text` (450–650 words): tradition, legend, scholarship, the two parts (Tao and Te),
     the title's meaning, its place in Chinese thought, how it came to the West.
   - `## Taoism in Brief` (400–550 words): the Tao that cannot be named, Te (virtue/power), wu wei (non-forcing
     action), the soft overcoming the hard, water, the uncarved block, simplicity and few desires, the sage, yin and
     yang only if relevant, emptiness and usefulness. Plain words.
   - `## A Note on This Translation` (200–300 words): James Legge (1815–1897), Scottish missionary and later first
     professor of Chinese at Oxford; the translation appeared in 1891 in *The Sacred Books of the East* (vol. 39,
     edited by Max Müller); his round brackets; his rhymed renderings of some passages; why it is still worth reading.
2. `chapters.md` — for EACH chapter in your assigned range, in order, using the exact `##` titles:
   ```
   ## Chapter N
   ### Reflection
   <70–140 words: what the chapter says in plain modern words, its key image, what it can mean today>
   ### Practice
   <25–60 words: one small, concrete exercise>
   ### Key Line
   > <a phrase or sentence quoted EXACTLY, word for word, from this chapter of original.md (from prose or from a
   > "| " verse line, without the "| ")>
   ```
3. `thirty_days.md` — `## The 30-Day Practice`, intro 150–250 words, then `### Day 1 – <Theme>` … `### Day 30 –
   <Theme>`. Each day: one passage quoted EXACTLY (a `>` quote, max ~40 words, from one sentence or one verse line),
   then `Source: Chapter N`, then a 2–4 sentence task. Arc: week 1 stillness and emptiness; week 2 softness, water,
   yielding; week 3 simplicity, desire, contentment; week 4 leading, serving, wu wei in work and relationships;
   days 29–30 review and commitment.
4. `finder.md` — `## Quick Finder`: 18–25 situations → chapter(s) and day(s). Format:
   `- **Situation** — Chapter 8, Chapter 78 · Day N`.
5. `back.md` — `## A Glossary` (25–40 entries, alphabetical, `- **term** — plain meaning`: Tao, Te, wu wei, sage,
   the uncarved block, the female/the mother, the valley, heaven and earth, the ten thousand things, Legge's old
   words…), `## Afterword: The Way of Water` (250–400 words), `## Further Reading` (only public-domain classics with
   translator and year you are sure of: *The Analects* of Confucius (James Legge, 1861); *Chuang Tzu* (Herbert A.
   Giles, 1889); *The Sayings of Lao-Tzŭ* (Lionel Giles, 1904) — NO: Lionel Giles died 1958, leave him out; Marcus
   Aurelius, *Meditations* (George Long, 1862), noting that it is available in this same annotated series).

Self-check: every `>` quote must appear verbatim in original.md inside the chapter named (normalise only whitespace;
ignore the "| " line prefixes when matching). Script: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/tao/check_<yourpart>.py. Fix until 0
misses. Final report: word counts, quote check, anything unsure; part C also suggests one short verbatim line for
the back cover and one for the epigraph.
