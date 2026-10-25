#!/usr/bin/env python3
"""Check part C: front.md, thirty_days.md, finder.md, back.md."""
import os, re, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "book", "text")
misses = []

def miss(msg):
    misses.append(msg)
    print("MISS:", msg)

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def norm_plain(s):
    s = s.replace("*", "")
    s = s.replace("“", '"').replace("”", '"').replace("’", "'")
    return norm(s).lower()

def read(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read()

def split_sections(text, level="## "):
    secs, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith(level) and not line.startswith(level + "#"):
            if cur is not None:
                secs[cur] = "\n".join(buf)
            cur, buf = line[len(level):].strip(), []
        else:
            buf.append(line)
    if cur is not None:
        secs[cur] = "\n".join(buf)
    return secs

def words(s):
    s = re.sub(r"[*>#_]", " ", s)
    return len(re.findall(r"[A-Za-z0-9À-ɏ'’&.-]+", s))

orig = read("original.md")
osecs = {k: norm(v) for k, v in split_sections(orig).items()}
orig_all = norm(orig)
orig_plain = norm_plain(orig)
SECTION_NAMES = set(osecs)

def check_range(label, n, lo, hi):
    status = "ok" if lo <= n <= hi else "OUT OF RANGE"
    print(f"  {label}: {n} words ({lo}-{hi}) {status}")
    if status != "ok":
        miss(f"{label} has {n} words, wanted {lo}-{hi}")

ALLOW_INLINE = {"publishers of evangelical literature"}

def check_inline_quotes(name, text):
    """Double-quoted phrases of 3+ words in our own prose must be verbatim in original."""
    body = "\n".join(l for l in text.splitlines() if not l.startswith(">"))
    for q in re.findall(r'"([^"\n]+)"', body):
        qq = norm_plain(q).strip(" .,;:!?")
        if len(qq.split()) < 3 or qq in ALLOW_INLINE:
            continue
        if qq not in orig_plain:
            miss(f"{name}: inline quote not in original: \"{q}\"")

def blockquotes(text):
    """Yield (quote, following_text) for each > block."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith(">"):
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip())
                i += 1
            yield " ".join(q), "\n".join(lines[i:i + 4])
        else:
            i += 1

# ---------- front.md ----------
print("front.md")
front = read("front.md")
fsecs = split_sections(front)
for title, lo, hi in [("How to Use This Book", 300, 420), ("Who Was Brother Lawrence?", 450, 650),
                      ("The Practice in Brief", 400, 550), ("A Note on This Text", 200, 300)]:
    if title not in fsecs:
        miss(f"front.md missing section {title}")
    else:
        check_range(title, words(fsecs[title]), lo, hi)
check_inline_quotes("front.md", front)
for q, _ in blockquotes(front):
    if norm(q) not in orig_all:
        miss(f"front.md quote not in original: {q}")

# ---------- thirty_days.md ----------
print("thirty_days.md")
td = read("thirty_days.md")
if "## The 30-Day Practice" not in td:
    miss("thirty_days.md missing heading")
intro = td.split("## The 30-Day Practice", 1)[-1].split("### Day 1", 1)[0]
check_range("30-day intro", words(intro), 150, 250)
days = re.split(r"^### ", td, flags=re.M)[1:]
nums = []
for d in days:
    head, _, body = d.partition("\n")
    m = re.match(r"Day (\d+) – (.+)$", head.strip())
    if not m:
        miss(f"bad day heading: {head}")
        continue
    n = int(m.group(1)); nums.append(n)
    qs = list(blockquotes(body))
    if len(qs) != 1:
        miss(f"Day {n}: expected 1 quote, got {len(qs)}")
        continue
    q = norm(qs[0][0])
    src = re.search(r"^Source: (.+)$", body, flags=re.M)
    if not src:
        miss(f"Day {n}: no Source line"); continue
    sec = src.group(1).strip()
    if sec not in SECTION_NAMES:
        miss(f"Day {n}: unknown section {sec}"); continue
    if q not in osecs[sec]:
        where = [k for k, v in osecs.items() if q in v]
        miss(f"Day {n}: quote not in {sec} (found in: {where}): {q}")
    if len(q.split()) > 42:
        miss(f"Day {n}: quote too long ({len(q.split())} words)")
    task = body.split(src.group(0), 1)[1].strip()
    ns = len(re.findall(r"[.!?](\s|$)", task))
    if not 2 <= ns <= 4:
        miss(f"Day {n}: task has {ns} sentences")
    print(f"  Day {n:2d} ok-check  {sec:22s} {len(q.split()):2d} words, task {ns} sentences")
if nums != list(range(1, 31)):
    miss(f"days not 1..30: {nums}")
check_inline_quotes("thirty_days.md", td)

# ---------- finder.md ----------
print("finder.md")
fd = read("finder.md")
items = [l for l in fd.splitlines() if l.startswith("- **")]
if not 18 <= len(items) <= 25:
    miss(f"finder has {len(items)} items")
print(f"  {len(items)} situations")
for l in items:
    m = re.match(r"- \*\*(.+?)\*\* — (.+?) · (.+)$", l)
    if not m:
        miss(f"finder bad format: {l}"); continue
    for s in [x.strip() for x in m.group(2).split(",")]:
        if s not in SECTION_NAMES:
            miss(f"finder unknown section '{s}' in: {l}")
    for dn in re.findall(r"Day (\d+)", m.group(3)):
        if not 1 <= int(dn) <= 30:
            miss(f"finder bad day {dn}")
check_inline_quotes("finder.md", fd)

# ---------- back.md ----------
print("back.md")
bk = read("back.md")
bsecs = split_sections(bk)
for t in ["A Glossary", "Afterword: The Kitchen Was His Chapel", "Further Reading"]:
    if t not in bsecs:
        miss(f"back.md missing {t}")
gl = [re.match(r"- \*\*(.+?)\*\* — ", l) for l in bsecs.get("A Glossary", "").splitlines() if l.startswith("- ")]
terms = [m.group(1) for m in gl if m]
if len(terms) != len(gl):
    miss("glossary format error")
if not 20 <= len(terms) <= 35:
    miss(f"glossary has {len(terms)} entries")
key = lambda t: re.sub(r"[^a-z ]", "", re.sub(r"^the ", "", t.lower())).strip()
if [key(t) for t in terms] != sorted(key(t) for t in terms):
    miss(f"glossary not alphabetical: {terms}")
print(f"  glossary {len(terms)} entries")
check_range("Afterword", words(bsecs.get("Afterword: The Kitchen Was His Chapel", "")), 250, 400)
check_inline_quotes("back.md", bk)
for q, _ in blockquotes(bk):
    if norm(q) not in orig_all:
        miss(f"back.md quote not in original: {q}")

print(f"\n{len(misses)} misses")
sys.exit(1 if misses else 0)
