#!/usr/bin/env python3
"""Check notes for 04_how_to_get, 07_man_who_can, 10_what_is_truth."""
import re, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
WORKS = ["04_how_to_get", "07_man_who_can", "10_what_is_truth"]


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("*", "")
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return len(s.split())


def eng_chapters(path):
    chaps, cur = [], None
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            cur = [line[3:].strip(), []]
            chaps.append(cur)
        elif cur:
            cur[1].append(line)
    return [(t, norm("".join(b))) for t, b in chaps]


def check(work):
    probs = []
    src = eng_chapters(os.path.join(BASE, "eng", work + ".md"))
    path = os.path.join(BASE, "notes", work + ".md")
    if not os.path.exists(path):
        return [f"{work}: notes file missing"]
    text = open(path, encoding="utf-8").read()
    m = re.match(r"# INTRO (\S+)\n(.*?)(?=^## )", text, re.S | re.M)
    if not m or m.group(1) != work:
        probs.append(f"{work}: INTRO header missing/wrong")
    else:
        n = words(m.group(2))
        if not 250 <= n <= 400:
            probs.append(f"{work}: intro {n} words")
    if text.count("# INTRO") != 1:
        probs.append(f"{work}: expected exactly one INTRO")
    secs = re.split(r"^## ", text, flags=re.M)[1:]
    titles = [s.split("\n", 1)[0].strip() for s in secs]
    if titles != [t for t, _ in src]:
        probs.append(f"{work}: titles/order mismatch\n  got {titles}\n  want {[t for t, _ in src]}")
    for sec, (stitle, body) in zip(secs, src):
        title = sec.split("\n", 1)[0].strip()
        parts = re.split(r"^### ", sec, flags=re.M)[1:]
        names = [p.split("\n", 1)[0].strip() for p in parts]
        if names != ["Reflection", "Practice", "Key Thought"]:
            probs.append(f"{work}/{title}: subsections {names}")
            continue
        get = lambda i: parts[i].split("\n", 1)[1].strip()
        r, p, k = get(0), get(1), get(2)
        if not 90 <= words(r) <= 150:
            probs.append(f"{work}/{title}: reflection {words(r)} words")
        if not 25 <= words(p) <= 55:
            probs.append(f"{work}/{title}: practice {words(p)} words")
        qlines = [l for l in k.splitlines() if l.strip()]
        if not qlines or not all(l.startswith(">") for l in qlines):
            probs.append(f"{work}/{title}: key thought not a quote")
            continue
        q = norm(" ".join(l.lstrip(">").strip() for l in qlines))
        if len(q) < 10:
            probs.append(f"{work}/{title}: quote too short")
        elif q not in body:
            probs.append(f"{work}/{title}: quote not verbatim: {q}")
    return probs


def main():
    allp = []
    for w in WORKS:
        allp += check(w)
    for p in allp:
        print(p)
    print(f"{len(allp)} problems")
    sys.exit(1 if allp else 0)


if __name__ == "__main__":
    main()
