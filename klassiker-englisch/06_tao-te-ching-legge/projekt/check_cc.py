import re,sys
B='book/text/'
def split(t):
    d={};cur=None
    for l in t.split('\n'):
        m=re.match(r'^## Chapter (\d+)\s*$',l)
        if m: cur=int(m.group(1)); d[cur]=[]; continue
        if cur: d[cur].append(l)
    return d
norm=lambda s:re.sub(r'\s+',' ',s).strip()
orig={k:norm(' '.join(l[2:] if l.startswith('| ') else l for l in v)) for k,v in split(open(B+'original.md').read()).items()}
mine=split(open(B+'chapters_c.md').read())
miss=0
exp=list(range(55,82))
if sorted(mine)!=exp or list(mine)!=exp: print('CHAPTER SET/ORDER WRONG',list(mine)); miss+=1
wc=lambda s:len(re.findall(r"[A-Za-z0-9'’-]+",s))
for n,lines in mine.items():
    txt='\n'.join(lines)
    secs=re.split(r'^### (.+)$',txt,flags=re.M)
    names=secs[1::2]; bodies=secs[2::2]
    if names!=['Reflection','Practice','Key Line']: print(n,'BAD SECTIONS',names); miss+=1; continue
    r,p,k=wc(bodies[0]),wc(bodies[1]),bodies[2]
    if not 70<=r<=140: print(n,'reflection words',r); miss+=1
    if not 25<=p<=60: print(n,'practice words',p); miss+=1
    q=norm(' '.join(l[1:] for l in k.strip().split('\n') if l.startswith('>')))
    if not q or q not in orig[n]: print(n,'QUOTE MISS:',q); miss+=1
    print(n,'R',r,'P',p)
print('misses:',miss)
