import re,sys
T='book/text/'
norm=lambda s:re.sub(r'\s+',' ',s.replace('*','')).strip()
orig=open(T+'original.md',encoding='utf-8').read()
secs={};cur=None
for line in orig.split('\n'):
    if line.startswith('## '): cur=line[3:].strip(); secs[cur]=[]
    elif cur and not line.startswith('%%'): secs[cur].append(line)
secs={k:norm('\n'.join(v)) for k,v in secs.items()}
ch=open(T+'chapters_b.md',encoding='utf-8').read()
miss=0;cur=None
for line in ch.split('\n'):
    if line.startswith('## '):
        cur=line[3:].strip()
        if cur not in secs: print('BAD TITLE',cur);miss+=1
    elif line.startswith('> '):
        q=norm(line[2:])
        if q not in secs.get(cur,''): print('MISS',cur,q);miss+=1
print('misses',miss)
