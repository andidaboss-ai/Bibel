#!/usr/bin/env python3
"""Check front/thirty_days/finder/back for the Allen annotated edition."""
import re, sys, os
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'book', 'text')
rd = lambda f: open(os.path.join(T, f), encoding='utf-8').read()
orig = rd('original.md')
chap, cur = {}, None
for line in orig.splitlines():
    if line.startswith('## '):
        cur = line[3:].strip(); chap[cur] = []; continue
    if cur:
        chap[cur].append(re.sub(r'^\|\s?', '', line))
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
ctext = {k: norm('\n'.join(v)) for k, v in chap.items()}
titles = [t for t in chap if t != 'Foreword']
miss = []
wc = lambda s: len(re.findall(r"[A-Za-z0-9’'-]+", re.sub(r'[*_>#]', ' ', s)))
def sections(s, lvl='## '):
    out, name = {}, None
    for line in s.splitlines():
        if line.startswith(lvl) and not line.startswith(lvl + '#'):
            name = line[len(lvl):].strip(); out[name] = []
        elif name is not None:
            out[name].append(line)
    return {k: '\n'.join(v) for k, v in out.items()}
def rng(label, n, lo, hi):
    ok = lo <= n <= hi
    print(f"  {'ok ' if ok else 'MISS'} {label}: {n} words ({lo}-{hi})")
    if not ok: miss.append(label)
# front
print('front.md'); fs = sections(rd('front.md'))
for name, lo, hi in [('How to Use This Book',300,420),('Who Was James Allen?',400,600),('The Ideas in Brief',400,550),('A Note on This Text',150,250)]:
    if name not in fs: miss.append('front missing ' + name); print('  MISS missing', name); continue
    rng(name, wc(fs[name]), lo, hi)
if list(fs) != ['How to Use This Book','Who Was James Allen?','The Ideas in Brief','A Note on This Text']:
    miss.append('front order'); print('  MISS order', list(fs))
# thirty days
print('thirty_days.md'); td = rd('thirty_days.md')
intro = td.split('### Day 1')[0].split('## The 30-Day Practice', 1)[1]
rng('intro', wc(intro), 150, 250)
days = re.split(r'^### ', td, flags=re.M)[1:]
nums = []
for d in days:
    head, *body = d.split('\n'); m = re.match(r'Day (\d+) – (.+)$', head)
    if not m: miss.append('bad head ' + head); print('  MISS head', head); continue
    n = int(m.group(1)); nums.append(n); body = '\n'.join(body)
    qs = [l[2:].strip() for l in body.splitlines() if l.startswith('> ')]
    src = re.findall(r'^Source: (.+)$', body, flags=re.M)
    if len(qs) != 1 or len(src) != 1:
        miss.append(f'day {n} structure'); print(f'  MISS day {n}: {len(qs)} quotes, {len(src)} sources'); continue
    q, s = qs[0], src[0].strip()
    if s not in titles: miss.append(f'day {n} source'); print(f'  MISS day {n}: bad source {s!r}'); continue
    if norm(q) not in ctext[s]: miss.append(f'day {n} quote'); print(f'  MISS day {n}: quote not in {s}: {q}')
    if wc(q) > 40: miss.append(f'day {n} long'); print(f'  MISS day {n}: quote {wc(q)} words')
    task = body.split('Source:')[1].split('\n', 1)[1].strip()
    sn = len(re.findall(r'[.!?](?:["”)]?)(?:\s|$)', task))
    if not 2 <= sn <= 4: miss.append(f'day {n} task'); print(f'  MISS day {n}: task {sn} sentences')
if nums != list(range(1, 31)): miss.append('day numbering'); print('  MISS numbering', nums)
used = {}
for d in days:
    s = re.search(r'^Source: (.+)$', d, flags=re.M)
    if s: used[s.group(1)] = used.get(s.group(1), 0) + 1
print('  chapters used:', len(used), '/', len(titles), '; unused:', [t for t in titles if t not in used])
# finder
print('finder.md'); fl = [l for l in rd('finder.md').splitlines() if l.startswith('- ')]
if not 18 <= len(fl) <= 25: miss.append('finder count'); print('  MISS count', len(fl))
for l in fl:
    m = re.match(r'- \*\*(.+?)\*\* — (.+) · Days? ([\d, ]+)$', l)
    if not m: miss.append('finder fmt'); print('  MISS fmt', l); continue
    for c in m.group(2).split('; '):
        if c not in titles: miss.append('finder chap'); print('  MISS chapter', c)
    for d in m.group(3).split(','):
        if not 1 <= int(d) <= 30: miss.append('finder day'); print('  MISS day', d)
print(f'  {len(fl)} entries checked')
# back
print('back.md'); bs = sections(rd('back.md'))
gl = re.findall(r'^- \*\*(.+?)\*\* — ', bs.get('A Glossary', ''), flags=re.M)
key = lambda w: re.sub(r'^the ', '', w.lower()).replace("'", '')
if not 20 <= len(gl) <= 35: miss.append('glossary count'); print('  MISS glossary count', len(gl))
if [key(g) for g in gl] != sorted(key(g) for g in gl): miss.append('glossary order'); print('  MISS glossary not alphabetical')
print(f'  glossary {len(gl)} entries')
aft = [k for k in bs if k.startswith('Afterword')]
if aft: rng('Afterword', wc(bs[aft[0]]), 250, 400)
else: miss.append('afterword'); print('  MISS afterword')
if 'Further Reading' not in bs: miss.append('further'); print('  MISS further reading')
# any other > quotes in these files must be in original
for f in ['front.md', 'finder.md', 'back.md']:
    for l in rd(f).splitlines():
        if l.startswith('> ') and norm(l[2:]) not in norm(orig.replace('| ', '')):
            miss.append(f + ' quote'); print('  MISS', f, l)
print(f'\n{len(miss)} misses'); sys.exit(1 if miss else 0)
