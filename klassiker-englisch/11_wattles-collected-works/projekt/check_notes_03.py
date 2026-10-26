import re, sys, os
base = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(base, 'eng/03_being_great.md'), encoding='utf-8').read()
notes = open(os.path.join(base, 'notes/03_being_great.md'), encoding='utf-8').read()
norm = lambda s: re.sub(r'\s+', ' ', s.replace('*', '')).strip()
wc = lambda s: len(re.findall(r"\S+", s))
chapters = {}
order = []
for part in re.split(r'^## ', src, flags=re.M)[1:]:
    t, _, body = part.partition('\n'); t = t.strip()
    order.append(t); chapters[t] = norm(body)
expected = [t for t in order if t != 'Preface']
problems = []
m = re.match(r'# INTRO 03_being_great\n(.*?)(?=^## )', notes, flags=re.S | re.M)
if not m: problems.append('intro missing / not first')
else:
    n = wc(m.group(1))
    if not 250 <= n <= 400: problems.append(f'intro words {n}')
secs = re.split(r'^## ', notes, flags=re.M)[1:]
titles = [s.partition('\n')[0].strip() for s in secs]
if titles != expected: problems.append(f'titles/order mismatch: {titles}')
for s in secs:
    t, _, body = s.partition('\n'); t = t.strip()
    mm = re.match(r'### Reflection\n(.*?)\n### Practice\n(.*?)\n### Key Thought\n(.*)$', body.strip() + '\n', flags=re.S)
    if not mm: problems.append(f'{t}: structure'); continue
    r, p, k = mm.groups()
    if not 90 <= wc(r) <= 150: problems.append(f'{t}: reflection {wc(r)}')
    if not 25 <= wc(p) <= 55: problems.append(f'{t}: practice {wc(p)}')
    q = [l for l in k.strip().splitlines() if l.strip()]
    if len(q) != 1 or not q[0].startswith('> '): problems.append(f'{t}: key thought format'); continue
    if norm(q[0][2:]) not in chapters.get(t, ''): problems.append(f'{t}: quote not found')
for x in problems: print(x)
print(f'{len(problems)} problems')
sys.exit(1 if problems else 0)
