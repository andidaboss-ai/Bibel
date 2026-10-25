import re, sys
base = "/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/mulford/book/text/"
orig_lines = open(base + "original.md", encoding="utf-8").read().splitlines()
norm = lambda s: re.sub(r"\s+", " ", s.replace("*", "")).strip()

# sections of original (excluding %% lines)
sections, cur = {}, None
for l in orig_lines:
    if l.startswith("## "):
        cur = l[3:].strip(); sections[cur] = []
    elif cur and not l.startswith("%%"):
        sections[cur].append(l)
sections = {k: norm(" ".join(v)) for k, v in sections.items()}
order = list(sections)

text = open(base + "chapters_a.md", encoding="utf-8").read()
titles = re.findall(r"^## (.+)$", text, re.M)
expected = order[1:8]
print("titles ok" if titles == expected else f"TITLE MISMATCH {titles} vs {expected}")

misses = 0
for block in re.split(r"^## ", text, flags=re.M)[1:]:
    title = block.splitlines()[0].strip()
    parts = re.split(r"^### (.+)$", block, flags=re.M)
    d = {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}
    for name in ("Reflection", "Practice"):
        print(f"{title[:40]:40} {name:10} {len(d.get(name, '').split())} words")
    for q in re.findall(r"^>\s?(.+)$", block, re.M):
        if norm(q) not in sections.get(title, ""):
            misses += 1; print("MISS:", title, "|", q)
print("misses:", misses)
