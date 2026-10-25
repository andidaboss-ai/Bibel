import re, sys
base = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/marcus/book/text/'
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
def split(text):
    parts, cur = {}, None
    for line in text.splitlines():
        m = re.match(r'^## (.+)$', line)
        if m: cur = m.group(1).strip(); parts[cur] = []; continue
        if cur: parts[cur].append(line)
    return {k: '\n'.join(v) for k, v in parts.items()}
orig = {k: norm(v) for k, v in split(open(base+'original.md').read()).items()}
ch = split(open(base+'chapters_a.md').read())
want = ['The First Book','The Second Book','The Third Book','The Fourth Book','The Fifth Book','The Sixth Book']
miss = 0
assert list(ch) == want, list(ch)
for b in want:
    body = ch[b]
    secs = re.split(r'^### (.+)$', body, flags=re.M)
    d = {secs[i].strip(): secs[i+1] for i in range(1, len(secs), 2)}
    assert list(d) == ['Reflection','Practice','Key Thought'], (b, list(d))
    wr = len(d['Reflection'].split()); wp = len(d['Practice'].split())
    q = norm(' '.join(l[1:] for l in d['Key Thought'].splitlines() if l.startswith('>')))
    ok = q in orig[b]
    if not ok: miss += 1
    flag = '' if 250 <= wr <= 380 and 60 <= wp <= 120 else '  <-- WORD COUNT'
    print(f'{b}: reflection {wr}, practice {wp}, quote {"OK" if ok else "MISS"}{flag}')
print('misses:', miss)
