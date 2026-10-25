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
    if re.search(r'(y|t)o[uo][rbe]?\s+f[oe][rbe]+c', low) and len(t) < 50: return True
    if re.search(r'^\d*\s*(f[oe][rbe]+w[oq][rbe]+d)\s*\d*$', low): return True
    if len(t) <= 4 and not re.search(r'[a-z]{2}', t): return True
    return False

def stream(fn, a, b, src):
    L = open(SRC + fn, encoding='utf-8').read().split('\n')[a-1:b]
    toks = []  # list of (tok, lineinfo)
    pend_break = False
    for n, s in enumerate(L, a):
        t = fixline(s, src)
        if not t or is_junk(t):
            pend_break = True if (not t) else pend_break
            continue
        if pend_break and toks:
            toks.append(('¶', n))
        pend_break = False
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
    if oka and not okb:
        choice, tag = sa, 'A'
    elif okb and not oka:
        choice, tag = sb, 'B'
    elif oka and okb:
        choice, tag = sa, 'CONFLICT'
    else:
        choice, tag = sa, 'BOTHBAD'
    if not sa_np and sb_np and tag == 'B' and op == 'insert':
        tag = 'B-INS'
    if sa_np and not sb_np and op == 'delete':
        tag = 'A-ONLY' if tag != 'A' else 'A-ONLY'
    first = True
    for w, n in choice:
        if w == '¶':
            res.append(['¶?', n, None, 'BRK in-repl'])
            continue
        res.append([w, na, nb, ('%s|%s|%s' % (tag, ta, tb)) if first else 'cont'])
        first = False
    if not choice:
        res.append(['', na, nb, '%s|%s|%s' % (tag, ta, tb)])

json.dump(res, open(W + 'work1/merged.json', 'w'), ensure_ascii=False)
c = Counter(r[3].split('|')[0] for r in res if r[3] and r[3] != 'cont')
print(c)
