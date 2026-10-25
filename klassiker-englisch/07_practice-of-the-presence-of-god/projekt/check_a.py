import re, sys
base = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/lawrence/book/text/'
orig = open(base + 'original.md', encoding='utf-8').read()
mine = open(base + 'chapters_a.md', encoding='utf-8').read()
EXPECT = ['First Conversation', 'Second Conversation', 'Third Conversation', 'Fourth Conversation',
          'First Letter', 'Second Letter', 'Third Letter', 'Fourth Letter', 'Fifth Letter']
RANGES = {'Reflection': (80, 150), 'Practice': (25, 60)}
norm = lambda s: re.sub(r'\s+', ' ', s).strip()

def split(text, level):
    parts = re.split(r'^%s (.+)$' % ('#' * level), text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]

osec = dict(split(orig, 2))
problems = []
secs = split(mine, 2)
if [t for t, _ in secs] != EXPECT:
    problems.append('heading order: %s' % [t for t, _ in secs])
for title, body in secs:
    subs = split(body, 3)
    if [t for t, _ in subs] != ['Reflection', 'Practice', 'Key Line']:
        problems.append('%s: subheadings %s' % (title, [t for t, _ in subs]))
    for st, sb in subs:
        if st in RANGES:
            n = len(sb.split()); lo, hi = RANGES[st]
            print('%-20s %-10s %d words' % (title, st, n))
            if not lo <= n <= hi:
                problems.append('%s/%s: %d words' % (title, st, n))
        if st == 'Key Line':
            q = norm(' '.join(l[1:].strip() for l in sb.splitlines() if l.startswith('>')))
            if not q:
                problems.append('%s: no quote' % title)
            elif q not in norm(osec.get(title, '')):
                problems.append('%s: quote not found: %s' % (title, q))
    for l in body.splitlines():
        if l.startswith('>') and not any(st == 'Key Line' and l in sb for st, sb in subs):
            problems.append('%s: stray quote line %s' % (title, l))
print('\n'.join(problems))
print('%d problems' % len(problems))
sys.exit(1 if problems else 0)
