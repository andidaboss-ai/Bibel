#!/usr/bin/env python3
"""Check chapters_b.md (list entries 27-38) and chapters_e.md (98-116)."""
import re, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(BASE, "book", "text")
SUP = "¹²³⁴⁵⁶⁷⁸⁹⁰"
JOBS = [("chapters_b.md", 27, 38), ("chapters_e.md", 98, 116)]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return len(re.findall(r"[A-Za-z0-9’']+(?:[-–][A-Za-z0-9’']+)*", s))


# chapter list
titles = []
for line in open(os.path.join(BASE, "chapter_list.txt"), encoding="utf-8"):
    line = line.strip()
    m = re.match(r"^(\d+)\s+(## .*)$", line)
    if m:
        titles.append(m.group(2)[3:].strip())

# original sections
orig = open(os.path.join(TXT, "original.md"), encoding="utf-8").read()
sections = {}
order = []
cur = None
for line in orig.splitlines():
    if line.startswith("## "):
        cur = line[3:].strip()
        order.append(cur)
        sections[cur] = []
    elif cur is not None:
        sections[cur].append(line)
sections = {k: norm("\n".join(v)) for k, v in sections.items()}
if order != titles:
    print("WARN: chapter_list.txt and original.md headings differ")

problems = 0


def bad(msg):
    global problems
    problems += 1
    print("PROBLEM:", msg)


for fname, a, b in JOBS:
    path = os.path.join(TXT, fname)
    text = open(path, encoding="utf-8").read()
    expected = titles[a - 1:b]
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    got = [parts[i].strip() for i in range(1, len(parts), 2)]
    bodies = [parts[i + 1] for i in range(1, len(parts), 2)]
    if parts[0].strip():
        bad(f"{fname}: text before first heading")
    if got != expected:
        bad(f"{fname}: titles mismatch\n  expected {expected}\n  got      {got}")
    wsum = 0
    for t, body in zip(got, bodies):
        subs = re.split(r"^### (.+)$", body, flags=re.M)
        names = [subs[i].strip() for i in range(1, len(subs), 2)]
        if names != ["Reflection", "Practice", "Key Line"]:
            bad(f"{fname} [{t}]: subsections {names}")
            continue
        if subs[0].strip():
            bad(f"{fname} [{t}]: text before Reflection")
        refl, prac, key = (subs[i + 1].strip() for i in range(1, len(subs), 2))
        wr, wp = words(refl), words(prac)
        wsum += wr + wp
        if not 70 <= wr <= 130:
            bad(f"{fname} [{t}]: Reflection {wr} words")
        if not 20 <= wp <= 50:
            bad(f"{fname} [{t}]: Practice {wp} words")
        for chunk, nm in ((refl, "Reflection"), (prac, "Practice")):
            if re.search(r"^\s*>", chunk, flags=re.M):
                bad(f"{fname} [{t}]: blockquote inside {nm}")
        klines = [l for l in key.splitlines() if l.strip()]
        if not klines or not all(l.startswith(">") for l in klines):
            bad(f"{fname} [{t}]: Key Line not a > quote")
            continue
        q = norm(" ".join(l[1:] for l in klines))
        if any(c in q for c in SUP):
            bad(f"{fname} [{t}]: superscript in quote")
        if "*" in q:
            bad(f"{fname} [{t}]: italics in quote")
        if t not in sections:
            bad(f"{fname} [{t}]: section not in original")
        elif q not in sections[t]:
            bad(f"{fname} [{t}]: quote not verbatim: {q}")
        if len(q.split()) < 4:
            bad(f"{fname} [{t}]: quote too short")
    print(f"{fname}: {len(got)} sections, {wsum} words (Reflection+Practice)")

print(f"{problems} problems")
sys.exit(1 if problems else 0)
