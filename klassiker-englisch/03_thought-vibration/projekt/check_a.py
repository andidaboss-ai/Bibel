import re,sys
D='/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/atkinson/book/text/'
def norm(s): return re.sub(r'\s+',' ',s.replace('*','')).strip()
def sections(t):
    out={};order=[];cur=None
    for l in t.splitlines():
        if l.startswith('## '):
            cur=l[3:].strip();order.append(cur);out[cur]=[]
        elif cur: out[cur].append(l)
    return order,out
oo,os_=sections(open(D+'original.md').read())
co,cs=sections(open(D+'chapters_a.md').read())
exp=oo[2:11]
print('titles match:',co==exp)
miss=0
for t in co:
    body=norm('\n'.join(l for l in os_.get(t,[]) if not l.startswith('%%')))
    txt='\n'.join(cs[t])
    for q in re.findall(r'^> (.+)$',txt,re.M):
        ok=norm(q) in body
        if not ok: miss+=1
        print('OK ' if ok else 'MISS',t,'|',q[:60])
    parts=re.split(r'^### ',txt,flags=re.M)
    print('   words:',{p.split('\n')[0]:len(re.findall(r"[\w’'-]+",p.split('\n',1)[1])) for p in parts[1:]})
print('misses:',miss)
