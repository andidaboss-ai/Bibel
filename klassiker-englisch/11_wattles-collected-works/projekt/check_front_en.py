#!/usr/bin/env python3
"""Check front/back matter of the English Wattles edition:
enbook/text/front.md, thirty_days.md, finder.md, back.md."""
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
TEXT = os.path.join(BASE, "enbook", "text")
ENG = os.path.join(BASE, "eng")

WORKS = {
    "The Science of Getting Rich": "01_getting_rich",
    "The Science of Being Well": "02_being_well",
    "The Science of Being Great": "03_being_great",
    "How to Get What You Want": "04_how_to_get",
    "A New Christ": "05_new_christ",
    "Jesus: The Man and His Work": "06_jesus",
    "Making the Man Who Can": "07_man_who_can",
    "The New Science of Living and Healing": "08_living_healing",
    "Hell-Fire Harrison": "09_hellfire_harrison",
    "What Is Truth?": "10_what_is_truth",
}

probs = []


def P(msg):
    probs.append(msg)


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("*", "").replace("—", "--").replace("–", "-")
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    s = re.sub(r"[*_#>]", " ", s)
    return len([w for w in s.split() if re.search(r"\w", w)])


def sentences(s):
    s = re.sub(r"\s+", " ", s.strip())
    return [x for x in re.split(r"(?<=[.!?])[\"”’]?\s+(?=[A-Z“\"])", s) if x.strip()]


CHAPS = {}
for title, fn in WORKS.items():
    path = os.path.join(ENG, fn + ".md")
    if not os.path.exists(path):
        CHAPS[title] = None
        continue
    d, cur = {}, None
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            cur = line[3:].strip()
            d[cur] = []
        elif cur is not None:
            d[cur].append(line)
    CHAPS[title] = {k: norm("".join(v)) for k, v in d.items()}
ALL = norm(" ".join(" ".join(c.values()) for c in CHAPS.values() if c))


def chapter_ok(work, chap, where):
    if work not in CHAPS:
        P(f"{where}: unknown work '{work}'")
        return None
    if CHAPS[work] is None:
        P(f"{where}: source file for '{work}' missing")
        return None
    if chap not in CHAPS[work]:
        P(f"{where}: '{work}' has no chapter '{chap}'")
        return None
    return CHAPS[work][chap]


def read(name):
    path = os.path.join(TEXT, name)
    if not os.path.exists(path):
        P(f"{name}: missing")
        return ""
    return open(path, encoding="utf-8").read()


def h2(text):
    out = []
    for part in re.split(r"^## ", text, flags=re.M)[1:]:
        t, _, b = part.partition("\n")
        out.append((t.strip(), b))
    return out


def check_inline_quotes(name, text):
    """Double-quoted phrases of 3+ words outside > blocks must be Wattles' words."""
    body = "\n".join(l for l in text.splitlines() if not l.startswith(">"))
    for q in re.findall(r'"([^"\n]+)"', body):
        q2 = norm(q).rstrip(".,")
        if len(q2.split()) >= 3 and q2 not in ALL and q2.lower() not in ALL.lower():
            P(f"{name}: quoted phrase not found in Wattles: \"{q}\"")


# ---------- front.md
FRONT = [("How to Use This Book", 300, 420), ("Who Was Wallace D. Wattles?", 450, 650),
         ("New Thought in Brief", 400, 550), ("A Note on the Texts", 200, 320)]
text = read("front.md")
secs = h2(text)
if [t for t, _ in secs] != [t for t, _, _ in FRONT]:
    P(f"front.md: sections {[t for t, _ in secs]}")
for (t, b), (_, lo, hi) in zip(secs, FRONT):
    n = words(b)
    if not lo <= n <= hi:
        P(f"front.md/{t}: {n} words (want {lo}-{hi})")
check_inline_quotes("front.md", text)

# ---------- thirty_days.md
text = read("thirty_days.md")
secs = h2(text)
if len(secs) != 1 or secs[0][0] != "The 30-Day Practice":
    P(f"thirty_days.md: expected one section 'The 30-Day Practice', got {[t for t, _ in secs]}")
if secs:
    body = secs[0][1]
    parts = re.split(r"^### ", body, flags=re.M)
    n = words(parts[0])
    if not 150 <= n <= 250:
        P(f"thirty_days.md: intro {n} words (want 150-250)")
    days = parts[1:]
    if len(days) != 30:
        P(f"thirty_days.md: {len(days)} days")
    for i, d in enumerate(days, 1):
        head, _, rest = d.partition("\n")
        m = re.fullmatch(r"Day (\d+) – (.+)", head.strip())
        if not m or int(m.group(1)) != i:
            P(f"Day {i}: bad heading '{head.strip()}'")
        where = f"Day {i}"
        lines = [l for l in rest.strip().splitlines()]
        qlines = [l for l in lines if l.startswith(">")]
        src = [l for l in lines if l.startswith("Source:")]
        task = "\n".join(l for l in lines if l.strip() and not l.startswith(">") and not l.startswith("Source:"))
        if not qlines:
            P(f"{where}: no quote")
            continue
        if len(src) != 1:
            P(f"{where}: expected one Source line")
            continue
        q = norm(" ".join(l.lstrip(">").strip() for l in qlines))
        if words(q) > 42:
            P(f"{where}: quote {words(q)} words")
        if len(sentences(q)) != 1:
            P(f"{where}: quote is not one sentence")
        sm = re.fullmatch(r"Source: (.+), ([^,]+(?:, [^,]+)?)", src[0].strip())
        work = chap = None
        for w in WORKS:
            if src[0].strip().startswith(f"Source: {w}, "):
                work, chap = w, src[0].strip()[len(f"Source: {w}, "):]
        if not work:
            P(f"{where}: Source line names no known work: {src[0]}")
            continue
        cbody = chapter_ok(work, chap, where)
        if cbody is not None and q not in cbody:
            P(f"{where}: quote not verbatim in {work} / {chap}: {q}")
        ns = len(sentences(task))
        if not 2 <= ns <= 4:
            P(f"{where}: task has {ns} sentences")
        if re.search(r"\bfast(s|ing)?\b|skip(ping)? (a |your )?(meal|breakfast|lunch|dinner)|eat less|go without food", task, re.I):
            P(f"{where}: task mentions fasting or skipping meals")
check_inline_quotes("thirty_days.md", text)

# ---------- finder.md
text = read("finder.md")
secs = h2(text)
if len(secs) != 1 or secs[0][0] != "Quick Finder":
    P("finder.md: expected one section 'Quick Finder'")
if secs:
    body = secs[0][1]
    intro = "\n".join(l for l in body.splitlines() if l.strip() and not l.startswith("- "))
    if len(sentences(intro)) != 1:
        P(f"finder.md: intro is {len(sentences(intro))} sentences")
    items = [l for l in body.splitlines() if l.startswith("- ")]
    if not 20 <= len(items) <= 25:
        P(f"finder.md: {len(items)} items")
    for it in items:
        m = re.fullmatch(r"- \*\*(When [^*]+)\*\* — (.+) · Days? ([\d, ]+)", it)
        if not m:
            P(f"finder: bad format: {it}")
            continue
        for ds in m.group(3).split(","):
            if not 1 <= int(ds) <= 30:
                P(f"finder: bad day {ds} in {it}")
        for ref in m.group(2).split("; "):
            hit = [w for w in WORKS if ref.startswith(w + ": ")]
            if not hit:
                P(f"finder: unknown work in '{ref}'")
                continue
            w = max(hit, key=len)
            chapter_ok(w, ref[len(w) + 2:], f"finder '{m.group(1)}'")

# ---------- back.md
text = read("back.md")
secs = dict(h2(text))
want = ["A Glossary", "Afterword: The Certain Way Today", "Further Reading"]
if [t for t, _ in h2(text)] != want:
    P(f"back.md: sections {[t for t, _ in h2(text)]}")
g = [l for l in secs.get("A Glossary", "").splitlines() if l.startswith("- **")]
if not 25 <= len(g) <= 40:
    P(f"back.md: glossary {len(g)} entries")
terms = [re.match(r"- \*\*(.+?)\*\*", l).group(1) for l in g]
if terms != sorted(terms, key=lambda t: re.sub(r"^The ", "", t).lower()):
    P("back.md: glossary not alphabetical")
for need in ["Certain Way", "Formless Substance", "Thinking Stuff", "Creative plane", "Competitive plane",
             "Use value", "Cash value", "Advancing Man", "Principle of Health", "Principle of Power",
             "New Thought", "The Nautilus", "Elizabeth Towne", "Christian socialism",
             "Cosmic consciousness", "Fletcherism"]:
    if need not in terms:
        P(f"back.md: glossary lacks '{need}'")
n = words(secs.get("Afterword: The Certain Way Today", ""))
if not 250 <= n <= 400:
    P(f"back.md: afterword {n} words")
fr = secs.get("Further Reading", "")
for need in ["As a Man Thinketh", "Out from the Heart", "Your Word Is Your Wand", "Your Forces and How to Use Them",
             "Thought Vibration", "Thoughts Are Things", "Meditations"]:
    if need not in fr:
        P(f"back.md: further reading lacks {need}")
check_inline_quotes("back.md", text)

for p in probs:
    print(p)
print(f"{len(probs)} problems")
sys.exit(1 if probs else 0)
