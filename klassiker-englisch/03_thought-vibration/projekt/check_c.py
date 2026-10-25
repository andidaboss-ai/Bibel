import re, sys
base = "/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/book/text/"
def norm(s):
    return re.sub(r"\s+", " ", s.replace("*", "")).strip()
orig_raw = open(base + "original.md", encoding="utf-8").read()
orig = norm(orig_raw)
titles = re.findall(r"^## (.+)$", orig_raw, re.M)
# section text map
secs = {}
for chunk in re.split(r"^## ", orig_raw, flags=re.M)[1:]:
    head, _, body = chunk.partition("\n")
    secs[head.strip()] = norm(body)
txt = open(base + "thirty_days.md", encoding="utf-8").read()
miss = 0
days = re.findall(r"^### (Day \d+) – .*?\n\n> (.+?)\n\nSource: (.+?)\n\n(.+?)(?=\n\n### |\Z)", txt, re.M | re.S)
print("days found:", len(days))
for d, q, src, task in days:
    q = norm(q)
    if src not in secs:
        print("BAD SOURCE", d, src); miss += 1
    elif q not in secs[src]:
        print("MISS", d, q[:60]); miss += 1
    n = len(re.findall(r"[.!?](\s|$)", task.strip()))
    if not 2 <= n <= 4:
        print("sentences", d, n)
print("misses:", miss)
# finder titles
fd = open(base + "finder.md", encoding="utf-8").read() if __import__("os").path.exists(base + "finder.md") else ""
for line in fd.splitlines():
    if line.startswith("- **"):
        part = line.split(" — ", 1)[1].split(" · ")[0]
        for t in [x.replace("LNC", "Law, Not Chance") for x in part.replace("Law, Not Chance", "LNC").split(", ")]:
            if t not in titles and t != "Law, Not Chance" and t.strip() not in titles:
                print("FINDER BAD TITLE:", t)
