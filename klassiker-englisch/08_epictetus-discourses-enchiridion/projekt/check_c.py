import re, sys
base = sys.argv[1] if len(sys.argv) > 1 else '.'
orig = open(f'{base}/book/text/original.md', encoding='utf-8').read()
out = open(f'{base}/book/text/chapters_c.md', encoding='utf-8').read()
titles = [l.split('## ',1)[1].strip() for l in open(f'{base}/discourse_list.txt', encoding='utf-8').read().splitlines() if '## ' in l][44:66]
def norm(s):
    s = re.sub(r'(?m)^\| ', '', s)
    return re.sub(r'\s+', ' ', s).strip()
osec = {}
for chunk in re.split(r'(?m)^## ', orig)[1:]:
    t, _, body = chunk.partition('\n'); osec[t.strip()] = norm(body)
probs = []
chunks = re.split(r'(?m)^## ', out)[1:]
got = [c.partition('\n')[0].strip() for c in chunks]
if got != titles: probs.append(f'title mismatch/order: {[ (a,b) for a,b in zip(got,titles) if a!=b ] or (len(got),len(titles))}')
for c in chunks:
    t, _, body = c.partition('\n'); t = t.strip()
    parts = re.split(r'(?m)^### ', body)[1:]
    heads = [p.partition('\n')[0].strip() for p in parts]
    if heads != ['Reflection', 'Practice', 'Key Line']: probs.append(f'{t}: subheads {heads}'); continue
    texts = {p.partition('\n')[0].strip(): p.partition('\n')[2].strip() for p in parts}
    wr = len(texts['Reflection'].split()); wp = len(texts['Practice'].split())
    if not 80 <= wr <= 140: probs.append(f'{t}: Reflection {wr} words')
    if not 25 <= wp <= 55: probs.append(f'{t}: Practice {wp} words')
    q = [l for l in texts['Key Line'].splitlines() if l.strip()]
    if not q or not all(l.startswith('> ') for l in q): probs.append(f'{t}: Key Line not a > quote'); continue
    qt = norm(' '.join(l[2:] for l in q))
    if t not in osec: probs.append(f'{t}: section not in original'); continue
    if qt not in osec[t]: probs.append(f'{t}: quote not verbatim: {qt}')
    print(f'{wr:4d} {wp:3d}  {t}')
print(f'{len(probs)} problems'); [print(' -', p) for p in probs]
