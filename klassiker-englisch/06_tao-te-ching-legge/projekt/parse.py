import re
t=open('src/t.txt',encoding='utf-8').read()
body=t[t.index('PART 1.'):t.index('*** END OF THE PROJECT')].replace('PART 1.','').replace('PART II.','')
paras=[]; cur=[]
for l in body.split('\n'):
    if not l.strip():
        if cur: paras.append(cur); cur=[]
    else: cur.append(l.rstrip())
if cur: paras.append(cur)
chapters={}; ch=0; v=0; amb=[]
for p in paras:
    first=p[0].strip()
    m1=re.match(r'^(\d+)\. (\d+)\.\s*(.*)$',first)
    m2=re.match(r'^(\d+)\.\s*$',first)
    m3=re.match(r'^(\d+)\.\s+(.*)$',first)
    newch=False
    if m1 and int(m1.group(1))==ch+1:
        ch+=1; newch=True; v=int(m1.group(2)); p=[f'{m1.group(2)}. {m1.group(3)}'.rstrip()]+p[1:]
    elif m2 and int(m2.group(1))==ch+1 and int(m2.group(1))!=v+1:
        ch+=1; newch=True; v=0; p=p[1:]
    elif m3 and int(m3.group(1))==ch+1 and int(m3.group(1))!=v+1:
        ch+=1; newch=True; v=0; p=[m3.group(2)]+p[1:]
    else:
        if (m2 or m3) and int((m2 or m3).group(1))==ch+1: amb.append((ch,first[:40]))
        if m2: v=int(m2.group(1))
        elif m3: v=int(m3.group(1))
    if newch: chapters[ch]=[]
    if not p or ch==0: continue
    prose=[l for l in p if not l.startswith('  ')]; vs=[l for l in p if l.startswith('  ')]
    if prose: chapters[ch].append(' '.join(x.strip() for x in prose))
    if vs: chapters[ch].append('\n'.join('| '+l.strip() for l in vs))
print(len(chapters), [n for n in range(1,82) if n not in chapters], 'ambiguous:', amb)
out=[]
for n in sorted(chapters):
    blocks=[re.sub(r'  +',' ',b) for b in chapters[n]]
    out.append(f'## Chapter {n}\n\n'+'\n\n'.join(blocks))
open('book/text/original.md','w',encoding='utf-8').write('\n\n'.join(out)+'\n')
