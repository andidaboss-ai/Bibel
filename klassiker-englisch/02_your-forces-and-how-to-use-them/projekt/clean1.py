import re, sys, json, difflib
from collections import Counter

SRC = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/src/'
OUT = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/work1/'
import os; os.makedirs(OUT, exist_ok=True)

def lines(fn, a, b):
    with open(SRC + fn, encoding='utf-8') as f:
        L = f.read().split('\n')
    return L[a-1:b]

def is_junk(s, src):
    t = s.strip()
    if not t:
        return False
    if re.fullmatch(r'[\divxlIVXL\s\.,]*\d[\d\s\.]*', t):
        return True
    low = t.lower()
    if 'googl' in low or 'coo>' in low or re.search(r'o,i,|ih,\.', low):
        return True
    # running heads: contain "forces" & "use" with garbage, short
    if re.search(r'(y|t)ou[rb]?\s+fo[rbe]+c', low) and len(t) < 50:
        return True
    if re.search(r'^\d*\s*(fo[rbe]+w[oq][rbe]+d)\s*\d*$', low):
        return True
    if len(t) <= 3 and not re.search(r'[a-z]{2}', t):
        return True
    return False

def paragraphs(L, src):
    """return list of (para_text, flags) ; page breaks noted"""
    paras = []
    cur = []
    i = 0
    gap = False; junkgap = False
    for s in L:
        t = re.sub(r'\s+', ' ', s).strip()
        if not t:
            if cur: gap = True
            continue
        if is_junk(t, src):
            if cur: junkgap = True; gap = True
            continue
        if gap and cur:
            prev = cur[-1]
            if junkgap:
                # page break: continue unless previous line short and ends sentence
                if len(prev) < 42 and re.search(r'[\.\?\!:;”"’\']$', prev):
                    paras.append(cur); cur = []
                else:
                    cur.append('<PB>')
            else:
                paras.append(cur); cur = []
        gap = False; junkgap = False
        cur.append(t)
    if cur: paras.append(cur)
    out = []
    for p in paras:
        txt = ''
        for ln in p:
            if ln == '<PB>':
                txt += ' ¶PB '
                continue
            if txt.endswith('-') and not txt.endswith('--'):
                txt = txt[:-1] + '­'  # soft marker for hyphen join
                txt += ln
            elif txt.endswith('­PB '):
                txt += ln
            else:
                txt = (txt + ' ' + ln) if txt else ln
        # hyphen across page break
        txt = re.sub(r'-\s*¶PB\s*', '­', txt)
        txt = re.sub(r'\s*¶PB\s*', ' ', txt)
        out.append(txt)
    return out

A = paragraphs(lines('a.txt', 130, 3730), 'a')
B = paragraphs(lines('b.txt', 256, 4309), 'b')
json.dump(A, open(OUT + 'A.json', 'w'), ensure_ascii=False, indent=0)
json.dump(B, open(OUT + 'B.json', 'w'), ensure_ascii=False, indent=0)
print(len(A), len(B))
