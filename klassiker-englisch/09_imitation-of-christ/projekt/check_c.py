import re, sys, os
D = os.path.dirname(os.path.abspath(__file__))
orig = open(os.path.join(D, "book/text/original.md"), encoding="utf-8").read()
mine = open(os.path.join(D, "book/text/chapters_c.md"), encoding="utf-8").read()
titles = [l.strip()[4:].strip() if False else re.sub(r"^\s*\d+\s+", "", l).rstrip("\n")
          for l in open(os.path.join(D, "chapter_list.txt"), encoding="utf-8")]
expected = [t for t in titles if t.startswith("## ")][38:68]
assert len(expected) == 30, len(expected)

def sections(text):
    parts = re.split(r"(?m)^(## .*)$", text)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]

osec = {}
for t, b in sections(orig):
    osec.setdefault(t, b)
norm = lambda s: re.sub(r"\s+", " ", s).strip()
wc = lambda s: len(re.findall(r"[A-Za-z0-9’']+", s))
probs = []
ms = sections(mine)
if [t for t, _ in ms] != expected:
    probs.append("title list/order mismatch")
    for a, b in zip([t for t, _ in ms], expected):
        if a != b: probs.append(f"  got {a!r} expected {b!r}")
for t, body in ms:
    subs = re.split(r"(?m)^### (.*)$", body)
    names = subs[1::2]
    if names != ["Reflection", "Practice", "Key Line"]:
        probs.append(f"{t}: subheadings {names}"); continue
    r, p, k = subs[2], subs[4], subs[6]
    if not 70 <= wc(r) <= 130: probs.append(f"{t}: reflection {wc(r)} words")
    if not 20 <= wc(p) <= 50: probs.append(f"{t}: practice {wc(p)} words")
    q = " ".join(l.lstrip(">").strip() for l in k.strip().splitlines() if l.startswith(">"))
    if not q: probs.append(f"{t}: no quote"); continue
    if re.search(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]", q): probs.append(f"{t}: superscript in quote")
    if norm(q) not in norm(osec.get(t, "")): probs.append(f"{t}: quote not found: {q}")
print("\n".join(probs))
print(f"{len(ms)} sections, {len(probs)} problems")
sys.exit(1 if probs else 0)
