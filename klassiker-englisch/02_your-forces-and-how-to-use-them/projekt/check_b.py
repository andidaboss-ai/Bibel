import re, sys
base = "/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/book/text/"
ws = lambda s: re.sub(r"\s+", " ", s).strip()
orig = open(base + "original.md", encoding="utf-8").read()
# split original into sections by '## ' (not '###')
secs = {}
for m in re.finditer(r"^## (.+)$", orig, re.M):
    pass
parts = re.split(r"^## (?!#)(.+)$", orig, flags=re.M)
for i in range(1, len(parts), 2):
    body = parts[i + 1].replace("*", "")  # maxims count without asterisks
    secs[parts[i].strip()] = ws(body)
order = list(secs)
first, last = order.index("Concentration and the Power Back of Suggestion"), order.index("The Greatest Power in Man")
expected = order[first:last + 1]
doc = open(base + "chapters_b.md", encoding="utf-8").read()
blocks = re.split(r"^## (?!#)(.+)$", doc, flags=re.M)
titles = [blocks[i].strip() for i in range(1, len(blocks), 2)]
miss = 0
if titles != expected:
    print("TITLE MISMATCH", titles); miss += 1
for i in range(1, len(blocks), 2):
    t, body = blocks[i].strip(), blocks[i + 1]
    src = secs.get(t, "")
    sub = dict(re.findall(r"^### (\w[\w ]*)\n(.*?)(?=^### |\Z)", body, re.M | re.S))
    rw = len(sub.get("Reflection", "").split()); pw = len(sub.get("Practice", "").split())
    print(f"{t[:45]:45} refl={rw} prac={pw}", "" if 170 <= rw <= 280 and 50 <= pw <= 110 else "  <-- WORDCOUNT")
    quotes = [ws(q) for q in re.findall(r"^> (.+)$", body, re.M)]
    if len(quotes) != 1: print("  key thought count", len(quotes)); miss += 1
    inline = [ws(q) for q in re.findall(r"“([^”]+)”|\"([^\"]+)\"", sub.get("Reflection", "")) for q in q if q]
    for q in quotes + inline:
        qq = q.rstrip(",.")
        if qq not in src and qq not in ws(orig.replace("*", "")):
            print("  MISS:", q); miss += 1
        elif qq not in src:
            print("  (elsewhere in book, not this section):", q)
print("misses:", miss)
sys.exit(1 if miss else 0)
