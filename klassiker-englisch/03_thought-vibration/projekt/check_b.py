import re,sys
base='/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/book/text/'
norm=lambda s: re.sub(r'\s+',' ',s.replace('*','').replace('\\','')).strip()
orig=open(base+'original.md').read()
o=norm(orig)
text=open(base+'chapters_b.md').read()
miss=0
for q in re.findall(r'^> (.+)$',text,re.M):
    if norm(q) not in o: miss+=1; print('MISS:',q)
titles=re.findall(r'^## (.+)$',text,re.M)
ot=re.findall(r'^## (.+)$',orig,re.M)
exp=ot[ot.index('Asserting the Life-Force'):]
print('titles ok' if titles==exp else ('TITLE MISMATCH',titles))
# word counts
for sec in re.split(r'^## ',text,flags=re.M)[1:]:
    t=sec.split('\n')[0]
    parts=re.split(r'^### ',sec,flags=re.M)
    wc={p.split('\n')[0]:len(p.split('\n',1)[1].split()) for p in parts[1:]}
    print(t,wc)
print('misses:',miss)
