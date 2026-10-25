import re, sys, os
d = os.path.dirname(os.path.abspath(__file__))
orig = open(os.path.join(d, 'original.md'), encoding='utf-8').read()
misses = total = 0
for fn in ['chapters.md', 'thirty_days.md']:
    for i, line in enumerate(open(os.path.join(d, fn), encoding='utf-8'), 1):
        if line.startswith('>'):
            q = line[1:].strip()
            total += 1
            if q not in orig:
                misses += 1
                print(f'MISS {fn}:{i}: {q}')
# chapter title order check
ot = re.findall(r'^## (.+)$', orig, re.M)
ct = re.findall(r'^## (.+)$', open(os.path.join(d, 'chapters.md'), encoding='utf-8').read(), re.M)
print('titles match:', ot == ct, len(ot), len(ct))
print(f'{total} quotes checked, {misses} misses')
sys.exit(1 if misses else 0)
