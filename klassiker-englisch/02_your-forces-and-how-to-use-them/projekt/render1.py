import re, json
from collections import Counter
W = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/'
SRC = W + 'src/'
r = json.load(open(W + 'work1/merged2.json'))

def key(t):
    return re.sub(r'[^a-z0-9]', '', t.lower().replace('­', ''))

# hyphenated compounds appearing mid-line in either text
mid = Counter()
for fn in ('a.txt', 'b.txt'):
    for line in open(SRC + fn, encoding='utf-8'):
        for w in re.findall(r'[A-Za-z]+-[A-Za-z]+(?:-[A-Za-z]+)?', line.rstrip()[:-1] if line.rstrip().endswith('-') else line):
            mid[w.lower()] += 1
VA = Counter()
for fn in ('a.txt', 'b.txt'):
    txt = open(SRC + fn, encoding='utf-8').read()
    txt = re.sub(r'-\s*\n\s*', '', txt)
    for w in txt.split(): VA[key(w)] += 1

hyph_log = []
def dehyph(w):
    if '­' not in w: return w
    parts = w.split('­')
    out = parts[0]
    for p in parts[1:]:
        l = re.sub(r'[^A-Za-z\-]', '', out.split('-')[-1] if False else out).lower()
        lw = re.findall(r'[A-Za-z]+$', out)
        rw = re.findall(r'^[A-Za-z]+', p)
        if lw and rw:
            comp = (lw[0] + '-' + rw[0]).lower()
            if mid[comp] > 0:
                out = out + '-' + p; hyph_log.append(comp); continue
        out = out + p
    return out

paras = [[]]
for w, na, nb, tag in r:
    if w == '¶':
        paras.append([]); continue
    if w == '¶?':
        paras[-1].append('⟦BRK?⟧'); continue
    if w in ('',):
        continue
    paras[-1].append(dehyph(w))
txt = '\n\n'.join(' '.join(p) for p in paras if p)
open(W + 'work1/draft.txt', 'w').write(txt)
open(W + 'work1/hyph.txt', 'w').write('\n'.join(sorted(set(hyph_log))))
# suspicious tokens
sus = Counter()
for w in txt.split():
    k = key(w)
    if k and VA[k] < 4 and not k.isdigit():
        sus[w] += 1
open(W + 'work1/sus.txt', 'w').write('\n'.join('%s\t%d' % (w, c) for w, c in sus.most_common()))
print(len(paras), len(sus))
