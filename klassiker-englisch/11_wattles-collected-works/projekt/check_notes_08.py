"""Check editorial notes for 08_living_healing and 09_hellfire_harrison.
usage: python3 check_notes_08.py
Verifies: INTRO heading and 250-400 words; chapter titles and order match eng/ file;
each chapter has Reflection (90-150), Practice (25-55), Key Thought quote found verbatim
(whitespace-normalised) in the same chapter of the eng/ file."""
import re, os
D = os.path.dirname(os.path.abspath(__file__))
W = lambda t: len(re.findall(r"[A-Za-z0-9’'-]+", t))
norm = lambda t: re.sub(r'\s+', ' ', t).strip()

def secs(text):
    parts = re.split(r'^## (.*)$', text, flags=re.M)
    return parts[0], [(parts[i].strip(), parts[i+1]) for i in range(1, len(parts), 2)]

bad = 0
def err(m):
    global bad; bad += 1; print('PROBLEM:', m)

for name in ['08_living_healing', '09_hellfire_harrison']:
    src = open(os.path.join(D, 'eng', name + '.md')).read()
    out = open(os.path.join(D, 'notes', name + '.md')).read()
    _, es = secs(src); head, ns = secs(out)
    m = re.match(r'\s*# INTRO (\S+)\s*\n(.*)', head, flags=re.S)
    if not m or m.group(1) != name: err(f'{name}: missing/wrong INTRO heading')
    else:
        n = W(m.group(2)); print(f'{name} INTRO {n} words')
        if not 250 <= n <= 400: err(f'{name}: intro {n} words')
    if [t for t, _ in es] != [t for t, _ in ns]:
        err(f'{name}: titles/order differ: {[t for t,_ in ns]}')
    ed = dict(es)
    for t, body in ns:
        p = re.split(r'^### (Reflection|Practice|Key Thought)\s*$', body, flags=re.M)
        d = {p[i]: p[i+1] for i in range(1, len(p), 2)}
        if list(d) != ['Reflection', 'Practice', 'Key Thought']:
            err(f'{name}/{t}: subsections {list(d)}'); continue
        r, pr = W(d['Reflection']), W(d['Practice'])
        if not 90 <= r <= 150: err(f'{name}/{t}: Reflection {r}')
        if not 25 <= pr <= 55: err(f'{name}/{t}: Practice {pr}')
        q = [l[1:].strip() for l in d['Key Thought'].strip().splitlines() if l.startswith('>')]
        if len(q) != 1 or not q[0]: err(f'{name}/{t}: key thought missing'); continue
        if t in ed and norm(q[0]) not in norm(ed[t]): err(f'{name}/{t}: quote not verbatim: {q[0][:60]}')
        print(f'  {t[:40]:40s} R{r:4d} P{pr:3d}')
print('problems:', bad)
