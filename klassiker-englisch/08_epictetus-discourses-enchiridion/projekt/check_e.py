#!/usr/bin/env python3
"""Check front/thirty_days/finder/back for the Epictetus edition."""
import os, re, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'book', 'text')
miss = 0

def err(msg):
    global miss
    miss += 1
    print('MISS:', msg)

def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s).strip()

def words(s):
    return len(re.findall(r"[A-Za-z0-9À-ɏ’'*-]+", s))

# --- original sections
secs = {}
order = []
cur = None
for line in open(os.path.join(BASE, 'original.md'), encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('## '):
        cur = line[3:].strip(); secs[cur] = []; order.append(cur); continue
    if cur is None: continue
    secs[cur].append(line[2:] if line.startswith('| ') else line)
secs = {k: norm(' '.join(v)) for k, v in secs.items()}

def resolve(ref):
    ref = ref.strip()
    m = re.fullmatch(r'Enchiridion, Chapter (\d+)', ref)
    if m:
        t = 'Chapter ' + m.group(1)
        return t if t in secs else None
    if ref.startswith('Chapter '):
        return None  # must be written "Enchiridion, Chapter N"
    return ref if ref in secs and not ref.startswith('George Long') else None

def split_md(path):
    """Return list of (title, body) for ## sections."""
    out, t, b = [], None, []
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('## '):
            if t: out.append((t, b))
            t, b = line[3:].strip(), []
        elif t: b.append(line)
    if t: out.append((t, b))
    return out

def prose(lines):
    return ' '.join(l for l in lines if not l.startswith('#'))

# --- thirty days
path = os.path.join(BASE, 'thirty_days.md')
text = open(path, encoding='utf-8').read()
if not text.startswith('## The 30-Day Practice'):
    err('thirty_days: missing heading')
parts = re.split(r'^### ', text, flags=re.M)
intro = parts[0].split('\n', 1)[1]
w = words(intro)
print('30-day intro words:', w)
if not 150 <= w <= 250: err('30-day intro word count %d' % w)
days = parts[1:]
if len(days) != 30: err('expected 30 days, got %d' % len(days))
for i, d in enumerate(days, 1):
    head, body = d.split('\n', 1)
    m = re.fullmatch(r'Day (\d+) – (.+)', head.strip())
    if not m or int(m.group(1)) != i:
        err('bad day heading: %r' % head); continue
    quotes = [l[1:].strip() for l in body.split('\n') if l.startswith('>')]
    srcs = re.findall(r'^Source: (.+)$', body, flags=re.M)
    if len(quotes) != 1 or len(srcs) != 1:
        err('Day %d: needs exactly one quote line and one Source line' % i); continue
    title = resolve(srcs[0])
    if not title:
        err('Day %d: invalid Source %r' % (i, srcs[0])); continue
    q = norm(quotes[0])
    if q not in secs[title]:
        err('Day %d: quote not found in %s: %s' % (i, title, q))
    if words(q) > 42: err('Day %d: quote too long (%d words)' % (i, words(q)))
    task = body.split('Source:', 1)[1].split('\n', 1)[1].strip()
    n = len(re.findall(r'[.!?](?:["”)]*)(?:\s|$)', task))
    if not 2 <= n <= 4: err('Day %d: task has %d sentences' % (i, n))

# --- finder
path = os.path.join(BASE, 'finder.md')
lines = open(path, encoding='utf-8').read().split('\n')
if lines[0] != '## Quick Finder': err('finder: heading')
items = [l for l in lines if l.startswith('- ')]
print('finder items:', len(items))
if not 20 <= len(items) <= 25: err('finder: %d items' % len(items))
for l in items:
    m = re.fullmatch(r'- \*\*(.+?)\*\* — (.+?) · Days? ([\d, ]+)', l)
    if not m: err('finder format: %s' % l); continue
    pieces = m.group(2).split('; ')
    buf = ''
    for p in pieces:
        buf = p if not buf else buf + '; ' + p
        if resolve(buf):
            buf = ''
    if buf: err('finder bad reference %r in: %s' % (buf, l))
    for dn in m.group(3).split(','):
        if not 1 <= int(dn) <= 30: err('finder bad day %s' % dn)

# --- front & back word counts
ranges = {
    'How to Use This Book': (300, 420), 'Who Was Epictetus?': (450, 650),
    'Stoicism in Brief': (450, 600), 'A Note on This Translation': (200, 300),
}
for fn in ('front.md', 'back.md'):
    for t, b in split_md(os.path.join(BASE, fn)):
        w = words(prose(b))
        print('%s / %s: %d words' % (fn, t, w))
        if t in ranges and not ranges[t][0] <= w <= ranges[t][1]:
            err('%s word count %d' % (t, w))
        if t.startswith('Afterword') and not 250 <= w <= 400:
            err('Afterword word count %d' % w)
        if t == 'A Glossary':
            ent = [l for l in b if l.startswith('- **')]
            terms = [re.match(r'- \*\*(.+?)\*\*', l).group(1) for l in ent]
            print('glossary entries:', len(ent))
            if not 25 <= len(ent) <= 40: err('glossary entries %d' % len(ent))
            key = [re.sub(r'^the ', '', x.lower()).replace('æ', 'ae') for x in terms]
            if key != sorted(key): err('glossary not alphabetical')
        for l in b:
            if l.startswith('>'):
                q = norm(l[1:])
                if not any(q in s for s in secs.values()): err('%s quote not in text: %s' % (fn, q))
    if 'front' in fn:
        pass
names = [t for t, _ in split_md(os.path.join(BASE, 'front.md'))]
if names != list(ranges): err('front.md headings: %s' % names)

print('\nMISSES:', miss)
sys.exit(1 if miss else 0)
