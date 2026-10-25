import re, sys
base = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/mulford/book/text/'
def norm(s):
    return re.sub(r'\s+', ' ', s.replace('*', '')).strip()
orig = norm(open(base + 'original.md').read())
titles = set(l[3:].strip() for l in open(base + 'original.md') if l.startswith('## '))
miss = 0; n = 0
for line in open(base + 'thirty_days.md'):
    if line.startswith('> '):
        n += 1
        q = norm(line[2:])
        if q not in orig:
            miss += 1; print('MISS:', q)
    if line.startswith('Source: '):
        t = line[8:].strip()
        if t not in titles:
            miss += 1; print('BAD SOURCE:', t)
print(f'{n} quotes, {miss} misses')
