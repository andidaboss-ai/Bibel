# Task: original editorial notes for "The Collected Works of Wallace D. Wattles (Annotated)"

Wallace Delois Wattles (1860–1911), American New Thought writer and Christian socialist; lived in Indiana (Elwood);
wrote for Elizabeth Towne's magazine *The Nautilus*; most books published by Elizabeth Towne, Holyoke, Mass.
Only state facts you are sure of. Clean texts: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/wattles/eng/*.md
(one `## ` section per chapter). Do NOT change the texts.

We publish on Amazon KDP; public-domain books need clearly ORIGINAL added material. All your writing must be your own;
never copy or paraphrase other editions, commentaries, summaries or Wikipedia. Quote ONLY Wattles' text.

Audience: modern readers (20–65, US/UK) interested in mindset, success, health, faith, personal growth.
Tone: clear, warm, practical, honest, modern American English; never hype.

Honesty and care rules (important):
- WEALTH: Wattles says right thinking makes one rich "with certainty". Present his teaching (clear vision, gratitude,
  purposeful action, giving more in use value than you take in cash value, the creative vs. competitive mind) and add
  where needed that no book can promise wealth; results depend on action, circumstances, and luck.
- HEALTH: The Science of Being Well and The New Science of Living and Healing teach eating only when hungry, skipping
  breakfast, fasting, chewing, and that thought heals disease. Explain the teaching fairly and say clearly that this is
  historical, not medical advice; fasting or changing diet can be dangerous for many people (diabetes, pregnancy,
  eating disorders, medication); illness is never the patient's fault; see a doctor. Never promise healing.
- POVERTY/BLAME: never imply that poor or sick people caused their situation.
- Politics/religion: Wattles was a Christian socialist (A New Christ, the Jesus lecture). Explain respectfully and
  historically; don't take sides; note where views are of their time (e.g. on race, gender or ethnic slurs).
- Mental health: suggest professional help where heavy topics come up.

For EACH chapter in your assigned file(s), in order, with the exact `##` title, write into your output file:
```
## <exact title>
### Reflection
<90–150 words: what the chapter says in plain modern words, its key idea, what it can mean today>
### Practice
<25–55 words: one small, concrete exercise>
### Key Thought
> <a phrase or sentence quoted EXACTLY, word for word, from this chapter of the eng/ file>
```
(For the novel Hell-Fire Harrison: Reflection = what happens and what it shows about Wattles' ideas, Practice = a short
reflective question or exercise, Key Thought = a line from the chapter.)

Also write ONE introduction per work, as the first section of your output file:
```
# INTRO <work file name, e.g. 01_getting_rich>
<250–400 words: when and where it appeared, what it is about, its place in Wattles' work, how to read it today;
include the care notes that apply to that work>
```
Self-check: write a script check_notes_<your part>.py in the wattles folder that verifies titles/order, word ranges and
that every `>` quote appears verbatim (whitespace-normalised) in the named chapter of the eng/ file; fix until 0
problems. Edit only your own output files. Report briefly.
