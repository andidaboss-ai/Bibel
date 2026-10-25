import re, sys
base = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/lawrence/book/text/'
orig = open(base + 'original.md', encoding='utf-8').read()
ch = open(base + 'chapters_b.md', encoding='utf-8').read()
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
def split(t):
    parts = re.split(r'^## (.+)$', t, flags=re.M)
    return [(parts[i].strip(), parts[i+1]) for i in range(1, len(parts), 2)]
osec = dict(split(orig))
want = ['Sixth','Seventh','Eighth','Ninth','Tenth','Eleventh','Twelfth','Thirteenth','Fourteenth','Fifteenth']
want = [w + ' Letter' for w in want]
secs = split(ch)
probs = []
if [s for s, _ in secs] != want:
    probs.append('heading order: %s' % [s for s, _ in secs])
wc = lambda s: len(re.findall(r"[A-Za-z0-9'’-]+", s))
for name, body in secs:
    sub = re.split(r'^### (.+)$', body, flags=re.M)
    subs = [(sub[i].strip(), sub[i+1]) for i in range(1, len(sub), 2)]
    if [s for s, _ in subs] != ['Reflection', 'Practice', 'Key Line']:
        probs.append(f'{name}: subheadings {[s for s,_ in subs]}'); continue
    d = dict(subs)
    r, p = wc(d['Reflection']), wc(d['Practice'])
    print(f'{name}: reflection {r}, practice {p}')
    if not 80 <= r <= 150: probs.append(f'{name}: reflection {r} words')
    if not 25 <= p <= 60: probs.append(f'{name}: practice {p} words')
    src = norm(osec.get(name, ''))
    q = norm(' '.join(l[1:].strip() for l in d['Key Line'].splitlines() if l.startswith('>')))
    if not q: probs.append(f'{name}: no key line')
    elif q not in src: probs.append(f'{name}: key line not verbatim: {q}')
    for m in re.findall(r'"([^"]+)"', d['Reflection'] + d['Practice']):
        mm = m.rstrip('.,;:')
        if mm not in src:
            print(f'  note (inline quote not in section, check it is own wording): {m}')
print('\n'.join(probs))
print(f'{len(probs)} problems')
sys.exit(1 if probs else 0)
