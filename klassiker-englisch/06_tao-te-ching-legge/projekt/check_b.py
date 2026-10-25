import re,sys
D='/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/tao/book/text/'
def split(t):
    parts=re.split(r'^## Chapter (\d+)\s*$',t,flags=re.M)
    return {int(parts[i]):parts[i+1] for i in range(1,len(parts),2)}
norm=lambda s:re.sub(r'\s+',' ',s).strip()
orig={k:norm(re.sub(r'^\| ','',v,flags=re.M)) for k,v in split(open(D+'original.md').read()).items()}
ch=split(open(D+'chapters_b.md').read())
bad=0
exp=list(range(28,55))
if sorted(ch)!=exp: print('chapter set wrong',sorted(ch)); bad+=1
for n,body in ch.items():
    secs=re.split(r'^### (Reflection|Practice|Key Line)\s*$',body,flags=re.M)
    names=secs[1::2]
    if names!=['Reflection','Practice','Key Line']: print(n,'sections',names); bad+=1; continue
    r,p,k=[s.strip() for s in secs[2::2]]
    wr,wp=len(r.split()),len(p.split())
    if not 70<=wr<=140: print(n,'reflection words',wr); bad+=1
    if not 25<=wp<=60: print(n,'practice words',wp); bad+=1
    q=norm(' '.join(l[1:].strip() for l in k.splitlines() if l.startswith('>')))
    if not q or q not in orig[n]: print(n,'QUOTE MISS:',q); bad+=1
    print(n,wr,wp,'ok' if q in orig[n] else 'MISS')
print('problems:',bad)
