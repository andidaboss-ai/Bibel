import re, sys
B = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/kempis/'
orig = open(B+'book/text/original.md', encoding='utf-8').read()
titles = [l.strip()[3:] if l.strip().startswith('## ') else l.strip() for l in open(B+'chapter_list.txt', encoding='utf-8')]
titles = [re.sub(r'^\s*\d+\s*', '', t) for t in titles]
titles = [t[3:] if t.startswith('## ') else t for t in titles]
want = titles[68:97]
# split original into sections
secs = {}
parts = re.split(r'^## (.+)$', orig, flags=re.M)
for i in range(1, len(parts), 2):
    secs[parts[i].strip()] = parts[i+1]
ws = lambda s: re.sub(r'\s+', ' ', s).strip()
doc = open(B+'book/text/chapters_d.md', encoding='utf-8').read()
dp = re.split(r'^## (.+)$', doc, flags=re.M)
got = [dp[i].strip() for i in range(1, len(dp), 2)]
probs = []
if got != want:
    probs.append('title mismatch: %d got vs %d want' % (len(got), len(want)))
    for a, b in zip(got, want):
        if a != b: probs.append('  %r != %r' % (a, b))
for i in range(1, len(dp), 2):
    t = dp[i].strip(); body = dp[i+1]
    sub = re.split(r'^### (.+)$', body, flags=re.M)
    heads = [sub[j].strip() for j in range(1, len(sub), 2)]
    if heads != ['Reflection', 'Practice', 'Key Line']:
        probs.append(f'{t}: headings {heads}'); continue
    r, p, k = (sub[j+1] for j in range(1, len(sub), 2))
    for name, txt, lo, hi in (('Reflection', r, 70, 130), ('Practice', p, 20, 50)):
        n = len(txt.split())
        if not lo <= n <= hi: probs.append(f'{t}: {name} {n} words')
    q = ws(' '.join(l.lstrip('>').strip() for l in k.strip().splitlines() if l.startswith('>')))
    if not q: probs.append(f'{t}: no quote')
    elif re.search('[¹²³⁴⁵⁶⁷⁸⁹⁰]', q): probs.append(f'{t}: marker in quote')
    elif q not in ws(secs.get(t, '')): probs.append(f'{t}: quote not found: {q}')
for x in probs: print(x)
print(len(probs), 'problems')
