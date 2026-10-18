# The Bible in Plain Language – English style guide

This is the English edition of *Die Bibel in Leichter Sprache*. It has exactly the same structure,
the same sections and the same explanation boxes as the German edition.

## Sources (legally binding)

- **Bible text:** translated **only** from the public-domain **World English Bible (WEB)**:
  `texte/englisch-web/<testament>/<Book>/kapitel_NNN.txt` (one verse per line, with its number).
- **Headings, introductions and boxes:** translated from our own German edition:
  `texte/leichte-sprache/<testament>/<Book>/kapitel_NNN.md`.
- **Never** take wording from any other English Bible (KJV – still under Crown copyright in the UK –,
  NIV, ESV, NLT, NKJV, NRSV, CEV, GNT/Good News, ERV/Easy-to-Read, NIrV, ICB, EasyEnglish, The Message, …),
  not in the Bible text and not in the boxes. If a phrase happens to sound like another Bible because the
  WEB says the same thing, that is fine.
- Quotations in boxes and introductions must be **word for word from our own English text** of that passage
  (checked by `python3 werkzeuge/pruefung/zitate_en.py`).

## File format

Output: `texte/plain-english/<testament>/<Book>/kapitel_NNN.md` (same folder names as the German edition).

```
# Genesis – Chapter 1          (Psalms: "# Psalm 23")
### God creates the world      (chapter title, translated from the German ### line)

---

## Before we begin: What is the book of Genesis?     (only where the German has "Bevor es losgeht")

text …

---

## In the beginning (Verses 1–2)        (one verse: "(Verse 3)")

[1] In the beginning, God created the heavens and the earth.

[2] …

> **What does this mean?**
> …

---
```

Fixed markers (translate the German ones exactly like this):

| German | English |
|---|---|
| `# 1. Mose – Kapitel 1` | `# Genesis – Chapter 1` (book names: column `name_englisch` in `daten/buecher.json`) |
| `# Psalm 23` | `# Psalm 23` |
| `## Bevor es losgeht: …` | `## Before we begin: …` |
| `## Rückblick: …` | `## Looking back: …` |
| `(Vers 3–5)` / `(Vers 3)` | `(Verses 3–5)` / `(Verse 3)` |
| `> **Was bedeutet das?**` | `> **What does this mean?**` |
| `> **Wichtiger Hinweis**` | `> **Important note**` |
| `> **Wichtiger Hinweis vorab**` | `> **Important note first**` |
| `> **Wie geht es weiter?**` | `> **What comes next?**` |
| `> **Für heute:**` | `> **For today:**` |
| other bold lead-ins `> **Xyz:**` | translate them |

- Every verse starts with its number in square brackets: `[1]`, `[2]`, … **No verse may be missing**, and the
  order must be kept. Verse numbers follow the WEB (same as the German edition).
- Keep the German section division (same headings, same verse ranges, same boxes in the same places).
- Short lines: one thought per line, like the German edition (sense lines).

## Language (plain language)

- Short sentences. One idea per sentence.
- Common, everyday words. Explain a necessary hard word the first time (“Holy means: …”).
- Active voice. Simple past or present.
- Friendly, calm, never preachy.
- **Nothing is left out:** every statement, name, number, date and list from the WEB stays in.
- Nothing is added to the Bible text. Short explanations inside the text are allowed (“That means: …”).
  Interpretations belong only in the boxes.

## Fixed terms

| WEB | Plain Language |
|---|---|
| Yahweh | the LORD (capital letters, as a name for God) |
| Yahweh God | the LORD God |
| Lord Yahweh | the Lord GOD |
| Lord (Adonai) | Lord |
| Yahweh of Armies | the LORD of Armies |
| behold | leave out, or “Look!” |
| Names of people and places | **exactly as the WEB spells them** in that chapter (Josiah, Hezekiah, Elijah, Bethlehem …). In boxes, use the WEB spelling too. |

- Numbers: digits with a comma for thousands (10,000). Ranges with an en dash: 3–5. Bible references
  like this: Genesis 1:3; 1 Samuel 15:1–3; (verse 3); (verses 3–5); (Chapter 7).
- **Units:** convert to US customary units (feet, yards, miles, pounds, ounces, gallons, quarts) with “about”.
  Name the old unit in the box (“A cubit is about 18 inches.”). Money stays as in the WEB (shekels, talents),
  explained in the box.
- Quotation marks: “…” outside, ‘…’ inside, a third level “…” again. Apostrophe: ’. Ellipsis: …
- American spelling (color, honor, Savior).

## Boxes and introductions

- Translate the German box faithfully and in plain language. Keep the content and the balance
  (Jewish and Christian views, scholarly notes, warnings against misuse of texts).
- References to “German Bibles” (e.g. “in deutschen Bibeln 5,1”) become “in some Bibles 5:1”.
- German cultural details may stay if they are meaningful (“In Germany, …”), otherwise make them general.
- **Help lines** (German phone numbers) are replaced by:
  “In the US, call or text 988. In the UK and Ireland, call Samaritans at 116 123. Elsewhere, find help at findahelpline.com.”
  For abuse: add “In the US: Childhelp 1-800-422-4453, RAINN 1-800-656-4673.” For domestic violence:
  “US: 1-800-799-7233.” For addiction: “US: SAMHSA 1-800-662-4357.”
- Quotations: only word for word from our own English text (see above).

## Clarifications (from the pilot)

- Short explanations of hard words go **outside** spoken quotations, as their own line (“An expanse is a wide, open space.”), so they never sound like God or a person speaking.
- If the WEB uses an old name for a place that the German box calls by its modern name, keep the WEB name in the Bible text and explain it in the box (“Hiddekel is the old name of the Tigris.”).
- Units that the WEB already gives in English measures (mile, pound) stay as they are.
- A speech that goes on over several paragraphs: open a new “ at each new paragraph without closing the old one (like the WEB). A speech may stay open at the end of a chapter if it goes on in the next chapter.
- Emergency: “In an emergency, call your local emergency number (911 in the US, 999 in the UK).”
- Work chapter by chapter and **save every chapter file as soon as it is finished**. Skip chapters whose English file already exists and passes the checker.
