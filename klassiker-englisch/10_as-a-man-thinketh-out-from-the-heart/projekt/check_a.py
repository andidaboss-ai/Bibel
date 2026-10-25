import re, sys
T = 'book/text/'
orig = open(T+'original.md', encoding='utf-8').read()
ch = open(T+'chapters.md', encoding='utf-8').read()
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
def split(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i+1]) for i in range(1, len(parts), 2)]
osec = split(orig)
otitles = [t for t, _ in osec if t != 'Foreword']
obody = {t: norm('\n'.join(l[2:] if l.startswith('| ') else l for l in b.splitlines())) for t, b in osec}
csec = split(ch)
probs = []
if [t for t, _ in csec] != otitles:
    probs.append(f'titles mismatch: {[t for t,_ in csec]}')
wc = lambda s: len(re.findall(r"[A-Za-z0-9'’-]+", s))
for t, b in csec:
    subs = re.split(r'^### (.+)$', b, flags=re.M)
    names = [subs[i].strip() for i in range(1, len(subs), 2)]
    d = {subs[i].strip(): subs[i+1].strip() for i in range(1, len(subs), 2)}
    if names != ['Reflection', 'Practice', 'Key Thought']:
        probs.append(f'{t}: subsections {names}'); continue
    r, p = wc(d['Reflection']), wc(d['Practice'])
    print(f'{t}: reflection {r}, practice {p}')
    if not 110 <= r <= 170: probs.append(f'{t}: reflection {r} words')
    if not 30 <= p <= 60: probs.append(f'{t}: practice {p} words')
    qs = [l[1:].strip() for l in d['Key Thought'].splitlines() if l.startswith('>')]
    if len(qs) != 1: probs.append(f'{t}: {len(qs)} quotes')
    for q in qs:
        if norm(q) not in obody.get(t, ''): probs.append(f'{t}: quote not found: {q}')
    if '>' in d['Reflection'] + d['Practice']: probs.append(f'{t}: stray > ')
print(f'{len(probs)} problems'); [print(' -', x) for x in probs]
sys.exit(1 if probs else 0)
