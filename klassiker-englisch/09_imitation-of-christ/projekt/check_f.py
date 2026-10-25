#!/usr/bin/env python3
"""Check front/thirty_days/finder/back for the annotated Imitation."""
import re, sys, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'book', 'text')
orig = open(os.path.join(D, 'original.md'), encoding='utf-8').read()
parts = re.split(r'(?m)^## ', orig)[1:]
SUP = '¹²³⁴⁵⁶⁷⁸⁹⁰'
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def plain(s):  # section text as quotable: superscripts removed
    return norm(re.sub('[' + SUP + ']', '', s))
BOOKS = {'One': (2, 26), 'Two': (27, 38), 'Three': (39, 97), 'Four': (99, 116)}
def ref_to_idx(ref):
    ref = ref.strip()
    if ref == 'Book Four, A Devout Exhortation': return 98
    m = re.fullmatch(r'Book (One|Two|Three|Four), Chapter (\d+)', ref)
    if not m: return None
    a, b = BOOKS[m.group(1)]; n = int(m.group(2))
    return a + n - 1 if 1 <= n <= b - a + 1 else None
miss = []
def wc(s): return len(re.findall(r"[A-Za-z0-9’'à-]+", s))
def sections(text, level='## '):
    out = {}; cur = None
    for line in text.split('\n'):
        if line.startswith(level) and not line.startswith(level + '#'):
            cur = line[len(level):].strip(); out[cur] = []
        elif cur: out[cur].append(line)
    return {k: '\n'.join(v) for k, v in out.items()}
def rng(name, text, lo, hi):
    n = wc(text); ok = lo <= n <= hi
    print(f"  {name}: {n} words ({lo}-{hi}) {'OK' if ok else 'MISS'}")
    if not ok: miss.append(f'{name} word count {n}')
whole = plain('\n'.join(parts)).replace('*', '')
# front
print('front.md')
fs = sections(open(os.path.join(D, 'front.md'), encoding='utf-8').read())
for t, lo, hi in [('How to Use This Book', 300, 420), ('Who Was Thomas à Kempis?', 450, 650),
                  ('The Imitation in Brief', 400, 550), ('A Note on This Translation', 200, 300)]:
    if t not in fs: miss.append('front missing ' + t); continue
    rng(t, fs[t], lo, hi)
# thirty days
print('thirty_days.md')
td = open(os.path.join(D, 'thirty_days.md'), encoding='utf-8').read()
top = sections(td)
if 'The 30-Day Practice' not in top: miss.append('no 30-Day heading')
intro = td.split('### Day 1')[0].split('## The 30-Day Practice', 1)[-1]
rng('intro', intro, 150, 250)
days = re.split(r'(?m)^### ', td)[1:]
nums = []
day_src = {}
for d in days:
    head, body = d.split('\n', 1)
    m = re.fullmatch(r'Day (\d+) – (.+)', head.strip())
    if not m: miss.append('bad day head ' + head); continue
    n = int(m.group(1)); nums.append(n)
    q = [l[1:].strip() for l in body.split('\n') if l.startswith('>')]
    src = re.findall(r'(?m)^Source: (.+)$', body)
    if len(q) != 1 or len(src) != 1: miss.append(f'Day {n}: quote/source count'); continue
    q = q[0]; idx = ref_to_idx(src[0])
    if idx is None: miss.append(f'Day {n}: bad source {src[0]}'); continue
    day_src[n] = idx
    if any(c in q for c in SUP): miss.append(f'Day {n}: superscript in quote')
    if wc(q) > 42: miss.append(f'Day {n}: quote too long ({wc(q)})')
    if norm(q) not in plain(parts[idx - 1]):
        miss.append(f'Day {n}: quote not in section {idx} ({src[0]}): {q[:60]}')
    task = body.split(src[0], 1)[1].strip()
    sents = len(re.findall(r'[.!?]["”’]?(\s|$)', task))
    if not 2 <= sents <= 4: miss.append(f'Day {n}: task has {sents} sentences')
if nums != list(range(1, 31)): miss.append(f'day numbering {nums}')
print(f'  {len(nums)} days checked')
# finder
print('finder.md')
fl = [l for l in open(os.path.join(D, 'finder.md'), encoding='utf-8').read().split('\n') if l.startswith('- ')]
if not 20 <= len(fl) <= 25: miss.append(f'finder has {len(fl)} rows')
for l in fl:
    m = re.fullmatch(r'- \*\*(.+?)\*\* — (.+) · Days? (\d+(?:, \d+)*)', l)
    if not m: miss.append('finder bad format: ' + l); continue
    idxs = []
    for r in m.group(2).split('; '):
        i = ref_to_idx(r)
        if i is None: miss.append(f'finder bad ref {r!r}')
        idxs.append(i)
    for dn in map(int, m.group(3).split(', ')):
        if not 1 <= dn <= 30: miss.append(f'finder bad day {dn}')
        elif day_src.get(dn) not in idxs: print(f'  note: Day {dn} source not among refs in: {m.group(1)}')
print(f'  {len(fl)} rows checked')
# back
print('back.md')
bk = open(os.path.join(D, 'back.md'), encoding='utf-8').read()
bs = sections(bk)
for t in ['A Glossary', 'Afterword: The Hidden Life', 'Further Reading']:
    if t not in bs: miss.append('back missing ' + t)
g = [l for l in bs.get('A Glossary', '').split('\n') if l.startswith('- **')]
if not 25 <= len(g) <= 40: miss.append(f'glossary {len(g)} entries')
keys = [re.sub(r'^(the )|["“”\-]', '', re.match(r'- \*\*(.+?)\*\*', l).group(1)).lower() for l in g]
if keys != sorted(keys): miss.append('glossary not alphabetical: ' + str(keys))
print(f'  glossary {len(g)} entries')
rng('Afterword', bs.get('Afterword: The Hidden Life', ''), 250, 400)
# inline quotations attributed to Thomas in front/back (straight double quotes containing thou/thy)
for fn in ['front.md', 'back.md', 'thirty_days.md']:
    for q in re.findall(r'"([^"]+)"', open(os.path.join(D, fn), encoding='utf-8').read()):
        if re.search(r'\b(thou|thyself|thee|shall not walk)\b', q) and norm(q) not in whole:
            miss.append(f'{fn}: inline quote not verbatim: {q}')
print('\nMISSES:', len(miss))
for m in miss: print(' -', m)
sys.exit(1 if miss else 0)
