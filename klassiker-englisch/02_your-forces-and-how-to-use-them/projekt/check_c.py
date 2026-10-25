"""Verbatim quote check for thirty_days.md: every '>' quote must appear in original.md
(only whitespace normalised; leading/trailing '*' of italic maxims stripped from the source) and
inside the section named on the following 'Source:' line."""
import re, sys, os
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "book", "text")
ws = lambda s: re.sub(r"\s+", " ", s).strip()
orig = open(os.path.join(T, "original.md"), encoding="utf-8").read()
secs, cur = {}, None
for line in orig.splitlines():
    if line.startswith("## "):
        cur = line[3:].strip(); secs[cur] = []
    elif cur:
        l = line.strip()
        if l.startswith("*") and l.endswith("*"):
            l = l.strip("*")
        secs[cur].append(l)
secs = {k: ws(" ".join(v)) for k, v in secs.items()}
full = ws(" ".join(secs.values()))
f = sys.argv[1] if len(sys.argv) > 1 else os.path.join(T, "thirty_days.md")
lines = open(f, encoding="utf-8").read().splitlines()
n = miss = 0
days = 0
for i, line in enumerate(lines):
    if line.startswith("### Day"):
        days += 1
    if line.startswith(">"):
        n += 1
        q = ws(line[1:])
        src = next((l[7:].strip() for l in lines[i+1:i+4] if l.startswith("Source:")), None)
        if q not in full:
            miss += 1; print("MISS (not in original):", q)
        elif src not in secs:
            miss += 1; print("BAD SOURCE TITLE:", src, "|", q[:60])
        elif q not in secs[src]:
            miss += 1; print("WRONG SECTION:", src, "|", q[:60])
print(f"{days} days, {n} quotes, {miss} misses")
sys.exit(1 if miss else 0)
