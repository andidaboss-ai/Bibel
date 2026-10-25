import re, sys, os
base = os.path.dirname(os.path.abspath(__file__))
orig = open(os.path.join(base, 'book/text/original.md'), encoding='utf-8').read()
out = open(os.path.join(base, 'book/text/chapters_b.md'), encoding='utf-8').read()
titles = [re.sub(r'^\s*\d*\s*## ', '', l).strip() for l in open(os.path.join(base, 'discourse_list.txt'), encoding='utf-8')
          if '## ' in l][22:44]
def norm(s):
    s = re.sub(r'(?m)^\|\s?', '', s)
    return re.sub(r'\s+', ' ', s).strip()
# split original into sections
secs = {}
for m in re.finditer(r'(?m)^## ([^\n]+)\n(.*?)(?=^## |\Z)', orig, re.S):
    secs.setdefault(m.group(1).strip(), norm(m.group(2)))
problems = []
parts = re.split(r'(?m)^## ', out)[1:]
got = [p.split('\n', 1)[0].strip() for p in parts]
if got != titles:
    problems.append(f'titles mismatch:\n got {got}\n want {titles}')
wc = lambda s: len(re.findall(r"[A-Za-z0-9’'-]+", s))
for p in parts:
    t, body = p.split('\n', 1)
    t = t.strip()
    subs = re.split(r'(?m)^### ', body)
    names = [s.split('\n', 1)[0].strip() for s in subs[1:]]
    if names != ['Reflection', 'Practice', 'Key Line']:
        problems.append(f'{t}: subsections {names}'); continue
    d = {s.split('\n', 1)[0].strip(): s.split('\n', 1)[1].strip() for s in subs[1:]}
    r, pr = wc(d['Reflection']), wc(d['Practice'])
    if not 80 <= r <= 140: problems.append(f'{t}: Reflection {r} words')
    if not 25 <= pr <= 55: problems.append(f'{t}: Practice {pr} words')
    print(f'{r:4d} {pr:3d}  {t[:60]}')
    if t not in secs:
        problems.append(f'{t}: not in original'); continue
    quotes = re.findall(r'(?m)^> (.+)$', body)
    if len(quotes) != 1 or not d['Key Line'].startswith('>'):
        problems.append(f'{t}: expected one Key Line quote')
    for q in re.findall(r'(?m)^> (.+)$', body):
        if norm(q) not in secs[t]:
            problems.append(f'{t}: quote not found: {q}')
print(f'{len(problems)} problems')
for x in problems: print(' -', x)
sys.exit(1 if problems else 0)
