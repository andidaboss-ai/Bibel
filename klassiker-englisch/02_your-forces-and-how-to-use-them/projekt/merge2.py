import re, json, difflib
from collections import Counter

W = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/'
SRC = W + 'src/'

def key(t):
    return re.sub(r'[^a-z0-9]', '', t.lower().replace('­', ''))

def vocab_from(fn):
    txt = open(SRC + fn, encoding='utf-8').read()
    txt = re.sub(r'-\s*\n\s*', '', txt)
    return Counter(key(w) for w in txt.split())

VA = vocab_from('a.txt'); VB = vocab_from('b.txt')
def bigrams_from(fn):
    txt = open(SRC + fn, encoding='utf-8').read()
    txt = re.sub(r'-\s*\n\s*', '', txt)
    ks = [key(w) for w in txt.split()]
    return Counter(zip(ks, ks[1:]))
BA = bigrams_from('a.txt'); BB = bigrams_from('b.txt')
import math
def bg(x, y):
    return min(BA[(x, y)], BB[(x, y)])
def plaus(k):
    return min(VA[k], VB[k])
def freq(k):
    # need word in both texts ideally
    return min(VA[k], VB[k]) if k else 99

def fixline(s, src):
    s = re.sub(r'\s+', ' ', s).strip()
    if src == 'a':
        s = s.replace('’ ’', '”').replace('‘ ‘', '“')
        # right-margin junk after a final hyphen
        s = re.sub(r'(\w)[\-\*][;:\^\'’\*\.,]?$', r'\1-', s)
    else:
        s = re.sub(r'(\w)[\-][;:\^\'’\*\.,]?$', r'\1-', s)
    return s

def is_junk(t):
    if not t: return False
    if re.fullmatch(r'[\d\s\.,]+', t): return True
    low = t.lower()
    if 'googl' in low or 'coo>' in low or re.search(r'o,i,|ih,\.|^[\s,\.]+$', low): return True
    if re.search(r'^\W*\d*\W*(y|t)o[uo][rbe]?\s+f[oe][rbe]+c', low) and len(t) < 50 and ',' not in low: return True
    if re.fullmatch(r"[^a-z]*\S{3,6}\s+\S{4,8}\s+\S{2,4}\s+\S{3,4}\s*\S{2}\s+\S{2,4}\s+\S{3,5}[^a-z]*", low) and re.search(r'h\S{1,2}\s*\S{2}\s+\S{2,4}\s+\S{3,5}[^a-z]*$', low) and "," not in low: return True
    if low.strip() in ('use them', 'your forces and how to'): return True
    if re.search(r'^\d*\s*(f[oe][rbe]+w[oq][rbe]+d)\s*\d*$', low): return True
    if len(t) <= 4 and not re.search(r'[a-z]{2}', t): return True
    return False

JUNK=[]; PBLOG=[]
def stream(fn, a, b, src):
    L = open(SRC + fn, encoding='utf-8').read().split('\n')
    if src == 'a':
        LB = open(SRC + 'b.txt', encoding='utf-8').read().split('\n')
        L2 = L[:3318] + ['', ''] + LB[3869:3900] + ['', ''] + L[3365:]
        L = L2[:1365] + ['', 'GAPSTART'] + LB[1634:1714] + ['GAPEND', ''] + L2[1426:]
        b = b - (1426-1365) + 80 + 4 - (3365-3318) + 31 + 4
    L = L[a-1:b]
    toks = []  # list of (tok, lineinfo)
    blanks = 0; junkseen = False; prevline = ''
    for n, s in enumerate(L, a):
        t = fixline(s, src)
        if t and is_junk(t): JUNK.append((src, n, t))
        if not t or is_junk(t):
            if not t: blanks += 1
            else: junkseen = True
            continue
        if (blanks or junkseen) and toks:
            if blanks >= 2 or junkseen:
                if len(prevline) < 44 or (re.search(r'[\.\?\!][”"’]?$', prevline) and re.match(r'[“"\'‘]?[A-Z\\]', t)):
                    toks.append(('¶', n))
                    if re.search(r'[a-z,;]$', prevline): PBLOG.append((src, n, 'short-no-punct', prevline))
                elif re.search(r'[\.\?\!:”"’]$', prevline):
                    PBLOG.append((src, n, 'long-punct-joined', prevline))
            else:
                toks.append(('¶', n))
        blanks = 0; junkseen = False
        prevline = t
        for w in t.split(' '):
            toks.append((w, n))
        toks[-1] = (toks[-1][0] + '\n', toks[-1][1])  # mark line end
    # join hyphenations / attach empty-key tokens
    out = []
    i = 0
    while i < len(toks):
        w, n = toks[i]
        if w.endswith('-\n') and len(w) > 2:
            # find next real token (skip ¶)
            j = i + 1
            while j < len(toks) and toks[j][0] == '¶': j += 1
            if j < len(toks):
                w = w[:-2] + '­' + toks[j][0]
                i = j
                toks[i] = (w, n)
                continue
        w = w.rstrip('\n')
        if w != '¶' and key(w) == '' and out and out[-1][0] != '¶' and not re.fullmatch(r'[—\-]+', w) and not re.fullmatch(r'[“"‘\'\(]+', w):
            out[-1] = (out[-1][0] + w, out[-1][1])
        else:
            out.append((w, n))
        i += 1
    return out

A = stream('a.txt', 130, 3730, 'a')
B = stream('b.txt', 256, 4309, 'b')
ka = [key(w) if w != '¶' else '¶' for w, _ in A]
kb = [key(w) if w != '¶' else '¶' for w, _ in B]
sm = difflib.SequenceMatcher(None, ka, kb, autojunk=False)
res = []  # tokens
flags = []
def ok(seq):
    return all(freq(key(w)) >= 2 for w, _ in seq if w != '¶')
for op, i1, i2, j1, j2 in sm.get_opcodes():
    sa, sb = A[i1:i2], B[j1:j2]
    if op == 'equal':
        for (wa, na), (wb, nb) in zip(sa, sb):
            res.append([wa, na, nb, ''])
        continue
    # paragraph-break-only differences
    sa_np = [x for x in sa if x[0] != '¶']; sb_np = [x for x in sb if x[0] != '¶']
    if [key(w) for w, _ in sa_np] == [key(w) for w, _ in sb_np]:
        # break disagreement: drop breaks (flag)
        for (wa, na), (wb, nb) in zip(sa_np, sb_np):
            res.append([wa, na, nb, ''])
        if sa != sa_np or sb != sb_np:
            res.append(['¶?', sa[0][1] if sa else None, sb[0][1] if sb else None, 'BRK a=%d b=%d' % (len(sa)-len(sa_np), len(sb)-len(sb_np))])
        continue
    oka, okb = ok(sa_np), ok(sb_np)
    ta = ' '.join(w for w, _ in sa); tb = ' '.join(w for w, _ in sb)
    na = sa[0][1] if sa else (A[i1-1][1] if i1 else None)
    nb = sb[0][1] if sb else (B[j1-1][1] if j1 else None)
    prevk = ka[i1-1] if i1 else ''
    nextk = ka[i2] if i2 < len(ka) else ''
    def score(seq):
        ks = [key(w) for w, _ in seq if w != '¶']
        if not ks: return None
        sc = sum(math.log(1 + plaus(k)) for k in ks) / len(ks)
        sc += 0.7 * math.log(1 + bg(prevk, ks[0])) + 0.7 * math.log(1 + bg(ks[-1], nextk))
        for x, y in zip(ks, ks[1:]):
            sc += 0.3 * math.log(1 + bg(x, y))
        return sc
    scA, scB = score(sa_np), score(sb_np)
    if scA is None or scB is None:
        choice = sa; tag = 'A-ONLY' if scB is None else 'B-INS'
        if scB is None and all(len(key(w)) == 0 for w, _ in sa_np): tag = 'A-PUNCT'
    elif scA >= scB:
        choice = sa; tag = 'A' if scA - scB > 1.5 else 'A?'
    else:
        choice = sb; tag = 'B' if scB - scA > 1.5 else 'B?'
    if scA is not None and scB is not None and plaus(key(' '.join(w for w,_ in choice if w!='¶'))) == 0 and len(choice) == 1:
        tag += '!'
    first = True
    for w, n in choice:
        if w == '¶':
            res.append(['¶?', n, None, 'BRK in-repl'])
            continue
        res.append([w, na, nb, ('%s|%s|%s' % (tag, ta, tb)) if first else 'cont'])
        first = False
    if not choice:
        res.append(['', na, nb, '%s|%s|%s' % (tag, ta, tb)])

json.dump(res, open(W + 'work1/merged2.json', 'w'), ensure_ascii=False)
c = Counter(r[3].split('|')[0] for r in res if r[3] and r[3] != 'cont')
print(c)
open(W+'work1/pblog.txt','w').write('\n'.join('%s %d %s | %s'%x for x in PBLOG))
open(W+'work1/junk.txt','w').write('\n'.join('%s %d %s'%x for x in JUNK))
