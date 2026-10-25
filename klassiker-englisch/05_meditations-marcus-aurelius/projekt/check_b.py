import re, sys, os
base = os.path.dirname(os.path.abspath(__file__))
orig = open(os.path.join(base, 'book/text/original.md'), encoding='utf-8').read()
chap = open(os.path.join(base, 'book/text/chapters_b.md'), encoding='utf-8').read()
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
def split(t):
    parts = re.split(r'^## (.+)$', t, flags=re.M)
    return {parts[i].strip(): parts[i+1] for i in range(1, len(parts), 2)}
ob, cb = split(orig), split(chap)
expected = ['The %s Book' % n for n in ['Seventh','Eighth','Ninth','Tenth','Eleventh','Twelfth']]
miss = 0
if list(cb) != expected:
    print('TITLE/ORDER MISMATCH', list(cb)); miss += 1
wc = lambda s: len(re.findall(r"[A-Za-z0-9’'\-]+", s))
for title, body in cb.items():
    secs = dict(zip(*[iter(re.split(r'^### (.+)$', body, flags=re.M)[1:])]*2))
    r, p = wc(secs.get('Reflection','')), wc(secs.get('Practice',''))
    flag = '' if 250 <= r <= 380 and 60 <= p <= 120 else '  <-- WORDCOUNT'
    if flag: miss += 1
    print(f'{title}: Reflection {r}, Practice {p}{flag}')
    for q in re.findall(r'^>\s*(.+)$', body, flags=re.M):
        ok = norm(q) in norm(ob.get(title, ''))
        if not ok: miss += 1
        print('  ', 'OK  ' if ok else 'MISS', q[:70])
print('misses:', miss)
sys.exit(1 if miss else 0)
