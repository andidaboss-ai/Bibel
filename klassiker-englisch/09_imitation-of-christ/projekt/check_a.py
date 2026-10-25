import re,sys
base='book/text/'
orig=open(base+'original.md',encoding='utf-8').read()
titles=[re.sub(r'^\s*\d+\s*','',l).strip() for l in open('chapter_list.txt',encoding='utf-8')][1:26]
def secs(t):
    parts=re.split(r'^(## .*)$',t,flags=re.M); d=[]
    for i in range(1,len(parts),2): d.append((parts[i].strip(),parts[i+1]))
    return d
o={}
for h,b in secs(orig): o.setdefault(h,b)
n=lambda s:re.sub(r'\s+',' ',s).strip()
a=secs(open(base+'chapters_a.md',encoding='utf-8').read())
p=[]
if [h for h,_ in a]!=titles: p.append('titles/order mismatch')
for h,b in a:
    m=re.match(r'\s*### Reflection\n(.*?)\n### Practice\n(.*?)\n### Key Line\n(.*)$',b,re.S)
    if not m: p.append(h+': structure'); continue
    r,pr,k=m.groups()
    wr,wp=len(r.split()),len(pr.split())
    if not 70<=wr<=130: p.append(f'{h}: reflection {wr}w')
    if not 20<=wp<=50: p.append(f'{h}: practice {wp}w')
    q=' '.join(l[1:].strip() for l in k.strip().splitlines() if l.startswith('>'))
    if not q: p.append(h+': no quote')
    if re.search('[¹²³⁴⁵⁶⁷⁸⁹⁰]',q): p.append(h+': superscript')
    if n(q) not in n(o.get(h,'')): p.append(f'{h}: quote miss: {q}')
    print(wr,wp,h)
print('\n'.join(p)); print(len(p),'problems')
