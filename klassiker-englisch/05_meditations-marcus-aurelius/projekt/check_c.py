import re,sys
base='/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/marcus/book/text/'
norm=lambda s:re.sub(r'\s+',' ',s).strip()
t=open(base+'original.md').read()
parts=re.split(r'^## (.+)$',t,flags=re.M)
books={parts[i].strip():norm(parts[i+1]) for i in range(1,len(parts),2)}
f=sys.argv[1] if len(sys.argv)>1 else base+'thirty_days.md'
lines=open(f).read().split('\n')
miss=n=0
for i,l in enumerate(lines):
    if l.startswith('>'):
        q=norm(l.lstrip('>'))
        src=None
        for l2 in lines[i+1:i+4]:
            m=re.match(r'Source:\s*(.+)',l2.strip())
            if m: src=m.group(1).strip(); break
        n+=1
        if src not in books: print('BAD SOURCE',i+1,src,q[:60]); miss+=1
        elif q not in books[src]: print('MISS',i+1,src,q[:80]); miss+=1
days=re.findall(r'^### Day (\d+) – ',open(f).read(),flags=re.M)
print(f'quotes={n} misses={miss} days={len(days)}')
