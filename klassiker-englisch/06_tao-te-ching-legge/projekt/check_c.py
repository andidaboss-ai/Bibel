import re,sys
T='book/text/'
o=open(T+'original.md',encoding='utf-8').read()
norm=lambda s:re.sub(r'\s+',' ',s).strip()
ch={}
for blk in re.split(r'^## Chapter ',o,flags=re.M)[1:]:
    n,b=blk.split('\n',1)
    b=re.sub(r'^\| ?','',b,flags=re.M)
    ch[int(n)]=norm(b)
d=open(T+'thirty_days.md',encoding='utf-8').read()
days=re.split(r'^### ',d,flags=re.M)[1:]
miss=0
print('days:',len(days))
for i,s in enumerate(days,1):
    t=s.split('\n',1)[0]
    if not t.startswith(f'Day {i} – '): print('BAD TITLE',t); miss+=1
    q=[l[2:] for l in s.split('\n') if l.startswith('> ')]
    m=re.search(r'^Source: Chapter (\d+)\s*$',s,flags=re.M)
    if len(q)!=1 or not m: print('FORMAT',t); miss+=1; continue
    q=norm(q[0]); n=int(m.group(1))
    if q not in ch[n]: print('MISS',t,n,q); miss+=1
    if len(q.split())>40: print('LONG',t,len(q.split()))
    task=s.split(m.group(0),1)[1].strip()
    ns=len(re.findall(r'[.!?](\s|$)',task))
    if not 2<=ns<=4: print('SENTENCES',t,ns)
intro=re.split(r'^### ',d,flags=re.M)[0].split('\n',1)[1]
print('intro words',len(intro.split()))
print('misses',miss)
