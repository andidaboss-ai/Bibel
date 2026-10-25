import re, sys, os
base = os.path.dirname(os.path.abspath(__file__))
orig = open(os.path.join(base, 'book/text/original.md'), encoding='utf-8').read()
out = open(os.path.join(base, 'book/text/chapters_d.md'), encoding='utf-8').read()

def norm(s):
    s = re.sub(r'^\| ?', '', s, flags=re.M)
    return re.sub(r'\s+', ' ', s).strip()

def sections(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]

osec = {t: norm(b) for t, b in sections(orig)}
expected = [f'Chapter {i}' for i in range(1, 53)]
got = sections(out)
problems = []
if [t for t, _ in got] != expected:
    problems.append('titles/order mismatch: %s' % [t for t, _ in got])
wc = lambda s: len(s.split())
for title, body in got:
    sub = re.split(r'^### (.+)$', body, flags=re.M)
    heads = [sub[i].strip() for i in range(1, len(sub), 2)]
    if heads != ['Reflection', 'Practice', 'Key Line']:
        problems.append(f'{title}: subheads {heads}')
        continue
    refl, prac, key = (sub[i] for i in (2, 4, 6))
    if not 50 <= wc(refl) <= 100:
        problems.append(f'{title}: Reflection {wc(refl)} words')
    if not 20 <= wc(prac) <= 45:
        problems.append(f'{title}: Practice {wc(prac)} words')
    qlines = [l for l in key.strip().splitlines() if l.strip()]
    if not qlines or not all(l.startswith('>') for l in qlines):
        problems.append(f'{title}: Key Line not a > quote')
        continue
    q = norm(' '.join(l[1:] for l in qlines))
    if title not in osec or q not in osec[title]:
        problems.append(f'{title}: quote not found: {q}')
    for l in (refl + prac).splitlines():
        if l.startswith('>'):
            problems.append(f'{title}: stray quote in body')
for p in problems:
    print(p)
print(f'{len(problems)} problems')
sys.exit(1 if problems else 0)
