"""Completeness check: Spanish translation vs English source, chapter by chapter.
usage: python3 check_es.py <english.md> <spanish.md> [first_en_index last_index]
Ratio = Spanish words / English words; expected 0.85–1.45. Paragraph counts per chapter must match."""
import re, sys
def secs(p):
    s = open(p).read(); parts = re.split(r'^## (.*)$', s, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
en = secs(sys.argv[1]); es = secs(sys.argv[2])
if len(sys.argv) > 3: en = en[int(sys.argv[3]):int(sys.argv[4]) + 1]
w = lambda t: len(re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9’'-]+", t))
np = lambda t: len([p for p in t.split('\n\n') if p.strip()])
bad = 0
if len(en) != len(es): print(f'CHAPTER COUNT: en {len(en)} es {len(es)}'); bad += 1
for (te, be), (ts, bs) in zip(en, es):
    r = w(bs) / max(1, w(be)); flag = ''
    if not 0.85 <= r <= 1.45: flag += '  <-- RATIO'
    if np(be) != np(bs): flag += f'  <-- PARAS en {np(be)} es {np(bs)}'
    if flag: bad += 1
    print(f'{w(be):6d} {w(bs):6d} {r:5.2f}  {te[:36]:36s} | {ts[:36]}{flag}')
t = open(sys.argv[2]).read()
for pat, name in [(r'"', 'straight double quote'), (r"(?<=\w)'(?=\w)", "straight apostrophe"), (r'[„‚]', 'German quote'),
                  (r'\b(the|and|of|that|with)\b', 'English word?')]:
    n = len(re.findall(pat, t))
    if n: print('WARN', name, n)
for i, p in enumerate(t.split('\n\n')):
    if p.count('?') > p.count('¿') or p.count('!') > p.count('¡'):
        print('WARN missing ¿/¡ in paragraph', i, ':', p.strip()[:70])
if t.count('*') % 2: print('WARN odd number of *')
print('problems:', bad)
