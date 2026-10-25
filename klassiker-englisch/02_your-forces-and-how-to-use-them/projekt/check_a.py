import re, sys
base = sys.argv[1] if len(sys.argv) > 1 else 'book/text'
orig = open(f'{base}/original.md', encoding='utf-8').read()
ann = open(f'{base}/chapters_a.md', encoding='utf-8').read()
ws = lambda s: re.sub(r'\s+', ' ', s).strip()
def sections(t):
    parts = re.split(r'^## (.+)$', t, flags=re.M)
    return [(parts[i].strip(), parts[i+1]) for i in range(1, len(parts), 2)]
osec = dict(sections(orig))
otitles = [k for k, _ in sections(orig)]
expected = otitles[otitles.index('Promise Yourself'):otitles.index('How We Secure What We Persistently Desire') + 1]
asec = sections(ann)
miss = 0
if [k for k, _ in asec] != expected:
    print('TITLE MISMATCH', [k for k, _ in asec]); miss += 1
for title, body in asec:
    src = ws(osec.get(title, '').replace('*', ''))
    sub = dict((m[0], m[1]) for m in re.findall(r'^### (.+?)\n(.*?)(?=^### |\Z)', body, flags=re.M | re.S))
    wc = {k: len(re.findall(r"[A-Za-z0-9'’-]+", v)) for k, v in sub.items()}
    quotes = [ws(q) for q in re.findall(r'^> (.+)$', body, flags=re.M)]
    for q in quotes:
        if q not in src:
            print('MISS', title, '|', q); miss += 1
    # inline "..." quotes in Reflection
    for q in re.findall(r'"([^"]+)"', sub.get('Reflection', '')):
        if ws(q) not in src and ws(q).rstrip('.,') not in src:
            print('  inline (not verbatim, check):', title, '|', q)
    print(f'{title}: R={wc.get("Reflection")} P={wc.get("Practice")} quotes={len(quotes)}')
print('misses:', miss)
