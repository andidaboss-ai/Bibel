import re
W = '/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/larson/'
t = open(W + 'work1/d3.txt').read()
t = t.replace('truth. ⟦BRK?⟧ You may think', 'truth.\n\nYou may think')
assert '⟦' not in t, re.findall(r'.{50}⟦.{50}', t)
t = t.replace('­', '')

titles = {
 'I': 'The Ruling Principle in Man', 'II': 'How We Govern the Forces We Possess',
 'm': 'The Use of Mind in Practical Action', 'III': 'The Use of Mind in Practical Action',
 'IV': 'The Forces of the Subconscious', 'V': 'Training the Subconscious for Special Results',
 'VI': 'The Power of Subjective Thought', 'Vn': 'How Man Becomes What He Thinks', 'VII': 'How Man Becomes What He Thinks',
}
def chap(m):
    return '## ' + titles[m.group(1)]
t = re.sub(r'CHAPTER (\w+)\n\n[A-Z ,\.n]+(?=\n)', chap, t)
t = t.replace('PROMISE YOURSELF', '## Promise Yourself')
t = '## Foreword\n\n' + t.lstrip()

paras = t.split('\n\n')
# chapter-end mottos (boxed italic pages in the 1912 printing)
motto_starts = [
 'Man is ever in search of strength.',
 'Man lives to move forward.',
 'When you think of yourself do not think',
 'THE PATH TO GREATER THINGS',
 'When you have made up your mind what you want',
 'Life is growth and the object',
 'The greatest remedy in the world is change',
]
out = []
in_motto = False
for p in paras:
    p = p.strip()
    if p.startswith('## '):
        in_motto = False
        out.append(p); continue
    if any(p.startswith(m) for m in motto_starts):
        in_motto = True
        if p == 'THE PATH TO GREATER THINGS':
            out.append('### The Path to Greater Things'); continue
    if in_motto:
        p = '*' + p + '*'
    out.append(p)
t = '\n\n'.join(out) + '\n'

# typography
t = re.sub(r'\s*—\s*', '—', t)
t = t.replace('develop further - those', 'develop further those').replace('interesting-something', 'interesting—something')
t = re.sub(r'(^|[\s\(—])"', r'\1“', t, flags=re.M)
t = t.replace('"', '”')
t = re.sub(r"(^|[\s\(—“])'", r'\1‘', t, flags=re.M)
t = t.replace("'", '’')
t = re.sub(r'[ \t]+', ' ', t)
t = re.sub(r' ([,;:\.\?\!])', r'\1', t)
for a, b in [('accumulate in. your', 'accumulate in your'), ('subconscious,, does', 'subconscious, does'),
             ('my days,*’', 'my days,”'), ('would change. their tactics', 'would change their tactics'),
             ('you are’ tired', 'you are tired'), ('dies until’ he', 'dies until he'), ('goal w’e have', 'goal we have'),
             ('A’ number', 'A number'), ('it w’ill', 'it will'), ('but think’ of', 'but think of'), ('you w’ish', 'you wish'),
             ('and’ not', 'and not'), ('is, “ The', 'is, “The'), ('those lines,, it', 'those lines, it'),
             ('completely.. The', 'completely. The'), ('your powers.. Give', 'your powers. Give'),
             ('the.majority', 'the majority'), ('mind.should', 'mind should'), ('any.silver', 'any silver'), ('your.conception', 'your conception')]:
    assert a in t, a
    t = t.replace(a, b)
open(W + 'part1.md', 'w').write(t)
print(len(t.split()))
